"""Tests for resolving the Console refresh token from users.toml (#736)."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from pynetappfoundry.core.config import Config, ConfigurationError
from pynetappfoundry.utils.sops import SOPSError

REFRESH = "placeholder-refresh-token"
CIPHERTEXT = "SOPS[placeholder-ciphertext]"
CONSOLE_TOML = 'base_url = "https://api.example.test"\n'


def _write(config_dir: Path, *, consoleapi: str = "", users: str = "") -> Path:
    config_dir.mkdir(exist_ok=True)
    (config_dir / "consoleapi.toml").write_text(f"[general]\n{consoleapi or CONSOLE_TOML}")
    if users:
        (config_dir / "users.toml").write_text(users)
    return config_dir


def _config(config_dir: Path) -> Config:
    return Config(config_dir=str(config_dir), script_name="test")


@pytest.fixture(autouse=True)
def _clean_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("NF_CONSOLE_USER", raising=False)
    monkeypatch.delenv("NF_CONSOLE_PASSWORD", raising=False)


def test_plaintext_console_entry_becomes_refresh_token(tmp_path: Path) -> None:
    users = f'[console]\nuser = "label"\nenc = "{REFRESH}"\n'
    settings = _config(_write(tmp_path / "cfg", users=users)).get_console_api_settings()

    assert settings.refresh_token is not None
    assert settings.refresh_token.get_secret_value() == REFRESH
    assert settings.uses_refresh_token


def test_sops_value_is_decrypted(tmp_path: Path) -> None:
    users = f'[console]\nuser = "label"\nenc = "{CIPHERTEXT}"\n'
    config = _config(_write(tmp_path / "cfg", users=users))
    with (
        patch("pynetappfoundry.utils.sops.is_encrypted", return_value=True),
        patch("pynetappfoundry.utils.sops.decrypt_value", return_value=REFRESH) as decrypt,
    ):
        settings = config.get_console_api_settings()

    decrypt.assert_called_once_with(CIPHERTEXT)
    assert settings.refresh_token is not None
    assert settings.refresh_token.get_secret_value() == REFRESH


def test_env_vars_override_users_toml(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    users = '[console]\nuser = "label"\nenc = "placeholder-from-file"\n'
    config_dir = _write(tmp_path / "cfg", users=users)
    monkeypatch.setenv("NF_CONSOLE_USER", "env-label")
    monkeypatch.setenv("NF_CONSOLE_PASSWORD", "placeholder-from-env")

    settings = _config(config_dir).get_console_api_settings()

    assert settings.refresh_token is not None
    assert settings.refresh_token.get_secret_value() == "placeholder-from-env"


def test_env_vars_alone_configure_refresh_token(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    config_dir = _write(tmp_path / "cfg")
    monkeypatch.setenv("NF_CONSOLE_USER", "env-label")
    monkeypatch.setenv("NF_CONSOLE_PASSWORD", "placeholder-from-env")

    settings = _config(config_dir).get_console_api_settings()

    assert settings.refresh_token is not None


def test_no_console_entry_leaves_token_none(tmp_path: Path) -> None:
    config_dir = _write(
        tmp_path / "cfg",
        consoleapi=CONSOLE_TOML + 'user_token = "user-jwt"\n',
        users='[clusters]\nuser = "admin"\nenc = "pw"\n',
    )
    settings = _config(config_dir).get_console_api_settings()

    assert settings.refresh_token is None
    assert settings.user_token is not None
    assert settings.user_token.get_secret_value() == "user-jwt"


def test_refresh_token_in_consoleapi_toml_rejected_without_value(tmp_path: Path) -> None:
    config_dir = _write(
        tmp_path / "cfg", consoleapi=CONSOLE_TOML + f'refresh_token = "{REFRESH}"\n'
    )

    with pytest.raises(ConfigurationError) as exc_info:
        _config(config_dir).get_console_api_settings()

    assert "users.toml" in str(exc_info.value)
    assert REFRESH not in str(exc_info.value)


def test_decrypt_failure_raises_without_ciphertext(tmp_path: Path) -> None:
    users = f'[console]\nuser = "label"\nenc = "{CIPHERTEXT}"\n'
    config = _config(_write(tmp_path / "cfg", users=users))
    with (
        patch("pynetappfoundry.utils.sops.is_encrypted", return_value=True),
        patch(
            "pynetappfoundry.utils.sops.decrypt_value",
            side_effect=SOPSError(f"failed on {CIPHERTEXT}"),
        ),
        pytest.raises(ConfigurationError) as exc_info,
    ):
        config.get_console_api_settings()

    assert CIPHERTEXT not in str(exc_info.value)
    assert "placeholder-ciphertext" not in str(exc_info.value)


def test_refresh_token_with_user_token_is_a_configuration_error(tmp_path: Path) -> None:
    users = f'[console]\nuser = "label"\nenc = "{REFRESH}"\n'
    config_dir = _write(
        tmp_path / "cfg", consoleapi=CONSOLE_TOML + 'user_token = "user-jwt"\n', users=users
    )
    with pytest.raises(ConfigurationError) as exc_info:
        _config(config_dir).get_console_api_settings()

    assert "mutually exclusive" in str(exc_info.value)
    assert REFRESH not in str(exc_info.value)


def test_token_is_decrypted_once_across_calls(tmp_path: Path) -> None:
    users = f'[console]\nuser = "label"\nenc = "{CIPHERTEXT}"\n'
    config = _config(_write(tmp_path / "cfg", users=users))
    decrypt = MagicMock(return_value=REFRESH)
    with (
        patch("pynetappfoundry.utils.sops.is_encrypted", return_value=True),
        patch("pynetappfoundry.utils.sops.decrypt_value", decrypt),
    ):
        config.get_console_api_settings()
        config.get_console_api_settings()
        config.get_console_api_settings()

    assert decrypt.call_count == 1
