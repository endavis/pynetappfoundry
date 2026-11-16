"""Nullable ``["null", X]`` type cells (#1034)."""

from __future__ import annotations

import pytest

from tools.console_openapi.parser.types import parse_type


@pytest.mark.parametrize(
    ("cell", "primitive"),
    [
        ('["null", "integer"]', "integer"),
        ('["null", "string"]', "string"),
        ('["null", "boolean"]', "boolean"),
        ('["string", "null"]', "string"),
    ],
)
def test_nullable_cells(cell: str, primitive: str) -> None:
    t = parse_type(cell)
    assert t.primitive == primitive
    assert t.nullable is True


@pytest.mark.parametrize("cell", ['["null"]', '["null", "string", "integer"]', '["null", '])
def test_malformed_or_ambiguous_nullable_falls_back_to_object(cell: str) -> None:
    t = parse_type(cell)
    assert t.primitive == "object"
    assert t.nullable is False


def test_plain_primitive_is_not_nullable() -> None:
    assert parse_type("string").nullable is False
