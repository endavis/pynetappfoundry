---
title: DataSource
description: Unified entry point for reading cluster data from cache or live API
audience:
  - users
tags:
  - datasource
  - query
  - cache
  - api
---

# DataSource

`DataSource` is the unified entry point for all cluster reads in pynetappfoundry. It routes requests through cache or live API based on per-field metadata and a per-call `source=` override, and returns typed Pydantic model instances regardless of the underlying path.

## Overview

| Surface | Best for | Returns |
|---------|----------|---------|
| `DataSource` | All new read code: cached, derived, and realtime fields | Pydantic model instances |
| `QuerySet` | Direct REST operations: mutations, job tracking, relationship traversal | Pydantic model instances |
| `LazyClusterMetadata` | Legacy cache reads (migrated to `DataSource` shim internally) | Pydantic model instances |

!!! note "Use DataSource for new code"
    `DataSource` supersedes direct use of `QuerySet` for reads and the `fetch_realtime` family for realtime fields. Both remain available for use cases `DataSource` does not cover (writes, job tracking, relationship traversal). See [Query Layer](query-layer.md) for the full `QuerySet` API.

## Quick Start

```python
from pynetappfoundry.core.config import Config
from pynetappfoundry.data.source import DataSource
from pynetappfoundry.models.ontap.storage.volumes.model import OntapVolume

config = Config()
ds = DataSource(config)

# Query: iterate all online volumes for a cluster
for vol in ds.query(OntapVolume, cluster="prod1").filter(state="online"):
    print(vol.name, vol.size)

# Get: fetch a single volume by UUID
vol = ds.get(OntapVolume, cluster="prod1", id="abc-123-def")
if vol is not None:
    print(vol.name)
```

## Querying Data

`DataSource.query()` returns a `QueryBuilder` -- a lazy, chainable object that executes only when iterated.

```python
qb = ds.query(OntapVolume, cluster="prod1")
```

The `QueryBuilder` supports three chaining methods: `.filter()`, `.where()`, and `.fields()`. Each returns `self`, so calls compose freely.

### Filtering with `.filter()`

`.filter()` accepts a positional dict (supports dotted keys for nested fields) and/or keyword arguments (convenience for top-level scalars). On collision, kwargs win.

```python
# Dotted-key dict for nested fields (canonical form)
qb = ds.query(OntapVolume, cluster="prod1").filter({"svm.name": "vs1"})

# Keyword arguments for top-level fields
qb = ds.query(OntapVolume, cluster="prod1").filter(state="online")

# Both together
qb = ds.query(OntapVolume, cluster="prod1").filter(
    {"svm.name": "vs1", "autosize.mode": "grow"},
    state="online",
)
```

!!! note "Dotted keys, not dunder"
    `DataSource` uses dotted-string keys (`"svm.name"`) in filter dicts instead of the `svm__name` dunder syntax used by `QuerySet`. Top-level scalar kwargs like `state="online"` work the same in both.

### SQL-like Expressions with `.where()`

`.where()` accepts one or more string expressions that support comparison operators beyond simple equality. Expressions are ANDed together with any `.filter()` entries.

```python
large_vols = ds.query(OntapVolume, cluster="prod1", source="cache").where(
    "size > 1000000000",
    "state != 'offline'",
)
for vol in large_vols:
    print(vol.name, vol.size)
```

!!! warning "Cache-only"
    `.where()` expressions are evaluated by the cache query engine and are only supported when the routing decision uses the cache path. Use `source="cache"` to opt in explicitly. Combining `.where()` with `source="live"` raises `NotImplementedError` at iteration time.

### Field Projection with `.fields()`

`.fields()` restricts which fields are populated on the returned models. Use it to reduce response size and parsing cost on large collections.

```python
qb = ds.query(OntapVolume, cluster="prod1").filter(state="online").fields(
    "name", "uuid", "size",
)
```

Fields not included in the projection fall back to their model defaults (`""`, `0`, `False`, etc.).

### Chaining

All three methods compose in any order. Multiple `.filter()` and `.where()` calls accumulate; `.fields()` replaces any previously set projection.

```python
results = list(
    ds.query(OntapVolume, cluster="prod1", source="cache")
    .filter({"svm.name": "vs1"})
    .where("size > 500000000")
    .fields("name", "size", "state")
)
```

### Iterating Results

`QueryBuilder` implements `__iter__`, so you can use it directly in a `for` loop or wrap it with `list()` to collect all results.

```python
# Iterate lazily
for vol in ds.query(OntapVolume, cluster="prod1").filter(state="online"):
    process(vol)

# Collect into a list
all_vols = list(ds.query(OntapVolume, cluster="prod1"))
```

## Fetching a Single Instance

`DataSource.get()` fetches one model instance by its identifier. It returns `T | None` -- `None` if no match exists.

### Single-Key Models

Most models have a single identifier field (typically `uuid`).

```python
vol = ds.get(OntapVolume, cluster="prod1", id="abc-123-def")
if vol is not None:
    print(vol.name)
```

### Composite-Key Models

Some models have composite identifiers. Pass `id=` as a dict containing all required key fields.

```python
from pynetappfoundry.models.ontap.networking.ip.interfaces.model import OntapIpInterface

lif = ds.get(
    OntapIpInterface,
    cluster="prod1",
    id={"svm_name": "vs1", "name": "lif1"},
)
```

### Field Projection on `.get()`

Like `.query()`, `.get()` accepts an optional `fields=` parameter.

```python
vol = ds.get(
    OntapVolume, cluster="prod1", id="abc-123-def",
    fields=["name", "size", "state"],
)
```

## Source Modes

Every `DataSource` method accepts a `source=` parameter that controls where data is read from. The type is `SourceMode`, a literal union of three strings.

| Mode | Behavior | When to use |
|------|----------|-------------|
| `"auto"` (default) | Serves cached and derived fields from cache; fetches realtime and `requires_explicit_fetch` fields live only when explicitly named in `fields=` | General-purpose reads |
| `"cache"` | Forces all requested fields through the cache; raises `ValueError` if any field is realtime-only | Fast, deterministic reads against local data |
| `"live"` | Forces all requested fields through the live REST API; raises `ValueError` if any field is derived (derived fields exist only in cache) | Fresh data from the cluster, bypassing cache |

```python
# Default: auto-routing based on field metadata
vol = ds.get(OntapVolume, cluster="prod1", id="abc-123-def")

# Cache-only: fast, no network calls
vol = ds.get(OntapVolume, cluster="prod1", id="abc-123-def", source="cache")

# Live: bypass cache entirely
vol = ds.get(OntapVolume, cluster="prod1", id="abc-123-def", source="live")
```

!!! note "Relationship to CLI --live"
    The `--live` flag on CLI commands like `nf cache check` sets `source="live"` internally. Note that `--live` and `--where` are mutually exclusive on `nf cache check` because `.where()` expressions only work on cached data.

## Common Patterns

### Counting Results

Wrap a query in `list()` and take the length, or use a generator expression.

```python
count = sum(1 for _ in ds.query(OntapVolume, cluster="prod1").filter(state="online"))
```

### Existence Check

```python
has_offline = any(
    True for _ in ds.query(OntapVolume, cluster="prod1").filter(state="offline")
)
```

### Error Handling

`DataSource` raises `ValueError` for unregistered models, missing identifiers, and impossible source-mode combinations (e.g. requesting a realtime field with `source="cache"`).

```python
try:
    vol = ds.get(OntapVolume, cluster="prod1", id="bad-uuid", source="cache")
except ValueError as exc:
    print(f"Configuration error: {exc}")
```

## See Also

- [ADR-0012: Unified DataSource accessor](../decisions/0012-unified-datasource-accessor.md) -- design rationale and implementation phases
- [Query Layer](query-layer.md) -- `QuerySet`, `Mutation`, `JobTracker`, relationship traversal, and realtime functions
- [ONTAP Access Patterns](ontap-access-patterns.md) -- decision matrix for choosing between access surfaces
