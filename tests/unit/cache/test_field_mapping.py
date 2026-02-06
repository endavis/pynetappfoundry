"""Tests for the declarative field mapping framework."""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock

import pytest
from pydantic import BaseModel, Field

from pynetappfoundry.cache.field_mapping import (
    FieldMapping,
    TypeMapping,
    _coerce_cli_value,
    parse_api_record,
    parse_api_response,
    parse_cli_record,
    parse_cli_records,
)

# ---------------------------------------------------------------------------
# Test model
# ---------------------------------------------------------------------------


class _SampleModel(BaseModel):
    """Minimal model for testing."""

    name: str = ""
    value: int = 0
    flag: bool = False
    items: list[str] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# FieldMapping tests
# ---------------------------------------------------------------------------


class TestFieldMapping:
    """Tests for FieldMapping dataclass."""

    def test_frozen(self) -> None:
        """FieldMapping instances are immutable."""
        fm = FieldMapping(cache_attr="name")
        with pytest.raises(AttributeError):
            fm.cache_attr = "other"  # type: ignore[misc]

    def test_defaults(self) -> None:
        """Unset optional fields get correct defaults."""
        fm = FieldMapping(cache_attr="x")
        assert fm.api_path is None
        assert fm.cli_field is None
        assert fm.default == ""
        assert fm.transform is None
        assert fm.cli_transform is None

    def test_with_all_fields(self) -> None:
        """All fields can be set."""
        tx = lambda r: r.get("x")  # noqa: E731
        ctx = lambda r: r.get("y")  # noqa: E731
        fm = FieldMapping(
            cache_attr="a",
            api_path="b.c",
            cli_field="d",
            default=42,
            transform=tx,
            cli_transform=ctx,
        )
        assert fm.cache_attr == "a"
        assert fm.api_path == "b.c"
        assert fm.cli_field == "d"
        assert fm.default == 42
        assert fm.transform is tx
        assert fm.cli_transform is ctx


# ---------------------------------------------------------------------------
# TypeMapping tests
# ---------------------------------------------------------------------------


class TestTypeMapping:
    """Tests for TypeMapping dataclass."""

    @pytest.fixture
    def sample_mapping(self) -> TypeMapping:
        """TypeMapping with varied field definitions."""
        return TypeMapping(
            name="Sample",
            model_class=_SampleModel,
            api_endpoint="/test?fields=*",
            cli_command="test show",
            fields=(
                FieldMapping(cache_attr="name", api_path="name", cli_field="name"),
                FieldMapping(
                    cache_attr="value",
                    api_path="nested.value",
                    cli_field="val",
                    default=0,
                ),
                FieldMapping(cache_attr="flag", api_path="nested.flag", default=False),
                FieldMapping(
                    cache_attr="items",
                    default=[],
                    transform=lambda r: r.get("items", []),
                    cli_transform=lambda r: r.get("items", "").split(","),
                ),
            ),
        )

    def test_api_expected_fields_deduplication(self, sample_mapping: TypeMapping) -> None:
        """api_expected_fields deduplicates nested paths to top-level keys."""
        expected = sample_mapping.api_expected_fields()
        assert expected == ["name", "nested"]

    def test_api_expected_fields_with_index(self) -> None:
        """Array index paths extract the key before brackets."""
        tm = TypeMapping(
            name="T",
            model_class=_SampleModel,
            api_endpoint="/t",
            cli_command="t show",
            fields=(FieldMapping(cache_attr="name", api_path="items[0].name"),),
        )
        assert tm.api_expected_fields() == ["items"]

    def test_cli_expected_fields(self, sample_mapping: TypeMapping) -> None:
        """cli_expected_fields returns only fields with cli_field set."""
        expected = sample_mapping.cli_expected_fields()
        assert expected == ["name", "val"]

    def test_id_field_default(self, sample_mapping: TypeMapping) -> None:
        """Default id_field is 'name'."""
        assert sample_mapping.id_field == "name"

    def test_frozen(self, sample_mapping: TypeMapping) -> None:
        """TypeMapping instances are immutable."""
        with pytest.raises(AttributeError):
            sample_mapping.name = "other"  # type: ignore[misc]


# ---------------------------------------------------------------------------
# _coerce_cli_value tests
# ---------------------------------------------------------------------------


class TestCoerceCliValue:
    """Tests for CLI value coercion."""

    def test_dash_returns_default(self) -> None:
        """Dash means missing → default."""
        assert _coerce_cli_value("-", 0) == 0
        assert _coerce_cli_value("-", "") == ""
        assert _coerce_cli_value("-", False) is False

    def test_empty_returns_default(self) -> None:
        """Empty string returns default."""
        assert _coerce_cli_value("", 42) == 42

    def test_int_conversion(self) -> None:
        """String integers are converted."""
        assert _coerce_cli_value("123", 0) == 123

    def test_int_with_percent_suffix(self) -> None:
        """Percentage suffix is stripped before int conversion."""
        assert _coerce_cli_value("90%", 0) == 90

    def test_int_invalid_returns_default(self) -> None:
        """Non-numeric string with int default returns default."""
        assert _coerce_cli_value("abc", 0) == 0

    def test_bool_true_variants(self) -> None:
        """Various truthy CLI values are coerced to True."""
        for val in ("true", "True", "yes", "1", "on", "ON"):
            assert _coerce_cli_value(val, False) is True

    def test_bool_false_variants(self) -> None:
        """Various falsy CLI values are coerced to False."""
        for val in ("false", "False", "no", "0", "off"):
            assert _coerce_cli_value(val, False) is False

    def test_bool_precedence_over_int(self) -> None:
        """Bool default takes precedence over int (bool is subclass of int)."""
        assert _coerce_cli_value("1", False) is True
        assert isinstance(_coerce_cli_value("1", False), bool)

    def test_string_passthrough(self) -> None:
        """String defaults pass through unchanged."""
        assert _coerce_cli_value("hello", "") == "hello"

    def test_whitespace_stripped(self) -> None:
        """Leading/trailing whitespace is stripped."""
        assert _coerce_cli_value("  42  ", 0) == 42


# ---------------------------------------------------------------------------
# parse_api_record tests
# ---------------------------------------------------------------------------


class TestParseApiRecord:
    """Tests for parsing a single API record."""

    @pytest.fixture
    def mapping(self) -> TypeMapping:
        """Simple TypeMapping for testing."""
        return TypeMapping(
            name="Test",
            model_class=_SampleModel,
            api_endpoint="/test",
            cli_command="test show",
            fields=(
                FieldMapping(cache_attr="name", api_path="name"),
                FieldMapping(cache_attr="value", api_path="nested.value", default=0),
                FieldMapping(cache_attr="flag", api_path="deep.nested.flag", default=False),
            ),
        )

    def test_simple_path(self, mapping: TypeMapping) -> None:
        """Top-level key extraction works."""
        record = {"name": "test1", "nested": {"value": 42}, "deep": {"nested": {"flag": True}}}
        result = parse_api_record(mapping, record, "[test]")
        assert result.name == "test1"

    def test_nested_path(self, mapping: TypeMapping) -> None:
        """Dot-path extraction works."""
        record = {"name": "test1", "nested": {"value": 99}, "deep": {"nested": {"flag": True}}}
        result = parse_api_record(mapping, record, "[test]")
        assert result.value == 99

    def test_three_level_path(self, mapping: TypeMapping) -> None:
        """Three-level dot-path extraction works."""
        record = {"name": "test1", "nested": {"value": 0}, "deep": {"nested": {"flag": True}}}
        result = parse_api_record(mapping, record, "[test]")
        assert result.flag is True

    def test_missing_path_uses_default(self, mapping: TypeMapping) -> None:
        """Missing path falls back to default."""
        record = {"name": "test1"}
        result = parse_api_record(mapping, record, "[test]")
        assert result.value == 0
        assert result.flag is False

    def test_transform_overrides_api_path(self) -> None:
        """Transform function takes precedence over api_path."""
        tm = TypeMapping(
            name="T",
            model_class=_SampleModel,
            api_endpoint="/t",
            cli_command="t",
            fields=(
                FieldMapping(cache_attr="name", api_path="wrong", transform=lambda _: "custom"),
            ),
        )
        result = parse_api_record(tm, {"wrong": "original"}, "[test]")
        assert result.name == "custom"

    def test_transform_exception_uses_default(self) -> None:
        """Transform exception falls back to default."""

        def bad_transform(_: dict[str, Any]) -> str:
            raise ValueError("boom")

        tm = TypeMapping(
            name="T",
            model_class=_SampleModel,
            api_endpoint="/t",
            cli_command="t",
            fields=(FieldMapping(cache_attr="name", default="fallback", transform=bad_transform),),
        )
        result = parse_api_record(tm, {}, "[test]")
        assert result.name == "fallback"

    def test_no_api_path_no_transform_uses_default(self) -> None:
        """Field with neither api_path nor transform uses default."""
        tm = TypeMapping(
            name="T",
            model_class=_SampleModel,
            api_endpoint="/t",
            cli_command="t",
            fields=(FieldMapping(cache_attr="name", default="def"),),
        )
        result = parse_api_record(tm, {"name": "ignored"}, "[test]")
        assert result.name == "def"


# ---------------------------------------------------------------------------
# parse_cli_record tests
# ---------------------------------------------------------------------------


class TestParseCliRecord:
    """Tests for parsing a single CLI record."""

    @pytest.fixture
    def mapping(self) -> TypeMapping:
        """Simple TypeMapping for CLI testing."""
        return TypeMapping(
            name="Test",
            model_class=_SampleModel,
            api_endpoint="/test",
            cli_command="test show",
            fields=(
                FieldMapping(cache_attr="name", cli_field="name"),
                FieldMapping(cache_attr="value", cli_field="val", default=0),
                FieldMapping(cache_attr="flag", cli_field="is-active", default=False),
            ),
        )

    def test_simple_lookup(self, mapping: TypeMapping) -> None:
        """Simple CLI field lookup works."""
        record = {"name": "vol1", "val": "42", "is-active": "true"}
        result = parse_cli_record(mapping, record, "[test]")
        assert result.name == "vol1"

    def test_int_coercion(self, mapping: TypeMapping) -> None:
        """CLI string values are coerced to int based on default type."""
        record = {"name": "vol1", "val": "100", "is-active": "false"}
        result = parse_cli_record(mapping, record, "[test]")
        assert result.value == 100

    def test_bool_coercion(self, mapping: TypeMapping) -> None:
        """CLI boolean strings are coerced correctly."""
        record = {"name": "vol1", "val": "0", "is-active": "true"}
        result = parse_cli_record(mapping, record, "[test]")
        assert result.flag is True

    def test_missing_field_uses_default(self, mapping: TypeMapping) -> None:
        """Missing CLI field returns default."""
        record = {"name": "vol1"}
        result = parse_cli_record(mapping, record, "[test]")
        assert result.value == 0
        assert result.flag is False

    def test_cli_transform(self) -> None:
        """cli_transform overrides cli_field lookup."""
        tm = TypeMapping(
            name="T",
            model_class=_SampleModel,
            api_endpoint="/t",
            cli_command="t",
            fields=(
                FieldMapping(
                    cache_attr="items",
                    default=[],
                    cli_transform=lambda r: r.get("raw", "").split(","),
                ),
            ),
        )
        result = parse_cli_record(tm, {"raw": "a,b,c"}, "[test]")
        assert result.items == ["a", "b", "c"]

    def test_cli_transform_exception_uses_default(self) -> None:
        """cli_transform exception falls back to default."""

        def bad_cli_transform(_: dict[str, Any]) -> list[str]:
            raise ValueError("boom")

        tm = TypeMapping(
            name="T",
            model_class=_SampleModel,
            api_endpoint="/t",
            cli_command="t",
            fields=(FieldMapping(cache_attr="items", default=[], cli_transform=bad_cli_transform),),
        )
        result = parse_cli_record(tm, {}, "[test]")
        assert result.items == []

    def test_non_string_value_passthrough(self) -> None:
        """Non-string CLI values are passed through without coercion."""
        tm = TypeMapping(
            name="T",
            model_class=_SampleModel,
            api_endpoint="/t",
            cli_command="t",
            fields=(FieldMapping(cache_attr="value", cli_field="val", default=0),),
        )
        result = parse_cli_record(tm, {"val": 42}, "[test]")
        assert result.value == 42


# ---------------------------------------------------------------------------
# parse_api_response tests
# ---------------------------------------------------------------------------


class TestParseApiResponse:
    """Tests for parsing a full API response."""

    @pytest.fixture
    def mapping(self) -> TypeMapping:
        """TypeMapping for response-level testing."""
        return TypeMapping(
            name="Test",
            model_class=_SampleModel,
            api_endpoint="/test",
            cli_command="test show",
            fields=(
                FieldMapping(cache_attr="name", api_path="name"),
                FieldMapping(cache_attr="value", api_path="value", default=0),
            ),
        )

    def test_none_response_returns_empty(self, mapping: TypeMapping) -> None:
        """None response returns empty list."""
        assert parse_api_response(mapping, None, "[t]", MagicMock()) == []

    def test_empty_records_returns_empty(self, mapping: TypeMapping) -> None:
        """Empty records list returns empty list."""
        result = parse_api_response(mapping, {"records": []}, "[t]", MagicMock())
        assert result == []

    def test_multiple_records(self, mapping: TypeMapping) -> None:
        """Multiple records are parsed individually."""
        response = {
            "records": [
                {"name": "a", "value": 1},
                {"name": "b", "value": 2},
            ]
        }
        results = parse_api_response(mapping, response, "[t]", MagicMock())
        assert len(results) == 2
        assert results[0].name == "a"
        assert results[1].name == "b"

    def test_calls_log_missing_fn(self, mapping: TypeMapping) -> None:
        """log_missing_fn is called for each record."""
        mock_log = MagicMock()
        response = {"records": [{"name": "a"}, {"name": "b"}]}
        parse_api_response(mapping, response, "[t]", mock_log)
        assert mock_log.call_count == 2
        # Verify expected fields are passed
        call_args = mock_log.call_args_list[0]
        assert call_args[0][1] == ["name", "value"]  # api_expected_fields()
        assert call_args[0][2] == "Test"  # mapping.name


# ---------------------------------------------------------------------------
# parse_cli_records tests
# ---------------------------------------------------------------------------


class TestParseCliRecords:
    """Tests for parsing CLI output records."""

    @pytest.fixture
    def mapping(self) -> TypeMapping:
        """TypeMapping for CLI records testing."""
        return TypeMapping(
            name="Test",
            model_class=_SampleModel,
            api_endpoint="/test",
            cli_command="test show",
            fields=(
                FieldMapping(cache_attr="name", api_path="name", cli_field="name"),
                FieldMapping(cache_attr="value", api_path="value", cli_field="val", default=0),
            ),
        )

    def test_empty_records_returns_empty(self, mapping: TypeMapping) -> None:
        """Empty records list returns empty list."""
        assert parse_cli_records(mapping, [], "[t]", MagicMock()) == []

    def test_multiple_records(self, mapping: TypeMapping) -> None:
        """Multiple CLI records are parsed individually."""
        records = [
            {"name": "a", "val": "1"},
            {"name": "b", "val": "2"},
        ]
        results = parse_cli_records(mapping, records, "[t]", MagicMock())
        assert len(results) == 2
        assert results[0].name == "a"
        assert results[1].value == 2

    def test_calls_log_missing_fn(self, mapping: TypeMapping) -> None:
        """log_missing_fn is called for each CLI record."""
        mock_log = MagicMock()
        records = [{"name": "a"}, {"name": "b"}]
        parse_cli_records(mapping, records, "[t]", mock_log)
        assert mock_log.call_count == 2
        call_args = mock_log.call_args_list[0]
        assert call_args[0][1] == ["name", "val"]  # cli_expected_fields()
        assert call_args[0][2] == "Test(CLI)"
