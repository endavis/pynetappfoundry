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
from collections.abc import Callable
from concurrent.futures import Future, ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import UTC, datetime
from enum import Enum
from typing import TYPE_CHECKING, Any, ClassVar, cast

from pynetappfoundry.cache._metadata import (
    CachedClusterMetadata,
    RelationshipsInfo,
)
from pynetappfoundry.cache.cloud.metadata.mapping import CLOUD_METADATA_MAPPING
from pynetappfoundry.cache.cloud.metadata.model import CloudMetadata
from pynetappfoundry.cache.cloud.targets.model import CloudTargetInfo
from pynetappfoundry.cache.cluster.licensing.model import (
    CapacityLicense,
    LicenseFeature,
    LicenseInfo,
)
from pynetappfoundry.cache.cluster.mediators.mapping import MEDIATOR_MAPPING
from pynetappfoundry.cache.cluster.mediators.model import MediatorInfo
from pynetappfoundry.cache.cluster.model import ClusterInfo
from pynetappfoundry.cache.cluster.nodes.mapping import NODE_MAPPING
from pynetappfoundry.cache.cluster.nodes.model import NodeInfo
from pynetappfoundry.cache.cluster.peers.mapping import CLUSTER_PEER_MAPPING
from pynetappfoundry.cache.cluster.peers.model import ClusterPeer
from pynetappfoundry.cache.cluster.schedules.model import ScheduleInfo
from pynetappfoundry.cache.field_mapping import parse_api_response, parse_cli_records
from pynetappfoundry.cache.name_services.dns.model import DNSInfo
from pynetappfoundry.cache.network.ethernet.broadcast_domains.model import (
    BroadcastDomain,
)
from pynetappfoundry.cache.network.ip.interfaces.model import NetworkLIF
from pynetappfoundry.cache.network.ip.subnets.model import IPSubnetInfo
from pynetappfoundry.cache.network.model import NetworkInfo
from pynetappfoundry.cache.protocols.cifs.services.model import CIFSServiceInfo
from pynetappfoundry.cache.protocols.cifs.shares.model import CIFSShareInfo
from pynetappfoundry.cache.protocols.model import ProtocolsInfo
from pynetappfoundry.cache.protocols.nfs.export_policies.model import (
    ExportPolicyInfo,
    ExportRuleInfo,
)
from pynetappfoundry.cache.protocols.nfs.services.model import NFSServiceInfo
from pynetappfoundry.cache.protocols.s3.buckets.model import S3BucketInfo
from pynetappfoundry.cache.protocols.san.igroups.model import IgroupInfo
from pynetappfoundry.cache.snapmirror.relationships.mapping import SNAPMIRROR_MAPPING
from pynetappfoundry.cache.snapmirror.relationships.model import SnapMirrorRelationship
from pynetappfoundry.cache.storage.aggregates.mapping import AGGREGATE_MAPPING
from pynetappfoundry.cache.storage.aggregates.model import AggregateInfo
from pynetappfoundry.cache.storage.flexcache.model import FlexCacheInfo
from pynetappfoundry.cache.storage.luns.model import LunInfo
from pynetappfoundry.cache.storage.model import StorageInfo
from pynetappfoundry.cache.storage.qos.model import QosPolicyInfo
from pynetappfoundry.cache.storage.qtrees.model import QtreeInfo
from pynetappfoundry.cache.storage.snapshot_policies.model import (
    SnapshotPolicyInfo,
    SnapshotScheduleInfo,
)
from pynetappfoundry.cache.storage.volumes.mapping import VOLUME_MAPPING
from pynetappfoundry.cache.storage.volumes.model import VolumeInfo
from pynetappfoundry.cache.svm.model import SVMInfo
from pynetappfoundry.cache.svm.peers.model import SVMPeerInfo
from pynetappfoundry.utils.cloud import (
    build_cloud_instance_link,
    build_cloud_instance_sso_link,
    build_cloud_resource_group_link,
)

if TYPE_CHECKING:
    from pynetappfoundry.clients.ontap.api import ONTAPAPIClient
    from pynetappfoundry.clients.ontap.cli import ONTAPCLI

logger = logging.getLogger(__name__)


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

        # Enrich cluster info with is_ha (derived from node count)
        cluster_info: ClusterInfo = results["cluster"]
        cluster_info = cluster_info.model_copy(
            update={"is_ha": len(results["nodes"]) > 1},
        )

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
            licenses=results["licenses"],
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

        response = self._cached_api_call("/cluster?fields=*", paginate=False)
        if not response:
            return ClusterInfo()

        logger.debug(
            "%s API response: cluster=%s", self._log_prefix, response.get("name", "unknown")
        )
        self._log_missing_fields(
            response,
            ["name", "uuid", "version", "contact", "location"],
            "Cluster",
            response.get("name", "unknown"),
        )
        return ClusterInfo(
            cluster_name=response.get("name", ""),
            cluster_uuid=response.get("uuid", ""),
            ontap_version=response.get("version", {}).get("full", ""),
            model=response.get("version", {}).get("generation", ""),
            contact=response.get("contact", ""),
            location=response.get("location", ""),
        )

    # -------------------------------------------------------------------------
    # Node Collection
    # -------------------------------------------------------------------------

    def collect_nodes(self) -> list[NodeInfo]:
        """Collect node information (API-only).

        Returns:
            List of NodeInfo objects.

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

    def _collect_nodes_via_api(self) -> list[NodeInfo]:
        """Collect nodes using REST API.

        Returns:
            List of NodeInfo from /cluster/nodes endpoint.
        """
        if not self.api_client:
            logger.debug("%s No API client available for nodes collection", self._log_prefix)
            return []

        # Use cached API call to avoid duplicate requests (also used by HA collection)
        response = self._cached_api_call(NODE_MAPPING.api_endpoint)
        if not response:
            return []

        return cast(
            list[NodeInfo],
            parse_api_response(NODE_MAPPING, response, self._log_prefix, self._log_missing_fields),
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
            "/network/ip/interfaces?fields=*",
            "/network/ethernet/broadcast-domains?fields=*",
            "/network/ipspaces?fields=*",
            "/name-services/dns?fields=*",
            "/network/ip/subnets?fields=*",
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
        lifs_response = responses.get(endpoints[0]) or {}
        logger.debug(
            "%s API response: %d LIFs", self._log_prefix, len(lifs_response.get("records", []))
        )
        intercluster_lifs = []
        data_lifs = []
        management_lifs = []

        for record in lifs_response.get("records", []):
            self._log_missing_fields(
                record,
                ["name", "ip", "location", "svm", "scope", "services"],
                "LIF",
                record.get("name", record.get("uuid", "unknown")),
            )
            lif = NetworkLIF(
                name=record.get("name", ""),
                ip_address=record.get("ip", {}).get("address", ""),
                netmask=record.get("ip", {}).get("netmask", ""),
                home_node=record.get("location", {}).get("home_node", {}).get("name", ""),
                home_port=record.get("location", {}).get("home_port", {}).get("name", ""),
                svm=record.get("svm", {}).get("name", ""),
            )
            # Determine role from service_policy or scope
            scope = record.get("scope", "")
            if scope == "cluster":
                intercluster_lifs.append(lif)
            elif scope == "svm":
                if "data" in record.get("services", []):
                    data_lifs.append(lif)
                else:
                    data_lifs.append(lif)  # Default to data
            else:
                management_lifs.append(lif)

        # Process broadcast domains response
        bd_response = responses.get(endpoints[1]) or {}
        logger.debug(
            "%s API response: %d broadcast domains",
            self._log_prefix,
            len(bd_response.get("records", [])),
        )
        broadcast_domains = []
        for record in bd_response.get("records", []):
            self._log_missing_fields(
                record,
                ["uuid", "name", "ipspace", "mtu", "ports"],
                "BroadcastDomain",
                record.get("name", record.get("uuid", "unknown")),
            )
            bd = BroadcastDomain(
                uuid=record.get("uuid", ""),
                name=record.get("name", ""),
                ipspace=record.get("ipspace", {}).get("name", ""),
                mtu=record.get("mtu", 0),
                ports=[p.get("name", "") for p in record.get("ports", []) if p.get("name")],
            )
            broadcast_domains.append(bd)

        # Process IPspaces response
        ipspace_response = responses.get(endpoints[2]) or {}
        logger.debug(
            "%s API response: %d IPspaces",
            self._log_prefix,
            len(ipspace_response.get("records", [])),
        )
        ipspaces = [r.get("name", "") for r in ipspace_response.get("records", [])]

        # Process DNS response
        dns = self._parse_dns_response(responses.get(endpoints[3]))

        # Process subnets response
        subnets = self._parse_subnets_response(responses.get(endpoints[4]))

        return NetworkInfo(
            intercluster_lifs=intercluster_lifs,
            data_lifs=data_lifs,
            management_lifs=management_lifs,
            broadcast_domains=broadcast_domains,
            ipspaces=ipspaces,
            dns=dns,
            subnets=subnets,
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
            AGGREGATE_MAPPING.api_endpoint,
            "/svm/svms?fields=*",
            "/cloud/targets?fields=*",
            "/storage/volumes?fields=*,autosize,files,nas.path,nas.security_style",
            "/storage/qtrees?fields=*",
            "/storage/snapshot-policies?fields=*,copies",
            "/cluster/schedules?fields=*",
            "/storage/luns?fields=*",
            "/protocols/san/igroups?fields=*",
            "/storage/qos/policies?fields=*",
            "/storage/flexcache/flexcaches?fields=*",
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
            list[AggregateInfo],
            parse_api_response(
                AGGREGATE_MAPPING,
                responses.get(endpoints[0]),
                self._log_prefix,
                self._log_missing_fields,
            ),
        )

        # Process SVMs response
        svm_response = responses.get(endpoints[1]) or {}
        logger.debug(
            "%s API response: %d SVMs", self._log_prefix, len(svm_response.get("records", []))
        )
        svms = []
        for record in svm_response.get("records", []):
            self._log_missing_fields(
                record,
                ["uuid", "name", "state", "subtype", "allowed_protocols", "language"],
                "SVM",
                record.get("name", record.get("uuid", "unknown")),
            )
            svm = SVMInfo(
                uuid=record.get("uuid", ""),
                name=record.get("name", ""),
                state=record.get("state", ""),
                subtype=record.get("subtype", ""),
                allowed_protocols=record.get("allowed_protocols", []) or [],
                language=record.get("language", ""),
            )
            svms.append(svm)

        # Process cloud targets response
        cloud_targets = self._parse_cloud_targets_response(responses.get(endpoints[2]))

        # Process volumes response
        volumes = self._parse_volumes_response(responses.get(endpoints[3]))

        # Process qtrees response
        qtrees = self._parse_qtrees_response(responses.get(endpoints[4]))

        # Process snapshot policies response
        snapshot_policies = self._parse_snapshot_policies_response(responses.get(endpoints[5]))

        # Process schedules response
        schedules = self._parse_schedules_response(responses.get(endpoints[6]))

        # Process LUNs response
        luns = self._parse_luns_response(responses.get(endpoints[7]))

        # Process igroups response
        igroups = self._parse_igroups_response(responses.get(endpoints[8]))

        # Process QoS policies response
        qos_policies = self._parse_qos_policies_response(responses.get(endpoints[9]))

        # Process FlexCache response
        flexcaches = self._parse_flexcaches_response(responses.get(endpoints[10]))

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

    def _parse_cloud_targets_response(self, response: Any) -> list[CloudTargetInfo]:
        """Parse cloud targets API response.

        Args:
            response: API response dict or None.

        Returns:
            List of CloudTargetInfo objects.
        """
        if not response:
            return []

        logger.debug(
            "%s API response: %d cloud targets", self._log_prefix, len(response.get("records", []))
        )
        cloud_targets = []
        for record in response.get("records", []):
            self._log_missing_fields(
                record,
                [
                    "name",
                    "uuid",
                    "provider_type",
                    "server",
                    "container",
                    "owner",
                    "scope",
                    "svm",
                    "ssl_enabled",
                    "authentication_type",
                    "ipspace",
                    "snapmirror_use",
                ],
                "CloudTarget",
                record.get("name", record.get("uuid", "unknown")),
            )
            target = CloudTargetInfo(
                name=record.get("name", ""),
                uuid=record.get("uuid", ""),
                provider_type=record.get("provider_type", ""),
                server=record.get("server", ""),
                container=record.get("container", ""),
                owner=record.get("owner", ""),
                scope=record.get("scope", ""),
                svm=record.get("svm", {}).get("name", "") if record.get("svm") else "",
                ssl_enabled=record.get("ssl_enabled", True),
                authentication_type=record.get("authentication_type", ""),
                ipspace=record.get("ipspace", {}).get("name", "") if record.get("ipspace") else "",
                snapmirror_use=record.get("snapmirror_use", ""),
                access_key=record.get("access_key", ""),
                azure_account=record.get("azure_account", ""),
            )
            cloud_targets.append(target)
        return cloud_targets

    # -------------------------------------------------------------------------
    # License Collection
    # -------------------------------------------------------------------------

    def collect_licenses(self) -> LicenseInfo:
        """Collect licensing information (API-only).

        Returns:
            LicenseInfo object.

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

    def _collect_licenses_via_api(self) -> LicenseInfo:
        """Collect licenses using REST API.

        Returns:
            LicenseInfo from /cluster/licensing/licenses endpoint.
        """
        if not self.api_client:
            logger.debug("%s No API client available for license collection", self._log_prefix)
            return LicenseInfo()

        response = self._cached_api_call("/cluster/licensing/licenses?fields=*")
        if not response:
            return LicenseInfo()

        logger.debug(
            "%s API response: %d licenses", self._log_prefix, len(response.get("records", []))
        )
        feature_licenses = []
        capacity_licenses = []

        for record in response.get("records", []):
            self._log_missing_fields(
                record,
                ["name", "state", "scope", "capacity"],
                "License",
                record.get("name", "unknown"),
            )
            name = record.get("name", "")
            state = record.get("state", "")
            scope = record.get("scope", "")

            # Check if it's a capacity license
            capacity = record.get("capacity", {})
            if capacity.get("maximum_size"):
                cap_license = CapacityLicense(
                    name=name,
                    licensed_capacity=capacity.get("maximum_size", 0),
                    used_capacity=capacity.get("used_size", 0),
                )
                capacity_licenses.append(cap_license)
            else:
                feature = LicenseFeature(name=name, state=state, scope=scope)
                feature_licenses.append(feature)

        return LicenseInfo(feature_licenses=feature_licenses, capacity_licenses=capacity_licenses)

    # -------------------------------------------------------------------------
    # Mediator Collection
    # -------------------------------------------------------------------------

    def collect_mediator(self) -> MediatorInfo:
        """Collect ONTAP Mediator information (API-only).

        Returns:
            MediatorInfo object.

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

    def _collect_mediator_via_api(self) -> MediatorInfo:
        """Collect mediator info using REST API.

        Returns:
            MediatorInfo from /cluster/mediators endpoint.
        """
        try:
            mediator_response = self._cached_api_call(MEDIATOR_MAPPING.api_endpoint)
            parsed = parse_api_response(
                MEDIATOR_MAPPING, mediator_response, self._log_prefix, self._log_missing_fields
            )
            if parsed:
                return cast(MediatorInfo, parsed[0])
        except Exception as e:
            logger.debug("%s Mediator endpoint not available: %s", self._log_prefix, e)

        return MediatorInfo()

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
            SNAPMIRROR_MAPPING.api_endpoint,
            "/cluster/peers?fields=*",
            "/svm/peers?fields=*",
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
            list[SnapMirrorRelationship],
            parse_api_response(
                SNAPMIRROR_MAPPING,
                responses.get(endpoints[0]),
                self._log_prefix,
                self._log_missing_fields,
            ),
        )

        # Process cluster peers
        cluster_peers = self._parse_cluster_peers_response(responses.get(endpoints[1]))

        # Process SVM peers
        svm_peers = self._parse_svm_peers_response(responses.get(endpoints[2]))

        return RelationshipsInfo(
            snapmirror_destinations=snapmirror_destinations,
            cluster_peers=cluster_peers,
            svm_peers=svm_peers,
        )

    # -------------------------------------------------------------------------
    # Volume Parsing
    # -------------------------------------------------------------------------

    def _parse_volumes_response(self, response: Any) -> list[VolumeInfo]:
        """Parse volumes API response.

        Delegates to the declarative field mapping framework.

        Args:
            response: API response dict or None.

        Returns:
            List of VolumeInfo objects.
        """
        results = parse_api_response(
            VOLUME_MAPPING, response, self._log_prefix, self._log_missing_fields
        )
        return cast(list[VolumeInfo], results)

    # -------------------------------------------------------------------------
    # Cluster Peer Parsing
    # -------------------------------------------------------------------------

    def _parse_cluster_peers_response(self, response: Any) -> list[ClusterPeer]:
        """Parse cluster peers API response.

        Delegates to the declarative field mapping framework.

        Args:
            response: API response dict or None.

        Returns:
            List of ClusterPeer objects.
        """
        results = parse_api_response(
            CLUSTER_PEER_MAPPING, response, self._log_prefix, self._log_missing_fields
        )
        return cast(list[ClusterPeer], results)

    def _parse_qtrees_response(self, response: Any) -> list[QtreeInfo]:
        """Parse qtrees API response.

        Args:
            response: API response dict or None.

        Returns:
            List of QtreeInfo objects.
        """
        if not response:
            return []

        logger.debug(
            "%s API response: %d qtrees", self._log_prefix, len(response.get("records", []))
        )
        qtrees = []
        for record in response.get("records", []):
            self._log_missing_fields(
                record,
                [
                    "id",
                    "name",
                    "svm",
                    "volume",
                    "path",
                    "security_style",
                    "unix_permissions",
                    "export_policy",
                ],
                "Qtree",
                record.get("name", str(record.get("id", "unknown"))),
            )
            qtree = QtreeInfo(
                id=record.get("id", 0),
                name=record.get("name", ""),
                svm=record.get("svm", {}).get("name", "") if record.get("svm") else "",
                volume=record.get("volume", {}).get("name", "") if record.get("volume") else "",
                path=record.get("path", ""),
                security_style=record.get("security_style", ""),
                unix_permissions=str(record.get("unix_permissions", "")),
                export_policy=(
                    record.get("export_policy", {}).get("name", "")
                    if record.get("export_policy")
                    else ""
                ),
            )
            qtrees.append(qtree)
        return qtrees

    def _parse_snapshot_policies_response(self, response: Any) -> list[SnapshotPolicyInfo]:
        """Parse snapshot policies API response.

        Args:
            response: API response dict or None.

        Returns:
            List of SnapshotPolicyInfo objects.
        """
        if not response:
            return []

        logger.debug(
            "%s API response: %d snapshot policies",
            self._log_prefix,
            len(response.get("records", [])),
        )
        policies = []
        for record in response.get("records", []):
            self._log_missing_fields(
                record,
                ["uuid", "name", "svm", "enabled", "scope", "copies"],
                "SnapshotPolicy",
                record.get("name", record.get("uuid", "unknown")),
            )
            schedules = []
            for copy in record.get("copies", []):
                sched = SnapshotScheduleInfo(
                    schedule=(
                        copy.get("schedule", {}).get("name", "")
                        if isinstance(copy.get("schedule"), dict)
                        else str(copy.get("schedule", ""))
                    ),
                    count=copy.get("count", 0),
                    prefix=copy.get("prefix", ""),
                    snapmirror_label=copy.get("snapmirror_label", ""),
                )
                schedules.append(sched)

            policy = SnapshotPolicyInfo(
                uuid=record.get("uuid", ""),
                name=record.get("name", ""),
                svm=record.get("svm", {}).get("name", "") if record.get("svm") else "",
                enabled=record.get("enabled", True),
                scope=record.get("scope", ""),
                schedules=schedules,
            )
            policies.append(policy)
        return policies

    def _parse_schedules_response(self, response: Any) -> list[ScheduleInfo]:
        """Parse cluster schedules API response.

        Args:
            response: API response dict or None.

        Returns:
            List of ScheduleInfo objects.
        """
        if not response:
            return []

        logger.debug(
            "%s API response: %d schedules", self._log_prefix, len(response.get("records", []))
        )
        schedules = []
        for record in response.get("records", []):
            self._log_missing_fields(
                record,
                ["uuid", "name", "type", "scope", "svm", "cron", "interval"],
                "Schedule",
                record.get("name", record.get("uuid", "unknown")),
            )
            cron = record.get("cron", {}) or {}
            schedule = ScheduleInfo(
                uuid=record.get("uuid", ""),
                name=record.get("name", ""),
                type=record.get("type", ""),
                scope=record.get("scope", ""),
                svm=record.get("svm", {}).get("name", "") if record.get("svm") else "",
                cron=cron,
                interval=record.get("interval", ""),
            )
            schedules.append(schedule)
        return schedules

    def _parse_luns_response(self, response: Any) -> list[LunInfo]:
        """Parse LUNs API response.

        Args:
            response: API response dict or None.

        Returns:
            List of LunInfo objects.
        """
        if not response:
            return []

        logger.debug("%s API response: %d LUNs", self._log_prefix, len(response.get("records", [])))
        luns = []
        for record in response.get("records", []):
            self._log_missing_fields(
                record,
                [
                    "uuid",
                    "name",
                    "svm",
                    "location",
                    "space",
                    "os_type",
                    "serial_number",
                    "enabled",
                    "comment",
                    "qos_policy",
                    "create_time",
                ],
                "LUN",
                record.get("name", record.get("uuid", "unknown")),
            )
            location = record.get("location", {})
            lun = LunInfo(
                uuid=record.get("uuid", ""),
                name=record.get("name", ""),
                svm=record.get("svm", {}).get("name", "") if record.get("svm") else "",
                volume=(
                    location.get("volume", {}).get("name", "") if location.get("volume") else ""
                ),
                size=record.get("space", {}).get("size", 0),
                os_type=record.get("os_type", ""),
                serial_number=record.get("serial_number", ""),
                enabled=record.get("enabled", True),
                comment=record.get("comment", "") or "",
                qos_policy=(
                    record.get("qos_policy", {}).get("name", "") if record.get("qos_policy") else ""
                ),
                create_time=record.get("create_time", ""),
            )
            luns.append(lun)
        return luns

    def _parse_igroups_response(self, response: Any) -> list[IgroupInfo]:
        """Parse igroups API response.

        Args:
            response: API response dict or None.

        Returns:
            List of IgroupInfo objects.
        """
        if not response:
            return []

        logger.debug(
            "%s API response: %d igroups", self._log_prefix, len(response.get("records", []))
        )
        igroups = []
        for record in response.get("records", []):
            self._log_missing_fields(
                record,
                ["uuid", "name", "svm", "protocol", "os_type", "initiators", "comment"],
                "Igroup",
                record.get("name", record.get("uuid", "unknown")),
            )
            initiators = [i.get("name", "") for i in record.get("initiators", []) if i.get("name")]
            igroup = IgroupInfo(
                uuid=record.get("uuid", ""),
                name=record.get("name", ""),
                svm=record.get("svm", {}).get("name", "") if record.get("svm") else "",
                protocol=record.get("protocol", ""),
                os_type=record.get("os_type", ""),
                initiators=initiators,
                comment=record.get("comment", "") or "",
            )
            igroups.append(igroup)
        return igroups

    def _parse_qos_policies_response(self, response: Any) -> list[QosPolicyInfo]:
        """Parse QoS policies API response.

        Args:
            response: API response dict or None.

        Returns:
            List of QosPolicyInfo objects.
        """
        if not response:
            return []

        logger.debug(
            "%s API response: %d QoS policies",
            self._log_prefix,
            len(response.get("records", [])),
        )
        policies = []
        for record in response.get("records", []):
            self._log_missing_fields(
                record,
                ["uuid", "name", "svm", "scope", "object_type", "fixed", "adaptive"],
                "QoSPolicy",
                record.get("name", record.get("uuid", "unknown")),
            )
            fixed = record.get("fixed", {}) or {}
            adaptive = record.get("adaptive", {}) or {}
            max_throughput_iops = fixed.get("max_throughput_iops", 0)
            max_throughput_mbps = fixed.get("max_throughput_mbps", 0)
            policy = QosPolicyInfo(
                uuid=record.get("uuid", ""),
                name=record.get("name", ""),
                svm=record.get("svm", {}).get("name", "") if record.get("svm") else "",
                scope=record.get("scope", ""),
                policy_class=record.get("object_type", ""),
                fixed_max_throughput_iops=max_throughput_iops if max_throughput_iops else 0,
                fixed_max_throughput_mbps=max_throughput_mbps if max_throughput_mbps else 0,
                adaptive_expected_iops=adaptive.get("expected_iops", 0) or 0,
                adaptive_peak_iops=adaptive.get("peak_iops", 0) or 0,
                adaptive_block_size=adaptive.get("block_size", ""),
            )
            policies.append(policy)
        return policies

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
            "/protocols/nfs/export-policies?fields=*,rules",
            "/protocols/cifs/shares?fields=*",
            "/protocols/nfs/services?fields=*",
            "/protocols/cifs/services?fields=*",
            "/protocols/s3/buckets?fields=*",
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

        export_policies = self._parse_export_policies_response(responses.get(endpoints[0]))
        cifs_shares = self._parse_cifs_shares_response(responses.get(endpoints[1]))
        nfs_services = self._parse_nfs_services_response(responses.get(endpoints[2]))
        cifs_services = self._parse_cifs_services_response(responses.get(endpoints[3]))
        s3_buckets = self._parse_s3_buckets_response(responses.get(endpoints[4]))

        return ProtocolsInfo(
            export_policies=export_policies,
            cifs_shares=cifs_shares,
            nfs_services=nfs_services,
            cifs_services=cifs_services,
            s3_buckets=s3_buckets,
        )

    def _parse_export_policies_response(self, response: Any) -> list[ExportPolicyInfo]:
        """Parse export policies API response.

        Args:
            response: API response dict or None.

        Returns:
            List of ExportPolicyInfo objects.
        """
        if not response:
            return []

        logger.debug(
            "%s API response: %d export policies",
            self._log_prefix,
            len(response.get("records", [])),
        )
        policies = []
        for record in response.get("records", []):
            self._log_missing_fields(
                record,
                ["id", "name", "svm", "rules"],
                "ExportPolicy",
                record.get("name", str(record.get("id", "unknown"))),
            )
            rules = []
            for rule_record in record.get("rules", []):
                rule = ExportRuleInfo(
                    index=rule_record.get("index", 0),
                    clients=[
                        c.get("match", "") for c in rule_record.get("clients", []) if c.get("match")
                    ],
                    protocols=rule_record.get("protocols", []) or [],
                    ro_rule=rule_record.get("ro_rule", []) or [],
                    rw_rule=rule_record.get("rw_rule", []) or [],
                    superuser=rule_record.get("superuser", []) or [],
                    anonymous_user=rule_record.get("anonymous_user", ""),
                )
                rules.append(rule)

            policy = ExportPolicyInfo(
                id=record.get("id", 0),
                name=record.get("name", ""),
                svm=record.get("svm", {}).get("name", "") if record.get("svm") else "",
                rules=rules,
            )
            policies.append(policy)
        return policies

    def _parse_cifs_shares_response(self, response: Any) -> list[CIFSShareInfo]:
        """Parse CIFS shares API response.

        Args:
            response: API response dict or None.

        Returns:
            List of CIFSShareInfo objects.
        """
        if not response:
            return []

        logger.debug(
            "%s API response: %d CIFS shares",
            self._log_prefix,
            len(response.get("records", [])),
        )
        shares = []
        for record in response.get("records", []):
            self._log_missing_fields(
                record,
                [
                    "name",
                    "path",
                    "svm",
                    "comment",
                    "home_directory",
                    "oplocks",
                    "access_based_enumeration",
                    "change_notify",
                    "encryption",
                    "unix_symlink",
                ],
                "CIFSShare",
                record.get("name", "unknown"),
            )
            share = CIFSShareInfo(
                name=record.get("name", ""),
                path=record.get("path", ""),
                svm=record.get("svm", {}).get("name", "") if record.get("svm") else "",
                comment=record.get("comment", "") or "",
                home_directory=record.get("home_directory", False),
                oplocks=record.get("oplocks", True),
                access_based_enumeration=record.get("access_based_enumeration", False),
                change_notify=record.get("change_notify", True),
                encryption=record.get("encryption", False),
                unix_symlink=record.get("unix_symlink", ""),
            )
            shares.append(share)
        return shares

    def _parse_nfs_services_response(self, response: Any) -> list[NFSServiceInfo]:
        """Parse NFS services API response.

        Args:
            response: API response dict or None.

        Returns:
            List of NFSServiceInfo objects.
        """
        if not response:
            return []

        logger.debug(
            "%s API response: %d NFS services",
            self._log_prefix,
            len(response.get("records", [])),
        )
        services = []
        for record in response.get("records", []):
            self._log_missing_fields(
                record,
                ["svm", "enabled", "protocol", "showmount_enabled", "vstorage_enabled"],
                "NFSService",
                record.get("svm", {}).get("name", "unknown")
                if isinstance(record.get("svm"), dict)
                else "unknown",
            )
            protocol = record.get("protocol", {})
            service = NFSServiceInfo(
                svm=record.get("svm", {}).get("name", "") if record.get("svm") else "",
                enabled=record.get("enabled", False),
                protocol_v3_enabled=protocol.get("v3_enabled", False),
                protocol_v4_enabled=protocol.get("v40_enabled", False),
                protocol_v41_enabled=protocol.get("v41_enabled", False),
                showmount_enabled=record.get("showmount_enabled", False),
                vstorage_enabled=record.get("vstorage_enabled", False),
            )
            services.append(service)
        return services

    def _parse_cifs_services_response(self, response: Any) -> list[CIFSServiceInfo]:
        """Parse CIFS services API response.

        Args:
            response: API response dict or None.

        Returns:
            List of CIFSServiceInfo objects.
        """
        if not response:
            return []

        logger.debug(
            "%s API response: %d CIFS services",
            self._log_prefix,
            len(response.get("records", [])),
        )
        services = []
        for record in response.get("records", []):
            self._log_missing_fields(
                record,
                ["svm", "name", "enabled", "ad_domain", "comment", "default_unix_user", "netbios"],
                "CIFSService",
                record.get("name", "unknown"),
            )
            ad_domain = record.get("ad_domain", {})
            service = CIFSServiceInfo(
                svm=record.get("svm", {}).get("name", "") if record.get("svm") else "",
                name=record.get("name", ""),
                enabled=record.get("enabled", False),
                ad_domain=ad_domain.get("fqdn", "")
                if isinstance(ad_domain, dict)
                else str(ad_domain or ""),
                comment=record.get("comment", "") or "",
                default_unix_user=record.get("default_unix_user", ""),
                netbios_aliases=record.get("netbios", {}).get("aliases", []) or []
                if record.get("netbios")
                else [],
            )
            services.append(service)
        return services

    def _parse_dns_response(self, response: Any) -> list[DNSInfo]:
        """Parse DNS API response.

        Args:
            response: API response dict or None.

        Returns:
            List of DNSInfo objects.
        """
        if not response:
            return []

        logger.debug(
            "%s API response: %d DNS configs",
            self._log_prefix,
            len(response.get("records", [])),
        )
        dns_configs = []
        for record in response.get("records", []):
            self._log_missing_fields(
                record,
                ["uuid", "svm", "scope", "domains", "servers", "timeout", "attempts"],
                "DNS",
                record.get("svm", {}).get("name", record.get("uuid", "unknown"))
                if isinstance(record.get("svm"), dict)
                else record.get("uuid", "unknown"),
            )
            dns = DNSInfo(
                uuid=record.get("uuid", ""),
                svm=record.get("svm", {}).get("name", "") if record.get("svm") else "",
                scope=record.get("scope", ""),
                domains=record.get("domains", []) or [],
                servers=record.get("servers", []) or [],
                timeout=record.get("timeout", 0),
                attempts=record.get("attempts", 0),
            )
            dns_configs.append(dns)
        return dns_configs

    def _parse_subnets_response(self, response: Any) -> list[IPSubnetInfo]:
        """Parse IP subnets API response.

        Args:
            response: API response dict or None.

        Returns:
            List of IPSubnetInfo objects.
        """
        if not response:
            return []

        logger.debug(
            "%s API response: %d subnets", self._log_prefix, len(response.get("records", []))
        )
        subnets = []
        for record in response.get("records", []):
            self._log_missing_fields(
                record,
                ["uuid", "name", "ipspace", "broadcast_domain", "subnet", "gateway", "ip_ranges"],
                "IPSubnet",
                record.get("name", record.get("uuid", "unknown")),
            )
            ip_ranges = []
            for r in record.get("ip_ranges", []):
                if isinstance(r, dict):
                    start = r.get("start", "")
                    end = r.get("end", "")
                    if start and end:
                        ip_ranges.append(f"{start}-{end}")
                    elif start:
                        ip_ranges.append(start)
                elif isinstance(r, str):
                    ip_ranges.append(r)

            subnet_obj = record.get("subnet", {})
            if subnet_obj:
                subnet_str = (
                    subnet_obj.get("address", "") + "/" + str(subnet_obj.get("netmask", ""))
                )
            else:
                subnet_str = ""

            subnet = IPSubnetInfo(
                uuid=record.get("uuid", ""),
                name=record.get("name", ""),
                ipspace=(
                    record.get("ipspace", {}).get("name", "") if record.get("ipspace") else ""
                ),
                broadcast_domain=(
                    record.get("broadcast_domain", {}).get("name", "")
                    if record.get("broadcast_domain")
                    else ""
                ),
                subnet=subnet_str,
                gateway=record.get("gateway", ""),
                ip_ranges=ip_ranges,
            )
            subnets.append(subnet)
        return subnets

    def _parse_flexcaches_response(self, response: Any) -> list[FlexCacheInfo]:
        """Parse FlexCache volumes API response.

        Args:
            response: API response dict or None.

        Returns:
            List of FlexCacheInfo objects.
        """
        if not response:
            return []

        logger.debug(
            "%s API response: %d FlexCache volumes",
            self._log_prefix,
            len(response.get("records", [])),
        )
        flexcaches = []
        for record in response.get("records", []):
            self._log_missing_fields(
                record,
                [
                    "uuid",
                    "name",
                    "svm",
                    "path",
                    "size",
                    "origins",
                    "global_file_locking_enabled",
                    "dr_cache",
                ],
                "FlexCache",
                record.get("name", record.get("uuid", "unknown")),
            )
            origins = []
            for origin in record.get("origins", []):
                vol = origin.get("volume", {})
                svm = origin.get("svm", {})
                vol_name = vol.get("name", "") if isinstance(vol, dict) else str(vol or "")
                svm_name = svm.get("name", "") if isinstance(svm, dict) else str(svm or "")
                if svm_name and vol_name:
                    origins.append(f"{svm_name}:{vol_name}")
                elif vol_name:
                    origins.append(vol_name)

            fc = FlexCacheInfo(
                uuid=record.get("uuid", ""),
                name=record.get("name", ""),
                svm=record.get("svm", {}).get("name", "") if record.get("svm") else "",
                path=record.get("path", ""),
                size=record.get("size", 0),
                origins=origins,
                global_file_locking_enabled=record.get("global_file_locking_enabled", False),
                dr_cache=record.get("dr_cache", False),
            )
            flexcaches.append(fc)
        return flexcaches

    def _parse_svm_peers_response(self, response: Any) -> list[SVMPeerInfo]:
        """Parse SVM peers API response.

        Args:
            response: API response dict or None.

        Returns:
            List of SVMPeerInfo objects.
        """
        if not response:
            return []

        logger.debug(
            "%s API response: %d SVM peers", self._log_prefix, len(response.get("records", []))
        )
        peers = []
        for record in response.get("records", []):
            self._log_missing_fields(
                record,
                ["uuid", "name", "svm", "peer", "state", "applications"],
                "SVMPeer",
                record.get("name", record.get("uuid", "unknown")),
            )
            svm = record.get("svm", {})
            peer_obj = record.get("peer", {})
            peer = SVMPeerInfo(
                uuid=record.get("uuid", ""),
                name=record.get("name", ""),
                svm=svm.get("name", "") if isinstance(svm, dict) else str(svm or ""),
                peer_svm=(
                    peer_obj.get("svm", {}).get("name", "")
                    if isinstance(peer_obj, dict) and isinstance(peer_obj.get("svm"), dict)
                    else ""
                ),
                peer_cluster=(
                    peer_obj.get("cluster", {}).get("name", "")
                    if isinstance(peer_obj, dict) and isinstance(peer_obj.get("cluster"), dict)
                    else ""
                ),
                state=record.get("state", ""),
                applications=record.get("applications", []) or [],
            )
            peers.append(peer)
        return peers

    def _parse_s3_buckets_response(self, response: Any) -> list[S3BucketInfo]:
        """Parse S3 buckets API response.

        Args:
            response: API response dict or None.

        Returns:
            List of S3BucketInfo objects.
        """
        if not response:
            return []

        logger.debug(
            "%s API response: %d S3 buckets", self._log_prefix, len(response.get("records", []))
        )
        buckets = []
        for record in response.get("records", []):
            self._log_missing_fields(
                record,
                ["uuid", "name", "svm", "type", "size", "versioning_state", "comment", "nas_path"],
                "S3Bucket",
                record.get("name", record.get("uuid", "unknown")),
            )
            bucket = S3BucketInfo(
                uuid=record.get("uuid", ""),
                name=record.get("name", ""),
                svm=record.get("svm", {}).get("name", "") if record.get("svm") else "",
                type=record.get("type", ""),
                size=record.get("size", 0),
                versioning_state=record.get("versioning_state", ""),
                comment=record.get("comment", "") or "",
                nas_path=record.get("nas_path", ""),
            )
            buckets.append(bucket)
        return buckets
