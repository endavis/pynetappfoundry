"""Benchmarks for CLI and package startup time (#903).

Each benchmark times a fresh interpreter, because import cost is paid once per process.
"""

from __future__ import annotations

import subprocess
import sys
from typing import Any

import pytest

_ROUNDS = 5


def _run(*args: str) -> None:
    subprocess.run([sys.executable, *args], check=True, capture_output=True)


@pytest.mark.benchmark
def test_bench_nf_help(benchmark: Any) -> None:
    """Benchmark ``nf --help`` startup."""
    benchmark.pedantic(
        _run,
        args=("-c", "from pynetappfoundry.cli import nf; nf(['--help'])"),
        rounds=_ROUNDS,
        iterations=1,
    )


@pytest.mark.benchmark
def test_bench_import_package(benchmark: Any) -> None:
    """Benchmark ``import pynetappfoundry``."""
    benchmark.pedantic(_run, args=("-c", "import pynetappfoundry"), rounds=_ROUNDS, iterations=1)


@pytest.mark.benchmark
def test_bench_full_registry_load(benchmark: Any) -> None:
    """Benchmark importing the cache and loading every registered mapping."""
    benchmark.pedantic(
        _run,
        args=(
            "-c",
            "from pynetappfoundry.cache import model_registry; len(model_registry.mappings)",
        ),
        rounds=_ROUNDS,
        iterations=1,
    )
