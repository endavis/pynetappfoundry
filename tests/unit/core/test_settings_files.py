"""Tests for the shared settings-file helpers (#1051)."""

from __future__ import annotations

import os
import stat
from pathlib import Path
from unittest.mock import patch

import pytest

from pynetappfoundry.core.config import ConfigurationError
from pynetappfoundry.core.settings_files import (
    atomic_write_text,
    find_setting_file,
    write_toml_values,
)

ORIGINAL = '# keep me\n[general]\nother = "x"  # inline\n'


def test_write_keeps_comments_and_unrelated_keys(tmp_path: Path) -> None:
    path = tmp_path / "a.toml"
    path.write_text(ORIGINAL)

    leaf = write_toml_values(path, ["general"], {"token": "placeholder-value"})

    text = path.read_text()
    assert "# keep me" in text
    assert "# inline" in text
    assert 'other = "x"' in text
    assert leaf == {"other": "x", "token": "placeholder-value"}


def test_write_creates_tables_and_parent_directories(tmp_path: Path) -> None:
    path = tmp_path / "deep" / "dir" / "a.toml"

    write_toml_values(path, ["one", "two"], {"k": "v"})

    assert "[one.two]" in path.read_text()


@pytest.mark.skipif(os.name == "nt", reason="Windows has no POSIX permission bits to keep")
def test_write_keeps_file_mode(tmp_path: Path) -> None:
    path = tmp_path / "a.toml"
    path.write_text(ORIGINAL)
    path.chmod(0o640)

    write_toml_values(path, ["general"], {"k": "v"})

    assert stat.S_IMODE(path.stat().st_mode) == 0o640


def test_failed_replace_leaves_original_and_no_temp_file(tmp_path: Path) -> None:
    path = tmp_path / "a.toml"
    path.write_text(ORIGINAL)

    with patch("os.replace", side_effect=OSError("boom")), pytest.raises(OSError):
        write_toml_values(path, ["general"], {"k": "v"})

    assert path.read_text() == ORIGINAL
    assert sorted(p.name for p in tmp_path.iterdir()) == ["a.toml"]


def test_temp_file_suffix_is_not_toml(tmp_path: Path) -> None:
    path = tmp_path / "a.toml"
    seen: list[str] = []
    real = os.replace

    def spy(src: str | Path, dst: str | Path) -> None:
        seen.append(Path(src).suffix)
        real(src, dst)

    with patch("os.replace", side_effect=spy):
        atomic_write_text(path, "x = 1\n")

    assert seen == [".tmp"]


def test_two_same_stem_files_are_ambiguous(tmp_path: Path) -> None:
    (tmp_path / "apis" / "a").mkdir(parents=True)
    (tmp_path / "apis" / "b").mkdir(parents=True)
    first = tmp_path / "apis" / "a" / "digitaladvisorapi.toml"
    second = tmp_path / "apis" / "b" / "digitaladvisorapi.toml"
    first.write_text("[general]\n")
    second.write_text("[general]\n")

    with pytest.raises(ConfigurationError) as exc:
        find_setting_file(tmp_path, "digitaladvisorapi", None)

    assert str(first) in str(exc.value)
    assert str(second) in str(exc.value)


def test_missing_file_defaults_to_apis_dir(tmp_path: Path) -> None:
    assert (
        find_setting_file(tmp_path, "digitaladvisorapi", None)
        == tmp_path / "apis" / "digitaladvisor" / "digitaladvisorapi.toml"
    )
