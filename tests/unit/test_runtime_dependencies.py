"""Guard the runtime dependency list in pyproject.toml (#896)."""

from __future__ import annotations

import tomllib
from pathlib import Path

from packaging.requirements import Requirement
from packaging.version import Version

PYPROJECT = Path(__file__).resolve().parents[2] / "pyproject.toml"


def _load() -> dict[str, object]:
    with PYPROJECT.open("rb") as fh:
        return tomllib.load(fh)


def _requirements(specs: list[str]) -> dict[str, Requirement]:
    reqs = (Requirement(s) for s in specs)
    return {r.name.lower(): r for r in reqs}


def _floor(req: Requirement) -> Version:
    floors = [Version(s.version) for s in req.specifier if s.operator == ">="]
    assert floors, f"{req.name} has no >= floor"
    return max(floors)


def _runtime() -> dict[str, Requirement]:
    project = _load()["project"]
    assert isinstance(project, dict)
    return _requirements(project["dependencies"])


def test_unused_packages_not_runtime_dependencies() -> None:
    runtime = _runtime()
    for name in ("pandas", "psutil", "doit"):
        assert name not in runtime, f"{name} must not be a runtime dependency"


def test_cryptography_cve_floor_kept() -> None:
    assert _floor(_runtime()["cryptography"]) >= Version("50")


def test_pydantic_floor_covers_perf_patches() -> None:
    assert _floor(_runtime()["pydantic"]) >= Version("2.10")


def test_doit_in_dev_extra() -> None:
    project = _load()["project"]
    assert isinstance(project, dict)
    dev = _requirements(project["optional-dependencies"]["dev"])
    assert "doit" in dev
