"""Cross-cutting metadata models — top-level container and HA/relationships.

These models don't map to a single ONTAP REST API URL path.
CachedClusterMetadata is the root container (register=False).
"""

from __future__ import annotations

from datetime import datetime
from functools import cached_property
from typing import ClassVar

from pydantic import BaseModel, Field

from pynetappfoundry.cache._base import (
    METADATA_SCHEMA_VERSION,
    CacheModel,
    HasUUID,
    _utcnow,
)
from pynetappfoundry.cache.cloud.metadata.model import CloudMetadata
from pynetappfoundry.cache.cluster.licensing.model import LicenseInfo
from pynetappfoundry.cache.cluster.model import ClusterInfo
from pynetappfoundry.cache.cluster.nodes.model import NodeInfo
from pynetappfoundry.cache.network.model import NetworkInfo
from pynetappfoundry.cache.protocols.model import ProtocolsInfo
from pynetappfoundry.cache.snapmirror.relationships.model import (
    SnapMirrorRelationship,
)
from pynetappfoundry.cache.storage.model import StorageInfo
from pynetappfoundry.cache.svm.peers.model import SVMPeerInfo


class HAInfo(CacheModel):
    """High Availability configuration information.

    For CVO HA configurations.
    """

    is_ha: bool = False
    partner_node: str = ""
    ha_state: str = ""
    mediator_address: str = ""


class RelationshipsInfo(CacheModel):
    """Cluster relationships information.

    Contains SnapMirror, cluster peering, and SVM peering info.
    """

    snapmirror_destinations: list[SnapMirrorRelationship] = Field(default_factory=list)
    cluster_peers: list[ClusterPeer] = Field(default_factory=list)
    svm_peers: list[SVMPeerInfo] = Field(default_factory=list)


# Deferred import to avoid circular reference — ClusterPeer used above in a
# forward-reference string annotation, resolved here after the class body.
from pynetappfoundry.cache.cluster.peers.model import ClusterPeer  # noqa: E402

RelationshipsInfo.model_rebuild()


class CachedClusterMetadata(CacheModel, register=False):
    """Complete cached metadata for a cluster.

    This is the top-level model containing all cached data categories.

    Schema Version History:
        1.0 - Initial schema with comprehensive model coverage

    Note: The cache_version field tracks the schema version of the stored data.
    When loading historical snapshots, use is_schema_compatible() to verify
    the snapshot can be safely deserialized with the current model.
    """

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
        """Build a flat UUID → object index across all cached object types.

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
