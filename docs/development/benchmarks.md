---
title: Performance Benchmarks
description: Running, interpreting, and comparing the pytest-benchmark suite
audience:
  - contributors
tags:
  - testing
  - performance
  - benchmarks
---

# Performance Benchmarks

## Overview

The benchmark suite under `tests/benchmarks/` measures the runtime of hot paths in
the cache and query layers using [pytest-benchmark](https://pytest-benchmark.readthedocs.io/).
Benchmarks are **disabled by default** so they do not slow down `doit test` or CI; they
must be explicitly enabled when you want to run them.

The suite is intended for two scenarios:

- Confirming a change has no unexpected impact on a hot path before opening a PR.
- Capturing a baseline on `main` and comparing a feature branch against it to detect
  regressions.

## Audience and Prerequisites

- **Audience:** Contributors making changes to the cache, diff engine, query engine,
  serialization, or `dict_path` utilities.
- **Prerequisites:** A working development environment (`uv sync` complete) and the
  `doit` task runner.

## Running the Benchmarks

Three `doit` tasks wrap the common invocations:

```bash
doit benchmark           # one-shot run, prints results to stdout
doit benchmark_save      # run and save as baseline under tmp/benchmarks/
doit benchmark_compare   # run and compare against the saved baseline 0001_baseline
```

For ad-hoc runs (e.g. a single file or a specific group), invoke pytest directly:

```bash
uv run pytest tests/benchmarks/ --benchmark-enable --benchmark-only -v
uv run pytest tests/benchmarks/test_bench_diff.py --benchmark-enable --benchmark-only -v
```

The `--benchmark-enable` flag is required because `pyproject.toml` sets
`addopts = "--strict-config --strict-markers --benchmark-disable"` under
`[tool.pytest.ini_options]`. This disables benchmark collection by default so the
regular test runs stay fast. The `doit` tasks above already pass `--benchmark-enable`
and `--benchmark-only` for you.

## What Each Suite Measures

Each file uses one or more `pytest.mark.benchmark(group=...)` markers so the output
groups related cases together.

### Dict path lookup — `test_bench_dict_path.py`

- **Group:** `dict_path`
- **Under test:** `pynetappfoundry.utils.dict_path.get_nested_value`
- **Why it matters:** `get_nested_value()` is called once per field per record
  during metadata collection. Even small regressions here are amplified across
  thousands of calls per cache refresh.
- **Cases:** shallow key, two/three/four-level nested access, indexed array
  (`nodes[0].name`), wildcard array (`nodes[*].name`), wildcard with nested
  access, and a "multi-field extraction" case that simulates pulling 10 fields
  from a single record (the typical collection-loop shape).

### Cache serialization — `test_bench_serialization.py`

- **Groups:** `serialization`, `deserialization`, `round_trip`
- **Under test:** `pynetappfoundry.cache.db._model_to_row` and
  `pynetappfoundry.cache.db._row_to_model`
- **Why it matters:** These functions sit on every cache read and write. They
  handle JSON encoding/decoding of nested sub-models, boolean coercion, datetime
  serialization, and extra field collection — so they dominate the CPU cost of
  bulk cache loads.
- **Cases:** single record plus batches of 100 and 1000 `BenchVolume` instances
  for both directions, and a single round-trip
  (`model -> row -> model`). The `BenchVolume` model in `conftest.py` mixes
  scalars, nested sub-models, and list fields to exercise every serialization
  branch.

### Cache diff engine — `test_bench_diff.py`

- **Groups:** `diff`, `diff_entity`
- **Under test:** `pynetappfoundry.cache.diff.compute_diff` and the lower-level
  `_diff_entity_list` helper.
- **Why it matters:** `compute_diff()` runs on every cache update cycle to detect
  added, removed, and modified entities between two `CachedClusterMetadata`
  snapshots.
- **Cases:** initial capture (`before=None`), no-change (two identical snapshots),
  ~10% modified, 10 added + 10 removed, and a 500-volume scale test. Two
  `_diff_entity_list` micro-benchmarks isolate the entity-level diff from the
  metadata traversal.

### Query engine — `test_bench_query_engine.py`

- **Groups:** `query_parse`, `query_resolve`, `query_build`, `query_e2e`
- **Under test:** `pynetappfoundry.cache.query_engine.parse_filter`,
  `parse_filters`, `resolve_field_path`, `build_sql_condition`, and
  `build_where_clause`.
- **Why it matters:** Filter parsing uses regex matching with no caching, so
  every query pays the parse cost fresh. Field-path resolution and SQL condition
  building run on every parsed filter.
- **Cases:** simple equality, numeric, dotted JSON path, `IN` / `NOT IN`,
  boolean, null, and a 10-filter batch parse; scalar vs JSON sub-field
  resolution; condition building for equality, `IN`, and JSON paths; and
  end-to-end `WHERE` clause construction from 5 and 10 parsed filters.

## Reading the Output

`pytest-benchmark` prints a table per group with columns including:

| Column | Meaning |
| :--- | :--- |
| `Min` / `Max` | Fastest and slowest single round (lower is better) |
| `Mean` | Arithmetic mean across rounds |
| `StdDev` | Standard deviation across rounds |
| `Median` | Middle value — usually the most stable single number to track |
| `IQR` | Interquartile range — a robust spread measure |
| `Outliers` | Rounds outside the IQR fence |
| `OPS` | Operations per second (higher is better) |
| `Rounds` | Number of measured rounds |
| `Iterations` | Calls per round (auto-tuned) |

The `Group` column comes from the `@pytest.mark.benchmark(group=...)` markers
listed above.

The conditions under which numbers are taken are pinned in `pyproject.toml`:

```toml
[tool.pytest-benchmark]
disable_gc = true
min_rounds = 5
warmup = true
```

That is: garbage collection is disabled during measurement, every test runs at
least five rounds, and pytest-benchmark performs a warm-up pass before the
measured rounds start. Keep these in mind when interpreting results — they are
designed to make numbers reproducible across runs on the same machine, not to
match production conditions.

## Comparing Runs / Detecting Regressions

The supported workflow for catching regressions is:

```bash
# 1. On main, capture a baseline
git checkout main
doit benchmark_save

# 2. Switch to your feature branch
git checkout my-feature

# 3. Run the same suite and diff against the baseline
doit benchmark_compare
```

`pytest-benchmark` prints a side-by-side table showing the percentage delta in
`Min`, `Mean`, `Median`, etc. for each test. Saved runs live under
`tmp/benchmarks/` (gitignored), so baselines are local to your checkout.

**Interpreting variance.** Benchmarks on a developer laptop are noisy. Background
processes, thermal throttling, and CPU frequency scaling can produce swings of
several percent run-to-run even with no code change. As a rule of thumb:

- Swings under ~5% in `Mean` / `Median` are usually noise.
- Consistent regressions of 10% or more in `Mean` / `Median` are worth
  investigating.
- Always re-run before drawing conclusions, ideally back-to-back on the same
  machine with no other heavy work running.

## Adding New Benchmarks

To add a new benchmark, drop a `test_bench_*.py` file into `tests/benchmarks/`,
mark each test with `@pytest.mark.benchmark(group="<group-name>")`, and reuse
the fixtures defined in `tests/benchmarks/conftest.py` (`bench_volumes_10`,
`bench_volumes_100`, `bench_volumes_1000`, `nested_api_response`) wherever
possible. Keep the production code under test imported at module level so the
benchmark measures the function, not the import.

## See Also

- [Cache Models](cache-models.md) — architecture of the cached model layer
  whose hot paths these benchmarks cover.
- [Cache Reference](../reference/cache.md) — user-facing reference for the
  cache subsystem.
- [CI/CD Testing Guide](ci-cd-testing.md) — how the regular (non-benchmark)
  test suite is run in CI.
