"""Characterization tests for the collect_all runners (issue #899).

These pin the observable behaviour of the sequential and parallel
``collect_all`` paths: progress-event order, failure handling, the data
source reported per phase, and the SSH pre-connect hand-off.
"""

from __future__ import annotations

import threading
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from pynetappfoundry.cache._metadata import RelationshipsInfo
from pynetappfoundry.cache.collector import (
    CollectionError,
    CollectionPhase,
    MetadataCollector,
    ProgressInfo,
)
from pynetappfoundry.models.ontap.cluster.mediators.model import OntapMediatorResponse
from pynetappfoundry.models.ontap.cluster.model import ClusterInfo
from pynetappfoundry.models.ontap.cluster.nodes.model import OntapNodeResponse
from pynetappfoundry.models.ontap.network.model import NetworkInfo
from pynetappfoundry.models.ontap.protocols.model import ProtocolsInfo
from pynetappfoundry.models.ontap.storage.model import StorageInfo

_ALL_PHASES = [
    CollectionPhase.CLUSTER,
    CollectionPhase.NODES,
    CollectionPhase.CLOUD,
    CollectionPhase.NETWORK,
    CollectionPhase.STORAGE,
    CollectionPhase.LICENSES,
    CollectionPhase.MEDIATOR,
    CollectionPhase.RELATIONSHIPS,
    CollectionPhase.PROTOCOLS,
]


def _make_collector(
    *,
    parallel: bool,
    cli_client: Any = None,
    nodes: list[OntapNodeResponse] | None = None,
    real_cloud: bool = False,
) -> tuple[MetadataCollector, list[ProgressInfo], list[Any]]:
    """Build a collector whose phase methods are stubbed with trivial results."""
    events: list[ProgressInfo] = []
    collector = MetadataCollector(
        api_client=MagicMock(),
        cli_client=cli_client,
        progress_callback=events.append,
        parallel=parallel,
    )
    node_list = nodes if nodes is not None else []

    def collect_nodes() -> list[OntapNodeResponse]:
        collector._results_cache["OntapNodeResponse"] = node_list
        return node_list

    patches = [
        patch.object(collector, "collect_cluster_info", return_value=ClusterInfo()),
        patch.object(collector, "collect_nodes", side_effect=collect_nodes),
        *(
            []
            if real_cloud
            else [patch.object(collector, "collect_cloud_metadata", return_value=[])]
        ),
        patch.object(collector, "collect_network", return_value=NetworkInfo()),
        patch.object(collector, "collect_storage", return_value=StorageInfo()),
        patch.object(collector, "collect_licenses", return_value=[]),
        patch.object(collector, "collect_mediator", return_value=OntapMediatorResponse()),
        patch.object(collector, "collect_relationships", return_value=RelationshipsInfo()),
        patch.object(collector, "collect_protocols", return_value=ProtocolsInfo()),
    ]
    for p in patches:
        p.start()
    return collector, events, patches


@pytest.fixture(autouse=True)
def _stop_patches() -> Any:
    yield
    patch.stopall()


def _statuses(events: list[ProgressInfo]) -> list[tuple[CollectionPhase, str]]:
    return [(e.phase, e.status) for e in events]


class TestSequentialRunner:
    def test_progress_order(self) -> None:
        collector, events, _ = _make_collector(parallel=False)
        collector.collect_all("c1")
        expected: list[tuple[CollectionPhase, str]] = []
        for phase in _ALL_PHASES:
            expected += [(phase, "starting"), (phase, "completed")]
        assert _statuses(events) == expected

    def test_failure_propagates_original_exception_and_stops(self) -> None:
        collector, events, _ = _make_collector(parallel=False)
        with (
            patch.object(collector, "collect_network", side_effect=RuntimeError("boom")),
            pytest.raises(RuntimeError, match="boom"),
        ):
            collector.collect_all("c1")
        assert (CollectionPhase.NETWORK, "failed") in _statuses(events)
        assert (CollectionPhase.STORAGE, "starting") not in _statuses(events)

    def test_cloud_failure_is_fatal(self) -> None:
        collector, events, _ = _make_collector(parallel=False)
        with (
            patch.object(collector, "collect_cloud_metadata", side_effect=RuntimeError("x")),
            pytest.raises(RuntimeError),
        ):
            collector.collect_all("c1")
        assert (CollectionPhase.CLOUD, "failed") in _statuses(events)

    def test_sources(self) -> None:
        collector, events, _ = _make_collector(parallel=False, cli_client=MagicMock())
        collector.collect_all("c1")
        completed = {e.phase: e.source for e in events if e.status == "completed"}
        assert completed[CollectionPhase.CLOUD] == "cli"
        assert all(completed[p] == "api" for p in _ALL_PHASES if p is not CollectionPhase.CLOUD)

    def test_cloud_source_none_without_cli(self) -> None:
        collector, events, _ = _make_collector(parallel=False)
        collector.collect_all("c1")
        completed = {e.phase: e.source for e in events if e.status == "completed"}
        assert completed[CollectionPhase.CLOUD] is None


class TestParallelRunner:
    def test_progress_order(self) -> None:
        collector, events, _ = _make_collector(parallel=True)
        collector.collect_all("c1")
        statuses = _statuses(events)
        assert [s for _, s in statuses[:9]] == ["starting"] * 9
        assert {p for p, _ in statuses[:9]} == set(_ALL_PHASES)
        assert statuses[-1] == (CollectionPhase.CLOUD, "completed")
        completed = {p for p, s in statuses if s == "completed"}
        assert completed == set(_ALL_PHASES)

    def test_failure_raises_collection_error(self) -> None:
        collector, events, _ = _make_collector(parallel=True)
        with (
            patch.object(collector, "collect_network", side_effect=RuntimeError("boom")),
            pytest.raises(CollectionError) as exc_info,
        ):
            collector.collect_all("c1")
        assert isinstance(exc_info.value.__cause__, RuntimeError)
        assert str(exc_info.value) == "Collection failed for phase network: boom"
        cloud_events = [s for p, s in _statuses(events) if p is CollectionPhase.CLOUD]
        assert cloud_events == ["starting"]

    def test_cloud_failure_is_non_fatal(self) -> None:
        collector, events, _ = _make_collector(parallel=True)
        with patch.object(collector, "collect_cloud_metadata", side_effect=RuntimeError("x")):
            result = collector.collect_all("c1")
        assert result.cloud == []
        assert (CollectionPhase.CLOUD, "failed") in _statuses(events)
        assert (CollectionPhase.CLOUD, "completed") not in _statuses(events)

    def test_sources(self) -> None:
        collector, events, _ = _make_collector(parallel=True, cli_client=MagicMock())
        collector.collect_all("c1")
        completed = {e.phase: e.source for e in events if e.status == "completed"}
        assert completed[CollectionPhase.CLOUD] == "cli"
        assert all(completed[p] == "api" for p in _ALL_PHASES if p is not CollectionPhase.CLOUD)


class TestSshPreconnect:
    def test_cvo_cloud_phase_runs_after_connect_completes(self) -> None:
        """For CVO clusters the CLI call must not run before the SSH connect finished."""
        cli = MagicMock()
        connected = threading.Event()
        release = threading.Event()

        def connect() -> None:
            release.wait(timeout=5)
            connected.set()

        def run_command(cmd: str) -> list[str]:
            assert connected.is_set(), "run_command ran before connect finished"
            return []

        cli.connect.side_effect = connect
        cli.run_command.side_effect = run_command

        collector, _, _ = _make_collector(
            parallel=True,
            cli_client=cli,
            nodes=[OntapNodeResponse(name="cvo", model_="CDvM200")],
            real_cloud=True,
        )
        threading.Timer(0.3, release.set).start()
        collector.collect_all("c1")
        assert connected.is_set()
        cli.run_command.assert_called_once()

    def test_onprem_does_not_wait_for_connect(self) -> None:
        cli = MagicMock()
        cli.connect.side_effect = lambda: time.sleep(2.0)
        collector, _, _ = _make_collector(
            parallel=True,
            cli_client=cli,
            nodes=[OntapNodeResponse(name="fas", model_="FAS8200")],
        )
        start = time.monotonic()
        collector.collect_all("c1")
        assert time.monotonic() - start < 1.8
        cli.run_command.assert_not_called()


class TestPoolConstants:
    def test_constant_values(self) -> None:
        from pynetappfoundry.cache import _collector_runner as r

        assert r.DEFAULT_MAX_WORKERS == 8
        assert r.NETWORK_FETCH_WORKERS == 5
        assert r.STORAGE_FETCH_WORKERS == 12
        assert r.RELATIONSHIPS_FETCH_WORKERS == 3
        assert r.PROTOCOLS_FETCH_WORKERS == 5
        assert MetadataCollector().max_workers == r.DEFAULT_MAX_WORKERS

    def test_composite_phases_use_named_pool_sizes(self) -> None:
        sizes: list[int] = []

        class RecordingExecutor(ThreadPoolExecutor):
            def __init__(self, max_workers: int | None = None, *a: Any, **k: Any) -> None:
                sizes.append(max_workers or 0)
                super().__init__(max_workers, *a, **k)

        collector = MetadataCollector(api_client=MagicMock(), parallel=True)
        with (
            patch("pynetappfoundry.cache._collector_runner.ThreadPoolExecutor", RecordingExecutor),
            patch.object(collector, "_fetch_model", return_value=[]),
            patch.object(collector, "_cached_api_call", return_value={"records": []}),
        ):
            collector.collect_storage()
            collector.collect_network()
            collector.collect_relationships()
            collector.collect_protocols()
        assert sizes == [12, 5, 3, 5]
