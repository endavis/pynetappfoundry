"""Tests for the sqlite-to-excel command."""

from __future__ import annotations

import sqlite3
from pathlib import Path

import openpyxl
from click.testing import CliRunner

from pynetappfoundry.cli.commands.utils.sqlite_to_excel import sqlite_to_excel


def _make_db(path: Path, tables: dict[str, str], rows: dict[str, list[tuple[object, ...]]]) -> None:
    conn = sqlite3.connect(path)
    for name, ddl in tables.items():
        conn.execute(f'CREATE TABLE "{name}" ({ddl})')
        for row in rows.get(name, []):
            conn.execute(f'INSERT INTO "{name}" VALUES ({",".join("?" * len(row))})', row)
    conn.commit()
    conn.close()


def _convert(tmp_path: Path) -> tuple[object, Path]:
    out = tmp_path / "out.xlsx"
    result = CliRunner().invoke(sqlite_to_excel, [str(tmp_path / "t.db"), "--output", str(out)])
    return result, out


def test_tables_become_sheets_with_types(tmp_path: Path) -> None:
    _make_db(
        tmp_path / "t.db",
        {"alpha": "a INTEGER, b TEXT, c REAL, d BLOB, e TEXT"},
        {"alpha": [(1, "x", 2.5, b"hi", None)]},
    )
    result, out = _convert(tmp_path)
    assert result.exit_code == 0, result.output  # type: ignore[attr-defined]
    ws = openpyxl.load_workbook(out)["alpha"]
    assert [c.value for c in ws[1]] == ["a", "b", "c", "d", "e"]
    row = [c.value for c in ws[2]]
    assert row[:3] == [1, "x", 2.5]
    assert row[3] in ("hi", b"hi")
    assert row[4] is None


def test_text_that_looks_like_url_stays_text(tmp_path: Path) -> None:
    _make_db(tmp_path / "t.db", {"u": "a TEXT"}, {"u": [("https://example.com",)]})
    result, out = _convert(tmp_path)
    assert result.exit_code == 0, result.output  # type: ignore[attr-defined]
    cell = openpyxl.load_workbook(out)["u"].cell(row=2, column=1)
    assert cell.value == "https://example.com"
    assert cell.hyperlink is None


def test_long_table_name_truncated(tmp_path: Path) -> None:
    long_name = "t" * 40
    _make_db(tmp_path / "t.db", {long_name: "a TEXT"}, {long_name: [("v",)]})
    result, out = _convert(tmp_path)
    assert result.exit_code == 0, result.output  # type: ignore[attr-defined]
    wb = openpyxl.load_workbook(out)
    assert wb.sheetnames == ["t" * 31]
    assert wb["t" * 31].cell(row=2, column=1).value == "v"


def test_no_tables_fails(tmp_path: Path) -> None:
    sqlite3.connect(tmp_path / "t.db").close()
    result, _ = _convert(tmp_path)
    assert result.exit_code != 0  # type: ignore[attr-defined]


def test_short_o_rejected(tmp_path: Path) -> None:
    """The short `-o` was dropped; only `--output` remains (#943)."""
    _make_db(tmp_path / "t.db", {"alpha": "a INTEGER"}, {"alpha": [(1,)]})
    result = CliRunner().invoke(
        sqlite_to_excel, [str(tmp_path / "t.db"), "-o", str(tmp_path / "o.xlsx")]
    )
    assert result.exit_code != 0
    assert "No such option" in result.output
    assert not (tmp_path / "o.xlsx").exists()


def test_long_output_writes_file(tmp_path: Path) -> None:
    """`--output` writes the workbook."""
    _make_db(tmp_path / "t.db", {"alpha": "a INTEGER"}, {"alpha": [(1,)]})
    result, out = _convert(tmp_path)
    assert result.exit_code == 0, result.output  # type: ignore[attr-defined]
    assert out.exists()
