"""End-to-end DataSource tests over the generated OCCM model (mocked client, no network)."""

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from pynetappfoundry.data.source import DataSource
from pynetappfoundry.models.console.cvo.get_onprem_working_environments import (
    OnPremClusterProperties,
    ResponseBody,
)

_CLIENT_PATH = "pynetappfoundry.clients.console.agent.ConsoleAgentClient"


@pytest.fixture(autouse=True)
def empty_occm_cache(tmp_path: Path) -> Iterator[None]:
    """Point the OCCM cache at an empty file so ``auto`` falls back to live."""
    from pynetappfoundry.cache.occm_db import OccmCacheDB
    from pynetappfoundry.data.occm_backend import OccmBackend

    with (
        OccmCacheDB(db_path=tmp_path / "occm_cache.db") as db,
        patch.object(OccmBackend, "_cache_db", db),
    ):
        yield


@pytest.fixture
def op() -> Iterator[MagicMock]:
    with patch(_CLIENT_PATH) as cls:
        mock: MagicMock = cls.return_value.ops.list_onprem_working_environments
        mock.return_value = []
        yield mock


def _ds() -> DataSource:
    config = MagicMock()
    config.data = {"connectors": {"c1": {"agent_id": "agent-1"}}}
    return DataSource(config)


def _env(public_id: str, **kwargs: Any) -> ResponseBody:
    return ResponseBody(publicId=public_id, name=f"n-{public_id}", **kwargs)


def test_mapping_resolves_to_occm() -> None:
    assert DataSource._resolve_mapping(ResponseBody).api_type == "occm"


def test_auto_query_goes_live(op: MagicMock) -> None:
    items = [_env("p1"), _env("p2")]
    op.return_value = items
    assert list(_ds().query(ResponseBody, cluster="c1")) == items
    op.assert_called_once_with()


def test_cache_source_on_empty_cache_returns_nothing(op: MagicMock) -> None:
    assert list(_ds().query(ResponseBody, cluster="c1", source="cache")) == []
    op.assert_not_called()


def test_fields_selection_sent(op: MagicMock) -> None:
    list(_ds().query(ResponseBody, cluster="c1").fields("ontapClusterProperties"))
    op.assert_called_once_with(fields="ontapClusterProperties")


def test_two_explicit_fields_sent_as_csv(op: MagicMock) -> None:
    list(_ds().query(ResponseBody, cluster="c1").fields("status", "svms"))
    op.assert_called_once_with(fields="status,svms")


def test_filter_on_explicit_field(op: MagicMock) -> None:
    match = _env("p1", ontapClusterProperties=OnPremClusterProperties(clusterUuid="u1"))
    other = _env("p2", ontapClusterProperties=OnPremClusterProperties(clusterUuid="u2"))
    op.return_value = [match, other]
    result = list(
        _ds().query(ResponseBody, cluster="c1").filter({"ontapClusterProperties.clusterUuid": "u1"})
    )
    assert result == [match]
    op.assert_called_once_with(fields="ontapClusterProperties")


def test_tenant_filter_not_sent(op: MagicMock) -> None:
    keep = _env("p1", tenantId="t1")
    op.return_value = [keep, _env("p2", tenantId="t2")]
    assert list(_ds().query(ResponseBody, cluster="c1").filter({"tenantId": "t1"})) == [keep]
    assert "tenant_id" not in op.call_args.kwargs


def test_get_by_public_id(op: MagicMock) -> None:
    op.return_value = [_env("pub-1"), _env("pub-2")]
    found = _ds().get(ResponseBody, cluster="c1", id="pub-1")
    assert found is not None
    assert found.publicId == "pub-1"
    assert op.call_count == 1


def test_get_missing_returns_none(op: MagicMock) -> None:
    op.return_value = [_env("pub-2")]
    assert _ds().get(ResponseBody, cluster="c1", id="pub-1") is None
    assert op.call_count == 1


def test_where_rejected_at_chain_time(op: MagicMock) -> None:
    with pytest.raises(ValueError, match="where"):
        _ds().query(ResponseBody, cluster="c1").where("name = 'x'")
    op.assert_not_called()


def test_path_params_rejected(op: MagicMock) -> None:
    with pytest.raises(ValueError, match="path_params"):
        _ds().query(ResponseBody, cluster="c1", path_params={"x": "y"})
    op.assert_not_called()
