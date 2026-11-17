"""Tests for OccmCollector and refresh_occm_cache (#1076, ADR-0030)."""

from __future__ import annotations

from pathlib import Path
from typing import Any
from unittest.mock import MagicMock

import pytest
import requests

from pynetappfoundry.cache.occm_collector import (
    OCCM_CACHED_MAPPINGS,
    OCCM_LIST_OPS,
    OccmCollector,
    refresh_occm_cache,
)
from pynetappfoundry.cache.occm_db import OccmCacheDB
from pynetappfoundry.clients.console.auth import ConsoleAuthError
from pynetappfoundry.console.discovery import AccountInventory, ConsoleInventory
from pynetappfoundry.models.console.cvo.get_onprem_working_environments import ResponseBody
from pynetappfoundry.models.console_types import ConsoleAgentInfo

_MAPPING = "OccmOnpremWorkingEnvironment"


def _inventory(*accounts: tuple[str | None, list[str]]) -> ConsoleInventory:
    return ConsoleInventory(
        accounts=[
            AccountInventory(
                scope=scope,
                agents=[
                    ConsoleAgentInfo(agentId=a, scope=scope, organization_id="org-1")
                    for a in agent_ids
                ],
            )
            for scope, agent_ids in accounts
        ]
    )


def _discovery(inventory: ConsoleInventory) -> MagicMock:
    discovery = MagicMock()
    discovery.discover.return_value = inventory
    return discovery


def _factory(envs: dict[str, list[str]], failing: dict[str, Exception] | None = None) -> MagicMock:
    """A client factory whose op lists the given public ids per agent id."""
    failing = failing or {}
    clients: dict[str, MagicMock] = {}

    def build(config: Any, agent_id: str, **kwargs: Any) -> MagicMock:
        if agent_id in failing and isinstance(failing[agent_id], ConsoleAuthError):
            raise failing[agent_id]
        client = MagicMock(name=f"client-{agent_id}")
        op = client.ops.list_onprem_working_environments
        if agent_id in failing:
            op.side_effect = failing[agent_id]
        else:
            op.return_value = [ResponseBody(publicId=p, name=f"n-{p}") for p in envs[agent_id]]
        clients[agent_id] = client
        return client

    factory = MagicMock(side_effect=build)
    factory.clients = clients
    return factory


def test_cached_mappings_and_ops() -> None:
    assert OCCM_CACHED_MAPPINGS == (_MAPPING,)
    assert OCCM_LIST_OPS == {
        "/occm/api/onprem/working-environments": "list_onprem_working_environments"
    }


def test_collect_passes_fields_star_and_dumps_json() -> None:
    factory = _factory({"a1": ["p1", "p2"]})
    config = MagicMock()
    snapshot = OccmCollector(
        config, discovery=_discovery(_inventory((None, ["a1"]))), agent_client_factory=factory
    ).collect()

    factory.clients["a1"].ops.list_onprem_working_environments.assert_called_once_with(fields="*")
    factory.assert_called_once_with(config, "a1")
    (agent,) = snapshot.agents
    assert [r["publicId"] for r in agent.records[_MAPPING]] == ["p1", "p2"]
    assert (agent.scope, agent.organization_id) == (None, "org-1")
    assert snapshot.failed_agents == ()


def test_scope_is_passed_only_for_scoped_agents() -> None:
    factory = _factory({"a1": [], "a2": []})
    config = MagicMock()
    OccmCollector(
        config,
        discovery=_discovery(_inventory((None, ["a1"]), ("A", ["a2"]))),
        agent_client_factory=factory,
    ).collect()
    assert [(c.args, c.kwargs) for c in factory.call_args_list] == [
        ((config, "a1"), {}),
        ((config, "a2"), {"scope": "A"}),
    ]


def test_agents_are_deduplicated_first_account_wins() -> None:
    factory = _factory({"a1": ["p1"]})
    snapshot = OccmCollector(
        MagicMock(),
        discovery=_discovery(_inventory(("A", ["a1"]), ("B", ["a1"]))),
        agent_client_factory=factory,
    ).collect()
    assert factory.call_count == 1
    assert [a.scope for a in snapshot.agents] == ["A"]


def test_unknown_mapping_raises() -> None:
    collector = OccmCollector(
        MagicMock(), discovery=_discovery(_inventory()), mappings=("NoSuchMapping",)
    )
    with pytest.raises(ValueError, match="Unknown OCCM mapping"):
        collector.collect()


def test_mapping_without_list_op_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("pynetappfoundry.cache.occm_collector.OCCM_LIST_OPS", {})
    collector = OccmCollector(MagicMock(), discovery=_discovery(_inventory()))
    with pytest.raises(ValueError, match="no list op"):
        collector.collect()


@pytest.mark.parametrize(
    "error",
    [
        requests.ConnectionError("down"),
        ConsoleAuthError("denied"),
        TypeError("bad"),
        ValueError("bad"),
    ],
)
def test_failing_agent_is_recorded_and_others_collected(error: Exception) -> None:
    factory = _factory({"a2": ["p2"]}, failing={"a1": error})
    snapshot = OccmCollector(
        MagicMock(),
        discovery=_discovery(_inventory((None, ["a1", "a2"]))),
        agent_client_factory=factory,
    ).collect()
    assert snapshot.failed_agents == ("a1",)
    assert [a.agent_id for a in snapshot.agents] == ["a2"]


def test_discovery_error_propagates_and_db_untouched(tmp_path: Path) -> None:
    discovery = MagicMock()
    discovery.discover.side_effect = requests.ConnectionError("no console")
    with OccmCacheDB(db_path=tmp_path / "occm_cache.db") as db:
        db.set(
            OccmCollector(
                MagicMock(),
                discovery=_discovery(_inventory((None, ["a1"]))),
                agent_client_factory=_factory({"a1": ["p1"]}),
            ).collect()
        )
        with pytest.raises(requests.ConnectionError):
            refresh_occm_cache(MagicMock(), db=db, discovery=discovery)
        assert db.list_agents() == ["a1"]
        assert db.agents_for_working_environment("p1") == ["a1"]


def test_refresh_with_injected_db(tmp_path: Path) -> None:
    with OccmCacheDB(db_path=tmp_path / "occm_cache.db") as db:
        snapshot = refresh_occm_cache(
            MagicMock(),
            db=db,
            discovery=_discovery(_inventory((None, ["a1"]))),
            agent_client_factory=_factory({"a1": ["p1"]}),
        )
        assert [a.agent_id for a in snapshot.agents] == ["a1"]
        assert db.agents_for_working_environment("p1") == ["a1"]
        assert [a.agent_id for a in db.agents()] == ["a1"]


def test_refresh_with_owned_db(tmp_path: Path) -> None:
    config = MagicMock()
    config.config_dir = tmp_path
    refresh_occm_cache(
        config,
        discovery=_discovery(_inventory((None, ["a1"]))),
        agent_client_factory=_factory({"a1": ["p1"]}),
    )
    with OccmCacheDB(db_path=tmp_path / ".cache" / "occm_cache.db") as db:
        assert db.working_environment_agents() == {"p1": ["a1"]}
