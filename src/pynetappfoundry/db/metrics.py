"""Metrics database for storing time-series data."""

from __future__ import annotations

import sqlite3
from datetime import datetime
from typing import TYPE_CHECKING, Any

from pynetappfoundry.db.base import adapt_datetime, convert_datetime

if TYPE_CHECKING:
    from pynetappfoundry.core.config import Config

# Register converters for this module
sqlite3.register_adapter(datetime, adapt_datetime)
sqlite3.register_converter("timestamp", convert_datetime)


class MetricDB:
    """SQLite database for storing metrics data."""

    def __init__(self, config: Config, db_name: str = "metrics.db") -> None:
        """Initialize the metrics database.

        Args:
            config: Configuration object with db_dir path.
            db_name: Name of the database file.
        """
        self.db_location = config.db_dir / db_name
        self.conn = sqlite3.connect(
            self.db_location, detect_types=sqlite3.PARSE_DECLTYPES
        )
        self.conn.row_factory = sqlite3.Row  # Enables dictionary-like access

    def create_table(self, table_name: str) -> None:
        """Create a metrics table if it doesn't exist.

        Args:
            table_name: Name of the table to create.
        """
        cur = self.conn.cursor()
        cur.execute(
            f'''
            SELECT name FROM sqlite_master WHERE type="table" AND name="{table_name}"
        '''
        )
        if cur.fetchone() is None:
            sql = f'''
                    CREATE TABLE IF NOT EXISTS "{table_name}" (
                        timestamp TEXT PRIMARY KEY,
                        read_ops REAL,
                        write_ops REAL,
                        read_latency REAL,
                        write_latency REAL,
                        read_throughput REAL,
                        write_throughput REAL
                    )
                '''
            with self.conn:
                self.conn.execute(sql)

    def upsert_data(self, table_name: str, data: dict[str, Any]) -> None:
        """Insert or update a single row of data.

        Args:
            table_name: Target table name.
            data: Dictionary of column/value pairs.
        """
        columns = ", ".join(data.keys())
        placeholders = ", ".join(f":{key}" for key in data.keys())
        updates = ", ".join(f"{key}=excluded.{key}" for key in data.keys())

        sql = f'''
            INSERT INTO "{table_name}" ({columns})
            VALUES ({placeholders})
            ON CONFLICT(timestamp) DO UPDATE SET
            {updates}
        '''

        with self.conn:
            self.conn.execute(sql, data)

    def upsert_many(self, table_name: str, all_data: list[dict[str, Any]]) -> None:
        """Insert or update multiple rows of data.

        Args:
            table_name: Target table name.
            all_data: List of dictionaries with column/value pairs.
        """
        columns = list(all_data[0].keys())
        placeholders = ", ".join(f":{key}" for key in columns)
        updates = ", ".join(f"{key}=excluded.{key}" for key in columns)

        sql = f'''
            INSERT INTO "{table_name}" ({', '.join(columns)})
            VALUES ({placeholders})
            ON CONFLICT(timestamp) DO UPDATE SET
            {updates}
        '''
        with self.conn:
            self.conn.executemany(sql, all_data)
