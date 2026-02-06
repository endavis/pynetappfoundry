"""Cluster metadata caching module.

Provides caching infrastructure for ONTAP cluster metadata that
doesn't change frequently. Cache is manually refreshed via CLI.

Usage:
    from pynetappfoundry.cache import ClusterMetadataDB, MetadataCollector

    # Initialize database
    db = ClusterMetadataDB(config=config)

    # Collect and cache metadata
    collector = MetadataCollector(api_client=api, cli_client=cli)
    metadata = collector.collect_all("mycluster")
    db.set("mycluster", metadata)

    # Retrieve cached data
    cached = db.get("mycluster")
"""

from pynetappfoundry.cache.collector import (
    CollectionError,
    CollectionPhase,
    MetadataCollector,
    ProgressCallback,
    ProgressInfo,
)
from pynetappfoundry.cache.db import ClusterMetadataDB
from pynetappfoundry.cache.diff import ChangeEntry, compute_diff, format_diff_summary
from pynetappfoundry.cache.history_db import CacheHistoryDB
from pynetappfoundry.cache.models import (
    METADATA_SCHEMA_MIN_COMPATIBLE,
    METADATA_SCHEMA_VERSION,
    AggregateInfo,
    BroadcastDomain,
    CachedClusterMetadata,
    CapacityLicense,
    CIFSServiceInfo,
    CIFSShareInfo,
    CloudMetadata,
    ClusterInfo,
    ClusterPeer,
    DNSInfo,
    ExportPolicyInfo,
    ExportRuleInfo,
    HAInfo,
    IgroupInfo,
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
    ScheduleInfo,
    SnapMirrorRelationship,
    SnapshotPolicyInfo,
    SnapshotScheduleInfo,
    StorageInfo,
    SVMInfo,
    VolumeInfo,
    is_schema_compatible,
    parse_schema_version,
)

__all__ = [
    "METADATA_SCHEMA_MIN_COMPATIBLE",
    "METADATA_SCHEMA_VERSION",
    "AggregateInfo",
    "BroadcastDomain",
    "CIFSServiceInfo",
    "CIFSShareInfo",
    "CacheHistoryDB",
    "CachedClusterMetadata",
    "CapacityLicense",
    "ChangeEntry",
    "CloudMetadata",
    "ClusterInfo",
    "ClusterMetadataDB",
    "ClusterPeer",
    "CollectionError",
    "CollectionPhase",
    "DNSInfo",
    "ExportPolicyInfo",
    "ExportRuleInfo",
    "HAInfo",
    "IgroupInfo",
    "LicenseFeature",
    "LicenseInfo",
    "LunInfo",
    "MetadataCollector",
    "NFSServiceInfo",
    "NetworkInfo",
    "NetworkLIF",
    "NodeInfo",
    "ProgressCallback",
    "ProgressInfo",
    "ProtocolsInfo",
    "QosPolicyInfo",
    "QtreeInfo",
    "RelationshipsInfo",
    "SVMInfo",
    "ScheduleInfo",
    "SnapMirrorRelationship",
    "SnapshotPolicyInfo",
    "SnapshotScheduleInfo",
    "StorageInfo",
    "VolumeInfo",
    "compute_diff",
    "format_diff_summary",
    "is_schema_compatible",
    "parse_schema_version",
]
