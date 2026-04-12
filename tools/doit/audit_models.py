"""Audit doit tasks for model-to-mapping coverage."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from rich.console import Console
from rich.table import Table

# Project root (tools/doit/ -> project root)
_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
# TODO(#533): hardcoded to ontap only — when aiqum/occm/dii models land,
# generalize to walk all subdirectories of models/ and cache/.
_MODELS_ROOT = _PROJECT_ROOT / "src" / "pynetappfoundry" / "models" / "ontap"
_CACHE_ROOT = _PROJECT_ROOT / "src" / "pynetappfoundry" / "cache" / "ontap"


def _find_dirs_with_file(root: Path, filename: str) -> set[str]:
    """Find all directories under *root* containing *filename*.

    Returns relative POSIX paths (e.g. ``storage/volumes``).
    """
    dirs: set[str] = set()
    for path in root.rglob(filename):
        rel = path.parent.relative_to(root)
        dirs.add(rel.as_posix())
    return dirs


def _check_unmapped_reason(model_rel: str) -> str | None:
    """Return the ``_UNMAPPED_REASON`` value from a model.py, or ``None``."""
    model_file = _MODELS_ROOT / model_rel / "model.py"
    if not model_file.exists():
        return None
    text = model_file.read_text()
    for line in text.splitlines():
        if line.startswith("_UNMAPPED_REASON"):
            # Extract the string value after '='
            _, _, value = line.partition("=")
            return value.strip().strip("\"'")
    return None


def _run_mapping_audit() -> bool:
    """Walk model and mapping directories, report coverage, return success."""
    console = Console()

    model_dirs = _find_dirs_with_file(_MODELS_ROOT, "model.py")
    mapping_dirs = _find_dirs_with_file(_CACHE_ROOT, "mapping.py")

    mapped = model_dirs & mapping_dirs
    unmapped = model_dirs - mapping_dirs

    intentional: dict[str, str] = {}
    gaps: set[str] = set()

    for rel in sorted(unmapped):
        reason = _check_unmapped_reason(rel)
        if reason:
            intentional[rel] = reason
        else:
            gaps.add(rel)

    # Summary table
    table = Table(title="Model-to-Mapping Audit", show_lines=True)
    table.add_column("Category", style="bold")
    table.add_column("Count", justify="right")
    table.add_column("Details")

    table.add_row("Mapped", str(len(mapped)), "")
    table.add_row(
        "Intentionally unmapped",
        str(len(intentional)),
        "\n".join(f"{k}: {v}" for k, v in sorted(intentional.items())),
    )

    if gaps:
        table.add_row(
            "[red]Gaps (missing mapping)[/red]",
            f"[red]{len(gaps)}[/red]",
            "\n".join(sorted(gaps)),
        )
    else:
        table.add_row("Gaps", "0", "[green]None[/green]")

    console.print()
    console.print(table)
    console.print()

    if gaps:
        console.print(
            f"[bold red]FAIL:[/bold red] {len(gaps)} model director(ies) "
            "lack a mapping.py and have no _UNMAPPED_REASON.",
        )
        return False

    console.print(
        "[bold green]All model directories are mapped or explicitly excluded.[/bold green]"
    )
    return True


def task_mapping_audit() -> dict[str, Any]:
    """Audit model directories for missing cache mappings."""
    return {
        "actions": [_run_mapping_audit],
        "verbosity": 2,
    }
