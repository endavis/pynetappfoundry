"""Tests for ``nf config show -s`` on empty and unknown sections (#1203)."""

from __future__ import annotations

import re
from pathlib import Path

from click.testing import CliRunner

from pynetappfoundry.cli.main import nf


def _config_dir(tmp_path: Path) -> Path:
    config_dir = tmp_path / "cfg"
    config_dir.mkdir()
    (config_dir / "inventory.toml").write_text(
        '[settings]\ntype = "data"\n\n[clusters.cl1]\nip = "10.0.0.1"\n'
    )
    # A settings file whose stem matches a data type puts "clusters" in both mappings.
    (config_dir / "clusters.toml").write_text('[general]\nnote = "x"\n')
    (config_dir / "empty.toml").write_text('[settings]\ntype = "data"\n\n[cloudinsights]\n')
    return config_dir


def _run(config_dir: Path, *args: str) -> tuple[int, str]:
    result = CliRunner().invoke(nf, ["--config-dir", str(config_dir), "config", "show", *args])
    return result.exit_code, " ".join(result.output.split())


def test_show_empty_section_reports_no_entries(tmp_path: Path) -> None:
    code, out = _run(_config_dir(tmp_path), "-s", "cloudinsights")

    assert code == 0
    assert "cloudinsights: no entries" in out
    assert "not found" not in out


def test_show_unknown_section_errors_with_unique_hint(tmp_path: Path) -> None:
    code, out = _run(_config_dir(tmp_path), "-s", "nope")

    assert code == 1
    assert "Section 'nope' not found." in out
    match = re.search(r"Available sections: (.*?)(?: Summary|$)", out)
    assert match is not None
    names = [n.strip() for n in match.group(1).split(",")]
    assert len(names) == len(set(names))
    assert "cloudinsights" in names
    assert "clusters" in names


def test_show_settings_file_named_like_empty_type_still_renders(tmp_path: Path) -> None:
    # cloudinsights is an empty inventory type here, and also the stem of a settings file:
    # the settings file is shown, as it was before #1203, not "no entries".
    config_dir = _config_dir(tmp_path)
    (config_dir / "cloudinsights.toml").write_text('[general]\nnote = "from-settings"\n')

    code, out = _run(config_dir, "-s", "cloudinsights")

    assert code == 0
    assert "from-settings" in out
    assert "no entries" not in out


def test_show_populated_section_still_renders(tmp_path: Path) -> None:
    code, out = _run(_config_dir(tmp_path), "-s", "clusters")

    assert code == 0
    assert "cl1" in out
    assert "10.0.0.1" in out
    assert "no entries" not in out
