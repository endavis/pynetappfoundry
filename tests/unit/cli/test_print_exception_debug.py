"""Tests for the explicit ``debug`` argument of ``print_exception``."""

from __future__ import annotations

import io
from unittest.mock import patch

from rich.console import Console

from pynetappfoundry.cli.utils import print_exception


def _run(debug: bool | None, mode: bool) -> str:
    buf = io.StringIO()
    with (
        patch("pynetappfoundry.cli.utils.console", Console(file=buf, width=200)),
        patch("pynetappfoundry.cli.utils.is_debug_mode", return_value=mode),
    ):
        print_exception("failed", ValueError("inner"), debug=debug)
    return buf.getvalue()


def test_explicit_debug_true_prints_traceback_even_if_mode_off() -> None:
    assert "ValueError" in _run(True, mode=False)


def test_explicit_debug_false_hides_traceback_even_if_mode_on() -> None:
    assert "Traceback" not in _run(False, mode=True)


def test_none_defers_to_debug_mode() -> None:
    assert "ValueError" in _run(None, mode=True)
    assert "Traceback" not in _run(None, mode=False)
