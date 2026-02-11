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

# Layer 1: Base class, protocol, schema utilities
from pynetappfoundry.cache._base import (
    METADATA_SCHEMA_MIN_COMPATIBLE,
    METADATA_SCHEMA_VERSION,
    CacheModel,
    HasUUID,
    is_schema_compatible,
    parse_schema_version,
)

# Layer 3: Container models (import leaf models from above)
from pynetappfoundry.cache._metadata import (
    CachedClusterMetadata,
    HAInfo,
    RelationshipsInfo,
)

# Layer 1: Registry
from pynetappfoundry.cache._registry import model_registry

# Layer 2: Leaf models (import triggers __init_subclass__ auto-registration)
from pynetappfoundry.cache.cloud.metadata import CloudMetadata
from pynetappfoundry.cache.cloud.targets import CloudTargetInfo
from pynetappfoundry.cache.cluster import ClusterInfo
from pynetappfoundry.cache.cluster.licensing import (
    CapacityLicense,
    LicenseFeature,
    LicenseInfo,
)
from pynetappfoundry.cache.cluster.nodes import NodeInfo
from pynetappfoundry.cache.cluster.peers import ClusterPeer
from pynetappfoundry.cache.cluster.schedules import ScheduleInfo

# Infrastructure (collector, db, diff, etc.)
from pynetappfoundry.cache.collector import (
    CollectionError,
    CollectionPhase,
    MetadataCollector,
    ProgressCallback,
    ProgressInfo,
)
from pynetappfoundry.cache.db import ClusterMetadataDB
from pynetappfoundry.cache.diff import ChangeEntry, compute_diff, format_diff_summary
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.history_db import CacheHistoryDB
from pynetappfoundry.cache.name_services.dns import DNSInfo
from pynetappfoundry.cache.network import NetworkInfo
from pynetappfoundry.cache.network.ethernet.broadcast_domains import BroadcastDomain
from pynetappfoundry.cache.network.ip.interfaces import NetworkLIF
from pynetappfoundry.cache.network.ip.subnets import IPSubnetInfo
from pynetappfoundry.cache.protocols import ProtocolsInfo
from pynetappfoundry.cache.protocols.cifs.services import CIFSServiceInfo
from pynetappfoundry.cache.protocols.cifs.shares import CIFSShareInfo
from pynetappfoundry.cache.protocols.nfs.export_policies import (
    ExportPolicyInfo,
    ExportRuleInfo,
)
from pynetappfoundry.cache.protocols.nfs.services import NFSServiceInfo
from pynetappfoundry.cache.protocols.s3.buckets import S3BucketInfo
from pynetappfoundry.cache.protocols.san.igroups import IgroupInfo
from pynetappfoundry.cache.snapmirror.relationships import SnapMirrorRelationship
from pynetappfoundry.cache.storage import StorageInfo
from pynetappfoundry.cache.storage.aggregates import AggregateInfo
from pynetappfoundry.cache.storage.flexcache import FlexCacheInfo
from pynetappfoundry.cache.storage.luns import LunInfo
from pynetappfoundry.cache.storage.qos import QosPolicyInfo
from pynetappfoundry.cache.storage.qtrees import QtreeInfo
from pynetappfoundry.cache.storage.snapshot_policies import (
    SnapshotPolicyInfo,
    SnapshotScheduleInfo,
)
from pynetappfoundry.cache.storage.volumes import VolumeInfo
from pynetappfoundry.cache.svm import SVMInfo
from pynetappfoundry.cache.svm.peers import SVMPeerInfo

__all__ = [
    "METADATA_SCHEMA_MIN_COMPATIBLE",
    "METADATA_SCHEMA_VERSION",
    "AggregateInfo",
    "BroadcastDomain",
    "CIFSServiceInfo",
    "CIFSShareInfo",
    "CacheHistoryDB",
    "CacheModel",
    "CachedClusterMetadata",
    "CapacityLicense",
    "ChangeEntry",
    "CloudMetadata",
    "CloudTargetInfo",
    "ClusterInfo",
    "ClusterMetadataDB",
    "ClusterPeer",
    "CollectionError",
    "CollectionPhase",
    "DNSInfo",
    "ExportPolicyInfo",
    "ExportRuleInfo",
    "FieldMapping",
    "FlexCacheInfo",
    "HAInfo",
    "HasUUID",
    "IPSubnetInfo",
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
    "S3BucketInfo",
    "SVMInfo",
    "SVMPeerInfo",
    "ScheduleInfo",
    "SnapMirrorRelationship",
    "SnapshotPolicyInfo",
    "SnapshotScheduleInfo",
    "StorageInfo",
    "TypeMapping",
    "VolumeInfo",
    "compute_diff",
    "format_diff_summary",
    "is_schema_compatible",
    "model_registry",
    "parse_schema_version",
]
