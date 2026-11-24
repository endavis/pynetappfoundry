"""Tests for per-object credential resolution and DII tenant settings (#1045)."""

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path
from unittest.mock import patch

import pytest

from pynetappfoundry.core.config import Config, ConfigurationError
from pynetappfoundry.utils.sops import SOPSError

CONFIG_FILES = {
    "data/inventory.toml": """\
[settings]
type = "data"

[aiqums.a1]
ip = "10.0.0.1"
user = "own-user"
enc = "own-pass"

[aiqums.a2]
ip = "10.0.0.2"

[cloudinsights.t1]
base_url = "https://t1.example.invalid"
user = "label"
enc = "t1-token"

[cloudinsights.t2]
ip = "10.0.0.5"

[ibm.ibm1]
ip = "10.0.0.3"
""",
    "users.toml": """\
[aiqums]
user = "default-user"
enc = "default-pass"

[cloudinsights]
user = "label"
enc = "type-token"
""",
    "diiapi.toml": """\
[general]
base_url = "https://general.example.invalid"
api_ro_token = "general-token"
base_api_path = "/rest/v1"
timeout = 12.0
""",
}


@pytest.fixture(autouse=True)
def _clean_env(monkeypatch: pytest.MonkeyPatch) -> Iterator[None]:
    for key in ("NF_A1_USER", "NF_A1_PASSWORD", "NF_T1_PASSWORD", "NF_T2_PASSWORD"):
        monkeypatch.delenv(key, raising=False)
    yield


@pytest.fixture
def config(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Config:
    monkeypatch.chdir(tmp_path)
    for rel, content in CONFIG_FILES.items():
        path = tmp_path / "cfg" / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
    return Config(config_dir="cfg", script_name="test")


def test_ibm_inventory_loads(config: Config) -> None:
    assert "ibm1" in config.data["ibm"]


def test_get_user_object_beats_type_default(config: Config) -> None:
    assert config.get_user("aiqums", "a1") == ("own-user", "own-pass")
    assert config.get_user("aiqums", "a2") == ("default-user", "default-pass")


def test_get_user_env_wins(config: Config, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("NF_A1_USER", "env-user")
    monkeypatch.setenv("NF_A1_PASSWORD", "env-pass")
    assert config.get_user("aiqums", "a1") == ("env-user", "env-pass")


def test_get_secret_order(config: Config, monkeypatch: pytest.MonkeyPatch) -> None:
    assert config.get_secret("cloudinsights", "t1") == "t1-token"
    assert config.get_secret("cloudinsights", "t2") == "type-token"
    assert config.get_secret("ibm", "ibm1") is None
    monkeypatch.setenv("NF_T1_PASSWORD", "env-token")
    assert config.get_secret("cloudinsights", "t1") == "env-token"


def test_get_secret_decrypts_sops(config: Config) -> None:
    config.data["cloudinsights"]["t1"]["enc"] = "SOPS[ciphertext]"
    with patch("pynetappfoundry.utils.sops.decrypt_value", return_value="plain") as dec:
        assert config.get_secret("cloudinsights", "t1") == "plain"
        assert config.get_secret("cloudinsights", "t1") == "plain"
    dec.assert_called_once_with("SOPS[ciphertext]")


def test_get_secret_error_is_sanitized(config: Config) -> None:
    config.data["cloudinsights"]["t1"]["enc"] = "SOPS[ciphertext-marker]"
    with (
        patch(
            "pynetappfoundry.utils.sops.decrypt_value",
            side_effect=SOPSError("leaky detail"),
        ),
        pytest.raises(ConfigurationError) as exc,
    ):
        config.get_secret("cloudinsights", "t1")
    assert "ciphertext-marker" not in str(exc.value)
    assert "leaky detail" not in str(exc.value)


def test_dii_settings_without_name_unchanged(config: Config) -> None:
    settings = config.get_dii_api_settings()
    assert settings.base_url == "https://general.example.invalid"
    assert settings.api_ro_token.get_secret_value() == "general-token"


def test_dii_settings_per_tenant(config: Config) -> None:
    settings = config.get_dii_api_settings("t1")
    assert settings.base_url == "https://t1.example.invalid"
    assert settings.api_ro_token.get_secret_value() == "t1-token"
    assert settings.timeout == 12.0


def test_dii_settings_tenant_falls_back_to_general_url(
    config: Config, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("NF_T2_PASSWORD", "t2-token")
    settings = config.get_dii_api_settings("t2")
    assert settings.base_url == "https://general.example.invalid"
    assert settings.api_ro_token.get_secret_value() == "t2-token"


def test_dii_rw_token_defaults_to_none(config: Config) -> None:
    assert config.get_dii_api_settings().api_rw_token is None
    assert config.get_dii_api_settings("t1").api_rw_token is None


def _with_general_rw(config: Config) -> Config:
    """Return a fresh Config whose ``diiapi.toml [general]`` also sets ``api_rw_token``.

    The ``config`` fixture has already chdir-ed into the directory holding ``cfg``.
    """
    path = Path("cfg") / "diiapi.toml"
    path.write_text(path.read_text() + 'api_rw_token = "general-rw-token"\n')
    return Config(config_dir="cfg", script_name="test")


def test_dii_rw_token_without_name_uses_general(config: Config) -> None:
    config = _with_general_rw(config)
    settings = config.get_dii_api_settings()
    assert settings.api_rw_token is not None
    assert settings.api_rw_token.get_secret_value() == "general-rw-token"


def test_dii_tenant_with_own_key_gets_no_rw_token(config: Config) -> None:
    config = _with_general_rw(config)
    settings = config.get_dii_api_settings("t1")
    assert settings.api_ro_token.get_secret_value() == "t1-token"
    assert settings.api_rw_token is None


def test_dii_tenant_without_own_key_inherits_general_keys(config: Config) -> None:
    users = Path("cfg") / "users.toml"
    users.write_text('[aiqums]\nuser = "default-user"\nenc = "default-pass"\n')
    config = _with_general_rw(config)
    settings = config.get_dii_api_settings("t2")
    assert settings.api_ro_token.get_secret_value() == "general-token"
    assert settings.api_rw_token is not None
    assert settings.api_rw_token.get_secret_value() == "general-rw-token"


def test_dii_settings_unknown_tenant_lists_names(config: Config) -> None:
    with pytest.raises(ConfigurationError, match=r"nope.*t1, t2"):
        config.get_dii_api_settings("nope")


def test_dii_tenant_rw_enc_sets_rw_token(config: Config) -> None:
    config = _with_general_rw(config)
    config.data["cloudinsights"]["t1"]["rw_enc"] = "t1-rw-token"
    settings = config.get_dii_api_settings("t1")
    assert settings.api_ro_token.get_secret_value() == "t1-token"
    assert settings.api_rw_token is not None
    assert settings.api_rw_token.get_secret_value() == "t1-rw-token"


def test_dii_tenant_rw_enc_wins_over_inherited_general_rw(config: Config) -> None:
    (Path("cfg") / "users.toml").write_text(
        '[aiqums]\nuser = "default-user"\nenc = "default-pass"\n'
    )
    config = _with_general_rw(config)
    config.data["cloudinsights"]["t2"]["rw_enc"] = "t2-rw-token"
    settings = config.get_dii_api_settings("t2")
    assert settings.api_ro_token.get_secret_value() == "general-token"
    assert settings.api_rw_token is not None
    assert settings.api_rw_token.get_secret_value() == "t2-rw-token"


def test_dii_tenant_without_rw_enc_is_unchanged(config: Config) -> None:
    (Path("cfg") / "users.toml").write_text(
        '[aiqums]\nuser = "default-user"\nenc = "default-pass"\n'
    )
    config = _with_general_rw(config)
    assert config.get_dii_api_settings("t1").api_rw_token is None
    inherited = config.get_dii_api_settings("t2").api_rw_token
    assert inherited is not None
    assert inherited.get_secret_value() == "general-rw-token"


def test_dii_tenant_rw_enc_decrypts_sops(config: Config) -> None:
    config.data["cloudinsights"]["t1"]["rw_enc"] = "SOPS[rw-ciphertext]"
    with patch("pynetappfoundry.utils.sops.decrypt_value", return_value="plain-rw") as dec:
        settings = config.get_dii_api_settings("t1")
    dec.assert_called_once_with("SOPS[rw-ciphertext]")
    assert settings.api_rw_token is not None
    assert settings.api_rw_token.get_secret_value() == "plain-rw"


def test_dii_tenant_rw_enc_ignores_environment(
    config: Config, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("NF_T1_PASSWORD", "env-token")
    monkeypatch.setenv("NF_T1_RW_PASSWORD", "env-rw")
    assert config.get_dii_api_settings("t1").api_rw_token is None


def test_dii_tenant_rw_enc_non_string_is_rejected_without_value(config: Config) -> None:
    config.data["cloudinsights"]["t1"]["rw_enc"] = ["leaky-marker"]
    with pytest.raises(ConfigurationError, match=r"rw_enc.*must be a string, not list") as exc:
        config.get_dii_api_settings("t1")
    assert "leaky-marker" not in str(exc.value)


def test_dii_tenant_rw_enc_decrypt_error_is_sanitized(config: Config) -> None:
    config.data["cloudinsights"]["t1"]["rw_enc"] = "SOPS[rw-marker]"
    with (
        patch("pynetappfoundry.utils.sops.decrypt_value", side_effect=SOPSError("leaky detail")),
        pytest.raises(ConfigurationError) as exc,
    ):
        config.get_dii_api_settings("t1")
    assert "rw-marker" not in str(exc.value)
    assert "leaky detail" not in str(exc.value)
