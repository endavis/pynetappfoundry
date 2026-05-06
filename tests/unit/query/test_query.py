"""Tests for pynetappfoundry.query.query module."""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock

import pytest

from pynetappfoundry.query import Query
from pynetappfoundry.query.query import Query as QueryDirect

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def mock_client() -> MagicMock:
    """Return a mocked APIWrapper with call_endpoint."""
    return MagicMock(spec=["call_endpoint"])


# ---------------------------------------------------------------------------
# Import / public API tests
# ---------------------------------------------------------------------------


class TestQueryImport:
    """Query is importable from the top-level query package."""

    def test_importable_from_package(self) -> None:
        assert Query is QueryDirect

    def test_present_in_all(self) -> None:
        import pynetappfoundry.query as pkg

        assert "Query" in pkg.__all__


# ---------------------------------------------------------------------------
# Constructor tests
# ---------------------------------------------------------------------------


class TestQueryInit:
    """Tests for Query.__init__."""

    def test_stores_client(self, mock_client: MagicMock) -> None:
        q = Query(mock_client, "/lake/query/timeseries")
        assert q._client is mock_client

    def test_stores_path(self, mock_client: MagicMock) -> None:
        q = Query(mock_client, "/lake/query/timeseries")
        assert q._path == "/lake/query/timeseries"

    def test_different_paths_stored_independently(self, mock_client: MagicMock) -> None:
        q1 = Query(mock_client, "/path/one")
        q2 = Query(mock_client, "/path/two")
        assert q1._path == "/path/one"
        assert q2._path == "/path/two"


# ---------------------------------------------------------------------------
# invoke tests
# ---------------------------------------------------------------------------


class TestQueryInvoke:
    """Tests for Query.invoke."""

    def test_calls_post_on_correct_path(self, mock_client: MagicMock) -> None:
        mock_client.call_endpoint.return_value = []
        q = Query(mock_client, "/lake/query/timeseries")
        q.invoke({"metric": "cpu"})
        mock_client.call_endpoint.assert_called_once_with(
            "/lake/query/timeseries", method="POST", body={"metric": "cpu"}
        )

    def test_passes_body_through(self, mock_client: MagicMock) -> None:
        mock_client.call_endpoint.return_value = []
        body: dict[str, Any] = {"metric": "iops", "interval": "5m", "filters": ["vol1"]}
        q = Query(mock_client, "/some/endpoint")
        q.invoke(body)
        _, kwargs = mock_client.call_endpoint.call_args
        assert kwargs["body"] == body

    def test_invoke_with_no_body(self, mock_client: MagicMock) -> None:
        """invoke() with no body sends body=None."""
        mock_client.call_endpoint.return_value = []
        q = Query(mock_client, "/some/endpoint")
        q.invoke()
        mock_client.call_endpoint.assert_called_once_with(
            "/some/endpoint", method="POST", body=None
        )

    def test_invoke_with_query_params(self, mock_client: MagicMock) -> None:
        """query_params kwarg is forwarded to call_endpoint."""
        mock_client.call_endpoint.return_value = {}
        q = Query(mock_client, "/some/endpoint")
        q.invoke({"metric": "iops"}, query_params={"expand": "true"})
        mock_client.call_endpoint.assert_called_once_with(
            "/some/endpoint",
            method="POST",
            body={"metric": "iops"},
            query_params={"expand": "true"},
        )

    def test_invoke_without_query_params_omits_kwarg(self, mock_client: MagicMock) -> None:
        """query_params is not forwarded when not provided."""
        mock_client.call_endpoint.return_value = {}
        q = Query(mock_client, "/some/endpoint")
        q.invoke({"metric": "iops"})
        call_kwargs = mock_client.call_endpoint.call_args[1]
        assert "query_params" not in call_kwargs

    def test_invoke_does_not_disable_retry(self, mock_client: MagicMock) -> None:
        """Query.invoke does NOT disable retry (opposite of Mutation.create).

        RPC query endpoints are idempotent reads — the client default retry
        config must be used unchanged.
        """
        from pynetappfoundry.core.models import RetryConfig

        mock_client.call_endpoint.return_value = []
        q = Query(mock_client, "/some/endpoint")
        q.invoke({"x": 1})
        call_kwargs = mock_client.call_endpoint.call_args[1]
        assert "retry_config" not in call_kwargs or call_kwargs.get("retry_config") != RetryConfig(
            enabled=False
        )

    def test_returns_list_response(self, mock_client: MagicMock) -> None:
        expected: list[dict[str, Any]] = [{"ts": 1, "value": 42}, {"ts": 2, "value": 43}]
        mock_client.call_endpoint.return_value = expected
        q = Query(mock_client, "/lake/query/timeseries")
        result = q.invoke({"metric": "cpu"})
        assert result == expected

    def test_returns_dict_response(self, mock_client: MagicMock) -> None:
        expected: dict[str, Any] = {"total": 5, "records": [{"ts": 1}]}
        mock_client.call_endpoint.return_value = expected
        q = Query(mock_client, "/lake/query/summary")
        result = q.invoke({"metric": "latency"})
        assert result == expected

    def test_returns_empty_list(self, mock_client: MagicMock) -> None:
        mock_client.call_endpoint.return_value = []
        q = Query(mock_client, "/lake/query/timeseries")
        result = q.invoke({})
        assert result == []

    def test_uses_stored_path_on_each_call(self, mock_client: MagicMock) -> None:
        mock_client.call_endpoint.return_value = []
        q = Query(mock_client, "/fixed/path")
        q.invoke({"a": 1})
        q.invoke({"b": 2})
        assert mock_client.call_endpoint.call_count == 2
        for c in mock_client.call_endpoint.call_args_list:
            assert c[0][0] == "/fixed/path"

    def test_works_with_any_mock_client(self) -> None:
        """Query is not coupled to any specific client type."""
        generic_client = MagicMock()
        generic_client.call_endpoint.return_value = {"ok": True}
        q = Query(generic_client, "/any/path")
        result = q.invoke({"x": 1})
        assert result == {"ok": True}
