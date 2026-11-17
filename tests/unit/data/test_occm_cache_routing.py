"""Cache-backed DataSource queries on the OCCM backend (#1076, ADR-0030)."""

from __future__ import annotations

from collections.abc import Iterator
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from pynetappfoundry.cache.field_mapping import TypeMapping
from pynetappfoundry.cache.occm_collector import OccmAgentSnapshot, OccmSnapshot
from pynetappfoundry.cache.occm_db import OccmCacheDB
from pynetappfoundry.console.discovery import ConsoleInventory
from pynetappfoundry.data._routing import RoutingDecision
from pynetappfoundry.data.occm_backend import OccmBackend
from pynetappfoundry.data.source import DataSource
from pynetappfoundry.models.console.cvo.get_onprem_working_environments import ResponseBody

_CLIENT_PATH = "pynetappfoundry.clients.console.agent.ConsoleAgentClient"
_MAPPING = "OccmOnpremWorkingEnvironment"


def _env(public_id: str, **extra: Any) -> dict[str, Any]:
    return ResponseBody(publicId=public_id, name=f"n-{public_id}", **extra).model_dump(mode="json")


def _config(connectors: dict[str, Any] | None = None) -> MagicMock:
    config = MagicMock()
    config.data = {"connectors": connectors or {"c1": {"agent_id": "agent-1"}}}
    return config


@pytest.fixture
def cache_db(tmp_path: Path) -> Iterator[OccmCacheDB]:
    with (
        OccmCacheDB(db_path=tmp_path / "occm_cache.db") as db,
        patch.object(OccmBackend, "_cache_db", db),
    ):
        yield db


@pytest.fixture
def collected(cache_db: OccmCacheDB) -> OccmCacheDB:
    cache_db.set(
        OccmSnapshot(
            cached_at=datetime.now(UTC),
            inventory=ConsoleInventory(),
            agents=(
                OccmAgentSnapshot(
                    agent_id="agent-1",
                    scope=None,
                    organization_id=None,
                    cached_at=datetime.now(UTC),
                    records={_MAPPING: [_env("p1", tenantId="t1"), _env("p2", tenantId="t2")]},
                ),
            ),
        )
    )
    return cache_db


@pytest.fixture
def client_cls() -> Iterator[MagicMock]:
    with patch(_CLIENT_PATH) as cls:
        cls.return_value.ops.list_onprem_working_environments.return_value = []
        yield cls


def _op(client_cls: MagicMock) -> MagicMock:
    op: MagicMock = client_cls.return_value.ops.list_onprem_working_environments
    return op


def test_cache_source_returns_parsed_records_without_client(
    collected: OccmCacheDB, client_cls: MagicMock
) -> None:
    results = list(DataSource(_config()).query(ResponseBody, cluster="c1", source="cache"))
    assert [(r.publicId, r.name) for r in results] == [("p1", "n-p1"), ("p2", "n-p2")]
    client_cls.assert_not_called()


def test_cluster_may_be_a_raw_agent_id(collected: OccmCacheDB, client_cls: MagicMock) -> None:
    results = list(DataSource(_config()).query(ResponseBody, cluster="agent-1", source="cache"))
    assert len(results) == 2
    client_cls.assert_not_called()


def test_connector_without_agent_id_raises(collected: OccmCacheDB, client_cls: MagicMock) -> None:
    ds = DataSource(_config({"c1": {}}))
    with pytest.raises(ValueError, match=r"connectors\.c1"):
        list(ds.query(ResponseBody, cluster="c1", source="cache"))
    client_cls.assert_not_called()


def test_cache_filter_uses_json_path(collected: OccmCacheDB, client_cls: MagicMock) -> None:
    results = list(
        DataSource(_config())
        .query(ResponseBody, cluster="c1", source="cache")
        .filter({"tenantId": "t2"})
    )
    assert [r.publicId for r in results] == ["p2"]
    client_cls.assert_not_called()


def test_auto_on_collected_agent_makes_no_live_call(
    collected: OccmCacheDB, client_cls: MagicMock
) -> None:
    results = list(DataSource(_config()).query(ResponseBody, cluster="c1"))
    assert len(results) == 2
    client_cls.assert_not_called()


def test_auto_on_uncollected_agent_falls_back_to_live_once(
    cache_db: OccmCacheDB, client_cls: MagicMock
) -> None:
    _op(client_cls).return_value = [ResponseBody(publicId="live-1", name="n")]
    results = list(DataSource(_config()).query(ResponseBody, cluster="c1"))
    assert [r.publicId for r in results] == ["live-1"]
    _op(client_cls).assert_called_once_with()


def test_get_reads_the_cache(collected: OccmCacheDB, client_cls: MagicMock) -> None:
    found = DataSource(_config()).get(ResponseBody, cluster="c1", id="p2")
    assert found is not None
    assert found.name == "n-p2"
    client_cls.assert_not_called()


def test_partial_decision_goes_live_once_with_the_union_of_fields(
    collected: OccmCacheDB, client_cls: MagicMock
) -> None:
    decision = RoutingDecision(cache_fields=("name",), live_fields=("status",))
    _op(client_cls).return_value = [ResponseBody(publicId="live-1", name="n")]
    results = OccmBackend(_config()).query(
        ResponseBody, DataSource._resolve_mapping(ResponseBody), decision, "c1", {}
    )
    assert [r.publicId for r in results] == ["live-1"]
    _op(client_cls).assert_called_once_with(fields="status")


def test_cache_filter_on_explicit_fetch_path(collected: OccmCacheDB, client_cls: MagicMock) -> None:
    collected.set(
        OccmSnapshot(
            cached_at=datetime.now(UTC),
            inventory=ConsoleInventory(),
            agents=(
                OccmAgentSnapshot(
                    agent_id="agent-1",
                    scope=None,
                    organization_id=None,
                    cached_at=datetime.now(UTC),
                    records={
                        _MAPPING: [
                            _env("p1", ontapClusterProperties={"clusterUuid": "u1"}),
                            _env("p2", ontapClusterProperties={"clusterUuid": "u2"}),
                        ]
                    },
                ),
            ),
        )
    )
    results = list(
        DataSource(_config())
        .query(ResponseBody, cluster="c1", source="cache")
        .filter({"ontapClusterProperties.clusterUuid": "u2"})
    )
    assert [r.publicId for r in results] == ["p2"]
    client_cls.assert_not_called()


def test_is_live_only_for_a_mapping_that_is_not_cached() -> None:
    mapping = DataSource._resolve_mapping(ResponseBody)
    stub = TypeMapping(
        name="Other",
        model_class=ResponseBody,
        api_endpoint="/occm/api/other",
        api_type="occm",
        fields=mapping.fields,
    )
    assert OccmBackend.is_live_only(stub) is True
    assert OccmBackend.is_live_only(mapping) is False
    decision = RoutingDecision(cache_fields=("name",), live_fields=())
    with pytest.raises(NotImplementedError, match="only OccmOnpremWorkingEnvironment"):
        OccmBackend(_config()).query(ResponseBody, stub, decision, "c1", {})
