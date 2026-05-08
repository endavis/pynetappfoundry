"""Corpus-specific AsciiDoc table parser.

Only the narrow subset of AsciiDoc tables used by the auto-generated NetApp
console docs is supported. Tables follow this strict shape::

    [cols=N*,options=header]
    |===
    |Name
    |Type
    |Required
    |Description

    |fieldName
    |string
    |True
    a|Description, possibly multi-line and possibly with bullets.

    ...
    |===

The parser fails loudly when a table does not match the expected column count
or header row -- this is intentional, see issue #697 (rubber-duck finding 6).
"""

from __future__ import annotations

from dataclasses import dataclass


class TableShapeError(ValueError):
    """Raised when a table does not match the expected column count or header row."""


@dataclass(frozen=True)
class Table:
    """Parsed AsciiDoc table."""

    headers: tuple[str, ...]
    rows: tuple[tuple[str, ...], ...]


def find_tables(body: str) -> list[tuple[int, int, str]]:
    """Return ``[(start_line, end_line, raw_block_text), ...]`` for every ``|===`` block.

    ``start_line`` and ``end_line`` are inclusive 0-based line indices into ``body``.
    """
    lines = body.splitlines()
    out: list[tuple[int, int, str]] = []
    i = 0
    while i < len(lines):
        if lines[i].strip() == "|===":
            start = i
            j = i + 1
            while j < len(lines) and lines[j].strip() != "|===":
                j += 1
            if j < len(lines):
                out.append((start, j, "\n".join(lines[start : j + 1])))
                i = j + 1
                continue
        i += 1
    return out


def parse_table(block: str, expected_cols: int | None = None) -> Table:
    """Parse a single ``|===`` block (without its surrounding attribute line).

    Cell starts are recognized at the start of a line as ``|`` or ``a|``. ``a|``
    cells may span multiple physical lines; their contents are concatenated until
    the next cell-start or table delimiter.
    """
    lines = block.splitlines()
    if not lines or lines[0].strip() != "|===" or lines[-1].strip() != "|===":
        raise TableShapeError("Block is not delimited by '|===' on both ends")

    cells: list[str] = []
    current: list[str] | None = None

    def _commit() -> None:
        if current is not None:
            cells.append("\n".join(current).strip())

    for line in lines[1:-1]:
        stripped = line.lstrip()
        if stripped.startswith("a|"):
            _commit()
            current = [stripped[2:].lstrip()]
        elif stripped.startswith("|"):
            # A line that begins with '|' may contain multiple cells separated by ' |'.
            # In this corpus, however, each header/data cell is on its own line and the
            # separator pattern ' |' does not appear inside cell text. Split conservatively.
            content = stripped[1:]
            # Treat blank-only line as part of preceding 'a|' cell.
            _commit()
            current = [content.rstrip()]
        else:
            # Continuation of the previous cell (typical for 'a|' multi-line content).
            if current is None:
                # Skip stray lines (e.g. a blank line before the first cell).
                if line.strip() == "":
                    continue
                # Unexpected content outside any cell - skip silently in lenient mode
                # but record nothing; this should not happen for the target corpus.
                continue
            current.append(line)
    _commit()

    cells = [c.strip() for c in cells]
    # Note: empty cells (e.g. ``a|`` with no description) are valid and must not be
    # filtered out; the row/column geometry depends on every cell being preserved.

    if expected_cols is None:
        # Try to infer column count from the header: headers contain no newlines
        # in this corpus.
        raise TableShapeError("expected_cols must be supplied")

    if len(cells) < expected_cols:
        raise TableShapeError(
            f"Table has {len(cells)} cells, fewer than the {expected_cols} required for the header"
        )
    if len(cells) % expected_cols != 0:
        raise TableShapeError(
            f"Table cell count {len(cells)} is not a multiple of column count {expected_cols}"
        )

    headers = tuple(cells[:expected_cols])
    body_cells = cells[expected_cols:]
    rows = tuple(
        tuple(body_cells[i : i + expected_cols]) for i in range(0, len(body_cells), expected_cols)
    )
    return Table(headers=headers, rows=rows)


def assert_headers(table: Table, expected: tuple[str, ...]) -> None:
    """Verify that ``table.headers`` matches ``expected`` exactly (case-insensitive)."""
    actual = tuple(h.strip().lower() for h in table.headers)
    want = tuple(h.strip().lower() for h in expected)
    if actual != want:
        raise TableShapeError(f"Unexpected headers: got {table.headers}, want {expected}")
