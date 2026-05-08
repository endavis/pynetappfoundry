"""Tests for the type-expression parser."""

from __future__ import annotations

from tools.console_openapi.parser.types import parse_type


def test_primitive_string() -> None:
    assert parse_type("string").primitive == "string"


def test_primitive_int_alias() -> None:
    assert parse_type("int").primitive == "integer"


def test_primitive_integer() -> None:
    assert parse_type("integer").primitive == "integer"


def test_primitive_number() -> None:
    assert parse_type("number").primitive == "number"


def test_primitive_boolean() -> None:
    assert parse_type("boolean").primitive == "boolean"


def test_array_of_string() -> None:
    t = parse_type("array[string]")
    assert t.array_items is not None
    assert t.array_items.primitive == "string"


def test_array_empty() -> None:
    t = parse_type("array[]")
    assert t.array_items is not None
    assert t.array_items.raw == ""


def test_link_ref() -> None:
    t = parse_type("link:#metadata[metadata]")
    assert t.ref_anchor == "metadata"


def test_array_of_link() -> None:
    t = parse_type("array[link:#permissionDetail[permissionDetail]]")
    assert t.array_items is not None
    assert t.array_items.ref_anchor == "permissionDetail"


def test_any_of_top_level() -> None:
    t = parse_type("Any of: string, integer")
    assert t.one_of is not None
    kinds = {m.primitive for m in t.one_of}
    assert kinds == {"string", "integer"}


def test_array_any_of() -> None:
    t = parse_type("array[Any of: link:#permissionDetail[permissionDetail], string]")
    assert t.array_items is not None
    assert t.array_items.one_of is not None
    refs = [m.ref_anchor for m in t.array_items.one_of if m.ref_anchor]
    primitives = [m.primitive for m in t.array_items.one_of if m.primitive]
    assert refs == ["permissionDetail"]
    assert primitives == ["string"]


def test_hash_mapping_to_string() -> None:
    t = parse_type("Hash mapping strings to string")
    assert t.additional_properties is not None
    assert t.additional_properties.primitive == "string"


def test_unknown_type_falls_back_to_object() -> None:
    t = parse_type("WeirdCustomType")
    assert t.primitive == "object"
    assert t.raw == "WeirdCustomType"
