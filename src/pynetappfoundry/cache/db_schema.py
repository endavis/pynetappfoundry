"""DDL generation for per-model SQL tables in the cluster metadata cache.

Walks CachedClusterMetadata.model_fields to discover storable models
and generates CREATE TABLE statements from their Pydantic field definitions.
"""

from __future__ import annotations

import types
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Union, get_args, get_origin

from pydantic import BaseModel

from pynetappfoundry.cache._base import OntapUUID


@dataclass(frozen=True)
class TableSpec:
    """Describes how a Pydantic model maps to a SQL table.

    Attributes:
        table_name: SQL table name (lowercased model class name).
        model_class: The Pydantic model class.
        metadata_path: Dot-path from CachedClusterMetadata root
                       (e.g. ``"storage.volumes"``).
        is_list: True for ``list[Model]`` fields, False for singletons.
        has_uuid: True if the model has a ``uuid`` field.
    """

    table_name: str
    model_class: type[BaseModel]
    metadata_path: str
    is_list: bool
    has_uuid: bool


# Fields on CachedClusterMetadata that are envelope/metadata, not data.
_SKIP_FIELDS = frozenset({"cluster_name", "cached_at", "cache_version"})


def _is_list_of_models(annotation: Any) -> type[BaseModel] | None:
    """Return the item model class if annotation is ``list[SomeModel]``, else None."""
    origin = get_origin(annotation)
    if origin is list:
        args = get_args(annotation)
        if args and isinstance(args[0], type) and issubclass(args[0], BaseModel):
            return args[0]
    return None


def _is_model_type(annotation: Any) -> type[BaseModel] | None:
    """Return the model class if annotation is a BaseModel subclass, else None."""
    if isinstance(annotation, type) and issubclass(annotation, BaseModel):
        return annotation
    return None


def _has_list_model_fields(model_class: type[BaseModel]) -> bool:
    """Check if a model has any list[BaseModel] fields (i.e., is a container)."""
    for field_info in model_class.model_fields.values():
        if _is_list_of_models(field_info.annotation) is not None:
            return True
    return False


def build_table_registry() -> dict[str, TableSpec]:
    """Walk CachedClusterMetadata fields and build a registry of table specs.

    Returns:
        Dict mapping ``metadata_path`` to ``TableSpec``.
    """
    # Deferred import to avoid circular references at module level.
    from pynetappfoundry.cache._metadata import CachedClusterMetadata

    registry: dict[str, TableSpec] = {}

    for field_name, field_info in CachedClusterMetadata.model_fields.items():
        if field_name in _SKIP_FIELDS:
            continue

        annotation = field_info.annotation

        # Case 1: list[SomeModel] at top level (e.g. nodes, cloud, license_packages)
        item_cls = _is_list_of_models(annotation)
        if item_cls is not None:
            _register_model(registry, field_name, item_cls, is_list=True)
            continue

        # Case 2: SomeModel singleton at top level (e.g. cluster, mediator)
        model_cls = _is_model_type(annotation)
        if model_cls is not None:
            # If the model has list[BaseModel] sub-fields, it's a container.
            if _has_list_model_fields(model_cls):
                _walk_container(registry, field_name, model_cls)
            else:
                # Pure singleton (e.g. ClusterInfo, OntapMediatorResponse)
                _register_model(registry, field_name, model_cls, is_list=False)

    return registry


def _register_model(
    registry: dict[str, TableSpec],
    metadata_path: str,
    model_class: type[BaseModel],
    *,
    is_list: bool,
) -> None:
    """Add a TableSpec for a model to the registry."""
    table_name = model_class.__name__.lower()
    has_uuid = "uuid" in model_class.model_fields
    registry[metadata_path] = TableSpec(
        table_name=table_name,
        model_class=model_class,
        metadata_path=metadata_path,
        is_list=is_list,
        has_uuid=has_uuid,
    )


def _walk_container(
    registry: dict[str, TableSpec],
    prefix: str,
    container_class: type[BaseModel],
) -> None:
    """Walk a container model's fields and register sub-models.

    Also registers the container as a singleton if it has non-list scalar fields
    beyond what its child lists cover (e.g. ``NetworkInfo.ipspaces``).
    """
    has_non_list_scalar = False

    for field_name, field_info in container_class.model_fields.items():
        annotation = field_info.annotation
        path = f"{prefix}.{field_name}"

        item_cls = _is_list_of_models(annotation)
        if item_cls is not None:
            _register_model(registry, path, item_cls, is_list=True)
            continue

        model_cls = _is_model_type(annotation)
        if model_cls is not None:
            if _has_list_model_fields(model_cls):
                _walk_container(registry, path, model_cls)
            else:
                _register_model(registry, path, model_cls, is_list=False)
            continue

        # Scalar or list[str] etc. — part of the container itself
        has_non_list_scalar = True

    # If the container has scalar fields (like NetworkInfo.ipspaces: list[str]),
    # register the container itself as a singleton so those fields are stored.
    if has_non_list_scalar:
        # Store the container model for its scalar-only fields.
        _register_model(registry, prefix, container_class, is_list=False)


# ---------------------------------------------------------------------------
# Type mapping
# ---------------------------------------------------------------------------


def _unwrap_annotation(annotation: Any) -> Any:
    """Unwrap Annotated, Optional, etc. to the core Python type."""
    origin = get_origin(annotation)

    # Annotated[str, ...] → str
    if origin is not None and hasattr(annotation, "__metadata__"):
        args = get_args(annotation)
        return _unwrap_annotation(args[0]) if args else annotation

    # Optional[X] → X  (Union[X, None])
    if origin is Union or origin is types.UnionType:
        args = tuple(a for a in get_args(annotation) if a is not type(None))
        if len(args) == 1:
            return _unwrap_annotation(args[0])

    return annotation


def _python_type_to_sql(annotation: Any) -> str:
    """Map a Python/Pydantic type annotation to a SQL column type.

    Returns:
        SQL type string: TEXT, INTEGER, REAL, or TEXT (for JSON).
    """
    core = _unwrap_annotation(annotation)

    if core is str or core is OntapUUID:
        return "TEXT"
    if core is int:
        return "INTEGER"
    if core is bool:
        return "INTEGER"
    if core is float:
        return "REAL"
    if core is datetime:
        return "TEXT"

    # list[...], dict[...], or any complex type → JSON as TEXT
    origin = get_origin(core)
    if origin is list or origin is dict:
        return "TEXT"

    # BaseModel sub-fields → JSON as TEXT
    if isinstance(core, type) and issubclass(core, BaseModel):
        return "TEXT"

    # Fallback: TEXT
    return "TEXT"


def _is_json_column(annotation: Any) -> bool:
    """Return True if the column stores JSON (list, dict, or BaseModel)."""
    core = _unwrap_annotation(annotation)
    origin = get_origin(core)
    if origin is list or origin is dict:
        return True
    return isinstance(core, type) and issubclass(core, BaseModel)


# ---------------------------------------------------------------------------
# DDL generation
# ---------------------------------------------------------------------------


def generate_table_ddl(table_name: str, model_class: type[BaseModel]) -> str:
    """Generate a CREATE TABLE statement for a Pydantic model.

    Every table uses ``_row_id INTEGER PRIMARY KEY AUTOINCREMENT`` to avoid
    collisions when UUID fields are empty.

    Args:
        table_name: SQL table name.
        model_class: The Pydantic model to generate DDL from.

    Returns:
        Complete CREATE TABLE SQL string.
    """
    lines: list[str] = []
    lines.append(f"CREATE TABLE {table_name} (")

    # cluster_name column — skip if the model already defines one
    model_has_cluster_name = "cluster_name" in model_class.model_fields
    if not model_has_cluster_name:
        lines.append("    cluster_name TEXT NOT NULL,")

    # Always use _row_id as PK to avoid empty-uuid collisions
    lines.append("    _row_id INTEGER PRIMARY KEY AUTOINCREMENT,")

    # Model fields (quote names to avoid SQLite reserved word conflicts)
    for field_name, field_info in model_class.model_fields.items():
        sql_type = _python_type_to_sql(field_info.annotation)
        quoted = f'"{field_name}"'
        if field_name == "cluster_name":
            lines.append(f"    {quoted} {sql_type} NOT NULL,")
        else:
            lines.append(f"    {quoted} {sql_type},")

    # Extra JSON column for extra="allow" fields
    lines.append("    _extra_json TEXT DEFAULT NULL")

    ddl = "\n".join(lines) + "\n)"
    return ddl


def generate_cluster_name_index_ddl(table_name: str) -> str:
    """Generate CREATE INDEX for cluster_name."""
    return f'CREATE INDEX IF NOT EXISTS idx_{table_name}_cluster ON {table_name} ("cluster_name")'


def generate_uuid_column_index_ddl(table_name: str) -> str:
    """Generate CREATE INDEX for (cluster_name, uuid) on UUID-bearing tables."""
    return (
        f'CREATE INDEX IF NOT EXISTS idx_{table_name}_uuid ON {table_name} ("cluster_name", "uuid")'
    )


# ---------------------------------------------------------------------------
# Fixed table DDL
# ---------------------------------------------------------------------------

UUID_INDEX_DDL = """\
CREATE TABLE _uuid_index (
    cluster_name TEXT NOT NULL,
    uuid TEXT NOT NULL,
    table_name TEXT NOT NULL,
    PRIMARY KEY (cluster_name, uuid)
)"""

ENVELOPE_DDL = """\
CREATE TABLE cluster_metadata (
    cluster_name TEXT PRIMARY KEY,
    cached_at TEXT NOT NULL,
    cache_version TEXT NOT NULL
)"""


# ---------------------------------------------------------------------------
# Module-level registry (built once on first import)
# ---------------------------------------------------------------------------

TABLE_REGISTRY: dict[str, TableSpec] = {}


def _ensure_registry() -> dict[str, TableSpec]:
    """Lazily build and cache the table registry."""
    global TABLE_REGISTRY
    if not TABLE_REGISTRY:
        TABLE_REGISTRY = build_table_registry()
    return TABLE_REGISTRY
