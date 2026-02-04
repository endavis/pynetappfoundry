"""Pydantic models for cached cluster metadata."""

from __future__ import annotations

from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


def _utcnow() -> datetime:
    """Get current UTC time as timezone-aware datetime."""
    return datetime.now(UTC)


class CloudMetadata(BaseModel):
    """Cloud provider metadata from virtual-machine instance show.

    Contains instance-level information from the cloud provider.
    Each node in a cluster has its own cloud metadata.
    """

    model_config = ConfigDict(extra="allow")

    node: str = ""  # Node name this metadata belongs to
    instance_id: str = ""
    account_id: str = ""
    image_id: str = ""
    instance_type: str = ""
    cpu_platform: str = ""
    region: str = ""
    provider: str = ""  # AWS, Azure, GCP
    consumer: str = ""
    primary_ip: str = ""
    metadata_version: str = ""
    # AWS-specific
    availability_zone: str = ""
    availability_zone_id: str = ""
    # Azure-specific
    fault_domain: str = ""
    update_domain: str = ""
    resource_group_name: str = ""
    offer: str = ""
    sku: str = ""
    sku_version: str = ""


class ClusterInfo(BaseModel):
    """Core cluster identity information.

    Contains cluster name, UUID, and version from ONTAP.
    """

    model_config = ConfigDict(extra="allow")

    cluster_name: str = ""
    cluster_uuid: str = ""
    ontap_version: str = ""
    model: str = ""

    @field_validator("model", mode="before")
    @classmethod
    def coerce_model_to_str(cls, v: object) -> str:
        """Coerce model field to string (API sometimes returns int)."""
        return str(v) if v is not None else ""


class NodeInfo(BaseModel):
    """Information about a single cluster node."""

    model_config = ConfigDict(extra="allow")

    name: str = ""
    serial_number: str = ""
    system_id: str = ""
    model: str = ""
    uptime: int = 0  # seconds
    is_epsilon: bool = False


class NetworkLIF(BaseModel):
    """Network logical interface information."""

    model_config = ConfigDict(extra="allow")

    name: str = ""
    ip_address: str = ""
    netmask: str = ""
    home_node: str = ""
    home_port: str = ""
    current_node: str = ""
    current_port: str = ""
    operational_status: str = ""
    role: str = ""  # data, cluster, intercluster, management
    svm: str = ""


class BroadcastDomain(BaseModel):
    """Broadcast domain configuration."""

    model_config = ConfigDict(extra="allow")

    name: str = ""
    ipspace: str = ""
    mtu: int = 0
    ports: list[str] = Field(default_factory=list)


class NetworkInfo(BaseModel):
    """Network configuration information.

    Contains LIFs, broadcast domains, and IPspaces.
    """

    model_config = ConfigDict(extra="allow")

    intercluster_lifs: list[NetworkLIF] = Field(default_factory=list)
    data_lifs: list[NetworkLIF] = Field(default_factory=list)
    management_lifs: list[NetworkLIF] = Field(default_factory=list)
    broadcast_domains: list[BroadcastDomain] = Field(default_factory=list)
    ipspaces: list[str] = Field(default_factory=list)


class AggregateInfo(BaseModel):
    """Storage aggregate information."""

    model_config = ConfigDict(extra="allow")

    name: str = ""
    node: str = ""
    state: str = ""
    type: str = ""  # hdd, ssd, hybrid
    total_size: int = 0  # bytes
    used_size: int = 0  # bytes


class SVMInfo(BaseModel):
    """Storage Virtual Machine information."""

    model_config = ConfigDict(extra="allow")

    name: str = ""
    state: str = ""
    subtype: str = ""  # default, dp_destination, sync_source
    root_volume: str = ""
    root_volume_aggregate: str = ""


class StorageInfo(BaseModel):
    """Storage topology information.

    Contains aggregates and SVMs.
    """

    model_config = ConfigDict(extra="allow")

    aggregates: list[AggregateInfo] = Field(default_factory=list)
    svms: list[SVMInfo] = Field(default_factory=list)


class LicenseFeature(BaseModel):
    """License feature information."""

    model_config = ConfigDict(extra="allow")

    name: str = ""
    state: str = ""  # compliant, noncompliant
    scope: str = ""  # cluster, node


class CapacityLicense(BaseModel):
    """Capacity-based license information."""

    model_config = ConfigDict(extra="allow")

    name: str = ""
    licensed_capacity: int = 0  # bytes
    used_capacity: int = 0  # bytes


class LicenseInfo(BaseModel):
    """Licensing information.

    Contains feature and capacity licenses.
    """

    model_config = ConfigDict(extra="allow")

    feature_licenses: list[LicenseFeature] = Field(default_factory=list)
    capacity_licenses: list[CapacityLicense] = Field(default_factory=list)


class HAInfo(BaseModel):
    """High Availability configuration information.

    For CVO HA configurations.
    """

    model_config = ConfigDict(extra="allow")

    is_ha: bool = False
    partner_node: str = ""
    ha_state: str = ""
    takeover_state: str = ""
    mediator_address: str = ""
    mediator_status: str = ""


class SnapMirrorRelationship(BaseModel):
    """SnapMirror relationship information."""

    model_config = ConfigDict(extra="allow")

    source_path: str = ""
    destination_path: str = ""
    relationship_type: str = ""  # extended_data_protection, data_protection
    state: str = ""  # snapmirrored, uninitialized, broken-off
    healthy: bool = True
    lag_time: str = ""


class ClusterPeer(BaseModel):
    """Cluster peering information."""

    model_config = ConfigDict(extra="allow")

    name: str = ""
    uuid: str = ""
    remote_cluster_name: str = ""
    peer_addresses: list[str] = Field(default_factory=list)
    authentication_state: str = ""
    availability: str = ""


class RelationshipsInfo(BaseModel):
    """Cluster relationships information.

    Contains SnapMirror and peering info.
    """

    model_config = ConfigDict(extra="allow")

    snapmirror_destinations: list[SnapMirrorRelationship] = Field(default_factory=list)
    cluster_peers: list[ClusterPeer] = Field(default_factory=list)


class CachedClusterMetadata(BaseModel):
    """Complete cached metadata for a cluster.

    This is the top-level model containing all cached data categories.
    """

    model_config = ConfigDict(extra="allow")

    # Cache metadata
    cluster_name: str
    cached_at: datetime = Field(default_factory=_utcnow)
    cache_version: str = "1.1"  # Bumped for cloud list change

    # Data categories
    cloud: list[CloudMetadata] = Field(default_factory=list)
    cluster: ClusterInfo = Field(default_factory=ClusterInfo)
    nodes: list[NodeInfo] = Field(default_factory=list)
    network: NetworkInfo = Field(default_factory=NetworkInfo)
    storage: StorageInfo = Field(default_factory=StorageInfo)
    licenses: LicenseInfo = Field(default_factory=LicenseInfo)
    ha: HAInfo = Field(default_factory=HAInfo)
    relationships: RelationshipsInfo = Field(default_factory=RelationshipsInfo)

    def is_stale(self, ttl_days: int = 30) -> bool:
        """Check if the cache is stale based on TTL.

        Args:
            ttl_days: Number of days before cache is considered stale.

        Returns:
            True if cache is older than ttl_days.
        """
        age = _utcnow() - self.cached_at
        return age.days > ttl_days

    def to_flat_dict(self) -> dict[str, str | int | bool | None]:
        """Convert to flat dictionary for merging with cluster config.

        For cloud metadata, uses the first node's data if available.

        Returns:
            Flat dictionary with selected commonly-used fields.
        """
        # Use first node's cloud data if available
        first_cloud = self.cloud[0] if self.cloud else CloudMetadata()
        return {
            # Cloud metadata (from first node)
            "instance_id": first_cloud.instance_id,
            "provider": first_cloud.provider,
            "region": first_cloud.region or first_cloud.availability_zone,
            "instance_type": first_cloud.instance_type,
            "availability_zone": first_cloud.availability_zone,
            # Cluster info
            "cluster_uuid": self.cluster.cluster_uuid,
            "ontap_version": self.cluster.ontap_version,
            "model": self.cluster.model,
            # Cache metadata
            "_cached_at": self.cached_at.isoformat(),
            "_cache_version": self.cache_version,
        }
