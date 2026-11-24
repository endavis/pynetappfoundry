"""Tests for ``nf config set-credential --setting`` (#1089)."""

from __future__ import annotations

import logging
import re
import tomllib
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import pytest
from click.testing import CliRunner, Result

from pynetappfoundry.cli.main import nf
from pynetappfoundry.core.config import (
    _CONSOLE_SOPS_FIELDS,
    _DIGITAL_ADVISOR_SOPS_FIELDS,
    _DII_SOPS_FIELDS,
    _SMTP_SOPS_FIELDS,
    SOPS_SETTING_TARGETS,
    Config,
)
from pynetappfoundry.utils.sops import SOPSError

MODULE = "pynetappfoundry.cli.commands.config.credentials"
DECRYPT = "pynetappfoundry.utils.sops.decrypt_value"
PLAIN = "PLAIN-placeholder"
CIPHERTEXT = "SOPS[placeholder-ciphertext]"

ROOT_DATA = '[settings]\ntype = "data"\n\n[clusters.root-cl]\nip = "10.0.0.1"\n'
CONSOLE_BODY = '[general]\nbase_url = "https://api.example.invalid"\n'
CONSOLE_WITH_ID = CONSOLE_BODY + 'client_id = "placeholder-id"\norg_id = "org-placeholder"\n'
SMTP_BODY = '[SMTP]\nserver = "smtp.example.invalid"\nuser = "mailer"\n'

# target -> (relative path of the existing file, its content, table, key)
CASES = {
    "consoleapi.client_secret": ("apis/console/consoleapi.toml", CONSOLE_BODY, "general"),
    "consoleapi.service_token": ("apis/console/consoleapi.toml", CONSOLE_BODY, "general"),
    "consoleapi.user_token": ("apis/console/consoleapi.toml", CONSOLE_BODY, "general"),
    "diiapi.api_ro_token": (
        "apis/dii/diiapi.toml",
        '[general]\nbase_url = "https://dii.example.invalid"\n',
        "general",
    ),
    "diiapi.api_rw_token": (
        "apis/dii/diiapi.toml",
        '[general]\nbase_url = "https://dii.example.invalid"\n',
        "general",
    ),
    "settings.smtp_password": ("settings.toml", SMTP_BODY, "SMTP"),
}


@pytest.fixture(autouse=True)
def _clean_env(monkeypatch: pytest.MonkeyPatch) -> None:
    for key in (
        "NF_CONSOLE_USER",
        "NF_CONSOLE_PASSWORD",
        "NF_CONSOLE_CLIENT_ID",
        "NF_CONSOLE_CLIENT_SECRET",
        "NF_CONSOLE_SERVICE_TOKEN",
        "NF_CONSOLE_USER_TOKEN",
        "NF_CONSOLE_BASE_URL",
    ):
        monkeypatch.delenv(key, raising=False)


def _write(config_dir: Path, files: dict[str, str]) -> Path:
    for rel, content in files.items():
        path = config_dir / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
    return config_dir


def _config_dir(tmp_path: Path, files: dict[str, str] | None = None) -> Path:
    base = {"root.toml": ROOT_DATA, "Org1/scope.toml": "", "Org2/scope.toml": ""}
    return _write(tmp_path / "cfg", {**base, **(files or {})})


@contextmanager
def _sops(installed: bool = True, encrypt_error: Exception | None = None) -> Iterator[MagicMock]:
    with (
        patch(f"{MODULE}.is_sops_installed", return_value=installed),
        patch(f"{MODULE}.get_age_key_path") as key_path,
        patch(f"{MODULE}.get_public_key_from_file", return_value="age1placeholderkey"),
        patch(f"{MODULE}.encrypt_value", return_value=CIPHERTEXT, side_effect=encrypt_error) as enc,
    ):
        key_path.return_value.exists.return_value = True
        yield enc


def _invoke(
    config_dir: Path,
    *args: str,
    installed: bool = True,
    encrypt_error: Exception | None = None,
    value_input: str | None = None,
) -> tuple[Result, MagicMock]:
    value = f"{PLAIN}\n{PLAIN}\n" if value_input is None else value_input
    with _sops(installed, encrypt_error) as encrypt:
        result = CliRunner().invoke(
            nf,
            ["--config-dir", str(config_dir), "config", "set-credential", *args],
            input=value,
        )
    return result, encrypt


def _flat(result: Result) -> str:
    return " ".join(result.output.split())


def _snapshot(config_dir: Path) -> dict[str, str]:
    return {str(p.relative_to(config_dir)): p.read_text() for p in config_dir.rglob("*.toml")}


def _load(path: Path) -> dict[str, Any]:
    return tomllib.loads(path.read_text(encoding="utf-8"))


@pytest.mark.parametrize("target", sorted(CASES))
def test_target_writes_encrypted_value_into_existing_file(tmp_path: Path, target: str) -> None:
    rel, content, table = CASES[target]
    config_dir = _config_dir(tmp_path, {rel: content})
    before = set(_snapshot(config_dir))

    result, encrypt = _invoke(config_dir, "--setting", target)

    assert result.exit_code == 0, result.output
    key = target.split(".", 1)[1].removeprefix("smtp_")
    assert _load(config_dir / rel)[table][key] == CIPHERTEXT
    encrypt.assert_called_once_with(PLAIN, "age1placeholderkey")
    assert set(_snapshot(config_dir)) == before
    assert PLAIN not in result.output
    assert "(encrypted)" in result.output


def test_scope_writes_scope_file_and_leaves_root_untouched(tmp_path: Path) -> None:
    config_dir = _config_dir(
        tmp_path,
        {"apis/console/consoleapi.toml": CONSOLE_BODY, "Org1/consoleapi.toml": CONSOLE_WITH_ID},
    )
    root_before = (config_dir / "apis/console/consoleapi.toml").read_bytes()

    result, _ = _invoke(config_dir, "--setting", "consoleapi.client_secret", "--scope", "Org1")

    assert result.exit_code == 0, result.output
    assert _load(config_dir / "Org1/consoleapi.toml")["general"]["client_secret"] == CIPHERTEXT
    assert (config_dir / "apis/console/consoleapi.toml").read_bytes() == root_before
    assert "client_id" not in _flat(result)


def test_missing_scope_file_is_created_with_a_warning(tmp_path: Path) -> None:
    config_dir = _config_dir(tmp_path)

    result, _ = _invoke(config_dir, "--setting", "consoleapi.client_secret", "--scope", "Org1")

    assert result.exit_code == 0, result.output
    assert _load(config_dir / "Org1/consoleapi.toml") == {"general": {"client_secret": CIPHERTEXT}}
    out = _flat(result)
    assert "client_id" in out
    assert "org_id" in out


def test_missing_table_is_appended(tmp_path: Path) -> None:
    config_dir = _config_dir(tmp_path, {"settings.toml": '[licensing]\nmailfrom = "a@b.invalid"\n'})

    result, _ = _invoke(config_dir, "--setting", "settings.smtp_password")

    assert result.exit_code == 0, result.output
    data = _load(config_dir / "settings.toml")
    assert data["SMTP"] == {"password": CIPHERTEXT}
    assert data["licensing"] == {"mailfrom": "a@b.invalid"}


def test_unknown_target_is_a_click_choice_error(tmp_path: Path) -> None:
    config_dir = _config_dir(tmp_path)
    before = _snapshot(config_dir)

    result, encrypt = _invoke(config_dir, "--setting", "ontapapi.password")

    assert result.exit_code == 2
    encrypt.assert_not_called()
    assert _snapshot(config_dir) == before


@pytest.mark.parametrize("target", ["diiapi.api_ro_token", "settings.smtp_password"])
def test_scope_is_rejected_for_non_scope_files(tmp_path: Path, target: str) -> None:
    config_dir = _config_dir(tmp_path)
    before = _snapshot(config_dir)

    result, encrypt = _invoke(config_dir, "--setting", target, "--scope", "Org1")

    assert result.exit_code == 1
    out = _flat(result)
    assert "consoleapi.toml" in out
    assert "monitoring.toml" in out
    assert "Value" not in out
    encrypt.assert_not_called()
    assert _snapshot(config_dir) == before


def test_unknown_scope_is_rejected(tmp_path: Path) -> None:
    config_dir = _config_dir(tmp_path)
    before = _snapshot(config_dir)

    result, encrypt = _invoke(config_dir, "--setting", "consoleapi.client_secret", "--scope", "No")

    assert result.exit_code == 1
    assert "Unknown scope" in _flat(result)
    encrypt.assert_not_called()
    assert _snapshot(config_dir) == before


@pytest.mark.parametrize(
    "extra",
    [
        ["--cluster", "root-cl"],
        ["--type", "clusters"],
        ["--name", "x"],
        ["--user", "someone"],
        ["--no-encrypt"],
        ["--read-write"],
    ],
)
def test_conflicting_options_are_rejected(tmp_path: Path, extra: list[str]) -> None:
    config_dir = _config_dir(tmp_path)
    before = _snapshot(config_dir)

    result, encrypt = _invoke(
        config_dir, "--setting", "consoleapi.client_secret", *extra, value_input=""
    )

    assert result.exit_code == 1
    out = _flat(result)
    assert "--setting cannot be combined with" in out
    assert extra[0] in out
    assert "Value" not in out
    encrypt.assert_not_called()
    assert _snapshot(config_dir) == before


def test_password_option_supplies_the_value(tmp_path: Path) -> None:
    config_dir = _config_dir(tmp_path, {"consoleapi.toml": CONSOLE_BODY})

    result, encrypt = _invoke(
        config_dir, "--setting", "consoleapi.service_token", "--password", PLAIN, value_input=""
    )

    assert result.exit_code == 0, result.output
    encrypt.assert_called_once_with(PLAIN, "age1placeholderkey")


def test_missing_sops_errors_without_plaintext_fallback(tmp_path: Path) -> None:
    config_dir = _config_dir(tmp_path, {"consoleapi.toml": CONSOLE_BODY})
    before = _snapshot(config_dir)

    result, _ = _invoke(config_dir, "--setting", "consoleapi.client_secret", installed=False)

    assert result.exit_code == 1
    assert "nf config init-sops" in _flat(result)
    assert _snapshot(config_dir) == before
    assert PLAIN not in result.output


def test_sops_error_is_reported_as_encryption_failed(tmp_path: Path) -> None:
    config_dir = _config_dir(tmp_path, {"consoleapi.toml": CONSOLE_BODY})
    before = _snapshot(config_dir)

    result, _ = _invoke(
        config_dir,
        "--setting",
        "consoleapi.client_secret",
        encrypt_error=SOPSError("sops exploded"),
    )

    assert result.exit_code == 1
    assert "Encryption failed" in _flat(result)
    assert _snapshot(config_dir) == before


def test_two_files_with_the_stem_are_refused(tmp_path: Path) -> None:
    config_dir = _config_dir(
        tmp_path, {"a/consoleapi.toml": CONSOLE_BODY, "b/consoleapi.toml": CONSOLE_BODY}
    )
    before = _snapshot(config_dir)

    result, encrypt = _invoke(config_dir, "--setting", "consoleapi.client_secret")

    assert result.exit_code == 1
    squashed = "".join(result.output.split())
    assert re.search(r"[\\/]a[\\/]consoleapi\.toml", squashed)
    assert re.search(r"[\\/]b[\\/]consoleapi\.toml", squashed)
    assert "Value" not in _flat(result)
    encrypt.assert_not_called()
    assert _snapshot(config_dir) == before


def test_comments_and_unrelated_keys_are_kept(tmp_path: Path) -> None:
    original = (
        "# top comment\n"
        "[SMTP]\n"
        "# server comment\n"
        'server = "smtp.example.invalid"  # inline comment\n'
        'password = "old-placeholder"  # old password\n'
        "port = 25\n"
    )
    config_dir = _config_dir(tmp_path, {"settings.toml": original})

    result, _ = _invoke(config_dir, "--setting", "settings.smtp_password")

    assert result.exit_code == 0, result.output
    text = (config_dir / "settings.toml").read_text()
    for kept in ("# top comment", "# server comment", "# inline comment", "port = 25"):
        assert kept in text
    assert text.count("password =") == 1
    assert _load(config_dir / "settings.toml")["SMTP"]["password"] == CIPHERTEXT


def test_new_key_is_appended_after_existing_keys(tmp_path: Path) -> None:
    config_dir = _config_dir(
        tmp_path, {"consoleapi.toml": CONSOLE_BODY + "# trailing comment\ntimeout = 5\n"}
    )

    result, _ = _invoke(config_dir, "--setting", "consoleapi.service_token")

    assert result.exit_code == 0, result.output
    text = (config_dir / "consoleapi.toml").read_text()
    assert "# trailing comment" in text
    assert _load(config_dir / "consoleapi.toml")["general"]["timeout"] == 5


def test_client_secret_without_client_id_warns(tmp_path: Path) -> None:
    config_dir = _config_dir(tmp_path, {"consoleapi.toml": CONSOLE_BODY})

    result, _ = _invoke(config_dir, "--setting", "consoleapi.client_secret")

    assert result.exit_code == 0, result.output
    assert "no client_id" in _flat(result)


def test_client_secret_with_client_id_does_not_warn(tmp_path: Path) -> None:
    config_dir = _config_dir(tmp_path, {"consoleapi.toml": CONSOLE_WITH_ID})

    result, _ = _invoke(config_dir, "--setting", "consoleapi.client_secret")

    assert result.exit_code == 0, result.output
    assert "no client_id" not in _flat(result)


def test_smtp_password_without_user_warns(tmp_path: Path) -> None:
    config_dir = _config_dir(tmp_path, {"settings.toml": '[SMTP]\nserver = "smtp.invalid"\n'})

    result, _ = _invoke(config_dir, "--setting", "settings.smtp_password")

    assert result.exit_code == 0, result.output
    assert "no user" in _flat(result)


def test_smtp_password_with_user_does_not_warn(tmp_path: Path) -> None:
    config_dir = _config_dir(tmp_path, {"settings.toml": SMTP_BODY})

    result, _ = _invoke(config_dir, "--setting", "settings.smtp_password")

    assert result.exit_code == 0, result.output
    assert "no user" not in _flat(result)


def test_stored_values_load_back_through_config(tmp_path: Path) -> None:
    config_dir = _config_dir(
        tmp_path,
        {
            "consoleapi.toml": CONSOLE_BODY,
            "Org1/consoleapi.toml": CONSOLE_WITH_ID,
            "diiapi.toml": '[general]\nbase_url = "https://dii.example.invalid"\n',
            "settings.toml": SMTP_BODY,
        },
    )
    for args in (
        ("--setting", "consoleapi.client_secret", "--scope", "Org1"),
        ("--setting", "consoleapi.service_token"),
        ("--setting", "diiapi.api_ro_token"),
        ("--setting", "settings.smtp_password"),
    ):
        result, _ = _invoke(config_dir, *args)
        assert result.exit_code == 0, result.output

    config = Config(config_dir=str(config_dir), script_name="test")
    with patch(DECRYPT, return_value=PLAIN):
        scoped = config.get_console_api_settings(scope="Org1")
        root = config.get_console_api_settings()
        dii = config.get_dii_api_settings()
        smtp = config.get_smtp_settings()

    assert scoped.client_secret is not None
    assert scoped.client_secret.get_secret_value() == PLAIN
    assert root.service_token is not None
    assert root.service_token.get_secret_value() == PLAIN
    assert dii.api_ro_token is not None
    assert dii.api_ro_token.get_secret_value() == PLAIN
    assert smtp.password.get_secret_value() == PLAIN


def _tree_text(config_dir: Path) -> str:
    return "\n".join(_snapshot(config_dir).values())


def test_plaintext_never_leaks_on_success(tmp_path: Path, caplog: pytest.LogCaptureFixture) -> None:
    config_dir = _config_dir(tmp_path, {"consoleapi.toml": CONSOLE_BODY})

    with caplog.at_level(logging.DEBUG):
        result, _ = _invoke(config_dir, "--setting", "consoleapi.client_secret")

    assert result.exit_code == 0, result.output
    assert PLAIN not in result.output
    assert PLAIN not in caplog.text
    assert PLAIN not in _tree_text(config_dir)


def test_plaintext_never_leaks_on_failure(tmp_path: Path, caplog: pytest.LogCaptureFixture) -> None:
    config_dir = _config_dir(tmp_path, {"consoleapi.toml": CONSOLE_BODY})

    with caplog.at_level(logging.DEBUG):
        result, _ = _invoke(
            config_dir, "--setting", "consoleapi.client_secret", encrypt_error=SOPSError("boom")
        )

    assert result.exit_code == 1
    assert PLAIN not in result.output
    assert PLAIN not in caplog.text
    assert PLAIN not in _tree_text(config_dir)


def test_targets_cover_exactly_the_fields_the_loader_decrypts() -> None:
    expected = (
        {("settings", "SMTP", f) for f in _SMTP_SOPS_FIELDS}
        | {("diiapi", "general", f) for f in _DII_SOPS_FIELDS}
        | {("consoleapi", "general", f) for f in _CONSOLE_SOPS_FIELDS}
        | {("digitaladvisorapi", "general", f) for f in _DIGITAL_ADVISOR_SOPS_FIELDS}
    )
    assert set(SOPS_SETTING_TARGETS.values()) == expected
    assert len(SOPS_SETTING_TARGETS) == len(expected)


def test_type_console_names_refresh_token_and_points_to_setting(tmp_path: Path) -> None:
    config_dir = _config_dir(tmp_path)

    result, _ = _invoke(
        config_dir, "--type", "console", "--scope", "Org1", "--user", "label", "--no-encrypt"
    )

    assert result.exit_code == 0, result.output
    out = _flat(result)
    assert "Refresh token stored" in out
    assert "--setting consoleapi.client_secret --scope Org1" in out


def test_help_explains_refresh_token_versus_client_secret() -> None:
    result = CliRunner().invoke(nf, ["config", "set-credential", "--help"])

    out = " ".join(result.output.split())
    assert result.exit_code == 0
    assert "refresh token" in out
    assert "--setting consoleapi.client_secret" in out


def test_type_writer_keeps_users_toml_comments(tmp_path: Path) -> None:
    config_dir = _config_dir(
        tmp_path, {"users.toml": '# keep me\n[clusters]\nuser = "old"  # old user\nenc = "x"\n'}
    )

    result, _ = _invoke(
        config_dir, "--type", "clusters", "--user", "new", "--password", PLAIN, "--no-encrypt"
    )

    assert result.exit_code == 0, result.output
    text = (config_dir / "users.toml").read_text()
    assert "# keep me" in text
    assert "# old user" in text
    assert _load(config_dir / "users.toml")["clusters"]["user"] == "new"


def test_object_writer_keeps_data_file_comments(tmp_path: Path) -> None:
    data = (
        '# inventory\n[settings]\ntype = "data"\n\n'
        '[aiqums.a1]\n# address\nip = "10.0.0.5"  # primary\n'
    )
    config_dir = _config_dir(tmp_path, {"data/aiqums.toml": data})

    result, _ = _invoke(
        config_dir,
        "--type",
        "aiqums",
        "--name",
        "a1",
        "--user",
        "admin",
        "--password",
        PLAIN,
        "--no-encrypt",
    )

    assert result.exit_code == 0, result.output
    text = (config_dir / "data/aiqums.toml").read_text()
    for kept in ("# inventory", "# address", "# primary"):
        assert kept in text
    assert _load(config_dir / "data/aiqums.toml")["aiqums"]["a1"]["user"] == "admin"


def test_object_writer_keeps_inline_tables(tmp_path: Path) -> None:
    data = '[settings]\ntype = "data"\n\n[aiqums]\na1 = {ip = "10.0.0.5"}\n'
    config_dir = _config_dir(tmp_path, {"data/aiqums.toml": data})

    result, _ = _invoke(
        config_dir,
        "--type",
        "aiqums",
        "--name",
        "a1",
        "--user",
        "admin",
        "--password",
        PLAIN,
        "--no-encrypt",
    )

    assert result.exit_code == 0, result.output
    parsed = _load(config_dir / "data/aiqums.toml")["aiqums"]["a1"]
    assert parsed == {"ip": "10.0.0.5", "user": "admin", "enc": PLAIN}


def test_missing_user_for_type_mode_is_a_usage_error(tmp_path: Path) -> None:
    config_dir = _config_dir(tmp_path)

    result, _ = _invoke(config_dir, "--type", "clusters", value_input="")

    assert result.exit_code == 2
    assert "--user" in result.output


def test_encrypt_value_command_is_removed(tmp_path: Path) -> None:
    result = CliRunner().invoke(nf, ["config", "encrypt-value"])

    assert result.exit_code == 2
    assert "No such command" in result.output


@pytest.mark.parametrize(
    ("stem", "name"),
    [
        ("ontapapi", "ontap"),
        ("aiqumapi", "aiqum"),
        ("diiapi", "dii"),
        ("consoleapi", "console"),
        ("digitaladvisorapi", "digitaladvisor"),
    ],
)
def test_missing_root_api_file_defaults_to_apis_dir(tmp_path: Path, stem: str, name: str) -> None:
    from pynetappfoundry.cli.commands.config.credentials import _find_setting_file

    config_dir = _config_dir(tmp_path)

    found = _find_setting_file(config_dir, stem, None)

    assert found == config_dir / "apis" / name / f"{stem}.toml"


def test_missing_root_api_file_is_created_in_apis_dir(tmp_path: Path) -> None:
    config_dir = _config_dir(tmp_path)
    assert not (config_dir / "apis").exists()

    result, _ = _invoke(config_dir, "--setting", "consoleapi.client_secret")

    assert result.exit_code == 0, result.output
    created = config_dir / "apis/console/consoleapi.toml"
    assert _load(created) == {"general": {"client_secret": CIPHERTEXT}}
    assert not (config_dir / "consoleapi.toml").exists()


def test_missing_dii_file_is_created_in_apis_dir(tmp_path: Path) -> None:
    config_dir = _config_dir(tmp_path)

    result, _ = _invoke(config_dir, "--setting", "diiapi.api_ro_token")

    assert result.exit_code == 0, result.output
    assert _load(config_dir / "apis/dii/diiapi.toml")["general"]["api_ro_token"] == CIPHERTEXT
    assert not (config_dir / "diiapi.toml").exists()


def test_existing_top_level_api_file_is_still_the_one_written(tmp_path: Path) -> None:
    config_dir = _config_dir(tmp_path, {"consoleapi.toml": CONSOLE_BODY})

    result, _ = _invoke(config_dir, "--setting", "consoleapi.client_secret")

    assert result.exit_code == 0, result.output
    assert _load(config_dir / "consoleapi.toml")["general"]["client_secret"] == CIPHERTEXT
    assert not (config_dir / "apis").exists()


def test_missing_scope_api_file_stays_in_scope_dir(tmp_path: Path) -> None:
    config_dir = _config_dir(tmp_path)

    result, _ = _invoke(config_dir, "--setting", "consoleapi.client_secret", "--scope", "Org1")

    assert result.exit_code == 0, result.output
    assert (config_dir / "Org1/consoleapi.toml").is_file()
    assert not (config_dir / "apis").exists()


def test_missing_non_api_file_is_created_at_top_level(tmp_path: Path) -> None:
    config_dir = _config_dir(tmp_path)

    result, _ = _invoke(config_dir, "--setting", "settings.smtp_password")

    assert result.exit_code == 0, result.output
    assert _load(config_dir / "settings.toml")["SMTP"]["password"] == CIPHERTEXT
    assert not (config_dir / "apis").exists()


def test_read_write_encrypts_the_tenant_key(tmp_path: Path) -> None:
    config_dir = _config_dir(
        tmp_path,
        {"root.toml": ROOT_DATA + '\n[cloudinsights.t1]\nbase_url = "https://t1.invalid"\n'},
    )

    result, encrypt = _invoke(config_dir, "--type", "cloudinsights", "--name", "t1", "--read-write")

    assert result.exit_code == 0, result.output
    encrypt.assert_called_once()
    assert encrypt.call_args.args[0] == PLAIN
    tenant = _load(config_dir / "root.toml")["cloudinsights"]["t1"]
    assert tenant["rw_enc"] == CIPHERTEXT
    assert PLAIN not in result.output
    assert CIPHERTEXT not in result.output
