"""Benchmarks for nested dictionary path resolution.

get_nested_value() is called per-field per-record during metadata
collection, making it one of the hottest paths in the codebase.
"""

from __future__ import annotations

from typing import Any

import pytest

from pynetappfoundry.utils.dict_path import get_nested_value


@pytest.mark.benchmark(group="dict_path")
def test_bench_shallow_key(benchmark: Any, nested_api_response: dict[str, Any]) -> None:
    """Single top-level key lookup."""
    benchmark(get_nested_value, nested_api_response, "name")


@pytest.mark.benchmark(group="dict_path")
def test_bench_two_level(benchmark: Any, nested_api_response: dict[str, Any]) -> None:
    """Two-level nested dict access."""
    benchmark(get_nested_value, nested_api_response, "svm.name")


@pytest.mark.benchmark(group="dict_path")
def test_bench_three_level(benchmark: Any, nested_api_response: dict[str, Any]) -> None:
    """Three-level nested dict access."""
    benchmark(get_nested_value, nested_api_response, "space.snapshot.used")


@pytest.mark.benchmark(group="dict_path")
def test_bench_four_level(benchmark: Any, nested_api_response: dict[str, Any]) -> None:
    """Four-level nested dict access."""
    benchmark(get_nested_value, nested_api_response, "cloud.instance.type")


@pytest.mark.benchmark(group="dict_path")
def test_bench_array_index(benchmark: Any, nested_api_response: dict[str, Any]) -> None:
    """Array index access: nodes[0].name."""
    benchmark(get_nested_value, nested_api_response, "nodes[0].name")


@pytest.mark.benchmark(group="dict_path")
def test_bench_wildcard(benchmark: Any, nested_api_response: dict[str, Any]) -> None:
    """Wildcard array access: nodes[*].name (4 items)."""
    benchmark(get_nested_value, nested_api_response, "nodes[*].name")


@pytest.mark.benchmark(group="dict_path")
def test_bench_wildcard_nested(benchmark: Any, nested_api_response: dict[str, Any]) -> None:
    """Wildcard with nested access: nodes[*].interfaces (4 items x 4 interfaces)."""
    benchmark(get_nested_value, nested_api_response, "nodes[*].interfaces")


@pytest.mark.benchmark(group="dict_path")
def test_bench_multi_field_extraction(benchmark: Any, nested_api_response: dict[str, Any]) -> None:
    """Simulate extracting 10 fields from one record (typical collection loop)."""
    paths = [
        "name",
        "uuid",
        "svm.name",
        "svm.uuid",
        "autosize.mode",
        "autosize.grow_threshold",
        "space.available",
        "space.used",
        "cloud.provider",
        "cloud.region",
    ]

    def extract_all() -> list[Any]:
        return [get_nested_value(nested_api_response, p) for p in paths]

    benchmark(extract_all)
