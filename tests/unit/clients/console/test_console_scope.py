"""Console clients and facade pass the config scope through only when set (#1080)."""

from __future__ import annotations

from pathlib import Path
from typing import Any
from unittest.mock import MagicMock

import pytest

from pynetappfoundry.clients.console.agent import ConsoleAgentClient
from pynetappfoundry.clients.console.api import ConsoleAPIClient
from pynetappfoundry.console import Console
from pynetappfoundry.core.models import ConsoleAPISettings
from pynetappfoundry.models.console_types import Connector


def _config(tmp_path: Path, **settings: Any) -> MagicMock:
    values: dict[str, Any] = {
        "base_url": "https://api.example.invalid",
        "user_token": "placeholder-user-token",
        "org_id": "org-1",
        "agent_ids": ["agent-a"],
    }
    values.update(settings)
    config = MagicMock()
    config.get_console_api_settings.return_value = ConsoleAPISettings(**values)
    config.get_schema_location.return_value = tmp_path
    return config


@pytest.fixture(autouse=True)
def _no_wrapper(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("pynetappfoundry.clients.console.api.APIWrapper", MagicMock())
    monkeypatch.setattr("pynetappfoundry.clients.console.agent.APIWrapper", MagicMock())


def test_api_client_passes_scope_when_set(tmp_path: Path) -> None:
    config = _config(tmp_path)
    client = ConsoleAPIClient(config, scope="Org1")
    config.get_console_api_settings.assert_called_once_with(scope="Org1")
    assert client.scope == "Org1"


def test_api_client_omits_scope_when_unset(tmp_path: Path) -> None:
    config = _config(tmp_path)
    client = ConsoleAPIClient(config)
    config.get_console_api_settings.assert_called_once_with()
    assert client.scope is None


def test_agent_client_passes_scope_when_set(tmp_path: Path) -> None:
    config = _config(tmp_path)
    client = ConsoleAgentClient(config, "agent-a", scope="Org1")
    config.get_console_api_settings.assert_called_once_with(scope="Org1")
    assert client.scope == "Org1"


def test_agent_client_omits_scope_when_unset(tmp_path: Path) -> None:
    config = _config(tmp_path)
    ConsoleAgentClient(config, "agent-a")
    config.get_console_api_settings.assert_called_once_with()


def test_facade_with_scope_uses_scope_settings_and_agent_clients(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    agent_cls = MagicMock()
    agent_cls.return_value.get_connector.return_value = Connector.model_validate({"agent_id": "a"})
    agent_cls.return_value.find_onprem_working_environment.return_value = object()
    monkeypatch.setattr("pynetappfoundry.console.ConsoleAgentClient", agent_cls)
    config = _config(tmp_path)

    console = Console(config, scope="Org1")

    assert console.org_id == "org-1"
    config.get_console_api_settings.assert_called_with(scope="Org1")
    console.get_connector("agent-a")
    assert agent_cls.call_args.kwargs["scope"] == "Org1"
    # find_connector reads the scope's agent_ids when none are given
    console.find_connector("cluster-uuid")
    assert agent_cls.call_args.args[1] == "agent-a"
    assert all(call.kwargs.get("scope") == "Org1" for call in agent_cls.call_args_list)
    assert all(
        call.kwargs == {"scope": "Org1"} for call in config.get_console_api_settings.call_args_list
    )


def test_facade_without_scope_passes_no_scope(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    agent_cls = MagicMock()
    agent_cls.return_value.get_connector.return_value = Connector.model_validate({"agent_id": "a"})
    monkeypatch.setattr("pynetappfoundry.console.ConsoleAgentClient", agent_cls)
    config = _config(tmp_path)

    console = Console(config)
    console.get_connector("agent-a")

    assert "scope" not in agent_cls.call_args.kwargs
    config.get_console_api_settings.assert_called_with()
