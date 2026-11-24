"""Tests for ``nf config set-credential --type X --name Y`` (#1045)."""

from __future__ import annotations

import tomllib
from pathlib import Path

import pytest
from click.testing import CliRunner

from pynetappfoundry.cli.main import nf

SECRET = "placeholder-secret"

DATA_FILE = """\
[settings]
type = "data"

[clusters.c1]
ip = "10.0.0.1"

[aiqums.aiqum1]
ip = "10.0.0.2"

[cloudinsights.t1]
base_url = "https://t1.example.invalid"

[ibm.ibm1]
ip = "10.0.0.3"
"""


def _config_dir(tmp_path: Path, content: str | None = DATA_FILE) -> Path:
    config_dir = tmp_path / "cfg"
    (config_dir / "data").mkdir(parents=True)
    if content is not None:
        (config_dir / "data" / "inventory.toml").write_text(content)
    return config_dir


def _invoke(config_dir: Path, *args: str, user_input: str | None = None) -> tuple[int, str]:
    result = CliRunner().invoke(
        nf,
        ["--config-dir", str(config_dir), "config", "set-credential", *args],
        input=f"{SECRET}\n{SECRET}\n" if user_input is None else user_input,
    )
    return result.exit_code, result.output


def _inventory(config_dir: Path) -> dict[str, dict[str, dict[str, str]]]:
    with open(config_dir / "data" / "inventory.toml", "rb") as f:
        return tomllib.load(f)


@pytest.mark.parametrize(
    ("obj_type", "name"),
    [
        ("clusters", "c1"),
        ("aiqums", "aiqum1"),
        ("cloudinsights", "t1"),
        ("ibm", "ibm1"),
    ],
)
def test_name_writes_object_entry(tmp_path: Path, obj_type: str, name: str) -> None:
    config_dir = _config_dir(tmp_path)

    code, output = _invoke(
        config_dir, "--type", obj_type, "--name", name, "--user", "lbl", "--no-encrypt"
    )

    assert code == 0, output
    entry = _inventory(config_dir)[obj_type][name]
    assert entry["user"] == "lbl"
    assert entry["enc"] == SECRET
    assert not (config_dir / "users.toml").exists()
    assert SECRET not in output


def test_cluster_alias_matches_type_and_name(tmp_path: Path) -> None:
    alias_dir = _config_dir(tmp_path / "a")
    full_dir = _config_dir(tmp_path / "b")

    alias_code, alias_out = _invoke(alias_dir, "--cluster", "c1", "--user", "u", "--no-encrypt")
    full_code, full_out = _invoke(
        full_dir, "--type", "clusters", "--name", "c1", "--user", "u", "--no-encrypt"
    )

    assert alias_code == full_code == 0
    assert _inventory(alias_dir) == _inventory(full_dir)

    # Rich may wrap long paths, so compare with all whitespace removed.
    def _norm(out: str, directory: Path) -> str:
        return "".join(out.split()).replace("".join(str(directory).split()), "X")

    assert _norm(alias_out, alias_dir) == _norm(full_out, full_dir)


def test_unknown_object_lists_available(tmp_path: Path) -> None:
    config_dir = _config_dir(tmp_path)
    before = (config_dir / "data" / "inventory.toml").read_text()

    code, output = _invoke(
        config_dir, "--type", "aiqums", "--name", "nope", "--user", "u", "--no-encrypt"
    )

    assert code != 0
    assert "nope" in output
    assert "aiqum1" in output
    assert (config_dir / "data" / "inventory.toml").read_text() == before


def test_unknown_cluster_message_unchanged(tmp_path: Path) -> None:
    code, output = _invoke(
        _config_dir(tmp_path), "--cluster", "nope", "--user", "u", "--no-encrypt"
    )

    assert code != 0
    assert "Cluster 'nope' not found in configuration." in output
    assert "Available clusters: c1" in output


def test_no_objects_of_type_hint(tmp_path: Path) -> None:
    config_dir = _config_dir(tmp_path)

    code, output = _invoke(
        config_dir, "--type", "azure", "--name", "x", "--user", "u", "--no-encrypt"
    )

    assert code != 0
    assert "No azure are defined" in output


@pytest.mark.parametrize(
    "args",
    [
        ("--name", "aiqum1"),
        ("--cluster", "c1", "--name", "c1"),
        ("--type", "console", "--name", "x"),
    ],
)
def test_invalid_flag_combinations_do_not_prompt_or_write(
    tmp_path: Path, args: tuple[str, ...]
) -> None:
    config_dir = _config_dir(tmp_path)
    before = (config_dir / "data" / "inventory.toml").read_text()

    code, output = _invoke(config_dir, *args, "--user", "u", "--no-encrypt", user_input="")

    assert code != 0, output
    assert (config_dir / "data" / "inventory.toml").read_text() == before
    assert not (config_dir / "users.toml").exists()


def test_type_without_name_still_writes_users_toml(tmp_path: Path) -> None:
    config_dir = _config_dir(tmp_path)

    code, output = _invoke(config_dir, "--type", "aiqums", "--user", "admin", "--no-encrypt")

    assert code == 0, output
    users = tomllib.loads((config_dir / "users.toml").read_text())
    assert users["aiqums"] == {"user": "admin", "enc": SECRET}
    assert "enc" not in _inventory(config_dir)["aiqums"]["aiqum1"]


def test_object_found_in_flat_data_type_file(tmp_path: Path) -> None:
    config_dir = _config_dir(tmp_path, content=None)
    (config_dir / "elsewhere").mkdir()
    target = config_dir / "elsewhere" / "inv.toml"
    target.write_text('[settings]\ntype = "data"\n\n[aiqums.a2]\nip = "10.0.0.9"\n')

    code, output = _invoke(
        config_dir, "--type", "aiqums", "--name", "a2", "--user", "u", "--no-encrypt"
    )

    assert code == 0, output
    assert tomllib.loads(target.read_text())["aiqums"]["a2"]["enc"] == SECRET


def test_read_write_stores_rw_enc_on_the_tenant(tmp_path: Path) -> None:
    config_dir = _config_dir(tmp_path)

    code, output = _invoke(
        config_dir, "--type", "cloudinsights", "--name", "t1", "--read-write", "--no-encrypt"
    )

    assert code == 0, output
    tenant = _inventory(config_dir)["cloudinsights"]["t1"]
    assert tenant["rw_enc"] == SECRET
    assert "enc" not in tenant
    assert "user" not in tenant
    assert tenant["base_url"] == "https://t1.example.invalid"
    assert SECRET not in output
    assert "Read-write key" in output


@pytest.mark.parametrize(
    "args",
    [
        ("--cluster", "c1", "--read-write"),
        ("--type", "aiqums", "--name", "aiqum1", "--read-write"),
        ("--type", "cloudinsights", "--read-write"),
        ("--type", "cloudinsights", "--name", "t1", "--user", "u", "--read-write"),
        ("--read-write",),
    ],
)
def test_read_write_invalid_combinations_do_not_prompt_or_write(
    tmp_path: Path, args: tuple[str, ...]
) -> None:
    config_dir = _config_dir(tmp_path)
    before = (config_dir / "data" / "inventory.toml").read_text()

    code, output = _invoke(config_dir, *args, "--no-encrypt", user_input="")

    assert code != 0, output
    assert "--read-write" in output
    assert (config_dir / "data" / "inventory.toml").read_text() == before
    assert not (config_dir / "users.toml").exists()


def test_read_write_unknown_tenant_is_rejected_before_prompt(tmp_path: Path) -> None:
    config_dir = _config_dir(tmp_path)
    before = (config_dir / "data" / "inventory.toml").read_text()

    code, output = _invoke(
        config_dir,
        "--type",
        "cloudinsights",
        "--name",
        "nope",
        "--read-write",
        "--no-encrypt",
        user_input="",
    )

    assert code != 0
    assert "not found" in output
    assert (config_dir / "data" / "inventory.toml").read_text() == before
