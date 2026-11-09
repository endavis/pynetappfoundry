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
