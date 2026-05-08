---
title: Cache System
description: Architecture, storage layout, lazy loading, and CLI for the cluster metadata cache
audience:
  - users
  - contributors
tags:
  - reference
  - cache
  - sqlite
  - ontap
---

# Cache System

The cache system stores ONTAP cluster metadata locally so that lookups, reports,
and queries can run without re-hitting every cluster on every command. This
document covers the cache architecture, the per-model SQL storage layout,
schema versioning and migrations, lazy loading with on-demand fetch, the field
mapping framework, the OpenAPI codegen pipeline, history tracking, the CLI,
and the public API.

## Overview

The cache system is composed of three storage layers and three runtime
components:

1. **`ClusterMetadataDB`** — Per-model SQLite tables holding the current
   cached snapshot for each cluster (see [Storage Architecture](#storage-architecture)).
2. **`CacheHistoryDB`** — Append-only history of changes between snapshots,
   stored in a separate SQLite file for data isolation.
3. **`MetadataCollector`** — All-or-nothing collector that pulls metadata from
   ONTAP REST and (optionally) the CLI and produces a `CachedClusterMetadata`.
4. **`LazyClusterMetadata`** — Lazy proxy returned by
   `ClusterMetadataDB.get_lazy()`. Defers per-field-group SQL queries until
   the caller actually touches a data attribute.
5. **`DataSource`** — Unified accessor that routes field-group reads through
   the cache or live ONTAP API as appropriate.
6. **Field mapping framework (`FieldMapping` / `TypeMapping`)** — Declarative
   metadata that drives both the collector (what to fetch, what to persist)
   and the codegen pipeline.

```
                                    +----------------------+
+-----------------+                 |  ClusterMetadataDB   |
|  ONTAP Cluster  |--+              |  (per-model tables)  |
+-----------------+  |              |                      |
                     |  +---------+ |  envelope            |
                     +->|Collector|>|  + ontapvolume       |
                     |  +---------+ |  + ontapsvm          |
                     |              |  + ontapipinterface  |
                     |              |  + ...               |
                     |              +----------+-----------+
                     |                         |
                     |              +----------v-----------+
                     |              |  LazyClusterMetadata |
                     |              |  (per-field-group    |
                     |              |   deferred load)     |
                     |              +----------+-----------+
                     |                         | cache miss
                     |              +----------v-----------+
                     +------------->|  DataSource          |
                                    |  (live API fallback) |
                                    +----------------------+
```

## Database Files

Both databases are SQLite files stored in the user's config directory:

| Database | File | Purpose |
|----------|------|---------|
| `ClusterMetadataDB` | `{config_dir}/.cache/cluster_metadata.db` | Current per-cluster snapshot |
| `CacheHistoryDB` | `{config_dir}/.cache/cache_history.db` | Append-only change history |

!!! info "User-facing access guide"
    For a task-oriented walkthrough of the three ONTAP access patterns
    (cache, lazy proxy, live), see
    [ONTAP Access Patterns](../usage/ontap-access-patterns.md).

## Storage Architecture

The cache database is **not** a single JSON blob. Per ADR-0009, each storable
Pydantic model in `CachedClusterMetadata` gets its own SQLite table, generated
at import time from the model's field definitions.

### Table registry

`ClusterMetadataDB` builds a `TABLE_REGISTRY` (`db.py:_ensure_registry`) by
walking `CachedClusterMetadata.model_fields`
(`db_schema.build_table_registry`):

- `list[Model]` fields at the top level (e.g. `nodes`, `cloud`,
  `license_packages`) become a single table per item type.
- Singleton `Model` fields that contain only scalars (e.g. `cluster`,
  `mediator`) become a singleton table.
- Container models with `list[Model]` sub-fields (e.g. `StorageInfo`,
  `NetworkInfo`, `ProtocolsInfo`, `RelationshipsInfo`) are **not** stored as
  tables themselves. The walker descends into them and registers each list
  child as its own table. The container is only registered as a singleton if
  it has additional non-list scalar fields (e.g. `NetworkInfo.ipspaces:
  list[str]`).

Each entry in the registry is a `TableSpec` with the SQL table name (the
lowercased model class name), the model class, the dot-path on
`CachedClusterMetadata` (e.g. `"storage.volumes"`), an `is_list` flag, and a
`has_uuid` flag.

### Envelope table

A small fixed envelope table holds one row per cluster with the cache
metadata. This is the entry point used by `get`, `get_lazy`, `is_stale`,
`list_clusters`, and `get_status` (which need only the envelope, not the full
data set):

```sql
CREATE TABLE cluster_metadata (
    cluster_name TEXT PRIMARY KEY,
    cached_at TEXT NOT NULL,
    cache_version TEXT NOT NULL
)
```

### Per-model table layout

Per-model tables are generated by `db_schema.generate_table_ddl()`. Each table
has:

- A `cluster_name TEXT NOT NULL` column (omitted if the model itself defines
  `cluster_name`).
- An auto-incrementing `_row_id INTEGER PRIMARY KEY AUTOINCREMENT`.
- One column per Pydantic field, quoted to dodge SQLite reserved words. SQL
  types are derived from the Python annotation: `str` and `OntapUUID` →
  `TEXT`, `int` and `bool` → `INTEGER`, `float` → `REAL`, `datetime` → `TEXT`,
  and any `list`, `dict`, or nested `BaseModel` field → `TEXT` storing JSON.
- An `_extra_json TEXT DEFAULT NULL` column at the end that captures
  `extra="allow"` fields from newer ONTAP versions for forward compatibility.

Two indices are created per table: `idx_{table}_cluster` on `cluster_name`
(always), and `idx_{table}_uuid` on `(cluster_name, uuid)` if the model has a
`uuid` field.

!!! note "Why `_row_id` is the primary key"
    Many ONTAP objects have empty or missing UUIDs in test fixtures and on
    fresh clusters. Using a synthetic auto-increment PK avoids unique-key
    collisions and lets the cache store multiple anonymous rows per cluster
    without ad-hoc disambiguation.

### Read and write paths

- **Write** (`set`): the envelope row is upserted, then `_delete_model_data`
  clears all per-cluster rows from every model table inside a single
  transaction, then `_insert_model_data` walks the registry and inserts new
  rows for each table. Each row goes through `_model_to_row` which serialises
  list/dict/sub-model fields to JSON, coerces booleans to `0/1`, and
  collects extra fields into `_extra_json`.
- **Read** (`get` / `get_lazy`): the envelope row is fetched first.
  `get` then calls `_reconstruct_metadata`, which delegates to
  `_query_registry_subset` to query every table and rebuild the full
  `CachedClusterMetadata`. `get_lazy` skips the data queries entirely and
  returns a [`LazyClusterMetadata`](#lazy-loading-and-on-demand-fetch) proxy.
- **Query** (`query_model`, `query_with_filters`): targeted SQL against a
  single per-model table. See [Public API Reference](#public-api-reference).

## Schema Versioning and Migrations

Two version constants live in `cache/_base.py`:

```python
METADATA_SCHEMA_VERSION = "2.0"        # current cache_version on new snapshots
METADATA_SCHEMA_MIN_COMPATIBLE = "2.0" # oldest version that can be loaded
```

`METADATA_SCHEMA_VERSION` is the data-model version stamped into each
snapshot's envelope row as `cache_version`. The `MAJOR.MINOR` format follows
semantic versioning: bump MINOR for backward-compatible additions (new
optional fields), bump MAJOR for breaking changes (removed/renamed fields,
type changes).

`is_schema_compatible(snapshot_version)` returns `True` only if the snapshot
is at or above `METADATA_SCHEMA_MIN_COMPATIBLE`. When the cache layer loads a
historical snapshot it uses this check to decide whether the snapshot can be
deserialised against the current Pydantic models.

### Snapshot schema version history

| `cache_version` | Changes |
|-----------------|---------|
| `2.0` | Renamed cache fields to match the ONTAP REST URL hierarchy: `network.lifs` → `network.ip_interfaces`, `network.broadcast_domains` → `network.ethernet_broadcast_domains`, `network.subnets` → `network.ip_subnets`, `protocols.export_policies` → `protocols.nfs_export_policies`. |
| `1.0` | Initial schema with comprehensive model coverage. |

### SQLite database schema versioning

The contract for what migrations may do — additive vs. destructive, downgrade
behavior, visibility — is recorded in
[ADR-0018](../decisions/0018-cache-schema-versioning-and-backward-compatibility-policy.md).
The cache is rebuild-tolerant: destructive migrations are allowed, and
`nf cache refresh` is the documented fallback.

In addition to the `cache_version` stamped into each snapshot,
`ClusterMetadataDB` tracks the **on-disk SQLite schema** version through the
shared `SQLiteDB` base class. The current value is `SCHEMA_VERSION = 4`, and
the DB applies the following upgrades on open:

| DB schema | Migration | What it does |
|-----------|-----------|--------------|
| `v1` → `v2` | `_upgrade_to_v2` | Reads the old `metadata_json` blob, decomposes each cluster into per-model tables (ADR-0009), then drops the JSON column from the envelope table. |
| `v2` → `v3` | `_upgrade_to_v3` | Drops the unused `_uuid_index` table. UUID resolution moved to the in-memory `CachedClusterMetadata.uuid_index` cached property (ADR-0005). |
| `v3` → `v4` | `_upgrade_to_v4` | Drops and recreates every per-model table to switch column names from the old flat naming (`ip_address`) to the new nested-model layout (`ip` stored as JSON), per ADR-0011. The envelope is cleared so callers detect a missing snapshot and trigger a fresh collection. |

!!! warning "v3 → v4 is destructive"
    The v4 migration deletes existing cached rows. After upgrading,
    `nf cache refresh` (or `--all`) must be run to repopulate the cache.

## Lazy Loading and On-Demand Fetch

Loading the full `CachedClusterMetadata` requires hitting every per-model
table. For commands that only need one slice of the data (e.g. just
`storage.volumes`), this is wasteful. `LazyClusterMetadata` defers the SQL
queries until the caller actually touches a data attribute.

### `LazyClusterMetadata`

Returned by `ClusterMetadataDB.get_lazy(cluster_name)`. The proxy is **not** a
Pydantic model — it is a thin object stored in `__slots__` with three
envelope properties (`cluster_name`, `cached_at`, `cache_version`) populated
eagerly from the envelope row, plus a `_loaded` cache for materialised field
groups.

The nine top-level data field names — `cloud`, `cluster`, `nodes`, `network`,
`storage`, `license_packages`, `mediator`, `relationships`, `protocols` —
form `_DATA_FIELDS`. Access goes through `__getattr__`, which calls
`_load_field_group(name)` on first read and caches the result for subsequent
reads.

### `_load_field_group` fallback chain

`_load_field_group` tries two sources in order and returns the first one
that produces a value:

1. **DataSource** — per-model routing through `DataSource.query(source="cache")`
   for every registry entry in the field group. Skipped when no `config` is
   available.
2. **Model default** (`_get_default`). Returns the
   `CachedClusterMetadata.model_fields[name]` default factory (or `default`),
   so callers get an empty container instead of `None`.

If the resolved value is a plain `dict` and the target field is a nested
Pydantic container, it is validated via `model_class.model_validate(value)`
before being cached.

### Materialisation

Calling `_materialize()` forces all nine field groups to load and returns a
real `CachedClusterMetadata`. The `to_flat_dict`, `uuid_index`, `model_dump`,
and `model_dump_json` methods on the proxy go through `_materialize()`, so
using any of them triggers a full load.

`is_stale(ttl_days=30)` is the only delegated method that does **not**
materialise — it computes age from the envelope `cached_at` directly.

!!! info "User-facing equivalent"
    The user-facing guide for choosing between `get`, `get_lazy`, and the
    direct API client lives in
    [ONTAP Access Patterns](../usage/ontap-access-patterns.md).

## Field Mapping Framework

The collector and the cache write path are both driven by **field mappings**
(see ADR-0004). Each ONTAP object type has a `TypeMapping` and one
`FieldMapping` per model attribute. The full developer guide lives in
[Field Mapping Framework](../development/field-mapping.md) and the user-facing
query syntax in [Query Layer](../usage/query-layer.md). This section covers
only the cache-relevant aspects.

`FieldMapping` carries a `cache_strategy` literal that controls how the
collector and cache treat the field:

| Strategy | Collected during bulk refresh | Persisted to SQLite | Notes |
|----------|------------------------------|---------------------|-------|
| `"cache"` (default) | Yes | Yes | Standard cached field. |
| `"realtime"` | No | No | Skipped on cache write, fetched live per-object on demand. |
| `"derived"` | No directly | Yes (after post-collection) | Computed from other fields by `post_collection` callbacks once all phases finish. |

`TypeMapping` exposes three convenience accessors backed by these flags:

- `cached_fields()` — fields with `cache_strategy="cache"`.
- `realtime_fields()` — fields with `cache_strategy="realtime"`.
- `derived_fields()` — fields with `cache_strategy="derived"`.

The collector uses `parse_api_record(..., skip_realtime=True)` to drop
realtime and derived fields when building model instances destined for the
cache, so volatile metrics never leave the live API path.

## Realtime Field Handling

`cache_strategy="realtime"` means a field is excluded **at the database write
boundary**. The exclusion path is:

1. `realtime_attrs(model_class)` (`db.py`) calls
   `model_registry.get_mapping(model_class.__name__)` and returns the set of
   `cache_attr` names whose mapping has `cache_strategy="realtime"`. The
   result is `functools.cache`-memoised per class.
2. `_insert_model_data` looks up that set once per model spec and passes it
   as `exclude` to `_model_to_row` for every row.
3. `_model_to_row` checks `if field_name in exclude: continue` while
   building the row dict, so realtime fields never become SQL columns
   during INSERT.

A second helper, `all_realtime_attrs()`, returns the union across **every**
registered model — used elsewhere when a global filter is needed.

### Concrete example

If `OntapVolume` defines `space_used` with `cache_strategy="realtime"`:

- A `nf cache refresh` inserts an `ontapvolume` row with no value in the
  `space_used` column (the column still exists in the table — only the value
  is omitted at write time, so the row reads back as `None` and the field
  falls through to the model default on `_row_to_model`).
- A subsequent `db.get(...).storage.volumes[0].space_used` returns the model
  default (empty string / zero) unless a `LazyClusterMetadata` proxy backed
  by a `DataSource` is used to refresh the field live.

## OpenAPI Codegen Pipeline

Most `Ontap*Response` models in the [Model Reference](#model-reference) are
**generated** from the ONTAP OpenAPI 3.0 spec rather than written by hand.
The codegen tool lives at `tools/codegen/openapi_codegen.py`.

### Inputs and outputs

```bash
uv run python tools/codegen/openapi_codegen.py \
    --spec docs/example-config/apis/ontap/openapi3.json \
    --output src/pynetappfoundry/cache/ontap/ \
    --api-type ontap
```

- **Input**: an OpenAPI 3.0 JSON spec
  (`docs/example-config/apis/ontap/openapi3.json` for ONTAP).
- **Output**: per-endpoint module trees under
  `src/pynetappfoundry/cache/ontap/<api-path>/` containing a generated
  `model.py` (the Pydantic model class), `mapping.py` (the `TypeMapping` and
  `FieldMapping` definitions), and one or more `*.toml` overlay files for
  field strategy overrides.
- `--api-type` selects the API tag (`ontap`, `aiqum`, `dii`, `occm`).
- `--endpoints` filters generation to a specific list of paths.
- `--dry-run` prints the plan without writing files.

### Endpoint deduplication

Two OpenAPI endpoints frequently resolve to the same module path — for
example `/storage/volumes` (the list endpoint) and
`/storage/volumes/{uuid}` (the get-by-id endpoint) both map to
`storage/volumes`. `_deduplicate_endpoints` groups endpoints by their target
module path and keeps the candidate with the most leaf fields (the richer
schema), so the generated model is always the union view.

### Doit task wrapper

A doit task in `tools/doit/codegen.py` wraps the same entry point so the
codegen can be run via `doit` alongside the rest of the build. Run `doit
list` to discover the current task name.

## Nested Models Pattern

Per ADR-0011, all cache models use **nested sub-objects that mirror the
ONTAP REST API response shape** rather than flat attributes with dot-encoded
names. This means user code can write `iface.ip.address` instead of the older
`iface.ip_address`, matching the API documentation directly.

```python
# Before (flat)
class OntapSvmIpInterface(OntapModel):
    ip_address: str = ""
    ip_netmask: str = ""
    location_home_node_name: str = ""

# After (nested)
class OntapSvmIpInterface(OntapModel):
    class Ip(OntapModel):
        address: str = ""
        netmask: str = ""
    class Location(OntapModel):
        class HomeNode(OntapModel):
            name: str = ""
        home_node: HomeNode = HomeNode()
    ip: Ip = Ip()
    location: Location = Location()
```

### Cache-boundary translation

The cache layer is the only consumer that needs a flat representation. The
translation happens at the SQL boundary:

- **Write**: `_model_to_row` serialises each nested sub-model field to a JSON
  string in its own `TEXT` column (because `_is_json_column` returns `True`
  for `BaseModel` annotations).
- **Read**: `_row_to_model` reverses the process, parsing the JSON column
  back into a `dict` that Pydantic validates into the nested sub-model when
  reconstructing the parent model.

This is why the v3 → v4 migration drops and recreates every per-model table:
the column names changed from flat (`ip_address`) to nested
(`ip` storing JSON).

## CachedClusterMetadata Reference

The root cache container is `CachedClusterMetadata` (in
`cache/_metadata.py`). It carries three envelope fields and nine data field
groups:

```python
class CachedClusterMetadata(CacheModel):
    # Envelope
    cluster_name: str
    cached_at: datetime = Field(default_factory=_utcnow)
    cache_version: str = METADATA_SCHEMA_VERSION

    # Data field groups
    cloud: list[CloudMetadata] = Field(default_factory=list)
    cluster: ClusterInfo = Field(default_factory=ClusterInfo)
    nodes: list[OntapNodeResponse] = Field(default_factory=list)
    network: NetworkInfo = Field(default_factory=NetworkInfo)
    storage: StorageInfo = Field(default_factory=StorageInfo)
    license_packages: list[OntapLicensePackageResponse] = Field(default_factory=list)
    mediator: OntapMediatorResponse = Field(default_factory=OntapMediatorResponse)
    relationships: RelationshipsInfo = Field(default_factory=RelationshipsInfo)
    protocols: ProtocolsInfo = Field(default_factory=ProtocolsInfo)
```

`is_stale(ttl_days=30)` reports staleness from `cached_at`. `to_flat_dict()`
returns a flat dictionary of commonly-merged fields used by report and
template code paths.

### UUID cross-reference index

`CachedClusterMetadata.uuid_index` is a `cached_property` that builds a flat
`dict[str, HasUUID]` mapping UUID strings to their corresponding model
objects across all UUID-bearing types in the snapshot. This enables O(1)
resolution of foreign-key UUID references stored in cache objects.

```python
cached = cache_db.get("cluster-name")

# Resolve any UUID to its object regardless of type
obj = cached.uuid_index.get("53a08885-1d82-11ea-a91e-000d3aa4b171")

# Cross-reference example: resolve a SnapMirror relationship's schedule
for rel in cached.relationships.snapmirror_destinations:
    schedule = cached.uuid_index.get(rel.transfer_schedule_uuid)
    if schedule:
        print(f"{rel.destination_path} uses schedule: {schedule.name}")
```

The index is built lazily on first access and cached for the lifetime of the
object. UUID-bearing types are discovered automatically via introspection —
walking model fields and nested `BaseModel` containers and indexing any list
item that satisfies the `HasUUID` protocol. Objects with empty UUID strings
are excluded. The index does not appear in `model_dump()` or
`model_dump_json()` output. See ADR-0005 for the rationale.

## History Tracking

### How it works

Every time `nf cache refresh` runs:

1. Load the previous snapshot from history (if any).
2. Check schema compatibility via `is_schema_compatible`.
3. Collect new metadata from the cluster.
4. Compute the diff between old and new metadata.
5. If changes are detected (or this is the initial capture), record the
   change in `CacheHistoryDB`.
6. Update the main cache via `ClusterMetadataDB.set`.

### Change records

Each row in the `cache_changes` table contains:

| Field | Type | Description |
|-------|------|-------------|
| `id` | `INTEGER` | Auto-incrementing primary key |
| `cluster_name` | `TEXT` | Cluster identifier |
| `changed_at` | `TEXT` | ISO timestamp of the change |
| `before_json` | `TEXT` | Previous metadata snapshot, `NULL` for the initial capture |
| `after_json` | `TEXT` | New metadata snapshot |
| `summary_json` | `TEXT` | List of change entries (added / removed / modified) |

### Diff summary format

Changes are tracked as a list of change entries:

```json
[
  {
    "category": "nodes",
    "type": "added",
    "entity": "node2"
  },
  {
    "category": "storage.aggregates",
    "type": "modified",
    "entity": "aggr1",
    "field": "disk_count",
    "old": 12,
    "new": 24
  },
  {
    "category": "network.ip_interfaces",
    "type": "removed",
    "entity": "lif1"
  }
]
```

## CLI Commands

### Refresh cache

```bash
# Refresh single cluster
nf cache refresh cluster1

# Refresh all clusters
nf cache refresh --all

# Refresh with filter
nf cache refresh --all -f '{"env": "Prod"}'

# Verbose mode (show phase-by-phase progress)
nf cache refresh --all -v

# Parallel cluster processing (default: 4 workers)
nf cache refresh --all --parallel-clusters 8

# Disable cluster-level parallelism (strictly sequential)
nf cache refresh --all --parallel-clusters 1
```

Cluster collection runs in parallel by default (4 workers). Database writes
are serialised on the main thread for SQLite thread-safety. In verbose
parallel mode each cluster's phase output is buffered and flushed as a
coherent block on completion; blocks may appear in any order.

### View history

```bash
# List all change history
nf cache history list

# List history for a specific cluster
nf cache history list cluster1

# Filter by date range
nf cache history list --since 2024-01-01 --until 2024-06-30

# Show more records
nf cache history list -n 50 --offset 20
```

### View change details

```bash
# Show full change details
nf cache history show 5

# Output as JSON
nf cache history show 5 --json

# Show formatted diff
nf cache history diff 5

# Filter diff to a specific category
nf cache history diff 5 -c nodes
nf cache history diff 5 -c storage.aggregates
```

### Point-in-time snapshots

```bash
# View cache state at a specific date
nf cache history snapshot cluster1 --date 2024-01-15

# Get full JSON snapshot
nf cache history snapshot cluster1 -d 2024-06-01T12:00:00 --json

# Restore cache to a previous state
nf cache history snapshot cluster1 -d 2024-01-15 --restore
```

### Query cached data (`nf cache check`)

`nf cache check` runs ad-hoc filter expressions against cached model data
using the same filter language as `query_with_filters`. Exit codes follow
grep conventions (0 = no matches, 1 = matches found, 2 = error), which
makes it suitable for CI scripts.

```bash
# Find volumes where autosize mode is not grow_shrink on one cluster
nf cache check cluster1 storage.volumes \
    -w "autosize.mode != 'grow_shrink'" \
    -F name,svm.name,autosize.mode

# Check all cached clusters, JSON output
nf cache check --all nodes -w "model = 'FAS8200'" --json

# Filter clusters first with --filter (-f), then run the data check
nf cache check -f '{"env":"Prod"}' storage.volumes \
    -w "size > 1073741824" --count
```

### Compliance checks (`nf cache compliance`)

`nf cache compliance` evaluates compliance rules (defined in TOML config)
against cached cluster metadata. Each rule specifies a model and a filter
expression; any matching records are reported as violations. Exit codes
match `nf cache check` (0 = clean, 1 = violations, 2 = error).

```bash
# Run all compliance rules against one cluster
nf cache compliance cluster1

# Run against every cached Prod cluster, errors only
nf cache compliance --all -f '{"env":"Prod"}' -s error

# Run a single named rule
nf cache compliance --all -k vol_autosize
```

Both `check` and `compliance` are driven by the cache query engine — they
never hit live ONTAP, so they are safe to run in tight loops against the
cached snapshot.

### Field projection (`nf cache query`)

`nf cache query` retrieves a specific set of field paths from cached
snapshots, across one or many clusters, with CSV/JSON/table output.
Filter predicates select array items by field value using bracket syntax.

```bash
nf cache query --all storage.volumes -F name,svm.name,size

# Filter predicate — select items matching a field value
nf cache query cluster1 'volumes["name=vol1"].size'

# OR filter — match multiple values
nf cache query cluster1 'volumes["name=vol1 || name=vol2"].size'

# Glob pattern — match by substring or pattern (* and ? supported)
nf cache query cluster1 'volumes["name=*PROD*"].size'
```

### Raw cache views (`nf cache show` and `nf cache inspect`)

`nf cache show` pretty-prints the cached snapshot for a cluster as a
tree, optionally filtered to one section. `nf cache inspect` compares
cache, live CLI, and live API data for a single named object — useful
for debugging field-mapping issues.

```bash
nf cache show cluster1
nf cache show cluster1 storage.volumes --json
nf cache inspect cluster1 volume-name storage.volumes
```

### Schema view (`nf cache schema`)

`nf cache schema` renders the current `CachedClusterMetadata` schema as a
tree (or flat list) of field paths and Python types. Useful for
discovering valid paths for `query`, `check`, and `history diff -c`.

```bash
nf cache schema
nf cache schema --flat
nf cache schema --json
```

### Cluster cache status (`nf cache status`)

`nf cache status` lists every cluster currently in the cache with its
`cached_at` timestamp, age, and stale flag (relative to a configurable
TTL).

```bash
nf cache status
nf cache status --ttl 7
```

### Clearing the cache (`nf cache clear`)

`nf cache clear` removes cached rows for a single cluster or every
cluster. Cached history is **not** touched.

```bash
nf cache clear cluster1         # Single cluster (prompts for confirmation)
nf cache clear --all --force    # All clusters, no prompt
```

## Schema Compatibility

### Compatibility checking

When loading historical snapshots, the system checks schema compatibility:

```python
from pynetappfoundry.cache import is_schema_compatible, CachedClusterMetadata

# Check if a snapshot version can be loaded
if is_schema_compatible(snapshot_data.get("cache_version")):
    metadata = CachedClusterMetadata.model_validate(snapshot_data)
else:
    # Handle incompatible version
    pass
```

### What happens with incompatible schemas

| Operation | Incompatible schema behaviour |
|-----------|------------------------------|
| `cache refresh` | Treats as initial capture, logs warning |
| `history snapshot --restore` | Rejects with error message |
| `history show --json` | Returns raw JSON (no validation) |
| `history diff` | Shows summary from stored data |

## Schema Update Checklist

When modifying the cache schema, work through this checklist:

1. **Update the model** in the appropriate
   `src/pynetappfoundry/models/<api-type>/<api-path>/model.py` file. Use
   nested sub-models per ADR-0011.
2. **Decide the strategy for any new field** — `cache`, `realtime`, or
   `derived`. Update the corresponding `FieldMapping` (or TOML overlay) so
   the collector and cache write path agree.
3. **Update the snapshot schema version** in `cache/_base.py` if the change
   is observable in stored snapshots:

    ```python
    METADATA_SCHEMA_VERSION = "2.1"  # MINOR for additive
    # or
    METADATA_SCHEMA_VERSION = "3.0"  # MAJOR for breaking
    ```

4. **Update minimum compatible version** if the change is breaking:

    ```python
    METADATA_SCHEMA_MIN_COMPATIBLE = "3.0"
    ```

5. **Document the change** in the
   [Snapshot schema version history](#snapshot-schema-version-history)
   table above.
6. **Bump the SQLite schema version** (`ClusterMetadataDB.SCHEMA_VERSION`)
   and add an `_upgrade_to_vN` method if the **on-disk column layout** has
   to change. The v3 → v4 migration is the reference example for a
   destructive recreate-and-clear migration.
7. **Update the collector** (`src/pynetappfoundry/cache/collector.py`) if
   new fields need to be populated.
8. **Diff logic updates automatically** — tracked fields are derived at
   runtime from each model's `model_fields`, so new fields on cache models
   are picked up without manual changes to
   `src/pynetappfoundry/cache/diff.py`.
9. **Add tests** for new fields in `tests/unit/cache/`.
10. **Run the full check suite**:

    ```bash
    doit check
    ```

### Migration strategies

#### Option 1: Clean break (recommended for major changes)

Set `METADATA_SCHEMA_MIN_COMPATIBLE` to the new version. Old snapshots
become read-only (viewable via `--json` but not restorable).

```python
METADATA_SCHEMA_VERSION = "3.0"
METADATA_SCHEMA_MIN_COMPATIBLE = "3.0"
```

#### Option 2: Migration function (for recoverable changes)

Add migration logic when loading old snapshots:

```python
def migrate_snapshot(data: dict, from_version: str) -> dict:
    """Migrate snapshot data to the current schema."""
    major, minor = parse_schema_version(from_version)
    # Add migration steps as needed
    data["cache_version"] = METADATA_SCHEMA_VERSION
    return data
```

## Model Reference

All models use `ConfigDict(extra="allow")` for forward compatibility with new
API fields. Codegen-generated models are produced from the ONTAP OpenAPI spec
via [the codegen pipeline](#openapi-codegen-pipeline).

### Cloud and cluster

| Model | Key fields | Description |
|-------|------------|-------------|
| `CloudMetadata` | `node`, `instance_id`, `provider`, `region`, `instance_type`, `availability_zone` | Cloud provider metadata per node (CLI-only) |
| `ClusterInfo` | `cluster_name`, `cluster_uuid`, `ontap_version`, `contact`, `location`, `is_ha`, `san_optimized` | Core cluster identity |
| `OntapNodeResponse` | `uuid`, `name`, `state`, `serial_number`, `location`, `membership`, `version`, `controller`, `ha` | Cluster node information (codegen-generated) |
| `OntapLicensePackageResponse` | `name`, `scope`, `state`, `description`, `entitlement`, `licenses` | License package (codegen-generated) |
| `OntapMediatorResponse` | `uuid`, `ip_address`, `port`, `reachable`, `peer_cluster`, `dr_group` | ONTAP Mediator configuration (codegen-generated) |

### Network

| Model | Key fields | Description |
|-------|------------|-------------|
| `OntapIpInterface` | `uuid`, `name`, `enabled`, `state`, `scope`, `ip`, `location`, `svm` | Logical interface (codegen-generated) |
| `OntapBroadcastDomain` | `uuid`, `name`, `mtu`, `ipspace`, `ports` | Broadcast domain (codegen-generated) |
| `OntapIpSubnet` | `uuid`, `name`, `gateway`, `subnet`, `ipspace`, `broadcast_domain` | IP subnet (codegen-generated) |
| `OntapDns` | `uuid`, `domains`, `servers`, `scope`, `svm` | DNS configuration (codegen-generated) |

**Container:** `NetworkInfo` holds `ip_interfaces`,
`ethernet_broadcast_domains`, `ipspaces`, `dns`, `ip_subnets`.

### Storage

| Model | Key fields | Description |
|-------|------------|-------------|
| `OntapAggregate` | `uuid`, `name`, `state`, `node`, `volume_count`, `space` | Storage aggregate (codegen-generated) |
| `OntapSvm` | `uuid`, `name`, `state`, `subtype`, `language`, `comment` | Storage VM (codegen-generated) |
| `OntapVolume` | `uuid`, `name`, `state`, `style`, `size`, `type_`, `svm`, `space` | Volume (codegen-generated) |
| `OntapQtree` | `id`, `name`, `path`, `security_style`, `svm`, `volume` | Qtree (codegen-generated) |
| `OntapCloudTarget` | `uuid`, `name`, `provider_type`, `server`, `container`, `scope` | Cloud object store target (codegen-generated) |
| `OntapFlexcache` | `uuid`, `name`, `size`, `path`, `svm`, `origins` | FlexCache volume (codegen-generated) |
| `OntapSnapshotPolicy` | `uuid`, `name`, `enabled`, `scope`, `comment`, `svm`, `copies` | Snapshot policy (codegen-generated) |
| `OntapSchedule` | `uuid`, `name`, `type_`, `scope`, `cron`, `svm` | Job schedule (codegen-generated) |
| `OntapLun` | `uuid`, `name`, `enabled`, `os_type`, `serial_number`, `svm`, `space`, `status` | LUN (codegen-generated) |
| `OntapIgroup` | `uuid`, `name`, `protocol`, `os_type`, `svm`, `initiators` | Initiator group (codegen-generated) |
| `OntapQosPolicy` | `uuid`, `name`, `scope`, `policy_class`, `svm` | QoS policy (codegen-generated) |

**Container:** `StorageInfo` holds `aggregates`, `svms`, `cloud_targets`,
`volumes`, `qtrees`, `snapshot_policies`, `schedules`, `luns`, `igroups`,
`qos_policies`, `flexcaches`, `svm_top_metrics_users`.

### Protocols

| Model | Key fields | Description |
|-------|------------|-------------|
| `OntapExportPolicy` | `index`, `protocols`, `clients`, `ro_rule`, `rw_rule`, `superuser` | NFS export policy rule (codegen-generated) |
| `OntapCifsShare` | `name`, `path`, `comment`, `volume`, `svm`, `acls` | CIFS/SMB share (codegen-generated) |
| `OntapCifsService` | `name`, `enabled`, `comment`, `ad_domain`, `security`, `svm` | CIFS service config (codegen-generated) |
| `OntapNfsService` | `enabled`, `state`, `protocol`, `security`, `transport`, `svm` | NFS service config (codegen-generated) |
| `OntapS3Bucket` | `uuid`, `name`, `type_`, `size`, `comment`, `svm`, `volume` | S3 bucket (codegen-generated) |

**Container:** `ProtocolsInfo` holds `nfs_export_policies`, `cifs_shares`,
`nfs_services`, `cifs_services`, `s3_buckets`.

### Relationships

| Model | Key fields | Description |
|-------|------------|-------------|
| `OntapSnapmirrorRelationship` | `uuid`, `state`, `healthy`, `source`, `destination`, `policy`, `transfer`, `lag_time` | SnapMirror relationship (codegen-generated) |
| `OntapClusterPeer` | `uuid`, `name`, `ip_address`, `remote`, `status`, `version` | Cluster peer (codegen-generated) |
| `OntapSvmPeer` | `uuid`, `name`, `state`, `applications`, `peer`, `svm` | SVM peer (codegen-generated) |

**Container:** `RelationshipsInfo` holds `snapmirror_destinations`,
`cluster_peers`, `svm_peers`.

## Collection Phases

`MetadataCollector` uses all-or-nothing collection semantics: every API phase
must succeed completely or the entire collection is aborted — no partial cache
updates. Cloud metadata is the only CLI-based phase and is optional (failure
logs a warning but does not abort collection).

| Phase | Source | Required | Endpoints |
|-------|--------|----------|-----------|
| `CLOUD` | CLI | No | `virtual-machine instance show` (ONTAP CLI, one row per node) |
| `CLUSTER` | API | Yes | `/cluster` |
| `NODES` | API | Yes | `/cluster/nodes` |
| `NETWORK` | API | Yes | `/network/ip/interfaces`, `/network/ethernet/broadcast-domains`, `/network/ipspaces`, `/name-services/dns`, `/network/ip/subnets` |
| `STORAGE` | API | Yes | `/storage/aggregates`, `/svm/svms`, `/cloud/targets`, `/storage/volumes`, `/storage/qtrees`, `/storage/snapshot-policies`, `/cluster/schedules`, `/storage/luns`, `/protocols/san/igroups`, `/storage/qos/policies`, `/storage/flexcache/flexcaches` |
| `LICENSES` | API | Yes | `/cluster/licensing/licenses` |
| `MEDIATOR` | API | Yes | `/cluster/mediators` |
| `RELATIONSHIPS` | API | Yes | `/snapmirror/relationships`, `/cluster/peers`, `/svm/peers` |
| `PROTOCOLS` | API | Yes | `/protocols/nfs/export-policies`, `/protocols/cifs/shares`, `/protocols/nfs/services`, `/protocols/cifs/services`, `/protocols/s3/buckets` |

After all phases complete, `collect_all` runs a post-collection pass that
populates parameterized per-SVM endpoints (currently
`svm_top_metrics_users` on `StorageInfo`). These follow-up calls are keyed
off the SVMs returned by the `STORAGE` phase.

## Public API Reference

### Imports

```python
from pynetappfoundry.cache import (
    CachedClusterMetadata,
    CacheHistoryDB,
    ClusterMetadataDB,
    LazyClusterMetadata,
    MetadataCollector,
    CollectionError,
    CollectionPhase,
    FieldMapping,
    TypeMapping,
    HasUUID,
    METADATA_SCHEMA_VERSION,
    METADATA_SCHEMA_MIN_COMPATIBLE,
    compute_diff,
    format_diff_summary,
    is_schema_compatible,
    parse_schema_version,
    model_registry,
)
```

Concrete model classes live in their per-endpoint modules under
`src/pynetappfoundry/models/ontap/<api-path>/model.py`. For example:

```python
from pynetappfoundry.models.ontap.cluster.model import ClusterInfo
from pynetappfoundry.models.ontap.cluster.nodes.model import OntapNodeResponse
from pynetappfoundry.models.ontap.cluster.mediators.model import OntapMediatorResponse
from pynetappfoundry.models.ontap.cluster.peers.model import OntapClusterPeer
from pynetappfoundry.models.ontap.network.model import NetworkInfo
from pynetappfoundry.models.ontap.network.ip.interfaces.model import OntapIpInterface
from pynetappfoundry.models.ontap.storage.model import StorageInfo
from pynetappfoundry.models.ontap.storage.aggregates.model import OntapAggregate
from pynetappfoundry.models.ontap.storage.volumes.model import OntapVolume
```

### `ClusterMetadataDB`

```python
db = ClusterMetadataDB(config=config)

# Store metadata (decomposes into per-model tables in a single transaction)
db.set("cluster1", metadata)

# Retrieve full metadata (queries every per-model table)
metadata = db.get("cluster1")  # CachedClusterMetadata or None

# Retrieve a lazy proxy (envelope only — data fields load on first access)
lazy = db.get_lazy("cluster1")  # LazyClusterMetadata or None
volumes = lazy.storage.volumes  # triggers a single field-group query

# Staleness check (envelope-only, no data queries)
stale = db.is_stale("cluster1", ttl_days=30)  # True / False / None

# List clusters with envelope info
clusters = db.list_clusters()  # list[dict[str, str]]

# List clusters with cached_at, age_days, is_stale
status = db.get_status(ttl_days=30)

# Targeted query against a single per-model table (equality filters)
volumes = db.query_model("cluster1", "storage.volumes", state="online")

# Expressive filter expressions (comparison, in/not in, null, json_extract)
volumes = db.query_with_filters(
    "cluster1",
    "storage.volumes",
    [
        "state = 'online'",
        "size > 1073741824",
        "autosize.mode != 'grow_shrink'",
    ],
)

# JSON export / import (round-trips through CachedClusterMetadata)
json_str = db.export_json("cluster1")
db.import_json("cluster1", json_str)

# Clear (single cluster or all)
deleted = db.clear("cluster1")
deleted = db.clear()
```

### `CacheHistoryDB`

```python
db = CacheHistoryDB(config=config)

# Record a change
change_id = db.record_change(
    cluster_name="cluster1",
    before_json=old_metadata.model_dump_json() if old_metadata else None,
    after_json=new_metadata.model_dump_json(),
    summary=changes,  # List of change dicts from compute_diff()
)

# Get the most recent snapshot
snapshot = db.get_latest_snapshot("cluster1")
# Returns: {"after_json": "...", "changed_at": "..."}

# Get the snapshot at a specific date
snapshot = db.get_snapshot_at_date("cluster1", "2024-01-15")

# Query history with optional filters
records = db.get_change_history(
    cluster_name="cluster1",
    limit=50,
    offset=0,
    since="2024-01-01",
    until="2024-06-30",
)

# Get a specific change
record = db.get_change_by_id(5)

# Total count
count = db.get_history_count(cluster_name="cluster1")

db.close()
```

### `MetadataCollector`

```python
collector = MetadataCollector(
    api_client=api_client,           # ONTAPAPIClient instance
    cli_client=cli_client,           # ONTAPCLI instance (optional)
    progress_callback=callback,      # Optional progress updates
    aws_sso_config=sso_config,       # Optional AWS SSO config
    parallel=True,                   # Run independent phases in parallel
    max_workers=8,
)

# Collect all metadata for a cluster
metadata = collector.collect_all("cluster1")
```

### Diff functions

```python
from pynetappfoundry.cache import compute_diff, format_diff_summary

# Compute changes between two snapshots
changes = compute_diff(old_metadata, new_metadata)
# Returns: list[ChangeEntry]

# Format for display
formatted = format_diff_summary(changes)
# Returns: Rich-formatted string
```

## Benchmarks

Performance benchmarks for the core cache data paths live under
`tests/benchmarks/` and run as part of the broader pytest-benchmark suite.

| File | What it measures |
|------|------------------|
| `test_bench_serialization.py` | `_model_to_row` / `_row_to_model` — the core path for every cache DB read and write, including JSON encoding of nested sub-models, boolean coercion, datetime serialisation, and `_extra_json` collection. |
| `test_bench_dict_path.py` | `get_nested_value` — called per-field per-record during metadata collection, one of the hottest paths in the codebase. |
| `test_bench_diff.py` | `compute_diff` — runs on every cache update cycle to compare two `CachedClusterMetadata` snapshots field-by-field. |
| `test_bench_query_engine.py` | `parse_filter` / `parse_filters` / `build_where_clause` — the SQL query engine filter parser, run uncached on every `query_with_filters` call. |

## Troubleshooting

### Common issues

#### "Incompatible schema version" error

**Cause:** Trying to restore a snapshot created with an older schema
version.

**Solution:**

- Use `--json` to view the raw data.
- Manually extract needed information.
- Or refresh the cache to create a new snapshot.

#### History not recording changes

**Cause:** Cache refresh completed but no history entry was created.

**Explanation:** History is only recorded when:

- It is the initial capture (no previous snapshot).
- Changes are detected between old and new metadata.

If metadata is identical, no history entry is created.

#### Large history database

**Cause:** Many clusters with frequent changes.

**Solution:** History is append-only by design. To manage size:

- Query with `--limit` and `--offset` for pagination.
- Consider periodic archival of old records (manual process).

#### Cache empty after upgrade

**Cause:** The v3 → v4 SQLite schema migration drops and recreates every
per-model table because of the nested-model column rename.

**Solution:** Run `nf cache refresh --all` to repopulate the cache.

### Debugging

Enable verbose logging to see cache operations:

```bash
# Verbose refresh shows phase timings
nf cache refresh cluster1 -v

# Check the log file for detailed information
# The log path is shown at the start of refresh
```

## See Also

- [ONTAP Access Patterns](../usage/ontap-access-patterns.md) — user-facing
  guide for choosing between full load, lazy proxy, and live API access.
- [Query Layer](../usage/query-layer.md) — user-facing query syntax built on
  `query_with_filters`.
- [Field Mapping Framework](../development/field-mapping.md) — developer
  guide to `FieldMapping` / `TypeMapping`.
- ADR-0001 — SQLite metadata cache (original decision).
- ADR-0003 — Base `SQLiteDB` class with version-based migrations.
- ADR-0004 — Declarative field mapping framework.
- ADR-0005 — UUID index for cache cross-references.
- ADR-0009 — Per-model SQL table storage for the cache layer.
- ADR-0011 — Nested models to replace the flat model pattern.
- ADR-0018 — Cache schema versioning and backward-compatibility policy.
