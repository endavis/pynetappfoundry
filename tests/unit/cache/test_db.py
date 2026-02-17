"""Tests for cache database operations."""

from __future__ import annotations

import sqlite3
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest

from pynetappfoundry.cache import CachedClusterMetadata
from pynetappfoundry.cache.cloud.metadata.model import CloudMetadata
from pynetappfoundry.cache.cluster.model import ClusterInfo
from pynetappfoundry.cache.cluster.nodes.model import OntapNodeResponse
from pynetappfoundry.cache.db import ClusterMetadataDB, _validate_cluster_name
from pynetappfoundry.cache.storage.volumes.model import OntapVolume


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
                OntapNodeResponse(name="node1", serial_number="123"),
                OntapNodeResponse(name="node2", serial_number="456"),
            ],
        )

    def test_init_creates_tables(self, db: ClusterMetadataDB) -> None:
        """Test that initialization creates required tables."""
        cursor = db.conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = {row["name"] for row in cursor.fetchall()}
        assert "cluster_metadata" in tables
        assert "_schema_version" in tables
        assert "_uuid_index" in tables

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

    # ------------------------------------------------------------------
    # New v2 tests
    # ------------------------------------------------------------------

    def test_set_decomposes_to_tables(
        self, db: ClusterMetadataDB, sample_metadata: CachedClusterMetadata
    ) -> None:
        """Verify rows exist in per-model tables after set()."""
        db.set("test-cluster", sample_metadata)

        # Check nodes table
        cursor = db.conn.execute(
            "SELECT * FROM ontapnoderesponse WHERE cluster_name = ?",
            ("test-cluster",),
        )
        rows = cursor.fetchall()
        assert len(rows) == 2

        # Check cloud table
        cursor = db.conn.execute(
            "SELECT * FROM cloudmetadata WHERE cluster_name = ?",
            ("test-cluster",),
        )
        rows = cursor.fetchall()
        assert len(rows) == 1

        # Check envelope table has no metadata_json
        cursor = db.conn.execute(
            "SELECT * FROM cluster_metadata WHERE cluster_name = ?",
            ("test-cluster",),
        )
        row = dict(cursor.fetchone())
        assert "metadata_json" not in row
        assert "cached_at" in row
        assert "cache_version" in row

    def test_get_reconstructs_metadata(
        self, db: ClusterMetadataDB, sample_metadata: CachedClusterMetadata
    ) -> None:
        """Round-trip set() → get() preserves all data."""
        db.set("test-cluster", sample_metadata)
        got = db.get("test-cluster")

        assert got is not None
        assert got.cluster_name == sample_metadata.cluster_name
        assert got.cluster.ontap_version == sample_metadata.cluster.ontap_version
        assert got.cluster.cluster_name == sample_metadata.cluster.cluster_name
        assert len(got.nodes) == len(sample_metadata.nodes)
        assert got.nodes[0].name == sample_metadata.nodes[0].name
        assert got.nodes[1].serial_number == sample_metadata.nodes[1].serial_number
        assert len(got.cloud) == len(sample_metadata.cloud)
        assert got.cloud[0].provider == sample_metadata.cloud[0].provider

    def test_query_model_basic(self, db: ClusterMetadataDB) -> None:
        """query_model returns filtered results."""
        meta = CachedClusterMetadata(
            cluster_name="test-cluster",
            nodes=[
                OntapNodeResponse(name="node1", serial_number="AAA"),
                OntapNodeResponse(name="node2", serial_number="BBB"),
            ],
        )
        db.set("test-cluster", meta)

        results = db.query_model("test-cluster", "nodes", name="node1")
        assert len(results) == 1
        assert results[0].name == "node1"
        assert results[0].serial_number == "AAA"

    def test_query_model_no_filter(self, db: ClusterMetadataDB) -> None:
        """query_model without filters returns all rows."""
        meta = CachedClusterMetadata(
            cluster_name="test-cluster",
            nodes=[
                OntapNodeResponse(name="n1"),
                OntapNodeResponse(name="n2"),
                OntapNodeResponse(name="n3"),
            ],
        )
        db.set("test-cluster", meta)

        results = db.query_model("test-cluster", "nodes")
        assert len(results) == 3

    def test_query_model_unknown_model(self, db: ClusterMetadataDB) -> None:
        """query_model raises for unknown model name."""
        with pytest.raises(ValueError, match="Unknown model name"):
            db.query_model("test-cluster", "nonexistent.path")

    def test_query_model_unknown_field(self, db: ClusterMetadataDB) -> None:
        """query_model raises for unknown filter field."""
        with pytest.raises(ValueError, match="Unknown field"):
            db.query_model("test-cluster", "nodes", bogus_field="x")

    def test_export_import_round_trip(
        self, db: ClusterMetadataDB, sample_metadata: CachedClusterMetadata
    ) -> None:
        """export_json → import_json preserves data."""
        db.set("test-cluster", sample_metadata)
        exported = db.export_json("test-cluster")
        assert exported is not None

        db.clear("test-cluster")
        assert db.get("test-cluster") is None

        db.import_json("test-cluster", exported)
        got = db.get("test-cluster")
        assert got is not None
        assert got.cluster.ontap_version == "9.14.1"
        assert len(got.nodes) == 2

    def test_export_nonexistent(self, db: ClusterMetadataDB) -> None:
        """export_json returns None for missing cluster."""
        assert db.export_json("nonexistent") is None

    def test_uuid_index_populated(self, db: ClusterMetadataDB) -> None:
        """_uuid_index table should have entries for models with non-empty uuids."""
        meta = CachedClusterMetadata(
            cluster_name="test-cluster",
            nodes=[
                OntapNodeResponse(
                    name="node1",
                    uuid="12345678-1234-1234-1234-123456789abc",
                ),
            ],
        )
        db.set("test-cluster", meta)

        cursor = db.conn.execute(
            "SELECT * FROM _uuid_index WHERE cluster_name = ?",
            ("test-cluster",),
        )
        rows = [dict(r) for r in cursor.fetchall()]
        assert len(rows) >= 1
        uuids = {r["uuid"] for r in rows}
        assert "12345678-1234-1234-1234-123456789abc" in uuids

    def test_uuid_index_skips_empty(self, db: ClusterMetadataDB) -> None:
        """_uuid_index should not include entries with empty uuid."""
        meta = CachedClusterMetadata(
            cluster_name="test-cluster",
            nodes=[OntapNodeResponse(name="node1")],  # uuid defaults to ""
        )
        db.set("test-cluster", meta)

        cursor = db.conn.execute(
            "SELECT * FROM _uuid_index WHERE cluster_name = ?",
            ("test-cluster",),
        )
        rows = cursor.fetchall()
        # No entries because uuid is empty
        assert len(rows) == 0

    def test_clear_removes_from_all_tables(
        self, db: ClusterMetadataDB, sample_metadata: CachedClusterMetadata
    ) -> None:
        """clear() should remove rows from all model tables and uuid_index."""
        db.set("test-cluster", sample_metadata)
        db.clear("test-cluster")

        # Check model tables are empty
        cursor = db.conn.execute(
            "SELECT COUNT(*) FROM ontapnoderesponse WHERE cluster_name = ?",
            ("test-cluster",),
        )
        assert cursor.fetchone()[0] == 0

        cursor = db.conn.execute(
            "SELECT COUNT(*) FROM cloudmetadata WHERE cluster_name = ?",
            ("test-cluster",),
        )
        assert cursor.fetchone()[0] == 0

        cursor = db.conn.execute(
            "SELECT COUNT(*) FROM _uuid_index WHERE cluster_name = ?",
            ("test-cluster",),
        )
        assert cursor.fetchone()[0] == 0

    def test_list_field_json_round_trip(self, db: ClusterMetadataDB) -> None:
        """Sub-model list fields survive serialization round-trip."""
        from pynetappfoundry.cache.cluster.nodes.model import (
            OntapNodeResponseClusterInterface,
        )

        meta = CachedClusterMetadata(
            cluster_name="test-cluster",
            nodes=[
                OntapNodeResponse(
                    name="node1",
                    cluster_interfaces=[
                        OntapNodeResponseClusterInterface(
                            cluster_interfaces_name="e0a",
                            cluster_interfaces_ip_address="10.0.0.1",
                        ),
                    ],
                ),
            ],
        )
        db.set("test-cluster", meta)
        got = db.get("test-cluster")

        assert got is not None
        assert len(got.nodes[0].cluster_interfaces) == 1
        assert got.nodes[0].cluster_interfaces[0].cluster_interfaces_name == "e0a"
        assert got.nodes[0].cluster_interfaces[0].cluster_interfaces_ip_address == "10.0.0.1"

    def test_extra_fields_preserved(self, db: ClusterMetadataDB) -> None:
        """Extra fields (extra='allow') round-trip via _extra_json."""
        meta = CachedClusterMetadata(
            cluster_name="test-cluster",
            cloud=[CloudMetadata(provider="AWS", **{"future_field": "hello"})],
        )
        db.set("test-cluster", meta)
        got = db.get("test-cluster")

        assert got is not None
        assert got.cloud[0].future_field == "hello"  # type: ignore[attr-defined]

    def test_set_updates_clears_old_model_data(self, db: ClusterMetadataDB) -> None:
        """Updating a cluster replaces all model rows, not appends."""
        meta1 = CachedClusterMetadata(
            cluster_name="test-cluster",
            nodes=[
                OntapNodeResponse(name="node1"),
                OntapNodeResponse(name="node2"),
            ],
        )
        db.set("test-cluster", meta1)

        # Update with fewer nodes
        meta2 = CachedClusterMetadata(
            cluster_name="test-cluster",
            nodes=[OntapNodeResponse(name="node3")],
        )
        db.set("test-cluster", meta2)

        got = db.get("test-cluster")
        assert got is not None
        assert len(got.nodes) == 1
        assert got.nodes[0].name == "node3"

    def test_multiple_clusters_isolated(self, db: ClusterMetadataDB) -> None:
        """Data for different clusters is isolated."""
        meta1 = CachedClusterMetadata(
            cluster_name="cluster-a",
            nodes=[OntapNodeResponse(name="nodeA")],
        )
        meta2 = CachedClusterMetadata(
            cluster_name="cluster-b",
            nodes=[OntapNodeResponse(name="nodeB1"), OntapNodeResponse(name="nodeB2")],
        )
        db.set("clusterA", meta1)
        db.set("clusterB", meta2)

        got_a = db.get("clusterA")
        got_b = db.get("clusterB")
        assert got_a is not None
        assert got_b is not None
        assert len(got_a.nodes) == 1
        assert len(got_b.nodes) == 2
        assert got_a.nodes[0].name == "nodeA"

    def test_storage_volumes_round_trip(self, db: ClusterMetadataDB) -> None:
        """Large models like OntapVolume serialize and deserialize correctly."""
        from pynetappfoundry.cache.storage.model import StorageInfo

        meta = CachedClusterMetadata(
            cluster_name="test-cluster",
            storage=StorageInfo(
                volumes=[
                    OntapVolume(
                        name="vol1",
                        uuid="11111111-1111-1111-1111-111111111111",
                        size=1073741824,
                        state="online",
                    ),
                ],
            ),
        )
        db.set("test-cluster", meta)
        got = db.get("test-cluster")

        assert got is not None
        assert len(got.storage.volumes) == 1
        assert got.storage.volumes[0].name == "vol1"
        assert got.storage.volumes[0].uuid == "11111111-1111-1111-1111-111111111111"
        assert got.storage.volumes[0].size == 1073741824


class TestClusterMetadataDBMigration:
    """Tests for v1 → v2 migration."""

    def test_migration_v1_to_v2(self, tmp_path: Path) -> None:
        """Create a v1 database, then open with v2 code and verify data."""
        db_path = tmp_path / "migrate.db"

        # Create v1 database manually
        conn = sqlite3.connect(db_path)
        conn.execute(
            "CREATE TABLE cluster_metadata ("
            "  cluster_name TEXT PRIMARY KEY,"
            "  cached_at TEXT NOT NULL,"
            "  cache_version TEXT NOT NULL,"
            "  metadata_json TEXT NOT NULL"
            ")"
        )
        conn.execute("CREATE TABLE _schema_version (version INTEGER NOT NULL)")
        conn.execute("INSERT INTO _schema_version (version) VALUES (1)")

        # Insert a v1 row
        meta = CachedClusterMetadata(
            cluster_name="migrated-cluster",
            cloud=[CloudMetadata(provider="GCP", region="us-central1")],
            cluster=ClusterInfo(cluster_name="migrated-cluster", ontap_version="9.13.1"),
            nodes=[OntapNodeResponse(name="mnode1", serial_number="M001")],
        )
        conn.execute(
            "INSERT INTO cluster_metadata (cluster_name, cached_at, cache_version, metadata_json) "
            "VALUES (?, ?, ?, ?)",
            (
                "migrated-cluster",
                meta.cached_at.isoformat(),
                meta.cache_version,
                meta.model_dump_json(),
            ),
        )
        conn.commit()
        conn.close()

        # Open with v2 code — should trigger migration
        db = ClusterMetadataDB(db_path=db_path)

        # Verify data survived migration
        got = db.get("migrated-cluster")
        assert got is not None
        assert got.cluster_name == "migrated-cluster"
        assert got.cloud[0].provider == "GCP"
        assert got.cluster.ontap_version == "9.13.1"
        assert len(got.nodes) == 1
        assert got.nodes[0].name == "mnode1"

        # Verify envelope table no longer has metadata_json
        cursor = db.conn.execute("PRAGMA table_info(cluster_metadata)")
        columns = {row[1] for row in cursor.fetchall()}
        assert "metadata_json" not in columns
        assert "cached_at" in columns

        db.close()


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
        db_path = tmp_path / "close_test.db"
        db = ClusterMetadataDB(db_path=db_path)
        db.close()
        # Attempting operations after close should fail
        with pytest.raises(sqlite3.ProgrammingError):
            db.list_clusters()
