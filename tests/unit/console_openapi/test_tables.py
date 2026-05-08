"""Tests for the AsciiDoc table parser."""

from __future__ import annotations

import pytest

from tools.console_openapi.parser.asciidoc_tables import (
    TableShapeError,
    assert_headers,
    parse_table,
)

_BODY_TABLE = """\
|===
|Name
|Type
|Required
|Description

|workspacePublicId
|string
|True
a|Workspace identifier.


|metadata
|link:#metadata[metadata]
|False
a|Optional metadata block.

|===
"""


def test_parse_body_table() -> None:
    table = parse_table(_BODY_TABLE, expected_cols=4)
    assert_headers(table, ("Name", "Type", "Required", "Description"))
    assert len(table.rows) == 2
    first = table.rows[0]
    assert first[0] == "workspacePublicId"
    assert first[1] == "string"
    assert first[2] == "True"
    assert "Workspace identifier" in first[3]


def test_wrong_column_count_raises() -> None:
    bad = "|===\n|Only\n|Three\n|Columns\n|===\n"
    with pytest.raises(TableShapeError):
        parse_table(bad, expected_cols=4)


def test_wrong_headers_raises() -> None:
    table = parse_table(_BODY_TABLE, expected_cols=4)
    with pytest.raises(TableShapeError):
        assert_headers(table, ("Wrong", "Headers", "Here", "Now"))
