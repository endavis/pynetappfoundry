"""Audit doit task for deeply nested mapping fields."""

from __future__ import annotations

from typing import Any

from rich.console import Console
from rich.table import Table


def _run_nested_audit() -> bool:
    """Walk all mappings, report fields with 3+ dot depth, return success."""
    import pynetappfoundry.cache  # noqa: F401 — triggers registry bootstrap
    from pynetappfoundry.cache._registry import model_registry

    console = Console()
    mappings = model_registry.mappings

    table = Table(title="Deeply Nested Field Audit (cache_attr depth >= 4)", show_lines=True)
    table.add_column("Mapping", style="bold")
    table.add_column("Total Deep", justify="right")
    table.add_column("Already Explicit", justify="right")
    table.add_column("Needs Review", justify="right")

    total_deep = 0
    total_explicit = 0
    total_needs_review = 0

    for name, mapping in sorted(mappings.items()):
        deep_fields: list[str] = []
        explicit_fields: list[str] = []

        for field in mapping.fields:
            if field.cache_attr.count(".") >= 3:
                deep_fields.append(field.cache_attr)
                if field.requires_explicit_fetch:
                    explicit_fields.append(field.cache_attr)

        if not deep_fields:
            continue

        needs_review = len(deep_fields) - len(explicit_fields)
        total_deep += len(deep_fields)
        total_explicit += len(explicit_fields)
        total_needs_review += needs_review

        review_style = "[red]" if needs_review > 0 else "[green]"
        table.add_row(
            name,
            str(len(deep_fields)),
            str(len(explicit_fields)),
            f"{review_style}{needs_review}[/]",
        )

    # Summary row
    table.add_section()
    review_style = "[red]" if total_needs_review > 0 else "[green]"
    table.add_row(
        "[bold]TOTAL[/bold]",
        f"[bold]{total_deep}[/bold]",
        f"[bold]{total_explicit}[/bold]",
        f"[bold]{review_style}{total_needs_review}[/]",
    )

    console.print()
    console.print(table)
    console.print()

    if total_needs_review > 0:
        console.print(
            f"[yellow]{total_needs_review} deeply nested field(s) "
            "lack requires_explicit_fetch — review recommended.[/yellow]"
        )
    else:
        console.print(
            "[bold green]All deeply nested fields have requires_explicit_fetch set.[/bold green]"
        )

    # Informational — always succeeds.
    return True


def task_mapping_nested_audit() -> dict[str, Any]:
    """Audit mappings for deeply nested fields (cache_attr depth >= 4)."""
    return {
        "actions": [_run_nested_audit],
        "verbosity": 2,
    }
