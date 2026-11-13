"""Tests for the Console facade sharing the user refresh provider (#736)."""

from __future__ import annotations

from pathlib import Path
from typing import Any
from unittest.mock import MagicMock

import pytest

from pynetappfoundry.console import Console
from pynetappfoundry.core.models import ConsoleAPISettings
from pynetappfoundry.models.console_types import Connector


def _config(settings: ConsoleAPISettings, tmp_path: Path) -> MagicMock:
    config = MagicMock()
    config.get_console_api_settings.return_value = settings
    config.get_schema_location.return_value = tmp_path
    return config


def _console(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, **settings: Any
) -> tuple[Console, MagicMock]:
    monkeypatch.setattr("pynetappfoundry.clients.console.api.APIWrapper", MagicMock())
    provider_cls = MagicMock()
    monkeypatch.setattr("pynetappfoundry.clients.console.api.RefreshTokenProvider", provider_cls)
    monkeypatch.setattr(
        "pynetappfoundry.clients.console.api.ClientCredentialsTokenProvider", MagicMock()
    )
    agent_cls = MagicMock()
    agent_cls.return_value.get_connector.return_value = Connector.model_validate({"agent_id": "a"})
    monkeypatch.setattr("pynetappfoundry.console.ConsoleAgentClient", agent_cls)
    values: dict[str, Any] = {
        "base_url": "https://api.bluexp.netapp.com",
        "org_id": "org-default",
    }
    values.update(settings)
    return Console(_config(ConsoleAPISettings(**values), tmp_path)), agent_cls


def test_refresh_token_passes_user_provider(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    console, agent_cls = _console(tmp_path, monkeypatch, refresh_token="placeholder-refresh-token")

    console.get_connector("agent-a")

    provider = console._client.user_token_provider
    assert provider is not None
    assert agent_cls.call_args.kwargs["token_provider"] is provider


def test_user_provider_wins_over_service_provider(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    console, agent_cls = _console(
        tmp_path,
        monkeypatch,
        refresh_token="placeholder-refresh-token",
        client_id="cid",
        client_secret="placeholder-client-secret",
    )

    console.get_connector("agent-a")

    assert console._client.service_token_provider is not None
    assert agent_cls.call_args.kwargs["token_provider"] is console._client.user_token_provider


def test_client_credentials_alone_still_pass_service_provider(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    console, agent_cls = _console(
        tmp_path, monkeypatch, client_id="cid", client_secret="placeholder-client-secret"
    )

    console.get_connector("agent-a")

    assert console._client.user_token_provider is None
    service = console._client.service_token_provider
    assert service is not None
    assert agent_cls.call_args.kwargs["token_provider"] is service
