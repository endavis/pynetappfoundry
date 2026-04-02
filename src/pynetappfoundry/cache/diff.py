"""Diff computation for cluster metadata changes.

Computes differences between two CachedClusterMetadata snapshots
for change history tracking.

Tracked fields are derived dynamically from each model's ``model_fields``,
so new fields added to cache models are automatically tracked without
manual updates to this module.

Entity configurations are built dynamically by introspecting
``CachedClusterMetadata`` model fields and looking up ``TypeMapping``
entries in the model registry.  A small overrides dict handles
models whose key/display fields don't follow the convention
(``uuid`` if present, else ``name``).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, get_args, get_origin

from pydantic import BaseModel

from pynetappfoundry.cache._base import CacheModel
from pynetappfoundry.models.ontap.cloud.metadata.model import CloudMetadata
from pynetappfoundry.models.ontap.cluster.licensing.licenses.model import (
    OntapLicensePackageResponse,
)
from pynetappfoundry.models.ontap.cluster.model import ClusterInfo
from pynetappfoundry.models.ontap.name_services.dns.model import OntapDns
from pynetappfoundry.models.ontap.protocols.cifs.services.model import OntapCifsService
from pynetappfoundry.models.ontap.protocols.cifs.shares.model import OntapCifsShare
from pynetappfoundry.models.ontap.protocols.nfs.export_policies.model import OntapExportPolicy
from pynetappfoundry.models.ontap.protocols.nfs.services.model import OntapNfsService
from pynetappfoundry.models.ontap.snapmirror.relationships.model import (
    OntapSnapmirrorRelationship,
)
from pynetappfoundry.models.ontap.storage.qtrees.model import OntapQtree

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


def _is_populated(value: Any) -> bool:
    """Check whether a value is meaningfully populated.

    Pydantic sub-models with all-default/empty fields are considered
    *not* populated, so they behave like ``""`` or ``0`` when deciding
    whether a parent record should be treated as "present".
    """
    if isinstance(value, BaseModel):
        return any(_is_populated(getattr(value, f)) for f in type(value).model_fields)
    return bool(value)


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


def _flatten_model_attrs(entity: Any, prefix: str = "") -> dict[str, Any]:
    """Build a flat dict of model attributes including dotted nested paths.

    For a model with ``source.path``, the returned dict contains both
    ``"source": <OntapSource(...)>`` and ``"source.path": "svm1:vol1"``.
    """
    result: dict[str, Any] = {}
    model_cls = type(entity)
    if not hasattr(model_cls, "model_fields"):
        return result
    for field_name in model_cls.model_fields:
        value = getattr(entity, field_name, "")
        key = f"{prefix}{field_name}" if prefix else field_name
        result[key] = value
        # Recurse into nested Pydantic models (not lists/dicts)
        if hasattr(type(value), "model_fields"):
            nested = _flatten_model_attrs(value, prefix=f"{key}.")
            result.update(nested)
    return result


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
            fmt_dict = _flatten_model_attrs(entity)
            return display_field.format(**fmt_dict)
        except (KeyError, AttributeError):
            return str(entity)
    value = getattr(entity, display_field, None)
    if value is None or value == "":
        return str(entity)
    return str(value)


# ---------------------------------------------------------------------------
# Dynamic entity config builder
# ---------------------------------------------------------------------------

# Overrides for models whose key/display fields don't follow the convention
# (convention: key_field="uuid" if present else "name", display_field="name").
# key: model class, value: (key_field, display_field)
_DIFF_OVERRIDES: dict[type[CacheModel], tuple[str, str]] = {
    CloudMetadata: ("node", "node"),
    OntapDns: ("uuid", "{svm.uuid}"),
    OntapQtree: ("name", "name"),
    OntapExportPolicy: ("index", "index"),
    OntapCifsShare: ("name", "name"),
    OntapNfsService: ("svm.name", "{svm.name}"),
    OntapCifsService: ("svm.name", "{svm.name}"),
    OntapSnapmirrorRelationship: ("uuid", "{source.path}->{destination.path}"),
    OntapLicensePackageResponse: ("name", "name"),
}

# Singleton fields on CachedClusterMetadata that are diffed separately
# by _diff_cluster_info() and _diff_mediator_info().
_SINGLETON_FIELDS = frozenset({"cluster", "mediator"})

# Metadata-only fields on CachedClusterMetadata (not diffable entities).
_METADATA_FIELDS = frozenset({"cluster_name", "cached_at", "cache_version"})


def _build_entity_configs() -> dict[str, EntityConfig]:
    """Build entity configs by introspecting CachedClusterMetadata.

    Walks the model fields of ``CachedClusterMetadata`` recursively to
    discover all ``list[CacheModel]`` fields and their category paths.
    For each discovered model, looks up a matching ``TypeMapping`` in the
    model registry to confirm it is a diffable entity, then applies
    convention-based defaults or overrides for key/display fields.

    Returns:
        Mapping of category path to EntityConfig.
    """
    from pynetappfoundry.cache._metadata import CachedClusterMetadata
    from pynetappfoundry.cache._registry import model_registry

    # Build a set of model classes that have TypeMappings registered
    mapped_classes: set[type[BaseModel]] = {
        mapping.model_class for mapping in model_registry.mappings.values()
    }

    configs: dict[str, EntityConfig] = {}

    def _walk(model_cls: type[BaseModel], prefix: str) -> None:
        for field_name, field_info in model_cls.model_fields.items():
            path = f"{prefix}.{field_name}" if prefix else field_name

            # Skip metadata and singleton fields at the top level
            if not prefix and field_name in (_METADATA_FIELDS | _SINGLETON_FIELDS):
                continue

            annotation = field_info.annotation
            origin = get_origin(annotation)
            args = get_args(annotation)

            if origin is list and args:
                inner = args[0]
                if not (isinstance(inner, type) and issubclass(inner, CacheModel)):
                    continue  # list[str] or other non-model list
                if inner not in mapped_classes:
                    continue  # no TypeMapping → not a diffable entity

                # Determine key_field and display_field
                if inner in _DIFF_OVERRIDES:
                    key_field, display_field = _DIFF_OVERRIDES[inner]
                elif "uuid" in inner.model_fields:
                    key_field = "uuid"
                    display_field = "name"
                elif "name" in inner.model_fields:
                    key_field = "name"
                    display_field = "name"
                else:
                    continue  # no suitable identity key

                configs[path] = EntityConfig(
                    key_field=key_field,
                    model_class=inner,
                    display_field=display_field,
                )

            elif isinstance(annotation, type) and issubclass(annotation, BaseModel):
                # Container model (e.g., StorageInfo, NetworkInfo) — recurse
                _walk(annotation, path)

    _walk(CachedClusterMetadata, "")
    return configs


# Lazy singleton — built on first access.
_entity_configs: dict[str, EntityConfig] | None = None


def _get_entity_configs() -> dict[str, EntityConfig]:
    """Return the entity configs dict, building it on first access.

    Returns:
        Mapping of category path to EntityConfig.
    """
    global _entity_configs
    if _entity_configs is None:
        _entity_configs = _build_entity_configs()
    return _entity_configs


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
        for category, config in _get_entity_configs().items():
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
    for category, config in _get_entity_configs().items():
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

    def _resolve_key(entity: Any) -> Any:
        """Resolve a potentially dotted key_field path."""
        if "." not in key_field:
            return getattr(entity, key_field, None)
        obj = entity
        for part in key_field.split("."):
            obj = getattr(obj, part, None)
            if obj is None:
                return None
        return obj

    # Build lookup maps by key
    before_map: dict[str, Any] = {}
    for entity in before_list:
        key = _resolve_key(entity)
        if key is not None:
            before_map[key] = entity

    after_map: dict[str, Any] = {}
    for entity in after_list:
        key = _resolve_key(entity)
        if key is not None:
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

    Tracked fields are derived dynamically from OntapMediatorResponse.model_fields.

    Args:
        before: Previous snapshot (None for initial).
        after: New snapshot.

    Returns:
        List of change dictionaries.
    """
    from pynetappfoundry.models.ontap.cluster.mediators.model import OntapMediatorResponse

    changes: list[dict[str, Any]] = []
    category = "mediator"
    tracked_fields = list(OntapMediatorResponse.model_fields)

    if before is None:
        # Initial capture - record mediator if any field is populated.
        # Nested sub-models are considered populated only when they contain
        # at least one truthy leaf value.
        mediator = after.mediator
        if any(_is_populated(getattr(mediator, f)) for f in tracked_fields):
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
