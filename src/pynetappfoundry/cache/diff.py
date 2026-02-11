"""Diff computation for cluster metadata changes.

Computes differences between two CachedClusterMetadata snapshots
for change history tracking.

Tracked fields are derived dynamically from each model's ``model_fields``,
so new fields added to cache models are automatically tracked without
manual updates to this module.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

from pydantic import BaseModel

from pynetappfoundry.cache._base import CacheModel
from pynetappfoundry.cache.cloud.metadata.model import CloudMetadata
from pynetappfoundry.cache.cloud.targets.model import CloudTargetInfo
from pynetappfoundry.cache.cluster.licensing.model import CapacityLicense, LicenseFeature
from pynetappfoundry.cache.cluster.model import ClusterInfo
from pynetappfoundry.cache.cluster.nodes.model import NodeInfo
from pynetappfoundry.cache.cluster.peers.model import ClusterPeer
from pynetappfoundry.cache.cluster.schedules.model import ScheduleInfo
from pynetappfoundry.cache.name_services.dns.model import DNSInfo
from pynetappfoundry.cache.network.ethernet.broadcast_domains.model import BroadcastDomain
from pynetappfoundry.cache.network.ip.interfaces.model import NetworkLIF
from pynetappfoundry.cache.network.ip.subnets.model import IPSubnetInfo
from pynetappfoundry.cache.protocols.cifs.services.model import CIFSServiceInfo
from pynetappfoundry.cache.protocols.cifs.shares.model import CIFSShareInfo
from pynetappfoundry.cache.protocols.nfs.export_policies.model import ExportPolicyInfo
from pynetappfoundry.cache.protocols.nfs.services.model import NFSServiceInfo
from pynetappfoundry.cache.protocols.s3.buckets.model import S3BucketInfo
from pynetappfoundry.cache.protocols.san.igroups.model import IgroupInfo
from pynetappfoundry.cache.snapmirror.relationships.model import SnapMirrorRelationship
from pynetappfoundry.cache.storage.aggregates.model import AggregateInfo
from pynetappfoundry.cache.storage.flexcache.model import FlexCacheInfo
from pynetappfoundry.cache.storage.luns.model import LunInfo
from pynetappfoundry.cache.storage.qos.model import QosPolicyInfo
from pynetappfoundry.cache.storage.qtrees.model import QtreeInfo
from pynetappfoundry.cache.storage.snapshot_policies.model import SnapshotPolicyInfo
from pynetappfoundry.cache.storage.volumes.model import VolumeInfo
from pynetappfoundry.cache.svm.model import SVMInfo
from pynetappfoundry.cache.svm.peers.model import SVMPeerInfo

if TYPE_CHECKING:
    from pynetappfoundry.cache._metadata import CachedClusterMetadata


class ChangeEntry(BaseModel):
    """A single change entry in the diff summary.

    Attributes:
        category: The metadata category (e.g., 'nodes', 'storage.aggregates').
        change_type: Type of change ('added', 'removed', 'modified').
        entity: The entity identifier (e.g., node name, aggregate name).
        field: For modifications, the field that changed.
        old_value: For modifications, the old value.
        new_value: For modifications, the new value.
    """

    category: str
    change_type: str  # 'added', 'removed', 'modified'
    entity: str
    field: str | None = None
    old_value: Any = None
    new_value: Any = None


@dataclass(frozen=True, slots=True)
class EntityConfig:
    """Configuration for diffing a category of entities.

    Attributes:
        key_field: Field used to uniquely identify entities (usually 'uuid' or 'name').
        model_class: The Pydantic model class. Tracked fields are derived from
            model_class.model_fields at runtime, excluding key_field.
        display_field: Field or format string for human-readable entity names
            in change output. If it contains '{', it is treated as a format
            template (e.g., '{source_path}->{destination_path}'); otherwise
            it is a plain attribute name.
    """

    key_field: str
    model_class: type[CacheModel]
    display_field: str


def _get_tracked_fields(config: EntityConfig) -> list[str]:
    """Derive tracked fields from model_class.model_fields, excluding key_field.

    Args:
        config: Entity configuration.

    Returns:
        List of field names to compare for modifications.
    """
    return [f for f in config.model_class.model_fields if f != config.key_field]


def _get_display_name(entity: Any, display_field: str) -> str:
    """Get a human-readable display name for an entity.

    If *display_field* contains ``{``, it is treated as a format template
    where placeholders are resolved from entity attributes.  Otherwise it
    is a simple attribute name lookup.

    Args:
        entity: The model instance.
        display_field: Attribute name or format string.

    Returns:
        Display name string, or ``str(entity)`` as fallback.
    """
    if "{" in display_field:
        try:
            fmt_dict = {field: getattr(entity, field, "") for field in type(entity).model_fields}
            return display_field.format(**fmt_dict)
        except (KeyError, AttributeError):
            return str(entity)
    value = getattr(entity, display_field, "") or ""
    return value or str(entity)


# Entity configurations: maps category path -> EntityConfig.
# key_field is used for identity matching between snapshots.
# display_field is the human-readable label shown in change output.
# Tracked fields are derived automatically from model_class.model_fields.
_ENTITY_CONFIGS: dict[str, EntityConfig] = {
    # --- Models WITH uuid (use uuid as stable identity key) ---
    "nodes": EntityConfig(
        key_field="uuid",
        model_class=NodeInfo,
        display_field="name",
    ),
    "network.broadcast_domains": EntityConfig(
        key_field="uuid",
        model_class=BroadcastDomain,
        display_field="name",
    ),
    "network.subnets": EntityConfig(
        key_field="uuid",
        model_class=IPSubnetInfo,
        display_field="name",
    ),
    "network.dns": EntityConfig(
        key_field="uuid",
        model_class=DNSInfo,
        display_field="svm",
    ),
    "storage.aggregates": EntityConfig(
        key_field="uuid",
        model_class=AggregateInfo,
        display_field="name",
    ),
    "storage.svms": EntityConfig(
        key_field="uuid",
        model_class=SVMInfo,
        display_field="name",
    ),
    "storage.cloud_targets": EntityConfig(
        key_field="uuid",
        model_class=CloudTargetInfo,
        display_field="name",
    ),
    "storage.volumes": EntityConfig(
        key_field="uuid",
        model_class=VolumeInfo,
        display_field="name",
    ),
    "storage.snapshot_policies": EntityConfig(
        key_field="uuid",
        model_class=SnapshotPolicyInfo,
        display_field="name",
    ),
    "storage.schedules": EntityConfig(
        key_field="uuid",
        model_class=ScheduleInfo,
        display_field="name",
    ),
    "storage.luns": EntityConfig(
        key_field="uuid",
        model_class=LunInfo,
        display_field="name",
    ),
    "storage.igroups": EntityConfig(
        key_field="uuid",
        model_class=IgroupInfo,
        display_field="name",
    ),
    "storage.qos_policies": EntityConfig(
        key_field="uuid",
        model_class=QosPolicyInfo,
        display_field="name",
    ),
    "storage.flexcaches": EntityConfig(
        key_field="uuid",
        model_class=FlexCacheInfo,
        display_field="name",
    ),
    "protocols.s3_buckets": EntityConfig(
        key_field="uuid",
        model_class=S3BucketInfo,
        display_field="name",
    ),
    "relationships.snapmirror_destinations": EntityConfig(
        key_field="uuid",
        model_class=SnapMirrorRelationship,
        display_field="{source_path}->{destination_path}",
    ),
    "relationships.cluster_peers": EntityConfig(
        key_field="uuid",
        model_class=ClusterPeer,
        display_field="name",
    ),
    "relationships.svm_peers": EntityConfig(
        key_field="uuid",
        model_class=SVMPeerInfo,
        display_field="name",
    ),
    # --- Models WITHOUT uuid (keep current key) ---
    "cloud": EntityConfig(
        key_field="node",
        model_class=CloudMetadata,
        display_field="node",
    ),
    "network.intercluster_lifs": EntityConfig(
        key_field="name",
        model_class=NetworkLIF,
        display_field="name",
    ),
    "network.data_lifs": EntityConfig(
        key_field="name",
        model_class=NetworkLIF,
        display_field="name",
    ),
    "network.management_lifs": EntityConfig(
        key_field="name",
        model_class=NetworkLIF,
        display_field="name",
    ),
    "storage.qtrees": EntityConfig(
        key_field="name",
        model_class=QtreeInfo,
        display_field="name",
    ),
    "protocols.export_policies": EntityConfig(
        key_field="name",
        model_class=ExportPolicyInfo,
        display_field="name",
    ),
    "protocols.cifs_shares": EntityConfig(
        key_field="name",
        model_class=CIFSShareInfo,
        display_field="name",
    ),
    "protocols.nfs_services": EntityConfig(
        key_field="svm",
        model_class=NFSServiceInfo,
        display_field="svm",
    ),
    "protocols.cifs_services": EntityConfig(
        key_field="svm",
        model_class=CIFSServiceInfo,
        display_field="svm",
    ),
    "licenses.feature_licenses": EntityConfig(
        key_field="name",
        model_class=LicenseFeature,
        display_field="name",
    ),
    "licenses.capacity_licenses": EntityConfig(
        key_field="name",
        model_class=CapacityLicense,
        display_field="name",
    ),
}


def compute_diff(
    before: CachedClusterMetadata | None,
    after: CachedClusterMetadata,
) -> list[dict[str, Any]]:
    """Compute differences between two metadata snapshots.

    Args:
        before: Previous metadata snapshot (None for initial capture).
        after: New metadata snapshot.

    Returns:
        List of change dictionaries with keys:
        - category: The category path (e.g., 'nodes', 'storage.aggregates')
        - type: 'added', 'removed', or 'modified'
        - entity: The entity display name
        - field: (for modified) Which field changed
        - old: (for modified) The old value
        - new: (for modified) The new value
    """
    changes: list[dict[str, Any]] = []

    # Handle initial capture (no before)
    if before is None:
        # Record all entities as "added"
        for category, config in _ENTITY_CONFIGS.items():
            entities = _get_entities(after, category)
            for entity in entities:
                display = _get_display_name(entity, config.display_field)
                changes.append(
                    {
                        "category": category,
                        "type": "added",
                        "entity": display,
                    }
                )
        # Also check singleton categories
        changes.extend(_diff_cluster_info(None, after))
        changes.extend(_diff_mediator_info(None, after))
        return changes

    # Compare each category
    for category, config in _ENTITY_CONFIGS.items():
        before_entities = _get_entities(before, category)
        after_entities = _get_entities(after, category)
        changes.extend(
            _diff_entity_list(
                category=category,
                before_list=before_entities,
                after_list=after_entities,
                config=config,
            )
        )

    # Compare singleton categories
    changes.extend(_diff_cluster_info(before, after))
    changes.extend(_diff_mediator_info(before, after))

    return changes


def _get_entities(metadata: CachedClusterMetadata, category: str) -> list[Any]:
    """Get the entity list for a given category path.

    Args:
        metadata: The metadata object.
        category: Dot-separated category path (e.g., 'storage.aggregates').

    Returns:
        List of entities for that category.
    """
    parts = category.split(".")
    obj: Any = metadata

    for part in parts:
        if obj is None:
            return []
        obj = getattr(obj, part, None)

    if obj is None:
        return []
    if isinstance(obj, list):
        return obj
    return [obj]


def _diff_entity_list(
    category: str,
    before_list: list[Any],
    after_list: list[Any],
    config: EntityConfig,
) -> list[dict[str, Any]]:
    """Diff two lists of entities.

    Args:
        category: Category name for the change entries.
        before_list: Entities from before snapshot.
        after_list: Entities from after snapshot.
        config: EntityConfig with key_field, model_class, and display_field.

    Returns:
        List of change dictionaries.
    """
    changes: list[dict[str, Any]] = []
    key_field = config.key_field
    tracked_fields = _get_tracked_fields(config)

    # Build lookup maps by key
    before_map: dict[str, Any] = {}
    for entity in before_list:
        key = getattr(entity, key_field, "") or ""
        if key:
            before_map[key] = entity

    after_map: dict[str, Any] = {}
    for entity in after_list:
        key = getattr(entity, key_field, "") or ""
        if key:
            after_map[key] = entity

    # Find removed entities
    for key in before_map:
        if key not in after_map:
            changes.append(
                {
                    "category": category,
                    "type": "removed",
                    "entity": _get_display_name(before_map[key], config.display_field),
                }
            )

    # Find added entities
    for key in after_map:
        if key not in before_map:
            changes.append(
                {
                    "category": category,
                    "type": "added",
                    "entity": _get_display_name(after_map[key], config.display_field),
                }
            )

    # Find modified entities
    for key in before_map:
        if key in after_map:
            before_entity = before_map[key]
            after_entity = after_map[key]

            for field in tracked_fields:
                old_val = getattr(before_entity, field, None)
                new_val = getattr(after_entity, field, None)

                if old_val != new_val:
                    changes.append(
                        {
                            "category": category,
                            "type": "modified",
                            "entity": _get_display_name(after_entity, config.display_field),
                            "field": field,
                            "old": old_val,
                            "new": new_val,
                        }
                    )

    return changes


def _diff_cluster_info(
    before: CachedClusterMetadata | None,
    after: CachedClusterMetadata,
) -> list[dict[str, Any]]:
    """Diff cluster info (singleton).

    Tracked fields are derived dynamically from ClusterInfo.model_fields.

    Args:
        before: Previous snapshot (None for initial).
        after: New snapshot.

    Returns:
        List of change dictionaries.
    """
    changes: list[dict[str, Any]] = []
    category = "cluster"
    tracked_fields = list(ClusterInfo.model_fields)

    if before is None:
        # Initial capture - just record existence
        if after.cluster.cluster_name:
            changes.append(
                {
                    "category": category,
                    "type": "added",
                    "entity": after.cluster.cluster_name or "cluster",
                }
            )
        return changes

    before_cluster = before.cluster
    after_cluster = after.cluster

    for field in tracked_fields:
        old_val = getattr(before_cluster, field, None)
        new_val = getattr(after_cluster, field, None)

        if old_val != new_val:
            changes.append(
                {
                    "category": category,
                    "type": "modified",
                    "entity": after_cluster.cluster_name or "cluster",
                    "field": field,
                    "old": old_val,
                    "new": new_val,
                }
            )

    return changes


def _diff_mediator_info(
    before: CachedClusterMetadata | None,
    after: CachedClusterMetadata,
) -> list[dict[str, Any]]:
    """Diff mediator info (singleton).

    Tracked fields are derived dynamically from MediatorInfo.model_fields.

    Args:
        before: Previous snapshot (None for initial).
        after: New snapshot.

    Returns:
        List of change dictionaries.
    """
    from pynetappfoundry.cache.cluster.mediators.model import MediatorInfo

    changes: list[dict[str, Any]] = []
    category = "mediator"
    tracked_fields = list(MediatorInfo.model_fields)

    if before is None:
        # Initial capture - record mediator if any field is populated
        mediator = after.mediator
        if any(getattr(mediator, f) for f in tracked_fields):
            changes.append(
                {
                    "category": category,
                    "type": "added",
                    "entity": "mediator_config",
                }
            )
        return changes

    before_mediator = before.mediator
    after_mediator = after.mediator

    for field in tracked_fields:
        old_val = getattr(before_mediator, field, None)
        new_val = getattr(after_mediator, field, None)

        if old_val != new_val:
            changes.append(
                {
                    "category": category,
                    "type": "modified",
                    "entity": "mediator_config",
                    "field": field,
                    "old": old_val,
                    "new": new_val,
                }
            )

    return changes


def format_diff_summary(changes: list[dict[str, object]]) -> str:
    """Format a diff summary for display.

    Args:
        changes: List of change dictionaries from compute_diff.

    Returns:
        Human-readable summary string.
    """
    if not changes:
        return "No changes detected."

    lines: list[str] = []
    added = [c for c in changes if c["type"] == "added"]
    removed = [c for c in changes if c["type"] == "removed"]
    modified = [c for c in changes if c["type"] == "modified"]

    if added:
        lines.append(f"Added ({len(added)}):")
        for change in added:
            lines.append(f"  + {change['category']}: {change['entity']}")

    if removed:
        lines.append(f"Removed ({len(removed)}):")
        for change in removed:
            lines.append(f"  - {change['category']}: {change['entity']}")

    if modified:
        lines.append(f"Modified ({len(modified)}):")
        for change in modified:
            field = change.get("field", "")
            old = change.get("old", "")
            new = change.get("new", "")
            lines.append(f"  ~ {change['category']}: {change['entity']}.{field}: {old} -> {new}")

    return "\n".join(lines)
