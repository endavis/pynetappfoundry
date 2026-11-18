"""The OCCM backend uses a connector's scope Console account (#1080)."""

from __future__ import annotations

from collections.abc import Iterator
from datetime import UTC, datetime
from pathlib import Path
from unittest.mock import MagicMock, PropertyMock, patch

import pytest

from pynetappfoundry.cache.occm.onprem_working_environments.mapping import (
    OCCMONPREMWORKINGENVIRONMENT_MAPPING as MAPPING,
)
from pynetappfoundry.cache.occm_collector import OccmSnapshot
from pynetappfoundry.cache.occm_db import OccmCacheDB
from pynetappfoundry.console.discovery import AccountInventory, ConsoleInventory
from pynetappfoundry.data._routing import RoutingDecision
from pynetappfoundry.data.occm_backend import OccmBackend
from pynetappfoundry.models.console.cvo.get_onprem_working_environments import ResponseBody
from pynetappfoundry.models.console_types import ConsoleAgentInfo

_CLIENT_PATH = "pynetappfoundry.clients.console.agent.ConsoleAgentClient"
_REAL_CACHE_EXISTS = OccmBackend._cache_exists  # before the autouse fixture patches it
_LIVE = RoutingDecision(cache_fields=(), live_fields=("name", "publicId"))


def _config(scopes: dict[str, str | None]) -> MagicMock:
    config = MagicMock()
    config.data = {"connectors": {name: {"agent_id": f"agent-{name}"} for name in scopes}}
    config.get_scope.side_effect = lambda data_type, name: scopes.get(name)
    return config


@pytest.fixture(autouse=True)
def _empty_occm_cache(tmp_path: Path) -> Iterator[None]:
    """Raw agent ids look up their owning scope in the cache; give them an empty one (#1083)."""
    with (
        OccmCacheDB(db_path=tmp_path / "occm_cache.db") as db,
        patch.object(OccmBackend, "_cache_db", db),
        patch.object(OccmBackend, "_cache_exists", return_value=True),
    ):
        yield


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


def _cache_agents(backend: OccmBackend, *agents: ConsoleAgentInfo) -> None:
    by_scope: dict[str | None, list[ConsoleAgentInfo]] = {}
    for agent in agents:
        by_scope.setdefault(agent.scope, []).append(agent)
    inventory = ConsoleInventory(
        accounts=[AccountInventory(scope=s, agents=a) for s, a in by_scope.items()]
    )
    backend._cache_db.set(OccmSnapshot(cached_at=datetime.now(UTC), inventory=inventory, agents=()))


def _info(agent_id: str, name: str, scope: str | None, status: str = "active") -> ConsoleAgentInfo:
    return ConsoleAgentInfo(agentId=agent_id, name=name, status=status, scope=scope)


def _nameless_config(scopes: dict[str, str | None], **extra: object) -> MagicMock:
    config = MagicMock()
    config.data = {"connectors": {name: dict(extra) for name in scopes}}
    config.get_scope.side_effect = lambda data_type, name: scopes.get(name)
    return config


def test_connector_without_agent_id_resolves_by_name_in_its_scope(client_cls: MagicMock) -> None:
    backend = OccmBackend(_nameless_config({"c1": "Org1"}))
    _cache_agents(backend, _info("found-1", "c1", "Org1"), _info("other", "c1", None))
    _query(backend, "c1")
    assert client_cls.call_args.args[1] == "found-1"
    assert client_cls.call_args.kwargs == {"scope": "Org1"}


def test_root_connector_without_agent_id_resolves_in_root(client_cls: MagicMock) -> None:
    backend = OccmBackend(_nameless_config({"c1": None}))
    _cache_agents(backend, _info("root-1", "c1", None), _info("org-1", "c1", "Org1"))
    _query(backend, "c1")
    assert client_cls.call_args.args[1] == "root-1"
    assert client_cls.call_args.kwargs == {}


def test_blank_agent_id_resolves_by_name(client_cls: MagicMock) -> None:
    backend = OccmBackend(_nameless_config({"c1": None}, agent_id="  "))
    _cache_agents(backend, _info("root-1", "c1", None))
    _query(backend, "c1")
    assert client_cls.call_args.args[1] == "root-1"


def test_name_only_in_another_scope_raises(client_cls: MagicMock) -> None:
    backend = OccmBackend(_nameless_config({"c1": "Org1"}))
    _cache_agents(backend, _info("other", "c1", "Org2"))
    with pytest.raises(ValueError, match=r"connectors\.c1.*'Org1'"):
        _query(backend, "c1")
    client_cls.assert_not_called()


def test_empty_cache_raises_pointing_at_refresh(client_cls: MagicMock) -> None:
    backend = OccmBackend(_nameless_config({"c1": None}))
    with pytest.raises(ValueError, match=r"connectors\.c1.*no agents.*nf cache occm refresh"):
        _query(backend, "c1")
    client_cls.assert_not_called()


def test_duplicate_names_in_scope_raise_naming_both_ids(client_cls: MagicMock) -> None:
    backend = OccmBackend(_nameless_config({"c1": None}))
    _cache_agents(backend, _info("id-a", "c1", None), _info("id-b", "c1", None, "inactive"))
    with pytest.raises(ValueError, match=r"id-a \(status active\), id-b \(status inactive\)"):
        _query(backend, "c1")
    client_cls.assert_not_called()


def test_connector_with_agent_id_does_not_read_the_cache(client_cls: MagicMock) -> None:
    backend = OccmBackend(_config({"c1": None}))
    with patch.object(OccmBackend, "_cache_db", MagicMock(side_effect=AssertionError)) as db:
        _query(backend, "c1")
    assert client_cls.call_args.args[1] == "agent-c1"
    assert db.method_calls == []


def test_raw_id_cached_in_one_scope_uses_that_scope(client_cls: MagicMock) -> None:
    backend = OccmBackend(_config({"c1": None}))
    _cache_agents(backend, _info("raw-agent", "x", "Org1"))
    _query(backend, "raw-agent")
    assert client_cls.call_args.kwargs == {"scope": "Org1"}


def test_raw_id_cached_in_root_and_a_scope_uses_root(client_cls: MagicMock) -> None:
    backend = OccmBackend(_config({"c1": None}))
    _cache_agents(backend, _info("raw-agent", "x", None), _info("raw-agent", "x", "Org1"))
    _query(backend, "raw-agent")
    assert client_cls.call_args.kwargs == {}


def test_raw_id_cached_in_two_scopes_raises(client_cls: MagicMock) -> None:
    backend = OccmBackend(_config({"c1": None}))
    _cache_agents(backend, _info("raw-agent", "x", "Org1"), _info("raw-agent", "x", "Org2"))
    with pytest.raises(ValueError, match=r"raw-agent.*Org1, Org2.*\[connectors\]"):
        _query(backend, "raw-agent")
    client_cls.assert_not_called()


def test_missing_cache_file_gives_root_and_creates_no_file(
    client_cls: MagicMock, tmp_path: Path
) -> None:
    config = _config({"c1": "Org1"})
    config.config_dir = tmp_path
    backend = OccmBackend(config)
    with (
        patch.object(OccmBackend, "_cache_exists", _REAL_CACHE_EXISTS),
        patch.object(
            OccmBackend, "_cache_db", new_callable=PropertyMock, side_effect=AssertionError
        ),
    ):
        _query(backend, "raw-agent")
    assert client_cls.call_args.kwargs == {}
    assert not (tmp_path / ".cache").exists()


def test_missing_cache_file_gives_the_refresh_error_and_creates_no_file(
    client_cls: MagicMock, tmp_path: Path
) -> None:
    config = _nameless_config({"c1": None})
    config.config_dir = tmp_path
    backend = OccmBackend(config)
    with (
        patch.object(OccmBackend, "_cache_exists", _REAL_CACHE_EXISTS),
        patch.object(
            OccmBackend, "_cache_db", new_callable=PropertyMock, side_effect=AssertionError
        ),
        pytest.raises(ValueError, match=r"connectors\.c1.*nf cache occm refresh"),
    ):
        _query(backend, "c1")
    assert not (tmp_path / ".cache").exists()
