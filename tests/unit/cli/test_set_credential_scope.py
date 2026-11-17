"""Tests for ``nf config set-credential --scope`` (#1081)."""

from __future__ import annotations

import tomllib
from pathlib import Path

import pytest
from click.testing import CliRunner

from pynetappfoundry.cli.main import nf
from pynetappfoundry.core.config import Config

SECRET = "placeholder-secret"

ROOT_DATA = """\
[settings]
type = "data"

[clusters.root-cl]
ip = "10.0.0.1"
"""

SCOPE_DATA = """\
[settings]
type = "data"

[clusters.org1-cl]
ip = "10.1.0.1"

[aiqums.org1-aiqum]
ip = "10.1.0.2"
"""

CONSOLE_GENERAL = '[general]\nbase_url = "https://api.org1.example.invalid"\nservice_token = "x"\n'


@pytest.fixture(autouse=True)
def _clean_env(monkeypatch: pytest.MonkeyPatch) -> None:
    for key in ("NF_CONSOLE_USER", "NF_CONSOLE_PASSWORD"):
        monkeypatch.delenv(key, raising=False)


def _config_dir(tmp_path: Path, *, console_account: bool = False) -> Path:
    config_dir = tmp_path / "cfg"
    (config_dir / "Org1").mkdir(parents=True)
    (config_dir / "Org2").mkdir()
    (config_dir / "root.toml").write_text(ROOT_DATA)
    (config_dir / "Org1" / "scope.toml").write_text("")
    (config_dir / "Org2" / "scope.toml").write_text("")
    (config_dir / "Org1" / "inv.toml").write_text(SCOPE_DATA)
    if console_account:
        (config_dir / "Org1" / "consoleapi.toml").write_text(CONSOLE_GENERAL)
    return config_dir


def _invoke(config_dir: Path, *args: str) -> tuple[int, str]:
    result = CliRunner().invoke(
        nf,
        ["--config-dir", str(config_dir), "config", "set-credential", *args, "--no-encrypt"],
        input=f"{SECRET}\n{SECRET}\n",
    )
    return result.exit_code, result.output


def _snapshot(config_dir: Path) -> dict[str, str]:
    return {str(p.relative_to(config_dir)): p.read_text() for p in config_dir.rglob("*.toml")}


def test_type_scope_writes_scope_users_toml_only(tmp_path: Path) -> None:
    config_dir = _config_dir(tmp_path)
    (config_dir / "users.toml").write_text('[clusters]\nuser = "root"\nenc = "root-pass"\n')
    root_before = (config_dir / "users.toml").read_text()

    code, output = _invoke(config_dir, "--type", "clusters", "--scope", "Org1", "--user", "u")

    assert code == 0, output
    users = tomllib.loads((config_dir / "Org1" / "users.toml").read_text())
    assert users["clusters"] == {"user": "u", "enc": SECRET}
    assert (config_dir / "users.toml").read_text() == root_before
    assert "Org1" in output
    assert SECRET not in output


def test_type_scope_keeps_existing_sections(tmp_path: Path) -> None:
    config_dir = _config_dir(tmp_path)
    (config_dir / "Org1" / "users.toml").write_text('[aiqums]\nuser = "keep"\nenc = "keep-pass"\n')

    code, output = _invoke(config_dir, "--type", "clusters", "--scope", "Org1", "--user", "u")

    assert code == 0, output
    users = tomllib.loads((config_dir / "Org1" / "users.toml").read_text())
    assert users["aiqums"] == {"user": "keep", "enc": "keep-pass"}
    assert users["clusters"]["user"] == "u"


def test_console_scope_writes_token_a_fresh_config_reads(tmp_path: Path) -> None:
    config_dir = _config_dir(tmp_path, console_account=True)

    code, output = _invoke(config_dir, "--type", "console", "--scope", "Org1", "--user", "lbl")

    assert code == 0, output
    users = tomllib.loads((config_dir / "Org1" / "users.toml").read_text())
    assert users["console"] == {"user": "lbl", "enc": SECRET}
    assert not (config_dir / "users.toml").exists()
    settings = Config(config_dir=str(config_dir), script_name="t").get_console_api_settings(
        scope="Org1"
    )
    assert settings.refresh_token is not None
    assert settings.refresh_token.get_secret_value() == SECRET
    assert SECRET not in output


def test_console_scope_without_account_warns_and_writes(tmp_path: Path) -> None:
    config_dir = _config_dir(tmp_path)

    code, output = _invoke(config_dir, "--type", "console", "--scope", "Org1", "--user", "lbl")

    assert code == 0, output
    assert "no Console account" in " ".join(output.split())
    assert (config_dir / "Org1" / "users.toml").exists()


def test_unknown_scope_lists_scopes_and_writes_nothing(tmp_path: Path) -> None:
    config_dir = _config_dir(tmp_path)
    before = _snapshot(config_dir)

    code, output = _invoke(config_dir, "--type", "clusters", "--scope", "Nope", "--user", "u")

    assert code != 0
    assert "Unknown scope" in output
    assert "Org1" in output
    assert _snapshot(config_dir) == before


@pytest.mark.parametrize(
    "args",
    [
        ("--cluster", "org1-cl"),
        ("--type", "clusters", "--name", "org1-cl"),
        ("--type", "aiqums", "--name", "org1-aiqum"),
    ],
)
def test_object_with_matching_scope_succeeds(tmp_path: Path, args: tuple[str, ...]) -> None:
    config_dir = _config_dir(tmp_path)

    code, output = _invoke(config_dir, *args, "--scope", "Org1", "--user", "u")

    assert code == 0, output
    inv = tomllib.loads((config_dir / "Org1" / "inv.toml").read_text())
    obj_type = "aiqums" if "aiqums" in args else "clusters"
    name = "org1-aiqum" if "aiqums" in args else "org1-cl"
    assert inv[obj_type][name]["enc"] == SECRET
    assert not (config_dir / "Org1" / "users.toml").exists()


def test_object_in_other_scope_fails_naming_real_scope(tmp_path: Path) -> None:
    config_dir = _config_dir(tmp_path)
    before = _snapshot(config_dir)

    code, output = _invoke(config_dir, "--cluster", "org1-cl", "--scope", "Org2", "--user", "u")

    assert code != 0
    flat = " ".join(output.split())
    assert "scope 'Org1'" in flat
    assert "Org2" in flat
    assert _snapshot(config_dir) == before


def test_root_object_with_scope_fails_naming_root(tmp_path: Path) -> None:
    config_dir = _config_dir(tmp_path)
    before = _snapshot(config_dir)

    code, output = _invoke(config_dir, "--cluster", "root-cl", "--scope", "Org1", "--user", "u")

    assert code != 0
    assert "root" in output
    assert _snapshot(config_dir) == before


def test_scoped_object_with_root_scope_flag_absent_still_works(tmp_path: Path) -> None:
    config_dir = _config_dir(tmp_path)

    code, output = _invoke(config_dir, "--cluster", "org1-cl", "--user", "u")

    assert code == 0, output
