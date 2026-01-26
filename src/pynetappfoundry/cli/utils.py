"""CLI utility functions."""

from __future__ import annotations

from rich.console import Console
from rich.table import Table

console = Console()


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
