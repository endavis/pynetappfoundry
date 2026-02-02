"""Tests for database classes."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from pynetappfoundry.db.azevents import AzEventsDB
from pynetappfoundry.db.base import adapt_datetime, convert_datetime
from pynetappfoundry.db.metrics import MetricDB, _validate_table_name


class TestTableNameValidation:
    """Tests for table name validation to prevent SQL injection."""

    def test_valid_table_names(self) -> None:
        """Test that valid table names pass validation."""
        valid_names = [
            "metrics",
            "test_metrics",
            "_private_table",
            "cluster1_metrics",
            "metrics.2024",
            "cluster-01-data",
            "A" * 128,  # Max length
        ]
        for name in valid_names:
            _validate_table_name(name)  # Should not raise

    def test_invalid_table_names(self) -> None:
        """Test that invalid table names are rejected."""
        invalid_names = [
            "1_starts_with_number",
            "-starts-with-hyphen",
            ".starts_with_dot",
            "has spaces",
            "has;semicolon",
            "has'quote",
            'has"doublequote',
            "has(parens)",
            "Robert'); DROP TABLE students;--",
            "",
            "A" * 129,  # Too long
        ]
        for name in invalid_names:
            with pytest.raises(ValueError, match="Invalid table name"):
                _validate_table_name(name)


class TestDatetimeAdapters:
    """Tests for datetime adapter and converter functions."""

    def test_adapt_datetime(self) -> None:
        """Test converting datetime to ISO format string."""
        dt = datetime(2024, 3, 15, 10, 30, 45)
        result = adapt_datetime(dt)
        assert result == "2024-03-15T10:30:45"

    def test_adapt_datetime_with_microseconds(self) -> None:
        """Test converting datetime with microseconds."""
        dt = datetime(2024, 3, 15, 10, 30, 45, 123456)
        result = adapt_datetime(dt)
        assert result == "2024-03-15T10:30:45.123456"

    def test_convert_datetime(self) -> None:
        """Test converting ISO format bytes to datetime."""
        s = b"2024-03-15T10:30:45"
        result = convert_datetime(s)
        assert result == datetime(2024, 3, 15, 10, 30, 45)

    def test_convert_datetime_with_microseconds(self) -> None:
        """Test converting ISO format bytes with microseconds."""
        s = b"2024-03-15T10:30:45.123456"
        result = convert_datetime(s)
        assert result == datetime(2024, 3, 15, 10, 30, 45, 123456)


@pytest.fixture
def mock_config(tmp_path: Path) -> MagicMock:
    """Create a mock config with db_dir."""
    config = MagicMock()
    config.db_dir = tmp_path
    return config


class TestMetricDB:
    """Tests for MetricDB class."""

    def test_init_creates_connection(self, mock_config: MagicMock) -> None:
        """Test that MetricDB creates a database connection."""
        db = MetricDB(mock_config)
        assert db.conn is not None
        assert db.db_location == mock_config.db_dir / "metrics.db"
        db.conn.close()

    def test_init_custom_db_name(self, mock_config: MagicMock) -> None:
        """Test MetricDB with custom database name."""
        db = MetricDB(mock_config, db_name="custom.db")
        assert db.db_location == mock_config.db_dir / "custom.db"
        db.conn.close()

    def test_create_table(self, mock_config: MagicMock) -> None:
        """Test creating a metrics table."""
        db = MetricDB(mock_config)
        db.create_table("test_metrics")

        # Verify table exists
        cur = db.conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='test_metrics'")
        result = cur.fetchone()
        assert result is not None
        assert result[0] == "test_metrics"
        db.conn.close()

    def test_create_table_has_expected_columns(self, mock_config: MagicMock) -> None:
        """Test that created table has expected columns."""
        db = MetricDB(mock_config)
        db.create_table("test_metrics")

        cur = db.conn.cursor()
        cur.execute("PRAGMA table_info(test_metrics)")
        columns = {row[1] for row in cur.fetchall()}

        expected_columns = {
            "timestamp",
            "read_ops",
            "write_ops",
            "read_latency",
            "write_latency",
            "read_throughput",
            "write_throughput",
        }
        assert columns == expected_columns
        db.conn.close()

    def test_create_table_idempotent(self, mock_config: MagicMock) -> None:
        """Test that create_table can be called multiple times."""
        db = MetricDB(mock_config)
        db.create_table("test_metrics")
        db.create_table("test_metrics")  # Should not raise

        cur = db.conn.cursor()
        cur.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='test_metrics'")
        count = cur.fetchone()[0]
        assert count == 1
        db.conn.close()

    def test_upsert_data_insert(self, mock_config: MagicMock) -> None:
        """Test inserting data with upsert_data."""
        db = MetricDB(mock_config)
        db.create_table("test_metrics")

        data = {
            "timestamp": "2024-03-15T10:00:00",
            "read_ops": 100.0,
            "write_ops": 50.0,
            "read_latency": 1.5,
            "write_latency": 2.0,
            "read_throughput": 1000.0,
            "write_throughput": 500.0,
        }
        db.upsert_data("test_metrics", data)

        cur = db.conn.cursor()
        cur.execute("SELECT * FROM test_metrics WHERE timestamp = ?", (data["timestamp"],))
        row = cur.fetchone()
        assert row is not None
        assert row["read_ops"] == 100.0
        assert row["write_ops"] == 50.0
        db.conn.close()

    def test_upsert_data_update(self, mock_config: MagicMock) -> None:
        """Test updating data with upsert_data (conflict on timestamp)."""
        db = MetricDB(mock_config)
        db.create_table("test_metrics")

        data = {
            "timestamp": "2024-03-15T10:00:00",
            "read_ops": 100.0,
            "write_ops": 50.0,
            "read_latency": 1.5,
            "write_latency": 2.0,
            "read_throughput": 1000.0,
            "write_throughput": 500.0,
        }
        db.upsert_data("test_metrics", data)

        # Update with same timestamp
        updated_data = {
            "timestamp": "2024-03-15T10:00:00",
            "read_ops": 200.0,  # Changed
            "write_ops": 100.0,  # Changed
            "read_latency": 1.5,
            "write_latency": 2.0,
            "read_throughput": 2000.0,  # Changed
            "write_throughput": 1000.0,  # Changed
        }
        db.upsert_data("test_metrics", updated_data)

        cur = db.conn.cursor()
        cur.execute("SELECT * FROM test_metrics WHERE timestamp = ?", (data["timestamp"],))
        row = cur.fetchone()
        assert row["read_ops"] == 200.0  # Should be updated
        assert row["write_ops"] == 100.0
        db.conn.close()

    def test_upsert_many(self, mock_config: MagicMock) -> None:
        """Test inserting multiple rows with upsert_many."""
        db = MetricDB(mock_config)
        db.create_table("test_metrics")

        all_data = [
            {
                "timestamp": "2024-03-15T10:00:00",
                "read_ops": 100.0,
                "write_ops": 50.0,
                "read_latency": 1.5,
                "write_latency": 2.0,
                "read_throughput": 1000.0,
                "write_throughput": 500.0,
            },
            {
                "timestamp": "2024-03-15T10:01:00",
                "read_ops": 110.0,
                "write_ops": 55.0,
                "read_latency": 1.6,
                "write_latency": 2.1,
                "read_throughput": 1100.0,
                "write_throughput": 550.0,
            },
            {
                "timestamp": "2024-03-15T10:02:00",
                "read_ops": 120.0,
                "write_ops": 60.0,
                "read_latency": 1.7,
                "write_latency": 2.2,
                "read_throughput": 1200.0,
                "write_throughput": 600.0,
            },
        ]
        db.upsert_many("test_metrics", all_data)

        cur = db.conn.cursor()
        cur.execute("SELECT COUNT(*) FROM test_metrics")
        count = cur.fetchone()[0]
        assert count == 3

        cur.execute("SELECT * FROM test_metrics ORDER BY timestamp")
        rows = cur.fetchall()
        assert rows[0]["read_ops"] == 100.0
        assert rows[1]["read_ops"] == 110.0
        assert rows[2]["read_ops"] == 120.0
        db.conn.close()

    def test_upsert_many_updates_on_conflict(self, mock_config: MagicMock) -> None:
        """Test that upsert_many updates on timestamp conflict."""
        db = MetricDB(mock_config)
        db.create_table("test_metrics")

        # Insert initial data
        initial_data = [
            {
                "timestamp": "2024-03-15T10:00:00",
                "read_ops": 100.0,
                "write_ops": 50.0,
                "read_latency": 1.5,
                "write_latency": 2.0,
                "read_throughput": 1000.0,
                "write_throughput": 500.0,
            },
        ]
        db.upsert_many("test_metrics", initial_data)

        # Update with same timestamp
        updated_data = [
            {
                "timestamp": "2024-03-15T10:00:00",
                "read_ops": 999.0,  # Changed
                "write_ops": 888.0,  # Changed
                "read_latency": 1.5,
                "write_latency": 2.0,
                "read_throughput": 1000.0,
                "write_throughput": 500.0,
            },
        ]
        db.upsert_many("test_metrics", updated_data)

        cur = db.conn.cursor()
        cur.execute("SELECT COUNT(*) FROM test_metrics")
        count = cur.fetchone()[0]
        assert count == 1  # Should still be 1 row

        cur.execute("SELECT * FROM test_metrics")
        row = cur.fetchone()
        assert row["read_ops"] == 999.0  # Should be updated
        assert row["write_ops"] == 888.0
        db.conn.close()

    def test_row_factory_provides_dict_access(self, mock_config: MagicMock) -> None:
        """Test that rows can be accessed like dictionaries."""
        db = MetricDB(mock_config)
        db.create_table("test_metrics")

        data = {
            "timestamp": "2024-03-15T10:00:00",
            "read_ops": 100.0,
            "write_ops": 50.0,
            "read_latency": 1.5,
            "write_latency": 2.0,
            "read_throughput": 1000.0,
            "write_throughput": 500.0,
        }
        db.upsert_data("test_metrics", data)

        cur = db.conn.cursor()
        cur.execute("SELECT * FROM test_metrics")
        row = cur.fetchone()

        # Test dictionary-like access
        assert row["timestamp"] == "2024-03-15T10:00:00"
        assert row["read_ops"] == 100.0

        # Test that keys() method works (using list for explicit test)
        keys_list = list(row.keys())
        assert "timestamp" in keys_list
        assert "read_ops" in keys_list
        db.conn.close()


class TestAzEventsDB:
    """Tests for AzEventsDB class."""

    def test_creates_table_on_init(self, mock_config: MagicMock) -> None:
        """Test that AzEventsDB creates table on initialization."""
        db = AzEventsDB(mock_config)

        cur = db.conn.cursor()
        cur.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='maintenance_events'"
        )
        result = cur.fetchone()
        assert result is not None
        db.conn.close()

    def test_creates_all_schema_columns(self, mock_config: MagicMock) -> None:
        """Test that all schema columns are created."""
        db = AzEventsDB(mock_config)

        cur = db.conn.cursor()
        cur.execute("PRAGMA table_info(maintenance_events)")
        columns = {row[1] for row in cur.fetchall()}

        expected_columns = {col_name for col_name, _ in AzEventsDB.SCHEMA}
        assert columns == expected_columns
        db.conn.close()

    def test_migrates_missing_columns(self, mock_config: MagicMock) -> None:
        """Test that missing columns are added to existing table."""
        import sqlite3

        # Create an old-style table without SMB columns
        db_location = mock_config.db_dir / "azevents.db"
        conn = sqlite3.connect(db_location)
        conn.execute(
            """
            CREATE TABLE maintenance_events (
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
        conn.commit()
        conn.close()

        # Now open with AzEventsDB which should migrate
        db = AzEventsDB(mock_config)

        cur = db.conn.cursor()
        cur.execute("PRAGMA table_info(maintenance_events)")
        columns = {row[1] for row in cur.fetchall()}

        # Verify SMB columns were added
        assert "lif_failover_start" in columns
        assert "lif_failover_complete" in columns
        assert "cifs_transition_ms" in columns
        assert "cifs_witness_time" in columns
        assert "cifs_witness_clients" in columns
        assert "aggr_giveback_start" in columns
        assert "aggr_giveback_complete" in columns
        db.conn.close()

    def test_preserves_existing_data_on_migration(self, mock_config: MagicMock) -> None:
        """Test that existing data is preserved during migration."""
        import sqlite3

        # Create an old-style table with data
        db_location = mock_config.db_dir / "azevents.db"
        conn = sqlite3.connect(db_location)
        conn.execute(
            """
            CREATE TABLE maintenance_events (
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
        conn.execute(
            """
            INSERT INTO maintenance_events (event_id, cluster, node)
            VALUES ('test-event-123', 'test-cluster', 'test-node')
        """
        )
        conn.commit()
        conn.close()

        # Now open with AzEventsDB which should migrate
        db = AzEventsDB(mock_config)

        # Verify data is preserved
        event = db.get_event_by_id("test-event-123")
        assert event is not None
        assert event["cluster"] == "test-cluster"
        assert event["node"] == "test-node"
        db.conn.close()

    def test_upsert_with_new_columns(self, mock_config: MagicMock) -> None:
        """Test that upsert works with new SMB columns."""
        db = AzEventsDB(mock_config)

        event = {
            "event_id": "test-event-456",
            "cluster": "test-cluster",
            "node": "test-node",
            "lif_failover_start": "2024-01-15T12:01:00Z",
            "lif_failover_complete": "2024-01-15T12:04:00Z",
            "cifs_transition_ms": 14450,
            "cifs_witness_clients": 5,
        }
        db.upsert_event(event)

        result = db.get_event_by_id("test-event-456")
        assert result is not None
        assert result["lif_failover_start"] == "2024-01-15T12:01:00Z"
        assert result["cifs_transition_ms"] == 14450
        assert result["cifs_witness_clients"] == 5
        db.conn.close()

    def test_no_duplicate_columns_on_reopen(self, mock_config: MagicMock) -> None:
        """Test that reopening database doesn't create duplicate columns."""
        db1 = AzEventsDB(mock_config)
        db1.conn.close()

        # Reopen
        db2 = AzEventsDB(mock_config)

        cur = db2.conn.cursor()
        cur.execute("PRAGMA table_info(maintenance_events)")
        columns = [row[1] for row in cur.fetchall()]

        # Check no duplicates
        assert len(columns) == len(set(columns))
        db2.conn.close()
