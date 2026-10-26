"""Tests for the Console model codegen doit tasks (#825)."""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any

import pytest

from tools.doit import console_openapi_tasks as tasks

MODELS = Path("models")


def _git(repo: Path, *args: str) -> str:
    """Run ``git`` in ``repo`` with a fixed identity and no signing; return stdout."""
    result = subprocess.run(  # nosec B603 B607 - fixed argv, no shell
        [
            "git",
            "-c",
            "user.name=Test",
            "-c",
            "user.email=test@example.com",
            "-c",
            "commit.gpgsign=false",
            *args,
        ],
        cwd=repo,
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout


@pytest.fixture
def repo(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """A git repo with one committed module under ``models/``, as the working directory."""
    _git(tmp_path, "init", "-q")
    (tmp_path / MODELS).mkdir()
    (tmp_path / MODELS / "a.py").write_text("A = 1\n")
    _git(tmp_path, "add", ".")
    _git(tmp_path, "commit", "-q", "-m", "init")
    monkeypatch.chdir(tmp_path)
    return tmp_path


def test_formatters_are_pinned() -> None:
    flags = tasks._DATAMODEL_CODEGEN_FLAGS
    i = flags.index("--formatters")
    assert flags[i + 1 : i + 3] == ("black", "isort")


def test_unchanged_tree_passes(repo: Path) -> None:
    assert tasks._check_models_unchanged(MODELS) is True


def test_new_untracked_file_fails(repo: Path, capsys: pytest.CaptureFixture[str]) -> None:
    (repo / MODELS / "new.py").write_text("B = 2\n")

    assert tasks._check_models_unchanged(MODELS) is False
    assert "?? models/new.py" in capsys.readouterr().out


def test_new_file_in_new_subpackage_fails(repo: Path) -> None:
    (repo / MODELS / "sub").mkdir()
    (repo / MODELS / "sub" / "x.py").write_text("X = 1\n")

    assert tasks._check_models_unchanged(MODELS) is False


def test_deleted_file_fails(repo: Path) -> None:
    (repo / MODELS / "a.py").unlink()

    assert tasks._check_models_unchanged(MODELS) is False


def test_edited_file_fails(repo: Path) -> None:
    (repo / MODELS / "a.py").write_text("A = 2\n")

    assert tasks._check_models_unchanged(MODELS) is False


def test_change_outside_the_tree_is_ignored(repo: Path) -> None:
    (repo / "other.py").write_text("C = 3\n")

    assert tasks._check_models_unchanged(MODELS) is True


def test_generation_clears_stale_modules(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """A module the generator stops producing must not survive regeneration."""
    spec = tmp_path / "spec.yaml"
    spec.write_text("openapi: 3.0.3\n")
    out = tmp_path / "console"
    out.mkdir()
    (out / "stale.py").write_text("OLD = 1\n")
    monkeypatch.setattr(tasks, "_CONSOLE_SPEC", spec)
    monkeypatch.setattr(tasks, "_CONSOLE_MODELS_DIR", out)

    calls: list[list[str]] = []

    def fake_run(cmd: list[str], **_: Any) -> subprocess.CompletedProcess[str]:
        calls.append(cmd)
        if "datamodel-codegen" in cmd:
            (out / "fresh.py").write_text("NEW = 1\n")
        return subprocess.CompletedProcess(cmd, 0)

    monkeypatch.setattr(subprocess, "run", fake_run)

    tasks._generate_console_models()

    assert sorted(p.name for p in out.iterdir()) == ["fresh.py"]
    codegen = next(c for c in calls if "datamodel-codegen" in c)
    assert "--formatters" in codegen


def test_check_task_regenerates_then_checks() -> None:
    actions = tasks.task_console_models_check()["actions"]

    assert actions == [tasks._generate_console_models, tasks._check_models_unchanged]
