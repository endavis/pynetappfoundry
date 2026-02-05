"""SQLite database operations for cluster metadata cache."""

from __future__ import annotations

import json
import re
import sqlite3
from datetime import UTC, datetime
from pathlib import Path
from typing import TYPE_CHECKING, ClassVar

from pynetappfoundry.cache.models import CachedClusterMetadata
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


class ClusterMetadataDB(SQLiteDB):
    """SQLite database for caching cluster metadata.

    Stores serialized CachedClusterMetadata objects in a single table
    with cluster_name as the primary key.

    Note: Change history is stored in a separate database (CacheHistoryDB)
    for data safety and isolation.
    """

    SCHEMA_VERSION: ClassVar[int] = 1
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
        self._migrate_old_schema_info()
        self._init_db()

    def _migrate_old_schema_info(self) -> None:
        """Migrate from old schema_info table to _schema_version if needed."""
        cursor = self.conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='schema_info'"
        )
        if cursor.fetchone() is not None:
            # Old schema_info exists - drop it (we'll use _schema_version now)
            self.conn.execute("DROP TABLE schema_info")

    def _create_schema(self) -> None:
        """Create the cluster_metadata table."""
        self.conn.execute(f"""
            CREATE TABLE {self.TABLE_NAME} (
                cluster_name TEXT PRIMARY KEY,
                cached_at TEXT NOT NULL,
                cache_version TEXT NOT NULL,
                metadata_json TEXT NOT NULL
            )
        """)

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
            f"SELECT metadata_json FROM {self.TABLE_NAME} WHERE cluster_name = ?",
            (cluster_name,),
        )
        row = cursor.fetchone()
        if row:
            data = json.loads(row["metadata_json"])
            return CachedClusterMetadata.model_validate(data)
        return None

    def set(self, cluster_name: str, metadata: CachedClusterMetadata) -> None:
        """Store or update cached metadata for a cluster.

        Args:
            cluster_name: Name of the cluster.
            metadata: Metadata to cache.

        Raises:
            ValueError: If cluster_name is invalid.
        """
        _validate_cluster_name(cluster_name)
        metadata_json = metadata.model_dump_json()
        with self.conn:
            self.conn.execute(
                f"""
                INSERT OR REPLACE INTO {self.TABLE_NAME}
                (cluster_name, cached_at, cache_version, metadata_json)
                VALUES (?, ?, ?, ?)
            """,
                (
                    cluster_name,
                    metadata.cached_at.isoformat(),
                    metadata.cache_version,
                    metadata_json,
                ),
            )

    def clear(self, cluster_name: str | None = None) -> int:
        """Clear cached metadata.

        Args:
            cluster_name: If provided, clear only this cluster.
                         If None, clear all cached data.

        Returns:
            Number of rows deleted.

        Raises:
            ValueError: If cluster_name is provided but invalid.
        """
        with self.conn:
            if cluster_name:
                _validate_cluster_name(cluster_name)
                cursor = self.conn.execute(
                    f"DELETE FROM {self.TABLE_NAME} WHERE cluster_name = ?",
                    (cluster_name,),
                )
            else:
                cursor = self.conn.execute(f"DELETE FROM {self.TABLE_NAME}")
            return cursor.rowcount

    def is_stale(self, cluster_name: str, ttl_days: int = 30) -> bool | None:
        """Check if cached data is stale.

        Args:
            cluster_name: Name of the cluster.
            ttl_days: Number of days before cache is considered stale.

        Returns:
            True if stale, False if fresh, None if not cached.

        Raises:
            ValueError: If cluster_name is invalid.
        """
        metadata = self.get(cluster_name)
        if metadata is None:
            return None
        return metadata.is_stale(ttl_days)

    def list_clusters(self) -> list[dict[str, str]]:
        """List all cached clusters with cache info.

        Returns:
            List of dicts with cluster_name, cached_at, cache_version.
        """
        cursor = self.conn.execute(
            f"SELECT cluster_name, cached_at, cache_version FROM {self.TABLE_NAME}"
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
            # Handle both ISO format with and without timezone
            if cached_at_str.endswith("Z"):
                cached_at_str = cached_at_str[:-1] + "+00:00"
            if "+" not in cached_at_str and "-" not in cached_at_str[-6:]:
                # No timezone info, assume UTC
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
