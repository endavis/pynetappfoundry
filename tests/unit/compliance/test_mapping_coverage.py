"""Regression guard: every model directory must have a mapping or be excluded."""

from __future__ import annotations

from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
# TODO(#533): hardcoded to ontap only — when aiqum/occm/dii models land,
# generalize to walk all subdirectories of models/ and cache/.
_MODELS_ROOT = _PROJECT_ROOT / "src" / "pynetappfoundry" / "models" / "ontap"
_CACHE_ROOT = _PROJECT_ROOT / "src" / "pynetappfoundry" / "cache" / "ontap"

# Model directories that are intentionally unmapped (aggregate containers).
EXCLUDED: frozenset[str] = frozenset({"network", "protocols", "storage"})


def _dirs_with_file(root: Path, filename: str) -> set[str]:
    """Return relative POSIX paths of directories under *root* containing *filename*."""
    return {p.parent.relative_to(root).as_posix() for p in root.rglob(filename)}


def test_every_model_directory_has_mapping_or_exclusion() -> None:
    """New model directories must have a mapping.py or be explicitly excluded."""
    model_dirs = _dirs_with_file(_MODELS_ROOT, "model.py")
    mapping_dirs = _dirs_with_file(_CACHE_ROOT, "mapping.py")

    unmapped = model_dirs - mapping_dirs
    gaps = unmapped - EXCLUDED

    assert gaps == set(), (
        f"Model directories without a mapping.py or EXCLUDED entry: {sorted(gaps)}. "
        "Add a mapping.py in cache/ontap/<path>/ or add the path to EXCLUDED in this test."
    )
