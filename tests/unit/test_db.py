"""Tests for database classes."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from unittest.mock import MagicMock

import pytest

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
