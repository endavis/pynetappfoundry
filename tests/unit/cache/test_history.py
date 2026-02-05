"""Tests for cache history database and integration."""

from __future__ import annotations

from pathlib import Path

import pytest
from click.testing import CliRunner

from pynetappfoundry.cache import CachedClusterMetadata, compute_diff
from pynetappfoundry.cache.history_db import CacheHistoryDB
from pynetappfoundry.cache.models import NodeInfo
from pynetappfoundry.cli.commands.cache.history import history


class TestCacheHistoryDB:
    """Tests for CacheHistoryDB class."""

    @pytest.fixture
    def db(self, tmp_path: Path) -> CacheHistoryDB:
        """Create a test history database."""
        db_path = tmp_path / "test_history.db"
        return CacheHistoryDB(db_path=db_path)

    def test_init_creates_table(self, db: CacheHistoryDB) -> None:
        """Test that initialization creates the cache_changes table."""
        cursor = db.conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = {row["name"] for row in cursor.fetchall()}
        assert "cache_changes" in tables

    def test_record_change_initial(self, db: CacheHistoryDB) -> None:
        """Test recording initial change (no before)."""
        change_id = db.record_change(
            cluster_name="test-cluster",
            before_json=None,
            after_json='{"cluster_name": "test-cluster"}',
            summary=[{"category": "nodes", "type": "added", "entity": "node1"}],
        )
        assert change_id > 0

    def test_record_change_with_before(self, db: CacheHistoryDB) -> None:
        """Test recording change with before snapshot."""
        change_id = db.record_change(
            cluster_name="test-cluster",
            before_json='{"version": "1"}',
            after_json='{"version": "2"}',
            summary=[
                {
                    "category": "cluster",
                    "type": "modified",
                    "entity": "cluster",
                    "field": "version",
                    "old": "1",
                    "new": "2",
                }
            ],
        )
        assert change_id > 0

    def test_get_latest_snapshot_empty(self, db: CacheHistoryDB) -> None:
        """Test get_latest_snapshot returns None when no history."""
        result = db.get_latest_snapshot("test-cluster")
        assert result is None

    def test_get_latest_snapshot(self, db: CacheHistoryDB) -> None:
        """Test get_latest_snapshot returns most recent snapshot."""
        # Record two changes
        db.record_change(
            cluster_name="test-cluster",
            before_json=None,
            after_json='{"version": "1"}',
            summary=[],
        )
        db.record_change(
            cluster_name="test-cluster",
            before_json='{"version": "1"}',
            after_json='{"version": "2"}',
            summary=[],
        )

        result = db.get_latest_snapshot("test-cluster")
        assert result is not None
        assert result["after_json"] == '{"version": "2"}'

    def test_get_change_by_id(self, db: CacheHistoryDB) -> None:
        """Test retrieving a specific change by ID."""
        change_id = db.record_change(
            cluster_name="test-cluster",
            before_json='{"before": true}',
            after_json='{"after": true}',
            summary=[{"category": "test", "type": "added", "entity": "item"}],
        )

        record = db.get_change_by_id(change_id)
        assert record is not None
        assert record["id"] == change_id
        assert record["cluster_name"] == "test-cluster"
        assert record["before_json"] == '{"before": true}'
        assert record["after_json"] == '{"after": true}'
        assert record["summary"] == [{"category": "test", "type": "added", "entity": "item"}]

    def test_get_change_by_id_not_found(self, db: CacheHistoryDB) -> None:
        """Test get_change_by_id returns None for nonexistent ID."""
        result = db.get_change_by_id(9999)
        assert result is None

    def test_get_change_history_empty(self, db: CacheHistoryDB) -> None:
        """Test get_change_history returns empty list when no history."""
        result = db.get_change_history(cluster_name="test-cluster")
        assert result == []

    def test_get_change_history(self, db: CacheHistoryDB) -> None:
        """Test retrieving change history."""
        # Record multiple changes
        for i in range(3):
            db.record_change(
                cluster_name="test-cluster",
                before_json=None,
                after_json=f'{{"version": {i}}}',
                summary=[{"index": i}],
            )

        result = db.get_change_history(cluster_name="test-cluster")
        assert len(result) == 3
        # Should be in reverse order (newest first)
        assert result[0]["summary"] == [{"index": 2}]
        assert result[2]["summary"] == [{"index": 0}]

    def test_get_change_history_all_clusters(self, db: CacheHistoryDB) -> None:
        """Test retrieving history for all clusters."""
        db.record_change(
            cluster_name="cluster1",
            before_json=None,
            after_json="{}",
            summary=[],
        )
        db.record_change(
            cluster_name="cluster2",
            before_json=None,
            after_json="{}",
            summary=[],
        )

        result = db.get_change_history(cluster_name=None)
        assert len(result) == 2
        clusters = {r["cluster_name"] for r in result}
        assert clusters == {"cluster1", "cluster2"}

    def test_get_change_history_limit(self, db: CacheHistoryDB) -> None:
        """Test limit parameter in get_change_history."""
        for i in range(5):
            db.record_change(
                cluster_name="test-cluster",
                before_json=None,
                after_json=f'{{"version": {i}}}',
                summary=[],
            )

        result = db.get_change_history(cluster_name="test-cluster", limit=2)
        assert len(result) == 2

    def test_get_change_history_offset(self, db: CacheHistoryDB) -> None:
        """Test offset parameter in get_change_history."""
        for i in range(5):
            db.record_change(
                cluster_name="test-cluster",
                before_json=None,
                after_json=f'{{"version": {i}}}',
                summary=[{"index": i}],
            )

        result = db.get_change_history(cluster_name="test-cluster", limit=2, offset=2)
        assert len(result) == 2
        # Should skip the first 2 (indices 4, 3) and get indices 2, 1
        assert result[0]["summary"] == [{"index": 2}]
        assert result[1]["summary"] == [{"index": 1}]

    def test_get_history_count(self, db: CacheHistoryDB) -> None:
        """Test getting total history count."""
        for _ in range(3):
            db.record_change(
                cluster_name="test-cluster",
                before_json=None,
                after_json="{}",
                summary=[],
            )

        count = db.get_history_count(cluster_name="test-cluster")
        assert count == 3

    def test_get_history_count_all(self, db: CacheHistoryDB) -> None:
        """Test getting total history count for all clusters."""
        db.record_change("cluster1", None, "{}", [])
        db.record_change("cluster1", None, "{}", [])
        db.record_change("cluster2", None, "{}", [])

        assert db.get_history_count() == 3
        assert db.get_history_count("cluster1") == 2
        assert db.get_history_count("cluster2") == 1

    def test_invalid_cluster_name_on_record_change(self, db: CacheHistoryDB) -> None:
        """Test that invalid cluster name raises error on record_change."""
        with pytest.raises(ValueError, match="Invalid cluster name"):
            db.record_change("123invalid", None, "{}", [])

    def test_invalid_cluster_name_on_get_latest_snapshot(self, db: CacheHistoryDB) -> None:
        """Test that invalid cluster name raises error on get_latest_snapshot."""
        with pytest.raises(ValueError, match="Invalid cluster name"):
            db.get_latest_snapshot("123invalid")

    def test_invalid_cluster_name_on_get_history(self, db: CacheHistoryDB) -> None:
        """Test that invalid cluster name raises error on get_change_history."""
        with pytest.raises(ValueError, match="Invalid cluster name"):
            db.get_change_history(cluster_name="123invalid")

    def test_get_snapshot_at_date_not_found(self, db: CacheHistoryDB) -> None:
        """Test get_snapshot_at_date returns None when no snapshot exists."""
        result = db.get_snapshot_at_date("test-cluster", "2024-01-01")
        assert result is None

    def test_get_snapshot_at_date_exact(self, db: CacheHistoryDB) -> None:
        """Test get_snapshot_at_date returns snapshot on exact date."""
        # Manually insert records with specific dates
        db.conn.execute(
            """
            INSERT INTO cache_changes
            (cluster_name, changed_at, before_json, after_json, summary_json)
            VALUES (?, ?, ?, ?, ?)
            """,
            ("test-cluster", "2024-01-15T10:00:00", None, '{"v": 1}', "[]"),
        )
        db.conn.commit()

        result = db.get_snapshot_at_date("test-cluster", "2024-01-15T10:00:00")
        assert result is not None
        assert result["after_json"] == '{"v": 1}'

    def test_get_snapshot_at_date_before(self, db: CacheHistoryDB) -> None:
        """Test get_snapshot_at_date returns most recent snapshot before date."""
        # Insert records with specific dates
        db.conn.execute(
            """
            INSERT INTO cache_changes
            (cluster_name, changed_at, before_json, after_json, summary_json)
            VALUES (?, ?, ?, ?, ?)
            """,
            ("test-cluster", "2024-01-10T10:00:00", None, '{"v": 1}', "[]"),
        )
        db.conn.execute(
            """
            INSERT INTO cache_changes
            (cluster_name, changed_at, before_json, after_json, summary_json)
            VALUES (?, ?, ?, ?, ?)
            """,
            ("test-cluster", "2024-01-20T10:00:00", '{"v": 1}', '{"v": 2}', "[]"),
        )
        db.conn.commit()

        # Query for date between the two
        result = db.get_snapshot_at_date("test-cluster", "2024-01-15")
        assert result is not None
        assert result["after_json"] == '{"v": 1}'

        # Query for date after both
        result = db.get_snapshot_at_date("test-cluster", "2024-01-25")
        assert result is not None
        assert result["after_json"] == '{"v": 2}'

    def test_get_snapshot_at_date_no_match_before(self, db: CacheHistoryDB) -> None:
        """Test get_snapshot_at_date returns None if date is before all snapshots."""
        db.conn.execute(
            """
            INSERT INTO cache_changes
            (cluster_name, changed_at, before_json, after_json, summary_json)
            VALUES (?, ?, ?, ?, ?)
            """,
            ("test-cluster", "2024-01-15T10:00:00", None, '{"v": 1}', "[]"),
        )
        db.conn.commit()

        result = db.get_snapshot_at_date("test-cluster", "2024-01-01")
        assert result is None


class TestHistoryIntegration:
    """Integration tests for history tracking during cache operations."""

    @pytest.fixture
    def history_db(self, tmp_path: Path) -> CacheHistoryDB:
        """Create a test history database."""
        db_path = tmp_path / "test_history.db"
        return CacheHistoryDB(db_path=db_path)

    def test_initial_capture_records_history(self, history_db: CacheHistoryDB) -> None:
        """Test that first cache refresh records initial snapshot."""
        metadata = CachedClusterMetadata(
            cluster_name="test-cluster",
            nodes=[NodeInfo(name="node1", serial_number="123")],
        )

        # Simulate what refresh command does
        previous = history_db.get_latest_snapshot("test-cluster")
        assert previous is None

        changes = compute_diff(None, metadata)
        assert len(changes) > 0  # Initial capture has adds

        change_id = history_db.record_change(
            cluster_name="test-cluster",
            before_json=None,
            after_json=metadata.model_dump_json(),
            summary=changes,
        )
        assert change_id > 0

        # Verify history was recorded
        history_records = history_db.get_change_history("test-cluster")
        assert len(history_records) == 1
        assert history_records[0]["cluster_name"] == "test-cluster"

    def test_subsequent_refresh_with_changes(self, history_db: CacheHistoryDB) -> None:
        """Test that subsequent refresh with changes records diff."""
        # Initial state
        metadata_v1 = CachedClusterMetadata(
            cluster_name="test-cluster",
            nodes=[NodeInfo(name="node1", serial_number="123")],
        )
        history_db.record_change(
            cluster_name="test-cluster",
            before_json=None,
            after_json=metadata_v1.model_dump_json(),
            summary=compute_diff(None, metadata_v1),
        )

        # Updated state with changed serial
        metadata_v2 = CachedClusterMetadata(
            cluster_name="test-cluster",
            nodes=[NodeInfo(name="node1", serial_number="456")],
        )

        # Get previous snapshot
        latest = history_db.get_latest_snapshot("test-cluster")
        assert latest is not None

        # Parse previous metadata
        import json

        prev_data = json.loads(str(latest["after_json"]))
        prev_metadata = CachedClusterMetadata.model_validate(prev_data)

        # Compute diff
        changes = compute_diff(prev_metadata, metadata_v2)
        assert len(changes) > 0

        # Record the change
        history_db.record_change(
            cluster_name="test-cluster",
            before_json=prev_metadata.model_dump_json(),
            after_json=metadata_v2.model_dump_json(),
            summary=changes,
        )

        # Should now have 2 history entries
        assert history_db.get_history_count("test-cluster") == 2

        # Latest snapshot should be v2
        latest = history_db.get_latest_snapshot("test-cluster")
        assert latest is not None
        assert '"456"' in str(latest["after_json"])

    def test_refresh_without_changes_not_recorded(self, history_db: CacheHistoryDB) -> None:
        """Test that refresh with no changes doesn't add history entry."""
        metadata = CachedClusterMetadata(
            cluster_name="test-cluster",
            nodes=[NodeInfo(name="node1", serial_number="123")],
        )

        # Initial record
        history_db.record_change(
            cluster_name="test-cluster",
            before_json=None,
            after_json=metadata.model_dump_json(),
            summary=compute_diff(None, metadata),
        )

        # Simulate refresh with same metadata
        import json

        latest = history_db.get_latest_snapshot("test-cluster")
        assert latest is not None
        prev_data = json.loads(str(latest["after_json"]))
        prev_metadata = CachedClusterMetadata.model_validate(prev_data)

        # Identical metadata - no changes
        changes = compute_diff(prev_metadata, metadata)
        assert len(changes) == 0

        # Don't record if no changes (this is the logic in refresh.py)
        # Count should still be 1
        assert history_db.get_history_count("test-cluster") == 1


class TestHistoryCLI:
    """Tests for history CLI commands."""

    @pytest.fixture
    def runner(self) -> CliRunner:
        """Create a CLI runner."""
        return CliRunner()

    def test_history_list_no_config(self, runner: CliRunner) -> None:
        """Test history list fails without config directory."""
        result = runner.invoke(history, ["list"], obj={"config_dir": "nonexistent_config"})
        assert result.exit_code != 0
        assert "Configuration directory not found" in result.output

    def test_format_summary_brief_initial(self) -> None:
        """Test brief summary format for initial capture."""
        from pynetappfoundry.cli.commands.cache.history import _format_summary_brief

        # Empty summary means initial capture
        result = _format_summary_brief([])
        assert result == "Initial capture"

    def test_format_summary_brief_changes(self) -> None:
        """Test brief summary format with changes."""
        from pynetappfoundry.cli.commands.cache.history import _format_summary_brief

        summary: list[dict[str, object]] = [
            {"type": "added"},
            {"type": "added"},
            {"type": "removed"},
            {"type": "modified"},
            {"type": "modified"},
            {"type": "modified"},
        ]
        result = _format_summary_brief(summary)
        assert "+2" in result  # 2 added
        assert "-1" in result  # 1 removed
        assert "~3" in result  # 3 modified

    def test_snapshot_no_config(self, runner: CliRunner) -> None:
        """Test snapshot command fails without config directory."""
        result = runner.invoke(
            history,
            ["snapshot", "test-cluster", "--date", "2024-01-15"],
            obj={"config_dir": "nonexistent_config"},
        )
        assert result.exit_code != 0
        assert "Configuration directory not found" in result.output

    def test_display_snapshot_summary(self) -> None:
        """Test _display_snapshot_summary function."""
        from pynetappfoundry.cli.commands.cache.history import _display_snapshot_summary

        # Should not raise with valid data
        data: dict[str, object] = {
            "cluster_name": "test-cluster",
            "nodes": [{"name": "node1"}],
            "storage": {"aggregates": [], "volumes": [{"name": "vol1"}]},
            "network": {"interfaces": [], "ports": []},
            "svms": [],
        }
        # Just verify it doesn't raise
        _display_snapshot_summary(data)

    def test_display_snapshot_summary_empty(self) -> None:
        """Test _display_snapshot_summary with empty data."""
        from pynetappfoundry.cli.commands.cache.history import _display_snapshot_summary

        # Should handle empty/missing data gracefully
        data: dict[str, object] = {}
        _display_snapshot_summary(data)


class TestHistoryPreservation:
    """Tests verifying history is preserved through various operations."""

    @pytest.fixture
    def history_db(self, tmp_path: Path) -> CacheHistoryDB:
        """Create a test history database."""
        db_path = tmp_path / "test_preserve.db"
        return CacheHistoryDB(db_path=db_path)

    def test_history_survives_database_reopen(self, tmp_path: Path) -> None:
        """Test that history survives database close and reopen."""
        db_path = tmp_path / "reopen_test.db"

        # Create and populate
        db1 = CacheHistoryDB(db_path=db_path)
        db1.record_change(
            cluster_name="test-cluster",
            before_json=None,
            after_json='{"test": true}',
            summary=[{"type": "added", "entity": "test"}],
        )
        db1.close()

        # Reopen
        db2 = CacheHistoryDB(db_path=db_path)
        history_records = db2.get_change_history("test-cluster")
        assert len(history_records) == 1
        assert history_records[0]["summary"] == [{"type": "added", "entity": "test"}]
        db2.close()
