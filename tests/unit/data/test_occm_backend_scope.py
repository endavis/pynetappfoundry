"""The OCCM backend uses a connector's scope Console account (#1080)."""

from __future__ import annotations

from collections.abc import Iterator
from unittest.mock import MagicMock, patch

import pytest

from pynetappfoundry.cache.occm.onprem_working_environments.mapping import (
    OCCMONPREMWORKINGENVIRONMENT_MAPPING as MAPPING,
)
from pynetappfoundry.data._routing import RoutingDecision
from pynetappfoundry.data.occm_backend import OccmBackend
from pynetappfoundry.models.console.cvo.get_onprem_working_environments import ResponseBody

_CLIENT_PATH = "pynetappfoundry.clients.console.agent.ConsoleAgentClient"
_LIVE = RoutingDecision(cache_fields=(), live_fields=("name", "publicId"))


def _config(scopes: dict[str, str | None]) -> MagicMock:
    config = MagicMock()
    config.data = {"connectors": {name: {"agent_id": f"agent-{name}"} for name in scopes}}
    config.get_scope.side_effect = lambda data_type, name: scopes.get(name)
    return config


@pytest.fixture
def client_cls() -> Iterator[MagicMock]:
    with patch(_CLIENT_PATH) as cls:
        cls.return_value.ops.list_onprem_working_environments.return_value = []
        yield cls


def _query(backend: OccmBackend, cluster: str) -> None:
    backend.query(ResponseBody, MAPPING, _LIVE, cluster, {})


def test_scoped_connector_client_gets_scope(client_cls: MagicMock) -> None:
    backend = OccmBackend(_config({"c1": "Org1"}))
    _query(backend, "c1")
    assert client_cls.call_args.args[1] == "agent-c1"
    assert client_cls.call_args.kwargs == {"scope": "Org1"}


def test_root_connector_passes_no_scope_keyword(client_cls: MagicMock) -> None:
    backend = OccmBackend(_config({"c1": None}))
    _query(backend, "c1")
    assert client_cls.call_args.kwargs == {}


def test_raw_agent_id_passes_no_scope_keyword(client_cls: MagicMock) -> None:
    backend = OccmBackend(_config({"c1": "Org1"}))
    _query(backend, "raw-agent")
    assert client_cls.call_args.args[1] == "raw-agent"
    assert client_cls.call_args.kwargs == {}


def test_client_cache_is_keyed_per_scope(client_cls: MagicMock) -> None:
    config = _config({"c1": "Org1", "c2": "Org2", "c3": None})
    config.data["connectors"]["c2"]["agent_id"] = "agent-c1"
    config.data["connectors"]["c3"]["agent_id"] = "agent-c1"
    backend = OccmBackend(config)
    _query(backend, "c1")
    _query(backend, "c1")
    assert client_cls.call_count == 1
    _query(backend, "c2")
    _query(backend, "c3")
    # same agent id under three different scopes: three clients
    assert client_cls.call_count == 3
    assert set(backend._api_clients) == {
        ("Org1", "agent-c1"),
        ("Org2", "agent-c1"),
        (None, "agent-c1"),
    }
