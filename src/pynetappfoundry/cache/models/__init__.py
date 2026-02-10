"""Pydantic models for cached cluster metadata.

This package organizes cache models by ONTAP REST API category:
- cloud: Cloud provider metadata (/cloud)
- cluster: Cluster identity, nodes, licenses, HA, schedules (/cluster)
- name_services: DNS configuration (/name-services)
- network: LIFs, broadcast domains, subnets (/network)
- protocols: Export policies, NFS/CIFS/S3, LUNs, igroups (/protocols)
- snapmirror: SnapMirror relationships (/snapmirror)
- storage: Aggregates, volumes, snapshots, QoS, FlexCache (/storage)
- svm: SVMs and peering (/svm, /cluster/peers)
- base: Schema versioning, container models, CachedClusterMetadata
"""

from __future__ import annotations

from pynetappfoundry.cache.models.base import (
    METADATA_SCHEMA_MIN_COMPATIBLE,
    METADATA_SCHEMA_VERSION,
    CachedClusterMetadata,
    HasUUID,
    NetworkInfo,
    ProtocolsInfo,
    RelationshipsInfo,
    StorageInfo,
    _utcnow,
    is_schema_compatible,
    parse_schema_version,
)
from pynetappfoundry.cache.models.cloud import CloudMetadata, CloudTargetInfo
from pynetappfoundry.cache.models.cluster import (
    CapacityLicense,
    ClusterInfo,
    HAInfo,
    LicenseFeature,
    LicenseInfo,
    NodeInfo,
    ScheduleInfo,
)
from pynetappfoundry.cache.models.name_services import DNSInfo
from pynetappfoundry.cache.models.network import BroadcastDomain, IPSubnetInfo, NetworkLIF
from pynetappfoundry.cache.models.protocols import (
    CIFSServiceInfo,
    CIFSShareInfo,
    ExportPolicyInfo,
    ExportRuleInfo,
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
    SnapshotScheduleInfo,
    VolumeInfo,
)
from pynetappfoundry.cache.models.svm import ClusterPeer, SVMInfo, SVMPeerInfo

# Resolve forward references from TYPE_CHECKING imports in base.py.
# Container models and CachedClusterMetadata use string annotations for types
# defined in leaf modules; model_rebuild() resolves them now that all types
# are imported into this namespace.
NetworkInfo.model_rebuild()
StorageInfo.model_rebuild()
RelationshipsInfo.model_rebuild()
ProtocolsInfo.model_rebuild()
CachedClusterMetadata.model_rebuild()

__all__ = [
    "METADATA_SCHEMA_MIN_COMPATIBLE",
    "METADATA_SCHEMA_VERSION",
    "AggregateInfo",
    "BroadcastDomain",
    "CIFSServiceInfo",
    "CIFSShareInfo",
    "CachedClusterMetadata",
    "CapacityLicense",
    "CloudMetadata",
    "CloudTargetInfo",
    "ClusterInfo",
    "ClusterPeer",
    "DNSInfo",
    "ExportPolicyInfo",
    "ExportRuleInfo",
    "FlexCacheInfo",
    "HAInfo",
    "HasUUID",
    "IPSubnetInfo",
    "IgroupInfo",
    "LicenseFeature",
    "LicenseInfo",
    "LunInfo",
    "NFSServiceInfo",
    "NetworkInfo",
    "NetworkLIF",
    "NodeInfo",
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
    "VolumeInfo",
    "_utcnow",
    "is_schema_compatible",
    "parse_schema_version",
]
