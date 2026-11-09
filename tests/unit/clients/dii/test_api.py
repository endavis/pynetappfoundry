"""Tests for DIIAPIClient.get_all_pages offset/limit pagination."""

from __future__ import annotations

import logging
from typing import Any
from unittest.mock import MagicMock

import pytest

from pynetappfoundry.clients.dii import api as dii_api
from pynetappfoundry.clients.dii.api import DII_PAGE_SIZE, DIIAPIClient

PATH = "/assets/storages"


def _make_client(
    query_names: list[str] | None = None,
    responses: list[Any] | None = None,
) -> DIIAPIClient:
    """Build a client without __init__, with a stubbed spec lookup and endpoint."""
    client = DIIAPIClient.__new__(DIIAPIClient)
    names = ["limit", "offset"] if query_names is None else query_names
    client._extract_parameters = MagicMock(  # type: ignore[method-assign]
        return_value=([], [{"name": n, "in": "query"} for n in names])
    )
    client.call_endpoint = MagicMock(side_effect=responses or [])  # type: ignore[method-assign]
    return client


def _page(start: int, count: int) -> list[dict[str, int]]:
    return [{"id": i} for i in range(start, start + count)]


def _sent(client: DIIAPIClient) -> list[dict[str, Any]]:
    mock: MagicMock = client.call_endpoint  # type: ignore[assignment]
    return [c.kwargs["query_params"] for c in mock.call_args_list]


class TestGetAllPages:
    def test_multi_page_concatenation(self) -> None:
        n = DII_PAGE_SIZE
        client = _make_client(responses=[_page(0, n), _page(n, n), _page(2 * n, 5)])

        result = client.get_all_pages(PATH, {"vendor": "x"})

        assert [r["id"] for r in result] == list(range(2 * n + 5))
        sent = _sent(client)
        assert [p["offset"] for p in sent] == [0, n, 2 * n]
        assert all(p["limit"] == n and p["vendor"] == "x" for p in sent)

    def test_short_page_stops(self) -> None:
        client = _make_client(responses=[_page(0, DII_PAGE_SIZE), _page(DII_PAGE_SIZE, 1)])

        result = client.get_all_pages(PATH)

        assert len(result) == DII_PAGE_SIZE + 1
        assert len(_sent(client)) == 2

    def test_empty_page_past_the_end(self) -> None:
        client = _make_client(responses=[_page(0, DII_PAGE_SIZE), []])

        result = client.get_all_pages(PATH)

        assert len(result) == DII_PAGE_SIZE
        assert len(_sent(client)) == 2

    def test_non_paginating_endpoint_sends_no_offset_limit(self) -> None:
        client = _make_client(query_names=["vendor"], responses=[_page(0, 3)])

        result = client.get_all_pages(PATH, {"vendor": "x"})

        assert result == _page(0, 3)
        assert _sent(client) == [{"vendor": "x"}]

    def test_endpoint_with_only_limit_is_not_paginated(self) -> None:
        client = _make_client(query_names=["limit"], responses=[_page(0, 3)])

        client.get_all_pages(PATH)

        assert _sent(client) == [{}]

    @pytest.mark.parametrize("params", [{"offset": 5}, {"limit": 7}, {"offset": 5, "limit": 7}])
    def test_caller_offset_or_limit_is_single_request(self, params: dict[str, Any]) -> None:
        client = _make_client(responses=[_page(0, DII_PAGE_SIZE)])

        result = client.get_all_pages(PATH, params)

        assert len(result) == DII_PAGE_SIZE
        assert _sent(client) == [params]

    def test_non_list_first_page_returned_as_is(self) -> None:
        client = _make_client(responses=[{"items": []}])

        assert client.get_all_pages(PATH) == {"items": []}
        assert len(_sent(client)) == 1

    def test_non_list_mid_loop_stops(self) -> None:
        client = _make_client(responses=[_page(0, DII_PAGE_SIZE), None])

        result = client.get_all_pages(PATH)

        assert len(result) == DII_PAGE_SIZE

    def test_page_cap_logs_error_and_returns_gathered(
        self, monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture
    ) -> None:
        monkeypatch.setattr(dii_api, "DII_MAX_PAGES", 3)
        client = _make_client(responses=[_page(i * DII_PAGE_SIZE, DII_PAGE_SIZE) for i in range(5)])

        with caplog.at_level(logging.ERROR, logger=dii_api.logger.name):
            result = client.get_all_pages(PATH)

        assert len(result) == 3 * DII_PAGE_SIZE
        assert len(_sent(client)) == 3
        assert any(r.levelno == logging.ERROR for r in caplog.records)

    def test_first_page_short_warns(self, caplog: pytest.LogCaptureFixture) -> None:
        client = _make_client(responses=[_page(0, 10)])

        with caplog.at_level(logging.WARNING, logger=dii_api.logger.name):
            result = client.get_all_pages(PATH)

        assert len(result) == 10
        assert any(r.levelno == logging.WARNING for r in caplog.records)

    def test_empty_first_page_does_not_warn(self, caplog: pytest.LogCaptureFixture) -> None:
        client = _make_client(responses=[[]])

        with caplog.at_level(logging.WARNING, logger=dii_api.logger.name):
            assert client.get_all_pages(PATH) == []

        assert not caplog.records

    def test_caller_limit_does_not_warn(self, caplog: pytest.LogCaptureFixture) -> None:
        client = _make_client(responses=[_page(0, 2)])

        with caplog.at_level(logging.WARNING, logger=dii_api.logger.name):
            client.get_all_pages(PATH, {"limit": 100})

        assert not caplog.records
