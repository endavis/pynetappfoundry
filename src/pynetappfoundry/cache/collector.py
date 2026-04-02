"""Metadata collector for ONTAP clusters.

Collects cluster metadata using REST API with all-or-nothing semantics.
Collection either succeeds completely or fails entirely — no partial
cache updates. Cloud metadata (CLI-only) is optional; all other phases
are API-only and must succeed.
"""

from __future__ import annotations

import logging
import re
import threading
import time
from collections.abc import Callable, Sequence
from concurrent.futures import Future, ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import UTC, datetime
from enum import Enum
from functools import partial
from typing import TYPE_CHECKING, Any, ClassVar, cast

from pydantic import BaseModel

from pynetappfoundry.cache._metadata import (
    CachedClusterMetadata,
    RelationshipsInfo,
)
from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import (
    TypeMapping,
    parse_cli_records,
)
from pynetappfoundry.cache.field_mapping import (
    parse_api_record as _parse_api_record_raw,
)
from pynetappfoundry.cache.field_mapping import (
    parse_api_response as _parse_api_response_raw,
)
from pynetappfoundry.cache.ontap.cloud.metadata.mapping import CLOUD_METADATA_MAPPING
from pynetappfoundry.cache.ontap.cloud.targets.mapping import ONTAPCLOUDTARGET_MAPPING
from pynetappfoundry.cache.ontap.cluster.licensing.licenses.mapping import (
    ONTAPLICENSEPACKAGERESPONSE_MAPPING,
)
from pynetappfoundry.cache.ontap.cluster.mapping import CLUSTER_MAPPING
from pynetappfoundry.cache.ontap.cluster.mediators.mapping import ONTAPMEDIATORRESPONSE_MAPPING
from pynetappfoundry.cache.ontap.cluster.nodes.mapping import ONTAPNODERESPONSE_MAPPING
from pynetappfoundry.cache.ontap.cluster.peers.mapping import ONTAPCLUSTERPEER_MAPPING
from pynetappfoundry.cache.ontap.cluster.schedules.mapping import ONTAPSCHEDULE_MAPPING
from pynetappfoundry.cache.ontap.name_services.dns.mapping import ONTAPDNS_MAPPING
from pynetappfoundry.cache.ontap.network.ethernet.broadcast_domains.mapping import (
    ONTAPBROADCASTDOMAIN_MAPPING,
)
from pynetappfoundry.cache.ontap.network.ip.interfaces.mapping import ONTAPIPINTERFACE_MAPPING
from pynetappfoundry.cache.ontap.network.ip.subnets.mapping import ONTAPIPSUBNET_MAPPING
from pynetappfoundry.cache.ontap.protocols.cifs.services.mapping import ONTAPCIFSSERVICE_MAPPING
from pynetappfoundry.cache.ontap.protocols.cifs.shares.mapping import ONTAPCIFSSHARE_MAPPING
from pynetappfoundry.cache.ontap.protocols.nfs.export_policies.mapping import (
    ONTAPEXPORTPOLICY_MAPPING,
)
from pynetappfoundry.cache.ontap.protocols.nfs.services.mapping import ONTAPNFSSERVICE_MAPPING
from pynetappfoundry.cache.ontap.protocols.s3.buckets.mapping import ONTAPS3BUCKET_MAPPING
from pynetappfoundry.cache.ontap.protocols.san.igroups.mapping import ONTAPIGROUP_MAPPING
from pynetappfoundry.cache.ontap.snapmirror.relationships.mapping import (
    ONTAPSNAPMIRRORRELATIONSHIP_MAPPING,
)
from pynetappfoundry.cache.ontap.storage.aggregates.mapping import ONTAPAGGREGATE_MAPPING
from pynetappfoundry.cache.ontap.storage.flexcache.flexcaches.mapping import ONTAPFLEXCACHE_MAPPING
from pynetappfoundry.cache.ontap.storage.luns.mapping import ONTAPLUN_MAPPING
from pynetappfoundry.cache.ontap.storage.qos.policies.mapping import ONTAPQOSPOLICY_MAPPING
from pynetappfoundry.cache.ontap.storage.qtrees.mapping import ONTAPQTREE_MAPPING
from pynetappfoundry.cache.ontap.storage.snapshot_policies.mapping import (
    ONTAPSNAPSHOTPOLICY_MAPPING,
)
from pynetappfoundry.cache.ontap.storage.volumes.mapping import ONTAPVOLUME_MAPPING
from pynetappfoundry.cache.ontap.svm.peers.mapping import ONTAPSVMPEER_MAPPING
from pynetappfoundry.cache.ontap.svm.svms.mapping import ONTAPSVM_MAPPING
from pynetappfoundry.cache.ontap.svm.svms.top_metrics.users.mapping import (
    ONTAPTOPMETRICSSVMUSER_MAPPING,
)
from pynetappfoundry.models.ontap.cloud.metadata.model import CloudMetadata
from pynetappfoundry.models.ontap.cloud.targets.model import OntapCloudTarget
from pynetappfoundry.models.ontap.cluster.licensing.licenses.model import (
    OntapLicensePackageResponse,
)
from pynetappfoundry.models.ontap.cluster.mediators.model import OntapMediatorResponse
from pynetappfoundry.models.ontap.cluster.model import ClusterInfo
from pynetappfoundry.models.ontap.cluster.nodes.model import OntapNodeResponse
from pynetappfoundry.models.ontap.cluster.peers.model import OntapClusterPeer
from pynetappfoundry.models.ontap.cluster.schedules.model import OntapSchedule
from pynetappfoundry.models.ontap.name_services.dns.model import OntapDns
from pynetappfoundry.models.ontap.network.ethernet.broadcast_domains.model import (
    OntapBroadcastDomain,
)
from pynetappfoundry.models.ontap.network.ip.interfaces.model import OntapIpInterface
from pynetappfoundry.models.ontap.network.ip.subnets.model import OntapIpSubnet
from pynetappfoundry.models.ontap.network.model import NetworkInfo
from pynetappfoundry.models.ontap.protocols.cifs.services.model import OntapCifsService
from pynetappfoundry.models.ontap.protocols.cifs.shares.model import OntapCifsShare
from pynetappfoundry.models.ontap.protocols.model import ProtocolsInfo
from pynetappfoundry.models.ontap.protocols.nfs.export_policies.model import OntapExportPolicy
from pynetappfoundry.models.ontap.protocols.nfs.services.model import OntapNfsService
from pynetappfoundry.models.ontap.protocols.s3.buckets.model import OntapS3Bucket
from pynetappfoundry.models.ontap.protocols.san.igroups.model import OntapIgroup
from pynetappfoundry.models.ontap.snapmirror.relationships.model import (
    OntapSnapmirrorRelationship,
)
from pynetappfoundry.models.ontap.storage.aggregates.model import OntapAggregate
from pynetappfoundry.models.ontap.storage.flexcache.flexcaches.model import OntapFlexcache
from pynetappfoundry.models.ontap.storage.luns.model import OntapLun
from pynetappfoundry.models.ontap.storage.model import StorageInfo
from pynetappfoundry.models.ontap.storage.qos.policies.model import OntapQosPolicy
from pynetappfoundry.models.ontap.storage.qtrees.model import OntapQtree
from pynetappfoundry.models.ontap.storage.snapshot_policies.model import OntapSnapshotPolicy
from pynetappfoundry.models.ontap.storage.volumes.model import OntapVolume
from pynetappfoundry.models.ontap.svm.peers.model import OntapSvmPeer
from pynetappfoundry.models.ontap.svm.svms.model import OntapSvm
from pynetappfoundry.models.ontap.svm.svms.top_metrics.users.model import OntapTopMetricsSvmUser
from pynetappfoundry.utils.cloud import (
    build_cloud_instance_link,
    build_cloud_instance_sso_link,
    build_cloud_resource_group_link,
)

# Cache collector skips realtime fields (volatile metrics not persisted).
parse_api_record = partial(_parse_api_record_raw, skip_realtime=True)
parse_api_response = partial(_parse_api_response_raw, skip_realtime=True)

if TYPE_CHECKING:
    from pynetappfoundry.clients.ontap.api import ONTAPAPIClient
    from pynetappfoundry.clients.ontap.cli import ONTAPCLI

logger = logging.getLogger(__name__)


def _resolve_dotted_attr(obj: object, dotted_path: str) -> Any:
    """Resolve a dotted attribute path on an object.

    For example, ``_resolve_dotted_attr(parent, "svm.uuid")`` returns
    ``parent.svm.uuid``.  Returns ``None`` if any intermediate attribute
    is missing or ``None``.
    """
    current = obj
    for part in dotted_path.split("."):
        current = getattr(current, part, None)
        if current is None:
            return None
    return current


class CollectionPhase(Enum):
    """Phases of metadata collection."""

    CLOUD = "cloud"
    CLUSTER = "cluster"
    NODES = "nodes"
    NETWORK = "network"
    STORAGE = "storage"
    LICENSES = "licenses"
    MEDIATOR = "mediator"
    RELATIONSHIPS = "relationships"
    PROTOCOLS = "protocols"


@dataclass
class ProgressInfo:
    """Progress information for a collection phase."""

    phase: CollectionPhase
    phase_name: str
    status: str  # "starting", "completed", "failed"
    elapsed_seconds: float = 0.0
    error: str | None = None
    source: str | None = None  # "api", "cli", or None


# Type alias for progress callback
ProgressCallback = Callable[[ProgressInfo], None]


class CollectionError(Exception):
    """Error during metadata collection."""

    pass


class MetadataCollector:
    """Collects cluster metadata from ONTAP via API and CLI.

    Uses REST API for all collection phases (all-or-nothing). Cloud
    metadata is CLI-only and optional — failure warns but doesn't abort.
    """

    # Human-readable names for collection phases
    PHASE_NAMES: ClassVar[dict[CollectionPhase, str]] = {
        CollectionPhase.CLOUD: "Cloud metadata",
        CollectionPhase.CLUSTER: "Cluster info",
        CollectionPhase.NODES: "Nodes",
        CollectionPhase.NETWORK: "Network",
        CollectionPhase.STORAGE: "Storage",
        CollectionPhase.LICENSES: "Licenses",
        CollectionPhase.MEDIATOR: "Mediator",
        CollectionPhase.RELATIONSHIPS: "Relationships",
        CollectionPhase.PROTOCOLS: "Protocols",
    }

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
        max_workers: int = 8,
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
            max_workers: Maximum number of parallel workers. Default 8.
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

    @property
    def _log_prefix(self) -> str:
        """Return log prefix with cluster name for consistent logging."""
        if self._cluster_name:
            return f"[{self._cluster_name}:collector]"
        return "[collector]"

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
        if self.progress_callback:
            info = ProgressInfo(
                phase=phase,
                phase_name=self.PHASE_NAMES.get(phase, phase.value),
                status=status,
                elapsed_seconds=elapsed_seconds,
                error=error,
                source=source,
            )
            self.progress_callback(info)

    def _cached_api_call(self, endpoint: str, method: str = "GET", *, paginate: bool = True) -> Any:
        """Make an API call with caching to avoid duplicate requests.

        Args:
            endpoint: The API endpoint to call.
            method: HTTP method (default GET).
            paginate: When True (default), use ``get_all_records()`` to
                follow pagination and merge all pages.  When False, use
                ``call_endpoint()`` which returns only the first page
                (suitable for single-object endpoints like ``/cluster``).

        Returns:
            API response data (from cache if available).
        """
        if not self.api_client:
            return None

        cache_key = f"{method}:{endpoint}"

        with self._cache_lock:
            if cache_key in self._api_cache:
                logger.debug("%s API cache hit: %s", self._log_prefix, cache_key)
                return self._api_cache[cache_key]

        # Make the actual API call (outside the lock to allow parallel calls)
        logger.debug("%s API call: %s %s", self._log_prefix, method, endpoint)
        if paginate:
            response = self.api_client.get_all_records(endpoint, method=method)
        else:
            response = self.api_client.call_endpoint(endpoint, method=method)

        with self._cache_lock:
            self._api_cache[cache_key] = response

        return response

    def _clear_cache(self) -> None:
        """Clear the API response cache."""
        with self._cache_lock:
            self._api_cache.clear()

    def _collect_parameterized(
        self,
        mapping: TypeMapping,
        parent_objects: Sequence[BaseModel],
    ) -> list[BaseModel]:
        """Fetch child records from a parameterized endpoint by iterating parents.

        For each parent object, substitutes the parent's identifier into the
        URL placeholder, fetches child records, and aggregates them.

        Args:
            mapping: Child TypeMapping (must have parent_mapping and parent_id_field set).
            parent_objects: List of already-collected parent model instances.

        Returns:
            Aggregated list of child model instances across all parents.

        Raises:
            ValueError: If mapping.parent_mapping or mapping.parent_id_field is not set.
        """
        if not mapping.parent_mapping:
            raise ValueError(
                f"{mapping.name}: parent_mapping must be set for parameterized collection"
            )
        if not mapping.parent_id_field:
            raise ValueError(
                f"{mapping.name}: parent_id_field must be set for parameterized collection"
            )

        aggregated: list[BaseModel] = []
        for parent in parent_objects:
            parent_id = _resolve_dotted_attr(parent, mapping.parent_id_field)
            if not parent_id:
                parent_name = getattr(parent, "name", repr(parent))
                logger.warning(
                    "%s SKIP_PARENT: %s - parent %s has no '%s'",
                    self._log_prefix,
                    mapping.name,
                    parent_name,
                    mapping.parent_id_field,
                )
                continue

            url = mapping.build_parameterized_url(str(parent_id))
            try:
                response = self._cached_api_call(url)
                children = parse_api_response(
                    mapping, response, self._log_prefix, self._log_missing_fields
                )
                aggregated.extend(children)
            except Exception as e:
                parent_name = getattr(parent, "name", repr(parent))
                logger.warning(
                    "%s CHILD_FETCH_FAILED: %s for parent %s - %s: %s",
                    self._log_prefix,
                    mapping.name,
                    parent_name,
                    type(e).__name__,
                    e,
                )

        return aggregated

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
        storage_info: StorageInfo = results["storage"]
        svm_top_metrics_users = self._collect_svm_top_metrics_users(storage_info.svms)
        storage_info = storage_info.model_copy(
            update={"svm_top_metrics_users": svm_top_metrics_users}
        )
        results["storage"] = storage_info

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

    def _collect_all_sequential(self, cluster_name: str) -> dict[str, Any]:
        """Collect all metadata sequentially (original behavior).

        Args:
            cluster_name: Name of the cluster being collected.

        Returns:
            Dictionary of collection results keyed by phase name.
        """
        phases: list[tuple[CollectionPhase, Callable[[], Any]]] = [
            (CollectionPhase.CLOUD, self.collect_cloud_metadata),
            (CollectionPhase.CLUSTER, self.collect_cluster_info),
            (CollectionPhase.NODES, self.collect_nodes),
            (CollectionPhase.NETWORK, self.collect_network),
            (CollectionPhase.STORAGE, self.collect_storage),
            (CollectionPhase.LICENSES, self.collect_licenses),
            (CollectionPhase.MEDIATOR, self.collect_mediator),
            (CollectionPhase.RELATIONSHIPS, self.collect_relationships),
            (CollectionPhase.PROTOCOLS, self.collect_protocols),
        ]

        results: dict[str, Any] = {}
        for phase, collect_method in phases:
            phase_start = time.monotonic()
            self._report_progress(phase, "starting")
            logger.debug("%s Collecting %s", self._log_prefix, phase.value)

            try:
                result = collect_method()
                elapsed = time.monotonic() - phase_start
                source = self._determine_source(phase)
                self._report_progress(phase, "completed", elapsed, source=source)
                logger.debug(
                    "%s Collected %s in %.2fs via %s",
                    self._log_prefix,
                    phase.value,
                    elapsed,
                    source or "unknown",
                )
                results[phase.value] = result
            except Exception as e:
                elapsed = time.monotonic() - phase_start
                error_msg = str(e)
                self._report_progress(phase, "failed", elapsed, error=error_msg)
                logger.error(
                    "%s COLLECTION_ABORTED: Failed phase: %s - %s: %s",
                    self._log_prefix,
                    phase.value,
                    type(e).__name__,
                    error_msg,
                )
                raise

        return results

    def _collect_all_parallel(self, cluster_name: str) -> dict[str, Any]:
        """Collect all metadata in parallel for improved performance.

        Starts SSH connection early, then runs all API phases concurrently.

        Args:
            cluster_name: Name of the cluster being collected.

        Returns:
            Dictionary of collection results keyed by phase name.
        """
        results: dict[str, Any] = {}
        phase_timings: dict[CollectionPhase, tuple[float, str | None]] = {}

        # Define all phases
        phases: list[tuple[CollectionPhase, Callable[[], Any]]] = [
            (CollectionPhase.CLOUD, self.collect_cloud_metadata),
            (CollectionPhase.CLUSTER, self.collect_cluster_info),
            (CollectionPhase.NODES, self.collect_nodes),
            (CollectionPhase.NETWORK, self.collect_network),
            (CollectionPhase.STORAGE, self.collect_storage),
            (CollectionPhase.LICENSES, self.collect_licenses),
            (CollectionPhase.MEDIATOR, self.collect_mediator),
            (CollectionPhase.RELATIONSHIPS, self.collect_relationships),
            (CollectionPhase.PROTOCOLS, self.collect_protocols),
        ]

        # Report all phases as starting
        for phase, _ in phases:
            self._report_progress(phase, "starting")

        # Start SSH connection early in background if CLI client available
        ssh_connect_thread: threading.Thread | None = None
        if self.cli_client:
            logger.debug("%s Starting SSH connection in background", self._log_prefix)
            ssh_connect_thread = threading.Thread(
                target=self._connect_ssh_early,
                name=f"ssh-connect-{cluster_name}",
                daemon=True,
            )
            ssh_connect_thread.start()

        # Run all phases in parallel using ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all phases
            future_to_phase: dict[Future[Any], tuple[CollectionPhase, float]] = {}
            for phase, collect_method in phases:
                phase_start = time.monotonic()
                future = executor.submit(self._run_phase_safe, phase, collect_method)
                future_to_phase[future] = (phase, phase_start)

            # Collect results as they complete
            errors: list[tuple[CollectionPhase, Exception]] = []
            for future in as_completed(future_to_phase):
                phase, phase_start = future_to_phase[future]
                elapsed = time.monotonic() - phase_start
                source = self._determine_source(phase)

                try:
                    result, error = future.result()
                    if error:
                        phase_timings[phase] = (elapsed, source)
                        self._report_progress(phase, "failed", elapsed, error=str(error))
                        logger.error(
                            "%s Failed to collect %s: %s",
                            self._log_prefix,
                            phase.value,
                            error,
                        )
                        errors.append((phase, error))
                    else:
                        results[phase.value] = result
                        phase_timings[phase] = (elapsed, source)
                        self._report_progress(phase, "completed", elapsed, source=source)
                        logger.debug(
                            "%s Collected %s in %.2fs via %s",
                            self._log_prefix,
                            phase.value,
                            elapsed,
                            source or "unknown",
                        )
                except Exception as e:
                    phase_timings[phase] = (elapsed, source)
                    self._report_progress(phase, "failed", elapsed, error=str(e))
                    logger.error(
                        "%s Failed to collect %s: %s",
                        self._log_prefix,
                        phase.value,
                        e,
                        exc_info=True,
                    )
                    errors.append((phase, e))

        # Wait for SSH connection thread if it was started
        if ssh_connect_thread and ssh_connect_thread.is_alive():
            ssh_connect_thread.join(timeout=1.0)

        # If any phase failed, raise the first error
        if errors:
            first_phase, first_error = errors[0]
            logger.error(
                "%s COLLECTION_ABORTED: Failed phase: %s - %s: %s",
                self._log_prefix,
                first_phase.value,
                type(first_error).__name__,
                first_error,
            )
            raise CollectionError(
                f"Collection failed for phase {first_phase.value}: {first_error}"
            ) from first_error

        return results

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
        try:
            result = collect_method()
            return result, None
        except Exception as e:
            logger.debug("%s Phase %s failed: %s", self._log_prefix, phase.value, e)
            return None, e

    def _connect_ssh_early(self) -> None:
        """Establish SSH connection early to reduce latency.

        Called in a background thread to overlap with API calls.
        """
        if self.cli_client:
            try:
                logger.debug("%s Establishing early SSH connection", self._log_prefix)
                self.cli_client.connect()
                logger.debug("%s Early SSH connection established", self._log_prefix)
            except Exception as e:
                logger.debug(
                    "%s Early SSH connection failed (will retry later): %s", self._log_prefix, e
                )

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

    def _log_missing_fields(
        self,
        record: dict[str, Any],
        expected_fields: list[str],
        record_type: str,
        record_id: str,
    ) -> None:
        """Log error messages for expected API fields missing from a record.

        Only logs when a key is absent from the dict — not when present
        with a null, empty, or zero value.

        Args:
            record: The API response record dict.
            expected_fields: Top-level keys expected in the record.
            record_type: Human-readable type (e.g., "Volume", "Aggregate").
            record_id: Identifier for the record (name or uuid).
        """
        for field in expected_fields:
            if field not in record:
                logger.error(
                    "%s MISSING_FIELD: %s '%s' - '%s' not in API response",
                    self._log_prefix,
                    record_type,
                    record_id,
                    field,
                )

    # -------------------------------------------------------------------------
    # Cloud Metadata Collection
    # -------------------------------------------------------------------------

    def collect_cloud_metadata(self) -> list[CloudMetadata]:
        """Collect cloud provider metadata.

        Cloud metadata is only available via CLI (virtual-machine instance show).
        Returns one CloudMetadata per node in the cluster. This is the only
        CLI-only phase — failure warns but does not abort collection.

        Returns:
            List of CloudMetadata objects, one per node.
        """
        if self.cli_client:
            try:
                return self._collect_cloud_metadata_via_cli()
            except Exception as e:
                logger.error(
                    "%s CLI_FAILURE: Cloud metadata - %s: %s",
                    self._log_prefix,
                    type(e).__name__,
                    e,
                )
        return []

    def _collect_cloud_metadata_via_cli(self) -> list[CloudMetadata]:
        """Collect cloud metadata using CLI.

        Parses the raw CLI text into dict records, feeds them through
        ``parse_cli_records`` via the ``CLOUD_METADATA_MAPPING``, and
        then post-processes the results to build computed link fields
        that depend on collector state (``aws_sso_config``).

        Returns:
            List of CloudMetadata from virtual-machine instance show.
        """
        if not self.cli_client:
            logger.debug(
                "%s No CLI client available for cloud metadata collection", self._log_prefix
            )
            return []

        logger.debug("%s CLI command: virtual-machine instance show", self._log_prefix)
        output = self.cli_client.run_command("virtual-machine instance show")
        logger.debug("%s CLI response: %d lines", self._log_prefix, len(output))

        records = self._parse_vm_instance_output(output)
        items = parse_cli_records(
            CLOUD_METADATA_MAPPING,
            records,
            self._log_prefix,
            self._log_missing_fields,
        )
        results = cast(list[CloudMetadata], items)

        # Post-process: build computed link fields
        for cm in results:
            region = cm.region or cm.availability_zone
            cm.instance_link = build_cloud_instance_link(
                provider=cm.provider,
                instance_id=cm.instance_id,
                region=region,
                account_id=cm.account_id,
                resource_group=cm.resource_group_name,
            )
            cm.instance_sso_link = build_cloud_instance_sso_link(
                provider=cm.provider,
                instance_link=cm.instance_link,
                account_id=cm.account_id,
                sso_config=self.aws_sso_config,
            )
            cm.resource_group_link = build_cloud_resource_group_link(
                provider=cm.provider,
                account_id=cm.account_id,
                resource_group=cm.resource_group_name,
            )

        return results

    def _parse_vm_instance_output(self, output: list[str]) -> list[dict[str, str]]:
        """Parse virtual-machine instance show output into raw records.

        The CLI output contains entries for each node, separated by blank lines
        or new "Node:" entries. Each node has its own cloud metadata.

        Args:
            output: Lines of CLI output.

        Returns:
            List of raw record dicts (one per node) with normalized keys.
        """
        results: list[dict[str, str]] = []
        current_data: dict[str, str] = {}
        current_node: str = ""

        for line in output:
            line = line.strip()
            if not line:
                # Empty line may indicate end of a node's data
                continue

            if ":" not in line:
                continue

            parts = line.split(":", 1)
            if len(parts) != 2:
                continue

            key = parts[0].strip()
            value = parts[1].strip()
            key_normalized = self._normalize_cli_key(key)

            # Check if this is a new node entry
            if key_normalized == "node":
                # Save previous node's data if we have any
                if current_node and current_data:
                    current_data["node"] = current_node
                    results.append(current_data)
                # Start new node
                current_node = value
                current_data = {}
            else:
                current_data[key_normalized] = value

        # Don't forget the last node
        if current_node and current_data:
            current_data["node"] = current_node
            results.append(current_data)

        # If no node field was found but we have data, create single entry
        if not results and current_data:
            current_data["node"] = ""
            results.append(current_data)

        return results

    def _update_azure_cloud_links(
        self,
        cloud_metadata: list[CloudMetadata],
        cluster_name: str,
        is_ha: bool,
    ) -> list[CloudMetadata]:
        """Update Azure cloud metadata with correct instance links.

        Azure VM portal links require the VM name derived from cluster name
        and node information, not the instance_id from cloud metadata.

        Args:
            cloud_metadata: List of CloudMetadata objects to update.
            cluster_name: The cluster name.
            is_ha: Whether the cluster is HA.

        Returns:
            Updated list of CloudMetadata with correct Azure instance links.
        """
        updated = []
        for meta in cloud_metadata:
            if meta.provider.lower() != "azure":
                updated.append(meta)
                continue

            # Rebuild the instance link with cluster/node info
            instance_link = build_cloud_instance_link(
                provider=meta.provider,
                instance_id=meta.instance_id,
                account_id=meta.account_id,
                resource_group=meta.resource_group_name,
                cluster_name=cluster_name,
                node_name=meta.node,
                is_ha=is_ha,
            )

            # Rebuild SSO link (not applicable for Azure, but keep for consistency)
            instance_sso_link = build_cloud_instance_sso_link(
                provider=meta.provider,
                instance_link=instance_link,
                account_id=meta.account_id,
                sso_config=self.aws_sso_config,
            )

            # Create updated CloudMetadata with new links
            updated.append(
                CloudMetadata(
                    node=meta.node,
                    instance_id=meta.instance_id,
                    account_id=meta.account_id,
                    image_id=meta.image_id,
                    instance_type=meta.instance_type,
                    cpu_platform=meta.cpu_platform,
                    region=meta.region,
                    provider=meta.provider,
                    consumer=meta.consumer,
                    primary_ip=meta.primary_ip,
                    metadata_version=meta.metadata_version,
                    availability_zone=meta.availability_zone,
                    availability_zone_id=meta.availability_zone_id,
                    fault_domain=meta.fault_domain,
                    update_domain=meta.update_domain,
                    resource_group_name=meta.resource_group_name,
                    offer=meta.offer,
                    sku=meta.sku,
                    sku_version=meta.sku_version,
                    instance_link=instance_link,
                    instance_sso_link=instance_sso_link,
                    resource_group_link=meta.resource_group_link,
                )
            )
        return updated

    @staticmethod
    def _normalize_cli_key(key: str) -> str:
        """Normalize CLI output key to snake_case.

        Args:
            key: Original key from CLI output.

        Returns:
            Normalized key name.
        """
        # Replace spaces with underscores, lowercase
        normalized = key.lower().replace(" ", "_").replace("-", "_")
        # Remove any non-alphanumeric chars except underscore
        normalized = re.sub(r"[^a-z0-9_]", "", normalized)
        return normalized

    # -------------------------------------------------------------------------
    # Cluster Info Collection
    # -------------------------------------------------------------------------

    def collect_cluster_info(self) -> ClusterInfo:
        """Collect cluster identity information (API-only).

        Returns:
            ClusterInfo object.

        Raises:
            CollectionError: If no API client is available.
            Exception: If the API call fails.
        """
        if not self.api_client:
            raise CollectionError(
                f"{self._log_prefix} API_FAILURE: Cluster info - no API client available"
            )
        try:
            return self._collect_cluster_info_via_api()
        except Exception as e:
            logger.error(
                "%s API_FAILURE: Cluster info - %s: %s",
                self._log_prefix,
                type(e).__name__,
                e,
            )
            raise

    def _collect_cluster_info_via_api(self) -> ClusterInfo:
        """Collect cluster info using REST API.

        Returns:
            ClusterInfo from /cluster endpoint.
        """
        if not self.api_client:
            logger.debug("%s No API client available for cluster info collection", self._log_prefix)
            return ClusterInfo()

        response = self._cached_api_call(CLUSTER_MAPPING.build_collection_url(), paginate=False)
        if not response:
            return ClusterInfo()

        logger.debug(
            "%s API response: cluster=%s", self._log_prefix, response.get("name", "unknown")
        )
        self._log_missing_fields(
            response,
            CLUSTER_MAPPING.api_expected_fields(),
            "Cluster",
            response.get("name", "unknown"),
        )
        return cast(
            ClusterInfo,
            parse_api_record(CLUSTER_MAPPING, response, self._log_prefix),
        )

    # -------------------------------------------------------------------------
    # Node Collection
    # -------------------------------------------------------------------------

    def collect_nodes(self) -> list[OntapNodeResponse]:
        """Collect node information (API-only).

        Returns:
            List of OntapNodeResponse objects.

        Raises:
            CollectionError: If no API client is available.
            Exception: If the API call fails.
        """
        if not self.api_client:
            raise CollectionError(
                f"{self._log_prefix} API_FAILURE: Nodes - no API client available"
            )
        try:
            return self._collect_nodes_via_api()
        except Exception as e:
            logger.error(
                "%s API_FAILURE: Nodes - %s: %s",
                self._log_prefix,
                type(e).__name__,
                e,
            )
            raise

    def _collect_nodes_via_api(self) -> list[OntapNodeResponse]:
        """Collect nodes using REST API.

        Returns:
            List of OntapNodeResponse from /cluster/nodes endpoint.
        """
        if not self.api_client:
            logger.debug("%s No API client available for nodes collection", self._log_prefix)
            return []

        # Use cached API call to avoid duplicate requests (also used by HA collection)
        response = self._cached_api_call(ONTAPNODERESPONSE_MAPPING.build_collection_url())
        if not response:
            return []

        return cast(
            list[OntapNodeResponse],
            parse_api_response(
                ONTAPNODERESPONSE_MAPPING, response, self._log_prefix, self._log_missing_fields
            ),
        )

    # -------------------------------------------------------------------------
    # Network Collection
    # -------------------------------------------------------------------------

    def collect_network(self) -> NetworkInfo:
        """Collect network configuration (API-only).

        Returns:
            NetworkInfo object.

        Raises:
            CollectionError: If no API client is available.
            Exception: If the API call fails.
        """
        if not self.api_client:
            raise CollectionError(
                f"{self._log_prefix} API_FAILURE: Network - no API client available"
            )
        try:
            return self._collect_network_via_api()
        except Exception as e:
            logger.error(
                "%s API_FAILURE: Network - %s: %s",
                self._log_prefix,
                type(e).__name__,
                e,
            )
            raise

    def _collect_network_via_api(self) -> NetworkInfo:
        """Collect network info using REST API.

        Makes parallel API calls for improved performance.

        Returns:
            NetworkInfo from various network endpoints.
        """
        if not self.api_client:
            logger.debug("%s No API client available for network collection", self._log_prefix)
            return NetworkInfo()

        # Make all 5 API calls in parallel using cached calls
        endpoints = [
            ONTAPIPINTERFACE_MAPPING.build_collection_url(),
            ONTAPBROADCASTDOMAIN_MAPPING.build_collection_url(),
            "/network/ipspaces?fields=*",
            ONTAPDNS_MAPPING.build_collection_url(),
            ONTAPIPSUBNET_MAPPING.build_collection_url(),
        ]

        if self.parallel:
            with ThreadPoolExecutor(max_workers=5) as executor:
                futures = {executor.submit(self._cached_api_call, ep): ep for ep in endpoints}
                responses: dict[str, Any] = {}
                for future in as_completed(futures):
                    ep = futures[future]
                    responses[ep] = future.result()
        else:
            responses = {ep: self._cached_api_call(ep) for ep in endpoints}

        # Process LIFs response
        all_lifs = cast(
            list[OntapIpInterface],
            parse_api_response(
                ONTAPIPINTERFACE_MAPPING,
                responses.get(endpoints[0]),
                self._log_prefix,
                self._log_missing_fields,
            ),
        )
        # Process broadcast domains response
        broadcast_domains = cast(
            list[OntapBroadcastDomain],
            parse_api_response(
                ONTAPBROADCASTDOMAIN_MAPPING,
                responses.get(endpoints[1]),
                self._log_prefix,
                self._log_missing_fields,
            ),
        )

        # Process IPspaces response
        ipspace_response = responses.get(endpoints[2]) or {}
        logger.debug(
            "%s API response: %d IPspaces",
            self._log_prefix,
            len(ipspace_response.get("records", [])),
        )
        ipspaces = [r.get("name", "") for r in ipspace_response.get("records", [])]

        # Process DNS response
        dns = cast(
            list[OntapDns],
            parse_api_response(
                ONTAPDNS_MAPPING,
                responses.get(endpoints[3]),
                self._log_prefix,
                self._log_missing_fields,
            ),
        )

        # Process subnets response
        subnets = cast(
            list[OntapIpSubnet],
            parse_api_response(
                ONTAPIPSUBNET_MAPPING,
                responses.get(endpoints[4]),
                self._log_prefix,
                self._log_missing_fields,
            ),
        )

        return NetworkInfo(
            ip_interfaces=all_lifs,
            ethernet_broadcast_domains=broadcast_domains,
            ipspaces=ipspaces,
            dns=dns,
            ip_subnets=subnets,
        )

    # -------------------------------------------------------------------------
    # Storage Collection
    # -------------------------------------------------------------------------

    def collect_storage(self) -> StorageInfo:
        """Collect storage topology information (API-only).

        Returns:
            StorageInfo object.

        Raises:
            CollectionError: If no API client is available.
            Exception: If the API call fails.
        """
        if not self.api_client:
            raise CollectionError(
                f"{self._log_prefix} API_FAILURE: Storage - no API client available"
            )
        try:
            return self._collect_storage_via_api()
        except Exception as e:
            logger.error(
                "%s API_FAILURE: Storage - %s: %s",
                self._log_prefix,
                type(e).__name__,
                e,
            )
            raise

    def _collect_storage_via_api(self) -> StorageInfo:
        """Collect storage info using REST API.

        Makes parallel API calls for improved performance.

        Returns:
            StorageInfo from aggregate, SVM, and cloud target endpoints.
        """
        if not self.api_client:
            logger.debug("%s No API client available for storage collection", self._log_prefix)
            return StorageInfo()

        # Make all API calls in parallel using cached calls
        endpoints = [
            ONTAPAGGREGATE_MAPPING.build_collection_url(),
            ONTAPSVM_MAPPING.build_collection_url(),
            ONTAPCLOUDTARGET_MAPPING.build_collection_url(),
            ONTAPVOLUME_MAPPING.build_collection_url(),
            ONTAPQTREE_MAPPING.build_collection_url(),
            ONTAPSNAPSHOTPOLICY_MAPPING.build_collection_url(),
            ONTAPSCHEDULE_MAPPING.build_collection_url(),
            ONTAPLUN_MAPPING.build_collection_url(),
            ONTAPIGROUP_MAPPING.build_collection_url(),
            ONTAPQOSPOLICY_MAPPING.build_collection_url(),
            ONTAPFLEXCACHE_MAPPING.build_collection_url(),
        ]

        def safe_api_call(endpoint: str) -> Any:
            """Make API call, returning None on failure for optional endpoints."""
            try:
                return self._cached_api_call(endpoint)
            except Exception as e:
                # Cloud targets may not exist on older ONTAP versions
                if "cloud/targets" in endpoint:
                    logger.debug("%s Cloud targets endpoint not available: %s", self._log_prefix, e)
                    return None
                raise

        if self.parallel:
            with ThreadPoolExecutor(max_workers=11) as executor:
                futures = {executor.submit(safe_api_call, ep): ep for ep in endpoints}
                responses: dict[str, Any] = {}
                for future in as_completed(futures):
                    ep = futures[future]
                    responses[ep] = future.result()
        else:
            responses = {ep: safe_api_call(ep) for ep in endpoints}

        # Process aggregates response
        aggregates = cast(
            list[OntapAggregate],
            parse_api_response(
                ONTAPAGGREGATE_MAPPING,
                responses.get(endpoints[0]),
                self._log_prefix,
                self._log_missing_fields,
            ),
        )

        # Process SVMs response
        svms = cast(
            list[OntapSvm],
            parse_api_response(
                ONTAPSVM_MAPPING,
                responses.get(endpoints[1]),
                self._log_prefix,
                self._log_missing_fields,
            ),
        )

        # Process cloud targets response
        cloud_targets = cast(
            list[OntapCloudTarget],
            parse_api_response(
                ONTAPCLOUDTARGET_MAPPING,
                responses.get(endpoints[2]),
                self._log_prefix,
                self._log_missing_fields,
            ),
        )

        # Process volumes response
        volumes = cast(
            list[OntapVolume],
            parse_api_response(
                ONTAPVOLUME_MAPPING,
                responses.get(endpoints[3]),
                self._log_prefix,
                self._log_missing_fields,
            ),
        )

        # Process qtrees response
        qtrees = cast(
            list[OntapQtree],
            parse_api_response(
                ONTAPQTREE_MAPPING,
                responses.get(endpoints[4]),
                self._log_prefix,
                self._log_missing_fields,
            ),
        )

        # Process snapshot policies response
        snapshot_policies = cast(
            list[OntapSnapshotPolicy],
            parse_api_response(
                ONTAPSNAPSHOTPOLICY_MAPPING,
                responses.get(endpoints[5]),
                self._log_prefix,
                self._log_missing_fields,
            ),
        )

        # Process schedules response
        schedules = cast(
            list[OntapSchedule],
            parse_api_response(
                ONTAPSCHEDULE_MAPPING,
                responses.get(endpoints[6]),
                self._log_prefix,
                self._log_missing_fields,
            ),
        )

        # Process LUNs response
        luns = cast(
            list[OntapLun],
            parse_api_response(
                ONTAPLUN_MAPPING,
                responses.get(endpoints[7]),
                self._log_prefix,
                self._log_missing_fields,
            ),
        )

        # Process igroups response
        igroups = cast(
            list[OntapIgroup],
            parse_api_response(
                ONTAPIGROUP_MAPPING,
                responses.get(endpoints[8]),
                self._log_prefix,
                self._log_missing_fields,
            ),
        )

        # Process QoS policies response
        qos_policies = cast(
            list[OntapQosPolicy],
            parse_api_response(
                ONTAPQOSPOLICY_MAPPING,
                responses.get(endpoints[9]),
                self._log_prefix,
                self._log_missing_fields,
            ),
        )

        # Process FlexCache response
        flexcaches = cast(
            list[OntapFlexcache],
            parse_api_response(
                ONTAPFLEXCACHE_MAPPING,
                responses.get(endpoints[10]),
                self._log_prefix,
                self._log_missing_fields,
            ),
        )

        return StorageInfo(
            aggregates=aggregates,
            svms=svms,
            cloud_targets=cloud_targets,
            volumes=volumes,
            qtrees=qtrees,
            snapshot_policies=snapshot_policies,
            schedules=schedules,
            luns=luns,
            igroups=igroups,
            qos_policies=qos_policies,
            flexcaches=flexcaches,
        )

    # -------------------------------------------------------------------------
    # License Collection
    # -------------------------------------------------------------------------

    def collect_licenses(self) -> list[OntapLicensePackageResponse]:
        """Collect licensing information (API-only).

        Returns:
            List of OntapLicensePackageResponse objects.

        Raises:
            CollectionError: If no API client is available.
            Exception: If the API call fails.
        """
        if not self.api_client:
            raise CollectionError(
                f"{self._log_prefix} API_FAILURE: Licenses - no API client available"
            )
        try:
            return self._collect_licenses_via_api()
        except Exception as e:
            logger.error(
                "%s API_FAILURE: Licenses - %s: %s",
                self._log_prefix,
                type(e).__name__,
                e,
            )
            raise

    def _collect_licenses_via_api(self) -> list[OntapLicensePackageResponse]:
        """Collect licenses using REST API.

        Returns:
            List of OntapLicensePackageResponse from /cluster/licensing/licenses endpoint.
        """
        if not self.api_client:
            logger.debug("%s No API client available for license collection", self._log_prefix)
            return []

        response = self._cached_api_call(ONTAPLICENSEPACKAGERESPONSE_MAPPING.build_collection_url())
        return cast(
            list[OntapLicensePackageResponse],
            parse_api_response(
                ONTAPLICENSEPACKAGERESPONSE_MAPPING,
                response,
                self._log_prefix,
                self._log_missing_fields,
            ),
        )

    # -------------------------------------------------------------------------
    # Mediator Collection
    # -------------------------------------------------------------------------

    def collect_mediator(self) -> OntapMediatorResponse:
        """Collect ONTAP Mediator information (API-only).

        Returns:
            OntapMediatorResponse object.

        Raises:
            CollectionError: If no API client is available.
        """
        if not self.api_client:
            raise CollectionError(
                f"{self._log_prefix} API_FAILURE: Mediator - no API client available"
            )
        try:
            return self._collect_mediator_via_api()
        except Exception as e:
            logger.error(
                "%s API_FAILURE: Mediator - %s: %s",
                self._log_prefix,
                type(e).__name__,
                e,
            )
            raise

    def _collect_mediator_via_api(self) -> OntapMediatorResponse:
        """Collect mediator info using REST API.

        Returns:
            OntapMediatorResponse from /cluster/mediators endpoint.
        """
        try:
            mediator_response = self._cached_api_call(
                ONTAPMEDIATORRESPONSE_MAPPING.build_collection_url()
            )
            parsed = parse_api_response(
                ONTAPMEDIATORRESPONSE_MAPPING,
                mediator_response,
                self._log_prefix,
                self._log_missing_fields,
            )
            if parsed:
                return cast(OntapMediatorResponse, parsed[0])
        except Exception as e:
            logger.debug("%s Mediator endpoint not available: %s", self._log_prefix, e)

        return OntapMediatorResponse()

    # -------------------------------------------------------------------------
    # Relationships Collection
    # -------------------------------------------------------------------------

    def collect_relationships(self) -> RelationshipsInfo:
        """Collect cluster relationships information (API-only).

        Returns:
            RelationshipsInfo object.

        Raises:
            CollectionError: If no API client is available.
            Exception: If the API call fails.
        """
        if not self.api_client:
            raise CollectionError(
                f"{self._log_prefix} API_FAILURE: Relationships - no API client available"
            )
        try:
            return self._collect_relationships_via_api()
        except Exception as e:
            logger.error(
                "%s API_FAILURE: Relationships - %s: %s",
                self._log_prefix,
                type(e).__name__,
                e,
            )
            raise

    def _collect_relationships_via_api(self) -> RelationshipsInfo:
        """Collect relationships using REST API.

        Makes parallel API calls for improved performance.

        Returns:
            RelationshipsInfo from snapmirror and cluster peer endpoints.
        """
        if not self.api_client:
            logger.debug(
                "%s No API client available for relationships collection", self._log_prefix
            )
            return RelationshipsInfo()

        # Make all 3 API calls in parallel using cached calls
        # Request only needed fields for snapmirror to avoid timeout on large clusters
        endpoints = [
            ONTAPSNAPMIRRORRELATIONSHIP_MAPPING.build_collection_url(),
            ONTAPCLUSTERPEER_MAPPING.build_collection_url(),
            ONTAPSVMPEER_MAPPING.build_collection_url(),
        ]

        if self.parallel:
            with ThreadPoolExecutor(max_workers=3) as executor:
                futures = {executor.submit(self._cached_api_call, ep): ep for ep in endpoints}
                responses: dict[str, Any] = {}
                for future in as_completed(futures):
                    ep = futures[future]
                    responses[ep] = future.result()
        else:
            responses = {ep: self._cached_api_call(ep) for ep in endpoints}

        # Process SnapMirror relationships
        snapmirror_destinations = cast(
            list[OntapSnapmirrorRelationship],
            parse_api_response(
                ONTAPSNAPMIRRORRELATIONSHIP_MAPPING,
                responses.get(endpoints[0]),
                self._log_prefix,
                self._log_missing_fields,
            ),
        )

        # Process cluster peers
        cluster_peers = cast(
            list[OntapClusterPeer],
            parse_api_response(
                ONTAPCLUSTERPEER_MAPPING,
                responses.get(endpoints[1]),
                self._log_prefix,
                self._log_missing_fields,
            ),
        )

        # Process SVM peers
        svm_peers = cast(
            list[OntapSvmPeer],
            parse_api_response(
                ONTAPSVMPEER_MAPPING,
                responses.get(endpoints[2]),
                self._log_prefix,
                self._log_missing_fields,
            ),
        )

        return RelationshipsInfo(
            snapmirror_destinations=snapmirror_destinations,
            cluster_peers=cluster_peers,
            svm_peers=svm_peers,
        )

    # -------------------------------------------------------------------------
    # Parameterized Endpoint Collection
    # -------------------------------------------------------------------------

    def _collect_svm_top_metrics_users(self, svms: list[OntapSvm]) -> list[OntapTopMetricsSvmUser]:
        """Collect top-metrics users per SVM using parameterized endpoint.

        Args:
            svms: List of collected SVM objects (parents).

        Returns:
            Aggregated list of OntapTopMetricsSvmUser across all SVMs.
        """
        if not self.api_client:
            return []
        return cast(
            list[OntapTopMetricsSvmUser],
            self._collect_parameterized(ONTAPTOPMETRICSSVMUSER_MAPPING, svms),
        )

    # -------------------------------------------------------------------------
    # Protocols Collection
    # -------------------------------------------------------------------------

    def collect_protocols(self) -> ProtocolsInfo:
        """Collect protocol configuration information (API-only).

        Returns:
            ProtocolsInfo object.

        Raises:
            CollectionError: If no API client is available.
            Exception: If the API call fails.
        """
        if not self.api_client:
            raise CollectionError(
                f"{self._log_prefix} API_FAILURE: Protocols - no API client available"
            )
        try:
            return self._collect_protocols_via_api()
        except Exception as e:
            logger.error(
                "%s API_FAILURE: Protocols - %s: %s",
                self._log_prefix,
                type(e).__name__,
                e,
            )
            raise

    def _collect_protocols_via_api(self) -> ProtocolsInfo:
        """Collect protocol info using REST API.

        Makes parallel API calls for improved performance.

        Returns:
            ProtocolsInfo from various protocol endpoints.
        """
        if not self.api_client:
            logger.debug("%s No API client available for protocols collection", self._log_prefix)
            return ProtocolsInfo()

        endpoints = [
            ONTAPEXPORTPOLICY_MAPPING.build_collection_url(),
            ONTAPCIFSSHARE_MAPPING.build_collection_url(),
            ONTAPNFSSERVICE_MAPPING.build_collection_url(),
            ONTAPCIFSSERVICE_MAPPING.build_collection_url(),
            ONTAPS3BUCKET_MAPPING.build_collection_url(),
        ]

        if self.parallel:
            with ThreadPoolExecutor(max_workers=5) as executor:
                futures = {executor.submit(self._cached_api_call, ep): ep for ep in endpoints}
                responses: dict[str, Any] = {}
                for future in as_completed(futures):
                    ep = futures[future]
                    responses[ep] = future.result()
        else:
            responses = {ep: self._cached_api_call(ep) for ep in endpoints}

        export_policies = cast(
            list[OntapExportPolicy],
            parse_api_response(
                ONTAPEXPORTPOLICY_MAPPING,
                responses.get(endpoints[0]),
                self._log_prefix,
                self._log_missing_fields,
            ),
        )
        cifs_shares = cast(
            list[OntapCifsShare],
            parse_api_response(
                ONTAPCIFSSHARE_MAPPING,
                responses.get(endpoints[1]),
                self._log_prefix,
                self._log_missing_fields,
            ),
        )
        nfs_services = cast(
            list[OntapNfsService],
            parse_api_response(
                ONTAPNFSSERVICE_MAPPING,
                responses.get(endpoints[2]),
                self._log_prefix,
                self._log_missing_fields,
            ),
        )
        cifs_services = cast(
            list[OntapCifsService],
            parse_api_response(
                ONTAPCIFSSERVICE_MAPPING,
                responses.get(endpoints[3]),
                self._log_prefix,
                self._log_missing_fields,
            ),
        )
        s3_buckets = cast(
            list[OntapS3Bucket],
            parse_api_response(
                ONTAPS3BUCKET_MAPPING,
                responses.get(endpoints[4]),
                self._log_prefix,
                self._log_missing_fields,
            ),
        )

        return ProtocolsInfo(
            nfs_export_policies=export_policies,
            cifs_shares=cifs_shares,
            nfs_services=nfs_services,
            cifs_services=cifs_services,
            s3_buckets=s3_buckets,
        )
