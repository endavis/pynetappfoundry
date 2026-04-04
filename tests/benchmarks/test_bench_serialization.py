"""Benchmarks for model-to-row and row-to-model serialization.

These functions are the core path for all cache database reads and writes.
They handle JSON encoding/decoding of nested sub-models, boolean coercion,
datetime serialization, and extra field collection.
"""

from __future__ import annotations

from typing import Any

import pytest

from pynetappfoundry.cache.db import _model_to_row, _row_to_model

from .conftest import BenchVolume, _make_volume

# ---------------------------------------------------------------------------
# model_to_row benchmarks
# ---------------------------------------------------------------------------


@pytest.mark.benchmark(group="serialization")
def test_bench_model_to_row_single(benchmark: Any) -> None:
    """Serialize one populated volume to a SQL row dict."""
    vol = _make_volume(42)
    benchmark(_model_to_row, vol, BenchVolume)


@pytest.mark.benchmark(group="serialization")
def test_bench_model_to_row_batch_100(benchmark: Any, bench_volumes_100: list[BenchVolume]) -> None:
    """Serialize 100 volumes to row dicts."""

    def serialize_all() -> list[dict[str, Any]]:
        return [_model_to_row(v, BenchVolume) for v in bench_volumes_100]

    benchmark(serialize_all)


@pytest.mark.benchmark(group="serialization")
def test_bench_model_to_row_batch_1000(
    benchmark: Any, bench_volumes_1000: list[BenchVolume]
) -> None:
    """Serialize 1000 volumes to row dicts."""

    def serialize_all() -> list[dict[str, Any]]:
        return [_model_to_row(v, BenchVolume) for v in bench_volumes_1000]

    benchmark(serialize_all)


# ---------------------------------------------------------------------------
# row_to_model benchmarks
# ---------------------------------------------------------------------------


@pytest.mark.benchmark(group="deserialization")
def test_bench_row_to_model_single(benchmark: Any) -> None:
    """Deserialize one SQL row dict back to a model."""
    vol = _make_volume(42)
    row = _model_to_row(vol, BenchVolume)
    benchmark(_row_to_model, row, BenchVolume)


@pytest.mark.benchmark(group="deserialization")
def test_bench_row_to_model_batch_100(benchmark: Any, bench_volumes_100: list[BenchVolume]) -> None:
    """Deserialize 100 SQL rows back to models."""
    rows = [_model_to_row(v, BenchVolume) for v in bench_volumes_100]

    def deserialize_all() -> list[Any]:
        return [_row_to_model(r, BenchVolume) for r in rows]

    benchmark(deserialize_all)


@pytest.mark.benchmark(group="deserialization")
def test_bench_row_to_model_batch_1000(
    benchmark: Any, bench_volumes_1000: list[BenchVolume]
) -> None:
    """Deserialize 1000 SQL rows back to models."""
    rows = [_model_to_row(v, BenchVolume) for v in bench_volumes_1000]

    def deserialize_all() -> list[Any]:
        return [_row_to_model(r, BenchVolume) for r in rows]

    benchmark(deserialize_all)


# ---------------------------------------------------------------------------
# Round-trip benchmark
# ---------------------------------------------------------------------------


@pytest.mark.benchmark(group="round_trip")
def test_bench_round_trip_single(benchmark: Any) -> None:
    """Full serialize -> deserialize round-trip for one volume."""
    vol = _make_volume(42)

    def round_trip() -> Any:
        row = _model_to_row(vol, BenchVolume)
        return _row_to_model(row, BenchVolume)

    benchmark(round_trip)
