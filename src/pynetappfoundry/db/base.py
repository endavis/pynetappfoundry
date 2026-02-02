"""Base database utilities."""

from __future__ import annotations

import sqlite3
from abc import ABC, abstractmethod
from datetime import datetime
from typing import ClassVar


class SchemaUpgradeError(Exception):
    """Raised when a schema upgrade fails."""


class SQLiteDB(ABC):
    """Abstract base class for SQLite databases with version-based migrations.

    Provides automatic schema versioning and migration support. Subclasses must:
    - Set SCHEMA_VERSION class variable to current schema version
    - Implement _create_schema() for new database creation
    - Implement _upgrade_to_v{N}() methods for each version upgrade

    Example:
        class MyDB(SQLiteDB):
            SCHEMA_VERSION = 2

            def _create_schema(self) -> None:
                self.conn.execute("CREATE TABLE ...")

            def _upgrade_to_v2(self) -> None:
                self.conn.execute("ALTER TABLE ...")
    """

    SCHEMA_VERSION: ClassVar[int] = 1
    conn: sqlite3.Connection

    def _init_db(self) -> None:
        """Initialize database, creating schema or running migrations as needed.

        Call this in __init__ after establishing the connection.
        """
        current_version = self._get_schema_version()

        if current_version == 0:
            # New database
            with self.conn:
                self._create_schema()
                self._set_schema_version(self.SCHEMA_VERSION)
        elif current_version < self.SCHEMA_VERSION:
            # Existing database needs upgrade
            self._run_upgrades(current_version)
        elif current_version > self.SCHEMA_VERSION:
            raise SchemaUpgradeError(
                f"Database version {current_version} is newer than "
                f"supported version {self.SCHEMA_VERSION}. Downgrade not supported."
            )

    def _get_schema_version(self) -> int:
        """Get the current schema version from the database.

        Returns:
            0 for new database, 1 for existing database without version table,
            or the actual version number.
        """
        cursor = self.conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='_schema_version'"
        )
        if cursor.fetchone() is None:
            # Check if database has any tables (existing pre-migration DB)
            if self._has_existing_tables():
                return 1  # Treat as v1
            return 0  # New database

        cursor = self.conn.execute("SELECT version FROM _schema_version")
        row = cursor.fetchone()
        if row is None:
            return 1
        return int(row[0])

    def _set_schema_version(self, version: int) -> None:
        """Set the schema version in the database.

        Args:
            version: The version number to set.
        """
        self.conn.execute("CREATE TABLE IF NOT EXISTS _schema_version (version INTEGER NOT NULL)")
        self.conn.execute("DELETE FROM _schema_version")
        self.conn.execute("INSERT INTO _schema_version (version) VALUES (?)", (version,))

    def _has_existing_tables(self) -> bool:
        """Check if the database has any user tables.

        Returns:
            True if tables exist (excluding sqlite internal tables).
        """
        cursor = self.conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' "
            "AND name NOT LIKE 'sqlite_%' AND name != '_schema_version'"
        )
        return cursor.fetchone() is not None

    def _run_upgrades(self, from_version: int) -> None:
        """Run all required upgrades from from_version to SCHEMA_VERSION.

        Args:
            from_version: The current database version.

        Raises:
            SchemaUpgradeError: If an upgrade method is missing or fails.
        """
        for target_version in range(from_version + 1, self.SCHEMA_VERSION + 1):
            method_name = f"_upgrade_to_v{target_version}"
            upgrade_method = getattr(self, method_name, None)

            if upgrade_method is None:
                raise SchemaUpgradeError(
                    f"Missing upgrade method {method_name} for version {target_version}"
                )

            try:
                with self.conn:
                    upgrade_method()
                    self._set_schema_version(target_version)
            except Exception as e:
                raise SchemaUpgradeError(
                    f"Failed to upgrade to version {target_version}: {e}"
                ) from e

    @abstractmethod
    def _create_schema(self) -> None:
        """Create the database schema for a new database.

        Called when the database is first created. Subclasses must implement
        this to create all required tables with the current schema.
        """

    def close(self) -> None:
        """Close the database connection."""
        self.conn.close()

    def __enter__(self) -> SQLiteDB:
        """Context manager entry."""
        return self

    def __exit__(self, _exc_type: object, _exc_val: object, _exc_tb: object) -> None:
        """Context manager exit."""
        self.close()


def adapt_datetime(dt: datetime) -> str:
    """Adapter to convert datetime to ISO format string.

    Args:
        dt: Datetime object to convert.

    Returns:
        ISO format string.
    """
    return dt.isoformat()


def convert_datetime(s: bytes) -> datetime:
    """Converter to convert ISO format string to datetime.

    Args:
        s: Bytes containing ISO format date string.

    Returns:
        Datetime object.
    """
    return datetime.fromisoformat(s.decode())


# Register the default adapter and converter
sqlite3.register_adapter(datetime, adapt_datetime)
