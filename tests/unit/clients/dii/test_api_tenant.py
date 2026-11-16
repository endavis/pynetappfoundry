"""Tests for DIIAPIClient per-tenant construction (#1045)."""

from __future__ import annotations

from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

from pydantic import SecretStr

from pynetappfoundry.clients.dii.api import DIIAPIClient
from pynetappfoundry.core.models import DIIAPISettings


def _config(tmp_path: Path) -> MagicMock:
    config = MagicMock()
    config.get_schema_location.return_value = tmp_path
    config.get_dii_api_settings.return_value = DIIAPISettings(
        api_ro_token=SecretStr("tok"), base_url="https://dii.example.invalid"
    )
    return config


def _build(config: MagicMock, **kwargs: Any) -> MagicMock:
    with patch("pynetappfoundry.clients.dii.api.APIWrapper.__init__", return_value=None) as init:
        DIIAPIClient(config, **kwargs)
    return init


def test_without_name_uses_general_settings(tmp_path: Path) -> None:
    config = _config(tmp_path)

    init = _build(config)

    config.get_dii_api_settings.assert_called_once_with()
    kwargs = init.call_args.kwargs
    assert kwargs["name"] == ""
    assert kwargs["base_url"] == "https://dii.example.invalid"
    assert kwargs["auth_header"] == {"X-CloudInsights-ApiKey": "tok"}


def test_with_name_uses_tenant_settings(tmp_path: Path) -> None:
    config = _config(tmp_path)
    config.get_dii_api_settings.return_value = DIIAPISettings(
        api_ro_token=SecretStr("t1-tok"), base_url="https://t1.example.invalid"
    )

    init = _build(config, name="t1")

    config.get_dii_api_settings.assert_called_once_with("t1")
    kwargs = init.call_args.kwargs
    assert kwargs["name"] == "t1"
    assert kwargs["base_url"] == "https://t1.example.invalid"
    assert kwargs["auth_header"] == {"X-CloudInsights-ApiKey": "t1-tok"}
