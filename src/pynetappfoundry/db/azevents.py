"""Azure maintenance events database."""

from __future__ import annotations

import sqlite3
from datetime import datetime
from typing import TYPE_CHECKING, Any

from pynetappfoundry.db.base import adapt_datetime, convert_datetime

if TYPE_CHECKING:
    from pynetappfoundry.core.config import Config

# Register converters for this module
sqlite3.register_adapter(datetime, adapt_datetime)
sqlite3.register_converter("az_maint_not_before", convert_datetime)
sqlite3.register_converter("az_maint_scheduled", convert_datetime)
sqlite3.register_converter("az_maint_started", convert_datetime)
sqlite3.register_converter("az_maint_complete", convert_datetime)
sqlite3.register_converter("node_takeover_complete", convert_datetime)
sqlite3.register_converter("node_reboot_starts", convert_datetime)
sqlite3.register_converter("node_reboot_complete", convert_datetime)
sqlite3.register_converter("node_ready_for_giveback", convert_datetime)
sqlite3.register_converter("node_giveback_starts", convert_datetime)
sqlite3.register_converter("node_giveback_complete", convert_datetime)


class AzEventsDB:
    """SQLite database for storing Azure maintenance events."""

    def __init__(self, config: Config, db_name: str = "azevents.db") -> None:
        """Initialize the Azure events database.

        Args:
            config: Configuration object with db_dir path.
            db_name: Name of the database file.
        """
        db_location = config.db_dir / db_name
        self.conn = sqlite3.connect(db_location, detect_types=sqlite3.PARSE_DECLTYPES)
        self.conn.row_factory = sqlite3.Row  # Enables dictionary-like access
        self.create_table()

    def create_table(self) -> None:
        """Create the maintenance_events table if it doesn't exist."""
        cur = self.conn.cursor()
        cur.execute(
            """
            SELECT name FROM sqlite_master WHERE type='table' AND name='maintenance_events'
        """
        )
        if cur.fetchone() is None:
            with self.conn:
                self.conn.execute(
                    """
                    CREATE TABLE IF NOT EXISTS maintenance_events (
                        event_id TEXT PRIMARY KEY,
                        cluster TEXT DEFAULT 'Unknown',
                        node TEXT DEFAULT 'Unknown',
                        type TEXT DEFAULT 'Unknown',
                        az_maint_not_before TEXT,
                        az_maint_scheduled TEXT,
                        az_maint_started TEXT,
                        az_maint_complete TEXT,
                        node_takeover_complete TEXT,
                        node_reboot_starts TEXT,
                        node_reboot_complete TEXT,
                        node_ready_for_giveback TEXT,
                        node_giveback_starts TEXT,
                        node_giveback_complete TEXT
                    )
                """
                )

    def upsert_event(self, event: dict[str, Any]) -> None:
        """Insert or update a maintenance event.

        Args:
            event: Dictionary with event fields.
        """
        columns = ", ".join(event.keys())
        placeholders = ", ".join(f":{key}" for key in event)
        updates = ", ".join(f"{key}=excluded.{key}" for key in event)

        sql = f"""
            INSERT INTO maintenance_events ({columns})
            VALUES ({placeholders})
            ON CONFLICT(event_id) DO UPDATE SET
            {updates}
        """

        with self.conn:
            self.conn.execute(sql, event)

    def get_event_by_id(self, event_id: str) -> sqlite3.Row | None:
        """Get an event by its ID.

        Args:
            event_id: The event ID to look up.

        Returns:
            The event row or None if not found.
        """
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM maintenance_events WHERE event_id = ?", (event_id,))
        result: sqlite3.Row | None = cur.fetchone()
        return result

    def get_events_by_cluster(self, cluster: str) -> list[sqlite3.Row]:
        """Get all events for a cluster.

        Args:
            cluster: Cluster name to filter by.

        Returns:
            List of matching events.
        """
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM maintenance_events WHERE cluster = ?", (cluster,))
        return cur.fetchall()

    def get_events_by_node(self, node: str) -> list[sqlite3.Row]:
        """Get all events for a node.

        Args:
            node: Node name to filter by.

        Returns:
            List of matching events.
        """
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM maintenance_events WHERE node = ?", (node,))
        return cur.fetchall()

    def get_events_between_datetimes(
        self,
        field: str,
        start_datetime: datetime,
        end_datetime: datetime,
    ) -> list[sqlite3.Row]:
        """Get events within a time range for a specific field.

        Args:
            field: Date field to filter on.
            start_datetime: Start of time range.
            end_datetime: End of time range.

        Returns:
            List of matching events.
        """
        query = f"SELECT * FROM maintenance_events WHERE {field} BETWEEN ? AND ?"
        cur = self.conn.cursor()
        cur.execute(query, (start_datetime, end_datetime))
        return cur.fetchall()
