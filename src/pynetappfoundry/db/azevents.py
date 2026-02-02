"""Azure maintenance events database."""

from __future__ import annotations

import sqlite3
from datetime import datetime
from typing import TYPE_CHECKING, Any, ClassVar

from pynetappfoundry.db.base import SQLiteDB, adapt_datetime, convert_datetime

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
# SMB client impact tracking fields
sqlite3.register_converter("lif_failover_start", convert_datetime)
sqlite3.register_converter("lif_failover_complete", convert_datetime)
sqlite3.register_converter("cifs_witness_time", convert_datetime)
sqlite3.register_converter("aggr_giveback_start", convert_datetime)
sqlite3.register_converter("aggr_giveback_complete", convert_datetime)


class AzEventsDB(SQLiteDB):
    """SQLite database for storing Azure maintenance events."""

    SCHEMA_VERSION: ClassVar[int] = 2

    # V1 columns (original schema)
    V1_COLUMNS: ClassVar[list[tuple[str, str]]] = [
        ("event_id", "TEXT PRIMARY KEY"),
        ("cluster", "TEXT DEFAULT 'Unknown'"),
        ("node", "TEXT DEFAULT 'Unknown'"),
        ("type", "TEXT DEFAULT 'Unknown'"),
        ("az_maint_not_before", "TEXT"),
        ("az_maint_scheduled", "TEXT"),
        ("az_maint_started", "TEXT"),
        ("az_maint_complete", "TEXT"),
        ("node_takeover_complete", "TEXT"),
        ("node_reboot_starts", "TEXT"),
        ("node_reboot_complete", "TEXT"),
        ("node_ready_for_giveback", "TEXT"),
        ("node_giveback_starts", "TEXT"),
        ("node_giveback_complete", "TEXT"),
    ]

    # V2 columns (SMB client impact tracking)
    V2_COLUMNS: ClassVar[list[tuple[str, str]]] = [
        ("lif_failover_start", "TEXT"),
        ("lif_failover_complete", "TEXT"),
        ("cifs_transition_ms", "INTEGER"),
        ("cifs_witness_time", "TEXT"),
        ("cifs_witness_clients", "INTEGER"),
        ("aggr_giveback_start", "TEXT"),
        ("aggr_giveback_complete", "TEXT"),
    ]

    def __init__(self, config: Config, db_name: str = "azevents.db") -> None:
        """Initialize the Azure events database.

        Args:
            config: Configuration object with db_dir path.
            db_name: Name of the database file.
        """
        db_location = config.db_dir / db_name
        self.conn = sqlite3.connect(db_location, detect_types=sqlite3.PARSE_DECLTYPES)
        self.conn.row_factory = sqlite3.Row  # Enables dictionary-like access
        self._init_db()

    def _create_schema(self) -> None:
        """Create the maintenance_events table with current schema."""
        all_columns = self.V1_COLUMNS + self.V2_COLUMNS
        columns = ", ".join(f"{name} {col_type}" for name, col_type in all_columns)
        self.conn.execute(f"CREATE TABLE maintenance_events ({columns})")

    def _upgrade_to_v2(self) -> None:
        """Add SMB client impact tracking columns."""
        for col_name, col_type in self.V2_COLUMNS:
            # For ALTER TABLE, use simple type (no DEFAULT, no constraints)
            simple_type = col_type.split()[0]  # Gets TEXT, INTEGER, etc.
            self.conn.execute(f"ALTER TABLE maintenance_events ADD COLUMN {col_name} {simple_type}")

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
