"""Tests for ``Console.list_preferred_subscriptions`` (#1034)."""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock

import pytest
from pydantic import SecretStr

from pynetappfoundry.console import Console
from pynetappfoundry.core.models import ConsoleAPISettings
from pynetappfoundry.models.console_types import AccountSubscription


def _console(tmp_path: Any, monkeypatch: pytest.MonkeyPatch) -> Console:
    monkeypatch.setattr("pynetappfoundry.clients.console.api.APIWrapper", MagicMock())
    config = MagicMock()
    config.get_console_api_settings.return_value = ConsoleAPISettings(
        user_token=SecretStr("user-jwt"),
        base_url="https://api.bluexp.netapp.com",
        org_id="org-default",
    )
    config.get_schema_location.return_value = tmp_path
    return Console(config)


def test_delegates_with_explicit_account_id(tmp_path: Any, monkeypatch: pytest.MonkeyPatch) -> None:
    console = _console(tmp_path, monkeypatch)
    expected = [AccountSubscription.model_validate({"subscriptionId": "s1"})]
    mock = MagicMock(return_value=expected)
    monkeypatch.setattr(console._client, "list_preferred_subscriptions", mock)

    assert console.list_preferred_subscriptions("account-1", "aws") == expected
    mock.assert_called_once_with("account-1", "aws")


def test_defaults_account_id_to_org_id(tmp_path: Any, monkeypatch: pytest.MonkeyPatch) -> None:
    console = _console(tmp_path, monkeypatch)
    mock = MagicMock(return_value=[])
    monkeypatch.setattr(console._client, "list_preferred_subscriptions", mock)

    assert console.list_preferred_subscriptions() == []
    mock.assert_called_once_with("org-default", None)
