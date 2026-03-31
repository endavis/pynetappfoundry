"""Tests for LazyClusterMetadata lazy-loading proxy."""

from __future__ import annotations

import sqlite3
import uuid
from datetime import UTC, datetime, timedelta
from typing import Any
from unittest.mock import patch

import pytest

from pynetappfoundry.cache import CachedClusterMetadata, LazyClusterMetadata
from pynetappfoundry.cache._lazy import _DATA_FIELDS
from pynetappfoundry.cache.db import ClusterMetadataDB
from pynetappfoundry.models.ontap.cloud.metadata.model import CloudMetadata
from pynetappfoundry.models.ontap.cluster.model import ClusterInfo
from pynetappfoundry.models.ontap.cluster.nodes.model import OntapNodeResponse
from pynetappfoundry.models.ontap.storage.model import StorageInfo
from pynetappfoundry.models.ontap.storage.volumes.model import OntapVolume


@pytest.fixture
def db_path() -> str:
    """Return a unique shared in-memory DB URI for test isolation."""
    unique = uuid.uuid4().hex[:8]
    return f"file:test_lazy_{unique}?mode=memory&cache=shared"


@pytest.fixture
def db(db_path: str) -> ClusterMetadataDB:
    """Create an in-memory test database."""
    return ClusterMetadataDB(db_path=db_path)


@pytest.fixture
def sample_metadata() -> CachedClusterMetadata:
    """Create sample metadata with data in multiple field groups."""
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


@pytest.fixture
def populated_db(
    db: ClusterMetadataDB,
    sample_metadata: CachedClusterMetadata,
) -> ClusterMetadataDB:
    """Database with sample data already stored."""
    db.set("test-cluster", sample_metadata)
    return db


class TestEnvelopeFields:
    """Envelope fields are available without DB access."""

    def test_cluster_name_immediate(self, populated_db: ClusterMetadataDB) -> None:
        """cluster_name is available without loading data fields."""
        lazy = populated_db.get_lazy("test-cluster")
        assert lazy is not None
        assert lazy.cluster_name == "test-cluster"

    def test_cached_at_immediate(self, populated_db: ClusterMetadataDB) -> None:
        """cached_at is available without loading data fields."""
        lazy = populated_db.get_lazy("test-cluster")
        assert lazy is not None
        assert lazy.cached_at is not None
        assert len(lazy.cached_at) > 0

    def test_cache_version_immediate(self, populated_db: ClusterMetadataDB) -> None:
        """cache_version is available without loading data fields."""
        lazy = populated_db.get_lazy("test-cluster")
        assert lazy is not None
        assert lazy.cache_version is not None


class TestLazyLoading:
    """Data fields load lazily from the database."""

    def test_lazy_loads_only_accessed_field(
        self,
        populated_db: ClusterMetadataDB,
        db_path: str,
    ) -> None:
        """Accessing .cloud queries only cloud-related registry entries."""
        lazy = populated_db.get_lazy("test-cluster")
        assert lazy is not None

        from pynetappfoundry.cache.db import _query_registry_subset

        queried_paths: list[str] = []
        original_fn = _query_registry_subset

        def tracking_query(conn: Any, cluster_name: str, registry_subset: dict[str, Any]) -> Any:
            queried_paths.extend(registry_subset.keys())
            return original_fn(conn, cluster_name, registry_subset)

        with patch("pynetappfoundry.cache.db._query_registry_subset", tracking_query):
            _ = lazy.cloud

        assert len(queried_paths) > 0
        # Only cloud-related paths should be queried
        for path in queried_paths:
            assert path == "cloud" or path.startswith("cloud."), (
                f"Unexpected registry path queried: {path}"
            )

    def test_lazy_does_not_load_unaccessed_fields(
        self,
        populated_db: ClusterMetadataDB,
        db_path: str,
    ) -> None:
        """Accessing .cloud does not trigger loading of storage entries."""
        lazy = populated_db.get_lazy("test-cluster")
        assert lazy is not None

        from pynetappfoundry.cache.db import _query_registry_subset

        queried_paths: list[str] = []
        original_fn = _query_registry_subset

        def tracking_query(conn: Any, cluster_name: str, registry_subset: dict[str, Any]) -> Any:
            queried_paths.extend(registry_subset.keys())
            return original_fn(conn, cluster_name, registry_subset)

        with patch("pynetappfoundry.cache.db._query_registry_subset", tracking_query):
            _ = lazy.cloud

        # Storage paths should NOT be in the queried list
        for path in queried_paths:
            assert not path.startswith("storage"), f"Storage path queried: {path}"

    def test_field_cached_on_second_access(
        self,
        populated_db: ClusterMetadataDB,
        db_path: str,
    ) -> None:
        """Second access to same field uses cache, no re-query."""
        lazy = populated_db.get_lazy("test-cluster")
        assert lazy is not None

        # First access — loads from DB
        result1 = lazy.cloud

        connect_count = 0
        original_connect = sqlite3.connect

        def counting_connect(*args: Any, **kwargs: Any) -> Any:
            nonlocal connect_count
            connect_count += 1
            return original_connect(*args, **kwargs)

        with patch("pynetappfoundry.cache._lazy.sqlite3.connect", counting_connect):
            result2 = lazy.cloud

        assert result1 is result2
        assert connect_count == 0, "DB was opened on second access"

    def test_cloud_data_correct(self, populated_db: ClusterMetadataDB) -> None:
        """Lazy-loaded cloud data matches what was stored."""
        lazy = populated_db.get_lazy("test-cluster")
        assert lazy is not None
        assert len(lazy.cloud) == 1
        assert lazy.cloud[0].provider == "AWS"
        assert lazy.cloud[0].region == "us-east-1"

    def test_nodes_data_correct(self, populated_db: ClusterMetadataDB) -> None:
        """Lazy-loaded nodes data matches what was stored."""
        lazy = populated_db.get_lazy("test-cluster")
        assert lazy is not None
        assert len(lazy.nodes) == 2
        assert lazy.nodes[0].name == "node1"
        assert lazy.nodes[1].serial_number == "456"

    def test_cluster_singleton_correct(self, populated_db: ClusterMetadataDB) -> None:
        """Lazy-loaded singleton (cluster) matches what was stored."""
        lazy = populated_db.get_lazy("test-cluster")
        assert lazy is not None
        assert lazy.cluster.ontap_version == "9.14.1"
        assert lazy.cluster.cluster_name == "test-cluster"

    def test_container_fields_load_sub_tables(
        self,
        populated_db: ClusterMetadataDB,
    ) -> None:
        """Accessing .storage loads volumes and other storage sub-tables."""
        lazy = populated_db.get_lazy("test-cluster")
        assert lazy is not None
        assert len(lazy.storage.volumes) == 1
        assert lazy.storage.volumes[0].name == "vol1"
        assert lazy.storage.volumes[0].uuid == "11111111-1111-1111-1111-111111111111"

    def test_unknown_attribute_raises(self, populated_db: ClusterMetadataDB) -> None:
        """Accessing a non-existent attribute raises AttributeError."""
        lazy = populated_db.get_lazy("test-cluster")
        assert lazy is not None
        with pytest.raises(AttributeError, match="no_such_field"):
            lazy.no_such_field  # noqa: B018


class TestMaterialize:
    """Tests for _materialize() — full CachedClusterMetadata construction."""

    def test_materialize_returns_cached_cluster_metadata(
        self,
        populated_db: ClusterMetadataDB,
    ) -> None:
        """_materialize() returns a real CachedClusterMetadata."""
        lazy = populated_db.get_lazy("test-cluster")
        assert lazy is not None
        full = lazy._materialize()
        assert isinstance(full, CachedClusterMetadata)

    def test_materialize_data_matches_eager(
        self,
        populated_db: ClusterMetadataDB,
    ) -> None:
        """Materialized data matches eager get()."""
        lazy = populated_db.get_lazy("test-cluster")
        eager = populated_db.get("test-cluster")
        assert lazy is not None
        assert eager is not None

        full = lazy._materialize()
        assert full.model_dump() == eager.model_dump()

    def test_materialize_cached(self, populated_db: ClusterMetadataDB) -> None:
        """Second _materialize() call returns same instance."""
        lazy = populated_db.get_lazy("test-cluster")
        assert lazy is not None
        m1 = lazy._materialize()
        m2 = lazy._materialize()
        assert m1 is m2

    def test_uuid_index_triggers_full_load(
        self,
        populated_db: ClusterMetadataDB,
    ) -> None:
        """uuid_index property triggers materialization."""
        lazy = populated_db.get_lazy("test-cluster")
        assert lazy is not None
        index = lazy.uuid_index
        # Volume has a UUID, so it should appear in the index
        assert "11111111-1111-1111-1111-111111111111" in index


class TestIsStaleDelegation:
    """is_stale works without materialization."""

    def test_is_stale_fresh(self, populated_db: ClusterMetadataDB) -> None:
        """Fresh cache is not stale."""
        lazy = populated_db.get_lazy("test-cluster")
        assert lazy is not None
        assert lazy.is_stale(ttl_days=30) is False

    def test_is_stale_old(self, db: ClusterMetadataDB) -> None:
        """Old cache is stale."""
        old_time = datetime.now(UTC) - timedelta(days=35)
        meta = CachedClusterMetadata(
            cluster_name="old-cluster",
            cached_at=old_time,
        )
        db.set("old-cluster", meta)

        lazy = db.get_lazy("old-cluster")
        assert lazy is not None
        assert lazy.is_stale(ttl_days=30) is True

    def test_is_stale_no_materialization(
        self,
        populated_db: ClusterMetadataDB,
        db_path: str,
    ) -> None:
        """is_stale does not open a DB connection (uses envelope data)."""
        lazy = populated_db.get_lazy("test-cluster")
        assert lazy is not None

        connect_count = 0
        original_connect = sqlite3.connect

        def counting_connect(*args: Any, **kwargs: Any) -> Any:
            nonlocal connect_count
            connect_count += 1
            return original_connect(*args, **kwargs)

        with patch("pynetappfoundry.cache._lazy.sqlite3.connect", counting_connect):
            lazy.is_stale(ttl_days=30)

        assert connect_count == 0, "is_stale should not open DB"


class TestDelegatedMethods:
    """Tests for methods that delegate to the materialized instance."""

    def test_to_flat_dict(self, populated_db: ClusterMetadataDB) -> None:
        """to_flat_dict() delegates to materialized metadata."""
        lazy = populated_db.get_lazy("test-cluster")
        eager = populated_db.get("test-cluster")
        assert lazy is not None
        assert eager is not None
        assert lazy.to_flat_dict() == eager.to_flat_dict()

    def test_model_dump_matches_eager(self, populated_db: ClusterMetadataDB) -> None:
        """model_dump() matches eager loading."""
        lazy = populated_db.get_lazy("test-cluster")
        eager = populated_db.get("test-cluster")
        assert lazy is not None
        assert eager is not None
        assert lazy.model_dump() == eager.model_dump()

    def test_model_dump_json_matches_eager(self, populated_db: ClusterMetadataDB) -> None:
        """model_dump_json() matches eager loading."""
        lazy = populated_db.get_lazy("test-cluster")
        eager = populated_db.get("test-cluster")
        assert lazy is not None
        assert eager is not None
        # Parse both to compare as dicts (ordering may differ)
        import json

        lazy_data = json.loads(lazy.model_dump_json())
        eager_data = json.loads(eager.model_dump_json())
        assert lazy_data == eager_data


class TestGetLazy:
    """Tests for ClusterMetadataDB.get_lazy()."""

    def test_get_lazy_returns_lazy_instance(
        self,
        populated_db: ClusterMetadataDB,
    ) -> None:
        """get_lazy() returns a LazyClusterMetadata instance."""
        result = populated_db.get_lazy("test-cluster")
        assert isinstance(result, LazyClusterMetadata)

    def test_get_lazy_returns_none_for_missing(
        self,
        db: ClusterMetadataDB,
    ) -> None:
        """get_lazy() returns None when cluster not in DB."""
        result = db.get_lazy("nonexistent")
        assert result is None

    def test_get_lazy_invalid_name(self, db: ClusterMetadataDB) -> None:
        """get_lazy() raises ValueError for invalid cluster name."""
        with pytest.raises(ValueError, match="Invalid cluster name"):
            db.get_lazy("123invalid")

    def test_get_lazy_equivalent_to_get(
        self,
        populated_db: ClusterMetadataDB,
    ) -> None:
        """get_lazy()._materialize() produces same data as get()."""
        lazy = populated_db.get_lazy("test-cluster")
        eager = populated_db.get("test-cluster")
        assert lazy is not None
        assert eager is not None
        assert lazy._materialize().model_dump() == eager.model_dump()


class TestDataFieldsConstant:
    """Verify _DATA_FIELDS matches CachedClusterMetadata data fields."""

    def test_data_fields_match_model(self) -> None:
        """_DATA_FIELDS matches CachedClusterMetadata non-envelope fields."""
        envelope = {"cluster_name", "cached_at", "cache_version"}
        model_data_fields = set(CachedClusterMetadata.model_fields.keys()) - envelope
        assert model_data_fields == _DATA_FIELDS
