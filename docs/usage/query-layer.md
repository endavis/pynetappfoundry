---
title: Query Layer
description: Guide to the REST query layer (QuerySet, Query, Mutation, JobTracker, related, realtime)
audience:
  - users
  - contributors
tags:
  - ontap
  - api
  - query
  - mutation
  - realtime
---

!!! note "Prefer DataSource for new code"
    `DataSource` is the recommended entry point for reading cluster data.
    It routes reads through cache or live API based on the `source=` parameter
    and supports `.filter()`, `.where()`, and `.fields()` chaining.
    See the [DataSource guide](data-source.md) for details.

    `QuerySet` remains available as the lower-level REST query surface
    used internally by `DataSource` and for direct REST operations
    (mutations, job tracking, relationship traversal) that `DataSource`
    does not cover.

# Query Layer

`pynetappfoundry.query` is a thin, fluent layer on top of the ONTAP REST API client. It uses the same declarative `TypeMapping` metadata that drives the cache (see [ADR-0004](../decisions/0004-declarative-field-mapping-framework.md)) to translate model attribute names into API field paths and to parse responses back into Pydantic model instances.

The layer ships six public surfaces:

- `QuerySet` — fluent, lazy reads for collection-style GET endpoints
- `Query` — RPC-style POST reads for endpoints that accept a request body and return data
- `Mutation` — POST / PATCH / DELETE writes
- `JobTracker` (and `JobError`) — polling for async ONTAP jobs
- `related` / `related_one` — relationship-traversal sugar over `QuerySet`
- `fetch_realtime`, `fetch_realtime_collection`, `watch_realtime`, `compare_realtime` — on-demand access to fields marked `cache_strategy="realtime"`

## Overview

| Use case | Use this |
|----------|----------|
| Type-safe ad-hoc reads with filters / projection / ordering | `QuerySet` |
| Call a POST endpoint that returns data instead of mutating state | `Query` |
| Create / update / delete a resource | `Mutation` |
| Wait for an async ONTAP job | `JobTracker` (or `poll=True` shortcut on `Mutation`) |
| Express "fetch related X for this Y" intent | `related` / `related_one` |
| Read fields excluded from the cache (IOPS, latency, ...) | `fetch_realtime` family |

!!! note "TypeMappings are auto-registered"
    Every entry point in this module looks the model class up in the model registry. Mappings are auto-registered: the first registry lookup triggers the `cache` package import, which walks `cache/ontap/**/mapping.py` and registers every `TypeMapping`. If you see `ValueError: No TypeMapping registered for 'OntapXxx'`, verify that a `mapping.py` module exists under `cache/ontap/` for the model in question.

For the wider context of when to use the query layer instead of `ClusterEntry.ontap`, see the [decision section](#combining-with-clusterentryontap) below and the [ONTAP Access Patterns](ontap-access-patterns.md) guide.

## QuerySet Reads

`QuerySet` is a lazy, chainable query builder. Each chaining call returns a **new** `QuerySet` (cloned filters/fields/ordering/limit), so you can safely fork a base query.

```python
from pynetappfoundry.clients.ontap.api import ONTAPAPIClient
from pynetappfoundry.core.config import Config
from pynetappfoundry.models.ontap.storage.volumes.model import OntapVolume
from pynetappfoundry.query import QuerySet

config = Config()
cluster = config.clusters["mycluster"]
client = ONTAPAPIClient(cluster, config)

base = QuerySet(OntapVolume, client).filter(state="online")
```

### Filtering: `.filter(**kwargs)`

`.filter()` accepts model attribute names as keyword arguments. Each key is translated to an API field path via two lookup strategies, in order:

1. **Exact `cache_attr` match.** If the model's `TypeMapping` has a `FieldMapping` whose `cache_attr` equals the kwarg name, the corresponding `api_path` is used. For example, if `cache_attr="name"` then `name="vol1"` becomes `name=vol1`. Dotted `cache_attr` values (e.g. `svm.name`, `autosize.mode`) must be passed via `**{}` syntax since Python kwargs cannot contain `.`.
2. **Pass-through.** If no mapping match is found, the attribute name is sent to the API verbatim. This lets you use raw API field paths when you know what you want.

```python
# Dotted cache_attr via dict-splat (the common ONTAP case)
qs = QuerySet(OntapVolume, client, config=config).filter(**{"svm.name": "vs1", "autosize.mode": "grow"})

# Top-level cache_attr (state, name, uuid, size all exist on OntapVolume)
qs = QuerySet(OntapVolume, client, config=config).filter(state="online")

# Raw API field path (pass-through)
qs = QuerySet(OntapVolume, client, config=config).filter(**{"space.size": 1073741824})
```

!!! warning "Filtering is server-side; wildcards are an ONTAP feature"
    Values are sent verbatim to ONTAP. Wildcard semantics (e.g. `name="*_backup"`) are interpreted by the ONTAP REST API itself, not by `QuerySet`. Refer to the ONTAP REST documentation for the supported syntax for the field you are filtering on.

### Projection: `.fields(*names)`

`.fields()` overrides the default `fields=*` projection that the `TypeMapping` ships in `api_endpoint`. Names are translated using the same logic as `.filter()` (cache_attr, then dunder, then pass-through).

```python
qs = (
    QuerySet(OntapVolume, client)
    .filter(svm__name="vs1")
    .fields("name", "uuid", "size", "state")
)
```

Use projection on large collections to reduce response size and parsing cost.

### Ordering: `.order_by(*specs)`

Each spec is an attribute name optionally followed by a space and `asc` or `desc`. The attribute portion is translated; the suffix is preserved as-is.

```python
QuerySet(OntapVolume, client).order_by("name asc", "size desc")
```

### Limiting: `.limit(n)`

`.limit(n)` sets the `max_records` query parameter.

```python
QuerySet(OntapVolume, client).filter(state="online").limit(50)
```

### Terminal methods

| Method | Returns | Notes |
|--------|---------|-------|
| `.all()` | `list[Model]` | Executes the query, paginates via `client.get_all_records`, parses every record into a model instance. |
| `.first()` | `Model \| None` | Equivalent to `.limit(1).all()[0]` (or `None`). |
| `.get(**kwargs)` | `Model` | Convenience for `.filter(**kwargs).all()` that **must** return exactly one row. Raises `NotFoundError` for zero rows or `MultipleResultsError` for more than one. |
| `.count()` | `int` | Issues the query with `return_records=false` and reads `num_records` from the response. Does not fetch records. |
| `iter(qs)` | iterator | `__iter__` calls `.all()` once and yields its contents. |

```python
from pynetappfoundry.query import MultipleResultsError, NotFoundError

# All matching volumes, projected and ordered
volumes = (
    QuerySet(OntapVolume, client)
    .filter(svm__name="vs1", state="online")
    .fields("name", "uuid", "size")
    .order_by("name asc")
    .limit(50)
    .all()
)

# Exactly one (raises if zero or many)
try:
    vol = QuerySet(OntapVolume, client).get(uuid="abc-123-def")
except NotFoundError:
    print("No such volume")
except MultipleResultsError as exc:
    print(f"Ambiguous filter, got {exc.count} rows")

# Count without fetching records
total = QuerySet(OntapVolume, client).filter(state="online").count()
```

!!! note "Server-side filter vs. cache query engine"
    For complex predicates (`autosize.mode != 'grow_shrink'`, ranges, NOT, OR), the cache SQL query engine — used by `nf cache check` and `nf cache compliance` — is usually a better fit because it operates on the local SQLite cache without round-tripping to the cluster. `QuerySet` is the right tool when you want live data, single-cluster access, and the simple equality / wildcard semantics that ONTAP REST exposes natively.

    `nf cache check` also supports a `--live` flag that bypasses the cache and fetches data directly from each cluster via `DataSource(source="live")`. Note that `--live` and `--where` are mutually exclusive — SQL-like filter expressions are only supported on cached data.

## Query RPC Reads

`Query` is the lightweight companion to `Mutation` for endpoints that use POST as a query transport rather than as a write. It binds a client plus a fixed path, then forwards a JSON body to that path and returns the raw response payload.

```python
from pynetappfoundry.query import Query

q = Query(client, "/lake/query/timeseries")
results = q.invoke({"metric": "cpu", "interval": "1h"})
```

Use `Query` when the remote API expects a structured POST body for a read-style operation (for example, RPC-style analytics endpoints). Unlike `QuerySet`, it does not translate model fields or parse Pydantic models; unlike `Mutation`, it does not imply resource creation or lifecycle changes.

## Mutation Writes

`Mutation` wraps the same `TypeMapping` to translate flat model-attribute kwargs into the nested JSON body that ONTAP REST expects.

```python
from pynetappfoundry.query import Mutation

m = Mutation(OntapVolume, client)
```

### `.create(**kwargs)`

POST to the collection endpoint. Body construction calls `_attr_to_api_path` for every kwarg and merges sibling dotted paths into nested dicts (so `svm__name="vs1"` and `svm__uuid="..."` both become children of a single `svm` object).

POST is non-idempotent, so retry is **disabled** for `.create()` (`RetryConfig(enabled=False)`).

```python
new_vol = m.create(
    name="vol1",
    svm__name="vs1",
    size=1073741824,
)
```

### `.update(uuid, **kwargs)`

PATCH against `<collection>/<uuid>` with the same flat-to-nested body translation. PATCH uses the client's default retry behavior.

```python
m.update("abc-123-def", size=2147483648, state="offline")
```

### `.delete(uuid, **kwargs)`

DELETE against `<collection>/<uuid>`. Optional kwargs become a body (e.g. for force flags accepted by certain ONTAP endpoints).

```python
m.delete("abc-123-def")
```

### Return value parsing

`.create()` and `.update()` parse the API response back into a model instance when the response looks like a record (i.e. it contains at least one top-level key that the `TypeMapping` knows about). For 202-style async responses (`{"job": {...}}`) the raw dict is returned — see the next section for how to track the job.

## Async Job Tracking

Many ONTAP write endpoints return HTTP 202 with a job descriptor instead of the resource itself. The query layer offers two ways to wait for completion.

### Shortcut: `poll=True` on `Mutation`

`Mutation.create()` and `.update()` accept three keyword-only arguments to handle the job inline:

| Kwarg | Default | Purpose |
|-------|---------|---------|
| `poll` | `False` | When `True` and the response contains `job`, build a `JobTracker` and call `.wait()`. |
| `poll_interval` | `5` (seconds) | Delay between polls. |
| `poll_timeout` | `300` (seconds) | Maximum wall-clock wait before raising `TimeoutError`. |

When `poll=True` actually fires, the return value is the completed `OntapJob`, not a parsed resource model.

```python
from pynetappfoundry.query import JobError

try:
    job = m.create(
        poll=True,
        poll_interval=5,
        poll_timeout=300,
        name="vol1",
        svm__name="vs1",
        size=1073741824,
    )
    print(f"Job {job.uuid} state={job.state}")
except JobError as exc:
    print(f"Volume create failed: {exc.message} (code={exc.error_code})")
except TimeoutError as exc:
    print(f"Gave up waiting: {exc}")
```

### Manual: `JobTracker.from_response`

For finer control (non-blocking polls, custom retry, surfacing intermediate state), use `JobTracker` directly.

```python
from pynetappfoundry.query import JobError, JobTracker

response = m.create(name="vol1", svm__name="vs1", size=1073741824)
if isinstance(response, dict) and "job" in response:
    tracker = JobTracker.from_response(response, client, poll_interval=2, poll_timeout=120)

    # Single non-blocking poll
    snapshot = tracker.poll()
    print(f"Current state: {snapshot.state}")
    print(f"Terminal? {tracker.is_complete}")

    # Or block until terminal
    try:
        final = tracker.wait()
        print(f"Job {final.uuid} succeeded")
    except JobError as exc:
        # exc.job is the failed OntapJob; exc.message and exc.error_code are populated
        print(f"Job failed: {exc.message}")
```

`JobTracker.from_response` raises `ValueError` if the response dict has no `job.uuid`. `JobTracker.wait()` raises `JobError` on terminal `failure` and `TimeoutError` if `poll_timeout` elapses without the job reaching `success` or `failure`.

The `is_complete` property reports whether the **last polled** job state was terminal (`success` or `failure`); it returns `False` until you have polled at least once.

## Relationship Traversal

`related()` and `related_one()` are thin wrappers that express relationship-traversal intent more clearly than a raw `QuerySet().filter().all()` chain. Both **require** at least one filter kwarg and raise `ValueError` if called with none.

```python
from pynetappfoundry.models.ontap.storage.volumes.model import OntapVolume
from pynetappfoundry.models.ontap.svm.svms.model import OntapSvm
from pynetappfoundry.query import related, related_one

# Many: all volumes for an SVM
vols = related(OntapVolume, client, svm__uuid="abc-123")

# One-to-one: the SVM for a known UUID
svm = related_one(OntapSvm, client, uuid="svm-uuid-123")
```

`related(...)` is exactly `QuerySet(model, client).filter(**kwargs).all()`. `related_one(...)` is `.filter(**kwargs).first()`. Use them when the call site is clearly traversing a relationship; reach for `QuerySet` directly when you also need projection, ordering, or limiting.

## Realtime Fields

ONTAP exposes per-resource counters (IOPS, latency, throughput, deduplication savings, ...) that are too volatile to cache. The `cache.field_mapping.FieldMapping` framework marks these with `cache_strategy="realtime"`, which excludes them from bulk cache collection and surfaces them via `TypeMapping.realtime_fields()`. The four functions in `pynetappfoundry.query.realtime` are how you read those values on demand.

All four functions resolve the model's `TypeMapping`, optionally filter the realtime field set down to a `fields=` whitelist (matched on `cache_attr`), and project a request that asks ONTAP only for the top-level API keys actually needed.

### `fetch_realtime(model_class, config, cluster, uuid, fields=None)`

Fetch current realtime values for a single resource by UUID. Returns the Pydantic model instance directly (or ``None`` when the resource is not found). Routes through ``DataSource.get(..., source="live")``.

```python
from pynetappfoundry.core.config import Config
from pynetappfoundry.query import fetch_realtime

config = Config()
instance = fetch_realtime(
    OntapVolume,
    config,
    cluster="prod-cluster",
    uuid="abc-123-def",
    fields=["metric.iops.read", "metric.iops.write", "metric.latency.read"],
)
if instance is not None:
    print(instance.metric.iops.read, instance.metric.iops.write)
```

If the model has no realtime fields (or none survive the `fields=` filter), the function returns ``None`` without making a request.

### `fetch_realtime_collection(model_class, config, cluster, fields=None, **filters)`

Fetch realtime values for many resources in one request. `**filters` are translated via the same `cache_attr` lookup used elsewhere — pass dotted API paths as `**{"svm.name": "vs1"}` if you need them. The response always includes `uuid` and `name` for identification. Routes through `DataSource.query(..., source="live")`.

```python
from pynetappfoundry.query import fetch_realtime_collection

rows = fetch_realtime_collection(
    OntapVolume,
    config,
    cluster="prod-cluster",
    fields=["metric.iops.read", "metric.iops.write"],
    state="online",
)
for row in rows:
    print(row["name"], row["metric.iops.read"], row["metric.iops.write"])
```

### `watch_realtime(model_class, config, cluster, uuid, fields=None, interval=5, count=None)`

Generator that polls realtime values in a loop, adding an ISO-8601 UTC `_timestamp` key to each yielded dict. `count=None` runs forever; pass an integer to stop after N samples. `interval` is seconds between polls. A single `DataSource` is constructed before the loop and reused across iterations.

```python
from pynetappfoundry.query import watch_realtime

for snapshot in watch_realtime(
    OntapVolume,
    config,
    cluster="prod-cluster",
    uuid="abc-123-def",
    fields=["metric.iops.read"],
    interval=10,
    count=3,
):
    print(snapshot["_timestamp"], snapshot["metric.iops.read"])
```

### `compare_realtime(model_class, config, cluster, uuid, baseline, fields=None)`

Fetches the current realtime values and diffs them against a `baseline` dict (typically captured earlier with `fetch_realtime`). For numeric values, the result includes `baseline`, `current`, and `delta`. For non-numeric values, only `baseline` and `current`. Fields present in `current` but absent from `baseline` get a `current`-only entry.

```python
from pynetappfoundry.query import compare_realtime, fetch_realtime

baseline = fetch_realtime(
    OntapVolume, config, cluster="prod-cluster", uuid="abc-123-def",
    fields=["metric.iops.read", "metric.iops.write"],
)
# ... time passes, workload runs ...
diff = compare_realtime(
    OntapVolume, config, cluster="prod-cluster", uuid="abc-123-def",
    baseline=baseline,
    fields=["metric.iops.read", "metric.iops.write"],
)
print(diff["metric.iops.read"]["delta"])
```

## Combining with `ClusterEntry.ontap`

The query layer and `ClusterEntry.ontap` are complementary, not competing:

- Use **`cluster_entry.ontap`** for high-level reads of cached cluster metadata field groups (licenses, nodes, storage, network, ...). It serves sub-millisecond SQLite reads when the cache is populated and falls back to a live `DataSource` fetch on a miss. `--live` (`Config(no_cache=True)`) bypasses the cache without changing call sites.
- Use **`QuerySet`** for ad-hoc reads that don't fit a pre-defined field group: arbitrary filters, custom projections, ordering / limit, or models the cache does not collect.
- Use **`Query`** for RPC-style POST endpoints that return data rather than mutate resources.
- Use **`Mutation`** for any write. There is no write surface on `ClusterEntry.ontap`.
- Use **`fetch_realtime`** (and friends) for fields the cache deliberately excludes.

For the full decision matrix, see [ONTAP Access Patterns](ontap-access-patterns.md).

## Exceptions Reference

| Exception | Raised by | Meaning |
|-----------|-----------|---------|
| `NotFoundError` | `QuerySet.get()` | Filter matched zero rows. |
| `MultipleResultsError` | `QuerySet.get()` | Filter matched more than one row; the count is on `exc.count`. |
| `JobError` | `JobTracker.wait()` (and `Mutation` with `poll=True`) | The polled `OntapJob` reached the `failure` state. The failed job is on `exc.job`; `exc.message` and `exc.error_code` mirror the job's error fields. |
| `TimeoutError` | `JobTracker.wait()` (and `Mutation` with `poll=True`) | `poll_timeout` elapsed without the job reaching a terminal state. |
| `ValueError` | `QuerySet`, `Mutation`, `JobTracker.from_response`, `related`, `related_one`, the realtime functions | The model class has no registered `TypeMapping`, the API response has no `job.uuid`, or `related`/`related_one` was called without filter kwargs. |

`NotFoundError` and `MultipleResultsError` live in `pynetappfoundry.query.exceptions` and are also re-exported from `pynetappfoundry.query`.

## See Also

- [ONTAP Access Patterns](ontap-access-patterns.md) — when to use `ClusterEntry.ontap` vs. the query layer vs. the SDK vs. SSH.
- [ADR-0010: ClusterEntry and namespace access pattern](../decisions/0010-clusterentry-and-namespace-access-pattern.md) — rationale for the cache-first read namespace.
- [ADR-0004: Declarative field mapping framework](../decisions/0004-declarative-field-mapping-framework.md) — the `FieldMapping` / `TypeMapping` model that the query layer reads from.
