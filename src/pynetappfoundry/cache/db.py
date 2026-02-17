"""SQLite database operations for cluster metadata cache.

Schema v2 stores each Pydantic model in its own SQL table instead of a
single JSON blob.  The public API (``get``/``set``/``clear``/etc.) is
preserved so callers (collectors, query, inspect, diff, refresh) work
unchanged.
"""

from __future__ import annotations

import json
import re
import sqlite3
from datetime import UTC, datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any, ClassVar

from pydantic import BaseModel

from pynetappfoundry.cache._metadata import CachedClusterMetadata
from pynetappfoundry.cache.db_schema import (
    ENVELOPE_DDL,
    UUID_INDEX_DDL,
    _ensure_registry,
    _is_json_column,
    generate_cluster_name_index_ddl,
    generate_table_ddl,
    generate_uuid_column_index_ddl,
)
from pynetappfoundry.db.base import SQLiteDB

if TYPE_CHECKING:
    from pynetappfoundry.core.config import Config

# Pattern for valid cluster names: alphanumeric, underscores, hyphens
# Must start with a letter, max 128 characters
_CLUSTER_NAME_PATTERN = re.compile(r"^[a-zA-Z][a-zA-Z0-9_\-]{0,127}$")


def _validate_cluster_name(cluster_name: str) -> None:
    """Validate a cluster name to prevent SQL injection.

    Args:
        cluster_name: The cluster name to validate.

    Raises:
        ValueError: If the cluster name is invalid.
    """
    if not _CLUSTER_NAME_PATTERN.match(cluster_name):
        raise ValueError(
            f"Invalid cluster name: {cluster_name!r}. "
            "Cluster names must start with a letter, "
            "contain only alphanumeric characters, underscores, or hyphens, "
            "and be at most 128 characters."
        )


# ---------------------------------------------------------------------------
# Row conversion helpers
# ---------------------------------------------------------------------------


def _model_to_row(
    model_instance: BaseModel,
    model_class: type[BaseModel],
) -> dict[str, Any]:
    """Convert a Pydantic model instance to a dict suitable for SQL INSERT.

    Scalar fields are passed through.  ``list``/``dict``/sub-model fields
    are serialised to JSON strings.  Any extra fields (from ``extra="allow"``)
    are collected into the ``_extra_json`` column.
    """
    row: dict[str, Any] = {}
    known_fields = set(model_class.model_fields)

    for field_name, field_info in model_class.model_fields.items():
        value = getattr(model_instance, field_name)
        if _is_json_column(field_info.annotation):
            # Serialize list/dict/sub-model to JSON
            if isinstance(value, BaseModel):
                row[field_name] = value.model_dump_json()
            elif isinstance(value, list):
                row[field_name] = json.dumps(
                    [item.model_dump() if isinstance(item, BaseModel) else item for item in value]
                )
            elif isinstance(value, dict):
                row[field_name] = json.dumps(value)
            else:
                row[field_name] = json.dumps(value)
        elif isinstance(value, datetime):
            row[field_name] = value.isoformat()
        elif isinstance(value, bool):
            row[field_name] = int(value)
        else:
            row[field_name] = value

    # Collect extra fields
    extra_data: dict[str, Any] = {}
    for attr_name in model_instance.model_fields_set | set(model_instance.__pydantic_extra__ or {}):
        if attr_name not in known_fields:
            extra_data[attr_name] = getattr(model_instance, attr_name)

    row["_extra_json"] = json.dumps(extra_data) if extra_data else None
    return row


def _row_to_model(
    row: dict[str, Any],
    model_class: type[BaseModel],
) -> BaseModel:
    """Convert a SQL row dict back to a Pydantic model instance.

    Reverses ``_model_to_row``: JSON columns are parsed, booleans are
    coerced from int, and extra fields from ``_extra_json`` are merged.
    """
    kwargs: dict[str, Any] = {}

    for field_name, field_info in model_class.model_fields.items():
        value = row.get(field_name)
        if value is None:
            continue
        if _is_json_column(field_info.annotation):
            kwargs[field_name] = json.loads(value) if isinstance(value, str) else value
        else:
            kwargs[field_name] = value

    # Merge extra fields
    extra_json = row.get("_extra_json")
    if extra_json:
        extra = json.loads(extra_json) if isinstance(extra_json, str) else extra_json
        kwargs.update(extra)

    return model_class.model_validate(kwargs)


# ---------------------------------------------------------------------------
# Metadata path helpers
# ---------------------------------------------------------------------------


def _get_by_path(obj: Any, path: str) -> Any:
    """Traverse a dot-path on an object (e.g. ``"storage.volumes"``)."""
    for part in path.split("."):
        obj = getattr(obj, part)
    return obj


def _set_by_path(target: dict[str, Any], path: str, value: Any) -> None:
    """Set a value in a nested dict via dot-path, creating intermediate dicts."""
    parts = path.split(".")
    for part in parts[:-1]:
        target = target.setdefault(part, {})
    target[parts[-1]] = value


# ---------------------------------------------------------------------------
# ClusterMetadataDB
# ---------------------------------------------------------------------------


class ClusterMetadataDB(SQLiteDB):
    """SQLite database for caching cluster metadata.

    Schema v2 decomposes CachedClusterMetadata into per-model SQL tables.
    The public ``get``/``set``/``clear`` API is preserved.

    Note: Change history is stored in a separate database (CacheHistoryDB)
    for data safety and isolation.
    """

    SCHEMA_VERSION: ClassVar[int] = 2
    TABLE_NAME: ClassVar[str] = "cluster_metadata"

    def __init__(
        self,
        db_path: Path | None = None,
        config: Config | None = None,
    ) -> None:
        """Initialize the metadata cache database.

        Args:
            db_path: Direct path to database file (for testing).
            config: Configuration object with data_dir path.
                   If provided, uses {data_dir}/cache/cluster_metadata.db.

        Raises:
            ValueError: If neither db_path nor config is provided.
        """
        if db_path:
            self.db_path = db_path
        elif config:
            cache_dir = config.config_dir / ".cache"
            cache_dir.mkdir(parents=True, exist_ok=True)
            self.db_path = cache_dir / "cluster_metadata.db"
        else:
            raise ValueError("Either db_path or config must be provided")

        self.conn = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        self.conn.row_factory = sqlite3.Row
        self._registry = _ensure_registry()
        self._migrate_old_schema_info()
        self._init_db()

    def _migrate_old_schema_info(self) -> None:
        """Migrate from old schema_info table to _schema_version if needed."""
        cursor = self.conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='schema_info'"
        )
        if cursor.fetchone() is not None:
            self.conn.execute("DROP TABLE schema_info")

    # ------------------------------------------------------------------
    # Schema creation (new DB)
    # ------------------------------------------------------------------

    def _create_schema(self) -> None:
        """Create all tables for a fresh v2 database."""
        # Envelope table
        self.conn.execute(ENVELOPE_DDL)

        # Per-model tables
        for spec in self._registry.values():
            ddl = generate_table_ddl(spec.table_name, spec.model_class)
            self.conn.execute(ddl)
            self.conn.execute(generate_cluster_name_index_ddl(spec.table_name))
            if spec.has_uuid:
                self.conn.execute(generate_uuid_column_index_ddl(spec.table_name))

        # UUID index table
        self.conn.execute(UUID_INDEX_DDL)

    # ------------------------------------------------------------------
    # Migration v1 → v2
    # ------------------------------------------------------------------

    def _upgrade_to_v2(self) -> None:
        """Migrate from v1 (JSON blob) to v2 (per-model tables)."""
        # 1. Read all v1 data
        cursor = self.conn.execute(
            "SELECT cluster_name, cached_at, cache_version, metadata_json FROM cluster_metadata"
        )
        v1_rows = [dict(row) for row in cursor.fetchall()]

        # 2. Create new model tables + uuid index
        for spec in self._registry.values():
            ddl = generate_table_ddl(spec.table_name, spec.model_class)
            self.conn.execute(ddl)
            self.conn.execute(generate_cluster_name_index_ddl(spec.table_name))
            if spec.has_uuid:
                self.conn.execute(generate_uuid_column_index_ddl(spec.table_name))
        self.conn.execute(UUID_INDEX_DDL)

        # 3. Migrate each cluster's data
        for v1_row in v1_rows:
            cluster_name = v1_row["cluster_name"]
            metadata = CachedClusterMetadata.model_validate(json.loads(v1_row["metadata_json"]))
            self._insert_model_data(cluster_name, metadata)
            self._populate_uuid_index(cluster_name, metadata)

        # 4. Recreate envelope table without metadata_json
        #    (SQLite doesn't support DROP COLUMN before 3.35)
        self.conn.execute("ALTER TABLE cluster_metadata RENAME TO _old_cluster_metadata")
        self.conn.execute(ENVELOPE_DDL)
        self.conn.execute(
            "INSERT INTO cluster_metadata (cluster_name, cached_at, cache_version) "
            "SELECT cluster_name, cached_at, cache_version FROM _old_cluster_metadata"
        )
        self.conn.execute("DROP TABLE _old_cluster_metadata")

    # ------------------------------------------------------------------
    # Internal: decompose metadata into tables
    # ------------------------------------------------------------------

    def _insert_model_data(
        self,
        cluster_name: str,
        metadata: CachedClusterMetadata,
    ) -> None:
        """Walk TABLE_REGISTRY and insert model data into per-model tables."""
        for path, spec in self._registry.items():
            data = _get_by_path(metadata, path)

            if spec.is_list:
                if not data:
                    continue
                rows = [_model_to_row(item, spec.model_class) for item in data]
                for row in rows:
                    row["cluster_name"] = cluster_name
                self._bulk_insert(spec.table_name, rows)
            else:
                # Singleton
                row = _model_to_row(data, spec.model_class)
                row["cluster_name"] = cluster_name
                self._bulk_insert(spec.table_name, [row])

    def _bulk_insert(self, table_name: str, rows: list[dict[str, Any]]) -> None:
        """Insert multiple rows into a table using executemany."""
        if not rows:
            return
        columns = list(rows[0].keys())
        placeholders = ", ".join("?" for _ in columns)
        col_names = ", ".join(f'"{c}"' for c in columns)
        sql = f"INSERT INTO {table_name} ({col_names}) VALUES ({placeholders})"
        values = [tuple(row[c] for c in columns) for row in rows]
        self.conn.executemany(sql, values)

    def _populate_uuid_index(
        self,
        cluster_name: str,
        metadata: CachedClusterMetadata,
    ) -> None:
        """Populate the _uuid_index table from a CachedClusterMetadata."""
        rows: list[tuple[str, str, str]] = []
        for path, spec in self._registry.items():
            if not spec.has_uuid:
                continue
            data = _get_by_path(metadata, path)
            items = data if spec.is_list else [data]
            for item in items:
                uuid_val = getattr(item, "uuid", "")
                if uuid_val:
                    rows.append((cluster_name, uuid_val, spec.table_name))
        if rows:
            self.conn.executemany(
                "INSERT OR REPLACE INTO _uuid_index (cluster_name, uuid, table_name) "
                "VALUES (?, ?, ?)",
                rows,
            )

    # ------------------------------------------------------------------
    # Internal: reconstruct metadata from tables
    # ------------------------------------------------------------------

    def _reconstruct_metadata(
        self,
        cluster_name: str,
        envelope: dict[str, str],
    ) -> CachedClusterMetadata:
        """Read all model tables and rebuild a CachedClusterMetadata."""
        root_kwargs: dict[str, Any] = {
            "cluster_name": cluster_name,
            "cached_at": envelope["cached_at"],
            "cache_version": envelope["cache_version"],
        }

        for path, spec in self._registry.items():
            cursor = self.conn.execute(
                f"SELECT * FROM {spec.table_name} WHERE cluster_name = ?",
                (cluster_name,),
            )
            rows = [dict(r) for r in cursor.fetchall()]

            # Determine which columns to strip from the row before model construction.
            # Always strip _row_id.  Strip cluster_name only if the model doesn't
            # have its own cluster_name field (e.g. ClusterInfo keeps it).
            model_has_cluster_name = "cluster_name" in spec.model_class.model_fields
            strip_keys = {"_row_id"}
            if not model_has_cluster_name:
                strip_keys.add("cluster_name")

            if spec.is_list:
                models = [
                    _row_to_model(
                        {k: v for k, v in row.items() if k not in strip_keys},
                        spec.model_class,
                    )
                    for row in rows
                ]
                _set_by_path(root_kwargs, path, models)
            else:
                if rows:
                    row = rows[0]
                    model = _row_to_model(
                        {k: v for k, v in row.items() if k not in strip_keys},
                        spec.model_class,
                    )
                    _set_by_path(root_kwargs, path, model)

        return CachedClusterMetadata.model_validate(root_kwargs)

    # ------------------------------------------------------------------
    # Internal: delete model data for a cluster
    # ------------------------------------------------------------------

    def _delete_model_data(self, cluster_name: str) -> None:
        """Delete all model rows for a cluster from every table."""
        for spec in self._registry.values():
            self.conn.execute(
                f"DELETE FROM {spec.table_name} WHERE cluster_name = ?",
                (cluster_name,),
            )
        self.conn.execute(
            "DELETE FROM _uuid_index WHERE cluster_name = ?",
            (cluster_name,),
        )

    def _delete_all_model_data(self) -> None:
        """Delete all model rows from every table."""
        for spec in self._registry.values():
            self.conn.execute(f"DELETE FROM {spec.table_name}")
        self.conn.execute("DELETE FROM _uuid_index")

    # ------------------------------------------------------------------
    # Public API — preserved interface
    # ------------------------------------------------------------------

    def get(self, cluster_name: str) -> CachedClusterMetadata | None:
        """Retrieve cached metadata for a cluster.

        Args:
            cluster_name: Name of the cluster.

        Returns:
            CachedClusterMetadata if found, None otherwise.

        Raises:
            ValueError: If cluster_name is invalid.
        """
        _validate_cluster_name(cluster_name)
        cursor = self.conn.execute(
            "SELECT cluster_name, cached_at, cache_version "
            "FROM cluster_metadata WHERE cluster_name = ?",
            (cluster_name,),
        )
        row = cursor.fetchone()
        if row is None:
            return None
        return self._reconstruct_metadata(cluster_name, dict(row))

    def set(self, cluster_name: str, metadata: CachedClusterMetadata) -> None:
        """Store or update cached metadata for a cluster.

        Decomposes the metadata into per-model tables within a single
        transaction.

        Args:
            cluster_name: Name of the cluster.
            metadata: Metadata to cache.

        Raises:
            ValueError: If cluster_name is invalid.
        """
        _validate_cluster_name(cluster_name)
        with self.conn:
            # Upsert envelope
            self.conn.execute(
                "INSERT OR REPLACE INTO cluster_metadata "
                "(cluster_name, cached_at, cache_version) VALUES (?, ?, ?)",
                (
                    cluster_name,
                    metadata.cached_at.isoformat(),
                    metadata.cache_version,
                ),
            )
            # Delete old model rows then re-insert
            self._delete_model_data(cluster_name)
            self._insert_model_data(cluster_name, metadata)
            self._populate_uuid_index(cluster_name, metadata)

    def clear(self, cluster_name: str | None = None) -> int:
        """Clear cached metadata.

        Args:
            cluster_name: If provided, clear only this cluster.
                         If None, clear all cached data.

        Returns:
            Number of envelope rows deleted.

        Raises:
            ValueError: If cluster_name is provided but invalid.
        """
        with self.conn:
            if cluster_name:
                _validate_cluster_name(cluster_name)
                self._delete_model_data(cluster_name)
                cursor = self.conn.execute(
                    "DELETE FROM cluster_metadata WHERE cluster_name = ?",
                    (cluster_name,),
                )
            else:
                self._delete_all_model_data()
                cursor = self.conn.execute("DELETE FROM cluster_metadata")
            return cursor.rowcount

    def is_stale(self, cluster_name: str, ttl_days: int = 30) -> bool | None:
        """Check if cached data is stale (optimized — envelope only).

        Args:
            cluster_name: Name of the cluster.
            ttl_days: Number of days before cache is considered stale.

        Returns:
            True if stale, False if fresh, None if not cached.

        Raises:
            ValueError: If cluster_name is invalid.
        """
        _validate_cluster_name(cluster_name)
        cursor = self.conn.execute(
            "SELECT cached_at FROM cluster_metadata WHERE cluster_name = ?",
            (cluster_name,),
        )
        row = cursor.fetchone()
        if row is None:
            return None

        cached_at_str = row["cached_at"]
        if cached_at_str.endswith("Z"):
            cached_at_str = cached_at_str[:-1] + "+00:00"
        if "+" not in cached_at_str and "-" not in cached_at_str[-6:]:
            cached_at = datetime.fromisoformat(cached_at_str).replace(tzinfo=UTC)
        else:
            cached_at = datetime.fromisoformat(cached_at_str)

        age = datetime.now(UTC) - cached_at
        return age.days > ttl_days

    def list_clusters(self) -> list[dict[str, str]]:
        """List all cached clusters with cache info.

        Returns:
            List of dicts with cluster_name, cached_at, cache_version.
        """
        cursor = self.conn.execute(
            "SELECT cluster_name, cached_at, cache_version FROM cluster_metadata"
        )
        return [dict(row) for row in cursor.fetchall()]

    def get_status(self, ttl_days: int = 30) -> list[dict[str, str | int | bool]]:
        """Get cache status for all clusters.

        Args:
            ttl_days: Number of days before cache is considered stale.

        Returns:
            List of dicts with cluster info and staleness status.
        """
        clusters = self.list_clusters()
        result: list[dict[str, str | int | bool]] = []
        for cluster in clusters:
            cached_at_str = cluster["cached_at"]
            if cached_at_str.endswith("Z"):
                cached_at_str = cached_at_str[:-1] + "+00:00"
            if "+" not in cached_at_str and "-" not in cached_at_str[-6:]:
                cached_at = datetime.fromisoformat(cached_at_str).replace(tzinfo=UTC)
            else:
                cached_at = datetime.fromisoformat(cached_at_str)
            age = datetime.now(UTC) - cached_at
            result.append(
                {
                    "cluster_name": cluster["cluster_name"],
                    "cached_at": cluster["cached_at"],
                    "cache_version": cluster["cache_version"],
                    "age_days": age.days,
                    "is_stale": age.days > ttl_days,
                }
            )
        return result

    # ------------------------------------------------------------------
    # New public methods
    # ------------------------------------------------------------------

    def query_model(
        self,
        cluster_name: str,
        model_name: str,
        **filters: Any,
    ) -> list[BaseModel]:
        """Query a specific model table with optional equality filters.

        Args:
            cluster_name: Name of the cluster.
            model_name: The metadata_path key (e.g. ``"storage.volumes"``).
            **filters: Field-name=value equality filters.

        Returns:
            List of deserialized model instances.

        Raises:
            ValueError: If cluster_name is invalid or model_name not found.
        """
        _validate_cluster_name(cluster_name)
        spec = self._registry.get(model_name)
        if spec is None:
            raise ValueError(f"Unknown model name: {model_name!r}")

        conditions = ['"cluster_name" = ?']
        params: list[Any] = [cluster_name]
        for col, val in filters.items():
            if col not in spec.model_class.model_fields:
                raise ValueError(f"Unknown field {col!r} on {spec.model_class.__name__}")
            conditions.append(f'"{col}" = ?')
            params.append(val)

        sql = f"SELECT * FROM {spec.table_name} WHERE {' AND '.join(conditions)}"
        cursor = self.conn.execute(sql, params)
        rows = [dict(r) for r in cursor.fetchall()]

        return [
            _row_to_model(
                {k: v for k, v in row.items() if k not in ("cluster_name", "_row_id")},
                spec.model_class,
            )
            for row in rows
        ]

    def export_json(self, cluster_name: str) -> str | None:
        """Export cluster metadata as a JSON string.

        Args:
            cluster_name: Name of the cluster.

        Returns:
            JSON string or None if cluster not found.
        """
        metadata = self.get(cluster_name)
        if metadata is None:
            return None
        return metadata.model_dump_json()

    def import_json(self, cluster_name: str, json_str: str) -> None:
        """Import cluster metadata from a JSON string.

        Args:
            cluster_name: Name of the cluster.
            json_str: JSON string of CachedClusterMetadata.
        """
        metadata = CachedClusterMetadata.model_validate_json(json_str)
        self.set(cluster_name, metadata)
