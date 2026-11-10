"""Tests for the shared Excel writer helper."""

from __future__ import annotations

from pathlib import Path

import openpyxl

from pynetappfoundry.utils.excel import MAX_SHEET_NAME_LEN, ExcelWorkbook, safe_sheet_name


class TestSafeSheetName:
    def test_short_name_unchanged(self) -> None:
        assert safe_sheet_name("abc", []) == "abc"

    def test_truncates(self) -> None:
        assert safe_sheet_name("x" * 50, []) == "x" * MAX_SHEET_NAME_LEN

    def test_collision_is_case_insensitive(self) -> None:
        assert safe_sheet_name("Abc", ["abc"]) == "Abc1"

    def test_collision_keeps_limit(self) -> None:
        first = "x" * 31
        second = safe_sheet_name("x" * 40, [first])
        assert second == "x" * 30 + "1"
        assert safe_sheet_name("x" * 40, [first, second]) == "x" * 30 + "2"


class TestExcelWorkbook:
    def test_round_trip(self, tmp_path: Path) -> None:
        path = tmp_path / "o.xlsx"
        wb = ExcelWorkbook(path)
        sheet = wb.add_sheet("data")
        sheet.append(["a", "b"])
        sheet.append([1, 2.5])
        wb.close()
        ws = openpyxl.load_workbook(path)["data"]
        assert [c.value for c in ws[1]] == ["a", "b"]
        assert [c.value for c in ws[2]] == [1, 2.5]

    def test_duplicate_names_get_distinct_sheets(self, tmp_path: Path) -> None:
        path = tmp_path / "o.xlsx"
        wb = ExcelWorkbook(path)
        first = wb.add_sheet("x" * 40)
        second = wb.add_sheet("x" * 41)
        assert first.name != second.name
        assert wb.sheet_names == [first.name, second.name]
        wb.close()
        assert len(openpyxl.load_workbook(path).sheetnames) == 2

    def test_strings_are_not_turned_into_urls(self, tmp_path: Path) -> None:
        path = tmp_path / "o.xlsx"
        wb = ExcelWorkbook(path)
        wb.add_sheet("s").append(["https://example.com"])
        wb.close()
        cell = openpyxl.load_workbook(path)["s"].cell(row=1, column=1)
        assert cell.value == "https://example.com"
        assert cell.hyperlink is None

    def test_bytes_are_decoded(self, tmp_path: Path) -> None:
        path = tmp_path / "o.xlsx"
        wb = ExcelWorkbook(path)
        wb.add_sheet("s").append([b"hi", b"\xff"])
        wb.close()
        ws = openpyxl.load_workbook(path)["s"]
        assert ws.cell(row=1, column=1).value == "hi"
        assert ws.cell(row=1, column=2).value == "�"

    def test_inf_does_not_crash(self, tmp_path: Path) -> None:
        path = tmp_path / "o.xlsx"
        wb = ExcelWorkbook(path)
        wb.add_sheet("s").append([float("inf"), float("nan"), 1])
        wb.close()
        assert path.exists()

    def test_no_openpyxl_in_src(self) -> None:
        src = Path(__file__).resolve().parents[3] / "src"
        offenders = [p for p in src.rglob("*.py") if "openpyxl" in p.read_text(encoding="utf-8")]
        assert offenders == []
