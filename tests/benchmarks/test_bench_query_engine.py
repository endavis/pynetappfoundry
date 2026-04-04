"""Benchmarks for the SQL query engine filter parsing.

parse_filter() uses regex matching and value parsing on every query.
There is no caching, so this runs fresh each time.
"""

from __future__ import annotations

from typing import Any

import pytest

from pynetappfoundry.cache.query_engine import (
    build_sql_condition,
    build_where_clause,
    parse_filter,
    parse_filters,
    resolve_field_path,
)

from .conftest import QEVolume

# ---------------------------------------------------------------------------
# parse_filter benchmarks
# ---------------------------------------------------------------------------


@pytest.mark.benchmark(group="query_parse")
def test_bench_parse_filter_simple_eq(benchmark: Any) -> None:
    """Parse a simple equality filter."""
    benchmark(parse_filter, "name = 'vol_0001'")


@pytest.mark.benchmark(group="query_parse")
def test_bench_parse_filter_numeric(benchmark: Any) -> None:
    """Parse a numeric comparison filter."""
    benchmark(parse_filter, "size > 1073741824")


@pytest.mark.benchmark(group="query_parse")
def test_bench_parse_filter_dotted(benchmark: Any) -> None:
    """Parse a dotted JSON path filter."""
    benchmark(parse_filter, "autosize.mode != 'grow_shrink'")


@pytest.mark.benchmark(group="query_parse")
def test_bench_parse_filter_in_tuple(benchmark: Any) -> None:
    """Parse an IN filter with tuple value."""
    benchmark(parse_filter, "state in ('online', 'mixed', 'offline')")


@pytest.mark.benchmark(group="query_parse")
def test_bench_parse_filter_not_in(benchmark: Any) -> None:
    """Parse a NOT IN filter."""
    benchmark(parse_filter, "state not in ('offline', 'error')")


@pytest.mark.benchmark(group="query_parse")
def test_bench_parse_filter_boolean(benchmark: Any) -> None:
    """Parse a boolean filter."""
    benchmark(parse_filter, "access_time_enabled = true")


@pytest.mark.benchmark(group="query_parse")
def test_bench_parse_filter_null(benchmark: Any) -> None:
    """Parse a null filter."""
    benchmark(parse_filter, "comment = null")


@pytest.mark.benchmark(group="query_parse")
def test_bench_parse_filters_batch_10(benchmark: Any) -> None:
    """Parse 10 filters in a batch."""
    expressions = [
        "name = 'vol_0001'",
        "size > 1073741824",
        "autosize.mode != 'grow_shrink'",
        "state in ('online', 'mixed')",
        "access_time_enabled = true",
        "comment = null",
        "score >= 0.5",
        "size <= 10737418240",
        "state not in ('offline')",
        "autosize.grow_threshold > 80",
    ]
    benchmark(parse_filters, expressions)


# ---------------------------------------------------------------------------
# resolve_field_path benchmarks
# ---------------------------------------------------------------------------


@pytest.mark.benchmark(group="query_resolve")
def test_bench_resolve_scalar(benchmark: Any) -> None:
    """Resolve a scalar field path."""
    benchmark(resolve_field_path, "name", QEVolume)


@pytest.mark.benchmark(group="query_resolve")
def test_bench_resolve_json_subfield(benchmark: Any) -> None:
    """Resolve a JSON sub-field path (generates json_extract)."""
    benchmark(resolve_field_path, "autosize.mode", QEVolume)


# ---------------------------------------------------------------------------
# build_sql_condition benchmarks
# ---------------------------------------------------------------------------


@pytest.mark.benchmark(group="query_build")
def test_bench_build_condition_eq(benchmark: Any) -> None:
    """Build SQL condition for equality."""
    parsed = parse_filter("name = 'vol_0001'")
    benchmark(build_sql_condition, parsed, QEVolume)


@pytest.mark.benchmark(group="query_build")
def test_bench_build_condition_in(benchmark: Any) -> None:
    """Build SQL condition for IN clause."""
    parsed = parse_filter("state in ('online', 'mixed', 'offline')")
    benchmark(build_sql_condition, parsed, QEVolume)


@pytest.mark.benchmark(group="query_build")
def test_bench_build_condition_json(benchmark: Any) -> None:
    """Build SQL condition for JSON sub-field."""
    parsed = parse_filter("autosize.mode != 'grow_shrink'")
    benchmark(build_sql_condition, parsed, QEVolume)


# ---------------------------------------------------------------------------
# build_where_clause (end-to-end) benchmarks
# ---------------------------------------------------------------------------


@pytest.mark.benchmark(group="query_e2e")
def test_bench_where_clause_5_filters(benchmark: Any) -> None:
    """Build complete WHERE clause from 5 parsed filters."""
    filters = parse_filters(
        [
            "name = 'vol_0001'",
            "size > 1073741824",
            "state in ('online', 'mixed')",
            "autosize.mode != 'grow_shrink'",
            "access_time_enabled = true",
        ]
    )
    benchmark(build_where_clause, filters, QEVolume, cluster_name="bench-cluster")


@pytest.mark.benchmark(group="query_e2e")
def test_bench_where_clause_10_filters(benchmark: Any) -> None:
    """Build complete WHERE clause from 10 parsed filters."""
    filters = parse_filters(
        [
            "name = 'vol_0001'",
            "size > 1073741824",
            "state in ('online', 'mixed')",
            "autosize.mode != 'grow_shrink'",
            "access_time_enabled = true",
            "comment = null",
            "score >= 0.5",
            "size <= 10737418240",
            "state not in ('offline')",
            "autosize.grow_threshold > 80",
        ]
    )
    benchmark(build_where_clause, filters, QEVolume, cluster_name="bench-cluster")
