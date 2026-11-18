"""Tests for OccmCacheDB (#1076, ADR-0030)."""

from __future__ import annotations

import sqlite3
from collections.abc import Iterator
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock

import pytest

from pynetappfoundry.cache.occm_collector import OccmAgentSnapshot, OccmSnapshot
from pynetappfoundry.cache.occm_db import OccmCacheDB
from pynetappfoundry.console.discovery import AccountInventory, ConsoleInventory
from pynetappfoundry.models.console_types import (
    ConsoleAgentInfo,
    ConsoleWorkingEnvironment,
    Organization,
)

_MAPPING = "OccmOnpremWorkingEnvironment"


def _agent_snapshot(
    agent_id: str,
    records: list[dict[str, Any]],
    *,
    cached_at: datetime | None = None,
    scope: str | None = None,
) -> OccmAgentSnapshot:
    return OccmAgentSnapshot(
        agent_id=agent_id,
        scope=scope,
        organization_id="org-1",
        cached_at=cached_at or datetime.now(UTC),
        records={_MAPPING: records},
    )


def _snapshot(
    agents: list[OccmAgentSnapshot],
    *,
    failed: tuple[str, ...] = (),
    skipped: tuple[str, ...] = (),
    inventory: ConsoleInventory | None = None,
) -> OccmSnapshot:
    return OccmSnapshot(
        cached_at=datetime.now(UTC),
        inventory=inventory or ConsoleInventory(),
        agents=tuple(agents),
        failed_agents=failed,
        skipped_agents=skipped,
    )


def _we(public_id: str, **extra: Any) -> dict[str, Any]:
    return {"publicId": public_id, "name": f"n-{public_id}", **extra}


@pytest.fixture
def db(tmp_path: Path) -> Iterator[OccmCacheDB]:
    with OccmCacheDB(db_path=tmp_path / "occm_cache.db") as database:
        yield database


def test_schema_version_and_tables(db: OccmCacheDB) -> None:
    assert OccmCacheDB.SCHEMA_VERSION == 1
    tables = {
        r["name"] for r in db.conn.execute("SELECT name FROM sqlite_master WHERE type = 'table'")
    }
    assert {"occm_collections", "occm_records", "occm_inventory"} <= tables


def test_config_path_creates_cache_file(tmp_path: Path) -> None:
    config = MagicMock()
    config.config_dir = tmp_path
    with OccmCacheDB(config=config):
        pass
    assert (tmp_path / ".cache" / "occm_cache.db").exists()


def test_requires_path_or_config() -> None:
    with pytest.raises(ValueError, match="db_path or config"):
        OccmCacheDB()


def test_uri_path(tmp_path: Path) -> None:
    uri = f"file:{tmp_path / 'u.db'}"
    with OccmCacheDB(db_path=uri) as database:
        database.set(_snapshot([_agent_snapshot("a1", [_we("p1")])]))
        assert database.is_collected("a1", _MAPPING)


def test_round_trip_and_filters(db: OccmCacheDB) -> None:
    records = [
        _we("p1", ontapClusterProperties={"clusterUuid": "u1"}, isHa=True),
        _we("p2", ontapClusterProperties={"clusterUuid": "u2"}, isHa=False, status=None),
    ]
    db.set(_snapshot([_agent_snapshot("a1", records)]))

    assert [r["publicId"] for r in db.query_records("a1", _MAPPING, {})] == ["p1", "p2"]
    dotted = db.query_records("a1", _MAPPING, {"ontapClusterProperties.clusterUuid": "u2"})
    assert [r["publicId"] for r in dotted] == ["p2"]
    assert [r["publicId"] for r in db.query_records("a1", _MAPPING, {"status": None})] == [
        "p1",
        "p2",
    ]
    assert [r["publicId"] for r in db.query_records("a1", _MAPPING, {"isHa": True})] == ["p1"]
    assert db.query_records("other", _MAPPING, {}) == []


def test_list_filter_value_rejected(db: OccmCacheDB) -> None:
    with pytest.raises(ValueError, match="scalar"):
        db.query_records("a1", _MAPPING, {"name": ["x"]})


def test_key_with_quote_matches_nothing(db: OccmCacheDB) -> None:
    db.set(_snapshot([_agent_snapshot("a1", [_we("p1")])]))
    assert db.query_records("a1", _MAPPING, {'na"me': "x"}) == []


def test_set_replaces_agent_records(db: OccmCacheDB) -> None:
    db.set(_snapshot([_agent_snapshot("a1", [_we("p1"), _we("p2")])]))
    db.set(_snapshot([_agent_snapshot("a1", [_we("p3")])]))
    assert [r["publicId"] for r in db.query_records("a1", _MAPPING, {})] == ["p3"]


def test_agents_no_longer_discovered_are_pruned(db: OccmCacheDB) -> None:
    db.set(_snapshot([_agent_snapshot("a1", [_we("p1")]), _agent_snapshot("a2", [_we("p2")])]))
    db.set(_snapshot([_agent_snapshot("a1", [_we("p1")])]))
    assert db.list_agents() == ["a1"]
    assert db.query_records("a2", _MAPPING, {}) == []


def test_failed_agent_keeps_rows_and_cached_at(db: OccmCacheDB) -> None:
    old = datetime.now(UTC) - timedelta(days=40)
    db.set(_snapshot([_agent_snapshot("a1", [_we("p1")], cached_at=old)]))
    db.set(_snapshot([], failed=("a1",)))
    assert [r["publicId"] for r in db.query_records("a1", _MAPPING, {})] == ["p1"]
    assert db.is_stale("a1") is True


def test_skipped_agent_keeps_rows(db: OccmCacheDB) -> None:
    old = datetime.now(UTC) - timedelta(days=40)
    db.set(_snapshot([_agent_snapshot("a1", [_we("p1")], cached_at=old)]))
    db.set(_snapshot([], skipped=("a1",)))
    assert db.list_agents() == ["a1"]
    assert [r["publicId"] for r in db.query_records("a1", _MAPPING, {})] == ["p1"]
    assert db.is_stale("a1") is True


def test_agents_for_working_environment(db: OccmCacheDB) -> None:
    db.set(
        _snapshot(
            [
                _agent_snapshot("b-agent", [_we("shared"), _we("only-b")]),
                _agent_snapshot("a-agent", [_we("shared")]),
            ]
        )
    )
    assert db.agents_for_working_environment("shared") == ["a-agent", "b-agent"]
    assert db.agents_for_working_environment("only-b") == ["b-agent"]
    assert db.agents_for_working_environment("missing") == []
    assert db.working_environment_agents() == {
        "only-b": ["b-agent"],
        "shared": ["a-agent", "b-agent"],
    }


def _inventory(scope: str | None, org: str, agent: str, env: str) -> ConsoleInventory:
    return ConsoleInventory(
        accounts=[
            AccountInventory(
                scope=scope,
                organizations=[
                    Organization(id=org, name="Org", resourceClass="c", resourceType="t")
                ],
                agents=[
                    ConsoleAgentInfo(
                        agentId=agent, name="ag", status="active", scope=scope, organization_id=org
                    )
                ],
                working_environments=[
                    ConsoleWorkingEnvironment(
                        id=env,
                        name="we",
                        rawId="raw-1",
                        resourceType="ON_PREM",
                        state="up",
                        scope=scope,
                        organization_id=org,
                    )
                ],
            )
        ]
    )


def test_inventory_round_trip_keeps_scope_and_organization(db: OccmCacheDB) -> None:
    inventory = _inventory("A", "org-a", "agent-1", "env-1")
    db.set(_snapshot([], inventory=inventory))

    assert db.organizations() == inventory.accounts[0].organizations
    assert db.agents() == inventory.agents()
    assert db.working_environments() == inventory.working_environments()
    agent = db.agents()[0]
    assert (agent.scope, agent.organization_id) == ("A", "org-a")
    env = db.working_environments()[0]
    assert (env.public_id, env.scope, env.organization_id) == ("raw-1", "A", "org-a")


def test_inventory_replaced_on_each_set(db: OccmCacheDB) -> None:
    db.set(_snapshot([], inventory=_inventory("A", "org-a", "agent-1", "env-1")))
    db.set(_snapshot([], inventory=_inventory(None, "org-b", "agent-2", "env-2")))
    assert [o.id for o in db.organizations()] == ["org-b"]
    assert [a.agent_id for a in db.agents()] == ["agent-2"]
    assert [w.id for w in db.working_environments()] == ["env-2"]


def test_is_stale(db: OccmCacheDB) -> None:
    assert db.is_stale("a1") is None
    db.set(_snapshot([_agent_snapshot("a1", [_we("p1")])]))
    assert db.is_stale("a1") is False
    assert db.is_stale("a1", ttl_days=0) is True


def test_is_collected(db: OccmCacheDB) -> None:
    db.set(_snapshot([_agent_snapshot("a1", [])]))
    assert db.is_collected("a1", _MAPPING)
    assert not db.is_collected("a2", _MAPPING)


def test_clear_one_agent_keeps_the_rest(db: OccmCacheDB) -> None:
    db.set(
        _snapshot(
            [_agent_snapshot("a1", [_we("p1")]), _agent_snapshot("a2", [_we("p2"), _we("p3")])],
            inventory=_inventory(None, "org-a", "a1", "env-1"),
        )
    )
    assert db.clear("a2") == 2
    assert db.list_agents() == ["a1"]
    assert len(db.organizations()) == 1


def test_full_clear_empties_inventory_too(db: OccmCacheDB) -> None:
    db.set(
        _snapshot(
            [_agent_snapshot("a1", [_we("p1")])],
            inventory=_inventory(None, "org-a", "a1", "env-1"),
        )
    )
    assert db.clear() == 1
    assert db.list_agents() == []
    assert db.organizations() == []
    assert db.agents() == []


def test_set_is_one_transaction(db: OccmCacheDB) -> None:
    db.set(_snapshot([_agent_snapshot("a1", [_we("p1")])]))
    bad = _agent_snapshot("a2", [{"publicId": "p2", "bad": object()}])
    # json.dumps(default=str) copes with the object, so break the insert itself.
    db.conn.execute("DROP TABLE occm_collections")
    with pytest.raises(sqlite3.OperationalError):
        db.set(_snapshot([bad]))
    assert db.query_records("a2", _MAPPING, {}) == []


def _scoped_inventory(*scopes: str | None) -> ConsoleInventory:
    return ConsoleInventory(
        accounts=[
            AccountInventory(
                scope=s,
                organizations=[
                    Organization(id=f"org-{s}", name=f"o-{s}", resourceClass="C", resourceType="T")
                ],
            )
            for s in scopes
        ]
    )


def test_scoped_set_keeps_other_scopes(db: OccmCacheDB) -> None:
    db.set(
        _snapshot(
            [
                _agent_snapshot("root1", [_we("p0")], scope=None),
                _agent_snapshot("a1", [_we("p1")], scope="prod"),
                _agent_snapshot("a2", [_we("p2")], scope="prod"),
            ],
            inventory=_scoped_inventory(None, "prod"),
        )
    )
    scoped = OccmSnapshot(
        cached_at=datetime.now(UTC),
        inventory=_scoped_inventory("prod"),
        agents=(_agent_snapshot("a1", [_we("p1b")], scope="prod"),),
        scopes=("prod",),
    )
    db.set(scoped)
    assert db.list_agents() == ["a1", "root1"]
    assert db.agents_for_working_environment("p0") == ["root1"]
    assert db.agents_for_working_environment("p1b") == ["a1"]
    assert [o.id for o in db.organizations()] == ["org-None", "org-prod"]


def test_scoped_set_root_scope_prunes_only_root(db: OccmCacheDB) -> None:
    db.set(
        _snapshot(
            [
                _agent_snapshot("root1", [_we("p0")], scope=None),
                _agent_snapshot("a1", [_we("p1")], scope="prod"),
            ]
        )
    )
    db.set(
        OccmSnapshot(
            cached_at=datetime.now(UTC),
            inventory=_scoped_inventory(None),
            scopes=(None,),
        )
    )
    assert db.list_agents() == ["a1"]


def test_agent_status_values_and_staleness(db: OccmCacheDB) -> None:
    old = datetime.now(UTC) - timedelta(days=40)
    db.set(
        _snapshot(
            [
                _agent_snapshot("b", [_we("p1"), _we("p2")], cached_at=old, scope="prod"),
                _agent_snapshot("a", [_we("p3")]),
            ]
        )
    )
    statuses = db.agent_status()
    assert [s.agent_id for s in statuses] == ["a", "b"]
    a, b = statuses
    assert (a.scope, a.mapping_count, a.record_count, a.is_stale) == (None, 1, 1, False)
    assert (b.scope, b.record_count, b.is_stale) == ("prod", 2, True)
    assert b.oldest_cached_at == old
    assert not db.agent_status(ttl_days=50)[1].is_stale


def test_agent_status_empty(db: OccmCacheDB) -> None:
    assert db.agent_status() == []


def _agent(agent_id: str, name: str, scope: str | None, org: str | None) -> ConsoleAgentInfo:
    return ConsoleAgentInfo(
        agentId=agent_id, name=name, status="active", scope=scope, organization_id=org
    )


def _agents_db(db: OccmCacheDB, *agents: ConsoleAgentInfo) -> None:
    by_scope: dict[str | None, list[ConsoleAgentInfo]] = {}
    for agent in agents:
        by_scope.setdefault(agent.scope, []).append(agent)
    accounts = [AccountInventory(scope=s, agents=a) for s, a in by_scope.items()]
    db.set(_snapshot([], inventory=ConsoleInventory(accounts=accounts)))


def test_agents_named_matches_exactly_within_scope(db: OccmCacheDB) -> None:
    _agents_db(
        db,
        _agent("a1", "conn", None, None),
        _agent("a2", "conn", "Org1", "o1"),
        _agent("a3", "Conn", None, None),
    )
    assert [a.agent_id for a in db.agents_named("conn", scope=None)] == ["a1"]
    assert [a.agent_id for a in db.agents_named("conn", scope="Org1")] == ["a2"]
    assert db.agents_named("conn", scope="Other") == []


def test_agents_named_deduplicates_across_organizations(db: OccmCacheDB) -> None:
    _agents_db(db, _agent("a1", "conn", "A", "o1"), _agent("a1", "conn", "A", "o2"))
    assert [a.agent_id for a in db.agents_named("conn", scope="A")] == ["a1"]


def test_agents_named_on_empty_cache(db: OccmCacheDB) -> None:
    assert db.agents_named("conn", scope=None) == []


def test_agent_scopes(db: OccmCacheDB) -> None:
    _agents_db(
        db,
        _agent("a1", "x", None, None),
        _agent("a1", "x", "Org1", "o1"),
        _agent("a1", "x", "Org1", "o2"),
        _agent("a2", "y", "Org2", "o3"),
    )
    assert db.agent_scopes("a1") == [None, "Org1"]
    assert db.agent_scopes("a2") == ["Org2"]
    assert db.agent_scopes("missing") == []
