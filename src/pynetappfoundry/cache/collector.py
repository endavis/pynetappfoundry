"""Metadata collector for ONTAP clusters.

Collects cluster metadata using REST API (primary) with CLI fallback.
Optimized for performance with parallel API calls and response caching.
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

from pynetappfoundry.cache.field_mapping import parse_api_response
from pynetappfoundry.cache.mappings.volume import VOLUME_MAPPING
from pynetappfoundry.cache.models import (
    AggregateInfo,
    BroadcastDomain,
    CachedClusterMetadata,
    CapacityLicense,
    CIFSServiceInfo,
    CIFSShareInfo,
    CloudMetadata,
    CloudTargetInfo,
    ClusterInfo,
    ClusterPeer,
    DNSInfo,
    ExportPolicyInfo,
    ExportRuleInfo,
    FlexCacheInfo,
    HAInfo,
    IgroupInfo,
    IPSubnetInfo,
    LicenseFeature,
    LicenseInfo,
    LunInfo,
    NetworkInfo,
    NetworkLIF,
    NFSServiceInfo,
    NodeInfo,
    ProtocolsInfo,
    QosPolicyInfo,
    QtreeInfo,
    RelationshipsInfo,
    S3BucketInfo,
    ScheduleInfo,
    SnapMirrorRelationship,
    SnapshotPolicyInfo,
    SnapshotScheduleInfo,
    StorageInfo,
    SVMInfo,
    SVMPeerInfo,
    VolumeInfo,
)
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
    HA = "ha"
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

    Uses REST API as primary data source with CLI fallback for
    endpoints not available in REST (e.g., virtual-machine instance show).
    """

    # Human-readable names for collection phases
    PHASE_NAMES: ClassVar[dict[CollectionPhase, str]] = {
        CollectionPhase.CLOUD: "Cloud metadata",
        CollectionPhase.CLUSTER: "Cluster info",
        CollectionPhase.NODES: "Nodes",
        CollectionPhase.NETWORK: "Network",
        CollectionPhase.STORAGE: "Storage",
        CollectionPhase.LICENSES: "Licenses",
        CollectionPhase.HA: "HA info",
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

    def _cached_api_call(self, endpoint: str, method: str = "GET") -> Any:
        """Make an API call with caching to avoid duplicate requests.

        Args:
            endpoint: The API endpoint to call.
            method: HTTP method (default GET).

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

        # Post-process Azure cloud metadata to fix instance links
        ha_info: HAInfo = results["ha"]
        cloud_metadata = self._update_azure_cloud_links(
            results["cloud"],
            cluster_name,
            ha_info.is_ha,
        )

        return CachedClusterMetadata(
            cluster_name=cluster_name,
            cached_at=datetime.now(UTC),
            cloud=cloud_metadata,
            cluster=results["cluster"],
            nodes=results["nodes"],
            network=results["network"],
            storage=results["storage"],
            licenses=results["licenses"],
            ha=results["ha"],
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
            (CollectionPhase.HA, self.collect_ha_info),
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
                    "%s Failed to collect %s: %s",
                    self._log_prefix,
                    phase.value,
                    error_msg,
                    exc_info=True,
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
            (CollectionPhase.HA, self.collect_ha_info),
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
        # All others prefer API
        if self.api_client:
            return "api"
        if self.cli_client:
            return "cli"
        return None

    def _log_missing_fields(
        self,
        record: dict[str, Any],
        expected_fields: list[str],
        record_type: str,
        record_id: str,
    ) -> None:
        """Log debug messages for expected API fields missing from a record.

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
                logger.debug(
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
        Returns one CloudMetadata per node in the cluster.

        Returns:
            List of CloudMetadata objects, one per node.
        """
        if self.cli_client:
            try:
                return self._collect_cloud_metadata_via_cli()
            except Exception as e:
                logger.warning(f"{self._log_prefix} Failed to collect cloud metadata via CLI: {e}")
        return []

    def _collect_cloud_metadata_via_cli(self) -> list[CloudMetadata]:
        """Collect cloud metadata using CLI.

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
        return self._parse_vm_instance_output(output)

    def _parse_vm_instance_output(self, output: list[str]) -> list[CloudMetadata]:
        """Parse virtual-machine instance show output.

        The CLI output contains entries for each node, separated by blank lines
        or new "Node:" entries. Each node has its own cloud metadata.

        Args:
            output: Lines of CLI output.

        Returns:
            List of CloudMetadata objects, one per node.
        """
        results: list[CloudMetadata] = []
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
                    results.append(self._create_cloud_metadata(current_node, current_data))
                # Start new node
                current_node = value
                current_data = {}
            else:
                current_data[key_normalized] = value

        # Don't forget the last node
        if current_node and current_data:
            results.append(self._create_cloud_metadata(current_node, current_data))

        # If no node field was found but we have data, create single entry
        if not results and current_data:
            results.append(self._create_cloud_metadata("", current_data))

        return results

    def _create_cloud_metadata(self, node: str, data: dict[str, str]) -> CloudMetadata:
        """Create a CloudMetadata object from parsed data.

        Args:
            node: Node name.
            data: Parsed key-value data.

        Returns:
            CloudMetadata object.
        """
        self._log_missing_fields(
            data,
            [
                "instance_id",
                "account_id",
                "instance_type",
                "region",
                "provider",
                "primary_ip",
            ],
            "CloudMetadata",
            node or "unknown",
        )
        provider = data.get("provider", "")
        instance_id = data.get("instance_id", "")
        account_id = data.get("account_id", "")
        resource_group = data.get("resource_group_name", "")
        region = data.get("region", "") or data.get("availability_zone", "")

        # Build cloud console links
        instance_link = build_cloud_instance_link(
            provider=provider,
            instance_id=instance_id,
            region=region,
            account_id=account_id,
            resource_group=resource_group,
        )
        instance_sso_link = build_cloud_instance_sso_link(
            provider=provider,
            instance_link=instance_link,
            account_id=account_id,
            sso_config=self.aws_sso_config,
        )
        resource_group_link = build_cloud_resource_group_link(
            provider=provider,
            account_id=account_id,
            resource_group=resource_group,
        )

        return CloudMetadata(
            node=node,
            instance_id=instance_id,
            account_id=account_id,
            image_id=data.get("image_id", ""),
            instance_type=data.get("instance_type", ""),
            cpu_platform=data.get("cpu_platform", ""),
            region=data.get("region", ""),
            provider=provider,
            consumer=data.get("consumer", ""),
            primary_ip=data.get("primary_ip", ""),
            metadata_version=data.get("metadata_version", ""),
            availability_zone=data.get("availability_zone", ""),
            availability_zone_id=data.get("availability_zone_id", ""),
            fault_domain=data.get("fault_domain", ""),
            update_domain=data.get("update_domain", ""),
            resource_group_name=resource_group,
            offer=data.get("offer", ""),
            sku=data.get("sku", ""),
            sku_version=data.get("sku_version", ""),
            instance_link=instance_link,
            instance_sso_link=instance_sso_link,
            resource_group_link=resource_group_link,
        )

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
        """Collect cluster identity information.

        Returns:
            ClusterInfo object.
        """
        # Try API first
        if self.api_client:
            try:
                return self._collect_cluster_info_via_api()
            except Exception as e:
                logger.warning(f"{self._log_prefix} Failed to collect cluster info via API: {e}")

        # Fall back to CLI
        if self.cli_client:
            try:
                return self._collect_cluster_info_via_cli()
            except Exception as e:
                logger.warning(f"{self._log_prefix} Failed to collect cluster info via CLI: {e}")

        return ClusterInfo()

    def _collect_cluster_info_via_api(self) -> ClusterInfo:
        """Collect cluster info using REST API.

        Returns:
            ClusterInfo from /cluster endpoint.
        """
        if not self.api_client:
            logger.debug("%s No API client available for cluster info collection", self._log_prefix)
            return ClusterInfo()

        response = self._cached_api_call("/cluster?fields=*")
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

    def _collect_cluster_info_via_cli(self) -> ClusterInfo:
        """Collect cluster info using CLI.

        Returns:
            ClusterInfo from cluster identity show.
        """
        if not self.cli_client:
            logger.debug("%s No CLI client available for cluster info collection", self._log_prefix)
            return ClusterInfo()

        logger.debug("%s CLI command: cluster identity show", self._log_prefix)
        output, _ = self.cli_client.run_a_show_command_and_parse_seperator("cluster identity show")
        logger.debug("%s CLI response: %d entries", self._log_prefix, len(output))
        if output:
            data = output[0]
            self._log_missing_fields(
                data,
                ["cluster", "cluster-uuid"],
                "Cluster(CLI)",
                data.get("cluster", "unknown"),
            )
            return ClusterInfo(
                cluster_name=data.get("cluster", ""),
                cluster_uuid=data.get("cluster-uuid", ""),
            )
        return ClusterInfo()

    # -------------------------------------------------------------------------
    # Node Collection
    # -------------------------------------------------------------------------

    def collect_nodes(self) -> list[NodeInfo]:
        """Collect node information.

        Returns:
            List of NodeInfo objects.
        """
        if self.api_client:
            try:
                return self._collect_nodes_via_api()
            except Exception as e:
                logger.warning(f"{self._log_prefix} Failed to collect nodes via API: {e}")

        if self.cli_client:
            try:
                return self._collect_nodes_via_cli()
            except Exception as e:
                logger.warning(f"{self._log_prefix} Failed to collect nodes via CLI: {e}")

        return []

    def _collect_nodes_via_api(self) -> list[NodeInfo]:
        """Collect nodes using REST API.

        Returns:
            List of NodeInfo from /cluster/nodes endpoint.
        """
        if not self.api_client:
            logger.debug("%s No API client available for nodes collection", self._log_prefix)
            return []

        # Use cached API call to avoid duplicate requests (also used by HA collection)
        response = self._cached_api_call("/cluster/nodes?fields=*")
        if not response:
            return []

        logger.debug(
            "%s API response: %d nodes", self._log_prefix, len(response.get("records", []))
        )
        nodes = []
        for record in response.get("records", []):
            self._log_missing_fields(
                record,
                ["uuid", "name", "serial_number", "system_id", "model", "membership", "location"],
                "Node",
                record.get("name", record.get("uuid", "unknown")),
            )
            # membership may be a dict or other type depending on API version
            membership = record.get("membership")
            is_epsilon = membership.get("epsilon", False) if isinstance(membership, dict) else False
            nodes.append(
                NodeInfo(
                    uuid=record.get("uuid", ""),
                    name=record.get("name", ""),
                    serial_number=record.get("serial_number", ""),
                    system_id=str(record.get("system_id", "")),
                    model=str(record.get("model", "")),
                    is_epsilon=is_epsilon,
                    location=record.get("location", ""),
                )
            )
        return nodes

    def _collect_nodes_via_cli(self) -> list[NodeInfo]:
        """Collect nodes using CLI.

        Returns:
            List of NodeInfo from system node show.
        """
        if not self.cli_client:
            logger.debug("%s No CLI client available for nodes collection", self._log_prefix)
            return []

        logger.debug("%s CLI command: system node show", self._log_prefix)
        output, _ = self.cli_client.run_a_show_command_and_parse_seperator("system node show")
        logger.debug("%s CLI response: %d nodes", self._log_prefix, len(output))
        nodes = []
        for data in output:
            self._log_missing_fields(
                data,
                ["node", "serial-number", "system-id", "model"],
                "Node(CLI)",
                data.get("node", "unknown"),
            )
            nodes.append(
                NodeInfo(
                    name=data.get("node", ""),
                    serial_number=data.get("serial-number", ""),
                    system_id=data.get("system-id", ""),
                    model=data.get("model", ""),
                )
            )
        return nodes

    # -------------------------------------------------------------------------
    # Network Collection
    # -------------------------------------------------------------------------

    def collect_network(self) -> NetworkInfo:
        """Collect network configuration.

        Returns:
            NetworkInfo object.
        """
        if self.api_client:
            try:
                return self._collect_network_via_api()
            except Exception as e:
                logger.warning(f"{self._log_prefix} Failed to collect network via API: {e}")

        if self.cli_client:
            try:
                return self._collect_network_via_cli()
            except Exception as e:
                logger.warning(f"{self._log_prefix} Failed to collect network via CLI: {e}")

        return NetworkInfo()

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

    def _collect_network_via_cli(self) -> NetworkInfo:
        """Collect network info using CLI.

        Returns:
            NetworkInfo from network interface show.
        """
        if not self.cli_client:
            logger.debug("%s No CLI client available for network collection", self._log_prefix)
            return NetworkInfo()

        logger.debug("%s CLI command: network interface show", self._log_prefix)
        output, _ = self.cli_client.run_a_show_command_and_parse_seperator("network interface show")
        logger.debug("%s CLI response: %d interfaces", self._log_prefix, len(output))
        intercluster_lifs = []
        data_lifs = []
        management_lifs = []

        for data in output:
            self._log_missing_fields(
                data,
                ["lif", "address", "netmask", "home-node", "home-port", "role", "vserver"],
                "LIF(CLI)",
                data.get("lif", "unknown"),
            )
            lif = NetworkLIF(
                name=data.get("lif", ""),
                ip_address=data.get("address", ""),
                netmask=data.get("netmask", ""),
                home_node=data.get("home-node", ""),
                home_port=data.get("home-port", ""),
                role=data.get("role", ""),
                svm=data.get("vserver", ""),
            )
            role = data.get("role", "").lower()
            if "intercluster" in role:
                intercluster_lifs.append(lif)
            elif role in ("data", ""):
                data_lifs.append(lif)
            elif "mgmt" in role or "management" in role:
                management_lifs.append(lif)
            else:
                data_lifs.append(lif)

        return NetworkInfo(
            intercluster_lifs=intercluster_lifs,
            data_lifs=data_lifs,
            management_lifs=management_lifs,
        )

    # -------------------------------------------------------------------------
    # Storage Collection
    # -------------------------------------------------------------------------

    def collect_storage(self) -> StorageInfo:
        """Collect storage topology information.

        Returns:
            StorageInfo object.
        """
        if self.api_client:
            try:
                return self._collect_storage_via_api()
            except Exception as e:
                logger.warning(f"{self._log_prefix} Failed to collect storage via API: {e}")

        if self.cli_client:
            try:
                return self._collect_storage_via_cli()
            except Exception as e:
                logger.warning(f"{self._log_prefix} Failed to collect storage via CLI: {e}")

        return StorageInfo()

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
            "/storage/aggregates?fields=*",
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
        aggr_response = responses.get(endpoints[0]) or {}
        logger.debug(
            "%s API response: %d aggregates",
            self._log_prefix,
            len(aggr_response.get("records", [])),
        )
        aggregates = []
        for record in aggr_response.get("records", []):
            self._log_missing_fields(
                record,
                ["uuid", "name", "node", "state", "block_storage", "space"],
                "Aggregate",
                record.get("name", record.get("uuid", "unknown")),
            )
            block_storage = record.get("block_storage", {})
            primary = block_storage.get("primary", {})
            aggr = AggregateInfo(
                uuid=record.get("uuid", ""),
                name=record.get("name", ""),
                node=record.get("node", {}).get("name", ""),
                state=record.get("state", ""),
                type=primary.get("disk_type", ""),
                total_size=record.get("space", {}).get("block_storage", {}).get("size", 0),
                disk_count=primary.get("disk_count", 0),
                disk_type=primary.get("disk_type", ""),
                raid_type=primary.get("raid_type", ""),
            )
            aggregates.append(aggr)

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

    def _collect_storage_via_cli(self) -> StorageInfo:
        """Collect storage info using CLI.

        Returns:
            StorageInfo from aggr show, vserver show, and object-store config show.
        """
        if not self.cli_client:
            logger.debug("%s No CLI client available for storage collection", self._log_prefix)
            return StorageInfo()

        # Collect aggregates
        logger.debug("%s CLI command: aggr show", self._log_prefix)
        aggr_output, _ = self.cli_client.run_a_show_command_and_parse_seperator("aggr show")
        logger.debug("%s CLI response: %d aggregates", self._log_prefix, len(aggr_output))
        aggregates = []
        for data in aggr_output:
            self._log_missing_fields(
                data,
                ["aggregate", "node", "state", "type"],
                "Aggregate(CLI)",
                data.get("aggregate", "unknown"),
            )
            aggr = AggregateInfo(
                name=data.get("aggregate", ""),
                node=data.get("node", ""),
                state=data.get("state", ""),
                type=data.get("type", ""),
            )
            aggregates.append(aggr)

        # Collect SVMs
        logger.debug("%s CLI command: vserver show", self._log_prefix)
        svm_output, _ = self.cli_client.run_a_show_command_and_parse_seperator("vserver show")
        logger.debug("%s CLI response: %d SVMs", self._log_prefix, len(svm_output))
        svms = []
        for data in svm_output:
            self._log_missing_fields(
                data,
                ["vserver", "admin-state", "type", "root-volume"],
                "SVM(CLI)",
                data.get("vserver", "unknown"),
            )
            svm = SVMInfo(
                name=data.get("vserver", ""),
                state=data.get("admin-state", ""),
                subtype=data.get("type", ""),
                root_volume=data.get("root-volume", ""),
            )
            svms.append(svm)

        # Collect cloud targets
        cloud_targets = self._collect_cloud_targets_via_cli()

        return StorageInfo(aggregates=aggregates, svms=svms, cloud_targets=cloud_targets)

    def _collect_cloud_targets_via_cli(self) -> list[CloudTargetInfo]:
        """Collect cloud object store targets using CLI.

        Returns:
            List of CloudTargetInfo from storage aggregate object-store config show.
        """
        if not self.cli_client:
            logger.debug(
                "%s No CLI client available for cloud targets collection", self._log_prefix
            )
            return []

        try:
            logger.debug(
                "%s CLI command: storage aggregate object-store config show", self._log_prefix
            )
            output, _ = self.cli_client.run_a_show_command_and_parse_seperator(
                "storage aggregate object-store config show"
            )
            logger.debug("%s CLI response: %d cloud targets", self._log_prefix, len(output))
        except Exception as e:
            # Command may not be available on systems without FabricPool
            logger.debug("%s Cloud targets CLI command not available: %s", self._log_prefix, e)
            return []

        cloud_targets = []
        for data in output:
            self._log_missing_fields(
                data,
                [
                    "object-store-name",
                    "provider-type",
                    "server",
                    "container",
                    "owner",
                    "ssl-enabled",
                    "auth-type",
                    "ipspace",
                ],
                "CloudTarget(CLI)",
                data.get("object-store-name", "unknown"),
            )
            target = CloudTargetInfo(
                name=data.get("object-store-name", ""),
                provider_type=data.get("provider-type", ""),
                server=data.get("server", ""),
                container=data.get("container", "") or data.get("bucket", ""),
                owner=data.get("owner", ""),
                ssl_enabled=data.get("ssl-enabled", "").lower() == "true",
                authentication_type=data.get("auth-type", ""),
                ipspace=data.get("ipspace", ""),
            )
            cloud_targets.append(target)
        return cloud_targets

    # -------------------------------------------------------------------------
    # License Collection
    # -------------------------------------------------------------------------

    def collect_licenses(self) -> LicenseInfo:
        """Collect licensing information.

        Returns:
            LicenseInfo object.
        """
        if self.api_client:
            try:
                return self._collect_licenses_via_api()
            except Exception as e:
                logger.warning(f"{self._log_prefix} Failed to collect licenses via API: {e}")

        if self.cli_client:
            try:
                return self._collect_licenses_via_cli()
            except Exception as e:
                logger.warning(f"{self._log_prefix} Failed to collect licenses via CLI: {e}")

        return LicenseInfo()

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

    def _collect_licenses_via_cli(self) -> LicenseInfo:
        """Collect licenses using CLI.

        Returns:
            LicenseInfo from license show.
        """
        if not self.cli_client:
            logger.debug("%s No CLI client available for license collection", self._log_prefix)
            return LicenseInfo()

        logger.debug("%s CLI command: license show", self._log_prefix)
        output, _ = self.cli_client.run_a_show_command_and_parse_seperator("license show")
        logger.debug("%s CLI response: %d licenses", self._log_prefix, len(output))
        feature_licenses = []

        for data in output:
            self._log_missing_fields(
                data,
                ["package", "state", "scope"],
                "License(CLI)",
                data.get("package", "unknown"),
            )
            feature = LicenseFeature(
                name=data.get("package", ""),
                state=data.get("state", ""),
                scope=data.get("scope", ""),
            )
            feature_licenses.append(feature)

        return LicenseInfo(feature_licenses=feature_licenses)

    # -------------------------------------------------------------------------
    # HA Info Collection
    # -------------------------------------------------------------------------

    def collect_ha_info(self) -> HAInfo:
        """Collect HA configuration information.

        Returns:
            HAInfo object.
        """
        if self.api_client:
            try:
                return self._collect_ha_info_via_api()
            except Exception as e:
                logger.warning(f"{self._log_prefix} Failed to collect HA info via API: {e}")

        if self.cli_client:
            try:
                return self._collect_ha_info_via_cli()
            except Exception as e:
                logger.warning(f"{self._log_prefix} Failed to collect HA info via CLI: {e}")

        return HAInfo()

    def _collect_ha_info_via_api(self) -> HAInfo:
        """Collect HA info using REST API.

        Returns:
            HAInfo from /cluster endpoint.
        """
        if not self.api_client:
            logger.debug("%s No API client available for HA info collection", self._log_prefix)
            return HAInfo()

        # Use cached API call (same endpoint as nodes collection)
        nodes_response = self._cached_api_call("/cluster/nodes?fields=*")
        if not nodes_response:
            return HAInfo()

        logger.debug(
            "%s API response: %d nodes (from cache)",
            self._log_prefix,
            len(nodes_response.get("records", [])),
        )

        # Check HA fields on first node
        records = nodes_response.get("records", [])
        if records:
            self._log_missing_fields(
                records[0],
                ["ha"],
                "Node(HA)",
                records[0].get("name", records[0].get("uuid", "unknown")),
            )
            ha_obj = records[0].get("ha", {})
            if isinstance(ha_obj, dict):
                self._log_missing_fields(
                    ha_obj,
                    ["enabled", "partners", "takeover"],
                    "Node(HA).ha",
                    records[0].get("name", records[0].get("uuid", "unknown")),
                )

        # Check if HA is configured
        ha_configured = len(records) > 1

        # Try to get mediator info for cloud HA (use cached call)
        mediator_address = ""
        try:
            mediator_response = self._cached_api_call("/cluster/mediators?fields=*")
            if mediator_response:
                mediators = mediator_response.get("records", [])
                logger.debug("%s API response: %d mediators", self._log_prefix, len(mediators))
                if mediators:
                    mediator_address = mediators[0].get("ip_address", "")
        except Exception as e:
            logger.debug("%s Mediator endpoint not available: %s", self._log_prefix, e)

        return HAInfo(
            is_ha=ha_configured,
            mediator_address=mediator_address,
        )

    def _collect_ha_info_via_cli(self) -> HAInfo:
        """Collect HA info using CLI.

        Returns:
            HAInfo from storage failover show.
        """
        if not self.cli_client:
            logger.debug("%s No CLI client available for HA info collection", self._log_prefix)
            return HAInfo()

        logger.debug("%s CLI command: storage failover show", self._log_prefix)
        output, _ = self.cli_client.run_a_show_command_and_parse_seperator("storage failover show")
        logger.debug("%s CLI response: %d entries", self._log_prefix, len(output))
        if not output:
            return HAInfo(is_ha=False)

        # Parse first node's HA info
        first_node = output[0]
        self._log_missing_fields(
            first_node,
            ["partner-name", "node-state"],
            "HA(CLI)",
            first_node.get("node", "unknown"),
        )
        return HAInfo(
            is_ha=True,
            partner_node=first_node.get("partner-name", ""),
            ha_state=first_node.get("node-state", ""),
        )

    # -------------------------------------------------------------------------
    # Relationships Collection
    # -------------------------------------------------------------------------

    def collect_relationships(self) -> RelationshipsInfo:
        """Collect cluster relationships information.

        Returns:
            RelationshipsInfo object.
        """
        if self.api_client:
            try:
                return self._collect_relationships_via_api()
            except Exception as e:
                logger.warning(f"{self._log_prefix} Failed to collect relationships via API: {e}")

        if self.cli_client:
            try:
                return self._collect_relationships_via_cli()
            except Exception as e:
                logger.warning(f"{self._log_prefix} Failed to collect relationships via CLI: {e}")

        return RelationshipsInfo()

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
            "/snapmirror/relationships?fields=uuid,source,destination,policy.type,state",
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
        sm_response = responses.get(endpoints[0]) or {}
        logger.debug(
            "%s API response: %d SnapMirror relationships",
            self._log_prefix,
            len(sm_response.get("records", [])),
        )
        snapmirror_destinations = []
        for record in sm_response.get("records", []):
            self._log_missing_fields(
                record,
                ["uuid", "source", "destination", "policy", "state"],
                "SnapMirror",
                record.get("uuid", "unknown"),
            )
            sm = SnapMirrorRelationship(
                uuid=record.get("uuid", ""),
                source_path=self._format_path(record.get("source", {})),
                destination_path=self._format_path(record.get("destination", {})),
                relationship_type=record.get("policy", {}).get("type", ""),
                state=record.get("state", ""),
            )
            snapmirror_destinations.append(sm)

        # Process cluster peers
        peer_response = responses.get(endpoints[1]) or {}
        logger.debug(
            "%s API response: %d cluster peers",
            self._log_prefix,
            len(peer_response.get("records", [])),
        )
        cluster_peers = []
        for record in peer_response.get("records", []):
            self._log_missing_fields(
                record,
                ["name", "uuid", "remote", "authentication"],
                "ClusterPeer",
                record.get("name", record.get("uuid", "unknown")),
            )
            # Handle fields that may be dicts or strings depending on API version
            remote = record.get("remote")
            remote_name = remote.get("name", "") if isinstance(remote, dict) else str(remote or "")
            auth = record.get("authentication")
            auth_state = auth.get("state", "") if isinstance(auth, dict) else str(auth or "")
            # Get peer addresses from remote.ip_addresses (not peer_applications)
            peer_addresses = remote.get("ip_addresses", []) if isinstance(remote, dict) else []
            peer = ClusterPeer(
                name=record.get("name", ""),
                uuid=record.get("uuid", ""),
                remote_cluster_name=remote_name,
                peer_addresses=[addr for addr in peer_addresses if addr],
                authentication_state=auth_state,
            )
            cluster_peers.append(peer)

        # Process SVM peers
        svm_peers = self._parse_svm_peers_response(responses.get(endpoints[2]))

        return RelationshipsInfo(
            snapmirror_destinations=snapmirror_destinations,
            cluster_peers=cluster_peers,
            svm_peers=svm_peers,
        )

    def _collect_relationships_via_cli(self) -> RelationshipsInfo:
        """Collect relationships using CLI.

        Returns:
            RelationshipsInfo from snapmirror show and cluster peer show.
        """
        if not self.cli_client:
            logger.debug(
                "%s No CLI client available for relationships collection", self._log_prefix
            )
            return RelationshipsInfo()

        # Collect SnapMirror relationships
        logger.debug("%s CLI command: snapmirror show", self._log_prefix)
        sm_output, _ = self.cli_client.run_a_show_command_and_parse_seperator("snapmirror show")
        logger.debug(
            "%s CLI response: %d SnapMirror relationships", self._log_prefix, len(sm_output)
        )
        snapmirror_destinations = []
        for data in sm_output:
            self._log_missing_fields(
                data,
                ["source-path", "destination-path", "type", "state"],
                "SnapMirror(CLI)",
                data.get("source-path", "unknown"),
            )
            sm = SnapMirrorRelationship(
                source_path=data.get("source-path", ""),
                destination_path=data.get("destination-path", ""),
                relationship_type=data.get("type", ""),
                state=data.get("state", ""),
            )
            snapmirror_destinations.append(sm)

        # Collect cluster peers
        logger.debug("%s CLI command: cluster peer show", self._log_prefix)
        peer_output, _ = self.cli_client.run_a_show_command_and_parse_seperator("cluster peer show")
        logger.debug("%s CLI response: %d cluster peers", self._log_prefix, len(peer_output))
        cluster_peers = []
        for data in peer_output:
            self._log_missing_fields(
                data,
                ["peer-cluster", "remote-cluster-name", "auth-status-admin"],
                "ClusterPeer(CLI)",
                data.get("peer-cluster", "unknown"),
            )
            peer = ClusterPeer(
                name=data.get("peer-cluster", ""),
                remote_cluster_name=data.get("remote-cluster-name", ""),
                authentication_state=data.get("auth-status-admin", ""),
            )
            cluster_peers.append(peer)

        return RelationshipsInfo(
            snapmirror_destinations=snapmirror_destinations,
            cluster_peers=cluster_peers,
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
        """Collect protocol configuration information.

        Returns:
            ProtocolsInfo object.
        """
        if self.api_client:
            try:
                return self._collect_protocols_via_api()
            except Exception as e:
                logger.warning(f"{self._log_prefix} Failed to collect protocols via API: {e}")

        return ProtocolsInfo()

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

    @staticmethod
    def _format_path(path_info: dict[str, Any] | str | None) -> str:
        """Format SVM:volume path from API response.

        Args:
            path_info: Path info dict with svm and path keys, or a string path,
                or None.

        Returns:
            Formatted path string.
        """
        # Handle string paths (API may return path directly as string)
        if isinstance(path_info, str):
            return path_info
        if not path_info:
            return ""
        svm_dict = path_info.get("svm")
        svm: str = svm_dict.get("name", "") if isinstance(svm_dict, dict) else ""
        path_val = path_info.get("path")
        path: str = str(path_val) if path_val else ""
        if svm and path:
            return f"{svm}:{path}"
        return path or svm
