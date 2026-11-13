"""Tests for the org-scoped Console facade (ADR-0019 §1)."""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock

import pytest
from pydantic import SecretStr

from pynetappfoundry.console import Console
from pynetappfoundry.core.models import ConsoleAPISettings
from pynetappfoundry.models.console_types import Connector, Folder, Organization, Project


def _make_config(settings: ConsoleAPISettings, tmp_path: Any) -> MagicMock:
    config = MagicMock()
    config.get_console_api_settings.return_value = settings
    config.get_schema_location.return_value = tmp_path
    return config


@pytest.fixture
def settings_with_default_org() -> ConsoleAPISettings:
    return ConsoleAPISettings(
        user_token=SecretStr("user-jwt"),
        base_url="https://api.bluexp.netapp.com",
        base_api_path="/",
        org_id="org-default",
    )


@pytest.fixture
def settings_without_org() -> ConsoleAPISettings:
    return ConsoleAPISettings(
        user_token=SecretStr("user-jwt"),
        base_url="https://api.bluexp.netapp.com",
        base_api_path="/",
    )


class TestConsoleOrgBinding:
    """org_id resolution from constructor argument vs. settings default."""

    def test_constructor_arg_wins_over_settings_default(
        self,
        settings_with_default_org: ConsoleAPISettings,
        tmp_path: Any,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        monkeypatch.setattr(
            "pynetappfoundry.clients.console.api.APIWrapper",
            MagicMock(),
        )
        console = Console(_make_config(settings_with_default_org, tmp_path), org_id="org-explicit")
        assert console.org_id == "org-explicit"

    def test_settings_default_used_when_no_arg(
        self,
        settings_with_default_org: ConsoleAPISettings,
        tmp_path: Any,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        monkeypatch.setattr(
            "pynetappfoundry.clients.console.api.APIWrapper",
            MagicMock(),
        )
        console = Console(_make_config(settings_with_default_org, tmp_path))
        assert console.org_id == "org-default"

    def test_raises_when_no_org_id_anywhere(
        self,
        settings_without_org: ConsoleAPISettings,
        tmp_path: Any,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        monkeypatch.setattr(
            "pynetappfoundry.clients.console.api.APIWrapper",
            MagicMock(),
        )
        with pytest.raises(ValueError, match="org_id"):
            Console(_make_config(settings_without_org, tmp_path))


class TestConsoleDelegatesToClient:
    """The facade thinly delegates to ConsoleAPIClient with its bound org_id."""

    def test_get_organization_delegates_with_bound_org_id(
        self,
        settings_with_default_org: ConsoleAPISettings,
        tmp_path: Any,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        wrapper_instance = MagicMock()
        wrapper_instance.call_endpoint.return_value = {
            "id": "org-default",
            "name": "Default Org",
            "resourceClass": "tenancyv4",
            "resourceType": "organization",
        }
        monkeypatch.setattr(
            "pynetappfoundry.clients.console.api.APIWrapper",
            MagicMock(return_value=wrapper_instance),
        )

        console = Console(_make_config(settings_with_default_org, tmp_path))
        org = console.get_organization()

        assert isinstance(org, Organization)
        assert org.id == "org-default"
        wrapper_instance.call_endpoint.assert_called_once_with(
            method="GET",
            path_template="/v1/management/organizations/{organization_id}",
            path_params={"organization_id": "org-default"},
        )

    @pytest.mark.parametrize(
        ("method", "model", "path_template", "param"),
        [
            ("get_folder", Folder, "/v1/management/folders/{folder_id}", "folder_id"),
            ("get_project", Project, "/v1/management/projects/{project_id}", "project_id"),
        ],
    )
    def test_get_folder_and_project_delegate(
        self,
        method: str,
        model: type[Folder] | type[Project],
        path_template: str,
        param: str,
        settings_with_default_org: ConsoleAPISettings,
        tmp_path: Any,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        wrapper_instance = MagicMock()
        wrapper_instance.call_endpoint.return_value = {
            "id": "res-1",
            "name": "Res",
            "resourceClass": "tenancyv4",
            "resourceType": method.removeprefix("get_"),
        }
        monkeypatch.setattr(
            "pynetappfoundry.clients.console.api.APIWrapper",
            MagicMock(return_value=wrapper_instance),
        )

        console = Console(_make_config(settings_with_default_org, tmp_path))
        result = getattr(console, method)("res-1")

        assert isinstance(result, model)
        wrapper_instance.call_endpoint.assert_called_once_with(
            method="GET",
            path_template=path_template,
            path_params={param: "res-1"},
        )


def _connector(agent_id: str) -> Connector:
    return Connector.model_validate({"agent_id": agent_id})


class TestConsoleConnector:
    """#734: get_connector and find_connector."""

    @staticmethod
    def _console(tmp_path: Any, monkeypatch: pytest.MonkeyPatch, **settings: Any) -> Console:
        monkeypatch.setattr("pynetappfoundry.clients.console.api.APIWrapper", MagicMock())
        values: dict[str, Any] = {
            "user_token": "user-jwt",
            "base_url": "https://api.bluexp.netapp.com",
            "org_id": "org-default",
        }
        values.update(settings)
        return Console(_make_config(ConsoleAPISettings(**values), tmp_path))

    @staticmethod
    def _patch_agents(
        monkeypatch: pytest.MonkeyPatch, matching: set[str]
    ) -> tuple[MagicMock, list[MagicMock]]:
        built: list[MagicMock] = []

        def factory(config: Any, agent_id: str, **kwargs: Any) -> MagicMock:
            agent = MagicMock(name=agent_id)
            agent.agent_id = agent_id
            agent.find_onprem_working_environment.return_value = (
                object() if agent_id in matching else None
            )
            agent.get_connector.return_value = _connector(agent_id)
            built.append(agent)
            return agent

        mock = MagicMock(side_effect=factory)
        monkeypatch.setattr("pynetappfoundry.console.ConsoleAgentClient", mock)
        return mock, built

    def test_get_connector_uses_service_token_provider(
        self, tmp_path: Any, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        console = self._console(tmp_path, monkeypatch)
        mock, _ = self._patch_agents(monkeypatch, set())

        result = console.get_connector("agent-a")

        assert result == _connector("agent-a")
        assert mock.call_args.args[1] == "agent-a"
        assert mock.call_args.kwargs["token_provider"] is console._client.service_token_provider

    def test_find_returns_first_match_and_stops(
        self, tmp_path: Any, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        console = self._console(tmp_path, monkeypatch)
        _, built = self._patch_agents(monkeypatch, {"agent-b", "agent-c"})

        result = console.find_connector("cluster-uuid", ["agent-a", "agent-b", "agent-c"])

        assert result == _connector("agent-b")
        assert [a.agent_id for a in built] == ["agent-a", "agent-b"]

    def test_find_returns_none_when_no_agent_matches(
        self, tmp_path: Any, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        console = self._console(tmp_path, monkeypatch)
        self._patch_agents(monkeypatch, set())
        assert console.find_connector("cluster-uuid", ["agent-a", "agent-b"]) is None

    def test_find_uses_settings_agent_ids(
        self, tmp_path: Any, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        console = self._console(tmp_path, monkeypatch, agent_ids=["agent-s"])
        self._patch_agents(monkeypatch, {"agent-s"})
        assert console.find_connector("cluster-uuid") == _connector("agent-s")

    def test_argument_overrides_settings(
        self, tmp_path: Any, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        console = self._console(tmp_path, monkeypatch, agent_ids=["agent-s"])
        _, built = self._patch_agents(monkeypatch, {"agent-x"})

        result = console.find_connector("cluster-uuid", ["agent-x"])

        assert result == _connector("agent-x")
        assert [a.agent_id for a in built] == ["agent-x"]

    @pytest.mark.parametrize("agent_ids", [None, []])
    def test_raises_when_no_agent_ids_anywhere(
        self, tmp_path: Any, monkeypatch: pytest.MonkeyPatch, agent_ids: list[str] | None
    ) -> None:
        console = self._console(tmp_path, monkeypatch)
        self._patch_agents(monkeypatch, set())
        with pytest.raises(ValueError, match="agent_ids"):
            console.find_connector("cluster-uuid", agent_ids)

    def test_agent_error_propagates(self, tmp_path: Any, monkeypatch: pytest.MonkeyPatch) -> None:
        console = self._console(tmp_path, monkeypatch)
        mock, _ = self._patch_agents(monkeypatch, set())

        def boom(config: Any, agent_id: str, **kwargs: Any) -> MagicMock:
            agent = MagicMock()
            agent.find_onprem_working_environment.side_effect = RuntimeError("agent down")
            return agent

        mock.side_effect = boom
        with pytest.raises(RuntimeError, match="agent down"):
            console.find_connector("cluster-uuid", ["agent-a"])
