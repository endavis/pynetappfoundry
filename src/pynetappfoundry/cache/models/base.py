"""Schema versioning, protocols, container models, and top-level cache model."""

from __future__ import annotations

from datetime import UTC, datetime
from functools import cached_property
from typing import ClassVar, Protocol, runtime_checkable

from pydantic import BaseModel, ConfigDict, Field

from pynetappfoundry.cache.models.cloud import CloudMetadata, CloudTargetInfo
from pynetappfoundry.cache.models.cluster import (
    ClusterInfo,
    HAInfo,
    LicenseInfo,
    NodeInfo,
    ScheduleInfo,
)
from pynetappfoundry.cache.models.name_services import DNSInfo
from pynetappfoundry.cache.models.network import (
    BroadcastDomain,
    IPSubnetInfo,
    NetworkLIF,
)
from pynetappfoundry.cache.models.protocols import (
    CIFSServiceInfo,
    CIFSShareInfo,
    ExportPolicyInfo,
    IgroupInfo,
    LunInfo,
    NFSServiceInfo,
    QtreeInfo,
    S3BucketInfo,
)
from pynetappfoundry.cache.models.snapmirror import SnapMirrorRelationship
from pynetappfoundry.cache.models.storage import (
    AggregateInfo,
    FlexCacheInfo,
    QosPolicyInfo,
    SnapshotPolicyInfo,
    VolumeInfo,
)
from pynetappfoundry.cache.models.svm import ClusterPeer, SVMInfo, SVMPeerInfo

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


@runtime_checkable
class HasUUID(Protocol):
    """Protocol for models that have a uuid field."""

    uuid: str


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


class RelationshipsInfo(BaseModel):
    """Cluster relationships information.

    Contains SnapMirror, cluster peering, and SVM peering info.
    """

    model_config = ConfigDict(extra="allow")

    snapmirror_destinations: list[SnapMirrorRelationship] = Field(default_factory=list)
    cluster_peers: list[ClusterPeer] = Field(default_factory=list)
    svm_peers: list[SVMPeerInfo] = Field(default_factory=list)


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

    @cached_property
    def uuid_index(self) -> dict[str, HasUUID]:
        """Build a flat UUID -> object index across all cached object types.

        Discovers UUID-bearing objects via introspection: walks all model fields
        on this instance and nested BaseModel containers, indexing any list item
        that satisfies the HasUUID protocol.

        Built lazily on first access and cached for the lifetime of this object.
        Objects with empty uuid strings are excluded.

        Returns:
            Dictionary mapping UUID strings to their corresponding model objects.
        """
        index: dict[str, HasUUID] = {}
        for field_name in type(self).model_fields:
            value = getattr(self, field_name)
            if isinstance(value, list):
                self._index_list(value, index)
            elif isinstance(value, BaseModel):
                for nested_name in type(value).model_fields:
                    nested_value = getattr(value, nested_name)
                    if isinstance(nested_value, list):
                        self._index_list(nested_value, index)
        return index

    @staticmethod
    def _index_list(items: list[object], index: dict[str, HasUUID]) -> None:
        """Add HasUUID items from a list to the index."""
        for item in items:
            if isinstance(item, HasUUID) and item.uuid:
                index[item.uuid] = item
