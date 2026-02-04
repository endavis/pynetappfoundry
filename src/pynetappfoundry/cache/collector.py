"""Metadata collector for ONTAP clusters.

Collects cluster metadata using REST API (primary) with CLI fallback.
"""

from __future__ import annotations

import logging
import re
import time
from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, datetime
from enum import Enum
from typing import TYPE_CHECKING, Any, ClassVar

from pynetappfoundry.cache.models import (
    AggregateInfo,
    BroadcastDomain,
    CachedClusterMetadata,
    CapacityLicense,
    CloudMetadata,
    ClusterInfo,
    ClusterPeer,
    HAInfo,
    LicenseFeature,
    LicenseInfo,
    NetworkInfo,
    NetworkLIF,
    NodeInfo,
    RelationshipsInfo,
    SnapMirrorRelationship,
    StorageInfo,
    SVMInfo,
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
    }

    def __init__(
        self,
        api_client: ONTAPAPIClient | None = None,
        cli_client: ONTAPCLI | None = None,
        progress_callback: ProgressCallback | None = None,
    ) -> None:
        """Initialize the metadata collector.

        Args:
            api_client: ONTAP REST API client.
            cli_client: ONTAP CLI (SSH) client.
            progress_callback: Optional callback for progress updates.
        """
        self.api_client = api_client
        self.cli_client = cli_client
        self.progress_callback = progress_callback

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

    def collect_all(self, cluster_name: str) -> CachedClusterMetadata:
        """Collect all metadata categories for a cluster.

        Args:
            cluster_name: Name of the cluster being collected.

        Returns:
            Complete CachedClusterMetadata object.
        """
        logger.info("Starting metadata collection for cluster: %s", cluster_name)
        total_start = time.monotonic()

        # Define collection phases with their methods
        phases: list[tuple[CollectionPhase, Callable[[], Any]]] = [
            (CollectionPhase.CLOUD, self.collect_cloud_metadata),
            (CollectionPhase.CLUSTER, self.collect_cluster_info),
            (CollectionPhase.NODES, self.collect_nodes),
            (CollectionPhase.NETWORK, self.collect_network),
            (CollectionPhase.STORAGE, self.collect_storage),
            (CollectionPhase.LICENSES, self.collect_licenses),
            (CollectionPhase.HA, self.collect_ha_info),
            (CollectionPhase.RELATIONSHIPS, self.collect_relationships),
        ]

        results: dict[str, Any] = {}
        for phase, collect_method in phases:
            phase_start = time.monotonic()
            self._report_progress(phase, "starting")
            logger.debug("Collecting %s for %s", phase.value, cluster_name)

            try:
                result = collect_method()
                elapsed = time.monotonic() - phase_start
                # Determine source used (check if result came from API or CLI)
                source = self._determine_source(phase)
                self._report_progress(phase, "completed", elapsed, source=source)
                logger.debug(
                    "Collected %s for %s in %.2fs via %s",
                    phase.value,
                    cluster_name,
                    elapsed,
                    source or "unknown",
                )
                results[phase.value] = result
            except Exception as e:
                elapsed = time.monotonic() - phase_start
                error_msg = str(e)
                self._report_progress(phase, "failed", elapsed, error=error_msg)
                logger.error(
                    "Failed to collect %s for %s: %s",
                    phase.value,
                    cluster_name,
                    error_msg,
                    exc_info=True,
                )
                raise

        total_elapsed = time.monotonic() - total_start
        logger.info("Completed metadata collection for %s in %.2fs", cluster_name, total_elapsed)

        return CachedClusterMetadata(
            cluster_name=cluster_name,
            cached_at=datetime.now(UTC),
            cloud=results["cloud"],
            cluster=results["cluster"],
            nodes=results["nodes"],
            network=results["network"],
            storage=results["storage"],
            licenses=results["licenses"],
            ha=results["ha"],
            relationships=results["relationships"],
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

    # -------------------------------------------------------------------------
    # Cloud Metadata Collection
    # -------------------------------------------------------------------------

    def collect_cloud_metadata(self) -> CloudMetadata:
        """Collect cloud provider metadata.

        Cloud metadata is only available via CLI (virtual-machine instance show).

        Returns:
            CloudMetadata object.
        """
        if self.cli_client:
            try:
                return self._collect_cloud_metadata_via_cli()
            except Exception as e:
                logger.warning(f"Failed to collect cloud metadata via CLI: {e}")
        return CloudMetadata()

    def _collect_cloud_metadata_via_cli(self) -> CloudMetadata:
        """Collect cloud metadata using CLI.

        Returns:
            CloudMetadata from virtual-machine instance show.
        """
        if not self.cli_client:
            logger.debug("No CLI client available for cloud metadata collection")
            return CloudMetadata()

        logger.debug("CLI command: virtual-machine instance show")
        output = self.cli_client.run_command("virtual-machine instance show")
        logger.debug("CLI response: %d lines", len(output))
        return self._parse_vm_instance_output(output)

    def _parse_vm_instance_output(self, output: list[str]) -> CloudMetadata:
        """Parse virtual-machine instance show output.

        Args:
            output: Lines of CLI output.

        Returns:
            CloudMetadata object.
        """
        data: dict[str, str] = {}
        for line in output:
            if ":" not in line:
                continue
            parts = line.split(":", 1)
            if len(parts) == 2:
                key = parts[0].strip()
                value = parts[1].strip()
                # Normalize key names
                key_normalized = self._normalize_cli_key(key)
                data[key_normalized] = value

        return CloudMetadata(
            instance_id=data.get("instance_id", ""),
            account_id=data.get("account_id", ""),
            image_id=data.get("image_id", ""),
            instance_type=data.get("instance_type", ""),
            cpu_platform=data.get("cpu_platform", ""),
            region=data.get("region", ""),
            provider=data.get("provider", ""),
            consumer=data.get("consumer", ""),
            primary_ip=data.get("primary_ip", ""),
            metadata_version=data.get("metadata_version", ""),
            availability_zone=data.get("availability_zone", ""),
            availability_zone_id=data.get("availability_zone_id", ""),
            fault_domain=data.get("fault_domain", ""),
            update_domain=data.get("update_domain", ""),
            resource_group_name=data.get("resource_group_name", ""),
            offer=data.get("offer", ""),
            sku=data.get("sku", ""),
            sku_version=data.get("sku_version", ""),
        )

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
                logger.warning(f"Failed to collect cluster info via API: {e}")

        # Fall back to CLI
        if self.cli_client:
            try:
                return self._collect_cluster_info_via_cli()
            except Exception as e:
                logger.warning(f"Failed to collect cluster info via CLI: {e}")

        return ClusterInfo()

    def _collect_cluster_info_via_api(self) -> ClusterInfo:
        """Collect cluster info using REST API.

        Returns:
            ClusterInfo from /cluster endpoint.
        """
        if not self.api_client:
            logger.debug("No API client available for cluster info collection")
            return ClusterInfo()

        logger.debug("API call: GET /cluster?fields=*")
        response = self.api_client.call_endpoint("/cluster?fields=*", method="GET")
        logger.debug("API response: cluster=%s", response.get("name", "unknown"))
        return ClusterInfo(
            cluster_name=response.get("name", ""),
            cluster_uuid=response.get("uuid", ""),
            ontap_version=response.get("version", {}).get("full", ""),
            model=response.get("version", {}).get("generation", ""),
        )

    def _collect_cluster_info_via_cli(self) -> ClusterInfo:
        """Collect cluster info using CLI.

        Returns:
            ClusterInfo from cluster identity show.
        """
        if not self.cli_client:
            logger.debug("No CLI client available for cluster info collection")
            return ClusterInfo()

        logger.debug("CLI command: cluster identity show")
        output = self.cli_client.run_command_and_parse("cluster identity show")
        logger.debug("CLI response: %d entries", len(output))
        # Output is keyed by cluster name
        if output:
            first_key = next(iter(output))
            data = output[first_key]
            return ClusterInfo(
                cluster_name=data.get("Cluster", ""),
                cluster_uuid=data.get("Cluster UUID", ""),
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
                logger.warning(f"Failed to collect nodes via API: {e}")

        if self.cli_client:
            try:
                return self._collect_nodes_via_cli()
            except Exception as e:
                logger.warning(f"Failed to collect nodes via CLI: {e}")

        return []

    def _collect_nodes_via_api(self) -> list[NodeInfo]:
        """Collect nodes using REST API.

        Returns:
            List of NodeInfo from /cluster/nodes endpoint.
        """
        if not self.api_client:
            logger.debug("No API client available for nodes collection")
            return []

        logger.debug("API call: GET /cluster/nodes?fields=*")
        response = self.api_client.call_endpoint("/cluster/nodes?fields=*", method="GET")
        logger.debug("API response: %d nodes", len(response.get("records", [])))
        nodes = []
        for record in response.get("records", []):
            # membership may be a dict or other type depending on API version
            membership = record.get("membership")
            is_epsilon = membership.get("epsilon", False) if isinstance(membership, dict) else False
            nodes.append(
                NodeInfo(
                    name=record.get("name", ""),
                    serial_number=record.get("serial_number", ""),
                    system_id=str(record.get("system_id", "")),
                    model=str(record.get("model", "")),
                    uptime=record.get("uptime", 0),
                    is_epsilon=is_epsilon,
                )
            )
        return nodes

    def _collect_nodes_via_cli(self) -> list[NodeInfo]:
        """Collect nodes using CLI.

        Returns:
            List of NodeInfo from system node show.
        """
        if not self.cli_client:
            logger.debug("No CLI client available for nodes collection")
            return []

        logger.debug("CLI command: system node show")
        output = self.cli_client.run_command_and_parse("system node show")
        logger.debug("CLI response: %d nodes", len(output))
        nodes = []
        for node_name, data in output.items():
            nodes.append(
                NodeInfo(
                    name=node_name,
                    serial_number=data.get("Serial Number", ""),
                    system_id=data.get("System ID", ""),
                    model=data.get("Model", ""),
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
                logger.warning(f"Failed to collect network via API: {e}")

        if self.cli_client:
            try:
                return self._collect_network_via_cli()
            except Exception as e:
                logger.warning(f"Failed to collect network via CLI: {e}")

        return NetworkInfo()

    def _collect_network_via_api(self) -> NetworkInfo:
        """Collect network info using REST API.

        Returns:
            NetworkInfo from various network endpoints.
        """
        if not self.api_client:
            logger.debug("No API client available for network collection")
            return NetworkInfo()

        # Collect LIFs
        logger.debug("API call: GET /network/ip/interfaces?fields=*")
        lifs_response = self.api_client.call_endpoint(
            "/network/ip/interfaces?fields=*", method="GET"
        )
        logger.debug("API response: %d LIFs", len(lifs_response.get("records", [])))
        intercluster_lifs = []
        data_lifs = []
        management_lifs = []

        for record in lifs_response.get("records", []):
            lif = NetworkLIF(
                name=record.get("name", ""),
                ip_address=record.get("ip", {}).get("address", ""),
                netmask=record.get("ip", {}).get("netmask", ""),
                home_node=record.get("location", {}).get("home_node", {}).get("name", ""),
                home_port=record.get("location", {}).get("home_port", {}).get("name", ""),
                current_node=record.get("location", {}).get("node", {}).get("name", ""),
                current_port=record.get("location", {}).get("port", {}).get("name", ""),
                operational_status=record.get("state", ""),
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

        # Collect broadcast domains
        logger.debug("API call: GET /network/ethernet/broadcast-domains?fields=*")
        bd_response = self.api_client.call_endpoint(
            "/network/ethernet/broadcast-domains?fields=*", method="GET"
        )
        logger.debug("API response: %d broadcast domains", len(bd_response.get("records", [])))
        broadcast_domains = []
        for record in bd_response.get("records", []):
            bd = BroadcastDomain(
                name=record.get("name", ""),
                ipspace=record.get("ipspace", {}).get("name", ""),
                mtu=record.get("mtu", 0),
                ports=[p.get("name", "") for p in record.get("ports", []) if p.get("name")],
            )
            broadcast_domains.append(bd)

        # Collect IPspaces
        logger.debug("API call: GET /network/ipspaces?fields=*")
        ipspace_response = self.api_client.call_endpoint("/network/ipspaces?fields=*", method="GET")
        logger.debug("API response: %d IPspaces", len(ipspace_response.get("records", [])))
        ipspaces = [r.get("name", "") for r in ipspace_response.get("records", [])]

        return NetworkInfo(
            intercluster_lifs=intercluster_lifs,
            data_lifs=data_lifs,
            management_lifs=management_lifs,
            broadcast_domains=broadcast_domains,
            ipspaces=ipspaces,
        )

    def _collect_network_via_cli(self) -> NetworkInfo:
        """Collect network info using CLI.

        Returns:
            NetworkInfo from network interface show.
        """
        if not self.cli_client:
            logger.debug("No CLI client available for network collection")
            return NetworkInfo()

        logger.debug("CLI command: network interface show")
        output = self.cli_client.run_command_and_parse("network interface show")
        logger.debug("CLI response: %d interfaces", len(output))
        intercluster_lifs = []
        data_lifs = []
        management_lifs = []

        for lif_name, data in output.items():
            lif = NetworkLIF(
                name=lif_name,
                ip_address=data.get("Network Address", ""),
                netmask=data.get("Netmask", ""),
                home_node=data.get("Home Node", ""),
                home_port=data.get("Home Port", ""),
                current_node=data.get("Current Node", ""),
                current_port=data.get("Current Port", ""),
                operational_status=data.get("Operational Status", ""),
                role=data.get("Role", ""),
                svm=data.get("Vserver", ""),
            )
            role = data.get("Role", "").lower()
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
                logger.warning(f"Failed to collect storage via API: {e}")

        if self.cli_client:
            try:
                return self._collect_storage_via_cli()
            except Exception as e:
                logger.warning(f"Failed to collect storage via CLI: {e}")

        return StorageInfo()

    def _collect_storage_via_api(self) -> StorageInfo:
        """Collect storage info using REST API.

        Returns:
            StorageInfo from aggregate and SVM endpoints.
        """
        if not self.api_client:
            logger.debug("No API client available for storage collection")
            return StorageInfo()

        # Collect aggregates
        logger.debug("API call: GET /storage/aggregates?fields=*")
        aggr_response = self.api_client.call_endpoint("/storage/aggregates?fields=*", method="GET")
        logger.debug("API response: %d aggregates", len(aggr_response.get("records", [])))
        aggregates = []
        for record in aggr_response.get("records", []):
            aggr = AggregateInfo(
                name=record.get("name", ""),
                node=record.get("node", {}).get("name", ""),
                state=record.get("state", ""),
                type=record.get("block_storage", {}).get("primary", {}).get("disk_type", ""),
                total_size=record.get("space", {}).get("block_storage", {}).get("size", 0),
                used_size=record.get("space", {}).get("block_storage", {}).get("used", 0),
            )
            aggregates.append(aggr)

        # Collect SVMs
        logger.debug("API call: GET /svm/svms?fields=*")
        svm_response = self.api_client.call_endpoint("/svm/svms?fields=*", method="GET")
        logger.debug("API response: %d SVMs", len(svm_response.get("records", [])))
        svms = []
        for record in svm_response.get("records", []):
            svm = SVMInfo(
                name=record.get("name", ""),
                state=record.get("state", ""),
                subtype=record.get("subtype", ""),
            )
            svms.append(svm)

        return StorageInfo(aggregates=aggregates, svms=svms)

    def _collect_storage_via_cli(self) -> StorageInfo:
        """Collect storage info using CLI.

        Returns:
            StorageInfo from aggr show and vserver show.
        """
        if not self.cli_client:
            logger.debug("No CLI client available for storage collection")
            return StorageInfo()

        # Collect aggregates
        logger.debug("CLI command: aggr show")
        aggr_output = self.cli_client.run_command_and_parse("aggr show")
        logger.debug("CLI response: %d aggregates", len(aggr_output))
        aggregates = []
        for aggr_name, data in aggr_output.items():
            aggr = AggregateInfo(
                name=aggr_name,
                node=data.get("Node", ""),
                state=data.get("State", ""),
                type=data.get("Type", ""),
            )
            aggregates.append(aggr)

        # Collect SVMs
        logger.debug("CLI command: vserver show")
        svm_output = self.cli_client.run_command_and_parse("vserver show")
        logger.debug("CLI response: %d SVMs", len(svm_output))
        svms = []
        for svm_name, data in svm_output.items():
            svm = SVMInfo(
                name=svm_name,
                state=data.get("Admin State", ""),
                subtype=data.get("Vserver Type", ""),
                root_volume=data.get("Root Volume", ""),
            )
            svms.append(svm)

        return StorageInfo(aggregates=aggregates, svms=svms)

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
                logger.warning(f"Failed to collect licenses via API: {e}")

        if self.cli_client:
            try:
                return self._collect_licenses_via_cli()
            except Exception as e:
                logger.warning(f"Failed to collect licenses via CLI: {e}")

        return LicenseInfo()

    def _collect_licenses_via_api(self) -> LicenseInfo:
        """Collect licenses using REST API.

        Returns:
            LicenseInfo from /cluster/licensing/licenses endpoint.
        """
        if not self.api_client:
            logger.debug("No API client available for license collection")
            return LicenseInfo()

        logger.debug("API call: GET /cluster/licensing/licenses?fields=*")
        response = self.api_client.call_endpoint(
            "/cluster/licensing/licenses?fields=*", method="GET"
        )
        logger.debug("API response: %d licenses", len(response.get("records", [])))
        feature_licenses = []
        capacity_licenses = []

        for record in response.get("records", []):
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
            logger.debug("No CLI client available for license collection")
            return LicenseInfo()

        logger.debug("CLI command: license show")
        output = self.cli_client.run_command_and_parse("license show")
        logger.debug("CLI response: %d licenses", len(output))
        feature_licenses = []

        for license_name, data in output.items():
            feature = LicenseFeature(
                name=license_name,
                state=data.get("License State", ""),
                scope=data.get("Scope", ""),
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
                logger.warning(f"Failed to collect HA info via API: {e}")

        if self.cli_client:
            try:
                return self._collect_ha_info_via_cli()
            except Exception as e:
                logger.warning(f"Failed to collect HA info via CLI: {e}")

        return HAInfo()

    def _collect_ha_info_via_api(self) -> HAInfo:
        """Collect HA info using REST API.

        Returns:
            HAInfo from /cluster endpoint.
        """
        if not self.api_client:
            logger.debug("No API client available for HA info collection")
            return HAInfo()

        logger.debug("API call: GET /cluster/nodes?fields=*")
        nodes_response = self.api_client.call_endpoint("/cluster/nodes?fields=*", method="GET")
        logger.debug("API response: %d nodes", len(nodes_response.get("records", [])))

        # Check if HA is configured
        ha_configured = len(nodes_response.get("records", [])) > 1

        # Try to get mediator info for cloud HA
        mediator_address = ""
        mediator_status = ""
        # Mediator endpoint may not exist on all clusters
        logger.debug("API call: GET /cluster/mediators?fields=*")
        try:
            mediator_response = self.api_client.call_endpoint(
                "/cluster/mediators?fields=*", method="GET"
            )
            mediators = mediator_response.get("records", [])
            logger.debug("API response: %d mediators", len(mediators))
            if mediators:
                mediator_address = mediators[0].get("ip_address", "")
                mediator_status = mediators[0].get("reachable", "")
        except Exception as e:
            logger.debug("Mediator endpoint not available: %s", e)

        return HAInfo(
            is_ha=ha_configured,
            mediator_address=mediator_address,
            mediator_status=str(mediator_status) if mediator_status else "",
        )

    def _collect_ha_info_via_cli(self) -> HAInfo:
        """Collect HA info using CLI.

        Returns:
            HAInfo from storage failover show.
        """
        if not self.cli_client:
            logger.debug("No CLI client available for HA info collection")
            return HAInfo()

        logger.debug("CLI command: storage failover show")
        output = self.cli_client.run_command_and_parse("storage failover show")
        logger.debug("CLI response: %d entries", len(output))
        if not output:
            return HAInfo(is_ha=False)

        # Parse first node's HA info
        first_node = next(iter(output.values()), {})
        return HAInfo(
            is_ha=True,
            partner_node=first_node.get("Partner Name", ""),
            ha_state=first_node.get("Node State", ""),
            takeover_state=first_node.get("Takeover State", ""),
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
                logger.warning(f"Failed to collect relationships via API: {e}")

        if self.cli_client:
            try:
                return self._collect_relationships_via_cli()
            except Exception as e:
                logger.warning(f"Failed to collect relationships via CLI: {e}")

        return RelationshipsInfo()

    def _collect_relationships_via_api(self) -> RelationshipsInfo:
        """Collect relationships using REST API.

        Returns:
            RelationshipsInfo from snapmirror and cluster peer endpoints.
        """
        if not self.api_client:
            logger.debug("No API client available for relationships collection")
            return RelationshipsInfo()

        # Collect SnapMirror relationships
        logger.debug("API call: GET /snapmirror/relationships?fields=*")
        sm_response = self.api_client.call_endpoint(
            "/snapmirror/relationships?fields=*", method="GET"
        )
        logger.debug(
            "API response: %d SnapMirror relationships",
            len(sm_response.get("records", [])),
        )
        snapmirror_destinations = []
        for record in sm_response.get("records", []):
            sm = SnapMirrorRelationship(
                source_path=self._format_path(record.get("source", {})),
                destination_path=self._format_path(record.get("destination", {})),
                relationship_type=record.get("policy", {}).get("type", ""),
                state=record.get("state", ""),
                healthy=record.get("healthy", True),
                lag_time=record.get("lag_time", ""),
            )
            snapmirror_destinations.append(sm)

        # Collect cluster peers
        logger.debug("API call: GET /cluster/peers?fields=*")
        peer_response = self.api_client.call_endpoint("/cluster/peers?fields=*", method="GET")
        logger.debug("API response: %d cluster peers", len(peer_response.get("records", [])))
        cluster_peers = []
        for record in peer_response.get("records", []):
            peer = ClusterPeer(
                name=record.get("name", ""),
                uuid=record.get("uuid", ""),
                remote_cluster_name=record.get("remote", {}).get("name", ""),
                peer_addresses=[
                    addr.get("address", "")
                    for addr in record.get("peer_applications", [])
                    if addr.get("address")
                ],
                authentication_state=record.get("authentication", {}).get("state", ""),
                availability=record.get("status", {}).get("state", ""),
            )
            cluster_peers.append(peer)

        return RelationshipsInfo(
            snapmirror_destinations=snapmirror_destinations,
            cluster_peers=cluster_peers,
        )

    def _collect_relationships_via_cli(self) -> RelationshipsInfo:
        """Collect relationships using CLI.

        Returns:
            RelationshipsInfo from snapmirror show and cluster peer show.
        """
        if not self.cli_client:
            logger.debug("No CLI client available for relationships collection")
            return RelationshipsInfo()

        # Collect SnapMirror relationships
        logger.debug("CLI command: snapmirror show")
        sm_output = self.cli_client.run_command_and_parse("snapmirror show")
        logger.debug("CLI response: %d SnapMirror relationships", len(sm_output))
        snapmirror_destinations = []
        for dest_path, data in sm_output.items():
            sm = SnapMirrorRelationship(
                source_path=data.get("Source Path", ""),
                destination_path=dest_path,
                relationship_type=data.get("Relationship Type", ""),
                state=data.get("Mirror State", ""),
                healthy=data.get("Relationship Status", "").lower() == "idle",
                lag_time=data.get("Lag Time", ""),
            )
            snapmirror_destinations.append(sm)

        # Collect cluster peers
        logger.debug("CLI command: cluster peer show")
        peer_output = self.cli_client.run_command_and_parse("cluster peer show")
        logger.debug("CLI response: %d cluster peers", len(peer_output))
        cluster_peers = []
        for peer_name, data in peer_output.items():
            peer = ClusterPeer(
                name=peer_name,
                remote_cluster_name=data.get("Remote Cluster Name", ""),
                availability=data.get("Availability", ""),
                authentication_state=data.get("Authentication Status", ""),
            )
            cluster_peers.append(peer)

        return RelationshipsInfo(
            snapmirror_destinations=snapmirror_destinations,
            cluster_peers=cluster_peers,
        )

    @staticmethod
    def _format_path(path_info: dict[str, Any]) -> str:
        """Format SVM:volume path from API response.

        Args:
            path_info: Path info dict with svm and path keys.

        Returns:
            Formatted path string.
        """
        svm_dict = path_info.get("svm")
        svm: str = svm_dict.get("name", "") if isinstance(svm_dict, dict) else ""
        path_val = path_info.get("path")
        path: str = str(path_val) if path_val else ""
        if svm and path:
            return f"{svm}:{path}"
        return path or svm
