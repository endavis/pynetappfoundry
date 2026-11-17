"""Tests for Console discovery across accounts (#1078)."""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock

import pytest

from pynetappfoundry.console import ConsoleDiscovery, ConsoleInventory
from pynetappfoundry.models.console.tenancyv4 import get_organizations_resources as res
from pynetappfoundry.models.console_types import (
    ConsoleAgentInfo,
    ConsoleWorkingEnvironment,
    Organization,
)


def _org(org_id: str) -> Organization:
    return Organization(id=org_id, name=f"name-{org_id}", resourceClass="c", resourceType="t")


def _resource(rid: str, rtype: str, raw: str | None = None) -> res.Resource10GetResponseBody:
    return res.Resource10GetResponseBody.model_validate(
        {"id": rid, "name": f"we-{rid}", "rawId": raw, "resourceType": rtype, "state": "up"}
    )


def _fake_client(
    scope: str | None,
    orgs: list[str],
    resources: dict[str, list[res.Resource10GetResponseBody]],
    agents: dict[str, list[str]],
) -> MagicMock:
    client = MagicMock(name=f"client-{scope}")
    client.list_organizations.return_value = [_org(o) for o in orgs]
    client.list_organization_resources.side_effect = lambda org: resources.get(org, [])
    client.list_agents.side_effect = lambda org: [
        ConsoleAgentInfo(agentId=a, scope=scope, organization_id=org) for a in agents.get(org, [])
    ]
    return client


def _discovery(
    accounts: list[str | None], clients: dict[str | None, MagicMock]
) -> tuple[ConsoleDiscovery, MagicMock, MagicMock]:
    config = MagicMock()
    config.console_account_scopes.return_value = accounts
    factory = MagicMock(side_effect=lambda cfg, **kw: clients[kw.get("scope")])
    return ConsoleDiscovery(config, api_client_factory=factory), factory, config


def test_two_accounts_two_organizations_each_use_their_own_account() -> None:
    clients: dict[str | None, MagicMock] = {
        "A": _fake_client(
            "A", ["org-a"], {"org-a": [_resource("r1", "ON_PREM", "we-a")]}, {"org-a": ["agent-1"]}
        ),
        "B": _fake_client(
            "B", ["org-b"], {"org-b": [_resource("r2", "ON_PREM", "we-b")]}, {"org-b": ["agent-2"]}
        ),
    }
    discovery, factory, config = _discovery(["A", "B"], clients)

    inventory = discovery.discover()

    assert [call.kwargs for call in factory.call_args_list] == [{"scope": "A"}, {"scope": "B"}]
    assert all(call.args == (config,) for call in factory.call_args_list)
    clients["A"].list_agents.assert_called_once_with("org-a")
    clients["B"].list_agents.assert_called_once_with("org-b")
    clients["A"].list_organization_resources.assert_called_once_with("org-a")
    clients["B"].list_organization_resources.assert_called_once_with("org-b")
    assert [(a.scope, a.agent_id, a.organization_id) for a in inventory.agents()] == [
        ("A", "agent-1", "org-a"),
        ("B", "agent-2", "org-b"),
    ]
    assert [
        (w.scope, w.organization_id, w.public_id) for w in inventory.working_environments()
    ] == [
        ("A", "org-a", "we-a"),
        ("B", "org-b", "we-b"),
    ]
    assert [account.scope for account in inventory.accounts] == ["A", "B"]


def test_root_account_builds_the_client_without_a_scope_keyword() -> None:
    clients: dict[str | None, MagicMock] = {None: _fake_client(None, ["org-root"], {}, {})}
    discovery, factory, config = _discovery([None], clients)

    inventory = discovery.discover_account(None)

    factory.assert_called_once_with(config)
    assert inventory.scope is None
    assert [o.id for o in inventory.organizations] == ["org-root"]


def test_only_on_prem_resources_are_working_environments() -> None:
    resources = {
        "org-a": [
            _resource("r1", "ON_PREM", "raw-1"),
            _resource("r2", "VOLUME", "raw-2"),
            _resource("r3", "ON_PREM", "raw-3"),
        ]
    }
    clients: dict[str | None, MagicMock] = {"A": _fake_client("A", ["org-a"], resources, {})}
    discovery, _, _ = _discovery(["A"], clients)

    envs = discovery.discover_account("A").working_environments

    assert [(e.id, e.public_id) for e in envs] == [("r1", "raw-1"), ("r3", "raw-3")]
    assert all(isinstance(e, ConsoleWorkingEnvironment) for e in envs)


def test_account_without_organizations_gives_an_empty_inventory() -> None:
    clients: dict[str | None, MagicMock] = {"A": _fake_client("A", [], {}, {})}
    discovery, _, _ = _discovery(["A"], clients)

    inventory = discovery.discover_account("A")

    assert inventory.organizations == []
    assert inventory.agents == []
    assert inventory.working_environments == []
    clients["A"].list_agents.assert_not_called()


def test_errors_propagate() -> None:
    client = _fake_client("A", ["org-a"], {}, {})
    client.list_agents.side_effect = RuntimeError("boom")
    discovery, _, _ = _discovery(["A"], {"A": client})

    with pytest.raises(RuntimeError, match="boom"):
        discovery.discover()


def test_a_failing_account_is_not_skipped() -> None:
    good = _fake_client("A", ["org-a"], {}, {})
    bad = _fake_client("B", [], {}, {})
    bad.list_organizations.side_effect = RuntimeError("denied")
    discovery, _, _ = _discovery(["A", "B"], {"A": good, "B": bad})

    with pytest.raises(RuntimeError, match="denied"):
        discovery.discover()


def test_accounts_come_from_the_config() -> None:
    discovery, _, _ = _discovery([None, "A"], {})
    assert discovery.accounts() == [None, "A"]


def test_empty_inventory_has_empty_helpers() -> None:
    inventory = ConsoleInventory()
    assert inventory.agents() == []
    assert inventory.working_environments() == []


def test_default_factory_is_the_api_client(monkeypatch: pytest.MonkeyPatch) -> None:
    built: list[tuple[Any, dict[str, Any]]] = []

    def fake(config: Any, **kwargs: Any) -> MagicMock:
        built.append((config, kwargs))
        return _fake_client(kwargs.get("scope"), [], {}, {})

    monkeypatch.setattr("pynetappfoundry.console.discovery.ConsoleAPIClient", fake)
    config = MagicMock()
    config.console_account_scopes.return_value = ["A"]

    ConsoleDiscovery(config).discover()

    assert built == [(config, {"scope": "A"})]
