"""SQLite database for cache change history.

Stores change history separately from the main cache for data safety.
"""

from __future__ import annotations

import json
import sqlite3
from datetime import UTC, datetime
from pathlib import Path
from typing import TYPE_CHECKING, ClassVar

from pynetappfoundry.db.base import SQLiteDB

if TYPE_CHECKING:
    from pynetappfoundry.core.config import Config

# Pattern for valid cluster names: alphanumeric, underscores, hyphens
# Must start with a letter, max 128 characters
import re

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


class CacheHistoryDB(SQLiteDB):
    """SQLite database for cache change history.

    Stores change history in a separate database file from the main cache
    for data safety and isolation.
    """

    SCHEMA_VERSION: ClassVar[int] = 1
    TABLE_NAME: ClassVar[str] = "cache_changes"

    def __init__(
        self,
        db_path: Path | None = None,
        config: Config | None = None,
    ) -> None:
        """Initialize the cache history database.

        Args:
            db_path: Direct path to database file (for testing).
            config: Configuration object with config_dir path.
                   If provided, uses {config_dir}/.cache/cache_history.db.

        Raises:
            ValueError: If neither db_path nor config is provided.
        """
        if db_path:
            self.db_path = db_path
        elif config:
            cache_dir = config.config_dir / ".cache"
            cache_dir.mkdir(parents=True, exist_ok=True)
            self.db_path = cache_dir / "cache_history.db"
        else:
            raise ValueError("Either db_path or config must be provided")

        self.conn = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        self.conn.row_factory = sqlite3.Row
        self._init_db()

    def _create_schema(self) -> None:
        """Create the cache_changes table."""
        self.conn.execute(f"""
            CREATE TABLE {self.TABLE_NAME} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cluster_name TEXT NOT NULL,
                changed_at TEXT NOT NULL,
                before_json TEXT,
                after_json TEXT NOT NULL,
                summary_json TEXT NOT NULL
            )
        """)
        self.conn.execute(
            f"CREATE INDEX idx_cache_changes_cluster ON {self.TABLE_NAME}(cluster_name)"
        )
        self.conn.execute(f"CREATE INDEX idx_cache_changes_date ON {self.TABLE_NAME}(changed_at)")

    def get_latest_snapshot(self, cluster_name: str) -> dict[str, str | None] | None:
        """Get the most recent snapshot from change history.

        Args:
            cluster_name: Name of the cluster.

        Returns:
            Dict with 'after_json' and 'changed_at' if found, None otherwise.

        Raises:
            ValueError: If cluster_name is invalid.
        """
        _validate_cluster_name(cluster_name)
        cursor = self.conn.execute(
            f"""
            SELECT after_json, changed_at FROM {self.TABLE_NAME}
            WHERE cluster_name = ?
            ORDER BY id DESC
            LIMIT 1
            """,
            (cluster_name,),
        )
        row = cursor.fetchone()
        if row:
            return {"after_json": row["after_json"], "changed_at": row["changed_at"]}
        return None

    def record_change(
        self,
        cluster_name: str,
        before_json: str | None,
        after_json: str,
        summary: list[dict[str, object]],
    ) -> int:
        """Record a change event in the history.

        Args:
            cluster_name: Name of the cluster.
            before_json: JSON string of metadata before change (None for initial).
            after_json: JSON string of metadata after change.
            summary: List of change dictionaries from compute_diff.

        Returns:
            The ID of the inserted change record.

        Raises:
            ValueError: If cluster_name is invalid.
        """
        _validate_cluster_name(cluster_name)
        changed_at = datetime.now(UTC).isoformat()
        summary_json = json.dumps(summary)

        with self.conn:
            cursor = self.conn.execute(
                f"""
                INSERT INTO {self.TABLE_NAME}
                (cluster_name, changed_at, before_json, after_json, summary_json)
                VALUES (?, ?, ?, ?, ?)
                """,
                (cluster_name, changed_at, before_json, after_json, summary_json),
            )
            return cursor.lastrowid or 0

    def get_change_history(
        self,
        cluster_name: str | None = None,
        limit: int = 50,
        offset: int = 0,
        since: str | None = None,
        until: str | None = None,
    ) -> list[dict[str, object]]:
        """Get change history with optional filtering.

        Args:
            cluster_name: Filter by cluster name (None for all clusters).
            limit: Maximum number of records to return.
            offset: Number of records to skip.
            since: ISO datetime string to filter changes after this time.
            until: ISO datetime string to filter changes before this time.

        Returns:
            List of change records with id, cluster_name, changed_at,
            and summary (parsed from JSON).

        Raises:
            ValueError: If cluster_name is provided but invalid.
        """
        if cluster_name:
            _validate_cluster_name(cluster_name)

        conditions: list[str] = []
        params: list[object] = []

        if cluster_name:
            conditions.append("cluster_name = ?")
            params.append(cluster_name)
        if since:
            conditions.append("changed_at >= ?")
            params.append(since)
        if until:
            conditions.append("changed_at <= ?")
            params.append(until)

        where_clause = ""
        if conditions:
            where_clause = "WHERE " + " AND ".join(conditions)

        query = f"""
            SELECT id, cluster_name, changed_at, summary_json
            FROM {self.TABLE_NAME}
            {where_clause}
            ORDER BY id DESC
            LIMIT ? OFFSET ?
        """
        params.extend([limit, offset])

        cursor = self.conn.execute(query, params)
        results: list[dict[str, object]] = []
        for row in cursor.fetchall():
            results.append(
                {
                    "id": row["id"],
                    "cluster_name": row["cluster_name"],
                    "changed_at": row["changed_at"],
                    "summary": json.loads(row["summary_json"]),
                }
            )
        return results

    def get_change_by_id(self, change_id: int) -> dict[str, object] | None:
        """Get a specific change record by ID.

        Args:
            change_id: The ID of the change record.

        Returns:
            Dict with full change details including before_json and after_json,
            or None if not found.
        """
        cursor = self.conn.execute(
            f"""
            SELECT id, cluster_name, changed_at, before_json, after_json, summary_json
            FROM {self.TABLE_NAME}
            WHERE id = ?
            """,
            (change_id,),
        )
        row = cursor.fetchone()
        if row:
            return {
                "id": row["id"],
                "cluster_name": row["cluster_name"],
                "changed_at": row["changed_at"],
                "before_json": row["before_json"],
                "after_json": row["after_json"],
                "summary": json.loads(row["summary_json"]),
            }
        return None

    def get_history_count(self, cluster_name: str | None = None) -> int:
        """Get total count of change history records.

        Args:
            cluster_name: Filter by cluster name (None for all clusters).

        Returns:
            Total number of change records.

        Raises:
            ValueError: If cluster_name is provided but invalid.
        """
        if cluster_name:
            _validate_cluster_name(cluster_name)
            cursor = self.conn.execute(
                f"SELECT COUNT(*) FROM {self.TABLE_NAME} WHERE cluster_name = ?",
                (cluster_name,),
            )
        else:
            cursor = self.conn.execute(f"SELECT COUNT(*) FROM {self.TABLE_NAME}")
        result = cursor.fetchone()[0]
        return int(result)

    def get_snapshot_at_date(
        self,
        cluster_name: str,
        target_date: str,
    ) -> dict[str, object] | None:
        """Get the cluster snapshot as it was on or before a specific date.

        Returns the most recent snapshot recorded on or before the target date.

        Args:
            cluster_name: Name of the cluster.
            target_date: ISO datetime string (e.g., "2024-01-15" or "2024-01-15T10:30:00").

        Returns:
            Dict with id, cluster_name, changed_at, and after_json if found,
            or None if no snapshot exists on or before that date.

        Raises:
            ValueError: If cluster_name is invalid.
        """
        _validate_cluster_name(cluster_name)
        cursor = self.conn.execute(
            f"""
            SELECT id, cluster_name, changed_at, after_json
            FROM {self.TABLE_NAME}
            WHERE cluster_name = ? AND changed_at <= ?
            ORDER BY changed_at DESC
            LIMIT 1
            """,
            (cluster_name, target_date),
        )
        row = cursor.fetchone()
        if row:
            return {
                "id": row["id"],
                "cluster_name": row["cluster_name"],
                "changed_at": row["changed_at"],
                "after_json": row["after_json"],
            }
        return None
