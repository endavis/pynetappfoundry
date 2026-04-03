"""Tests for the SQL query engine with json_extract() support."""

from __future__ import annotations

import pytest
from pydantic import BaseModel, Field

from pynetappfoundry.cache.query_engine import (
    ParsedFilter,
    SQLCondition,
    build_sql_condition,
    build_where_clause,
    parse_filter,
    parse_filters,
    resolve_field_path,
)

# ---------------------------------------------------------------------------
# Test models (mimicking OntapVolume structure)
# ---------------------------------------------------------------------------


class _Autosize(BaseModel):
    mode: str = ""
    grow_threshold: int = 0
    maximum: int = 0


class _Aggregate(BaseModel):
    name: str = ""
    uuid: str = ""


class _AnalyticsInit(BaseModel):
    state: str = ""


class _Analytics(BaseModel):
    initialization: _AnalyticsInit = Field(default_factory=_AnalyticsInit)
    state: str = ""


class _TestVolume(BaseModel):
    name: str = ""
    uuid: str = ""
    size: int = 0
    state: str = ""
    access_time_enabled: bool = False
    comment: str | None = None
    autosize: _Autosize = Field(default_factory=_Autosize)
    aggregates: list[_Aggregate] = Field(default_factory=list)
    analytics: _Analytics = Field(default_factory=_Analytics)
    status: list[str] = Field(default_factory=list)
    score: float = 0.0


# ---------------------------------------------------------------------------
# parse_filter tests
# ---------------------------------------------------------------------------


class TestParseFilter:
    """Tests for parse_filter()."""

    def test_equality_string(self) -> None:
        result = parse_filter("name = 'vol1'")
        assert result == ParsedFilter(field_path="name", operator="=", value="vol1")

    def test_equality_double_quotes(self) -> None:
        result = parse_filter('name = "vol1"')
        assert result == ParsedFilter(field_path="name", operator="=", value="vol1")

    def test_inequality(self) -> None:
        result = parse_filter("autosize.mode != 'grow_shrink'")
        assert result == ParsedFilter(
            field_path="autosize.mode", operator="!=", value="grow_shrink"
        )

    def test_greater_than(self) -> None:
        result = parse_filter("size > 1073741824")
        assert result == ParsedFilter(field_path="size", operator=">", value=1073741824)

    def test_less_than(self) -> None:
        result = parse_filter("size < 100")
        assert result == ParsedFilter(field_path="size", operator="<", value=100)

    def test_greater_equal(self) -> None:
        result = parse_filter("autosize.grow_threshold >= 85")
        assert result == ParsedFilter(field_path="autosize.grow_threshold", operator=">=", value=85)

    def test_less_equal(self) -> None:
        result = parse_filter("size <= 500")
        assert result == ParsedFilter(field_path="size", operator="<=", value=500)

    def test_in_operator(self) -> None:
        result = parse_filter("state in ('online', 'mixed')")
        assert result == ParsedFilter(field_path="state", operator="in", value=["online", "mixed"])

    def test_not_in_operator(self) -> None:
        result = parse_filter("state not in ('offline')")
        assert result == ParsedFilter(field_path="state", operator="not in", value=["offline"])

    def test_numeric_integer(self) -> None:
        result = parse_filter("size = 1024")
        assert result.value == 1024
        assert isinstance(result.value, int)

    def test_numeric_float(self) -> None:
        result = parse_filter("score = 3.14")
        assert result.value == 3.14
        assert isinstance(result.value, float)

    def test_boolean_true(self) -> None:
        result = parse_filter("access_time_enabled = true")
        assert result.value is True

    def test_boolean_false(self) -> None:
        result = parse_filter("access_time_enabled = false")
        assert result.value is False

    def test_null(self) -> None:
        result = parse_filter("comment = null")
        assert result.value is None

    def test_none_keyword(self) -> None:
        result = parse_filter("comment = none")
        assert result.value is None

    def test_malformed_expression_raises(self) -> None:
        with pytest.raises(ValueError, match="Malformed filter expression"):
            parse_filter("bad")

    def test_malformed_no_value_raises(self) -> None:
        with pytest.raises(ValueError, match="Malformed filter expression"):
            parse_filter("name =")

    def test_in_without_tuple_raises(self) -> None:
        with pytest.raises(ValueError, match="requires a tuple value"):
            parse_filter("state in 'online'")

    def test_deep_path(self) -> None:
        result = parse_filter("analytics.initialization.state = 'running'")
        assert result.field_path == "analytics.initialization.state"
        assert result.value == "running"

    def test_in_with_numbers(self) -> None:
        result = parse_filter("size in (100, 200, 300)")
        assert result.value == [100, 200, 300]

    def test_whitespace_tolerance(self) -> None:
        result = parse_filter("  name   =   'vol1'  ")
        assert result == ParsedFilter(field_path="name", operator="=", value="vol1")


class TestParseFilters:
    """Tests for parse_filters()."""

    def test_multiple_filters(self) -> None:
        results = parse_filters(
            [
                "name = 'vol1'",
                "size > 100",
            ]
        )
        assert len(results) == 2
        assert results[0].field_path == "name"
        assert results[1].field_path == "size"

    def test_empty_list(self) -> None:
        results = parse_filters([])
        assert results == []


# ---------------------------------------------------------------------------
# resolve_field_path tests
# ---------------------------------------------------------------------------


class TestResolveFieldPath:
    """Tests for resolve_field_path()."""

    def test_scalar_field(self) -> None:
        result = resolve_field_path("name", _TestVolume)
        assert result == '"name"'

    def test_scalar_int_field(self) -> None:
        result = resolve_field_path("size", _TestVolume)
        assert result == '"size"'

    def test_json_sub_field(self) -> None:
        result = resolve_field_path("autosize.mode", _TestVolume)
        assert result == """json_extract("autosize", '$.mode')"""

    def test_deep_json_path(self) -> None:
        result = resolve_field_path("analytics.initialization.state", _TestVolume)
        assert result == """json_extract("analytics", '$.initialization.state')"""

    def test_unknown_field_raises(self) -> None:
        with pytest.raises(ValueError, match="Unknown field 'bogus'"):
            resolve_field_path("bogus", _TestVolume)

    def test_dot_path_on_scalar_raises(self) -> None:
        with pytest.raises(ValueError, match="Cannot use dot-path on scalar field"):
            resolve_field_path("name.sub", _TestVolume)

    def test_bare_json_column_raises(self) -> None:
        with pytest.raises(ValueError, match="Cannot filter on bare JSON column"):
            resolve_field_path("autosize", _TestVolume)

    def test_list_basemodel_sub_field_raises(self) -> None:
        with pytest.raises(ValueError, match="list\\[BaseModel\\]"):
            resolve_field_path("aggregates.name", _TestVolume)

    def test_list_scalar_sub_field_raises(self) -> None:
        with pytest.raises(ValueError, match="list column"):
            resolve_field_path("status.something", _TestVolume)

    def test_bool_field(self) -> None:
        result = resolve_field_path("access_time_enabled", _TestVolume)
        assert result == '"access_time_enabled"'


# ---------------------------------------------------------------------------
# build_sql_condition tests
# ---------------------------------------------------------------------------


class TestBuildSqlCondition:
    """Tests for build_sql_condition()."""

    def test_equality(self) -> None:
        parsed = ParsedFilter(field_path="name", operator="=", value="vol1")
        result = build_sql_condition(parsed, _TestVolume)
        assert result == SQLCondition(clause='"name" = ?', params=("vol1",))

    def test_inequality(self) -> None:
        parsed = ParsedFilter(field_path="name", operator="!=", value="vol1")
        result = build_sql_condition(parsed, _TestVolume)
        assert result == SQLCondition(clause='"name" != ?', params=("vol1",))

    def test_greater_than(self) -> None:
        parsed = ParsedFilter(field_path="size", operator=">", value=100)
        result = build_sql_condition(parsed, _TestVolume)
        assert result == SQLCondition(clause='"size" > ?', params=(100,))

    def test_less_equal(self) -> None:
        parsed = ParsedFilter(field_path="size", operator="<=", value=500)
        result = build_sql_condition(parsed, _TestVolume)
        assert result == SQLCondition(clause='"size" <= ?', params=(500,))

    def test_null_equality(self) -> None:
        parsed = ParsedFilter(field_path="comment", operator="=", value=None)
        result = build_sql_condition(parsed, _TestVolume)
        assert result == SQLCondition(clause='"comment" IS NULL', params=())

    def test_null_inequality(self) -> None:
        parsed = ParsedFilter(field_path="comment", operator="!=", value=None)
        result = build_sql_condition(parsed, _TestVolume)
        assert result == SQLCondition(clause='"comment" IS NOT NULL', params=())

    def test_null_with_gt_raises(self) -> None:
        parsed = ParsedFilter(field_path="comment", operator=">", value=None)
        with pytest.raises(ValueError, match="not valid with null"):
            build_sql_condition(parsed, _TestVolume)

    def test_in_operator(self) -> None:
        parsed = ParsedFilter(field_path="state", operator="in", value=["online", "mixed"])
        result = build_sql_condition(parsed, _TestVolume)
        assert result == SQLCondition(clause='"state" IN (?, ?)', params=("online", "mixed"))

    def test_not_in_operator(self) -> None:
        parsed = ParsedFilter(field_path="state", operator="not in", value=["offline"])
        result = build_sql_condition(parsed, _TestVolume)
        assert result == SQLCondition(clause='"state" NOT IN (?)', params=("offline",))

    def test_boolean_coercion_true(self) -> None:
        parsed = ParsedFilter(field_path="access_time_enabled", operator="=", value=True)
        result = build_sql_condition(parsed, _TestVolume)
        assert result == SQLCondition(clause='"access_time_enabled" = ?', params=(1,))

    def test_boolean_coercion_false(self) -> None:
        parsed = ParsedFilter(field_path="access_time_enabled", operator="=", value=False)
        result = build_sql_condition(parsed, _TestVolume)
        assert result == SQLCondition(clause='"access_time_enabled" = ?', params=(0,))

    def test_json_extract_equality(self) -> None:
        parsed = ParsedFilter(field_path="autosize.mode", operator="=", value="grow_shrink")
        result = build_sql_condition(parsed, _TestVolume)
        assert result.clause == """json_extract("autosize", '$.mode') = ?"""
        assert result.params == ("grow_shrink",)

    def test_json_extract_comparison(self) -> None:
        parsed = ParsedFilter(field_path="autosize.grow_threshold", operator=">=", value=85)
        result = build_sql_condition(parsed, _TestVolume)
        assert result.clause == """json_extract("autosize", '$.grow_threshold') >= ?"""
        assert result.params == (85,)

    def test_float_value(self) -> None:
        parsed = ParsedFilter(field_path="score", operator=">", value=2.5)
        result = build_sql_condition(parsed, _TestVolume)
        assert result == SQLCondition(clause='"score" > ?', params=(2.5,))


# ---------------------------------------------------------------------------
# build_where_clause tests
# ---------------------------------------------------------------------------


class TestBuildWhereClause:
    """Tests for build_where_clause()."""

    def test_single_filter(self) -> None:
        filters = [ParsedFilter(field_path="name", operator="=", value="vol1")]
        clause, params = build_where_clause(filters, _TestVolume)
        assert clause == 'WHERE "name" = ?'
        assert params == ["vol1"]

    def test_multiple_filters(self) -> None:
        filters = [
            ParsedFilter(field_path="name", operator="=", value="vol1"),
            ParsedFilter(field_path="size", operator=">", value=100),
        ]
        clause, params = build_where_clause(filters, _TestVolume)
        assert clause == 'WHERE "name" = ? AND "size" > ?'
        assert params == ["vol1", 100]

    def test_with_cluster_name(self) -> None:
        filters = [ParsedFilter(field_path="name", operator="=", value="vol1")]
        clause, params = build_where_clause(filters, _TestVolume, cluster_name="test-cluster")
        assert clause == 'WHERE "cluster_name" = ? AND "name" = ?'
        assert params == ["test-cluster", "vol1"]

    def test_cluster_name_only(self) -> None:
        clause, params = build_where_clause([], _TestVolume, cluster_name="test-cluster")
        assert clause == 'WHERE "cluster_name" = ?'
        assert params == ["test-cluster"]

    def test_empty_filters_no_cluster(self) -> None:
        clause, params = build_where_clause([], _TestVolume)
        assert clause == ""
        assert params == []

    def test_multiple_json_filters(self) -> None:
        filters = [
            ParsedFilter(field_path="autosize.mode", operator="!=", value="grow_shrink"),
            ParsedFilter(field_path="autosize.grow_threshold", operator=">=", value=85),
        ]
        clause, params = build_where_clause(filters, _TestVolume)
        assert "json_extract" in clause
        assert "AND" in clause
        assert params == ["grow_shrink", 85]
