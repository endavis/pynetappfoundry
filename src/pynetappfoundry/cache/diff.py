"""Diff computation for cluster metadata changes.

Computes differences between two CachedClusterMetadata snapshots
for change history tracking.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pydantic import BaseModel

if TYPE_CHECKING:
    from pynetappfoundry.cache.models import CachedClusterMetadata


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


# Entity configurations: (key_field, tracked_fields)
# key_field is the attribute used to identify unique entities
# tracked_fields are the fields we compare for modifications
_ENTITY_CONFIGS: dict[str, tuple[str, list[str]]] = {
    "cloud": ("node", ["instance_id", "instance_type", "region", "provider"]),
    "nodes": (
        "name",
        ["uuid", "serial_number", "model", "is_epsilon", "location"],
    ),
    "network.intercluster_lifs": (
        "name",
        ["ip_address", "home_node"],
    ),
    "network.data_lifs": (
        "name",
        ["ip_address", "home_node"],
    ),
    "network.management_lifs": (
        "name",
        ["ip_address", "home_node"],
    ),
    "network.broadcast_domains": (
        "name",
        ["uuid", "ipspace", "mtu"],
    ),
    "storage.aggregates": (
        "name",
        ["uuid", "state", "type", "total_size", "disk_count", "disk_type", "raid_type"],
    ),
    "storage.svms": (
        "name",
        ["uuid", "state", "subtype", "allowed_protocols", "language"],
    ),
    "storage.cloud_targets": (
        "name",
        ["uuid", "provider_type", "container"],
    ),
    "storage.volumes": (
        "name",
        [
            "uuid",
            "svm",
            "state",
            "type",
            "style",
            "size",
            "aggregate",
            "snapshot_policy",
            "export_policy",
            "junction_path",
            "nas_security_style",
        ],
    ),
    "storage.qtrees": (
        "name",
        ["id", "svm", "volume", "security_style", "export_policy"],
    ),
    "storage.snapshot_policies": (
        "name",
        ["uuid", "svm", "enabled", "scope"],
    ),
    "storage.schedules": (
        "name",
        ["uuid", "type", "scope", "svm"],
    ),
    "storage.luns": (
        "name",
        ["uuid", "svm", "volume", "size", "os_type", "enabled"],
    ),
    "storage.igroups": (
        "name",
        ["uuid", "svm", "protocol", "os_type"],
    ),
    "storage.qos_policies": (
        "name",
        ["uuid", "svm", "scope", "policy_class"],
    ),
    "protocols.export_policies": (
        "name",
        ["id", "svm"],
    ),
    "protocols.cifs_shares": (
        "name",
        ["path", "svm", "home_directory", "oplocks", "encryption"],
    ),
    "protocols.nfs_services": (
        "svm",
        ["enabled", "protocol_v3_enabled", "protocol_v4_enabled", "protocol_v41_enabled"],
    ),
    "protocols.cifs_services": (
        "svm",
        ["name", "enabled", "ad_domain"],
    ),
    "network.dns": (
        "svm",
        ["uuid", "scope", "domains", "servers"],
    ),
    "licenses.feature_licenses": (
        "name",
        ["state"],
    ),
    "licenses.capacity_licenses": (
        "name",
        ["licensed_capacity", "used_capacity"],
    ),
    "relationships.snapmirror_destinations": (
        "destination_path",
        ["uuid", "state"],
    ),
    "relationships.cluster_peers": (
        "name",
        ["authentication_state"],
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
        - entity: The entity identifier
        - field: (for modified) Which field changed
        - old: (for modified) The old value
        - new: (for modified) The new value
    """
    changes: list[dict[str, Any]] = []

    # Handle initial capture (no before)
    if before is None:
        # Record all entities as "added"
        for category, (key_field, _) in _ENTITY_CONFIGS.items():
            entities = _get_entities(after, category)
            for entity in entities:
                entity_key = getattr(entity, key_field, "") or str(entity)
                changes.append(
                    {
                        "category": category,
                        "type": "added",
                        "entity": entity_key,
                    }
                )
        # Also check singleton categories
        changes.extend(_diff_cluster_info(None, after))
        changes.extend(_diff_ha_info(None, after))
        return changes

    # Compare each category
    for category, (key_field, tracked_fields) in _ENTITY_CONFIGS.items():
        before_entities = _get_entities(before, category)
        after_entities = _get_entities(after, category)
        changes.extend(
            _diff_entity_list(
                category=category,
                before_list=before_entities,
                after_list=after_entities,
                key_field=key_field,
                tracked_fields=tracked_fields,
            )
        )

    # Compare singleton categories
    changes.extend(_diff_cluster_info(before, after))
    changes.extend(_diff_ha_info(before, after))

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
    key_field: str,
    tracked_fields: list[str],
) -> list[dict[str, Any]]:
    """Diff two lists of entities.

    Args:
        category: Category name for the change entries.
        before_list: Entities from before snapshot.
        after_list: Entities from after snapshot.
        key_field: Field to use as entity identifier.
        tracked_fields: Fields to compare for modifications.

    Returns:
        List of change dictionaries.
    """
    changes: list[dict[str, Any]] = []

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
                    "entity": key,
                }
            )

    # Find added entities
    for key in after_map:
        if key not in before_map:
            changes.append(
                {
                    "category": category,
                    "type": "added",
                    "entity": key,
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
                            "entity": key,
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

    Args:
        before: Previous snapshot (None for initial).
        after: New snapshot.

    Returns:
        List of change dictionaries.
    """
    changes: list[dict[str, Any]] = []
    category = "cluster"
    tracked_fields = [
        "cluster_name",
        "cluster_uuid",
        "ontap_version",
        "model",
        "contact",
        "location",
    ]

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


def _diff_ha_info(
    before: CachedClusterMetadata | None,
    after: CachedClusterMetadata,
) -> list[dict[str, Any]]:
    """Diff HA info (singleton).

    Args:
        before: Previous snapshot (None for initial).
        after: New snapshot.

    Returns:
        List of change dictionaries.
    """
    changes: list[dict[str, Any]] = []
    category = "ha"
    tracked_fields = [
        "is_ha",
        "partner_node",
        "ha_state",
        "mediator_address",
    ]

    if before is None:
        # Initial capture - just record existence if HA is configured
        if after.ha.is_ha:
            changes.append(
                {
                    "category": category,
                    "type": "added",
                    "entity": "ha_config",
                }
            )
        return changes

    before_ha = before.ha
    after_ha = after.ha

    for field in tracked_fields:
        old_val = getattr(before_ha, field, None)
        new_val = getattr(after_ha, field, None)

        if old_val != new_val:
            changes.append(
                {
                    "category": category,
                    "type": "modified",
                    "entity": "ha_config",
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
