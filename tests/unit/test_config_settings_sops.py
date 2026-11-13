"""Tests for SOPS-encrypted values in the SMTP, DII and Console settings files (#1025)."""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import pytest
from click.testing import CliRunner

from pynetappfoundry.cli.main import nf
from pynetappfoundry.core.config import Config, ConfigurationError
from pynetappfoundry.utils.sops import SOPSError, SOPSNotInstalledError

CIPHERTEXT = "SOPS[placeholder-ciphertext]"
INNER = "placeholder-ciphertext"
PLAIN = "placeholder-plain-value"
DECRYPT = "pynetappfoundry.utils.sops.decrypt_value"

SMTP_BODY = 'server = "smtp.example.test"\nuser = "mailer"\n'
DII_BODY = 'base_url = "https://dii.example.test"\n'
CONSOLE_BODY = 'base_url = "https://api.example.test"\n'


def _write(config_dir: Path, name: str, content: str) -> None:
    config_dir.mkdir(exist_ok=True)
    (config_dir / name).write_text(content)


def _smtp(tmp: Path, extra: str = "", body: str = SMTP_BODY) -> Config:
    _write(tmp / "cfg", "settings.toml", f"[SMTP]\n{body}{extra}")
    return Config(config_dir=str(tmp / "cfg"), script_name="test")


def _dii(tmp: Path, extra: str = "", body: str = DII_BODY) -> Config:
    _write(tmp / "cfg", "diiapi.toml", f"[general]\n{body}{extra}")
    return Config(config_dir=str(tmp / "cfg"), script_name="test")


def _console(tmp: Path, extra: str = "", users: str = "") -> Config:
    _write(tmp / "cfg", "consoleapi.toml", f"[general]\n{CONSOLE_BODY}{extra}")
    if users:
        _write(tmp / "cfg", "users.toml", users)
    return Config(config_dir=str(tmp / "cfg"), script_name="test")


def _secret(value: Any) -> str:
    return str(value.get_secret_value())


# (builder, reader name, field, section label, file name, getter for the secret)
CASES: list[Any] = [
    pytest.param(_smtp, "get_smtp_settings", "password", "[SMTP]", "settings.toml", id="smtp"),
    pytest.param(
        _dii, "get_dii_api_settings", "api_ro_token", "[general]", "diiapi.toml", id="dii"
    ),
    pytest.param(
        _console,
        "get_console_api_settings",
        "service_token",
        "[general]",
        "consoleapi.toml",
        id="svc",
    ),
    pytest.param(
        _console, "get_console_api_settings", "user_token", "[general]", "consoleapi.toml", id="usr"
    ),
]


@pytest.mark.parametrize(("build", "reader", "field", "section", "fname"), CASES)
class TestSecretFields:
    def test_sops_value_is_decrypted(
        self,
        tmp_path: Path,
        build: Callable[..., Config],
        reader: str,
        field: str,
        section: str,
        fname: str,
    ) -> None:
        config = build(tmp_path, f'{field} = "{CIPHERTEXT}"\n')
        with patch(DECRYPT, return_value=PLAIN) as decrypt:
            settings = getattr(config, reader)()
        decrypt.assert_called_once_with(CIPHERTEXT)
        assert _secret(getattr(settings, field)) == PLAIN

    def test_plaintext_passes_through(
        self,
        tmp_path: Path,
        build: Callable[..., Config],
        reader: str,
        field: str,
        section: str,
        fname: str,
    ) -> None:
        config = build(tmp_path, f'{field} = "{PLAIN}"\n')
        with patch(DECRYPT) as decrypt:
            settings = getattr(config, reader)()
        decrypt.assert_not_called()
        assert _secret(getattr(settings, field)) == PLAIN

    def test_decrypt_failure_message(
        self,
        tmp_path: Path,
        build: Callable[..., Config],
        reader: str,
        field: str,
        section: str,
        fname: str,
    ) -> None:
        config = build(tmp_path, f'{field} = "{CIPHERTEXT}"\n')
        err = SOPSError(f"failed on {CIPHERTEXT}")
        with patch(DECRYPT, side_effect=err), pytest.raises(ConfigurationError) as exc:
            getattr(config, reader)()
        message = str(exc.value)
        assert fname in message
        assert section in message
        assert field in message
        assert CIPHERTEXT not in message
        assert INNER not in message
        assert exc.value.__cause__ is err

    def test_sops_not_installed_reason(
        self,
        tmp_path: Path,
        build: Callable[..., Config],
        reader: str,
        field: str,
        section: str,
        fname: str,
    ) -> None:
        config = build(tmp_path, f'{field} = "{CIPHERTEXT}"\n')
        with (
            patch(DECRYPT, side_effect=SOPSNotInstalledError("nope")),
            pytest.raises(ConfigurationError, match="sops is not installed"),
        ):
            getattr(config, reader)()

    def test_decrypt_memoized_per_config(
        self,
        tmp_path: Path,
        build: Callable[..., Config],
        reader: str,
        field: str,
        section: str,
        fname: str,
    ) -> None:
        config = build(tmp_path, f'{field} = "{CIPHERTEXT}"\n')
        with patch(DECRYPT, return_value=PLAIN) as decrypt:
            for _ in range(3):
                getattr(config, reader)()
            assert decrypt.call_count == 1
            other = Config(config_dir=str(tmp_path / "cfg"), script_name="test")
            getattr(other, reader)()
            assert decrypt.call_count == 2

    def test_raw_settings_keep_ciphertext(
        self,
        tmp_path: Path,
        build: Callable[..., Config],
        reader: str,
        field: str,
        section: str,
        fname: str,
    ) -> None:
        config = build(tmp_path, f'{field} = "{CIPHERTEXT}"\n')
        with patch(DECRYPT, return_value=PLAIN):
            getattr(config, reader)()
        assert CIPHERTEXT in repr(config.settings)
        assert PLAIN not in repr(config.settings)


def test_console_client_secret_decrypted(tmp_path: Path) -> None:
    config = _console(tmp_path, f'client_id = "placeholder-id"\nclient_secret = "{CIPHERTEXT}"\n')
    with patch(DECRYPT, return_value=PLAIN) as decrypt:
        settings = config.get_console_api_settings()
    decrypt.assert_called_once_with(CIPHERTEXT)
    assert settings.client_secret is not None
    assert settings.client_secret.get_secret_value() == PLAIN


def test_console_two_sops_fields_decrypt_separately(tmp_path: Path) -> None:
    other = "SOPS[placeholder-other]"
    config = _console(
        tmp_path,
        f'client_id = "placeholder-id"\nclient_secret = "{CIPHERTEXT}"\nuser_token = "{other}"\n',
    )
    decrypt = MagicMock(side_effect=lambda v: f"plain-of-{v}")
    with patch(DECRYPT, decrypt):
        settings = config.get_console_api_settings()
    assert [c.args[0] for c in decrypt.call_args_list] == [CIPHERTEXT, other]
    assert settings.user_token is not None
    assert settings.user_token.get_secret_value() == f"plain-of-{other}"


def test_console_sops_fields_with_users_toml_refresh_token(tmp_path: Path) -> None:
    refresh = "SOPS[placeholder-refresh]"
    users = f'[console]\nuser = "label"\nenc = "{refresh}"\n'
    config = _console(
        tmp_path,
        f'client_id = "placeholder-id"\nclient_secret = "{CIPHERTEXT}"\n',
        users=users,
    )
    with patch(DECRYPT, side_effect=lambda v: f"plain-of-{v}"):
        settings = config.get_console_api_settings()
    assert settings.client_secret is not None
    assert settings.client_secret.get_secret_value() == f"plain-of-{CIPHERTEXT}"
    assert settings.refresh_token is not None
    assert settings.refresh_token.get_secret_value() == f"plain-of-{refresh}"


def test_console_user_token_and_refresh_token_still_exclusive(tmp_path: Path) -> None:
    users = f'[console]\nuser = "label"\nenc = "{PLAIN}"\n'
    config = _console(tmp_path, f'user_token = "{CIPHERTEXT}"\n', users=users)
    with patch(DECRYPT, return_value=PLAIN), pytest.raises(ConfigurationError, match="exclusive"):
        config.get_console_api_settings()


def test_non_dict_section_keeps_existing_error(tmp_path: Path) -> None:
    _write(tmp_path / "cfg", "settings.toml", 'SMTP = "x"\n')
    config = Config(config_dir=str(tmp_path / "cfg"), script_name="test")
    with pytest.raises(ConfigurationError, match="Invalid SMTP configuration"):
        config.get_smtp_settings()


def test_config_without_sops_values_unchanged(tmp_path: Path) -> None:
    settings = _smtp(tmp_path, 'password = "placeholder-pw"\nport = 587\n').get_smtp_settings()
    assert settings.server == "smtp.example.test"
    assert settings.port == 587
    assert _secret(settings.password) == "placeholder-pw"


def test_dii_validation_error_does_not_leak_plaintext(tmp_path: Path) -> None:
    config = _dii(tmp_path, body="", extra=f'api_ro_token = "{CIPHERTEXT}"\n')
    with patch(DECRYPT, return_value=PLAIN), pytest.raises(ConfigurationError) as exc:
        config.get_dii_api_settings()
    assert PLAIN not in str(exc.value)


def test_smtp_validation_error_does_not_leak_plaintext(tmp_path: Path) -> None:
    config = _smtp(tmp_path, body="", extra=f'password = "{CIPHERTEXT}"\n')
    with patch(DECRYPT, return_value=PLAIN), pytest.raises(ConfigurationError) as exc:
        config.get_smtp_settings()
    assert PLAIN not in str(exc.value)


# --- nf config validate: absent vs invalid vs decrypt failure ---


def _validate(tmp: Path) -> tuple[int, str]:
    result = CliRunner().invoke(
        nf, ["--config-dir", str(tmp / "cfg"), "config", "validate"], env={"NF_CONFIG_DIR": ""}
    )
    return result.exit_code, result.output


def test_validate_absent_sections_are_not_configured(tmp_path: Path) -> None:
    (tmp_path / "cfg").mkdir()
    _code, output = _validate(tmp_path)
    assert "DII API: Not configured" in output
    assert "SMTP: Not configured" in output


def test_validate_valid_sections(tmp_path: Path) -> None:
    _smtp(tmp_path)
    _dii(tmp_path, f'api_ro_token = "{PLAIN}"\n')
    _code, output = _validate(tmp_path)
    assert "DII API: Invalid" not in output
    assert "SMTP: Invalid" not in output
    assert "SMTP: Not configured" not in output
    assert "DII API: Not configured" not in output


def test_validate_invalid_section_reported(tmp_path: Path) -> None:
    _dii(tmp_path)  # api_ro_token missing
    code, output = _validate(tmp_path)
    assert code != 0
    assert "DII API: Invalid" in output
    assert "DII API: Not configured" not in output


def test_validate_decrypt_failure_reported_as_invalid(tmp_path: Path) -> None:
    _smtp(tmp_path, f'password = "{CIPHERTEXT}"\n')
    with patch(DECRYPT, side_effect=SOPSError(f"failed on {CIPHERTEXT}")):
        code, output = _validate(tmp_path)
    assert code != 0
    assert "SMTP: Invalid" in output
    assert "SMTP: Not configured" not in output
    assert "password" in output
    assert INNER not in output
