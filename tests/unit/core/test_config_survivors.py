"""Behavior tests for gaps the mutation run found in ``core.config`` (#1152).

Every secret here is an obviously fake placeholder. Each test builds its own config
directory under ``tmp_path`` and runs from it, so nothing reads the developer's real
config, HOME or SOPS files.
"""

from __future__ import annotations

import logging
from pathlib import Path
from types import SimpleNamespace
from typing import Any, cast
from unittest.mock import patch

import pytest

from pynetappfoundry.core import config as config_module
from pynetappfoundry.core.config import Config, ConfigurationError, resolve_tls_verify
from pynetappfoundry.utils.sops import SOPSError, SOPSNotInstalledError

CIPHER = "SOPS[placeholder-ciphertext]"
CIPHER_2 = "SOPS[placeholder-ciphertext-two]"
FAKE = "placeholder-plain-value"
DECRYPT = "pynetappfoundry.utils.sops.decrypt_value"
DECRYPT_REASON = (
    "sops could not decrypt it; check that sops and your age key (SOPS_AGE_KEY_FILE) are available"
)
_LOG_FILE = Path(config_module.__file__).name
INVENTORY = '[settings]\ntype = "data"\n'

_ENV_NAMES = (
    "NF_CONSOLE_USER",
    "NF_CONSOLE_PASSWORD",
    "NF__PASSWORD",
    "NF_T1_PASSWORD",
    "NF_T1_USER",
    "NF_MYOBJ_USER",
    "NF_MYOBJ_PASSWORD",
    "NF_MY_OBJ_PASSWORD",
    "NF_C1_USER",
    "NF_C1_PASSWORD",
    "NF_SO1_USER",
    "NF_SO1_PASSWORD",
)


@pytest.fixture(autouse=True)
def _isolated(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Run from ``tmp_path`` (Config creates ``data/`` under the cwd) with a clean env."""
    monkeypatch.chdir(tmp_path)
    for name in _ENV_NAMES:
        monkeypatch.delenv(name, raising=False)


def _cfg(tmp_path: Path, files: dict[str, str] | None = None) -> Config:
    root = tmp_path / "cfg"
    root.mkdir(exist_ok=True)
    for rel, content in (files or {}).items():
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
    return Config(config_dir=str(root), script_name="t")


def _decrypt_failure(field: str, file: str, section: str, reason: str = DECRYPT_REASON) -> str:
    return f"Failed to decrypt the SOPS value of '{field}' in {file} [{section}]: {reason}"


# --- __init__ ---------------------------------------------------------------------


class TestInit:
    def test_defaults_are_relative_to_the_working_directory(self, tmp_path: Path) -> None:
        (tmp_path / "config").mkdir()
        cfg = Config()
        cwd = Path.cwd()
        assert cfg.config_dir == cwd / "config"
        assert cfg.script_name == ""
        assert cfg.args is None
        assert cfg.data_dir == cwd / "data"
        assert cfg.output_dir == cwd / "data" / "output"
        assert cfg.db_dir == cwd / "data" / "db"
        assert cfg.files_dir == cwd / "data" / "files"
        assert cfg.log_dir == cwd / "data" / "logs"

    def test_args_are_kept(self, tmp_path: Path) -> None:
        args = object()
        cfg = Config(config_dir=str(tmp_path / "cfg"), script_name="t", args=args)
        assert cfg.args is args

    def test_azure_data_is_loaded(self, tmp_path: Path) -> None:
        cfg = _cfg(tmp_path, {"az.toml": INVENTORY + '[azure.sub1]\nsubscription = "s-1"\n'})
        assert cfg.data["azure"] == {"sub1": {"subscription": "s-1"}}

    def test_top_level_settings_are_logged(
        self, tmp_path: Path, caplog: pytest.LogCaptureFixture
    ) -> None:
        caplog.set_level(logging.DEBUG)
        cfg = _cfg(tmp_path, {"extra.toml": "x = 1\n"})
        assert f"Toplevel settings: {list(cfg.settings.keys())}" in caplog.messages


# --- scopes, _walk and get_setting errors --------------------------------------------


class TestScopeTreeErrors:
    def test_unknown_scope_lists_the_available_ones_sorted(self, tmp_path: Path) -> None:
        cfg = _cfg(tmp_path, {"b/scope.toml": "", "a/scope.toml": ""})
        with pytest.raises(ConfigurationError) as exc:
            cfg.get_scope_settings("x")
        assert str(exc.value) == "Unknown scope 'x' (available scopes: a, b)."

    def test_unknown_scope_without_any_scopes(self, tmp_path: Path) -> None:
        with pytest.raises(ConfigurationError) as exc:
            _cfg(tmp_path).get_scope_settings("x")
        assert str(exc.value) == "Unknown scope 'x' (available scopes: none)."


class TestWalkAndGetSetting:
    def test_found_value_has_an_empty_error(self) -> None:
        assert Config._walk({"a": {"b": 1}}, ("a", "b")) == (True, 1, "")

    def test_missing_top_level_key_names_the_root(self, tmp_path: Path) -> None:
        cfg = _cfg(tmp_path, {"a.toml": "[b]\nc = 1\n"})
        with pytest.raises(ConfigurationError) as exc:
            cfg.get_setting("zz")
        assert str(exc.value) == (
            "Missing configuration key 'zz'. Available keys at 'root': ['a']. "
            "Check your configuration files."
        )

    def test_missing_nested_key_names_the_full_parent_path(self, tmp_path: Path) -> None:
        cfg = _cfg(tmp_path, {"a.toml": "[b]\nc = 1\n"})
        with pytest.raises(ConfigurationError) as exc:
            cfg.get_setting("a", "b", "zz")
        assert str(exc.value) == (
            "Missing configuration key 'a.b.zz'. Available keys at 'a.b': ['c']. "
            "Check your configuration files."
        )

    def test_walking_into_a_scalar(self, tmp_path: Path) -> None:
        cfg = _cfg(tmp_path, {"a.toml": "[b]\nc = 1\n"})
        with pytest.raises(ConfigurationError) as exc:
            cfg.get_setting("a", "b", "c", "d")
        assert str(exc.value) == (
            "Cannot access 'd' in non-dict value at 'a.b.c'. Check your configuration files."
        )


# --- API settings readers -------------------------------------------------------------

_HINT = {
    "ontap": (
        "Ensure settings.toml has a valid [ontapapi.general] section with 'base_api_path' field."
    ),
    "dii": (
        "Ensure settings.toml has a valid [diiapi.general] section with "
        "'api_ro_token', 'base_url', and 'base_api_path' fields."
    ),
    "aiqum": "Ensure aiqumapi.toml has a valid [general] section (base_api_path, timeout).",
    "da": (
        "Ensure <config>/apis/digitaladvisor/digitaladvisorapi.toml has a [general] section "
        "with at least one of personal_access_token or refresh_token (both: the PAT is used "
        "first; access_token needs refresh_token)."
    ),
    "console": (
        "Ensure consoleapi.toml has a valid [general] section with 'base_url' and one of "
        "user_token, a refresh token (users.toml [console]), service_token or "
        "client_id/client_secret."
    ),
}

_INVALID = [
    pytest.param(
        "ontapapi.toml",
        '[general]\ntimeout = "slow"\n',
        "get_ontap_api_settings",
        "Invalid ONTAP API configuration: ",
        _HINT["ontap"],
        id="ontap",
    ),
    pytest.param(
        "diiapi.toml",
        '[general]\nbase_url = "https://dii.example.test"\n',
        "get_dii_api_settings",
        "Invalid DII API configuration: ",
        _HINT["dii"],
        id="dii",
    ),
    pytest.param(
        "aiqumapi.toml",
        '[general]\ntimeout = "slow"\n',
        "get_aiqum_api_settings",
        "Invalid AIQUM API configuration: ",
        _HINT["aiqum"],
        id="aiqum",
    ),
    pytest.param(
        "digitaladvisorapi.toml",
        "[general]\nfoo = 1\n",
        "get_digital_advisor_api_settings",
        "Invalid Digital Advisor API configuration: ",
        _HINT["da"],
        id="digital-advisor",
    ),
    pytest.param(
        "consoleapi.toml",
        "[general]\nfoo = 1\n",
        "get_console_api_settings",
        "Invalid Console API configuration: ",
        _HINT["console"],
        id="console",
    ),
]


@pytest.mark.parametrize(("fname", "body", "reader", "prefix", "hint"), _INVALID)
def test_invalid_settings_message_carries_its_remediation_hint(
    tmp_path: Path, fname: str, body: str, reader: str, prefix: str, hint: str
) -> None:
    cfg = _cfg(tmp_path, {fname: body})
    with pytest.raises(ConfigurationError) as exc:
        getattr(cfg, reader)()
    message = str(exc.value)
    assert message.startswith(prefix)
    assert message.endswith(f". {hint}")


def test_ontap_settings_read_the_general_table(tmp_path: Path) -> None:
    cfg = _cfg(tmp_path, {"ontapapi.toml": '[general]\nbase_api_path = "/custom"\n'})
    assert cfg.get_ontap_api_settings().base_api_path == "/custom"


# SOPS decrypt failures name the file and table they came from.
_DECRYPT_CONTEXT = [
    pytest.param(
        {
            "settings.toml": (
                f'[SMTP]\nserver = "smtp.example.test"\nuser = "u"\npassword = "{CIPHER}"\n'
            )
        },
        "get_smtp_settings",
        _decrypt_failure("password", "settings.toml", "SMTP"),
        id="smtp",
    ),
    pytest.param(
        {"diiapi.toml": f'[general]\nbase_url = "https://x.test"\napi_ro_token = "{CIPHER}"\n'},
        "get_dii_api_settings",
        _decrypt_failure("api_ro_token", "diiapi.toml", "general"),
        id="dii",
    ),
    pytest.param(
        {"digitaladvisorapi.toml": f'[general]\npersonal_access_token = "{CIPHER}"\n'},
        "get_digital_advisor_api_settings",
        _decrypt_failure("personal_access_token", "digitaladvisorapi.toml", "general"),
        id="digital-advisor",
    ),
]


@pytest.mark.parametrize(("files", "reader", "expected"), _DECRYPT_CONTEXT)
def test_decrypt_failure_names_file_and_section(
    tmp_path: Path, files: dict[str, str], reader: str, expected: str
) -> None:
    cfg = _cfg(tmp_path, files)
    with (
        patch(DECRYPT, side_effect=SOPSError("secret-detail")),
        pytest.raises(ConfigurationError) as exc,
    ):
        getattr(cfg, reader)()
    assert str(exc.value) == expected


class TestDiiTenant:
    def test_unknown_tenant_with_no_inventory(self, tmp_path: Path) -> None:
        cfg = _cfg(tmp_path, {"diiapi.toml": '[general]\nbase_url = "https://x.test"\n'})
        with pytest.raises(ConfigurationError) as exc:
            cfg.get_dii_api_settings("nope")
        assert str(exc.value) == (
            "No Cloud Insights tenant named 'nope' in the [cloudinsights] inventory "
            "(available: none)."
        )

    def test_tenant_without_secret_decrypts_general_with_its_context(self, tmp_path: Path) -> None:
        cfg = _cfg(
            tmp_path,
            {
                "diiapi.toml": (
                    f'[general]\nbase_url = "https://x.test"\napi_ro_token = "{CIPHER}"\n'
                ),
                "inv.toml": INVENTORY + '[cloudinsights.t1]\nbase_url = "https://t1.test"\n',
            },
        )
        with (
            patch(DECRYPT, side_effect=SOPSError("secret-detail")),
            pytest.raises(ConfigurationError) as exc,
        ):
            cfg.get_dii_api_settings("t1")
        assert str(exc.value) == _decrypt_failure("api_ro_token", "diiapi.toml", "general")

    def test_non_table_general_is_ignored_for_a_tenant(self, tmp_path: Path) -> None:
        cfg = _cfg(
            tmp_path,
            {
                "diiapi.toml": 'general = "not-a-table"\n',
                "inv.toml": INVENTORY
                + f'[cloudinsights.t1]\nbase_url = "https://t1.test"\nenc = "{FAKE}"\n',
            },
        )
        settings = cfg.get_dii_api_settings("t1")
        assert settings.base_url == "https://t1.test"
        assert settings.api_ro_token.get_secret_value() == FAKE


# --- Console --------------------------------------------------------------------------

_CONSOLE_GENERAL = '[general]\nbase_url = "https://api.example.test"\nservice_token = "fake-svc"\n'


class TestConsole:
    def test_refresh_token_in_consoleapi_toml_is_rejected(self, tmp_path: Path) -> None:
        cfg = _cfg(tmp_path, {"consoleapi.toml": _CONSOLE_GENERAL + 'refresh_token = "fake"\n'})
        with pytest.raises(ConfigurationError) as exc:
            cfg.get_console_api_settings()
        assert str(exc.value) == (
            "consoleapi.toml must not contain 'refresh_token'. Store the Console refresh "
            "token in users.toml under [console] ('enc'), for example with "
            "'nf config set-credential --type console'."
        )

    def test_scope_without_console_account(self, tmp_path: Path) -> None:
        cfg = _cfg(tmp_path, {"s/scope.toml": ""})
        with pytest.raises(ConfigurationError) as exc:
            cfg.get_console_api_settings(scope="s")
        assert str(exc.value) == (
            "Scope 's' has no Console account: add s/consoleapi.toml with a [general] table. "
            "A scope never falls back to the root Console account."
        )

    def test_scope_general_must_be_a_table(self, tmp_path: Path) -> None:
        cfg = _cfg(tmp_path, {"s/scope.toml": "", "s/consoleapi.toml": 'general = "x"\n'})
        with pytest.raises(ConfigurationError) as exc:
            cfg.get_console_api_settings(scope="s")
        assert str(exc.value) == "s/consoleapi.toml [general] must be a table."

    def test_root_refresh_token_failure_is_reworded_and_logged(
        self, tmp_path: Path, caplog: pytest.LogCaptureFixture
    ) -> None:
        cfg = _cfg(
            tmp_path,
            {
                "consoleapi.toml": _CONSOLE_GENERAL,
                "users.toml": f'[console]\nuser = "label"\nenc = "{CIPHER}"\n',
            },
        )
        with (
            patch(DECRYPT, side_effect=SOPSError("boom")),
            pytest.raises(ConfigurationError) as exc,
        ):
            cfg.get_console_api_settings()
        assert str(exc.value) == (
            "Could not resolve the Console refresh token from users.toml [console] "
            "(or NF_CONSOLE_USER/NF_CONSOLE_PASSWORD); check the 'user' and 'enc' "
            "keys and, for a SOPS value, that sops and its key are available."
        )
        assert "Failed to decrypt SOPS value for 'console': boom" in caplog.messages

    def test_scope_refresh_token_decrypt_failure_names_the_scope_file(self, tmp_path: Path) -> None:
        cfg = _cfg(
            tmp_path,
            {
                "s/scope.toml": "",
                "s/consoleapi.toml": _CONSOLE_GENERAL,
                "s/users.toml": f'[console]\nuser = "label"\nenc = "{CIPHER}"\n',
            },
        )
        with (
            patch(DECRYPT, side_effect=SOPSError("boom")),
            pytest.raises(ConfigurationError) as exc,
        ):
            cfg.get_console_api_settings(scope="s")
        assert str(exc.value) == _decrypt_failure("enc", "s/users.toml", "console")

    @pytest.mark.parametrize(
        "users",
        [
            pytest.param('console = "not-a-table"\n', id="not-a-table"),
            pytest.param('[console]\nenc = "fake-enc"\n', id="no-user"),
            pytest.param('[console]\nuser = "label"\n', id="no-enc"),
            pytest.param('[console]\nuser = "label"\nenc = 123\n', id="enc-not-a-string"),
        ],
    )
    def test_scope_refresh_token_section_must_be_complete(self, tmp_path: Path, users: str) -> None:
        cfg = _cfg(
            tmp_path,
            {
                "s/scope.toml": "",
                "s/consoleapi.toml": _CONSOLE_GENERAL,
                "s/users.toml": users,
            },
        )
        with pytest.raises(ConfigurationError) as exc:
            cfg.get_console_api_settings(scope="s")
        assert str(exc.value) == (
            "Could not resolve the Console refresh token from s/users.toml "
            "[console]; check the 'user' and 'enc' keys."
        )


# --- get_user -------------------------------------------------------------------------


class TestGetUser:
    def test_default_type_is_clusters(self, tmp_path: Path) -> None:
        cfg = _cfg(tmp_path, {"users.toml": '[clusters]\nuser = "admin"\nenc = "fake-pass"\n'})
        assert cfg.get_user() == ("admin", "fake-pass")

    def test_missing_user_without_object(self, tmp_path: Path) -> None:
        with pytest.raises(ConfigurationError) as exc:
            _cfg(tmp_path).get_user()
        assert str(exc.value) == (
            "Could not find user for type='clusters', object=''. "
            "Set NF_<OBJECT>_USER environment variable, or configure in "
            "users.toml (root or the object's scope) or the object's data file."
        )

    def test_missing_user_with_object(self, tmp_path: Path) -> None:
        with pytest.raises(ConfigurationError) as exc:
            _cfg(tmp_path).get_user("clusters", "my-obj")
        assert str(exc.value) == (
            "Could not find user for type='clusters', object='my-obj'. "
            "Set NF_MY_OBJ_USER environment variable, or configure in "
            "users.toml (root or the object's scope) or the object's data file."
        )

    def test_missing_password_without_object(self, tmp_path: Path) -> None:
        cfg = _cfg(tmp_path, {"users.toml": '[clusters]\nuser = "admin"\n'})
        with pytest.raises(ConfigurationError) as exc:
            cfg.get_user()
        assert str(exc.value) == (
            "Could not find password for type='clusters', object=''. "
            "Set NF_<OBJECT>_PASSWORD environment variable, "
            "or configure 'enc' in config files."
        )

    def test_missing_password_with_object(self, tmp_path: Path) -> None:
        cfg = _cfg(tmp_path, {"users.toml": '[clusters]\nuser = "admin"\n'})
        with pytest.raises(ConfigurationError) as exc:
            cfg.get_user("clusters", "my-obj")
        assert str(exc.value) == (
            "Could not find password for type='clusters', object='my-obj'. "
            "Set NF_MY_OBJ_PASSWORD environment variable, "
            "or configure 'enc' in config files."
        )

    def test_missing_credentials_are_logged(
        self, tmp_path: Path, caplog: pytest.LogCaptureFixture
    ) -> None:
        with pytest.raises(ConfigurationError):
            _cfg(tmp_path).get_user("clusters", "x")
        assert "Could not find user for clusters and x" in caplog.messages
        cfg = _cfg(tmp_path, {"users.toml": '[clusters]\nuser = "admin"\n'})
        with pytest.raises(ConfigurationError):
            cfg.get_user("clusters", "x")
        assert "Could not find password for clusters and x" in caplog.messages

    def test_environment_use_is_logged(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture
    ) -> None:
        monkeypatch.setenv("NF_MYOBJ_USER", "env-user")
        monkeypatch.setenv("NF_MYOBJ_PASSWORD", "env-pass")
        caplog.set_level(logging.DEBUG)
        assert _cfg(tmp_path).get_user("clusters", "myobj") == ("env-user", "env-pass")
        assert "Using user from NF_MYOBJ_USER" in caplog.messages
        assert "Using password from NF_MYOBJ_PASSWORD" in caplog.messages

    def test_env_password_alone_still_reads_the_object_user(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv("NF_C1_PASSWORD", "env-pass")
        cfg = _cfg(
            tmp_path,
            {
                "inv.toml": INVENTORY + '[aiqums.c1]\nuser = "entry-user"\n',
                "users.toml": '[aiqums]\nuser = "default-user"\nenc = "default-pass"\n',
            },
        )
        assert cfg.get_user("aiqums", "c1") == ("entry-user", "env-pass")

    def test_env_user_alone_still_reads_the_object_password(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv("NF_C1_USER", "env-user")
        cfg = _cfg(
            tmp_path,
            {
                "inv.toml": INVENTORY + '[aiqums.c1]\nenc = "entry-pass"\n',
                "users.toml": '[aiqums]\nuser = "default-user"\nenc = "default-pass"\n',
            },
        )
        assert cfg.get_user("aiqums", "c1") == ("env-user", "entry-pass")

    def test_env_password_alone_still_reads_the_scope_user(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv("NF_SO1_PASSWORD", "env-pass")
        cfg = _cfg(
            tmp_path,
            {
                "s/scope.toml": "",
                "s/inv.toml": INVENTORY + '[aiqums.so1]\nip = "10.0.0.1"\n',
                "s/users.toml": '[aiqums]\nuser = "scope-user"\nenc = "scope-pass"\n',
                "users.toml": '[aiqums]\nuser = "root-user"\nenc = "root-pass"\n',
            },
        )
        assert cfg.get_user("aiqums", "so1") == ("scope-user", "env-pass")


# --- get_secret -----------------------------------------------------------------------

_SECRET_USERS = '[cloudinsights]\nuser = "label"\nenc = "root-secret"\n'


class TestGetSecret:
    def test_empty_object_never_reads_an_environment_variable(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv("NF__PASSWORD", "env-fake")
        cfg = _cfg(tmp_path, {"users.toml": _SECRET_USERS})
        assert cfg.get_secret("cloudinsights", "") == "root-secret"

    def test_type_with_no_inventory_falls_back_to_users_toml(self, tmp_path: Path) -> None:
        cfg = _cfg(tmp_path, {"users.toml": _SECRET_USERS})
        assert cfg.get_secret("cloudinsights", "t1") == "root-secret"

    def test_empty_enc_is_no_secret(self, tmp_path: Path) -> None:
        cfg = _cfg(tmp_path, {"inv.toml": INVENTORY + '[cloudinsights.t1]\nenc = ""\n'})
        assert cfg.get_secret("cloudinsights", "t1") is None

    def test_non_string_enc_on_the_data_entry_raises(self, tmp_path: Path) -> None:
        cfg = _cfg(tmp_path, {"inv.toml": INVENTORY + "[cloudinsights.t1]\nenc = 123\n"})
        with pytest.raises(ConfigurationError) as exc:
            cfg.get_secret("cloudinsights", "t1")
        assert "the object's data file [cloudinsights.t1]" in str(exc.value)
        assert "must be a string" in str(exc.value)

    def test_non_string_enc_in_scope_users_toml_raises(self, tmp_path: Path) -> None:
        cfg = _cfg(
            tmp_path,
            {
                "s/scope.toml": "",
                "s/inv.toml": INVENTORY + '[cloudinsights.t1]\nbase_url = "https://t1.test"\n',
                "s/users.toml": '[cloudinsights]\nuser = "label"\nenc = 123\n',
            },
        )
        with pytest.raises(ConfigurationError) as exc:
            cfg.get_secret("cloudinsights", "t1")
        assert "s/users.toml [cloudinsights]" in str(exc.value)

    def test_non_string_enc_in_root_users_toml_raises(self, tmp_path: Path) -> None:
        cfg = _cfg(tmp_path, {"users.toml": '[cloudinsights]\nuser = "label"\nenc = 123\n'})
        with pytest.raises(ConfigurationError) as exc:
            cfg.get_secret("cloudinsights", "t1")
        assert "users.toml [cloudinsights]" in str(exc.value)

    def test_decrypt_failure_from_the_data_entry(self, tmp_path: Path) -> None:
        cfg = _cfg(tmp_path, {"inv.toml": INVENTORY + f'[cloudinsights.t1]\nenc = "{CIPHER}"\n'})
        with (
            patch(DECRYPT, side_effect=SOPSError("boom")),
            pytest.raises(ConfigurationError) as exc,
        ):
            cfg.get_secret("cloudinsights", "t1")
        assert str(exc.value) == _decrypt_failure(
            "enc", "the object's data file", "cloudinsights.t1"
        )

    def test_decrypt_failure_from_the_environment(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.setenv("NF_T1_PASSWORD", CIPHER)
        with (
            patch(DECRYPT, side_effect=SOPSError("boom")),
            pytest.raises(ConfigurationError) as exc,
        ):
            _cfg(tmp_path).get_secret("cloudinsights", "t1")
        assert str(exc.value) == _decrypt_failure("enc", "environment", "cloudinsights.t1")

    def test_decrypt_failure_from_root_users_toml(self, tmp_path: Path) -> None:
        cfg = _cfg(tmp_path, {"users.toml": f'[cloudinsights]\nuser = "label"\nenc = "{CIPHER}"\n'})
        with (
            patch(DECRYPT, side_effect=SOPSError("boom")),
            pytest.raises(ConfigurationError) as exc,
        ):
            cfg.get_secret("cloudinsights", "t1")
        assert str(exc.value) == _decrypt_failure("enc", "users.toml", "cloudinsights")

    def test_decrypt_failure_from_scope_users_toml(self, tmp_path: Path) -> None:
        cfg = _cfg(
            tmp_path,
            {
                "s/scope.toml": "",
                "s/inv.toml": INVENTORY + '[cloudinsights.t1]\nbase_url = "https://t1.test"\n',
                "s/users.toml": f'[cloudinsights]\nuser = "label"\nenc = "{CIPHER}"\n',
            },
        )
        with (
            patch(DECRYPT, side_effect=SOPSError("boom")),
            pytest.raises(ConfigurationError) as exc,
        ):
            cfg.get_secret("cloudinsights", "t1")
        assert str(exc.value) == _decrypt_failure("enc", "s/users.toml", "cloudinsights")


# --- _decrypt_setting_fields / _decrypt_if_encrypted ----------------------------------


class TestDecryptSettingFields:
    def test_plain_field_does_not_stop_later_fields(self, tmp_path: Path) -> None:
        cfg = _cfg(tmp_path)
        with patch(DECRYPT, return_value=FAKE):
            result = cfg._decrypt_setting_fields(
                {"a": "plain", "b": CIPHER}, ("a", "b"), file="f.toml", section="s"
            )
        assert result == {"a": "plain", "b": FAKE}

    def test_cached_field_does_not_stop_later_fields(self, tmp_path: Path) -> None:
        cfg = _cfg(tmp_path)
        with patch(DECRYPT, side_effect=lambda v: f"plain:{v}") as decrypt:
            result = cfg._decrypt_setting_fields(
                {"a": CIPHER, "b": CIPHER, "c": CIPHER_2},
                ("a", "b", "c"),
                file="f.toml",
                section="s",
            )
        assert result == {"a": f"plain:{CIPHER}", "b": f"plain:{CIPHER}", "c": f"plain:{CIPHER_2}"}
        assert decrypt.call_count == 2

    @pytest.mark.parametrize(
        ("error", "reason"),
        [
            pytest.param(SOPSError("secret-detail"), DECRYPT_REASON, id="generic"),
            pytest.param(
                SOPSNotInstalledError("secret-detail"), "sops is not installed", id="no-sops"
            ),
        ],
    )
    def test_failure_message_and_log(
        self,
        tmp_path: Path,
        caplog: pytest.LogCaptureFixture,
        error: SOPSError,
        reason: str,
    ) -> None:
        cfg = _cfg(tmp_path)
        with patch(DECRYPT, side_effect=error), pytest.raises(ConfigurationError) as exc:
            cfg._decrypt_setting_fields({"enc": CIPHER}, ("enc",), file="f.toml", section="sec")
        assert str(exc.value) == _decrypt_failure("enc", "f.toml", "sec", reason)
        # Only ERROR records: building the Config logs DEBUG lines that are captured
        # whenever an earlier test on the same worker lowered the log level.
        errors = [r.getMessage() for r in caplog.records if r.levelno >= logging.ERROR]
        assert errors == [
            f"Failed to decrypt SOPS value of 'enc' in f.toml [sec]: {type(error).__name__}"
        ]

    def test_decrypt_if_encrypted_failure_is_logged(
        self, tmp_path: Path, caplog: pytest.LogCaptureFixture
    ) -> None:
        cfg = _cfg(tmp_path)
        with patch(DECRYPT, side_effect=SOPSError("boom")), pytest.raises(ConfigurationError):
            cfg._decrypt_if_encrypted(CIPHER, object_name="obj")
        assert "Failed to decrypt SOPS value for 'obj': boom" in caplog.messages


# --- searchable keys, relaxation, find_closest, chk_or ---------------------------------


class TestSearchableKeys:
    def test_missing_name_and_keys_are_filled_in(self, tmp_path: Path) -> None:
        cfg = _cfg(
            tmp_path,
            {
                "settings.toml": '[aiqums]\nsearchable_keys = ["bu", "env"]\n',
                "inv.toml": INVENTORY
                + '[aiqums.q1]\nip = "1"\nbu = "B"\n[aiqums.q2]\nname = "custom"\nip = "2"\n',
            },
        )
        assert cfg.data["aiqums"] == {
            "q1": {"ip": "1", "bu": "B", "env": "", "name": "q1"},
            "q2": {"name": "custom", "ip": "2", "bu": "", "env": ""},
        }

    def test_searchable_keys_without_any_inventory(self, tmp_path: Path) -> None:
        cfg = _cfg(tmp_path, {"settings.toml": '[azure]\nsearchable_keys = ["x"]\n'})
        assert cfg.data == {}


class TestRelaxationOrder:
    def test_default_order_without_any_settings_file(self, tmp_path: Path) -> None:
        assert _cfg(tmp_path).get_relaxation_order("clusters") == [
            "region",
            "subapp",
            "cloud",
            "env",
            "app",
            "bu",
            "div",
        ]


_QUERIES = (
    '[aiqums.q1]\nip = "1"\nbu = "Eng"\nenv = "Dev"\ncloud = "aws"\n'
    '[aiqums.q2]\nip = "2"\nbu = "Eng"\nenv = "Prod"\ncloud = "gcp"\n'
    '[aiqums.q3]\nip = "3"\nbu = "Fin"\nenv = "Prod"\ncloud = "aws"\n'
)


class TestFindClosest:
    def _config(self, tmp_path: Path, order: str = "") -> Config:
        files = {"inv.toml": INVENTORY + _QUERIES}
        if order:
            files["settings.toml"] = f"[aiqums]\nrelaxation_order = {order}\n"
        return _cfg(tmp_path, files)

    def test_explicit_relaxation_order_is_used(self, tmp_path: Path) -> None:
        cfg = self._config(tmp_path, '["bu", "env"]')
        found = cfg.find_closest("aiqums", {"bu": "Fin", "env": "Dev"})
        assert found is not None
        assert found["ip"] == "1"

    def test_scope_key_in_the_order_is_skipped_not_a_stop(self, tmp_path: Path) -> None:
        cfg = self._config(tmp_path, '["scope", "env"]')
        found = cfg.find_closest("aiqums", {"bu": "Fin", "env": "Dev"})
        assert found is not None
        assert found["ip"] == "3"

    def test_empty_values_are_dropped_before_the_first_search(self, tmp_path: Path) -> None:
        found = self._config(tmp_path).find_closest("aiqums", {"cloud": "gcp", "env": ""})
        assert found is not None
        assert found["ip"] == "2"

    def test_relaxation_is_logged(self, tmp_path: Path, caplog: pytest.LogCaptureFixture) -> None:
        cfg = self._config(tmp_path, '["bu", "env"]')
        caplog.set_level(logging.DEBUG)
        cfg.find_closest("aiqums", {"bu": "Fin", "env": "Dev"})
        messages = "\n".join(caplog.messages)
        assert f"{_LOG_FILE} :find_closest" in caplog.messages
        assert f"{_LOG_FILE} :  data_type = 'aiqums'" in caplog.messages
        assert f"{_LOG_FILE} :  tree = {{'bu': 'Fin', 'env': 'Dev'}}" in caplog.messages
        assert f"{_LOG_FILE} :  initial search tree = {{'bu': 'Fin', 'env': 'Dev'}}" in (
            caplog.messages
        )
        assert "removing bu and searching tree = {'bu': 'Fin', 'env': 'Dev'}" in messages
        assert "find_closest - found = " in messages
        assert "search_returned {" in messages


class TestChkOr:
    def test_alternatives_may_contain_spaces(self, tmp_path: Path) -> None:
        cfg = _cfg(tmp_path)
        assert cfg.chk_or("us east || eu west", "us east") is True
        assert cfg.chk_or("us east || eu west", ["eu west"]) is True
        assert cfg.chk_or("us east || eu west", "us") is False


# --- logging of search and loading ----------------------------------------------------


class TestSearchLogging:
    def test_search_logs_each_item_and_decision(
        self, tmp_path: Path, caplog: pytest.LogCaptureFixture
    ) -> None:
        cfg = _cfg(
            tmp_path,
            {"inv.toml": INVENTORY + '[aiqums.q1]\nbu = "A"\n[aiqums.q2]\nenv = "x"\n'},
        )
        caplog.set_level(logging.DEBUG)
        assert list(cfg.search("aiqums", {"bu": "A"})) == ["q1"]
        text = "\n".join(caplog.messages)
        assert "data_type = 'aiqums'" in text
        assert "search_dict = {'bu': 'A'}" in text
        assert f"{_LOG_FILE} :    search:" in caplog.messages
        assert f"{_LOG_FILE} :      search: item - q1" in caplog.messages
        assert "search: checking bu" in text
        assert "search: check_term A, A returned True" in text
        assert "search: item - q1 matched" in text
        assert "search: bu not in item details, did not match" in text
        assert "search: item - q2 did not match" in text
        assert "search returned - ['q1']" in text


class TestLoadingLogs:
    def test_files_and_data_are_logged(
        self, tmp_path: Path, caplog: pytest.LogCaptureFixture
    ) -> None:
        caplog.set_level(logging.DEBUG)
        cfg = _cfg(
            tmp_path,
            {
                "inv.toml": INVENTORY + '[aiqums.q1]\nip = "1"\n',
                "other.toml": "x = 1\n",
                "s/scope.toml": "",
                "s/users.toml": '[clusters]\nuser = "u"\nenc = "e"\n',
            },
        )
        root = cfg.config_dir
        text = "\n".join(caplog.messages)
        assert f"parsing {root / 'inv.toml'}" in text
        assert "data file: inv" in text
        assert "adding 1 aiqums items" in text
        assert "config file: other" in text
        assert "scope s config file: users" in text
        listed = next(m for m in caplog.messages if "loaded the following files: " in m)
        paths = listed.split("loaded the following files: ", 1)[1].split(", ")
        assert sorted(paths) == sorted(
            str(root / rel) for rel in ("inv.toml", "other.toml", "s/users.toml")
        )

    def test_invalid_licensing_is_warned_about(
        self, tmp_path: Path, caplog: pytest.LogCaptureFixture
    ) -> None:
        cfg = _cfg(tmp_path, {"settings.toml": '[licensing]\nmailfrom = "a@x.test"\n'})
        assert cfg.get_licensing_settings() is None
        warnings = [r.getMessage() for r in caplog.records if r.levelno == logging.WARNING]
        assert len(warnings) == 1
        assert warnings[0].startswith("Invalid licensing configuration: ")
        assert "mailto" in warnings[0]


class TestLoadingErrors:
    def test_scope_marker_at_the_root(self, tmp_path: Path) -> None:
        root = tmp_path / "cfg"
        with pytest.raises(ConfigurationError) as exc:
            _cfg(tmp_path, {"scope.toml": ""})
        assert str(exc.value) == (
            f"{root / 'scope.toml'}: scope.toml is only valid directly inside a top-level "
            "directory of the config dir (not at the root, nested deeper, or in "
            "a hidden or 'apis' directory)."
        )

    def test_duplicate_object_name(self, tmp_path: Path) -> None:
        files = {
            "a.toml": INVENTORY + '[aiqums.q1]\nip = "1"\n',
            "b.toml": INVENTORY + '[aiqums.q1]\nip = "2"\n',
        }
        with pytest.raises(ConfigurationError) as exc:
            _cfg(tmp_path, files)
        message = str(exc.value)
        assert message.startswith("Duplicate aiqums name 'q1' in ")
        assert message.endswith("; object names must be unique across the config directory")

    def test_same_scope_settings_file_stem_in_two_directories_merges(self, tmp_path: Path) -> None:
        cfg = _cfg(
            tmp_path,
            {
                "s/scope.toml": "",
                "s/users.toml": '[console]\nuser = "a"\nenc = "e1"\n',
                "s/sub/users.toml": '[clusters]\nuser = "b"\nenc = "e2"\n',
            },
        )
        assert set(cfg.get_scope_settings("s")["users"]) == {"console", "clusters"}


# --- resolve_tls_verify ----------------------------------------------------------------


def _tls_config(**kwargs: Any) -> Config:
    return cast("Config", SimpleNamespace(**kwargs))


class TestResolveTlsVerify:
    def test_non_dict_data_and_settings_count_as_empty(self) -> None:
        cfg = _tls_config(data=None, settings=None, config_dir=Path.cwd())
        assert resolve_tls_verify(cfg, "c") is False

    def test_non_dict_inventory_section_counts_as_empty(self) -> None:
        cfg = _tls_config(data={"clusters": "oops"}, settings={}, config_dir=Path.cwd())
        assert resolve_tls_verify(cfg, "c") is False

    def test_non_dict_api_settings_count_as_empty(self) -> None:
        cfg = _tls_config(data={}, settings={"ontapapi": "oops"}, config_dir=Path.cwd())
        assert resolve_tls_verify(cfg, "c") is False

    def test_relative_bundle_without_a_config_dir_resolves_against_the_cwd(
        self, tmp_path: Path
    ) -> None:
        (tmp_path / "bundle.pem").write_text("fake")
        cfg = _tls_config(
            data={"clusters": {"c": {"ca_bundle": "bundle.pem"}}}, settings={}, config_dir=None
        )
        assert Path(cast("str", resolve_tls_verify(cfg, "c"))) == Path.cwd() / "bundle.pem"

    def test_global_error_names_the_settings_table(self) -> None:
        cfg = _tls_config(
            data={},
            settings={"ontapapi": {"general": {"verify_ssl": "yes"}}},
            config_dir=Path.cwd(),
        )
        with pytest.raises(ConfigurationError) as exc:
            resolve_tls_verify(cfg, "c")
        assert str(exc.value) == "ontapapi.general.verify_ssl must be true or false, got 'yes'."

    def test_bundle_and_verify_false_contradict(self) -> None:
        cfg = _tls_config(
            data={"clusters": {"c": {"ca_bundle": "x.pem", "verify_ssl": False}}},
            settings={},
            config_dir=Path.cwd(),
        )
        with pytest.raises(ConfigurationError) as exc:
            resolve_tls_verify(cfg, "c")
        assert str(exc.value) == (
            "clusters.c.ca_bundle is set together with clusters.c.verify_ssl = false; "
            "remove one of them."
        )

    def test_missing_bundle_file_message_names_the_path(self, tmp_path: Path) -> None:
        missing = tmp_path / "missing.pem"
        cfg = _tls_config(
            data={"clusters": {"c": {"ca_bundle": str(missing)}}},
            settings={},
            config_dir=Path.cwd(),
        )
        with pytest.raises(ConfigurationError) as exc:
            resolve_tls_verify(cfg, "c")
        assert str(exc.value) == (
            f"clusters.c.ca_bundle is {str(missing)!r}, which is not an existing CA bundle file."
        )

    def test_unreadable_bundle_message_names_the_path(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        bundle = tmp_path / "bundle.pem"
        bundle.write_text("fake")
        monkeypatch.setattr("pynetappfoundry.core.config.os.access", lambda *a, **k: False)
        cfg = _tls_config(
            data={"clusters": {"c": {"ca_bundle": str(bundle)}}},
            settings={},
            config_dir=Path.cwd(),
        )
        with pytest.raises(ConfigurationError) as exc:
            resolve_tls_verify(cfg, "c")
        assert str(exc.value) == (
            f"clusters.c.ca_bundle is {str(bundle)!r}, which is not readable."
        )
