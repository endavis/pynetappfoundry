"""Tests for writing rotated Digital Advisor tokens back to the config (#1051)."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pytest

from pynetappfoundry.clients.digitaladvisor import api
from pynetappfoundry.clients.digitaladvisor.auth import TokenPersistError
from pynetappfoundry.core.config import Config

NEW_ACCESS = "placeholder-new-access"
NEW_REFRESH = "placeholder-new-refresh"


def _config(tmp_path: Path, refresh: str) -> tuple[Config, Path]:
    path = tmp_path / "cfg" / "apis" / "digitaladvisor" / "digitaladvisorapi.toml"
    path.parent.mkdir(parents=True)
    path.write_text(f'# keep this comment\n[general]\nrefresh_token = "{refresh}"\n')
    return Config(config_dir=str(tmp_path / "cfg"), script_name="test"), path


def _encrypt(value: str, key: str) -> str:
    return f"SOPS[enc-{key}-{value}]"


def test_sops_stored_token_is_written_encrypted(tmp_path: Path) -> None:
    config, path = _config(tmp_path, "SOPS[old]")
    with (
        patch.object(api, "get_age_key_path"),
        patch.object(api, "get_public_key_from_file", return_value="agekey"),
        patch.object(api, "encrypt_value", side_effect=_encrypt) as enc,
    ):
        api.make_token_persister(config)(NEW_ACCESS, NEW_REFRESH)

    text = path.read_text()
    assert f"enc-agekey-{NEW_ACCESS}" in text
    assert f"enc-agekey-{NEW_REFRESH}" in text
    assert NEW_ACCESS not in text.replace(f"enc-agekey-{NEW_ACCESS}", "")
    assert enc.call_count == 2
    assert "# keep this comment" in text


def test_plain_stored_token_is_written_plain(tmp_path: Path) -> None:
    config, path = _config(tmp_path, "placeholder-old")
    with patch.object(api, "encrypt_value") as enc:
        api.make_token_persister(config)(NEW_ACCESS, NEW_REFRESH)
    enc.assert_not_called()
    text = path.read_text()
    assert f'access_token = "{NEW_ACCESS}"' in text
    assert f'refresh_token = "{NEW_REFRESH}"' in text
    assert "# keep this comment" in text


def test_written_file_loads_back_through_the_loader(tmp_path: Path) -> None:
    config, _ = _config(tmp_path, "SOPS[old]")
    with (
        patch.object(api, "get_age_key_path"),
        patch.object(api, "get_public_key_from_file", return_value="agekey"),
        patch.object(api, "encrypt_value", side_effect=_encrypt),
    ):
        api.make_token_persister(config)(NEW_ACCESS, NEW_REFRESH)

    reloaded = Config(config_dir=str(tmp_path / "cfg"), script_name="test")
    plain = {
        _encrypt(NEW_ACCESS, "agekey"): NEW_ACCESS,
        _encrypt(NEW_REFRESH, "agekey"): NEW_REFRESH,
    }
    with patch("pynetappfoundry.utils.sops.decrypt_value", side_effect=lambda v: plain[v]):
        settings = reloaded.get_digital_advisor_api_settings()
    assert settings.access_token is not None
    assert settings.access_token.get_secret_value() == NEW_ACCESS
    assert settings.refresh_token is not None
    assert settings.refresh_token.get_secret_value() == NEW_REFRESH


def test_write_failure_names_file_and_type_only(tmp_path: Path) -> None:
    config, path = _config(tmp_path, "placeholder-old")
    with (
        patch.object(api, "write_toml_values", side_effect=PermissionError(NEW_REFRESH)),
        pytest.raises(TokenPersistError) as exc,
    ):
        api.make_token_persister(config)(NEW_ACCESS, NEW_REFRESH)
    assert str(path) in str(exc.value)
    assert "PermissionError" in str(exc.value)
    assert NEW_REFRESH not in str(exc.value)
