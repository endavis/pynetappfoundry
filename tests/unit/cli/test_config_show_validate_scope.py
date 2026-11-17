"""Tests for ``nf config show --scope`` and ``nf config validate --scope`` (#1081)."""

from __future__ import annotations

from pathlib import Path

import pytest
from click.testing import CliRunner

from pynetappfoundry.cli.main import nf

SECRET_ENC = "placeholder-enc-value"

FILES = {
    "root.toml": '[settings]\ntype = "data"\n\n[clusters.root-cl]\nip = "10.0.0.1"\n',
    "users.toml": f'[clusters]\nuser = "root-user"\nenc = "{SECRET_ENC}-root"\n',
    "Org1/scope.toml": 'description = "Org one scope"\ntags = ["example"]\n',
    "Org1/inv.toml": (
        '[settings]\ntype = "data"\n\n'
        '[clusters.org1-cl]\nip = "10.1.0.1"\nuser = "own"\n'
        'enc = "own-pw"\n'
    ),
    "Org1/users.toml": f'[clusters]\nuser = "org1-user"\nenc = "{SECRET_ENC}-org1"\n',
    "Org1/monitoring.toml": "[settings]\ndefault_thresholds = {inodes = 71}\n",
    "Org1/consoleapi.toml": (
        '[general]\nbase_url = "https://api.org1.example.invalid"\n'
        'service_token = "placeholder-service-token"\norg_id = "org1-org"\n'
    ),
    "Org2/scope.toml": "",
    "Org2/inv.toml": '[settings]\ntype = "data"\n\n[clusters.org2-cl]\nip = "10.2.0.1"\n',
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
    for name in ("NF_ORG1_CL_USER", "NF_ORG2_CL_USER", "NF_ROOT_CL_USER"):
        monkeypatch.delenv(name, raising=False)


def _config_dir(tmp_path: Path, **overrides: str | None) -> Path:
    config_dir = tmp_path / "cfg"
    files = {**FILES}
    for rel, content in overrides.items():
        key = rel.replace("__", "/").replace("_toml", ".toml")
        if content is None:
            files.pop(key, None)
        else:
            files[key] = content
    for rel, content in files.items():
        path = config_dir / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
    return config_dir


def _run(config_dir: Path, *args: str) -> tuple[int, str]:
    result = CliRunner().invoke(nf, ["--config-dir", str(config_dir), "config", *args])
    return result.exit_code, " ".join(result.output.split())


# --- show --------------------------------------------------------------------


def test_show_scope_shows_only_the_scopes_own_files(tmp_path: Path) -> None:
    code, out = _run(_config_dir(tmp_path), "show", "--scope", "Org1")

    assert code == 0, out
    assert "org1-cl" in out
    assert "root-cl" not in out
    assert "org2-cl" not in out
    assert "fall back to the root" in out
    assert "Org one scope" in out
    assert "example" in out
    assert "inodes" in out
    assert "71" in out


def test_show_scope_masks_enc_unless_unmasked(tmp_path: Path) -> None:
    config_dir = _config_dir(tmp_path)

    _, masked = _run(config_dir, "show", "--scope", "Org1")
    _, unmasked = _run(config_dir, "show", "--scope", "Org1", "--unmask")

    assert SECRET_ENC not in masked
    assert "own-pw" not in masked
    assert "********" in masked
    assert "own-pw" in unmasked


def test_show_scope_section_users(tmp_path: Path) -> None:
    code, out = _run(_config_dir(tmp_path), "show", "--scope", "Org1", "-s", "users")

    assert code == 0, out
    assert "org1-user" in out
    assert SECRET_ENC not in out
    assert "org1-cl" not in out


def test_show_scope_section_settings_lists_the_scopes_sections(tmp_path: Path) -> None:
    code, out = _run(_config_dir(tmp_path), "show", "--scope", "Org1", "-s", "settings")

    assert code == 1
    assert "not found in scope 'Org1'" in out
    assert "clusters" in out
    assert "users" in out
    assert "monitoring" in out


def test_show_unknown_scope_exits_1(tmp_path: Path) -> None:
    code, out = _run(_config_dir(tmp_path), "show", "--scope", "Nope")

    assert code == 1
    assert "Unknown scope" in out
    assert "Org1" in out


def test_show_without_scope_lists_scopes_in_summary(tmp_path: Path) -> None:
    code, out = _run(_config_dir(tmp_path), "show")

    assert code == 0, out
    assert "Scopes: Org1, Org2" in out


def test_show_without_scopes_has_no_scopes_line(tmp_path: Path) -> None:
    config_dir = _config_dir(
        tmp_path,
        Org1__scope_toml=None,
    )
    for rel in FILES:
        if rel.startswith(("Org1/", "Org2/")):
            (config_dir / rel).unlink(missing_ok=True)

    code, out = _run(config_dir, "show")

    assert code == 0, out
    assert "Scopes:" not in out


# --- validate ----------------------------------------------------------------


def test_validate_scope_valid_lists_only_its_clusters(tmp_path: Path) -> None:
    code, out = _run(_config_dir(tmp_path), "validate", "--scope", "Org1")

    assert code == 0, out
    assert "org1-cl" in out
    assert "root-cl" not in out
    assert "org2-cl" not in out
    assert "Monitoring" in out
    assert "Console" in out
    assert "Console: Invalid" not in out
    assert "Not configured" not in out
    assert "Configuration is valid" in out


def test_validate_scope_invalid_users_section_is_keyed_by_scope(tmp_path: Path) -> None:
    config_dir = _config_dir(tmp_path, Org1__users_toml='[clusters]\nuser = "org1-user"\n')

    code, out = _run(config_dir, "validate", "--scope", "Org1")

    assert code == 1
    assert "Org1/users.clusters.enc" in out


def test_validate_scope_without_console_account_is_optional(tmp_path: Path) -> None:
    config_dir = _config_dir(tmp_path, Org1__consoleapi_toml=None)

    code, out = _run(config_dir, "validate", "--scope", "Org1")

    assert code == 0, out
    assert "Console: Not configured (optional)" in out


def test_validate_scope_invalid_consoleapi_exits_1(tmp_path: Path) -> None:
    config_dir = _config_dir(
        tmp_path,
        Org1__consoleapi_toml='[general]\nservice_token = "x"\nrefresh_token = "not-allowed"\n',
    )

    code, out = _run(config_dir, "validate", "--scope", "Org1")

    assert code == 1
    assert "Org1/consoleapi.general" in out


def test_validate_scope_without_monitoring_is_optional(tmp_path: Path) -> None:
    config_dir = _config_dir(tmp_path, Org1__monitoring_toml=None)

    code, out = _run(config_dir, "validate", "--scope", "Org1")

    assert code == 0, out
    assert "Monitoring: Not configured (optional)" in out


def test_validate_unknown_scope_exits_1(tmp_path: Path) -> None:
    code, out = _run(_config_dir(tmp_path), "validate", "--scope", "Nope")

    assert code == 1
    assert "Unknown scope" in out


def test_validate_without_scope_is_unchanged(tmp_path: Path) -> None:
    code, out = _run(_config_dir(tmp_path), "validate")

    assert code == 0, out
    assert "root-cl" in out
    assert "org1-cl" in out
    assert "Scope settings" not in out
