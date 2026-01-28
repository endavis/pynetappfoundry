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

from pynetappfoundry.cache.collector import CollectionError, MetadataCollector
from pynetappfoundry.cache.db import ClusterMetadataDB
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

__all__ = [
    "AggregateInfo",
    "BroadcastDomain",
    "CachedClusterMetadata",
    "CapacityLicense",
    "CloudMetadata",
    "ClusterInfo",
    "ClusterMetadataDB",
    "ClusterPeer",
    "CollectionError",
    "HAInfo",
    "LicenseFeature",
    "LicenseInfo",
    "MetadataCollector",
    "NetworkInfo",
    "NetworkLIF",
    "NodeInfo",
    "RelationshipsInfo",
    "SVMInfo",
    "SnapMirrorRelationship",
    "StorageInfo",
]
