"""Benchmarks for :class:`pynetappfoundry.cache.LazyClusterMetadata`.

Phase 3b of #495/#502 migrates the shim to a :class:`DataSource`-backed
implementation. These benchmarks compare ``.storage`` field-group access
through the new shim against the equivalent direct cache-DB read
(``_query_registry_subset`` over the same open connection), so reviewers
can quantify the overhead of DataSource routing on a populated database.
"""

from __future__ import annotations

import uuid
from typing import Any
from unittest.mock import MagicMock

import pytest

from pynetappfoundry.cache._metadata import CachedClusterMetadata
from pynetappfoundry.cache.db import ClusterMetadataDB, _query_registry_subset
from pynetappfoundry.cache.db_schema import _ensure_registry
from pynetappfoundry.core.config import Config
from pynetappfoundry.models.ontap.storage.aggregates.model import OntapAggregate
from pynetappfoundry.models.ontap.storage.model import StorageInfo
from pynetappfoundry.models.ontap.storage.volumes.model import OntapVolume

_VOLUME_COUNT = 500
_AGGREGATE_COUNT = 20


def _make_metadata() -> CachedClusterMetadata:
    """Build a CachedClusterMetadata populated with storage data only."""
    volumes = [
        OntapVolume(
            name=f"vol_{i:04d}",
            uuid=f"aaaaaaaa-bbbb-cccc-dddd-{i:012d}",
            size=1073741824 * (i % 10 + 1),
            state="online" if i % 5 != 0 else "offline",
        )
        for i in range(_VOLUME_COUNT)
    ]
    aggregates = [
        OntapAggregate(
            name=f"aggr_{i:02d}",
            uuid=f"00000000-0000-0000-0000-{i:012d}",
        )
        for i in range(_AGGREGATE_COUNT)
    ]
    return CachedClusterMetadata(
        cluster_name="bench-cluster",
        storage=StorageInfo(volumes=volumes, aggregates=aggregates),
    )


@pytest.fixture
def populated_bench_db() -> ClusterMetadataDB:
    """A per-test in-memory cache DB populated with ~500 volumes."""
    cfg = MagicMock(spec=Config)
    db_path = f"file:bench_lazy_{uuid.uuid4().hex[:8]}?mode=memory&cache=shared"
    db = ClusterMetadataDB(db_path=db_path, config=cfg)
    db.set("bench-cluster", _make_metadata())
    return db


def _storage_subset() -> dict[str, Any]:
    """Return the subset of the table registry covering the storage group."""
    registry = _ensure_registry()
    return {path: spec for path, spec in registry.items() if path.startswith("storage.")}


@pytest.mark.benchmark(group="lazy_field_group_load")
def test_bench_lazy_storage_via_shim(
    benchmark: Any,
    populated_bench_db: ClusterMetadataDB,
) -> None:
    """Time ``.storage`` access on a fresh LazyClusterMetadata shim.

    Each round constructs a new lazy metadata via ``get_lazy()`` so the
    internal per-group ``_loaded`` cache doesn't mask the real cost.
    """

    def _access_storage() -> int:
        lazy = populated_bench_db.get_lazy("bench-cluster")
        assert lazy is not None
        return len(lazy.storage.volumes)

    result = benchmark(_access_storage)
    assert result == _VOLUME_COUNT


@pytest.mark.benchmark(group="lazy_field_group_load")
def test_bench_lazy_storage_direct_db(
    benchmark: Any,
    populated_bench_db: ClusterMetadataDB,
) -> None:
    """Time the equivalent ``_query_registry_subset`` read directly.

    Mirrors the legacy (pre-#502) code path: a single
    ``_query_registry_subset`` call over the same shared SQLite
    connection for the storage subset.
    """
    subset = _storage_subset()

    def _direct_read() -> int:
        root = _query_registry_subset(populated_bench_db.conn, "bench-cluster", subset)
        storage = StorageInfo.model_validate(root.get("storage", {}))
        return len(storage.volumes)

    result = benchmark(_direct_read)
    assert result == _VOLUME_COUNT
