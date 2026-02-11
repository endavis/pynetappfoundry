"""Tests for cache database operations."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest

from pynetappfoundry.cache import (
    CachedClusterMetadata,
    CloudMetadata,
    ClusterInfo,
    NodeInfo,
)
from pynetappfoundry.cache.db import ClusterMetadataDB, _validate_cluster_name


class TestValidateClusterName:
    """Tests for cluster name validation."""

    def test_valid_names(self) -> None:
        """Test valid cluster names pass validation."""
        valid_names = [
            "cluster1",
            "my-cluster",
            "cluster_prod",
            "CLUSTER-PROD-01",
            "a" * 128,  # Max length
        ]
        for name in valid_names:
            _validate_cluster_name(name)  # Should not raise

    def test_invalid_names(self) -> None:
        """Test invalid cluster names raise ValueError."""
        invalid_names = [
            "123cluster",  # Starts with number
            "_cluster",  # Starts with underscore
            "-cluster",  # Starts with hyphen
            "cluster.name",  # Contains period
            "cluster name",  # Contains space
            "cluster;drop",  # Contains semicolon
            "",  # Empty
            "a" * 129,  # Too long
        ]
        for name in invalid_names:
            with pytest.raises(ValueError, match="Invalid cluster name"):
                _validate_cluster_name(name)


class TestClusterMetadataDB:
    """Tests for ClusterMetadataDB class."""

    @pytest.fixture
    def db(self, tmp_path: Path) -> ClusterMetadataDB:
        """Create a test database."""
        db_path = tmp_path / "test_cache.db"
        return ClusterMetadataDB(db_path=db_path)

    @pytest.fixture
    def sample_metadata(self) -> CachedClusterMetadata:
        """Create sample metadata for testing."""
        return CachedClusterMetadata(
            cluster_name="test-cluster",
            cloud=[CloudMetadata(provider="AWS", region="us-east-1")],
            cluster=ClusterInfo(
                cluster_name="test-cluster",
                ontap_version="9.14.1",
            ),
            nodes=[
                NodeInfo(name="node1", serial_number="123"),
                NodeInfo(name="node2", serial_number="456"),
            ],
        )

    def test_init_creates_tables(self, db: ClusterMetadataDB) -> None:
        """Test that initialization creates required tables."""
        cursor = db.conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = {row["name"] for row in cursor.fetchall()}
        assert "cluster_metadata" in tables
        assert "_schema_version" in tables

    def test_set_and_get(
        self, db: ClusterMetadataDB, sample_metadata: CachedClusterMetadata
    ) -> None:
        """Test storing and retrieving metadata."""
        db.set("test-cluster", sample_metadata)
        retrieved = db.get("test-cluster")

        assert retrieved is not None
        assert retrieved.cluster_name == "test-cluster"
        assert retrieved.cloud[0].provider == "AWS"
        assert retrieved.cluster.ontap_version == "9.14.1"
        assert len(retrieved.nodes) == 2

    def test_get_nonexistent(self, db: ClusterMetadataDB) -> None:
        """Test getting nonexistent cluster returns None."""
        result = db.get("nonexistent")
        assert result is None

    def test_set_updates_existing(
        self, db: ClusterMetadataDB, sample_metadata: CachedClusterMetadata
    ) -> None:
        """Test that set updates existing entry."""
        db.set("test-cluster", sample_metadata)

        # Update with new metadata
        updated_metadata = CachedClusterMetadata(
            cluster_name="test-cluster",
            cloud=[CloudMetadata(provider="Azure", region="eastus")],
        )
        db.set("test-cluster", updated_metadata)

        retrieved = db.get("test-cluster")
        assert retrieved is not None
        assert retrieved.cloud[0].provider == "Azure"
        assert retrieved.cloud[0].region == "eastus"

    def test_clear_specific_cluster(
        self, db: ClusterMetadataDB, sample_metadata: CachedClusterMetadata
    ) -> None:
        """Test clearing specific cluster cache."""
        db.set("cluster1", sample_metadata)
        db.set("cluster2", sample_metadata)

        deleted = db.clear("cluster1")
        assert deleted == 1

        assert db.get("cluster1") is None
        assert db.get("cluster2") is not None

    def test_clear_all(self, db: ClusterMetadataDB, sample_metadata: CachedClusterMetadata) -> None:
        """Test clearing all cached data."""
        db.set("cluster1", sample_metadata)
        db.set("cluster2", sample_metadata)

        deleted = db.clear()
        assert deleted == 2

        assert db.get("cluster1") is None
        assert db.get("cluster2") is None

    def test_clear_nonexistent(self, db: ClusterMetadataDB) -> None:
        """Test clearing nonexistent cluster returns 0."""
        deleted = db.clear("nonexistent")
        assert deleted == 0

    def test_is_stale_fresh(
        self, db: ClusterMetadataDB, sample_metadata: CachedClusterMetadata
    ) -> None:
        """Test is_stale returns False for fresh cache."""
        db.set("test-cluster", sample_metadata)
        result = db.is_stale("test-cluster", ttl_days=30)
        assert result is False

    def test_is_stale_old(self, db: ClusterMetadataDB) -> None:
        """Test is_stale returns True for old cache."""
        old_time = datetime.now(UTC) - timedelta(days=35)
        old_metadata = CachedClusterMetadata(
            cluster_name="old-cluster",
            cached_at=old_time,
        )
        db.set("old-cluster", old_metadata)

        result = db.is_stale("old-cluster", ttl_days=30)
        assert result is True

    def test_is_stale_nonexistent(self, db: ClusterMetadataDB) -> None:
        """Test is_stale returns None for nonexistent cluster."""
        result = db.is_stale("nonexistent", ttl_days=30)
        assert result is None

    def test_list_clusters_empty(self, db: ClusterMetadataDB) -> None:
        """Test listing clusters when empty."""
        clusters = db.list_clusters()
        assert clusters == []

    def test_list_clusters(
        self, db: ClusterMetadataDB, sample_metadata: CachedClusterMetadata
    ) -> None:
        """Test listing cached clusters."""
        db.set("cluster1", sample_metadata)
        db.set("cluster2", sample_metadata)

        clusters = db.list_clusters()
        assert len(clusters) == 2
        names = {c["cluster_name"] for c in clusters}
        assert names == {"cluster1", "cluster2"}

        # Check fields
        for cluster in clusters:
            assert "cluster_name" in cluster
            assert "cached_at" in cluster
            assert "cache_version" in cluster

    def test_get_status(
        self, db: ClusterMetadataDB, sample_metadata: CachedClusterMetadata
    ) -> None:
        """Test getting cache status."""
        db.set("fresh-cluster", sample_metadata)

        old_metadata = CachedClusterMetadata(
            cluster_name="old-cluster",
            cached_at=datetime.now(UTC) - timedelta(days=35),
        )
        db.set("old-cluster", old_metadata)

        status = db.get_status(ttl_days=30)
        assert len(status) == 2

        status_by_name = {s["cluster_name"]: s for s in status}

        assert status_by_name["fresh-cluster"]["is_stale"] is False
        assert status_by_name["old-cluster"]["is_stale"] is True

    def test_context_manager(self, tmp_path: Path) -> None:
        """Test using database as context manager."""
        db_path = tmp_path / "context_test.db"
        with ClusterMetadataDB(db_path=db_path) as db:
            metadata = CachedClusterMetadata(cluster_name="test")
            db.set("test", metadata)
            assert db.get("test") is not None
        # Connection should be closed after context exit

    def test_invalid_cluster_name_on_get(self, db: ClusterMetadataDB) -> None:
        """Test that invalid cluster name raises error on get."""
        with pytest.raises(ValueError, match="Invalid cluster name"):
            db.get("123invalid")

    def test_invalid_cluster_name_on_set(
        self, db: ClusterMetadataDB, sample_metadata: CachedClusterMetadata
    ) -> None:
        """Test that invalid cluster name raises error on set."""
        with pytest.raises(ValueError, match="Invalid cluster name"):
            db.set("123invalid", sample_metadata)

    def test_invalid_cluster_name_on_clear(self, db: ClusterMetadataDB) -> None:
        """Test that invalid cluster name raises error on clear."""
        with pytest.raises(ValueError, match="Invalid cluster name"):
            db.clear("123invalid")


class TestClusterMetadataDBInitialization:
    """Tests for database initialization options."""

    def test_init_with_db_path(self, tmp_path: Path) -> None:
        """Test initializing with direct db_path."""
        db_path = tmp_path / "direct.db"
        db = ClusterMetadataDB(db_path=db_path)
        assert db.db_path == db_path
        db.close()

    def test_init_requires_path_or_config(self) -> None:
        """Test that either db_path or config must be provided."""
        with pytest.raises(ValueError, match="Either db_path or config"):
            ClusterMetadataDB()

    def test_close(self, tmp_path: Path) -> None:
        """Test closing database connection."""
        import sqlite3

        db_path = tmp_path / "close_test.db"
        db = ClusterMetadataDB(db_path=db_path)
        db.close()
        # Attempting operations after close should fail
        with pytest.raises(sqlite3.ProgrammingError):
            db.list_clusters()
