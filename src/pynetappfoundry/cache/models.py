"""Pydantic models for cached cluster metadata."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import ClassVar

from pydantic import BaseModel, ConfigDict, Field, field_validator

# Schema version for CachedClusterMetadata model.
# Increment MINOR for backward-compatible changes (new optional fields).
# Increment MAJOR for breaking changes (removed/renamed fields, type changes).
# Format: "MAJOR.MINOR"
METADATA_SCHEMA_VERSION = "1.0"

# Minimum schema version that can be loaded without migration.
# Snapshots older than this may fail to deserialize or have missing data.
METADATA_SCHEMA_MIN_COMPATIBLE = "1.0"


def parse_schema_version(version: str) -> tuple[int, int]:
    """Parse a schema version string into (major, minor) tuple.

    Args:
        version: Version string in "MAJOR.MINOR" format.

    Returns:
        Tuple of (major, minor) integers.

    Raises:
        ValueError: If version string is invalid.
    """
    try:
        parts = version.split(".")
        return (int(parts[0]), int(parts[1]) if len(parts) > 1 else 0)
    except (ValueError, IndexError) as e:
        raise ValueError(f"Invalid schema version: {version!r}") from e


def is_schema_compatible(snapshot_version: str | None) -> bool:
    """Check if a snapshot schema version is compatible with current code.

    Args:
        snapshot_version: The cache_version from a stored snapshot, or None.

    Returns:
        True if the snapshot can be safely loaded, False otherwise.
    """
    if snapshot_version is None:
        # Very old snapshots without version - assume incompatible
        return False

    try:
        snap_major, snap_minor = parse_schema_version(snapshot_version)
        min_major, min_minor = parse_schema_version(METADATA_SCHEMA_MIN_COMPATIBLE)

        # Compatible if snapshot version >= minimum compatible version
        return (snap_major, snap_minor) >= (min_major, min_minor)
    except ValueError:
        return False


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
    # Resource links (computed from other fields)
    instance_link: str = ""  # URL to cloud console for this instance
    instance_sso_link: str = ""  # URL to cloud console via AWS SSO (AWS only)
    resource_group_link: str = ""  # URL to cloud console for resource group (Azure)


class ClusterInfo(BaseModel):
    """Core cluster identity information.

    Contains cluster name, UUID, and version from ONTAP.
    """

    model_config = ConfigDict(extra="allow")

    cluster_name: str = ""
    cluster_uuid: str = ""
    ontap_version: str = ""
    model: str = ""
    contact: str = ""
    location: str = ""

    @field_validator("model", mode="before")
    @classmethod
    def coerce_model_to_str(cls, v: object) -> str:
        """Coerce model field to string (API sometimes returns int)."""
        return str(v) if v is not None else ""


class NodeInfo(BaseModel):
    """Information about a single cluster node."""

    model_config = ConfigDict(extra="allow")

    uuid: str = ""
    name: str = ""
    serial_number: str = ""
    system_id: str = ""
    model: str = ""
    location: str = ""

    @field_validator("system_id", "model", mode="before")
    @classmethod
    def coerce_to_str(cls, v: object) -> str:
        """Coerce system_id and model to string (API sometimes returns int)."""
        return str(v) if v is not None else ""

    membership: str = ""
    version_full: str = ""
    storage_configuration: str = ""
    system_machine_type: str = ""
    controller_board: str = ""
    controller_memory_size: int = 0
    controller_cpu_count: int = 0
    vm_provider_type: str = ""
    ha_enabled: bool = False
    ha_auto_giveback: bool = False
    ha_partner_uuids: list[str] = Field(default_factory=list)
    system_aggregate_uuid: str = ""
    cluster_interface_uuids: list[str] = Field(default_factory=list)
    management_interface_uuids: list[str] = Field(default_factory=list)


class NetworkLIF(BaseModel):
    """Network logical interface information."""

    model_config = ConfigDict(extra="allow")

    name: str = ""
    ip_address: str = ""
    netmask: str = ""
    home_node: str = ""
    home_port: str = ""
    role: str = ""  # data, cluster, intercluster, management
    svm: str = ""


class BroadcastDomain(BaseModel):
    """Broadcast domain configuration."""

    model_config = ConfigDict(extra="allow")

    uuid: str = ""
    name: str = ""
    ipspace: str = ""
    mtu: int = 0
    ports: list[str] = Field(default_factory=list)


class IPSubnetInfo(BaseModel):
    """IP subnet information."""

    model_config = ConfigDict(extra="allow")

    uuid: str = ""
    name: str = ""
    ipspace: str = ""
    broadcast_domain: str = ""
    subnet: str = ""  # CIDR notation, e.g., "10.0.0.0/24"
    gateway: str = ""
    ip_ranges: list[str] = Field(default_factory=list)


class NetworkInfo(BaseModel):
    """Network configuration information.

    Contains LIFs, broadcast domains, IPspaces, DNS, and subnets.
    """

    model_config = ConfigDict(extra="allow")

    intercluster_lifs: list[NetworkLIF] = Field(default_factory=list)
    data_lifs: list[NetworkLIF] = Field(default_factory=list)
    management_lifs: list[NetworkLIF] = Field(default_factory=list)
    broadcast_domains: list[BroadcastDomain] = Field(default_factory=list)
    ipspaces: list[str] = Field(default_factory=list)
    dns: list[DNSInfo] = Field(default_factory=list)
    subnets: list[IPSubnetInfo] = Field(default_factory=list)


class AggregateInfo(BaseModel):
    """Storage aggregate information."""

    model_config = ConfigDict(extra="allow")

    uuid: str = ""
    name: str = ""
    node: str = ""
    state: str = ""
    type: str = ""  # hdd, ssd, hybrid
    total_size: int = 0  # bytes
    disk_count: int = 0
    disk_type: str = ""
    raid_type: str = ""
    # block_storage structural fields
    storage_type: str = ""  # hdd/hybrid/lun/ssd/vmdisk
    disk_class: str = ""  # capacity/performance/solid_state/virtual/archive/capacity_flash
    raid_size: int = 0  # max disks per RAID group
    checksum_style: str = ""  # block/advanced_zoned/mixed
    uses_partitions: bool = False  # root-data partitioning
    mirror_enabled: bool = False  # SyncMirror protection
    mirror_state: str = ""  # unmirrored/normal/degraded/resynchronizing/failed
    hybrid_cache_enabled: bool = False  # Flash Pool indicator
    # other structural fields
    snaplock_type: str = ""  # non_snaplock/compliance/enterprise
    home_node: str = ""  # home node (differs from node during takeover)
    dr_home_node: str = ""  # MetroCluster DR home node
    create_time: str = ""  # aggregate creation timestamp
    # config flags
    cloud_attach_eligible: bool = False  # FabricPool eligibility
    encryption_software: bool = False  # NAE enabled
    encryption_drive: bool = False  # SED enabled
    sidl_enabled: bool = False  # single-instance data logging
    inactive_data_reporting_enabled: bool = False  # inactive data reporting
    volume_count: int = 0  # number of volumes on the aggregate
    # expensive field (needs explicit API request)
    is_spare_low: bool = False  # disk pool health flag


class SVMInfo(BaseModel):
    """Storage Virtual Machine information."""

    model_config = ConfigDict(extra="allow")

    uuid: str = ""
    name: str = ""
    state: str = ""
    subtype: str = ""  # default, dp_destination, sync_source
    root_volume: str = ""
    root_volume_aggregate: str = ""
    allowed_protocols: list[str] = Field(default_factory=list)
    language: str = ""


class CloudTargetInfo(BaseModel):
    """Cloud object store target configuration.

    Represents a cloud target used for FabricPool tiering or SnapMirror-to-cloud.
    Available via /cloud/targets REST API (ONTAP 9.6+).
    """

    model_config = ConfigDict(extra="allow")

    name: str = ""
    uuid: str = ""
    provider_type: str = ""  # AWS_S3, Azure_Cloud, SGWS, etc.
    server: str = ""
    container: str = ""  # Bucket/container name
    owner: str = ""  # fabricpool, snapmirror
    scope: str = ""  # cluster, svm (9.12+)
    svm: str = ""
    ssl_enabled: bool = True
    authentication_type: str = ""  # key, cap, etc.
    ipspace: str = ""
    snapmirror_use: str = ""
    access_key: str = ""  # AWS/S3 access key ID
    azure_account: str = ""  # Azure account name


class VolumeInfo(BaseModel):
    """Volume information."""

    model_config = ConfigDict(extra="allow")

    uuid: str = ""
    name: str = ""
    svm: str = ""
    state: str = ""  # online, offline, restricted
    type: str = ""  # rw, dp, ls
    style: str = ""  # flexvol, flexgroup
    size: int = 0  # bytes
    autosize_mode: str = ""  # off, grow, grow_shrink
    autosize_grow_threshold: int = 0  # percentage
    autosize_shrink_threshold: int = 0  # percentage
    autosize_maximum: int = 0  # bytes
    autosize_minimum: int = 0  # bytes
    files_maximum: int = 0
    tiering_policy: str = ""  # none, snapshot-only, auto, all
    tiering_minimum_cooling_days: int = 0
    aggregate: str = ""  # FlexVol aggregate name
    aggregates: list[str] = Field(default_factory=list)  # FlexGroup aggregates
    snapshot_policy: str = ""
    export_policy: str = ""
    junction_path: str = ""
    nas_security_style: str = ""  # unix, ntfs, mixed


class ExportRuleInfo(BaseModel):
    """Export rule within an export policy."""

    model_config = ConfigDict(extra="allow")

    index: int = 0
    clients: list[str] = Field(default_factory=list)
    protocols: list[str] = Field(default_factory=list)
    ro_rule: list[str] = Field(default_factory=list)
    rw_rule: list[str] = Field(default_factory=list)
    superuser: list[str] = Field(default_factory=list)
    anonymous_user: str = ""


class ExportPolicyInfo(BaseModel):
    """NFS export policy information."""

    model_config = ConfigDict(extra="allow")

    id: int = 0
    name: str = ""
    svm: str = ""
    rules: list[ExportRuleInfo] = Field(default_factory=list)


class QtreeInfo(BaseModel):
    """Qtree information."""

    model_config = ConfigDict(extra="allow")

    id: int = 0
    name: str = ""
    svm: str = ""
    volume: str = ""
    path: str = ""
    security_style: str = ""  # unix, ntfs, mixed
    unix_permissions: str = ""
    export_policy: str = ""


class SnapshotScheduleInfo(BaseModel):
    """Schedule entry within a snapshot policy."""

    model_config = ConfigDict(extra="allow")

    schedule: str = ""
    count: int = 0
    prefix: str = ""
    snapmirror_label: str = ""


class SnapshotPolicyInfo(BaseModel):
    """Snapshot policy information."""

    model_config = ConfigDict(extra="allow")

    uuid: str = ""
    name: str = ""
    svm: str = ""
    enabled: bool = True
    scope: str = ""  # cluster, svm
    schedules: list[SnapshotScheduleInfo] = Field(default_factory=list)


class ScheduleInfo(BaseModel):
    """Job schedule information."""

    model_config = ConfigDict(extra="allow")

    uuid: str = ""
    name: str = ""
    type: str = ""  # cron, interval
    scope: str = ""  # cluster, svm
    svm: str = ""
    cron: dict[str, list[int]] = Field(default_factory=dict)
    interval: str = ""


class LunInfo(BaseModel):
    """LUN (Logical Unit Number) information."""

    model_config = ConfigDict(extra="allow")

    uuid: str = ""
    name: str = ""
    svm: str = ""
    volume: str = ""
    size: int = 0  # bytes
    os_type: str = ""  # linux, windows, vmware, etc.
    serial_number: str = ""
    enabled: bool = True
    comment: str = ""
    qos_policy: str = ""
    create_time: str = ""


class IgroupInfo(BaseModel):
    """Initiator group information."""

    model_config = ConfigDict(extra="allow")

    uuid: str = ""
    name: str = ""
    svm: str = ""
    protocol: str = ""  # fcp, iscsi, mixed
    os_type: str = ""  # linux, windows, vmware, etc.
    initiators: list[str] = Field(default_factory=list)
    comment: str = ""


class QosPolicyInfo(BaseModel):
    """QoS policy information."""

    model_config = ConfigDict(extra="allow")

    uuid: str = ""
    name: str = ""
    svm: str = ""
    scope: str = ""  # cluster, svm
    policy_class: str = ""  # preset, user_defined, system_defined
    fixed_max_throughput_iops: int = 0
    fixed_max_throughput_mbps: int = 0
    adaptive_expected_iops: int = 0
    adaptive_peak_iops: int = 0
    adaptive_block_size: str = ""  # any, 4k, 8k, etc.


class FlexCacheInfo(BaseModel):
    """FlexCache volume information."""

    model_config = ConfigDict(extra="allow")

    uuid: str = ""
    name: str = ""
    svm: str = ""
    path: str = ""
    size: int = 0  # bytes
    origins: list[str] = Field(default_factory=list)  # origin volume paths
    global_file_locking_enabled: bool = False
    dr_cache: bool = False


class StorageInfo(BaseModel):
    """Storage topology information.

    Contains aggregates, SVMs, cloud targets, volumes, qtrees,
    snapshot policies, schedules, LUNs, igroups, QoS policies,
    and FlexCache volumes.
    """

    model_config = ConfigDict(extra="allow")

    aggregates: list[AggregateInfo] = Field(default_factory=list)
    svms: list[SVMInfo] = Field(default_factory=list)
    cloud_targets: list[CloudTargetInfo] = Field(default_factory=list)
    volumes: list[VolumeInfo] = Field(default_factory=list)
    qtrees: list[QtreeInfo] = Field(default_factory=list)
    snapshot_policies: list[SnapshotPolicyInfo] = Field(default_factory=list)
    schedules: list[ScheduleInfo] = Field(default_factory=list)
    luns: list[LunInfo] = Field(default_factory=list)
    igroups: list[IgroupInfo] = Field(default_factory=list)
    qos_policies: list[QosPolicyInfo] = Field(default_factory=list)
    flexcaches: list[FlexCacheInfo] = Field(default_factory=list)


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
    mediator_address: str = ""


class SnapMirrorRelationship(BaseModel):
    """SnapMirror relationship information."""

    model_config = ConfigDict(extra="allow")

    uuid: str = ""
    source_path: str = ""
    destination_path: str = ""
    relationship_type: str = ""  # extended_data_protection, data_protection
    state: str = ""  # snapmirrored, uninitialized, broken-off


class ClusterPeer(BaseModel):
    """Cluster peering information."""

    model_config = ConfigDict(extra="allow")

    name: str = ""
    uuid: str = ""
    remote_cluster_name: str = ""
    peer_addresses: list[str] = Field(default_factory=list)
    authentication_state: str = ""
    authentication_in_use: str = ""
    encryption_state: str = ""


class SVMPeerInfo(BaseModel):
    """SVM peering information."""

    model_config = ConfigDict(extra="allow")

    uuid: str = ""
    name: str = ""
    svm: str = ""
    peer_svm: str = ""
    peer_cluster: str = ""
    state: str = ""  # peered, initiated, pending, etc.
    applications: list[str] = Field(default_factory=list)


class RelationshipsInfo(BaseModel):
    """Cluster relationships information.

    Contains SnapMirror, cluster peering, and SVM peering info.
    """

    model_config = ConfigDict(extra="allow")

    snapmirror_destinations: list[SnapMirrorRelationship] = Field(default_factory=list)
    cluster_peers: list[ClusterPeer] = Field(default_factory=list)
    svm_peers: list[SVMPeerInfo] = Field(default_factory=list)


class NFSServiceInfo(BaseModel):
    """NFS service configuration per SVM."""

    model_config = ConfigDict(extra="allow")

    svm: str = ""
    enabled: bool = False
    protocol_v3_enabled: bool = False
    protocol_v4_enabled: bool = False
    protocol_v41_enabled: bool = False
    showmount_enabled: bool = False
    vstorage_enabled: bool = False


class CIFSServiceInfo(BaseModel):
    """CIFS/SMB service configuration per SVM."""

    model_config = ConfigDict(extra="allow")

    svm: str = ""
    name: str = ""  # CIFS server name
    enabled: bool = False
    ad_domain: str = ""
    comment: str = ""
    default_unix_user: str = ""
    netbios_aliases: list[str] = Field(default_factory=list)


class DNSInfo(BaseModel):
    """DNS configuration per SVM or cluster."""

    model_config = ConfigDict(extra="allow")

    uuid: str = ""
    svm: str = ""
    scope: str = ""  # cluster, svm
    domains: list[str] = Field(default_factory=list)
    servers: list[str] = Field(default_factory=list)
    timeout: int = 0
    attempts: int = 0


class CIFSShareInfo(BaseModel):
    """CIFS/SMB share information."""

    model_config = ConfigDict(extra="allow")

    name: str = ""
    path: str = ""
    svm: str = ""
    comment: str = ""
    home_directory: bool = False
    oplocks: bool = True
    access_based_enumeration: bool = False
    change_notify: bool = True
    encryption: bool = False
    unix_symlink: str = ""  # local, widelink, disable


class S3BucketInfo(BaseModel):
    """S3 bucket information."""

    model_config = ConfigDict(extra="allow")

    uuid: str = ""
    name: str = ""
    svm: str = ""
    type: str = ""  # s3, nas-s3
    size: int = 0  # bytes
    versioning_state: str = ""  # enabled, disabled, suspended
    comment: str = ""
    nas_path: str = ""


class ProtocolsInfo(BaseModel):
    """Protocol configuration information.

    Contains export policies, CIFS shares, NFS/CIFS services,
    S3 buckets, and protocol-related data.
    """

    model_config = ConfigDict(extra="allow")

    export_policies: list[ExportPolicyInfo] = Field(default_factory=list)
    cifs_shares: list[CIFSShareInfo] = Field(default_factory=list)
    nfs_services: list[NFSServiceInfo] = Field(default_factory=list)
    cifs_services: list[CIFSServiceInfo] = Field(default_factory=list)
    s3_buckets: list[S3BucketInfo] = Field(default_factory=list)


class CachedClusterMetadata(BaseModel):
    """Complete cached metadata for a cluster.

    This is the top-level model containing all cached data categories.

    Schema Version History:
        1.0 - Initial schema with comprehensive model coverage

    Note: The cache_version field tracks the schema version of the stored data.
    When loading historical snapshots, use is_schema_compatible() to verify
    the snapshot can be safely deserialized with the current model.
    """

    model_config = ConfigDict(extra="allow")

    # Current schema version constant for reference
    CURRENT_SCHEMA_VERSION: ClassVar[str] = METADATA_SCHEMA_VERSION

    # Cache metadata
    cluster_name: str
    cached_at: datetime = Field(default_factory=_utcnow)
    cache_version: str = METADATA_SCHEMA_VERSION

    # Data categories
    cloud: list[CloudMetadata] = Field(default_factory=list)
    cluster: ClusterInfo = Field(default_factory=ClusterInfo)
    nodes: list[NodeInfo] = Field(default_factory=list)
    network: NetworkInfo = Field(default_factory=NetworkInfo)
    storage: StorageInfo = Field(default_factory=StorageInfo)
    licenses: LicenseInfo = Field(default_factory=LicenseInfo)
    ha: HAInfo = Field(default_factory=HAInfo)
    relationships: RelationshipsInfo = Field(default_factory=RelationshipsInfo)
    protocols: ProtocolsInfo = Field(default_factory=ProtocolsInfo)

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
