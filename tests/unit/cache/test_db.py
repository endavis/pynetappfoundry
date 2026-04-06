"""Tests for cache database operations."""

from __future__ import annotations

import json
import sqlite3
from datetime import UTC, datetime, timedelta
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from pydantic import BaseModel

from pynetappfoundry.cache import CachedClusterMetadata
from pynetappfoundry.cache.db import (
    ClusterMetadataDB,
    _model_to_row,
    _validate_cluster_name,
    realtime_attrs,
)
from pynetappfoundry.models.ontap.cloud.metadata.model import CloudMetadata
from pynetappfoundry.models.ontap.cluster.model import ClusterInfo
from pynetappfoundry.models.ontap.cluster.nodes.model import OntapNodeResponse
from pynetappfoundry.models.ontap.storage.volumes.model import OntapVolume


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
    def db(self) -> ClusterMetadataDB:
        """Create an in-memory test database."""
        return ClusterMetadataDB(db_path=":memory:")

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

    def test_clear_removes_from_all_tables(
        self, db: ClusterMetadataDB, sample_metadata: CachedClusterMetadata
    ) -> None:
        """clear() should remove rows from all model tables."""
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

    def test_list_field_json_round_trip(self, db: ClusterMetadataDB) -> None:
        """Sub-model list fields survive serialization round-trip."""
        from pynetappfoundry.models.ontap.cluster.nodes.model import (
            OntapNodeResponseClusterInterface2,
            OntapNodeResponseClusterInterface2Ip,
        )

        meta = CachedClusterMetadata(
            cluster_name="test-cluster",
            nodes=[
                OntapNodeResponse(
                    name="node1",
                    cluster_interfaces=[
                        OntapNodeResponseClusterInterface2(
                            name="e0a",
                            ip=OntapNodeResponseClusterInterface2Ip(address="10.0.0.1"),
                        ),
                    ],
                ),
            ],
        )
        db.set("test-cluster", meta)
        got = db.get("test-cluster")

        assert got is not None
        assert len(got.nodes[0].cluster_interfaces) == 1
        assert got.nodes[0].cluster_interfaces[0].name == "e0a"
        assert got.nodes[0].cluster_interfaces[0].ip.address == "10.0.0.1"

    def test_list_field_model_dump_uses_json_mode(self) -> None:
        """model_dump(mode='json') ensures non-JSON-native types serialize correctly.

        Without ``mode="json"``, ``model_dump()`` returns Python objects (e.g.
        ``datetime``) that ``json.dumps`` cannot handle.  The fix adds
        ``mode="json"`` so that list items with such types are converted to
        JSON-compatible primitives (e.g. ISO-8601 strings for datetimes).
        """

        class _Inner(BaseModel):
            ts: datetime
            label: str = ""

        class _Outer(BaseModel):
            items: list[_Inner] = []

        stamp = datetime(2025, 6, 15, 12, 0, 0, tzinfo=UTC)
        outer = _Outer(items=[_Inner(ts=stamp, label="a")])

        row = _model_to_row(outer, _Outer)

        # The 'items' column must be a valid JSON string
        parsed = json.loads(row["items"])
        assert isinstance(parsed, list)
        assert len(parsed) == 1
        # datetime should be serialized as an ISO-8601 string, not a raw object
        assert parsed[0]["ts"] == "2025-06-15T12:00:00Z"
        assert parsed[0]["label"] == "a"

    def test_dict_field_with_basemodel_values_serializes(self) -> None:
        """dict JSON columns containing BaseModel values must serialize.

        Defensive coverage for #483: ``_model_to_row`` falls through to
        ``json.dumps`` for dict-typed JSON columns. If a future model
        declares ``dict[str, SomeSubmodel]`` the encoder must handle the
        nested Pydantic instances rather than crashing with TypeError.
        """

        class _Inner(BaseModel):
            label: str = ""

        class _Outer(BaseModel):
            mapping: dict[str, _Inner] = {}

        outer = _Outer(mapping={"a": _Inner(label="hello")})

        row = _model_to_row(outer, _Outer)

        parsed = json.loads(row["mapping"])
        assert parsed == {"a": {"label": "hello"}}

    def test_extra_fields_with_basemodel_values_serialize(self) -> None:
        """Extra (``extra='allow'``) fields holding BaseModel values must serialize.

        Defensive coverage for #483: extras flow through ``_extra_json``
        unchecked. If a model accepted a Pydantic submodel as an extra
        attribute, the old encoder would have crashed.
        """

        class _Extra(BaseModel):
            kind: str = ""

        class _Outer(BaseModel):
            model_config = {"extra": "allow"}
            name: str = ""

        outer = _Outer(name="x", bonus=_Extra(kind="y"))  # type: ignore[call-arg]

        row = _model_to_row(outer, _Outer)

        parsed = json.loads(row["_extra_json"])
        assert parsed == {"bonus": {"kind": "y"}}

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
        from pynetappfoundry.models.ontap.storage.model import StorageInfo

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


class TestQueryWithFilters:
    """Tests for ClusterMetadataDB.query_with_filters()."""

    @pytest.fixture
    def db(self) -> ClusterMetadataDB:
        """Create an in-memory test database."""
        return ClusterMetadataDB(db_path=":memory:")

    @pytest.fixture
    def db_with_volumes(self, db: ClusterMetadataDB) -> ClusterMetadataDB:
        """Database with sample volume data including JSON fields."""
        from pynetappfoundry.models.ontap.storage.model import StorageInfo
        from pynetappfoundry.models.ontap.storage.volumes.model import OntapVolumeAutosize

        meta = CachedClusterMetadata(
            cluster_name="test-cluster",
            storage=StorageInfo(
                volumes=[
                    OntapVolume(
                        name="vol1",
                        uuid="11111111-1111-1111-1111-111111111111",
                        size=1073741824,
                        state="online",
                        autosize=OntapVolumeAutosize(
                            mode="grow_shrink",
                            grow_threshold=85,
                            maximum=2147483648,
                        ),
                    ),
                    OntapVolume(
                        name="vol2",
                        uuid="22222222-2222-2222-2222-222222222222",
                        size=536870912,
                        state="online",
                        autosize=OntapVolumeAutosize(
                            mode="off",
                            grow_threshold=0,
                            maximum=0,
                        ),
                    ),
                    OntapVolume(
                        name="vol3",
                        uuid="33333333-3333-3333-3333-333333333333",
                        size=2147483648,
                        state="offline",
                        autosize=OntapVolumeAutosize(
                            mode="grow_shrink",
                            grow_threshold=90,
                            maximum=4294967296,
                        ),
                    ),
                ],
            ),
        )
        db.set("test-cluster", meta)
        return db

    def test_filter_by_scalar_column(self, db_with_volumes: ClusterMetadataDB) -> None:
        """Filter by scalar column returns matching models."""
        results = db_with_volumes.query_with_filters(
            "test-cluster", "storage.volumes", ["name = 'vol1'"]
        )
        assert len(results) == 1
        assert results[0].name == "vol1"

    def test_filter_by_json_sub_field(self, db_with_volumes: ClusterMetadataDB) -> None:
        """Filter by JSON sub-field returns matching models."""
        results = db_with_volumes.query_with_filters(
            "test-cluster",
            "storage.volumes",
            ["autosize.mode = 'grow_shrink'"],
        )
        assert len(results) == 2
        names = {r.name for r in results}
        assert names == {"vol1", "vol3"}

    def test_filter_comparison_on_json_numeric(self, db_with_volumes: ClusterMetadataDB) -> None:
        """Filter with comparison on JSON numeric field."""
        results = db_with_volumes.query_with_filters(
            "test-cluster",
            "storage.volumes",
            ["autosize.grow_threshold >= 85"],
        )
        assert len(results) == 2
        names = {r.name for r in results}
        assert names == {"vol1", "vol3"}

    def test_multiple_filters_and(self, db_with_volumes: ClusterMetadataDB) -> None:
        """Multiple filters narrow results (AND logic)."""
        results = db_with_volumes.query_with_filters(
            "test-cluster",
            "storage.volumes",
            [
                "state = 'online'",
                "autosize.mode = 'grow_shrink'",
            ],
        )
        assert len(results) == 1
        assert results[0].name == "vol1"

    def test_no_matches_returns_empty(self, db_with_volumes: ClusterMetadataDB) -> None:
        """No matches returns empty list."""
        results = db_with_volumes.query_with_filters(
            "test-cluster",
            "storage.volumes",
            ["name = 'nonexistent'"],
        )
        assert results == []

    def test_invalid_model_name_raises(self, db_with_volumes: ClusterMetadataDB) -> None:
        """Invalid model name raises ValueError."""
        with pytest.raises(ValueError, match="Unknown model name"):
            db_with_volumes.query_with_filters(
                "test-cluster", "nonexistent.path", ["name = 'vol1'"]
            )

    def test_invalid_field_raises(self, db_with_volumes: ClusterMetadataDB) -> None:
        """Invalid field path raises ValueError."""
        with pytest.raises(ValueError, match="Unknown field"):
            db_with_volumes.query_with_filters("test-cluster", "storage.volumes", ["bogus = 'val'"])

    def test_empty_filters_returns_all(self, db_with_volumes: ClusterMetadataDB) -> None:
        """Empty filters list returns all rows for cluster."""
        results = db_with_volumes.query_with_filters("test-cluster", "storage.volumes", [])
        assert len(results) == 3

    def test_filter_by_size_greater_than(self, db_with_volumes: ClusterMetadataDB) -> None:
        """Filter by scalar numeric comparison."""
        results = db_with_volumes.query_with_filters(
            "test-cluster",
            "storage.volumes",
            ["size > 1073741824"],
        )
        assert len(results) == 1
        assert results[0].name == "vol3"

    def test_in_operator(self, db_with_volumes: ClusterMetadataDB) -> None:
        """Filter with in operator."""
        results = db_with_volumes.query_with_filters(
            "test-cluster",
            "storage.volumes",
            ["state in ('online', 'offline')"],
        )
        assert len(results) == 3

    def test_inequality_json_field(self, db_with_volumes: ClusterMetadataDB) -> None:
        """Filter JSON sub-field with inequality."""
        results = db_with_volumes.query_with_filters(
            "test-cluster",
            "storage.volumes",
            ["autosize.mode != 'off'"],
        )
        assert len(results) == 2
        names = {r.name for r in results}
        assert names == {"vol1", "vol3"}

    def test_invalid_cluster_name_raises(self, db_with_volumes: ClusterMetadataDB) -> None:
        """Invalid cluster name raises ValueError."""
        with pytest.raises(ValueError, match="Invalid cluster name"):
            db_with_volumes.query_with_filters("123invalid", "storage.volumes", ["name = 'vol1'"])


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

        # Open with current code — should trigger migration v1→v2→v3→v4
        db = ClusterMetadataDB(db_path=db_path)

        # v4 migration drops and recreates all model tables (nested model
        # refactoring changed column names), so cached data is lost.
        got = db.get("migrated-cluster")
        assert got is None

        # Verify envelope table no longer has metadata_json
        cursor = db.conn.execute("PRAGMA table_info(cluster_metadata)")
        columns = {row[1] for row in cursor.fetchall()}
        assert "metadata_json" not in columns
        assert "cached_at" in columns

        db.close()


class TestClusterMetadataDBMigrationV3:
    """Tests for v2 → v3 migration (drop _uuid_index table)."""

    def test_migration_v2_to_v3(self, tmp_path: Path) -> None:
        """Create a v2 database with _uuid_index data, open with v3 code, verify table is gone."""
        db_path = tmp_path / "migrate_v3.db"

        # Create a v2 database manually
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row

        # Envelope table
        conn.execute(
            "CREATE TABLE cluster_metadata ("
            "  cluster_name TEXT PRIMARY KEY,"
            "  cached_at TEXT NOT NULL,"
            "  cache_version TEXT NOT NULL"
            ")"
        )

        # _uuid_index table (the one v3 removes)
        conn.execute(
            "CREATE TABLE _uuid_index ("
            "  cluster_name TEXT NOT NULL,"
            "  uuid TEXT NOT NULL,"
            "  table_name TEXT NOT NULL,"
            "  PRIMARY KEY (cluster_name, uuid)"
            ")"
        )
        conn.execute(
            "INSERT INTO _uuid_index (cluster_name, uuid, table_name) VALUES (?, ?, ?)",
            ("test-cluster", "aaaa-bbbb-cccc", "ontapnoderesponse"),
        )

        # Schema version = 2
        conn.execute("CREATE TABLE _schema_version (version INTEGER NOT NULL)")
        conn.execute("INSERT INTO _schema_version (version) VALUES (2)")

        # Insert envelope row
        conn.execute(
            "INSERT INTO cluster_metadata (cluster_name, cached_at, cache_version) "
            "VALUES (?, ?, ?)",
            ("test-cluster", "2025-01-01T00:00:00+00:00", "1.0.0"),
        )

        # Create per-model tables so the v3 DB can reconstruct metadata.
        # We need at least the tables that CachedClusterMetadata expects.
        # Open a temporary in-memory v3 DB to discover table DDL, then replay.
        from pynetappfoundry.cache.db_schema import (
            _ensure_registry,
            generate_cluster_name_index_ddl,
            generate_table_ddl,
            generate_uuid_column_index_ddl,
        )

        registry = _ensure_registry()
        for spec in registry.values():
            ddl = generate_table_ddl(spec.table_name, spec.model_class)
            conn.execute(ddl)
            conn.execute(generate_cluster_name_index_ddl(spec.table_name))
            if spec.has_uuid:
                conn.execute(generate_uuid_column_index_ddl(spec.table_name))

        conn.commit()
        conn.close()

        # Open with current code — should trigger migration v2→v3→v4
        db = ClusterMetadataDB(db_path=db_path)

        # Verify _uuid_index table is gone (dropped in v3)
        cursor = db.conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='_uuid_index'"
        )
        assert cursor.fetchone() is None

        # Verify schema version is 4 (v4 drops/recreates tables)
        cursor = db.conn.execute("SELECT version FROM _schema_version")
        assert cursor.fetchone()[0] == 4

        # v4 clears envelope data (nested model refactoring)
        got = db.get("test-cluster")
        assert got is None

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

    def test_close(self) -> None:
        """Test closing database connection."""
        db = ClusterMetadataDB(db_path=":memory:")
        db.close()
        # Attempting operations after close should fail
        with pytest.raises(sqlite3.ProgrammingError):
            db.list_clusters()


class TestModelToRowExclude:
    """Tests for _model_to_row exclude parameter."""

    def test_excludes_fields_in_exclude_set(self) -> None:
        """_model_to_row skips fields listed in the exclude frozenset."""

        class _Sample(BaseModel):
            name: str = ""
            value: int = 0
            metric: float = 0.0

        instance = _Sample(name="test", value=42, metric=3.14)
        row = _model_to_row(instance, _Sample, frozenset({"metric"}))

        assert "name" in row
        assert "value" in row
        assert "metric" not in row

    def test_includes_all_fields_when_exclude_empty(self) -> None:
        """_model_to_row includes all fields when exclude is empty (backward compat)."""

        class _Sample2(BaseModel):
            name: str = ""
            value: int = 0

        instance = _Sample2(name="test", value=42)
        row = _model_to_row(instance, _Sample2, frozenset())

        assert "name" in row
        assert "value" in row
        assert row["name"] == "test"
        assert row["value"] == 42

    def test_includes_all_fields_when_exclude_not_provided(self) -> None:
        """_model_to_row includes all fields when exclude defaults."""

        class _Sample3(BaseModel):
            name: str = ""
            count: int = 0

        instance = _Sample3(name="hello", count=7)
        row = _model_to_row(instance, _Sample3)

        assert "name" in row
        assert "count" in row

    def test_excludes_multiple_fields(self) -> None:
        """_model_to_row can exclude multiple fields at once."""

        class _Multi(BaseModel):
            keep: str = ""
            drop_a: int = 0
            drop_b: float = 0.0

        instance = _Multi(keep="yes", drop_a=1, drop_b=2.0)
        row = _model_to_row(instance, _Multi, frozenset({"drop_a", "drop_b"}))

        assert "keep" in row
        assert "drop_a" not in row
        assert "drop_b" not in row


class TestRealtimeAttrs:
    """Tests for realtime_attrs helper."""

    def test_returns_realtime_cache_attrs_for_mapped_model(self) -> None:
        """realtime_attrs returns correct field names for models with realtime mappings."""
        # Import the mapping module to trigger register_mapping() calls
        import pynetappfoundry.cache.ontap.network.fc.ports.mapping  # noqa: F401
        from pynetappfoundry.models.ontap.network.fc.ports.model import OntapFcPort

        # Clear cache to ensure fresh lookup
        realtime_attrs.cache_clear()

        result = realtime_attrs(OntapFcPort)

        assert isinstance(result, frozenset)
        assert len(result) > 0
        # These are known realtime fields from ports.toml (dotted paths with nested models)
        assert "metric.duration" in result
        assert "metric.iops.total" in result

    def test_returns_empty_frozenset_for_unmapped_model(self) -> None:
        """realtime_attrs returns empty frozenset for models without mappings."""
        realtime_attrs.cache_clear()

        # CachedClusterMetadata is a container model with no TypeMapping
        result = realtime_attrs(CachedClusterMetadata)

        assert isinstance(result, frozenset)
        assert len(result) == 0

    def test_returns_empty_frozenset_for_model_without_realtime_fields(self) -> None:
        """realtime_attrs returns empty frozenset when mapping has no realtime fields."""
        realtime_attrs.cache_clear()

        # Create a mock mapping with no realtime fields
        mock_mapping = MagicMock()
        mock_mapping.realtime_fields.return_value = ()

        class _NoRealtime(BaseModel):
            name: str = ""

        with patch("pynetappfoundry.cache._registry.model_registry") as mock_registry:
            mock_registry.get_mapping.return_value = mock_mapping
            result = realtime_attrs(_NoRealtime)

        assert isinstance(result, frozenset)
        assert len(result) == 0

    def test_caches_result_per_model_class(self) -> None:
        """realtime_attrs caches results (functools.cache)."""
        realtime_attrs.cache_clear()

        # First call populates cache
        result1 = realtime_attrs(CachedClusterMetadata)
        result2 = realtime_attrs(CachedClusterMetadata)

        assert result1 is result2
        # Verify cache was used
        info = realtime_attrs.cache_info()
        assert info.hits >= 1
