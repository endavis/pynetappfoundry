"""Tests for the cache refresh orchestration library."""

from __future__ import annotations

import threading
from collections.abc import Iterator
from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from pynetappfoundry.cache import CachedClusterMetadata, CacheHistoryDB, ClusterMetadataDB
from pynetappfoundry.cache.refresher import (
    CacheRefresher,
    ClusterProgress,
    ClusterRefreshResult,
    RefreshStatus,
    categorize_failure,
    effective_workers,
)
from pynetappfoundry.models.ontap.cluster.model import ClusterInfo

MODULE = "pynetappfoundry.cache.refresher"


def _metadata(name: str, version: str = "9.14.1") -> CachedClusterMetadata:
    return CachedClusterMetadata(
        cluster_name=name,
        cluster=ClusterInfo(cluster_name=name, ontap_version=version),
    )


class _Observer:
    """Records observer events."""

    def __init__(self) -> None:
        self.started: list[tuple[str, int, int]] = []
        self.finished: list[tuple[ClusterRefreshResult, int, int]] = []
        self.started_threads: list[threading.Thread] = []
        self.finished_threads: list[threading.Thread] = []
        self.sink: MagicMock = MagicMock()

    def cluster_started(self, name: str, index: int, total: int) -> ClusterProgress | None:
        self.started.append((name, index, total))
        self.started_threads.append(threading.current_thread())
        return self.sink

    def cluster_finished(
        self,
        result: ClusterRefreshResult,
        progress: ClusterProgress | None,
        completed: int,
        total: int,
    ) -> None:
        self.finished.append((result, completed, total))
        self.finished_threads.append(threading.current_thread())


@pytest.fixture
def config() -> MagicMock:
    cfg = MagicMock()
    cfg.data = {"clusters": {n: {"ip": f"10.0.0.{i}"} for i, n in enumerate(["c1", "c2", "c3"])}}
    cfg.get_user.return_value = ("admin", "pw")
    cfg.settings = {}
    return cfg


@pytest.fixture
def dbs() -> Iterator[tuple[ClusterMetadataDB, CacheHistoryDB]]:
    db = ClusterMetadataDB(db_path=":memory:")
    history = CacheHistoryDB(db_path=":memory:")
    yield db, history
    history.close()
    db.close()


def _history_count(history: CacheHistoryDB) -> int:
    row = history.conn.execute("SELECT COUNT(*) FROM cache_changes").fetchone()
    return int(row[0])


class TestHelpers:
    def test_effective_workers(self) -> None:
        assert effective_workers(4, 0) == 1
        assert effective_workers(4, 1) == 1
        assert effective_workers(4, 3) == 3
        assert effective_workers(2, 5) == 2
        assert effective_workers(1, 5) == 1

    def test_categorize_failure(self) -> None:
        assert categorize_failure(RuntimeError("CLI_FAILURE: boom")) == ("CLI", "boom")
        assert categorize_failure(RuntimeError("API_FAILURE: bad")) == ("API", "bad")
        assert categorize_failure(RuntimeError("Collection failed for phase x"))[0] == "API"
        assert categorize_failure(ValueError("odd")) == ("API", "ValueError: odd")

    def test_result_failure_text(self) -> None:
        assert ClusterRefreshResult("c", RefreshStatus.OK).failure is None
        assert ClusterRefreshResult("c", RefreshStatus.NO_CLIENTS).failure == "No clients available"
        failed = ClusterRefreshResult(
            "c", RefreshStatus.COLLECT_FAILED, RuntimeError("CLI_FAILURE: x")
        )
        assert failed.failure == "CLI: x"


class TestLoadPrevious:
    def _refresher(self, snapshot: dict[str, Any] | None) -> CacheRefresher:
        history = MagicMock()
        history.get_latest_snapshot.return_value = snapshot
        return CacheRefresher(MagicMock(), MagicMock(), history)

    def test_no_snapshot(self) -> None:
        assert self._refresher(None)._load_previous("c1") is None

    def test_incompatible_schema_returns_none(self) -> None:
        snapshot = {"after_json": '{"cache_version": "0.0.0-nope"}'}
        with patch(f"{MODULE}.is_schema_compatible", return_value=False):
            assert self._refresher(snapshot)._load_previous("c1") is None

    def test_unparseable_returns_none(self) -> None:
        assert self._refresher({"after_json": "not json"})._load_previous("c1") is None

    def test_valid_snapshot_loaded(self) -> None:
        snapshot = {"after_json": _metadata("c1").model_dump_json()}
        loaded = self._refresher(snapshot)._load_previous("c1")
        assert loaded is not None
        assert loaded.cluster_name == "c1"


@pytest.fixture
def patched_clients() -> Iterator[dict[str, MagicMock]]:
    with (
        patch(f"{MODULE}.ONTAPAPIClient") as api,
        patch(f"{MODULE}.ONTAPCLI") as cli,
        patch(f"{MODULE}.MetadataCollector") as collector,
    ):
        collector.return_value.collect_all.side_effect = lambda name: _metadata(name)
        yield {"api": api, "cli": cli, "collector": collector}


class TestRunSequential:
    def test_initial_capture_then_identical_then_changed(
        self,
        config: MagicMock,
        dbs: tuple[ClusterMetadataDB, CacheHistoryDB],
        patched_clients: dict[str, MagicMock],
    ) -> None:
        db, history = dbs
        refresher = CacheRefresher(config, db, history)
        obs = _Observer()

        summary = refresher.run(["c1"], workers=1, observer=obs)
        assert summary.succeeded == 1
        assert summary.failed == 0
        assert _history_count(history) == 1
        assert db.get("c1") is not None
        assert obs.started == [("c1", 1, 1)]

        # Identical second run records no new history.
        refresher.run(["c1"], workers=1, observer=_Observer())
        assert _history_count(history) == 1

        # A changed run records exactly one more entry.
        patched_clients["collector"].return_value.collect_all.side_effect = lambda n: _metadata(
            n, "9.15.1"
        )
        refresher.run(["c1"], workers=1, observer=_Observer())
        assert _history_count(history) == 2

    def test_no_clients(
        self,
        config: MagicMock,
        dbs: tuple[ClusterMetadataDB, CacheHistoryDB],
        patched_clients: dict[str, MagicMock],
    ) -> None:
        patched_clients["api"].side_effect = RuntimeError("no api")
        patched_clients["cli"].side_effect = RuntimeError("no cli")
        obs = _Observer()
        summary = CacheRefresher(config, *dbs).run(["c1"], workers=1, observer=obs)
        assert summary.results[0].status is RefreshStatus.NO_CLIENTS
        assert summary.failures == {"c1": ["No clients available"]}
        kinds = [c.args[0] for c in obs.sink.on_client_unavailable.call_args_list]
        assert kinds == ["API", "CLI"]
        patched_clients["collector"].assert_not_called()

    def test_collect_failure_still_disconnects_cli(
        self,
        config: MagicMock,
        dbs: tuple[ClusterMetadataDB, CacheHistoryDB],
        patched_clients: dict[str, MagicMock],
    ) -> None:
        patched_clients["collector"].return_value.collect_all.side_effect = RuntimeError(
            "API_FAILURE: nope"
        )
        obs = _Observer()
        summary = CacheRefresher(config, *dbs).run(["c1"], workers=1, observer=obs)
        assert summary.results[0].status is RefreshStatus.COLLECT_FAILED
        assert summary.failures == {"c1": ["API: nope"]}
        patched_clients["cli"].return_value.disconnect.assert_called_once()
        obs.sink.on_collection_finished.assert_called_once_with(False)

    def test_persist_failure(
        self,
        config: MagicMock,
        dbs: tuple[ClusterMetadataDB, CacheHistoryDB],
        patched_clients: dict[str, MagicMock],
    ) -> None:
        db = MagicMock()
        db.set.side_effect = RuntimeError("disk full")
        summary = CacheRefresher(config, db, dbs[1]).run(["c1"], workers=1, observer=_Observer())
        assert summary.results[0].status is RefreshStatus.PERSIST_FAILED

    def test_no_executor_when_single_worker(
        self,
        config: MagicMock,
        dbs: tuple[ClusterMetadataDB, CacheHistoryDB],
        patched_clients: dict[str, MagicMock],
    ) -> None:
        with patch(f"{MODULE}.ThreadPoolExecutor") as executor:
            CacheRefresher(config, *dbs).run(["c1", "c2"], workers=1, observer=_Observer())
        executor.assert_not_called()


class TestRunParallel:
    def test_completion_counters_and_main_thread_persistence(
        self,
        config: MagicMock,
        dbs: tuple[ClusterMetadataDB, CacheHistoryDB],
        patched_clients: dict[str, MagicMock],
    ) -> None:
        db, history = dbs
        obs = _Observer()
        summary = CacheRefresher(config, db, history).run(
            ["c1", "c2", "c3"], workers=3, observer=obs
        )
        assert summary.succeeded == 3
        assert [c for _, c, _ in obs.finished] == [1, 2, 3]
        assert {t for _, _, t in obs.finished} == {3}
        assert sorted(r.cluster_name for r, _, _ in obs.finished) == ["c1", "c2", "c3"]
        main = threading.main_thread()
        assert all(t is main for t in obs.started_threads)
        assert all(t is main for t in obs.finished_threads)
        assert _history_count(history) == 3

    def test_exception_escaping_worker_is_collect_failure(
        self,
        config: MagicMock,
        dbs: tuple[ClusterMetadataDB, CacheHistoryDB],
        patched_clients: dict[str, MagicMock],
    ) -> None:
        with patch(f"{MODULE}._collect_cluster", side_effect=RuntimeError("worker died")):
            summary = CacheRefresher(config, *dbs).run(
                ["c1", "c2"], workers=2, observer=_Observer()
            )
        assert {r.status for r in summary.results} == {RefreshStatus.COLLECT_FAILED}
