"""Tests for the ``generate_models_check`` drift task and the generated headers (#901)."""

from __future__ import annotations

import subprocess
from collections.abc import Callable
from pathlib import Path

import pytest

from tools.codegen.generators import _EXCLUDED_ENDPOINTS, GENERATED_HEADER
from tools.doit import codegen as tasks

MODELS = Path("models/ontap")
MODEL = MODELS / "vols" / "model.py"
EXCLUDED = MODELS / "cluster" / "model.py"
REPO_ROOT = Path(__file__).resolve().parents[3]
MODELS_ROOT = REPO_ROOT / "src" / "pynetappfoundry" / "models"


def _git(repo: Path, *args: str) -> str:
    result = subprocess.run(
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
    """A git repo with a generated model and an excluded-endpoint model, as cwd."""
    _git(tmp_path, "init", "-q")
    for rel in (MODEL, EXCLUDED):
        (tmp_path / rel).parent.mkdir(parents=True, exist_ok=True)
        (tmp_path / rel).write_text(f"{GENERATED_HEADER}\nA = 1\n" if rel == MODEL else "A = 1\n")
    _git(tmp_path, "add", ".")
    _git(tmp_path, "commit", "-q", "-m", "init")
    monkeypatch.chdir(tmp_path)
    return tmp_path


def _gen(action: Callable[[], None] | None = None) -> Callable[[list[str]], list[Path]]:
    """A fake generator that writes nothing but MODEL, after running *action*."""

    def generate(apis: list[str]) -> list[Path]:
        if action is not None:
            action()
        return [MODEL]

    return generate


def _check(generate: Callable[[list[str]], list[Path]]) -> bool:
    return tasks._check_generated_models(generate, [MODELS], ("ontap",))


def test_clean_run_passes_and_stays_clean(repo: Path) -> None:
    assert _check(_gen()) is True
    assert _git(repo, "status", "--porcelain") == ""


def test_modified_file_fails_and_is_restored(repo: Path) -> None:
    def edit() -> None:
        (repo / MODEL).write_text(f"{GENERATED_HEADER}\nA = 2\n")

    assert _check(_gen(edit)) is False
    assert (repo / MODEL).read_text() == f"{GENERATED_HEADER}\nA = 1\n"


def test_drift_hint_names_each_api(repo: Path, capsys: pytest.CaptureFixture[str]) -> None:
    """The fix-it hint names each checked API, never a bare run that adds other specs."""

    def edit() -> None:
        (repo / MODEL).write_text(f"{GENERATED_HEADER}\nA = 2\n")

    assert tasks._check_generated_models(_gen(edit), [MODELS], ("dii", "ontap")) is False
    err = capsys.readouterr().err
    assert "'doit generate_models --api=dii' and 'doit generate_models --api=ontap'" in err


def test_new_file_fails_and_is_removed(repo: Path) -> None:
    new = repo / MODELS / "new" / "model.py"

    def add() -> None:
        new.parent.mkdir()
        new.write_text("B = 1\n")

    assert _check(_gen(add)) is False
    assert not new.exists()


def test_deleted_file_fails_and_is_restored(repo: Path) -> None:
    assert _check(_gen(lambda: (repo / MODEL).unlink())) is False
    assert (repo / MODEL).exists()


def test_stale_file_fails(repo: Path, capsys: pytest.CaptureFixture[str]) -> None:
    stale = MODELS / "gone" / "model.py"
    (repo / stale).parent.mkdir()
    (repo / stale).write_text(f"{GENERATED_HEADER}\nC = 1\n")
    _git(repo, "add", ".")
    _git(repo, "commit", "-q", "-m", "stale")
    assert _check(_gen()) is False
    assert stale.as_posix() in capsys.readouterr().err


def test_excluded_endpoint_is_not_stale(repo: Path) -> None:
    assert _EXCLUDED_ENDPOINTS == {}
    assert _check(_gen()) is True


def test_dirty_tree_fails_without_generating(repo: Path) -> None:
    (repo / MODEL).write_text("mine\n")
    called: list[bool] = []
    assert _check(_gen(lambda: called.append(True))) is False
    assert called == []
    assert (repo / MODEL).read_text() == "mine\n"


def test_generation_error_still_restores(repo: Path) -> None:
    def boom() -> None:
        (repo / MODEL).write_text("A = 9\n")
        raise RuntimeError("boom")

    with pytest.raises(RuntimeError):
        _check(_gen(boom))
    assert (repo / MODEL).read_text() == f"{GENERATED_HEADER}\nA = 1\n"


def test_missing_spec_fails_the_check(repo: Path) -> None:
    with pytest.raises(FileNotFoundError):
        tasks._generate_models(["ontap"], strict=True)


def test_task_is_wired_and_explicit_about_apis() -> None:
    task = tasks.task_generate_models_check()
    assert len(task["actions"]) == 1
    assert tasks._GENERATED_APIS == ("dii", "ontap")
    assert "generate_models_check" not in tasks.task_generate_models_check.__module__


def test_generated_paths_cover_models_cache_and_index() -> None:
    names = {p.as_posix() for p in tasks._generated_paths()}
    assert "src/pynetappfoundry/models/ontap" in names
    assert "src/pynetappfoundry/models/dii" in names
    assert "src/pynetappfoundry/cache/_mapping_index.py" in names


@pytest.mark.parametrize("api", ["ontap", "dii"])
def test_committed_tree_has_generated_models(api: str) -> None:
    headed = [
        f
        for f in (MODELS_ROOT / api).rglob("model.py")
        if f.read_text().startswith(GENERATED_HEADER + "\n")
    ]
    assert len(headed) > 100


def test_cluster_model_is_generated_and_traits_model_is_hand_written() -> None:
    cluster = MODELS_ROOT / "ontap" / "cluster" / "model.py"
    traits = MODELS_ROOT / "ontap" / "cluster" / "traits" / "model.py"
    assert cluster.read_text().startswith(GENERATED_HEADER)
    assert not traits.read_text().startswith(GENERATED_HEADER)
