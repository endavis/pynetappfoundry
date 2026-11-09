"""Metadata collector for ONTAP clusters.

Collects cluster metadata using REST API with all-or-nothing semantics.
Collection either succeeds completely or fails entirely — no partial
cache updates. Cloud metadata (CLI-only) is optional; all other phases
are API-only and must succeed.

``MetadataCollector`` is assembled from mixins in private sibling modules:
``_collector_api`` (API phases and the cached API call), ``_collector_cloud``
(cloud metadata), ``_collector_runner`` (phase and task runners),
``_collector_cli`` (SSH helpers) and ``_collector_progress`` (progress types).
"""

from __future__ import annotations

import threading
import time
from collections.abc import Callable
from concurrent.futures import Future
from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any, ClassVar

from pynetappfoundry.cache._collector_api import ApiPhasesMixin
from pynetappfoundry.cache._collector_base import logger
from pynetappfoundry.cache._collector_cli import SshPreconnect, connect_early
from pynetappfoundry.cache._collector_cloud import CloudPhaseMixin
from pynetappfoundry.cache._collector_progress import (
    PHASE_NAMES,
    CollectionPhase,
    ProgressCallback,
    ProgressInfo,
    report_progress,
)
from pynetappfoundry.cache._collector_runner import (
    DEFAULT_MAX_WORKERS,
    CollectionError,
    PhaseRunner,
    PhaseTask,
    run_phase_safe,
)
from pynetappfoundry.cache._metadata import CachedClusterMetadata
from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.models.ontap.cluster.model import ClusterInfo

if TYPE_CHECKING:
    from pynetappfoundry.clients.ontap.api import ONTAPAPIClient
    from pynetappfoundry.clients.ontap.cli import ONTAPCLI

__all__ = [
    "CollectionError",
    "CollectionPhase",
    "MetadataCollector",
    "ProgressCallback",
    "ProgressInfo",
]


class MetadataCollector(ApiPhasesMixin, CloudPhaseMixin):
    """Collects cluster metadata from ONTAP via API and CLI.

    Uses REST API for all collection phases (all-or-nothing). Cloud
    metadata is CLI-only and optional — failure warns but doesn't abort.
    """

    # Human-readable names for collection phases
    PHASE_NAMES: ClassVar[dict[CollectionPhase, str]] = PHASE_NAMES

    # Maps TypeMapping registry names to results dict keys for derived field evaluation.
    # Only TypeMappings that have derived fields need to be listed here.
    _MAPPING_RESULTS_KEYS: ClassVar[list[tuple[str, str]]] = [
        ("Cluster", "cluster"),
        ("OntapNodeResponse", "nodes"),
    ]

    def __init__(
        self,
        api_client: ONTAPAPIClient | None = None,
        cli_client: ONTAPCLI | None = None,
        progress_callback: ProgressCallback | None = None,
        aws_sso_config: dict[str, str | dict[str, str]] | None = None,
        parallel: bool = True,
        max_workers: int = DEFAULT_MAX_WORKERS,
    ) -> None:
        """Initialize the metadata collector.

        Args:
            api_client: ONTAP REST API client.
            cli_client: ONTAP CLI (SSH) client.
            progress_callback: Optional callback for progress updates.
            aws_sso_config: Optional AWS SSO configuration with:
                - 'subdomain': SSO portal subdomain (e.g., 'mycompany')
                - 'account_roles': dict mapping account_id to role_name
            parallel: Whether to run API calls in parallel. Default True.
            max_workers: Maximum number of parallel workers. Default 8 (``DEFAULT_MAX_WORKERS``).
        """
        self.api_client = api_client
        self.cli_client = cli_client
        self.progress_callback = progress_callback
        self.aws_sso_config = aws_sso_config
        self.parallel = parallel
        self.max_workers = max_workers

        # Cluster name for logging context (set during collect_all)
        self._cluster_name: str = ""

        # API response cache to avoid duplicate calls within a collection run
        self._api_cache: dict[str, Any] = {}
        self._cache_lock = threading.Lock()
        # In-flight API calls by cache key, so concurrent callers share one request
        self._inflight: dict[str, Future[Any]] = {}

        # Background SSH pre-connect for the current parallel run (CVO clusters
        # wait on it before the CLI call)
        self._ssh_preconnect: SshPreconnect | None = None

        # Cross-phase results cache used by fetch() to short-circuit
        # post-collection hooks (e.g. compute_is_ha looking up "OntapNodeResponse").
        # Populated by phase methods as they complete; consulted by
        # subsequent fetch() calls.
        self._results_cache: dict[str, Any] = {}

        # Phase results memoized by collect_group(), keyed by phase value, so
        # a dependency (e.g. nodes for cluster and cloud) is collected once.
        self._group_results: dict[str, Any] = {}

    def _report_progress(
        self,
        phase: CollectionPhase,
        status: str,
        elapsed_seconds: float = 0.0,
        error: str | None = None,
        source: str | None = None,
    ) -> None:
        """Report progress to callback if configured.

        Args:
            phase: The collection phase.
            status: Status string ("starting", "completed", "failed").
            elapsed_seconds: Time taken for this phase.
            error: Error message if failed.
            source: Data source used ("api", "cli").
        """
        report_progress(
            self.progress_callback,
            phase,
            status,
            elapsed_seconds,
            error,
            source,
            self.PHASE_NAMES,
        )

    def _evaluate_derived_fields(self, results: dict[str, Any]) -> dict[str, Any]:
        """Evaluate derived fields across all TypeMappings that declare them.

        Iterates ``_MAPPING_RESULTS_KEYS``, looks up each TypeMapping from
        the model registry, and for any that have ``derived_fields()``,
        calls each field's ``post_collection(item, results)`` on every item
        in the results dict.

        Handles both singular results (e.g. ``ClusterInfo``) and list results
        (e.g. ``list[OntapNodeResponse]``).

        Args:
            results: The full collection results dict keyed by phase name.

        Returns:
            Updated results dict with derived fields evaluated.
        """
        # Alias phase-keyed entries under their canonical ``dep_class.__name__``
        # key so post-collection hooks (which read ``results`` as their context
        # dict) find dependencies under the canonical name consistent with
        # ``fetchers.fetch()``. See ADR-0013 §5.
        for mapping_name, results_key in self._MAPPING_RESULTS_KEYS:
            if results_key in results and mapping_name != results_key:
                results[mapping_name] = results[results_key]

        for mapping_name, results_key in self._MAPPING_RESULTS_KEYS:
            if results_key not in results:
                continue

            mapping = model_registry.get_mapping(mapping_name)
            if mapping is None:
                continue

            derived = mapping.derived_fields()
            if not derived:
                continue

            result = results[results_key]
            is_list = isinstance(result, list)
            items = result if is_list else [result]

            for field in derived:
                if field.post_collection is None:
                    continue
                try:
                    items = [field.post_collection(item, results) for item in items]
                except Exception:
                    logger.error(
                        "%s DERIVED_FIELD_FAILURE: %s.%s - post_collection error",
                        self._log_prefix,
                        mapping_name,
                        field.cache_attr,
                    )
                    raise

            results[results_key] = items if is_list else items[0]

        return results

    def collect_all(self, cluster_name: str) -> CachedClusterMetadata:
        """Collect all metadata categories for a cluster.

        Uses parallel execution for API calls to improve performance.
        SSH connection for cloud metadata is started early in background.

        Args:
            cluster_name: Name of the cluster being collected.

        Returns:
            Complete CachedClusterMetadata object.
        """
        # Set cluster name for logging context
        self._cluster_name = cluster_name
        logger.info("%s Starting metadata collection", self._log_prefix)
        total_start = time.monotonic()

        # Clear cache from any previous run
        self._clear_cache()
        self._results_cache = {}

        if self.parallel:
            results = self._collect_all_parallel(cluster_name)
        else:
            results = self._collect_all_sequential(cluster_name)

        total_elapsed = time.monotonic() - total_start
        logger.info("%s Completed metadata collection in %.2fs", self._log_prefix, total_elapsed)

        # Evaluate derived fields (e.g. is_ha from node count)
        results = self._evaluate_derived_fields(results)
        cluster_info: ClusterInfo = results["cluster"]

        # Collect parameterized endpoints (requires parent objects from phases)
        results["storage"] = self._with_svm_top_metrics_users(results["storage"])

        # Post-process Azure cloud metadata to fix instance links
        cloud_metadata = self._update_azure_cloud_links(
            results["cloud"],
            cluster_name,
            cluster_info.is_ha,
        )

        return CachedClusterMetadata(
            cluster_name=cluster_name,
            cached_at=datetime.now(UTC),
            cloud=cloud_metadata,
            cluster=cluster_info,
            nodes=results["nodes"],
            network=results["network"],
            storage=results["storage"],
            license_packages=results["licenses"],
            mediator=results["mediator"],
            relationships=results["relationships"],
            protocols=results["protocols"],
        )

    # -------------------------------------------------------------------------
    # Single field-group collection (live ClusterEntry.ontap, #869)
    # -------------------------------------------------------------------------

    def collect_group(self, cluster_name: str, group: str) -> Any:
        """Collect one ``CachedClusterMetadata`` field group live.

        Returns the value :meth:`collect_all` would put in *group*, with the
        same post-processing, but runs only the phases that group needs:
        ``cluster`` also collects ``nodes`` (for the derived ``is_ha`` and
        ``is_cloud``), ``cloud`` also collects ``nodes`` and ``cluster`` (CVO
        detection and Azure links), and ``storage`` adds its
        ``svm_top_metrics_users``. Phase results are memoized on this
        collector, so a shared dependency is collected once.

        ``console`` is not collected by :meth:`collect_all` either, so it
        returns ``None`` and the caller falls back to the field default.

        Args:
            cluster_name: Name of the cluster being collected.
            group: A ``CachedClusterMetadata`` data field name.

        Returns:
            The collected field-group value, or ``None`` for ``console``.

        Raises:
            ValueError: If *group* is not a ``CachedClusterMetadata`` data field.
        """
        self._cluster_name = cluster_name
        if group == "console":
            return None
        if group == "cluster":
            # Nodes first: collect_nodes() fills _results_cache, so the
            # cluster mapping's is_ha/is_cloud hooks reuse them instead of
            # fetching nodes again.
            nodes = self._collect_phase(CollectionPhase.NODES)
            results = {"cluster": self._collect_phase(CollectionPhase.CLUSTER), "nodes": nodes}
            return self._evaluate_derived_fields(results)["cluster"]
        if group == "cloud":
            self._collect_phase(CollectionPhase.NODES)  # CVO detection reads these
            cluster_info: ClusterInfo = self.collect_group(cluster_name, "cluster")
            return self._update_azure_cloud_links(
                self._collect_phase(CollectionPhase.CLOUD), cluster_name, cluster_info.is_ha
            )
        if group == "storage":
            return self._with_svm_top_metrics_users(self._collect_phase(CollectionPhase.STORAGE))
        phase = self._GROUP_PHASES.get(group)
        if phase is None:
            raise ValueError(f"Unknown CachedClusterMetadata field group: {group!r}")
        return self._collect_phase(phase)

    # Field groups that map one-to-one onto a phase; the rest are handled in
    # collect_group() because they depend on another phase.
    _GROUP_PHASES: ClassVar[dict[str, CollectionPhase]] = {
        "nodes": CollectionPhase.NODES,
        "network": CollectionPhase.NETWORK,
        "license_packages": CollectionPhase.LICENSES,
        "mediator": CollectionPhase.MEDIATOR,
        "relationships": CollectionPhase.RELATIONSHIPS,
        "protocols": CollectionPhase.PROTOCOLS,
    }

    def _collect_phase(self, phase: CollectionPhase) -> Any:
        """Run *phase* once per collector and return its memoized result."""
        if phase.value not in self._group_results:
            methods: dict[CollectionPhase, Callable[[], Any]] = {
                CollectionPhase.CLUSTER: self.collect_cluster_info,
                CollectionPhase.NODES: self.collect_nodes,
                CollectionPhase.CLOUD: self.collect_cloud_metadata,
                CollectionPhase.NETWORK: self.collect_network,
                CollectionPhase.STORAGE: self.collect_storage,
                CollectionPhase.LICENSES: self.collect_licenses,
                CollectionPhase.MEDIATOR: self.collect_mediator,
                CollectionPhase.RELATIONSHIPS: self.collect_relationships,
                CollectionPhase.PROTOCOLS: self.collect_protocols,
            }
            logger.debug("%s Collecting %s (single group)", self._log_prefix, phase.value)
            self._group_results[phase.value] = methods[phase]()
        return self._group_results[phase.value]

    def _phase_runner(self) -> PhaseRunner:
        return PhaseRunner(
            report=self._report_progress,
            determine_source=self._determine_source,
            log_prefix=self._log_prefix,
        )

    def _collect_all_sequential(self, cluster_name: str) -> dict[str, Any]:
        """Collect all metadata sequentially (original behavior).

        Args:
            cluster_name: Name of the cluster being collected.

        Returns:
            Dictionary of collection results keyed by phase name.
        """
        self._ssh_preconnect = None
        phases: list[PhaseTask] = [
            (CollectionPhase.CLUSTER, self.collect_cluster_info),
            (CollectionPhase.NODES, self.collect_nodes),
            # CLOUD must run after NODES so _results_cache["OntapNodeResponse"]
            # is populated before CVO detection in collect_cloud_metadata().
            (CollectionPhase.CLOUD, self.collect_cloud_metadata),
            (CollectionPhase.NETWORK, self.collect_network),
            (CollectionPhase.STORAGE, self.collect_storage),
            (CollectionPhase.LICENSES, self.collect_licenses),
            (CollectionPhase.MEDIATOR, self.collect_mediator),
            (CollectionPhase.RELATIONSHIPS, self.collect_relationships),
            (CollectionPhase.PROTOCOLS, self.collect_protocols),
        ]
        return self._phase_runner().run_sequential(phases)

    def _collect_all_parallel(self, cluster_name: str) -> dict[str, Any]:
        """Collect all metadata in parallel for improved performance.

        Starts SSH connection early, then runs all API phases concurrently.
        CLOUD runs sequentially after the parallel block so that
        ``_results_cache["OntapNodeResponse"]`` is populated before CVO
        detection in :meth:`collect_cloud_metadata`.

        Args:
            cluster_name: Name of the cluster being collected.

        Returns:
            Dictionary of collection results keyed by phase name.
        """
        # CLOUD is excluded — it must run after NODES so that
        # _results_cache["OntapNodeResponse"] is populated before CVO
        # detection.  It runs sequentially after the parallel block.
        phases: list[PhaseTask] = [
            (CollectionPhase.CLUSTER, self.collect_cluster_info),
            (CollectionPhase.NODES, self.collect_nodes),
            (CollectionPhase.NETWORK, self.collect_network),
            (CollectionPhase.STORAGE, self.collect_storage),
            (CollectionPhase.LICENSES, self.collect_licenses),
            (CollectionPhase.MEDIATOR, self.collect_mediator),
            (CollectionPhase.RELATIONSHIPS, self.collect_relationships),
            (CollectionPhase.PROTOCOLS, self.collect_protocols),
        ]

        # Start SSH connection early in background if CLI client available;
        # the cloud phase waits for it before its CLI call (CVO clusters only).
        preconnect = SshPreconnect(self.cli_client, self._log_prefix, f"ssh-connect-{cluster_name}")
        self._ssh_preconnect = preconnect

        return self._phase_runner().run_parallel(
            phases,
            (CollectionPhase.CLOUD, self.collect_cloud_metadata),
            max_workers=self.max_workers,
            start_background=preconnect.start,
        )

    def _run_phase_safe(
        self, phase: CollectionPhase, collect_method: Callable[[], Any]
    ) -> tuple[Any, Exception | None]:
        """Run a collection phase safely, catching exceptions.

        Args:
            phase: The collection phase.
            collect_method: The method to call for collection.

        Returns:
            Tuple of (result, error) - error is None on success.
        """
        return run_phase_safe(phase, collect_method, self._log_prefix)

    def _connect_ssh_early(self) -> None:
        """Establish SSH connection early to reduce latency.

        Called in a background thread to overlap with API calls.
        """
        connect_early(self.cli_client, self._log_prefix)

    def _determine_source(self, phase: CollectionPhase) -> str | None:
        """Determine which data source is available for a phase.

        Args:
            phase: The collection phase.

        Returns:
            "api", "cli", or None if unknown.
        """
        # Cloud metadata is CLI-only
        if phase == CollectionPhase.CLOUD:
            return "cli" if self.cli_client else None
        # All other phases are API-only
        return "api" if self.api_client else None
