"""Rendering of remote values containing Rich-markup-like text (#904)."""

from __future__ import annotations

import importlib
import io
from collections.abc import Iterator

import pytest
from rich.console import Console

from pynetappfoundry.cli.commands.cache.query import _format_display_value
from pynetappfoundry.cli.commands.cache.show import _format_value

BAD = "x [/y] z"

check_mod = importlib.import_module("pynetappfoundry.cli.commands.cache.check")
session_mod = importlib.import_module("pynetappfoundry.cli.commands.cifs.session")
get_mod = importlib.import_module("pynetappfoundry.cli.commands.licenses.get")


@pytest.fixture
def render() -> Iterator[Console]:
    """A Console that records output."""
    yield Console(file=io.StringIO(), width=300, force_terminal=False)


def _out(console: Console) -> str:
    assert isinstance(console.file, io.StringIO)
    return console.file.getvalue()


def test_query_display_value_escapes_non_scalars(render: Console) -> None:
    render.print(_format_display_value({"k": BAD}))
    render.print(_format_display_value(object))
    assert BAD in _out(render)


def test_show_format_value_fallback_escapes(render: Console) -> None:
    render.print(_format_value(("a", BAD)))
    assert BAD in _out(render)


def test_check_table_escapes_cells(render: Console) -> None:
    table = check_mod._output_table({BAD: [{"f": BAD}]}, ["f"])
    render.print(table)
    assert BAD in _out(render)


def test_licenses_table_escapes_cells(render: Console, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(get_mod, "console", render)
    get_mod._print_table([(BAD, BAD, BAD, BAD, BAD)])
    assert BAD in _out(render)


def test_cifs_table_escapes_cells(render: Console, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(session_mod, "console", render)
    session_mod._render_table([tuple(BAD for _ in session_mod.COLUMNS)], "T")
    assert BAD in _out(render)
