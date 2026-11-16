"""Regression tests for #1052: DII models are live-only in DataSource routing.

No cache DB or network is touched -- backends and clients are mocked.
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from pynetappfoundry.data.dii_backend import DiiBackend
from pynetappfoundry.data.source import DataSource
from pynetappfoundry.models.dii.users.model import DiiUsersresponse


def test_dii_backend_is_live_only() -> None:
    assert DiiBackend.live_only is True


def test_auto_goes_live_with_single_backend_call() -> None:
    ds = DataSource(MagicMock())
    fake_backend = MagicMock(live_only=True)
    fake_backend.query.return_value = []
    ds._backends["dii"] = fake_backend
    list(ds.query(DiiUsersresponse, cluster="t"))
    fake_backend.query.assert_called_once()
    decision = fake_backend.query.call_args.args[2]
    assert decision.live_fields
    assert not decision.cache_fields


def test_auto_with_real_backend_and_mocked_client() -> None:
    ds = DataSource(MagicMock())
    client = MagicMock()
    client.get_all_pages.return_value = []
    with patch.object(DiiBackend, "_get_api_client", return_value=client):
        assert list(ds.query(DiiUsersresponse, cluster="t")) == []
    assert client.get_all_pages.call_count == 1


def test_cache_source_raises_at_query() -> None:
    ds = DataSource(MagicMock())
    with pytest.raises(ValueError, match="DiiBackend is live-only"):
        ds.query(DiiUsersresponse, cluster="t", source="cache")


def test_live_source_still_works() -> None:
    ds = DataSource(MagicMock())
    fake_backend = MagicMock(live_only=True)
    fake_backend.query.return_value = []
    ds._backends["dii"] = fake_backend
    assert list(ds.query(DiiUsersresponse, cluster="t", source="live")) == []
    fake_backend.query.assert_called_once()
