"""Tests for SQLiteDB base class and schema migration."""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import ClassVar

import pytest

from pynetappfoundry.db.base import SchemaUpgradeError, SQLiteDB


class SimpleDB(SQLiteDB):
    """Simple test database with single table."""

    SCHEMA_VERSION: ClassVar[int] = 1

    def __init__(self, db_path: Path) -> None:
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self._init_db()

    def _create_schema(self) -> None:
        self.conn.execute("CREATE TABLE test_table (id INTEGER PRIMARY KEY, name TEXT)")


class VersionedDB(SQLiteDB):
    """Test database with multiple versions."""

    SCHEMA_VERSION: ClassVar[int] = 3

    def __init__(self, db_path: Path) -> None:
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self._init_db()

    def _create_schema(self) -> None:
        # Current schema (v3)
        self.conn.execute(
            "CREATE TABLE test_table "
            "(id INTEGER PRIMARY KEY, name TEXT, email TEXT, active INTEGER)"
        )

    def _upgrade_to_v2(self) -> None:
        # Add email column
        self.conn.execute("ALTER TABLE test_table ADD COLUMN email TEXT")

    def _upgrade_to_v3(self) -> None:
        # Add active column
        self.conn.execute("ALTER TABLE test_table ADD COLUMN active INTEGER")


class MissingUpgradeDB(SQLiteDB):
    """Test database missing an upgrade method."""

    SCHEMA_VERSION: ClassVar[int] = 2

    def __init__(self, db_path: Path) -> None:
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self._init_db()

    def _create_schema(self) -> None:
        self.conn.execute("CREATE TABLE test_table (id INTEGER PRIMARY KEY, name TEXT)")

    # Intentionally missing _upgrade_to_v2


class FailingUpgradeDB(SQLiteDB):
    """Test database with failing upgrade."""

    SCHEMA_VERSION: ClassVar[int] = 2

    def __init__(self, db_path: Path) -> None:
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self._init_db()

    def _create_schema(self) -> None:
        self.conn.execute("CREATE TABLE test_table (id INTEGER PRIMARY KEY, name TEXT)")

    def _upgrade_to_v2(self) -> None:
        # This will fail - column already exists (simulating a bad migration)
        raise RuntimeError("Simulated migration failure")


class TestSQLiteDBNewDatabase:
    """Tests for creating new databases."""

    def test_new_database_creates_schema(self, tmp_path: Path) -> None:
        """Test that a new database creates the schema."""
        db_path = tmp_path / "new.db"
        db = SimpleDB(db_path)

        # Verify table was created
        cursor = db.conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='test_table'"
        )
        assert cursor.fetchone() is not None
        db.close()

    def test_new_database_sets_version(self, tmp_path: Path) -> None:
        """Test that a new database sets the correct version."""
        db_path = tmp_path / "new.db"
        db = SimpleDB(db_path)

        # Verify version was set
        cursor = db.conn.execute("SELECT version FROM _schema_version")
        version = cursor.fetchone()[0]
        assert version == 1
        db.close()

    def test_new_versioned_database_uses_current_schema(self, tmp_path: Path) -> None:
        """Test that a new versioned database creates current schema."""
        db_path = tmp_path / "versioned.db"
        db = VersionedDB(db_path)

        # Verify schema is at v3 with all columns
        cursor = db.conn.execute("PRAGMA table_info(test_table)")
        columns = {row[1] for row in cursor.fetchall()}
        assert columns == {"id", "name", "email", "active"}

        # Verify version
        cursor = db.conn.execute("SELECT version FROM _schema_version")
        assert cursor.fetchone()[0] == 3
        db.close()


class TestSQLiteDBExistingDatabase:
    """Tests for opening existing databases."""

    def test_existing_v1_database_upgrades(self, tmp_path: Path) -> None:
        """Test that an existing v1 database is upgraded to current version."""
        db_path = tmp_path / "v1.db"

        # Create v1 database manually (pre-migration state)
        conn = sqlite3.connect(db_path)
        conn.execute("CREATE TABLE test_table (id INTEGER PRIMARY KEY, name TEXT)")
        conn.commit()
        conn.close()

        # Open with VersionedDB (SCHEMA_VERSION = 3)
        db = VersionedDB(db_path)

        # Verify upgrade happened
        cursor = db.conn.execute("PRAGMA table_info(test_table)")
        columns = {row[1] for row in cursor.fetchall()}
        assert columns == {"id", "name", "email", "active"}

        # Verify version
        cursor = db.conn.execute("SELECT version FROM _schema_version")
        assert cursor.fetchone()[0] == 3
        db.close()

    def test_existing_v2_database_upgrades(self, tmp_path: Path) -> None:
        """Test that an existing v2 database is upgraded to v3."""
        db_path = tmp_path / "v2.db"

        # Create v2 database manually
        conn = sqlite3.connect(db_path)
        conn.execute("CREATE TABLE test_table (id INTEGER PRIMARY KEY, name TEXT, email TEXT)")
        conn.execute("CREATE TABLE _schema_version (version INTEGER NOT NULL)")
        conn.execute("INSERT INTO _schema_version (version) VALUES (2)")
        conn.commit()
        conn.close()

        # Open with VersionedDB
        db = VersionedDB(db_path)

        # Verify upgrade to v3 happened
        cursor = db.conn.execute("PRAGMA table_info(test_table)")
        columns = {row[1] for row in cursor.fetchall()}
        assert columns == {"id", "name", "email", "active"}

        cursor = db.conn.execute("SELECT version FROM _schema_version")
        assert cursor.fetchone()[0] == 3
        db.close()

    def test_existing_current_version_no_changes(self, tmp_path: Path) -> None:
        """Test that a database at current version is not modified."""
        db_path = tmp_path / "current.db"

        # Create with VersionedDB first
        db1 = VersionedDB(db_path)
        db1.conn.execute(
            "INSERT INTO test_table (name, email, active) VALUES ('test', 'test@example.com', 1)"
        )
        db1.conn.commit()
        db1.close()

        # Reopen
        db2 = VersionedDB(db_path)

        # Verify data is preserved
        cursor = db2.conn.execute("SELECT * FROM test_table")
        row = cursor.fetchone()
        assert row["name"] == "test"
        assert row["email"] == "test@example.com"
        assert row["active"] == 1
        db2.close()


class TestSQLiteDBMigrationErrors:
    """Tests for migration error handling."""

    def test_missing_upgrade_method_raises_error(self, tmp_path: Path) -> None:
        """Test that missing upgrade method raises SchemaUpgradeError."""
        db_path = tmp_path / "missing.db"

        # Create v1 database manually
        conn = sqlite3.connect(db_path)
        conn.execute("CREATE TABLE test_table (id INTEGER PRIMARY KEY, name TEXT)")
        conn.commit()
        conn.close()

        # Open with MissingUpgradeDB (needs _upgrade_to_v2)
        with pytest.raises(SchemaUpgradeError, match="Missing upgrade method"):
            MissingUpgradeDB(db_path)

    def test_failing_upgrade_raises_error(self, tmp_path: Path) -> None:
        """Test that a failing upgrade raises SchemaUpgradeError."""
        db_path = tmp_path / "failing.db"

        # Create v1 database manually
        conn = sqlite3.connect(db_path)
        conn.execute("CREATE TABLE test_table (id INTEGER PRIMARY KEY, name TEXT)")
        conn.commit()
        conn.close()

        # Open with FailingUpgradeDB
        with pytest.raises(SchemaUpgradeError, match="Failed to upgrade"):
            FailingUpgradeDB(db_path)

    def test_failing_upgrade_does_not_update_version(self, tmp_path: Path) -> None:
        """Test that a failing upgrade leaves version unchanged."""
        db_path = tmp_path / "failing.db"

        # Create v1 database manually
        conn = sqlite3.connect(db_path)
        conn.execute("CREATE TABLE test_table (id INTEGER PRIMARY KEY, name TEXT)")
        conn.commit()
        conn.close()

        # Attempt upgrade
        with pytest.raises(SchemaUpgradeError):
            FailingUpgradeDB(db_path)

        # Verify version is still 1 (or no version table)
        conn = sqlite3.connect(db_path)
        cursor = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='_schema_version'"
        )
        if cursor.fetchone() is not None:
            cursor = conn.execute("SELECT version FROM _schema_version")
            row = cursor.fetchone()
            if row:
                assert row[0] == 1
        conn.close()

    def test_downgrade_raises_error(self, tmp_path: Path) -> None:
        """Test that opening a newer database with older code raises error."""
        db_path = tmp_path / "newer.db"

        # Create v3 database
        conn = sqlite3.connect(db_path)
        conn.execute(
            "CREATE TABLE test_table "
            "(id INTEGER PRIMARY KEY, name TEXT, email TEXT, active INTEGER)"
        )
        conn.execute("CREATE TABLE _schema_version (version INTEGER NOT NULL)")
        conn.execute("INSERT INTO _schema_version (version) VALUES (3)")
        conn.commit()
        conn.close()

        # Try to open with SimpleDB (SCHEMA_VERSION = 1)
        with pytest.raises(SchemaUpgradeError, match="Downgrade not supported"):
            SimpleDB(db_path)


class TestSQLiteDBContextManager:
    """Tests for context manager support."""

    def test_context_manager_closes_connection(self, tmp_path: Path) -> None:
        """Test that context manager closes connection on exit."""
        db_path = tmp_path / "context.db"

        with SimpleDB(db_path) as db:
            db.conn.execute("INSERT INTO test_table (name) VALUES ('test')")
            db.conn.commit()

        # Connection should be closed
        with pytest.raises(sqlite3.ProgrammingError):
            db.conn.execute("SELECT * FROM test_table")

    def test_context_manager_closes_on_exception(self, tmp_path: Path) -> None:
        """Test that context manager closes connection on exception."""
        db_path = tmp_path / "context_exc.db"

        with pytest.raises(ValueError, match="test error"), SimpleDB(db_path) as db:
            raise ValueError("test error")

        # Connection should be closed
        with pytest.raises(sqlite3.ProgrammingError):
            db.conn.execute("SELECT * FROM test_table")


class TestSQLiteDBMultipleUpgrades:
    """Tests for sequential upgrades."""

    def test_sequential_upgrades_from_v1_to_v3(self, tmp_path: Path) -> None:
        """Test that all upgrades run sequentially from v1 to v3."""
        db_path = tmp_path / "sequential.db"

        # Create v1 database manually
        conn = sqlite3.connect(db_path)
        conn.execute("CREATE TABLE test_table (id INTEGER PRIMARY KEY, name TEXT)")
        conn.execute("INSERT INTO test_table (name) VALUES ('Alice')")
        conn.commit()
        conn.close()

        # Open with VersionedDB (v3)
        db = VersionedDB(db_path)

        # Verify all columns exist
        cursor = db.conn.execute("PRAGMA table_info(test_table)")
        columns = {row[1] for row in cursor.fetchall()}
        assert columns == {"id", "name", "email", "active"}

        # Verify data is preserved
        cursor = db.conn.execute("SELECT * FROM test_table")
        row = cursor.fetchone()
        assert row["name"] == "Alice"
        # New columns should be NULL
        assert row["email"] is None
        assert row["active"] is None

        db.close()


class TestSQLiteDBDataPreservation:
    """Tests for data preservation during migrations."""

    def test_data_preserved_during_upgrade(self, tmp_path: Path) -> None:
        """Test that existing data is preserved during upgrade."""
        db_path = tmp_path / "preserve.db"

        # Create v1 database with data
        conn = sqlite3.connect(db_path)
        conn.execute("CREATE TABLE test_table (id INTEGER PRIMARY KEY, name TEXT)")
        conn.execute("INSERT INTO test_table (name) VALUES ('Alice')")
        conn.execute("INSERT INTO test_table (name) VALUES ('Bob')")
        conn.execute("INSERT INTO test_table (name) VALUES ('Charlie')")
        conn.commit()
        conn.close()

        # Upgrade to v3
        db = VersionedDB(db_path)

        # Verify all data preserved
        cursor = db.conn.execute("SELECT name FROM test_table ORDER BY name")
        names = [row[0] for row in cursor.fetchall()]
        assert names == ["Alice", "Bob", "Charlie"]

        db.close()
