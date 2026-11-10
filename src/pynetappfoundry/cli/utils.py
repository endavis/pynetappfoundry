"""CLI utility functions."""

from __future__ import annotations

import logging
import traceback

import click
from rich.console import Console
from rich.markup import escape
from rich.table import Table

logger = logging.getLogger(__name__)
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
    """Print a success message to console and log to file.

    Args:
        message: Message to print.
    """
    console.print(f"[green]{escape(message)}[/green]")
    logger.info(message)


def print_error(message: str) -> None:
    """Print an error message to console and log to file.

    Args:
        message: Message to print.
    """
    console.print(f"[red]{escape(message)}[/red]")
    logger.error(message)


def print_warning(message: str) -> None:
    """Print a warning message to console and log to file.

    Args:
        message: Message to print.
    """
    console.print(f"[yellow]{escape(message)}[/yellow]")
    logger.warning(message)


def print_info(message: str) -> None:
    """Print an info message to console and log to file.

    Args:
        message: Message to print.
    """
    console.print(f"[blue]{escape(message)}[/blue]")
    logger.info(message)


def print_exception(
    message: str,
    exc: BaseException | None = None,
    *,
    debug: bool | None = None,
) -> None:
    """Print an error message with optional traceback in debug mode.

    Also logs to file - with the exception's traceback if exc is provided.

    Args:
        message: Error message to print.
        exc: Exception to include. If provided and debug mode is enabled,
             the full traceback will be printed to console. If provided,
             the traceback is also recorded in the log file.
        debug: Whether to print the traceback. ``None`` (default) reads the
             current debug mode; pass a value when it was captured earlier.
    """
    console.print(f"[red]{escape(message)}[/red]")
    if exc:
        logger.error(message, exc_info=exc)
    else:
        logger.error(message)
    show_traceback = is_debug_mode() if debug is None else debug
    if exc and show_traceback:
        console.print("[dim]" + escape("".join(traceback.format_exception(exc))) + "[/dim]")


def format_value_markup(value: object) -> str | None:
    """Format a scalar value with Rich markup for display.

    Provides consistent color-coding across CLI commands:
    - ``None`` → ``[yellow]null[/yellow]``
    - ``bool`` → ``[yellow]true/false[/yellow]``
    - ``int/float`` → ``[magenta]value[/magenta]``
    - ``str`` → ``[green]value[/green]`` (empty → ``[dim](empty)[/dim]``)

    Returns ``None`` for non-scalar types (dict, list, etc.) so callers can
    apply context-specific formatting.

    Args:
        value: Value to format.

    Returns:
        Rich-formatted string for scalars, or None if the value is not a
        supported scalar type.
    """
    if value is None:
        return "[yellow]null[/yellow]"
    if isinstance(value, bool):
        return f"[yellow]{str(value).lower()}[/yellow]"
    if isinstance(value, (int, float)):
        return f"[magenta]{value}[/magenta]"
    if isinstance(value, str):
        if not value:
            return "[dim](empty)[/dim]"
        return f"[green]{escape(value)}[/green]"
    return None


def print_debug(message: str) -> None:
    """Print debug message to console (if debug mode) and always log to file.

    Args:
        message: Debug message to print.
    """
    logger.debug(message)
    if is_debug_mode():
        console.print(f"[dim]{escape(message)}[/dim]")
