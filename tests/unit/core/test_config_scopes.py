"""Tests for scope directories in the config dir (#1080)."""

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from pynetappfoundry.core.config import Config, ConfigurationError
from pynetappfoundry.utils.sops import SOPSError

CIPHERTEXT = "SOPS[placeholder-ciphertext]"

ROOT_FILES = {
    "root/inventory.toml": """\
[settings]
type = "data"

[clusters.root-cl]
ip = "10.0.0.1"

[connectors.root-conn]
ip = "10.0.0.2"
agent_id = "root-agent"

[cloudinsights.root-ci]
base_url = "https://root-ci.example.invalid"
""",
    "users.toml": """\
[clusters]
user = "root-user"
enc = "root-pass"

[cloudinsights]
user = "label"
enc = "root-token"

[console]
user = "root-label"
enc = "root-refresh"
""",
    "monitoring.toml": """\
[settings]
default_thresholds = {inodes = 80, volume = 90}
root_only = 1
""",
    "consoleapi.toml": """\
[general]
base_url = "https://api.root.example.invalid"
ui_base_url = "https://ui.root.example.invalid"
base_api_path = "/root"
timeout = 11.0
org_id = "root-org"
agent_ids = ["root-agent"]
service_token = "root-service-token"
""",
}

SCOPE_FILES = {
    "Org1/scope.toml": 'name = "Org1"\ndescription = "d"\ntags = ["a"]\n',
    "Org1/inv.toml": """\
[settings]
type = "data"

[clusters.org1-cl]
ip = "10.1.0.1"
user = "own-user"
enc = "own-pass"

[clusters.org1-cl2]
ip = "10.1.0.2"

[connectors.org1-conn]
ip = "10.1.0.3"
agent_id = "org1-agent"

[cloudinsights.org1-ci]
ip = "10.1.0.4"
""",
    "Org1/sub/more.toml": """\
[settings]
type = "data"

[clusters.org1-nested]
ip = "10.1.0.5"
""",
    "Org1/users.toml": """\
[clusters]
user = "org1-user"
enc = "org1-pass"

[cloudinsights]
enc = "org1-token"

[console]
user = "org1-label"
enc = "org1-refresh"
""",
    "Org1/monitoring.toml": """\
[settings]
default_thresholds = {inodes = 70}
""",
    "Org1/consoleapi.toml": """\
[general]
base_url = "https://api.org1.example.invalid"
org_id = "org1-org"
agent_ids = ["org1-agent"]
service_token = "org1-service-token"
""",
    "plain/inv.toml": """\
[settings]
type = "data"

[clusters.plain-cl]
ip = "10.2.0.1"
""",
}


@pytest.fixture(autouse=True)
def _clean_env(monkeypatch: pytest.MonkeyPatch) -> None:
    for key in (
        "NF_ORG1_CL_USER",
        "NF_ORG1_CL_PASSWORD",
        "NF_ORG1_CL2_PASSWORD",
        "NF_CONSOLE_USER",
        "NF_CONSOLE_PASSWORD",
    ):
        monkeypatch.delenv(key, raising=False)


def _write(base: Path, files: dict[str, str]) -> None:
    for rel, content in files.items():
        path = base / "cfg" / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)


def _load(base: Path, monkeypatch: pytest.MonkeyPatch, *file_sets: dict[str, str]) -> Config:
    monkeypatch.chdir(base)
    for files in file_sets:
        _write(base, files)
    return Config(config_dir="cfg", script_name="test")


@pytest.fixture
def scoped(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Config:
    return _load(tmp_path, monkeypatch, ROOT_FILES, SCOPE_FILES)


@pytest.fixture
def unscoped(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Config:
    return _load(tmp_path, monkeypatch, ROOT_FILES)


# --- no scope.toml: unchanged behaviour -------------------------------------


def test_without_scopes_nothing_changes(unscoped: Config) -> None:
    assert unscoped.scopes == {}
    assert unscoped.scope_settings == {}
    assert unscoped.get_scope("clusters", "root-cl") is None
    assert "root-cl" in unscoped.data["clusters"]
    assert unscoped.settings["users"]["clusters"]["user"] == "root-user"
    assert unscoped.get_user("clusters", "root-cl") == ("root-user", "root-pass")


def test_missing_config_dir_loads_empty(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(tmp_path)
    config = Config(config_dir="nope", script_name="test")
    assert config.scopes == {}
    assert config.data == {}


# --- loading ----------------------------------------------------------------


def test_scope_data_is_attributed_including_subdirectories(scoped: Config) -> None:
    assert set(scoped.scopes) == {"Org1"}
    assert scoped.scopes["Org1"].description == "d"
    assert scoped.scopes["Org1"].tags == ["a"]
    assert scoped.get_scope("clusters", "org1-cl") == "Org1"
    assert scoped.get_scope("clusters", "org1-nested") == "Org1"
    assert scoped.get_scope("connectors", "org1-conn") == "Org1"
    assert "org1-cl" in scoped.data["clusters"]


def test_non_scope_directory_loads_as_root(scoped: Config) -> None:
    assert "plain-cl" in scoped.data["clusters"]
    assert scoped.get_scope("clusters", "plain-cl") is None
    assert scoped.get_scope("clusters", "root-cl") is None


def test_scope_settings_do_not_touch_root_settings(scoped: Config) -> None:
    assert scoped.settings["users"]["clusters"]["user"] == "root-user"
    assert scoped.settings["monitoring"]["settings"]["default_thresholds"]["inodes"] == 80
    assert scoped.settings["consoleapi"]["general"]["org_id"] == "root-org"
    assert scoped.scope_settings["Org1"]["users"]["clusters"]["user"] == "org1-user"
    assert "scope" not in scoped.data["clusters"]["org1-cl"]


# --- scope.toml validation --------------------------------------------------


def test_marker_name_must_match_directory(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    with pytest.raises(ConfigurationError, match="must equal the directory name"):
        _load(tmp_path, monkeypatch, {"Org1/scope.toml": 'name = "Other"\n'})


def test_marker_without_name_is_valid(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    config = _load(tmp_path, monkeypatch, {"Org1/scope.toml": ""})
    assert config.scopes["Org1"].name is None


def test_marker_unknown_key_raises(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    with pytest.raises(ConfigurationError, match=r"Invalid .*scope\.toml"):
        _load(tmp_path, monkeypatch, {"Org1/scope.toml": 'colour = "red"\n'})


@pytest.mark.parametrize(
    "rel",
    ["scope.toml", "Org1/deeper/scope.toml", ".hidden/scope.toml", "apis/scope.toml"],
)
def test_marker_in_wrong_place_raises(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, rel: str
) -> None:
    with pytest.raises(ConfigurationError, match="only valid directly inside a top-level"):
        _load(tmp_path, monkeypatch, {"Org1/scope.toml": "", rel: ""})


def test_marker_nested_under_non_scope_directory_raises(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    with pytest.raises(ConfigurationError, match=r"nested/inner/scope\.toml"):
        _load(tmp_path, monkeypatch, {"nested/inner/scope.toml": ""})


@pytest.mark.parametrize("name", ["settings", "ontapapi", "aiqumapi", "diiapi"])
def test_disallowed_settings_file_in_scope_raises(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, name: str
) -> None:
    files = {"Org1/scope.toml": "", f"Org1/{name}.toml": "[general]\nx = 1\n"}
    with pytest.raises(ConfigurationError) as exc:
        _load(tmp_path, monkeypatch, files)
    message = str(exc.value)
    assert f"{name}.toml" in message
    assert "consoleapi.toml, monitoring.toml, users.toml" in message


def test_scoped_consoleapi_allows_only_general(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    files = {"Org1/scope.toml": "", "Org1/consoleapi.toml": '[general]\nbase_url = "x"\n[extra]\n'}
    with pytest.raises(ConfigurationError, match="only contain a \\[general\\] table"):
        _load(tmp_path, monkeypatch, files)


# --- duplicate names --------------------------------------------------------

_DUP = '[settings]\ntype = "data"\n\n[clusters.dup]\nip = "1.1.1.1"\n'


def test_duplicate_across_scopes_raises(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    files = {"A/scope.toml": "", "B/scope.toml": "", "A/d.toml": _DUP, "B/d.toml": _DUP}
    with pytest.raises(ConfigurationError, match="Duplicate clusters name 'dup'") as exc:
        _load(tmp_path, monkeypatch, files)
    assert "A" in str(exc.value)
    assert "B" in str(exc.value)


def test_duplicate_root_and_scope_raises_either_order(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    files = {"A/scope.toml": "", "A/d.toml": _DUP, "root.toml": _DUP}
    with pytest.raises(ConfigurationError, match="Duplicate clusters name 'dup'") as exc:
        _load(tmp_path, monkeypatch, files)
    assert "root.toml" in str(exc.value)
    assert "d.toml" in str(exc.value)


def test_duplicate_in_same_scope_raises(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    files = {"A/scope.toml": "", "A/one.toml": _DUP, "A/sub/two.toml": _DUP}
    with pytest.raises(ConfigurationError, match="Duplicate clusters name 'dup'"):
        _load(tmp_path, monkeypatch, files)


def test_duplicate_root_root_is_still_last_one_wins(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    files = {
        "one.toml": _DUP,
        "two.toml": _DUP.replace("1.1.1.1", "2.2.2.2"),
    }
    config = _load(tmp_path, monkeypatch, files)
    assert config.data["clusters"]["dup"]["ip"] in {"1.1.1.1", "2.2.2.2"}
    assert config.get_scope("clusters", "dup") is None


# --- get_user ---------------------------------------------------------------


def test_get_user_object_entry_wins(scoped: Config) -> None:
    assert scoped.get_user("clusters", "org1-cl") == ("own-user", "own-pass")


def test_get_user_scope_default_before_root(scoped: Config) -> None:
    assert scoped.get_user("clusters", "org1-cl2") == ("org1-user", "org1-pass")
    assert scoped.get_user("clusters", "org1-nested") == ("org1-user", "org1-pass")


def test_get_user_fields_fall_back_independently(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    files = {
        "A/scope.toml": "",
        "A/d.toml": '[settings]\ntype = "data"\n\n[clusters.c]\nip = "1"\nuser = "obj-user"\n',
        "A/users.toml": '[clusters]\nenc = "scope-pass"\n',
        "users.toml": '[clusters]\nuser = "root-user"\nenc = "root-pass"\n',
    }
    config = _load(tmp_path, monkeypatch, files)
    assert config.get_user("clusters", "c") == ("obj-user", "scope-pass")


def test_get_user_scope_falls_back_to_root_for_missing_field(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    files = {
        "A/scope.toml": "",
        "A/d.toml": '[settings]\ntype = "data"\n\n[clusters.c]\nip = "1"\n',
        "A/users.toml": '[clusters]\nuser = "scope-user"\n',
        "users.toml": '[clusters]\nuser = "root-user"\nenc = "root-pass"\n',
    }
    config = _load(tmp_path, monkeypatch, files)
    assert config.get_user("clusters", "c") == ("scope-user", "root-pass")


def test_get_user_env_vars_still_win(scoped: Config, monkeypatch: pytest.MonkeyPatch) -> None:
    assert scoped.get_user("clusters", "org1-cl2") == ("org1-user", "org1-pass")
    # the object name is org1-cl2 -> NF_ORG1_CL2_*
    monkeypatch.setenv("NF_ORG1_CL2_USER", "env-user")
    monkeypatch.setenv("NF_ORG1_CL2_PASSWORD", "env-pass")
    assert scoped.get_user("clusters", "org1-cl2") == ("env-user", "env-pass")


def test_root_object_never_sees_scope_defaults(scoped: Config) -> None:
    assert scoped.get_user("clusters", "root-cl") == ("root-user", "root-pass")


def test_explicit_scope_overrides_object_scope(scoped: Config) -> None:
    # root-cl has no entry of its own; the explicit scope supplies defaults
    assert scoped.get_user("clusters", "root-cl", scope="Org1") == ("org1-user", "org1-pass")


def test_get_user_unknown_scope_raises(scoped: Config) -> None:
    with pytest.raises(ConfigurationError, match="Unknown scope 'Nope'"):
        scoped.get_user("clusters", "root-cl", scope="Nope")


# --- get_secret and DII -----------------------------------------------------


def test_get_secret_follows_scope_order(scoped: Config) -> None:
    assert scoped.get_secret("cloudinsights", "org1-ci") == "org1-token"
    assert scoped.get_secret("cloudinsights", "root-ci") == "root-token"


def test_dii_settings_for_scoped_tenant_use_scope_token(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    extra = {
        "diiapi.toml": '[general]\nbase_url = "https://g.example.invalid"\n'
        'api_ro_token = "general-token"\nbase_api_path = "/rest/v1"\n'
    }
    config = _load(tmp_path, monkeypatch, ROOT_FILES, SCOPE_FILES, extra)
    token = config.get_dii_api_settings("org1-ci").api_ro_token
    assert token.get_secret_value() == "org1-token"


def test_scope_sops_error_names_scope_file_not_ciphertext(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    files = {
        "Org1/scope.toml": "",
        "Org1/d.toml": '[settings]\ntype = "data"\n\n[cloudinsights.t]\nip = "1"\n',
        "Org1/users.toml": f'[cloudinsights]\nenc = "{CIPHERTEXT}"\n',
    }
    config = _load(tmp_path, monkeypatch, files)
    with (
        patch("pynetappfoundry.utils.sops.decrypt_value", side_effect=SOPSError("boom")),
        pytest.raises(ConfigurationError) as exc,
    ):
        config.get_secret("cloudinsights", "t")
    assert "Org1/users.toml" in str(exc.value)
    assert CIPHERTEXT not in str(exc.value)


# --- get_setting / get_object_setting --------------------------------------


def test_get_setting_scope_wins(scoped: Config) -> None:
    got = scoped.get_setting("monitoring", "settings", "default_thresholds", "inodes", scope="Org1")
    assert got == 70


def test_get_setting_missing_in_scope_falls_back_to_root(scoped: Config) -> None:
    assert scoped.get_setting("monitoring", "settings", "root_only", scope="Org1") == 1
    got = scoped.get_setting("monitoring", "settings", "default_thresholds", "volume", scope="Org1")
    assert got == 90


def test_get_setting_unknown_scope_raises(scoped: Config) -> None:
    with pytest.raises(ConfigurationError, match=r"Unknown scope 'Nope'.*Org1"):
        scoped.get_setting("monitoring", scope="Nope")


def test_get_setting_without_scope_keeps_messages(scoped: Config) -> None:
    with pytest.raises(ConfigurationError, match=r"Missing configuration key 'nope'\. Available"):
        scoped.get_setting("nope")
    scoped.settings["a"] = {"b": 3}
    with pytest.raises(ConfigurationError, match=r"Cannot access 'x' in non-dict value at 'a\.b'"):
        scoped.get_setting("a", "b", "x")
    assert scoped.get_setting("nope", "x", default="d") == "d"


def test_get_object_setting_uses_object_scope(scoped: Config) -> None:
    keys = ("monitoring", "settings", "default_thresholds", "inodes")
    assert scoped.get_object_setting("clusters", "org1-cl", *keys) == 70
    assert scoped.get_object_setting("clusters", "root-cl", *keys) == 80
    assert scoped.get_object_setting("clusters", "org1-cl", "nope", default="d") == "d"


# --- Console settings -------------------------------------------------------


def test_console_scope_inherits_only_base_keys(scoped: Config) -> None:
    settings = scoped.get_console_api_settings(scope="Org1")
    assert settings.base_url == "https://api.org1.example.invalid"  # scope overrides
    assert settings.ui_base_url == "https://ui.root.example.invalid"
    assert settings.base_api_path == "/root"
    assert settings.timeout == 11.0
    assert settings.org_id == "org1-org"
    assert settings.agent_ids == ["org1-agent"]
    assert settings.service_token is not None
    assert settings.service_token.get_secret_value() == "org1-service-token"


def test_console_scope_never_uses_root_credentials_or_ids(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    files = {
        "Org1/scope.toml": "",
        "Org1/consoleapi.toml": '[general]\nuser_token = "org1-user-token"\n',
    }
    config = _load(tmp_path, monkeypatch, ROOT_FILES, files)
    settings = config.get_console_api_settings(scope="Org1")
    assert settings.base_url == "https://api.root.example.invalid"
    assert settings.org_id is None
    assert settings.agent_ids == []
    assert settings.service_token is None
    assert settings.refresh_token is None
    assert settings.user_token is not None


def test_console_scope_without_consoleapi_raises_and_never_falls_back(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    config = _load(tmp_path, monkeypatch, ROOT_FILES, {"Org1/scope.toml": ""})
    with pytest.raises(ConfigurationError, match="Scope 'Org1' has no Console account"):
        config.get_console_api_settings(scope="Org1")
    assert config.get_console_api_settings().org_id == "root-org"


def test_console_unknown_scope_raises(scoped: Config) -> None:
    with pytest.raises(ConfigurationError, match="Unknown scope"):
        scoped.get_console_api_settings(scope="Nope")


def test_console_scope_rejects_refresh_token_in_consoleapi(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    files = {
        "Org1/scope.toml": "",
        "Org1/consoleapi.toml": '[general]\nbase_url = "x"\nrefresh_token = "t"\n',
    }
    config = _load(tmp_path, monkeypatch, files)
    with pytest.raises(ConfigurationError, match=r"Org1/consoleapi\.toml must not contain"):
        config.get_console_api_settings(scope="Org1")


def test_console_scope_refresh_token_from_scope_users_only(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    files = {
        "Org1/scope.toml": "",
        "Org1/consoleapi.toml": '[general]\nbase_url = "https://a.example.invalid"\n',
        "Org1/users.toml": '[console]\nuser = "l"\nenc = "org1-refresh"\n',
    }
    config = _load(tmp_path, monkeypatch, ROOT_FILES, files)
    settings = config.get_console_api_settings(scope="Org1")
    assert settings.refresh_token is not None
    assert settings.refresh_token.get_secret_value() == "org1-refresh"
    # root account is unchanged and keeps its own token
    root = config.get_console_api_settings()
    assert root.refresh_token is not None
    assert root.refresh_token.get_secret_value() == "root-refresh"


def test_console_scope_has_no_root_refresh_token_fallback(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    files = {
        "Org1/scope.toml": "",
        "Org1/consoleapi.toml": '[general]\nuser_token = "t"\n',
    }
    config = _load(tmp_path, monkeypatch, ROOT_FILES, files)
    # the root users.toml has [console]; the scope must not read it (it would also
    # clash with user_token as mutually exclusive)
    assert config.get_console_api_settings(scope="Org1").refresh_token is None


def test_console_scope_ignores_nf_console_env(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("NF_CONSOLE_PASSWORD", "env-refresh")
    monkeypatch.setenv("NF_CONSOLE_USER", "env-user")
    files = {
        "Org1/scope.toml": "",
        "Org1/consoleapi.toml": '[general]\nbase_url = "https://a.example.invalid"\n'
        'user_token = "t"\n',
    }
    config = _load(tmp_path, monkeypatch, ROOT_FILES, files)
    assert config.get_console_api_settings(scope="Org1").refresh_token is None


def test_console_scope_refresh_token_is_decrypted_once(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    files = {
        "Org1/scope.toml": "",
        "Org1/consoleapi.toml": '[general]\nbase_url = "https://a.example.invalid"\n',
        "Org1/users.toml": f'[console]\nuser = "l"\nenc = "{CIPHERTEXT}"\n',
    }
    config = _load(tmp_path, monkeypatch, files)
    decrypt = MagicMock(return_value="plain-refresh")
    with patch("pynetappfoundry.utils.sops.decrypt_value", decrypt):
        first = config.get_console_api_settings(scope="Org1")
        second = config.get_console_api_settings(scope="Org1")
    assert decrypt.call_count == 1
    assert first.refresh_token is not None
    assert second.refresh_token is not None
    assert second.refresh_token.get_secret_value() == "plain-refresh"


def test_console_scope_incomplete_users_console_raises(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    files = {
        "Org1/scope.toml": "",
        "Org1/consoleapi.toml": '[general]\nbase_url = "https://a.example.invalid"\n',
        "Org1/users.toml": '[console]\nuser = "l"\n',
    }
    config = _load(tmp_path, monkeypatch, files)
    with pytest.raises(ConfigurationError, match=r"Org1/users\.toml"):
        config.get_console_api_settings(scope="Org1")


def test_console_scope_none_is_unchanged(scoped: Config) -> None:
    settings = scoped.get_console_api_settings()
    assert settings.org_id == "root-org"
    assert settings.refresh_token is not None
    assert settings.refresh_token.get_secret_value() == "root-refresh"


@pytest.fixture(autouse=True)
def _no_real_sops() -> Iterator[None]:
    with patch(
        "pynetappfoundry.utils.sops.decrypt_value",
        side_effect=AssertionError("unexpected SOPS decrypt"),
    ):
        yield
