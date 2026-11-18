"""SQLite cache for collected AIQUM collections (#1055, ADR-0026).

A separate database file from the ONTAP cache (``cluster_metadata.db``): AIQUM
records are stored as raw JSON per ``(instance, mapping)`` and re-parsed with
``parse_api_record`` on read.  Equality filters become
``json_extract(record, ?) = ?`` with both the path and the value bound, so no
caller text reaches the SQL string.  The ONTAP cache and its ``SCHEMA_VERSION``
are untouched (ADR-0018 scope paragraph).
"""

from __future__ import annotations

import json
import sqlite3
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import TYPE_CHECKING, Any, ClassVar

from pynetappfoundry.cache._json_records import json_path
from pynetappfoundry.db.base import SQLiteDB

if TYPE_CHECKING:
    from pynetappfoundry.cache.aiqum_collector import AiqumSnapshot
    from pynetappfoundry.core.config import Config

_COLLECTIONS = "aiqum_collections"
_RECORDS = "aiqum_records"


class AiqumCacheDB(SQLiteDB):
    """SQLite database holding collected AIQUM collections, keyed by instance.

    Args:
        db_path: Direct path to the database file, ``":memory:"`` or a
            ``file:`` URI.
        config: Configuration whose ``config_dir`` holds
            ``.cache/aiqum_cache.db`` when *db_path* is not given.

    Raises:
        ValueError: If neither *db_path* nor *config* is provided.
    """

    SCHEMA_VERSION: ClassVar[int] = 1

    def __init__(
        self,
        db_path: Path | str | None = None,
        config: Config | None = None,
    ) -> None:
        if db_path:
            self.db_path: Path | str = db_path
        elif config:
            cache_dir = config.config_dir / ".cache"
            cache_dir.mkdir(parents=True, exist_ok=True)
            self.db_path = cache_dir / "aiqum_cache.db"
        else:
            raise ValueError("Either db_path or config must be provided")

        is_uri = isinstance(self.db_path, str) and self.db_path.startswith("file:")
        self.conn = sqlite3.connect(self.db_path, uri=is_uri)
        self.conn.row_factory = sqlite3.Row
        self._init_db()

    def _create_schema(self) -> None:
        """Create the collection and record tables."""
        self.conn.execute(f"""
            CREATE TABLE {_COLLECTIONS} (
                instance TEXT NOT NULL,
                mapping TEXT NOT NULL,
                cached_at TEXT NOT NULL,
                PRIMARY KEY (instance, mapping)
            )
        """)
        self.conn.execute(f"""
            CREATE TABLE {_RECORDS} (
                _row_id INTEGER PRIMARY KEY AUTOINCREMENT,
                instance TEXT NOT NULL,
                mapping TEXT NOT NULL,
                record_key TEXT,
                record TEXT NOT NULL
            )
        """)
        self.conn.execute(f"CREATE INDEX idx_aiqum_records_map ON {_RECORDS}(instance, mapping)")
        self.conn.execute(
            f"CREATE INDEX idx_aiqum_records_key ON {_RECORDS}(instance, mapping, record_key)"
        )

    def set(self, instance: str, snapshot: AiqumSnapshot) -> None:
        """Replace *instance*'s rows for the snapshot's mappings in one transaction."""
        from pynetappfoundry.cache._registry import model_registry

        cached_at = snapshot.cached_at.isoformat()
        with self.conn:
            for mapping_name, records in snapshot.records.items():
                mapping = model_registry.get_mapping(mapping_name)
                identifier = mapping.identifier_field if mapping else None
                self.conn.execute(
                    f"DELETE FROM {_RECORDS} WHERE instance = ? AND mapping = ?",
                    (instance, mapping_name),
                )
                self.conn.executemany(
                    f"INSERT INTO {_RECORDS} (instance, mapping, record_key, record) "
                    "VALUES (?, ?, ?, ?)",
                    [
                        (
                            instance,
                            mapping_name,
                            str(rec.get(identifier)) if isinstance(identifier, str) else None,
                            json.dumps(rec, default=str),
                        )
                        for rec in records
                    ],
                )
                self.conn.execute(
                    f"INSERT INTO {_COLLECTIONS} (instance, mapping, cached_at) VALUES (?, ?, ?) "
                    "ON CONFLICT(instance, mapping) DO UPDATE SET cached_at = excluded.cached_at",
                    (instance, mapping_name, cached_at),
                )

    def query_records(
        self, instance: str, mapping: str, filters: dict[str, Any]
    ) -> list[dict[str, Any]]:
        """Return the stored records of *mapping* on *instance* matching *filters*.

        Each filter is an exact match on a dotted JSON path.  ``None`` matches a
        null or missing value and a bool is compared as an int.

        Raises:
            ValueError: If a filter value is a list or dict.
        """
        sql = f"SELECT record FROM {_RECORDS} WHERE instance = ? AND mapping = ?"
        params: list[Any] = [instance, mapping]
        for key, value in filters.items():
            if isinstance(value, (list, dict, tuple, set)):
                raise ValueError(
                    f"Cache filter {key!r}: value must be a scalar, got {type(value).__name__}"
                )
            path = json_path(key)
            if path is None:
                return []
            if value is None:
                sql += " AND json_extract(record, ?) IS NULL"
                params.append(path)
            else:
                sql += " AND json_extract(record, ?) = ?"
                params.extend([path, int(value) if isinstance(value, bool) else value])
        sql += " ORDER BY _row_id"
        return [json.loads(row["record"]) for row in self.conn.execute(sql, params)]

    def clear(self, instance: str | None = None) -> int:
        """Delete one instance's rows, or everything when *instance* is ``None``.

        Returns:
            The number of record rows deleted.
        """
        with self.conn:
            if instance is None:
                cursor = self.conn.execute(f"DELETE FROM {_RECORDS}")
                self.conn.execute(f"DELETE FROM {_COLLECTIONS}")
            else:
                cursor = self.conn.execute(
                    f"DELETE FROM {_RECORDS} WHERE instance = ?", (instance,)
                )
                self.conn.execute(f"DELETE FROM {_COLLECTIONS} WHERE instance = ?", (instance,))
        return cursor.rowcount

    def list_instances(self) -> list[str]:
        """Return the sorted names of the instances with a collected snapshot."""
        rows = self.conn.execute(f"SELECT DISTINCT instance FROM {_COLLECTIONS} ORDER BY instance")
        return [str(row["instance"]) for row in rows]

    def list_collections(self, instance: str | None = None) -> list[dict[str, str]]:
        """Return the collected ``(instance, mapping, cached_at)`` rows, sorted.

        Args:
            instance: Restrict the rows to this instance; ``None`` returns all.
        """
        sql = f"SELECT instance, mapping, cached_at FROM {_COLLECTIONS}"
        params: tuple[str, ...] = ()
        if instance is not None:
            sql += " WHERE instance = ?"
            params = (instance,)
        sql += " ORDER BY instance, mapping"
        return [
            {
                "instance": str(row["instance"]),
                "mapping": str(row["mapping"]),
                "cached_at": str(row["cached_at"]),
            }
            for row in self.conn.execute(sql, params)
        ]

    def is_collected(self, instance: str, mapping: str) -> bool:
        """Return whether *mapping* has been collected for *instance*."""
        row = self.conn.execute(
            f"SELECT 1 FROM {_COLLECTIONS} WHERE instance = ? AND mapping = ?",
            (instance, mapping),
        ).fetchone()
        return row is not None

    def is_stale(self, instance: str, ttl_days: int = 30) -> bool | None:
        """Return whether *instance*'s oldest collection is older than *ttl_days*.

        Returns ``None`` when nothing was collected for *instance*.  Age never
        affects routing; this only reports it (ADR-0026).
        """
        row = self.conn.execute(
            f"SELECT MIN(cached_at) AS oldest FROM {_COLLECTIONS} WHERE instance = ?",
            (instance,),
        ).fetchone()
        if row is None or row["oldest"] is None:
            return None
        oldest = datetime.fromisoformat(row["oldest"])
        return datetime.now(UTC) - oldest > timedelta(days=ttl_days)
