"""Characterization tests for ``MetadataCollector._cached_api_call`` (issue #899)."""

from __future__ import annotations

import contextlib
import threading
from concurrent.futures import ThreadPoolExecutor
from typing import Any
from unittest.mock import MagicMock

from pynetappfoundry.cache.collector import MetadataCollector


def _barrier_client(barrier: threading.Barrier, payload: Any) -> MagicMock:
    client = MagicMock()

    def get_all_records(url: str, method: str = "GET") -> Any:
        with contextlib.suppress(threading.BrokenBarrierError):
            barrier.wait(timeout=0.5)
        return payload

    client.get_all_records.side_effect = get_all_records
    return client


class TestCachedApiCallConcurrency:
    def test_concurrent_callers_share_one_request(self) -> None:
        """Four threads asking for one endpoint cause exactly one API request."""
        payload = {"records": [{"name": "a"}]}
        client = _barrier_client(threading.Barrier(4), payload)
        collector = MetadataCollector(api_client=client)
        with ThreadPoolExecutor(max_workers=4) as pool:
            results = list(pool.map(lambda _: collector._cached_api_call("/x"), range(4)))
        assert client.get_all_records.call_count == 1
        assert all(r is results[0] for r in results)

    def test_failure_is_shared_not_cached_and_retried(self) -> None:
        barrier = threading.Barrier(3)
        client = MagicMock()
        calls = {"n": 0}
        lock = threading.Lock()

        def get_all_records(url: str, method: str = "GET") -> Any:
            with lock:
                calls["n"] += 1
                n = calls["n"]
            if n == 1:
                with contextlib.suppress(threading.BrokenBarrierError):
                    barrier.wait(timeout=0.5)
                raise ValueError("boom")
            return {"records": []}

        client.get_all_records.side_effect = get_all_records
        collector = MetadataCollector(api_client=client)

        def call(_: int) -> str:
            try:
                collector._cached_api_call("/x")
            except ValueError:
                return "err"
            return "ok"

        with ThreadPoolExecutor(max_workers=3) as pool:
            assert list(pool.map(call, range(3))) == ["err"] * 3
        assert calls["n"] == 1
        assert collector._cached_api_call("/x") == {"records": []}
        assert calls["n"] == 2
        assert getattr(collector, "_inflight", {}) == {}

    def test_paginate_false_uses_call_endpoint_once(self) -> None:
        client = MagicMock()
        client.call_endpoint.return_value = {"name": "c"}
        collector = MetadataCollector(api_client=client)
        assert collector._cached_api_call("/cluster", paginate=False) == {"name": "c"}
        assert collector._cached_api_call("/cluster", paginate=False) == {"name": "c"}
        client.call_endpoint.assert_called_once()
        client.get_all_records.assert_not_called()

    def test_no_api_client_returns_none(self) -> None:
        assert MetadataCollector()._cached_api_call("/x") is None

    def test_clear_cache_forces_refetch(self) -> None:
        client = MagicMock()
        client.get_all_records.return_value = {"records": []}
        collector = MetadataCollector(api_client=client)
        collector._cached_api_call("/x")
        collector._clear_cache()
        collector._cached_api_call("/x")
        assert client.get_all_records.call_count == 2


class TestSingleFlight:
    def test_caches_non_api_key_and_clear_resets(self) -> None:
        collector = MetadataCollector(api_client=MagicMock())
        calls: list[int] = []

        def produce() -> list[int]:
            calls.append(1)
            return [len(calls)]

        first = collector._single_flight("model:X", produce)
        assert collector._single_flight("model:X", produce) is first
        assert len(calls) == 1
        collector._clear_cache()
        assert collector._single_flight("model:X", produce) == [2]

    def test_concurrent_cluster_and_nodes_phases_share_one_request(self) -> None:
        payload = {
            "records": [
                {"name": "n1", "uuid": "11111111-1111-1111-1111-111111111111"},
                {"name": "n2", "uuid": "22222222-2222-2222-2222-222222222222"},
            ]
        }
        client = MagicMock()
        barrier = threading.Barrier(2)

        def get_all_records(url: str, method: str = "GET") -> Any:
            with contextlib.suppress(threading.BrokenBarrierError):
                barrier.wait(timeout=0.5)
            return payload

        client.get_all_records.side_effect = get_all_records
        client.call_endpoint.return_value = {
            "name": "c",
            "uuid": "33333333-3333-3333-3333-333333333333",
        }
        collector = MetadataCollector(api_client=client)
        with ThreadPoolExecutor(max_workers=2) as pool:
            f1 = pool.submit(collector._collect_nodes_via_api)
            f2 = pool.submit(collector._collect_cluster_info_via_api)
            f1.result()
            f2.result()
        node_calls = [
            c for c in client.get_all_records.call_args_list if "/cluster/nodes" in c.args[0]
        ]
        assert len(node_calls) == 1
        assert collector._inflight == {}
