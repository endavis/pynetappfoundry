"""CLI utility functions."""

from __future__ import annotations

import traceback

import click
from rich.console import Console
from rich.table import Table

console = Console()


def is_debug_mode() -> bool:
    """Check if debug mode is enabled.

    Returns:
        True if debug mode is enabled in the current Click context.
    """
    ctx = click.get_current_context(silent=True)
    if ctx and ctx.obj:
        return bool(ctx.obj.get("debug", False))
    return False


def print_table(
    title: str,
    columns: list[str],
    rows: list[list[str]],
    show_header: bool = True,
) -> None:
    """Print a formatted table to the console.

    Args:
        title: Table title.
        columns: Column headers.
        rows: List of row data.
        show_header: Whether to show column headers.
    """
    table = Table(title=title, show_header=show_header)
    for col in columns:
        table.add_column(col)
    for row in rows:
        table.add_row(*row)
    console.print(table)


def print_success(message: str) -> None:
    """Print a success message.

    Args:
        message: Message to print.
    """
    console.print(f"[green]{message}[/green]")


def print_error(message: str) -> None:
    """Print an error message.

    Args:
        message: Message to print.
    """
    console.print(f"[red]{message}[/red]")


def print_warning(message: str) -> None:
    """Print a warning message.

    Args:
        message: Message to print.
    """
    console.print(f"[yellow]{message}[/yellow]")


def print_info(message: str) -> None:
    """Print an info message.

    Args:
        message: Message to print.
    """
    console.print(f"[blue]{message}[/blue]")


def print_exception(message: str, exc: BaseException | None = None) -> None:
    """Print an error message with optional traceback in debug mode.

    Args:
        message: Error message to print.
        exc: Exception to include. If provided and debug mode is enabled,
             the full traceback will be printed.
    """
    console.print(f"[red]{message}[/red]")
    if exc and is_debug_mode():
        console.print("[dim]" + "".join(traceback.format_exception(exc)) + "[/dim]")
