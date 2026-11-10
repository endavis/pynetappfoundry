"""Shared click option decorators for flags repeated across commands.

``--filter``, ``--json``, ``--csv`` and ``--all`` were declared by hand in many
commands. These factories declare each once so names, flags and help text stay
consistent. Each factory returns ``click.option(...)`` directly, so it sits in a
decorator stack exactly where the hand-written option did.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any, TypeVar

import click

_FC = TypeVar("_FC", bound="Callable[..., Any] | click.Command")

FILTER_HELP = 'JSON cluster filter, e.g. \'{"bu":"Business","env":"Prod"}\''
JSON_HELP = "Output as JSON."
CSV_HELP = "Output as CSV with header row."
ALL_HELP = "Query all cached clusters."


def filter_option(param_name: str = "filter") -> Callable[[_FC], _FC]:
    """Declare ``--filter/-f``, the JSON cluster filter.

    Args:
        param_name: Name of the parameter passed to the command function.

    Returns:
        A decorator adding the option.
    """
    return click.option("--filter", "-f", param_name, help=FILTER_HELP)


def json_option(help_text: str = JSON_HELP) -> Callable[[_FC], _FC]:
    """Declare the ``--json`` flag, passed as ``output_json``.

    Args:
        help_text: Help text shown in ``--help``.

    Returns:
        A decorator adding the option.
    """
    return click.option("--json", "output_json", is_flag=True, help=help_text)


def csv_option(param_name: str = "output_csv", help_text: str = CSV_HELP) -> Callable[[_FC], _FC]:
    """Declare the ``--csv`` flag.

    Args:
        param_name: Name of the parameter passed to the command function.
        help_text: Help text shown in ``--help``.

    Returns:
        A decorator adding the option.
    """
    return click.option("--csv", param_name, is_flag=True, help=help_text)


def all_option(
    param_name: str = "query_all", help_text: str = ALL_HELP, *, short_flag: bool = False
) -> Callable[[_FC], _FC]:
    """Declare the ``--all`` flag, optionally with the ``-a`` short form.

    Args:
        param_name: Name of the parameter passed to the command function.
        help_text: Help text shown in ``--help``.
        short_flag: Also declare ``-a``.

    Returns:
        A decorator adding the option.
    """
    names = ["--all", "-a", param_name] if short_flag else ["--all", param_name]
    return click.option(*names, is_flag=True, help=help_text)
