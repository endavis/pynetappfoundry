"""EMS Events database for storing ONTAP event messages."""

from __future__ import annotations

import os
import sqlite3
from datetime import datetime
from typing import TYPE_CHECKING, Any

from pynetappfoundry.db.base import adapt_datetime, convert_datetime

if TYPE_CHECKING:
    from pynetappfoundry.core.config import Config

# Register converters for this module
sqlite3.register_adapter(datetime, adapt_datetime)
sqlite3.register_converter("time", convert_datetime)


class EmsEventsDB:
    """SQLite database for storing EMS events."""

    def __init__(
        self,
        config: Config,
        db_name: str = "ems_events.db",
        overwrite: bool = True,
    ) -> None:
        """Initialize the EMS events database.

        Args:
            config: Configuration object with db_dir path.
            db_name: Name of the database file.
            overwrite: If True, delete existing database on init.
        """
        db_dir = config.db_dir / "emsevents"
        os.makedirs(db_dir, exist_ok=True)
        db_location = db_dir / db_name
        self.overwrite = overwrite
        self.exists = False

        if os.path.exists(db_location):
            self.exists = True
            if self.overwrite:
                os.remove(db_location)

        self.conn = sqlite3.connect(db_location, detect_types=sqlite3.PARSE_DECLTYPES)
        self.create_table()

    def create_table(self) -> None:
        """Create the ems_events table if it doesn't exist."""
        cur = self.conn.cursor()
        cur.execute(
            """
            SELECT name FROM sqlite_master WHERE type='table' AND name='ems_events'
        """
        )
        if cur.fetchone() is None:
            with self.conn:
                self.conn.execute(
                    """
                    CREATE TABLE IF NOT EXISTS ems_events (
                        event_id TEXT,
                        cluster TEXT DEFAULT 'Unknown',
                        node TEXT DEFAULT 'Unknown',
                        time TEXT,
                        event TEXT DEFAULT 'Unknown',
                        severity TEXT DEFAULT 'Unknown',
                        message TEXT DEFAULT 'Unknown'
                    )
                """
                )

    def insert_event(self, event: dict[str, Any]) -> None:
        """Insert an EMS event.

        Args:
            event: Dictionary with event fields.
        """
        columns = ", ".join(event.keys())
        placeholders = ", ".join(f":{key}" for key in event)

        sql = f"""
            INSERT INTO ems_events ({columns})
            VALUES ({placeholders})
        """

        with self.conn:
            self.conn.execute(sql, event)

    def get_events_by_node(self, node: str) -> list[sqlite3.Row]:
        """Get events for a specific node.

        Args:
            node: Node name to filter by.

        Returns:
            List of matching events.
        """
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM ems_events WHERE node = ?", (node,))
        return cur.fetchall()

    def get_events_between_datetimes(
        self, start_datetime: datetime, end_datetime: datetime
    ) -> list[sqlite3.Row]:
        """Get events within a time range.

        Args:
            start_datetime: Start of time range.
            end_datetime: End of time range.

        Returns:
            List of matching events.
        """
        query = "SELECT * FROM ems_events WHERE time BETWEEN ? AND ?"
        cur = self.conn.cursor()
        cur.execute(query, (start_datetime, end_datetime))
        return cur.fetchall()
