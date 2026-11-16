"""Tests for the shared path-placeholder helpers in data._path_params (#990, #1054)."""

from __future__ import annotations

from typing import Any

import pytest

from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.data._path_params import caller_path_params, placeholders
from pynetappfoundry.models._base import OntapModel


class _Model(OntapModel):
    key: str = ""


def _mapping(endpoint: str) -> TypeMapping:
    return TypeMapping(
        name="PathModel",
        model_class=_Model,
        api_endpoint=endpoint,
        api_type="aiqum",
        identifier_field="key",
        fields=(FieldMapping(cache_attr="key"),),
    )


class TestPlaceholders:
    def test_none(self) -> None:
        assert placeholders(_mapping("/x/y")) == []

    def test_in_order(self) -> None:
        assert placeholders(_mapping("/x/{a}/y/{b}")) == ["a", "b"]

    def test_query_string_ignored(self) -> None:
        assert placeholders(_mapping("/x/{a}?q={b}")) == ["a"]


class TestCallerPathParams:
    def test_encodes_reserved_characters(self) -> None:
        m = _mapping("/x/{key}/metrics")
        out = caller_path_params(m, ["key"], {"key": "a/b?c#d{e}"})
        assert out == {"key": "a%2Fb%3Fc%23d%7Be%7D"}

    def test_int_value_stringified(self) -> None:
        assert caller_path_params(_mapping("/x/{key}"), ["key"], {"key": 7}) == {"key": "7"}

    def test_unknown_key(self) -> None:
        with pytest.raises(ValueError, match="unknown path_params key"):
            caller_path_params(_mapping("/x/{key}"), ["key"], {"key": "a", "other": "b"})

    def test_missing_placeholder(self) -> None:
        with pytest.raises(ValueError, match=r"missing value\(s\) for \{b\}"):
            caller_path_params(_mapping("/x/{a}/{b}"), ["a", "b"], {"a": "1"})

    @pytest.mark.parametrize("value", ["", ".", ".."])
    def test_rejects_dot_segments_and_empty(self, value: Any) -> None:
        with pytest.raises(ValueError, match="must not be"):
            caller_path_params(_mapping("/x/{key}"), ["key"], {"key": value})
