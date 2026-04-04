"""Benchmarks for change diff computation.

compute_diff() compares two CachedClusterMetadata snapshots field-by-field
to detect added, removed, and modified entities. It runs on every cache
update cycle.
"""

from __future__ import annotations

from typing import Any

import pytest

from pynetappfoundry.cache._metadata import CachedClusterMetadata
from pynetappfoundry.cache.diff import EntityConfig, _diff_entity_list, compute_diff
from pynetappfoundry.models.ontap.cluster.model import ClusterInfo
from pynetappfoundry.models.ontap.cluster.nodes.model import OntapNodeResponse
from pynetappfoundry.models.ontap.storage.volumes.model import OntapVolume

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_node(i: int, uptime: int = 86400) -> OntapNodeResponse:
    """Build a minimal OntapNodeResponse."""
    return OntapNodeResponse(
        name=f"node-{i:02d}",
        uuid=f"aaaaaaaa-bbbb-cccc-dddd-{i:012d}",
        model_="FAS8200",
        uptime=uptime,
        serial_number=f"SN{i:08d}",
    )


def _make_vol(i: int, state: str = "online") -> OntapVolume:
    """Build a minimal OntapVolume."""
    return OntapVolume(
        name=f"vol_{i:04d}",
        uuid=f"bbbbbbbb-cccc-dddd-eeee-{i:012d}",
        size=1073741824 * (i % 10 + 1),
        state=state,
        style="flexvol",
    )


def _make_metadata(
    *,
    num_nodes: int = 4,
    num_volumes: int = 100,
    node_uptime: int = 86400,
    vol_state: str = "online",
) -> CachedClusterMetadata:
    """Build a CachedClusterMetadata with controllable counts."""
    from pynetappfoundry.models.ontap.storage.model import StorageInfo

    return CachedClusterMetadata(
        cluster_name="bench-cluster",
        cluster=ClusterInfo(
            cluster_name="bench-cluster",
            cluster_uuid="cluster-uuid-001",
            ontap_version="9.14.1",
        ),
        nodes=[_make_node(i, uptime=node_uptime) for i in range(num_nodes)],
        storage=StorageInfo(
            volumes=[_make_vol(i, state=vol_state) for i in range(num_volumes)],
        ),
    )


# ---------------------------------------------------------------------------
# compute_diff benchmarks
# ---------------------------------------------------------------------------


@pytest.mark.benchmark(group="diff")
def test_bench_diff_initial_capture_small(benchmark: Any) -> None:
    """Initial capture (before=None) with 4 nodes + 50 volumes."""
    after = _make_metadata(num_nodes=4, num_volumes=50)
    benchmark(compute_diff, None, after)


@pytest.mark.benchmark(group="diff")
def test_bench_diff_no_changes(benchmark: Any) -> None:
    """Diff two identical snapshots (no changes) — 4 nodes + 100 volumes."""
    before = _make_metadata()
    after = _make_metadata()
    benchmark(compute_diff, before, after)


@pytest.mark.benchmark(group="diff")
def test_bench_diff_some_modified(benchmark: Any) -> None:
    """Diff with ~10% volumes modified (state change) — 100 volumes."""
    before = _make_metadata(num_volumes=100)
    # Modify every 10th volume
    after = _make_metadata(num_volumes=100)
    for i in range(0, 100, 10):
        after.storage.volumes[i] = _make_vol(i, state="offline")
    benchmark(compute_diff, before, after)


@pytest.mark.benchmark(group="diff")
def test_bench_diff_added_removed(benchmark: Any) -> None:
    """Diff with 10 added + 10 removed volumes."""
    before = _make_metadata(num_volumes=100)
    after = _make_metadata(num_volumes=100)
    # Remove first 10, add 10 new
    after.storage.volumes = after.storage.volumes[10:] + [_make_vol(1000 + i) for i in range(10)]
    benchmark(compute_diff, before, after)


@pytest.mark.benchmark(group="diff")
def test_bench_diff_large_500_volumes(benchmark: Any) -> None:
    """Diff with 500 volumes, ~10% modified."""
    before = _make_metadata(num_volumes=500)
    after = _make_metadata(num_volumes=500)
    for i in range(0, 500, 10):
        after.storage.volumes[i] = _make_vol(i, state="offline")
    benchmark(compute_diff, before, after)


# ---------------------------------------------------------------------------
# _diff_entity_list micro-benchmark (isolated from metadata traversal)
# ---------------------------------------------------------------------------


@pytest.mark.benchmark(group="diff_entity")
def test_bench_diff_entity_list_100_no_changes(benchmark: Any) -> None:
    """Diff 100 identical volume entity lists."""
    vols = [_make_vol(i) for i in range(100)]
    config = EntityConfig(
        key_field="uuid",
        model_class=OntapVolume,
        display_field="name",
    )
    benchmark(_diff_entity_list, "storage.volumes", vols, list(vols), config)


@pytest.mark.benchmark(group="diff_entity")
def test_bench_diff_entity_list_100_all_modified(benchmark: Any) -> None:
    """Diff 100 volumes where all have changed state."""
    before = [_make_vol(i, state="online") for i in range(100)]
    after = [_make_vol(i, state="offline") for i in range(100)]
    config = EntityConfig(
        key_field="uuid",
        model_class=OntapVolume,
        display_field="name",
    )
    benchmark(_diff_entity_list, "storage.volumes", before, after, config)
