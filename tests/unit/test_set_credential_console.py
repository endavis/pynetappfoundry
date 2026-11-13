"""Tests for ``nf config set-credential --type console`` (#736)."""

from __future__ import annotations

import tomllib
from pathlib import Path
from unittest.mock import patch

from click.testing import CliRunner

from pynetappfoundry.cli.main import nf

REFRESH = "placeholder-refresh-token"
MODULE = "pynetappfoundry.cli.commands.config.credentials"


def _config_dir(tmp_path: Path) -> Path:
    config_dir = tmp_path / "cfg"
    config_dir.mkdir()
    return config_dir


def _invoke(config_dir: Path, *args: str) -> tuple[int, str]:
    result = CliRunner().invoke(
        nf,
        ["--config-dir", str(config_dir), "config", "set-credential", *args],
        input=f"{REFRESH}\n{REFRESH}\n",
    )
    return result.exit_code, result.output


def test_type_console_no_encrypt_writes_users_toml(tmp_path: Path) -> None:
    config_dir = _config_dir(tmp_path)

    code, output = _invoke(config_dir, "--type", "console", "--user", "label", "--no-encrypt")

    assert code == 0, output
    data = tomllib.loads((config_dir / "users.toml").read_text())
    assert data["console"] == {"user": "label", "enc": REFRESH}


def test_type_console_encrypts_with_sops(tmp_path: Path) -> None:
    config_dir = _config_dir(tmp_path)
    with (
        patch(f"{MODULE}.is_sops_installed", return_value=True),
        patch(f"{MODULE}.get_age_key_path") as key_path,
        patch(f"{MODULE}.get_public_key_from_file", return_value="age1placeholderkey"),
        patch(f"{MODULE}.encrypt_value", return_value="SOPS[placeholder]") as encrypt,
    ):
        key_path.return_value.exists.return_value = True
        code, output = _invoke(config_dir, "--type", "console", "--user", "label")

    assert code == 0, output
    encrypt.assert_called_once_with(REFRESH, "age1placeholderkey")
    data = tomllib.loads((config_dir / "users.toml").read_text())
    assert data["console"] == {"user": "label", "enc": "SOPS[placeholder]"}
    assert REFRESH not in output


def test_type_clusters_behaviour_unchanged(tmp_path: Path) -> None:
    config_dir = _config_dir(tmp_path)

    code, output = _invoke(config_dir, "--type", "clusters", "--user", "admin", "--no-encrypt")

    assert code == 0, output
    data = tomllib.loads((config_dir / "users.toml").read_text())
    assert data["clusters"] == {"user": "admin", "enc": REFRESH}


def test_unknown_type_rejected(tmp_path: Path) -> None:
    code, _output = _invoke(_config_dir(tmp_path), "--type", "bogus", "--user", "u", "--no-encrypt")
    assert code != 0
