"""Shared Excel writer built on xlsxwriter.

Every report that writes a workbook goes through :class:`ExcelWorkbook`, so
sheet-name limits, BLOB values and NaN/inf are handled in one place.
"""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from pathlib import Path
from typing import Any

import xlsxwriter

MAX_SHEET_NAME_LEN = 31


def safe_sheet_name(name: str, existing: Iterable[str] = ()) -> str:
    """Return a valid, unique sheet name.

    Truncates to :data:`MAX_SHEET_NAME_LEN`. Excel compares names
    case-insensitively, so a collision with ``existing`` gets a numeric suffix
    (``1``, ``2``, ...) with the base shortened to keep the result within the limit.
    """
    taken = {n.lower() for n in existing}
    base = name[:MAX_SHEET_NAME_LEN]
    if base.lower() not in taken:
        return base
    counter = 1
    while True:
        suffix = str(counter)
        candidate = name[: MAX_SHEET_NAME_LEN - len(suffix)] + suffix
        if candidate.lower() not in taken:
            return candidate
        counter += 1


def _coerce(value: Any) -> Any:
    """Make a value writable: xlsxwriter cannot serialize ``bytes``."""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return value


class ExcelSheet:
    """A worksheet with an ``append`` that writes the next row."""

    def __init__(self, worksheet: Any, name: str) -> None:
        self.worksheet = worksheet
        self.name = name
        self._next_row = 0

    def append(self, values: Sequence[Any], cell_format: Any = None) -> None:
        """Write ``values`` as the next row, starting at column A."""
        for col, value in enumerate(values):
            self.worksheet.write(self._next_row, col, _coerce(value), cell_format)
        self._next_row += 1


class ExcelWorkbook:
    """An xlsxwriter workbook that de-duplicates and truncates sheet names."""

    def __init__(self, path: str | Path) -> None:
        self.workbook = xlsxwriter.Workbook(
            str(path), {"strings_to_urls": False, "nan_inf_to_errors": True}
        )
        self._sheets: list[ExcelSheet] = []

    @property
    def sheet_names(self) -> list[str]:
        """Names of the sheets added so far."""
        return [s.name for s in self._sheets]

    def add_sheet(self, name: str) -> ExcelSheet:
        """Add a sheet whose name is made valid and unique."""
        safe = safe_sheet_name(name, self.sheet_names)
        sheet = ExcelSheet(self.workbook.add_worksheet(safe), safe)
        self._sheets.append(sheet)
        return sheet

    def add_format(self, properties: dict[str, Any]) -> Any:
        """Create a cell format."""
        return self.workbook.add_format(properties)

    def close(self) -> None:
        """Write the file."""
        self.workbook.close()
