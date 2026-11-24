"""Tests for DIIAPIClient per-tenant construction (#1045)."""

from __future__ import annotations

from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import pytest
from pydantic import SecretStr

from pynetappfoundry.clients.dii.api import DIIAPIClient, DIIWriteTokenMissingError
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


def _rw_config(tmp_path: Path, *, rw: str | None) -> MagicMock:
    config = _config(tmp_path)
    config.get_dii_api_settings.return_value = DIIAPISettings(
        api_ro_token=SecretStr("ro-key-1003"),
        api_rw_token=SecretStr(rw) if rw is not None else None,
        base_url="https://dii.example.invalid",
    )
    return config


def test_default_client_sends_only_read_only_key(tmp_path: Path) -> None:
    config = _rw_config(tmp_path, rw="rw-key-1003")
    with patch("pynetappfoundry.clients.dii.api.APIWrapper.__init__", return_value=None) as init:
        client = DIIAPIClient(config)
    assert client.read_write is False
    assert init.call_args.kwargs["auth_header"] == {"X-CloudInsights-ApiKey": "ro-key-1003"}


def test_read_write_client_sends_only_read_write_key(tmp_path: Path) -> None:
    config = _rw_config(tmp_path, rw="rw-key-1003")
    with patch("pynetappfoundry.clients.dii.api.APIWrapper.__init__", return_value=None) as init:
        client = DIIAPIClient(config, read_write=True)
    assert client.read_write is True
    kwargs = init.call_args.kwargs
    assert kwargs["auth_header"] == {"X-CloudInsights-ApiKey": "rw-key-1003"}
    assert kwargs["name"] == "rw"


def test_read_write_client_named_tenant_log_name(tmp_path: Path) -> None:
    config = _rw_config(tmp_path, rw="rw-key-1003")
    with patch("pynetappfoundry.clients.dii.api.APIWrapper.__init__", return_value=None) as init:
        DIIAPIClient(config, "t1", read_write=True)
    assert init.call_args.kwargs["name"] == "t1:rw"


@pytest.mark.parametrize("name", [None, "t1"])
def test_read_write_without_key_raises_before_wrapper_init(
    tmp_path: Path, name: str | None
) -> None:
    config = _rw_config(tmp_path, rw=None)
    with (
        patch("pynetappfoundry.clients.dii.api.APIWrapper.__init__", return_value=None) as init,
        pytest.raises(DIIWriteTokenMissingError) as exc,
    ):
        DIIAPIClient(config, name, read_write=True)
    init.assert_not_called()
    assert "api_rw_token" in str(exc.value)
    assert "ro-key-1003" not in str(exc.value)


def test_named_tenant_missing_rw_key_hint_names_the_command(tmp_path: Path) -> None:
    config = _rw_config(tmp_path, rw=None)
    with (
        patch("pynetappfoundry.clients.dii.api.APIWrapper.__init__", return_value=None),
        pytest.raises(DIIWriteTokenMissingError) as exc,
    ):
        DIIAPIClient(config, "t1", read_write=True)
    assert "nf config set-credential --type cloudinsights --name t1 --read-write" in str(exc.value)
    assert "api_rw_token" in str(exc.value)
