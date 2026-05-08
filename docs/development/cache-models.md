---
title: Cache Model Architecture
description: End-to-end guide for the codegen pipeline, cache models, field strategies, and SQL storage
audience:
  - contributors
tags:
  - development
  - cache
  - codegen
  - architecture
---

# Cache Model Architecture

This document covers the complete lifecycle of cache models: fetching API specs,
generating models and mappings, customizing field strategies, and understanding
how changes propagate to the SQLite storage layer.

**ADRs:** [ADR-0004](../decisions/0004-declarative-field-mapping-framework.md),
[ADR-0007](../decisions/0007-url-tree-model-registry.md),
[ADR-0008](../decisions/0008-openapi-codegen-for-model-generation.md),
[ADR-0009](../decisions/0009-sql-table-storage.md)

---

## Pipeline Overview

```
API Endpoint (live cluster)
  │  doit fetch_spec --api=<type>
  ▼
Raw Spec (Swagger 1.2/2.0 or OpenAPI 3.0)
  │  docs/example-config/apis/<type>/all.json
  │  doit convert_specs
  ▼
OpenAPI 3.0 Spec (normalized)
  │  docs/example-config/apis/<type>/openapi3.json
  │  doit generate_models --api=<type>
  ▼
Generated Files (per endpoint)
  ├── model.py          Pydantic model classes
  ├── mapping.py        TypeMapping + FieldMapping definitions
  ├── __init__.py       Package exports
  └── <name>.toml       TOML overlay (field strategy customization)
```

Each stage is idempotent. Re-running any step updates outputs while preserving
user edits in TOML overlays.

---

## Step 1: Fetching API Specs

API specs are fetched from live endpoints and saved as raw JSON.

### Available APIs

| API | Auth Type | Spec Format | Spec Size |
|-----|-----------|-------------|-----------|
| ONTAP | Basic (admin/password) | Swagger 2.0 (YAML→JSON) | ~12MB, 550 paths, 1103 definitions |
| AIQUM | Basic (admin/password) | Swagger 2.0 | 89 paths, 191 definitions |
| DII | API Key | OpenAPI 3.0.1 | 363 paths, 199 schemas |
| OCCM | Session (email/password) | Swagger 1.2 | Custom multi-resource format |

### Fetching

```bash
# ONTAP
doit fetch_spec --api=ontap --host=10.0.0.1 --username=admin --password=secret

# AIQUM
doit fetch_spec --api=aiqum --host=aiqum.local --username=admin --password=secret

# DII (Data Infrastructure Insights)
doit fetch_spec --api=dii --host=tenant.cloudinsights.netapp.com --api-key=TOKEN

# OCCM (BlueXP Connector)
doit fetch_spec --api=occm --host=connector.local --username=user@co.com --password=secret

# Skip TLS verification (self-signed certs)
doit fetch_spec --api=ontap --host=10.0.0.1 --username=admin --password=secret --no-verify
```

Output: `docs/example-config/apis/<type>/all.json`

Each fetch script also sanitizes the spec (removes security blocks, fixes
dangling `$ref` references, removes fake paths).

### Spec Location

```
docs/example-config/apis/
├── ontap/
│   ├── all.json          ← raw fetched spec
│   └── openapi3.json     ← converted (Step 2)
├── aiqum/
│   ├── all.json
│   └── openapi3.json
├── dii/
│   ├── all.json
│   └── openapi3.json
└── occm/
    ├── all.json
    └── openapi3.json
```

---

## Step 2: Converting Specs to OpenAPI 3.0

All specs must be normalized to OpenAPI 3.0 before codegen can process them.

```bash
# Convert all specs
doit convert_specs

# Convert a single spec
doit convert_specs --api=ontap
```

| Source Format | Conversion |
|---------------|------------|
| Swagger 2.0 (ONTAP, AIQUM) | `swagger2openapi` (via npx) |
| OpenAPI 3.0 (DII) | Direct copy (already compatible) |
| Swagger 1.2 (OCCM) | Python converter → Swagger 2.0 → `swagger2openapi` |

**Prerequisite:** Node.js must be installed for the `swagger2openapi` tool.

---

## Step 3: Generating Models

The codegen tool parses the OpenAPI 3.0 spec and generates Python source files.

```bash
# Generate from all specs
doit generate_models

# Generate from a single API
doit generate_models --api=ontap

# Generate specific endpoints only
doit generate_models --api=ontap --endpoints=/storage/volumes,/cluster/nodes

# Preview without writing
doit generate_models --api=ontap --dry-run
```

### What Gets Generated

For each GET endpoint with a response schema, the codegen produces files
split between `src/pynetappfoundry/models/<api-type>/` (model classes) and
`src/pynetappfoundry/cache/<api-type>/` (mappings, init, TOML overlays):

#### `model.py` — Pydantic Model (in `models/<api-type>/`)

```python
from pynetappfoundry.models import OntapModel

class OntapVolume(OntapModel):
    """OntapVolume information."""

    name: str = ""
    uuid: str = ""
    state: str = ""
    size: int = 0
    svm_name: str = ""
    svm_uuid: str = ""
    # ... all fields from the API schema
```

- Model files live under `models/<api-type>/`, not `cache/<api-type>/`
- Flat structure: nested API objects are flattened with underscore-joined names
  (e.g., `svm.name` → `svm_name`)
- UUID fields use `OntapUUID` validated type
- Sub-models (arrays of objects) are generated as separate classes
  (e.g., `OntapVolumeAggregate`)
- All fields have defaults — models can be constructed with partial data

#### `mapping.py` — TypeMapping + FieldMapping

```python
ONTAPVOLUME_MAPPING = TypeMapping(
    name="OntapVolume",
    model_class=OntapVolume,
    api_endpoint="/storage/volumes?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(cache_attr="name", api_path="name"),
        FieldMapping(cache_attr="svm_name", api_path="svm.name"),
        FieldMapping(
            cache_attr="statistics_iops_total",
            api_path="statistics.iops_raw.total",
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="aggregates",
            transform=_transform_aggregates,
            default=[],
        ),
        # ...
    ),
)
```

- `api_endpoint` stores the base endpoint with `?fields=*` only
- `build_collection_url()` dynamically appends expensive field names by
  inspecting `requires_explicit_fetch` on each field — this is what the
  collector and CLI inspect call instead of `api_endpoint` directly
- Sub-model fields use `transform` functions instead of `api_path`
- `requires_explicit_fetch=True` marks ONTAP expensive fields

#### `__init__.py` — Package Exports (in `cache/<api-type>/`)

```python
from pynetappfoundry.cache.ontap.storage.volumes.mapping import ONTAPVOLUME_MAPPING
from pynetappfoundry.models.ontap.storage.volumes.model import OntapVolume

__all__ = ["ONTAPVOLUME_MAPPING", "OntapVolume"]
```

#### `<name>.toml` — TOML Overlay

```toml
[endpoint]
path = "/storage/volumes"
schema = "volume"
class_name = "OntapVolume"

[fields.name]
cache_strategy = "cache"

[fields.statistics_iops_total]
cache_strategy = "cache"
requires_explicit_fetch = true

[fields.svm_name]
cache_strategy = "cache"
```

The TOML overlay is the **user-editable configuration** for field strategies.
See [Field Strategies](#field-strategies) below.

### Directory Structure

Models and mappings follow the API URL path hierarchy (ADR-0007), split
across two packages:

```
src/pynetappfoundry/models/          ← Model classes (OntapModel subclasses)
├── _base.py                         ← OntapModel, OntapUUID, HasUUID
├── __init__.py
└── ontap/
    ├── storage/
    │   ├── volumes/
    │   │   └── model.py
    │   ├── aggregates/
    │   └── snapshot_policies/
    ├── cluster/
    │   ├── nodes/
    │   └── schedules/
    ├── protocols/
    │   ├── nfs/
    │   │   ├── services/
    │   │   └── export_policies/
    │   └── cifs/
    └── network/
        ├── ip/
        │   └── interfaces/
        └── ethernet/
            └── broadcast_domains/

src/pynetappfoundry/cache/           ← Mappings, registration, DB, collector
├── ontap/
│   ├── storage/
│   │   ├── volumes/
│   │   │   ├── mapping.py
│   │   │   ├── __init__.py
│   │   │   └── volumes.toml
│   │   ├── aggregates/
│   │   └── snapshot_policies/
│   └── ...
├── _base.py                         ← CacheModel = OntapModel alias, schema versioning
├── _registry.py
├── field_mapping.py
└── ...
```

### Expensive Field Detection

ONTAP REST API specs document expensive fields in endpoint descriptions:

```
### Expensive properties
* `analytics.*`
* `autosize.*`
* `statistics.*`
* `is_svm_root`
```

The codegen parses these patterns via regex and sets
`requires_explicit_fetch=True` on matching fields. At runtime,
`build_collection_url()` dynamically appends these fields to the query
string (e.g., `?fields=*` becomes `?fields=*,statistics,autosize`).
The `api_endpoint` itself stores only `?fields=*`.

DII, AIQUM, and OCCM specs don't document expensive fields — all fields
default to `requires_explicit_fetch=False`.

### TOML Overlay Preservation

When codegen re-runs, it preserves user edits in existing TOML files:

- **Existing fields**: User-edited entries (e.g., changed `cache_strategy`)
  are preserved as-is
- **New fields**: Added with default `cache_strategy = "cache"`
- **Removed fields**: Noted in a `_removed_fields` key (warning only, not deleted)

This means you can safely re-run codegen after updating an API spec without
losing field strategy customizations.

---

## Field Strategies

Every field on a mapping has a `cache_strategy` that controls how it's
collected and stored.

### Strategy Types

| Strategy | Collected During Bulk? | Persisted in DB? | How Accessed |
|----------|----------------------|------------------|--------------|
| `cache` | Yes | Yes | Read from SQLite cache |
| `realtime` | No (skipped) | No | Fetched on-demand per object |
| `derived` | No (skipped) | Yes | Computed post-collection via `post_collection` callable |

### How Strategies Work in Practice

#### `cache` (default)

The standard strategy. During bulk collection, the collector calls the API
endpoint, `parse_api_record()` extracts the field value from the response,
and it's stored in the SQLite table.

```toml
[fields.name]
cache_strategy = "cache"
```

#### `realtime`

The field is **skipped** by `parse_api_record()` during bulk collection.
The model gets its Pydantic default value (e.g., `""` for strings, `0` for
ints). The field is not persisted in the database.

Realtime fields are intended for volatile data that changes too quickly to
cache (e.g., live performance counters, active connection counts). They
would be fetched on-demand via per-object API calls.

```toml
[fields.statistics_iops_total]
cache_strategy = "realtime"
```

#### `derived`

The field is **skipped** by `parse_api_record()` during bulk collection
(gets model default). After all records are parsed, `parse_api_response()`
calls the field's `post_collection` callable to compute the derived value
from other fields.

Derived fields are for values that don't exist in the API response but can
be computed from other cached fields (e.g., `is_ha` computed from node
count, utilization percentages from raw counters).

```toml
[fields.is_ha]
cache_strategy = "derived"
```

The `post_collection` callable is defined in the mapping (not the TOML):

```python
FieldMapping(
    cache_attr="is_ha",
    cache_strategy="derived",
    post_collection=_compute_is_ha,
)
```

### Changing Field Strategies

To change a field's strategy, edit the TOML overlay:

```toml
# Before: field collected during bulk
[fields.statistics_iops_total]
cache_strategy = "cache"
requires_explicit_fetch = true

# After: field fetched on-demand only
[fields.statistics_iops_total]
cache_strategy = "realtime"
```

Then re-run codegen to regenerate the mapping:

```bash
doit generate_models --api=ontap --endpoints=/storage/volumes
```

**Important:** The TOML overlay drives the *intent*, but the codegen
currently generates `cache_strategy` from the TOML when preserving user
edits. If you edit the TOML and re-run codegen, the new strategy is
preserved in the TOML for the next regeneration. However, for the mapping
to reflect the change, you must also manually update `mapping.py` or ensure
the codegen reads the TOML strategy back (currently it preserves the TOML
but generates mappings from the spec). For safety, **manually verify
`mapping.py` after strategy changes**.

---

## Impact on SQLite Storage

### How Models Become Tables

The `db_schema.py` module walks `CachedClusterMetadata.model_fields` at
import time and generates `CREATE TABLE` statements from Pydantic field
definitions.

| Python Type | SQL Type |
|-------------|----------|
| `str`, `OntapUUID` | `TEXT` |
| `int`, `bool` | `INTEGER` |
| `float` | `REAL` |
| `list[...]`, `dict[...]`, sub-models | `TEXT` (JSON) |
| `datetime` | `TEXT` (ISO format) |

Every table has:
- `cluster_name TEXT NOT NULL` — partition key
- `_row_id INTEGER PRIMARY KEY AUTOINCREMENT` — avoids empty-UUID collisions
- `_extra_json TEXT DEFAULT NULL` — preserves `extra="allow"` fields from
  newer ONTAP versions

### What Happens When You Change a Field's Strategy

#### `cache` → `realtime`

1. **Collection**: `parse_api_record()` skips the field. The model gets its
   Pydantic default value.
2. **Storage**: The SQL column **still exists** in the table schema (DDL is
   generated from the Pydantic model, not the mapping). The column will
   contain the default value (empty string, 0, etc.).
3. **Migration**: No schema migration needed. The column remains but holds
   default values going forward. Old cached data retains its previous values
   until the cache is refreshed.

**Key insight**: The SQL table schema is driven by the **Pydantic model**,
not the mapping's `cache_strategy`. Changing a field to `realtime` doesn't
remove its column — it just stops populating it during collection.

#### `realtime` → `cache`

1. **Collection**: `parse_api_record()` now extracts the field. The API
   endpoint must include the field in its `?fields=` query.
2. **Storage**: The SQL column already exists (was getting defaults). It
   now gets real values on the next cache refresh.
3. **Migration**: No schema migration needed. Existing rows have default
   values; new rows get real values.
4. **If the field is expensive**: Add `requires_explicit_fetch = true` in
   the TOML and update the mapping's `api_endpoint` to include the field
   name in the query string.

#### `cache` → `derived`

1. **Collection**: `parse_api_record()` skips the field.
   `parse_api_response()` calls `post_collection` after all records are
   parsed.
2. **Storage**: The column still exists and gets the computed value.
3. **Requirement**: You must add a `post_collection` callable to the
   `FieldMapping` in `mapping.py`.

#### Adding a field to a cache model

If you add a field to a Pydantic model stored in `CachedClusterMetadata`:

1. **New databases**: Get the column automatically — `generate_table_ddl()`
   reads fields from the Pydantic model at import time.
2. **Existing databases**: The column won't exist. You **must** add a schema
   migration:
   - Bump `SCHEMA_VERSION` in `src/pynetappfoundry/cache/db.py`
   - Add an `_upgrade_to_vN()` method with
     `ALTER TABLE <table> ADD COLUMN "<field>" <type>`
   - Make it idempotent (check `PRAGMA table_info` first) — earlier
     migration chains may recreate tables with the current DDL
   - Add a test in `tests/unit/cache/test_db.py`
   - Update any existing migration tests that assert the schema version
3. **Table names**: Lowercased model class name (e.g., `CloudMetadata` →
   `cloudmetadata`)

#### Removing or renaming a field on a cache model

Per [ADR-0018](../decisions/0018-cache-schema-versioning-and-backward-compatibility-policy.md),
the cache is rebuild-tolerant and deprecate-in-place is not the default —
remove or rename a field by dropping and recreating the affected table(s)
in a schema migration. Cached data for that table is lost on upgrade and
the next `nf cache refresh` repopulates it.

1. Bump `SCHEMA_VERSION` in `src/pynetappfoundry/cache/db.py`.
2. Add an `_upgrade_to_vN()` method that drops and recreates the affected
   table(s) using the current DDL (the v3 → v4 migration is the reference
   example for a destructive recreate). Clear the affected envelope row(s)
   so collectors detect missing data and trigger a refresh.
3. Add a test in `tests/unit/cache/test_db.py`.
4. Update any existing migration tests that assert the schema version.

---

## Parameterized Endpoints (Planned)

Some API endpoints are parameterized (e.g., `/protocols/nfs/export-policies/{id}`).
These require a parent resource ID to fetch individual objects.

For **bulk collection**, the collector needs the non-parameterized version.
A future `TypeMapping.collection_endpoint` property will strip `{placeholder}`
segments from `api_endpoint` automatically:

```python
# Parameterized mapping (planned)
mapping.api_endpoint        # "/svm/svms/{svm.uuid}/top-metrics?fields=*"
mapping.collection_endpoint # "/svm/svms/top-metrics?fields=*"

# Non-parameterized mapping (unchanged)
mapping.api_endpoint        # "/storage/volumes?fields=*"
mapping.collection_endpoint # "/storage/volumes?fields=*"
```

### `parent_mapping` and `parent_id_field`

For future per-parent fetching, mappings can declare their parent:

```python
TypeMapping(
    api_endpoint="/svm/svms/{svm.uuid}/web?fields=*",
    parent_mapping="OntapSvm",
    parent_id_field="uuid",
)
```

This tells the framework: "To call this endpoint, look up each `OntapSvm`
from the cache, substitute its `uuid` into the `{svm.uuid}` placeholder,
and make individual API calls."

---

## Auto-Registration and Discovery

### Model Registration

Models are registered in the `ModelRegistry` singleton via explicit
`register_model()` calls in each cache `__init__.py`, not via
`__init_subclass__`.

### Mapping Registration

Each `mapping.py` explicitly registers its mapping at module level:

```python
model_registry.register_mapping("OntapVolume", ONTAPVOLUME_MAPPING)
```

### Import Chain

The `__init__.py` chain in `cache/` triggers model and mapping imports,
so registration happens automatically when the `cache` package is imported:

```
cache/__init__.py
  → cache/ontap/storage/__init__.py
    → cache/ontap/storage/volumes/__init__.py
      → imports models.ontap.storage.volumes.model (OntapVolume)
      → imports cache.ontap.storage.volumes.mapping (ONTAPVOLUME_MAPPING)
      → registers both via model_registry
```

### Three-Layer Import Hierarchy

Imports flow upward only (DAG, no circular deps):

1. **Layer 1**: `models._base` (OntapModel, OntapUUID, HasUUID) and `cache._registry` (ModelRegistry)
2. **Layer 2**: Leaf `model.py` files in `models/ontap/` (import only from `models._base`)
3. **Layer 3**: Container models in `cache/`, `_metadata.py` (import leaf models from `models/`)

---

## Adding a New API Type

!!! note "DataSource backend integration"
    This section covers models, mappings, and codegen for a new API type.
    For the full backend integration story (Backend subclass, `_BACKENDS`
    registration, routing, and authentication), see the
    [Adding Backends](adding-backends.md) guide.

To add support for a completely new API (beyond ONTAP/AIQUM/DII/OCCM):

### 1. Create a fetch script

`tools/scripts/fetch_<api>_spec.py` — downloads and sanitizes the spec.

### 2. Register in codegen config

In `tools/doit/codegen.py`, add to `_FETCH_APIS` and `_SPECS`:

```python
_FETCH_APIS = {
    "ontap": "basic",
    "aiqum": "basic",
    "dii": "apikey",
    "occm": "session",
    "newapi": "basic",  # or "apikey", "session"
}

_SPECS = {
    ...
    "newapi": {"format": "openapi_3", "source": "all.json"},
}
```

### 3. Generate models

```bash
doit fetch_spec --api=newapi --host=... --username=... --password=...
doit convert_specs --api=newapi
doit generate_models --api=newapi
```

### 4. Wire into the collector

Import the generated mappings and add API calls to the appropriate
collector method.

---

## Common Tasks

### Updating models after an ONTAP upgrade

```bash
# 1. Fetch the new spec from the upgraded cluster
doit fetch_spec --api=ontap --host=10.0.0.1 --username=admin --password=secret

# 2. Convert to OpenAPI 3.0
doit convert_specs --api=ontap

# 3. Regenerate models (preserves TOML overlay edits)
doit generate_models --api=ontap

# 4. Review changes
git diff src/pynetappfoundry/cache/ontap/

# 5. Run checks
doit check
```

### Marking a field as realtime

1. Edit the TOML overlay:

   ```toml
   [fields.statistics_iops_total]
   cache_strategy = "realtime"
   ```

2. Update `mapping.py` to add `cache_strategy="realtime"` on the field:

   ```python
   FieldMapping(
       cache_attr="statistics_iops_total",
       api_path="statistics.iops_raw.total",
       cache_strategy="realtime",
   ),
   ```

3. No need to edit `api_endpoint` — `build_collection_url()` dynamically
   builds the query string from `requires_explicit_fetch` fields.

4. Run `doit check` to verify.

### Adding a derived field

1. Add the field to the Pydantic model with a default:

   ```python
   is_ha: bool = False
   ```

2. Add the `FieldMapping` with `cache_strategy="derived"` and a
   `post_collection` callable:

   ```python
   def _compute_is_ha(item: OntapCluster) -> OntapCluster:
       item.is_ha = len(item.nodes) > 1
       return item

   FieldMapping(
       cache_attr="is_ha",
       cache_strategy="derived",
       post_collection=_compute_is_ha,
   ),
   ```

3. Update the TOML overlay:

   ```toml
   [fields.is_ha]
   cache_strategy = "derived"
   ```

### Adding `requires_explicit_fetch` to an existing field

1. Edit the TOML overlay:

   ```toml
   [fields.copies]
   cache_strategy = "cache"
   requires_explicit_fetch = true
   ```

2. Update `mapping.py`:
   - Add `requires_explicit_fetch=True` to the `FieldMapping`
   - No need to edit `api_endpoint` — `build_collection_url()` dynamically
     appends the field name to the query string at runtime

3. Run `doit check` to verify.

---

## Reference: Key Files

| File | Purpose |
|------|---------|
| `tools/codegen/adapters.py` | Parse OpenAPI specs into `ParsedEndpoint`/`ParsedField` |
| `tools/codegen/generators.py` | Generate `model.py`, `mapping.py`, `__init__.py`, TOML |
| `tools/codegen/expensive_fields.py` | Parse ONTAP expensive field annotations |
| `tools/codegen/openapi_codegen.py` | CLI entry point and pipeline orchestration |
| `tools/doit/codegen.py` | `doit` task wrappers for fetch, convert, generate |
| `src/.../models/_base.py` | `OntapModel` base class, `OntapUUID` type, `HasUUID` protocol |
| `src/.../cache/field_mapping.py` | `FieldMapping`, `TypeMapping`, generic parsers |
| `src/.../cache/_base.py` | `CacheModel` alias for `OntapModel`, schema versioning |
| `src/.../cache/_registry.py` | `ModelRegistry` singleton |
| `src/.../cache/db_schema.py` | DDL generation from Pydantic models |
| `src/.../cache/db.py` | `ClusterMetadataDB` — SQLite storage layer |
| `src/.../cache/collector.py` | Bulk collection using mappings |
