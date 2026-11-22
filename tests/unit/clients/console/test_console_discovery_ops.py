"""Tests for the organization-resources, list-connectors and get-agent operations (#1078)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, cast
from unittest.mock import MagicMock, patch

import pytest
from pydantic import SecretStr

from pynetappfoundry.clients.console.api import ConsoleAPIClient
from pynetappfoundry.core.models import ConsoleAPISettings
from pynetappfoundry.models.console.agentsmgmt import get_agent, get_list_connectors
from pynetappfoundry.models.console_types import ConsoleAgentInfo

_HOST = "https://api.bluexp.netapp.com"

# Shaped like the lab probes of #1078, with placeholder values.
_OCCM = {
    "agent": {
        "agentId": "agent-1clients",
        "agentType": "connector",
        "clientInfraStatus": None,
        "creatorUserId": "user-1",
        "name": "agent-name",
        "network": None,
        "provider": "aws",
        "region": "us-east-1",
        "status": None,
        "subnet": None,
        "systemId": "system-1",
        "useDockerInfra": None,
    },
    "automaticCallbackUris": None,
    "isServiceManager3": None,
    "manualOverrideUris": ["https://agent.example.invalid"],
    "primaryCallbackUri": None,
    "status": "active",
}


def _client(schema_dir: Path, scope: str | None = None) -> ConsoleAPIClient:
    """Build a client on the real Console spec (session-cached, see conftest) with a user token."""
    config = MagicMock()
    config.get_console_api_settings.return_value = ConsoleAPISettings(
        user_token=SecretStr("placeholder-user-token"), base_url=_HOST, base_api_path="/"
    )
    config.get_schema_location.return_value = schema_dir
    return ConsoleAPIClient(config, scope=scope)


def _respond(client: ConsoleAPIClient, *bodies: Any) -> Any:
    """Patch the user wrapper's transport to return ``bodies`` in turn; return the mock."""
    responses = []
    for body in bodies:
        response = MagicMock()
        response.status_code = 200
        response.json.return_value = body
        responses.append(response)
    return patch.object(
        client._require_user(), "_execute_request_with_retry", side_effect=responses
    )


def test_list_connectors_routes_to_agents_mgmt(real_spec_dir: Path) -> None:
    client = _client(real_spec_dir)
    with _respond(client, {"occms": [_OCCM]}) as mocked:
        result = client.ops.list_connectors("org-a")

    assert mocked.call_args.kwargs["url"] == f"{_HOST}/agents-mgmt/list-connectors/org-a"
    assert isinstance(result, get_list_connectors.ResponseBody)
    assert result.occms is not None
    assert result.occms[0].agent is not None
    assert result.occms[0].agent.agentId == "agent-1clients"


def test_get_agent_routes_and_encodes_the_id(real_spec_dir: Path) -> None:
    client = _client(real_spec_dir)
    with _respond(client, {"agent": _OCCM["agent"], "clientInfraStatus": None}) as mocked:
        result = client.ops.get_agent("agent/with slash")

    assert mocked.call_args.kwargs["url"] == f"{_HOST}/agents-mgmt/agent/agent%2Fwith%20slash"
    assert isinstance(result, get_agent.ResponseBody)
    assert result.agent is not None
    assert result.agent.region == "us-east-1"


def test_list_connectors_encodes_the_organization_id(real_spec_dir: Path) -> None:
    client = _client(real_spec_dir)
    with _respond(client, {}) as mocked:
        assert client.ops.list_connectors("org/a").occms is None

    assert mocked.call_args.kwargs["url"].endswith("/agents-mgmt/list-connectors/org%2Fa")


def test_list_organization_resources_routes_with_cursor(real_spec_dir: Path) -> None:
    client = _client(real_spec_dir)
    with _respond(client, {"items": []}) as mocked:
        client.ops.list_organization_resources("org-a", continue_="cursor-1")

    assert mocked.call_args.kwargs["url"] == (
        f"{_HOST}/v1/management/organizations/org-a/resources?continue=cursor-1"
    )


def test_list_agents_tags_the_scope_and_organization(real_spec_dir: Path) -> None:
    client = _client(real_spec_dir, scope="A")
    with _respond(client, {"occms": [_OCCM]}):
        agents = client.list_agents("org-a")

    assert agents == [
        ConsoleAgentInfo(
            agentId="agent-1clients",
            name="agent-name",
            status="active",
            agentType="connector",
            provider="aws",
            region="us-east-1",
            systemId="system-1",
            scope="A",
            organization_id="org-a",
        )
    ]


_INFRA_STATUS: dict[str, Any] = {"placeholderKey": "placeholder-value", "nested": {"inner": [1, 2]}}


def _agent_with_infra_status() -> dict[str, Any]:
    agent: dict[str, Any] = dict(cast("dict[str, Any]", _OCCM["agent"]))
    agent["clientInfraStatus"] = _INFRA_STATUS
    return agent


def test_list_connectors_accepts_an_object_client_infra_status(real_spec_dir: Path) -> None:
    client = _client(real_spec_dir)
    occm = {**_OCCM, "agent": _agent_with_infra_status()}
    with _respond(client, {"occms": [occm]}):
        result = client.ops.list_connectors("org-a")

    assert result.occms is not None
    assert result.occms[0].agent is not None
    assert result.occms[0].agent.clientInfraStatus == _INFRA_STATUS


def test_list_agents_returns_agents_with_an_object_client_infra_status(real_spec_dir: Path) -> None:
    client = _client(real_spec_dir)
    occm = {**_OCCM, "agent": _agent_with_infra_status()}
    with _respond(client, {"occms": [occm]}):
        agents = client.list_agents("org-a")

    assert [a.agent_id for a in agents] == ["agent-1clients"]
    assert all(isinstance(a, ConsoleAgentInfo) for a in agents)


def test_get_agent_accepts_object_client_infra_status_at_both_levels(real_spec_dir: Path) -> None:
    client = _client(real_spec_dir)
    body = {
        "agent": _agent_with_infra_status(),
        "clientInfraStatus": _INFRA_STATUS,
    }
    with _respond(client, body):
        result = client.ops.get_agent("agent-1clients")

    assert result.clientInfraStatus == _INFRA_STATUS
    assert result.agent is not None
    assert result.agent.clientInfraStatus == _INFRA_STATUS


def test_list_agents_without_occms_is_empty(real_spec_dir: Path) -> None:
    client = _client(real_spec_dir)
    with _respond(client, {"occms": None}):
        assert client.list_agents("org-a") == []


def test_get_agent_returns_the_compact_agent(real_spec_dir: Path) -> None:
    client = _client(real_spec_dir)
    with _respond(client, {"agent": _OCCM["agent"]}):
        agent = client.get_agent("agent-1clients")

    assert agent.agent_id == "agent-1clients"
    assert agent.scope is None
    assert agent.organization_id is None


def test_resources_follow_the_continue_cursor(real_spec_dir: Path) -> None:
    client = _client(real_spec_dir)
    pages = [
        {"continue": "c1", "items": [{"id": "r1", "resourceType": "ON_PREM"}]},
        {"items": [{"id": "r2", "resourceType": "VOLUME"}]},
    ]
    with _respond(client, *pages) as mocked:
        resources = client.list_organization_resources("org-a")

    assert [r.id for r in resources] == ["r1", "r2"]
    assert mocked.call_count == 2
    assert "c1" not in json.dumps(mocked.call_args_list[0].kwargs, default=str)
    assert "c1" in json.dumps(mocked.call_args_list[1].kwargs, default=str)


def test_a_repeated_cursor_raises(real_spec_dir: Path) -> None:
    client = _client(real_spec_dir)
    page = {"continue": "same", "items": []}
    with _respond(client, page, page, page), pytest.raises(RuntimeError, match="same continue"):
        client.list_organization_resources("org-a")


def test_resource_payload_with_nulls_and_single_key_tags_validates(real_spec_dir: Path) -> None:
    client = _client(real_spec_dir)
    item = {
        "id": "r1",
        "name": None,
        "rawId": "raw-1",
        "resourceType": "ON_PREM",
        "state": None,
        "tags": [{"env": "prod"}],
    }
    with _respond(client, {"items": [item]}):
        (resource,) = client.list_organization_resources("org-a")

    assert resource.rawId == "raw-1"
    assert resource.tags is not None


def test_connector_payload_with_nulls_validates() -> None:
    body = get_list_connectors.ResponseBody.model_validate({"occms": [_OCCM, {"agent": None}]})
    assert body.occms is not None
    assert len(body.occms) == 2
