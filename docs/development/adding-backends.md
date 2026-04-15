---
title: Adding a New API Backend
description: Developer guide for extending the DataSource framework with new API backends
audience:
  - contributors
tags:
  - development
  - datasource
  - backend
  - api
---

# Adding a New API Backend

This guide explains how to add a new API backend to the DataSource framework,
enabling `DataSource.query()` and `DataSource.get()` to fetch data from APIs
beyond ONTAP (e.g., AIQUM, DII, OCCM).

**ADRs:** [ADR-0012](../decisions/0012-unified-datasource-accessor.md) (superseded),
[ADR-0013](../decisions/0013-datasource-as-a-thin-facade-over-the-collector.md) (current)

---

## Architecture Overview

The `DataSource` class is a thin facade that routes queries to backend
implementations based on the `api_type` tag declared on each `TypeMapping`.
The flow is:

```
                         DataSource
                             |
                     _resolve_mapping()
                             |
                      TypeMapping.api_type
                             |
                   _BACKENDS registry lookup
                             |
              +--------------+--------------+
              |              |              |
        OntapBackend    (FutureBackend)   ...
              |
   +----------+----------+
   |          |           |
 cache    live(fetch)   partial
   |          |           |
 CacheDB   Collector   merge(cache+live)
```

1. **`DataSource`** resolves the `TypeMapping` for the requested Pydantic
   model class via the model registry.
2. The `TypeMapping.api_type` string selects the backend from `_BACKENDS`
   in `data/source.py`.
3. The **routing layer** (`data/_routing.py`) decides which fields come from
   cache and which from the live API, producing a `RoutingDecision`.
4. The **backend** executes the decision: cache read, live fetch, or a
   partial merge of both.

---

## Step-by-Step Checklist

Adding a new backend (e.g., `dii`) requires changes across several layers.
Use this checklist:

### 1. Create an API client

Create `clients/<api_type>/api.py` with a subclass of `APIWrapper`:

```python
# clients/dii/api.py
from pynetappfoundry.clients.openapi import APIWrapper

class DIIAPIClient(APIWrapper):
    def __init__(self, config: Config, **kwargs: Any) -> None:
        dii_settings = config.get_dii_api_settings()
        super().__init__(
            api_json_file=str(config.get_schema_location("dii") / "all.json"),
            base_url=dii_settings.base_url,
            auth_header={"X-CloudInsights-ApiKey": dii_settings.api_ro_token},
            base_api_path=dii_settings.base_api_path,
            timeout=dii_settings.timeout,
            **kwargs,
        )
```

Key differences from `ONTAPAPIClient`:

- **Authentication** varies per API. ONTAP uses HTTP Basic Auth; DII uses an
  API key header. Your client must construct the appropriate `auth_header`.
- **SSL verification** defaults to `True` in `APIWrapper`. ONTAP disables it
  (`verify_ssl=False`) because clusters typically use self-signed certificates.
  Only disable SSL verification when your API requires it.
- **OpenAPI spec** must be present at the path returned by
  `config.get_schema_location("<api_type>")`.

### 2. Create Pydantic models

Create models under `models/<api_type>/`:

```
models/
  dii/
    __init__.py
    storage/
      __init__.py
      model.py          # e.g., DiiStoragePool
```

Models should use `BaseModel` from Pydantic and follow the same patterns
as existing ONTAP models. Every field that the `DataSource` might return
should have a default value so that partially-populated instances are valid.

See [Cache Models](cache-models.md) for the full model creation workflow,
including codegen from OpenAPI specs.  See
[ADR-0008](../decisions/0008-openapi-codegen-for-model-generation.md) for
the codegen pipeline's round-trip invariant (regeneration must be a
no-op for existing endpoints) and the TOML-as-authority rule for
`cache_strategy` / `requires_explicit_fetch`.

### 3. Create field mappings

Create mappings under `cache/<api_type>/`:

```
cache/
  dii/
    __init__.py
    storage/
      __init__.py
      mapping.py        # TypeMapping + FieldMapping definitions
```

Each `TypeMapping` must set `api_type` to match the backend registry key:

```python
DII_STORAGE_MAPPING = TypeMapping(
    name="DiiStoragePool",
    model_class=DiiStoragePool,
    api_endpoint="/rest/v1/assets/storagePools",
    fields=(...),
    api_type="dii",                # must match _BACKENDS key
    records_path="_embedded.items", # DII uses HAL, not ONTAP envelope
    identifier_field="id",
)
```

!!! important "The `api_type` field is the routing key"
    `DataSource` uses `TypeMapping.api_type` to look up the backend in
    `_BACKENDS`. If `api_type` does not match a registered backend, queries
    raise `ValueError` at runtime.

### 4. Register mappings in the bootstrap

Extend `cache/__init__.py` to import your mapping modules. The existing
ONTAP bootstrap uses `pkgutil.walk_packages` to auto-discover `mapping.py`
files under `cache/ontap/`. Add a parallel walk for your API type:

```python
import pynetappfoundry.cache.dii as _dii_pkg

for _modinfo in _pkgutil.walk_packages(
    _dii_pkg.__path__,
    prefix="pynetappfoundry.cache.dii.",
):
    if _modinfo.name.endswith(".mapping"):
        _importlib.import_module(_modinfo.name)
```

### 5. Create the Backend subclass

Add your backend class to `data/backends.py`:

```python
class DiiBackend(Backend):
    """Backend for Data Infrastructure Insights."""

    def __init__(self, config: Config) -> None:
        super().__init__(config)

    def query(
        self,
        model_class: type[T],
        mapping: TypeMapping,
        decision: RoutingDecision,
        cluster: str,
        filters: dict[str, Any],
        *,
        where_expressions: tuple[str, ...] = (),
    ) -> list[T]:
        # Implement cache, live, and partial paths
        ...
```

### 6. Register in `_BACKENDS`

In `data/source.py`, add your backend to the registry:

```python
_BACKENDS: dict[str, type[Backend]] = {
    "ontap": OntapBackend,
    "dii": DiiBackend,
}
```

### 7. Update audit and compliance tools

Two files have `TODO(#533)` markers that are hardcoded to ONTAP only:

- `tools/doit/audit_models.py` (line 13) -- generalize `_MODELS_ROOT` and
  `_MAPPINGS_ROOT` to walk all API type subdirectories.
- `tests/unit/compliance/test_mapping_coverage.py` (line 8) -- same pattern.

---

## Backend ABC Contract

The `Backend` abstract base class (`data/backends.py`) defines the interface
that every backend must implement:

```python
class Backend(ABC):
    def __init__(self, config: Config) -> None:
        self._config = config

    @abstractmethod
    def query(
        self,
        model_class: type[T],
        mapping: TypeMapping,
        decision: RoutingDecision,
        cluster: str,
        filters: dict[str, Any],
        *,
        where_expressions: tuple[str, ...] = (),
    ) -> list[T]:
        ...
```

### `query()` responsibilities

1. **Inspect the `RoutingDecision`** to determine which fields come from
   cache (`decision.cache_fields`) and which from the live API
   (`decision.live_fields`). If both are populated, `decision.partial` is
   `True` and you must implement a merge strategy.

2. **Return a list of populated Pydantic model instances.** The list may be
   empty if no records match the filters.

3. **Stamp `_fetched_fields`** on every returned instance. Call
   `_mark_fetched(instance, fields_tuple)` or populate the
   `_fetched_fields` set directly. This tells downstream code which fields
   were actually fetched versus left at their defaults.

4. **Handle `where_expressions`** on the cache path. On live and partial
   paths, raise `NotImplementedError` if `where_expressions` is non-empty
   (v1 limitation).

### Arguments

| Argument | Description |
| :--- | :--- |
| `model_class` | The Pydantic model class to instantiate (e.g., `OntapVolume`). |
| `mapping` | The `TypeMapping` that declares the endpoint, fields, and API type. |
| `decision` | A `RoutingDecision` from `decide_path()` indicating cache vs live routing. |
| `cluster` | Cluster name string passed through from the caller. |
| `filters` | Equality filter dict with dotted API paths as keys. |
| `where_expressions` | SQL-like filter strings for the cache path (ANDed with `filters`). |

---

## OntapBackend Reference Patterns

`OntapBackend` is the reference implementation. Key patterns to study:

### Lazy client construction

Clients are created on first use and cached per cluster:

```python
@cached_property
def _cache_db(self) -> ClusterMetadataDB:
    from pynetappfoundry.cache.db import ClusterMetadataDB
    return ClusterMetadataDB(config=self._config)

def _get_api_client(self, cluster: str) -> ONTAPAPIClient:
    if cluster not in self._api_clients:
        ...  # construct and cache
    return self._api_clients[cluster]
```

### Three query paths

The `query()` method dispatches to one of three paths based on the routing
decision:

1. **Cache-only** (`decision.cache_fields` populated, no `live_fields`):
   queries the SQLite cache via `_fetch_cache()`.

2. **Live-only** (`decision.live_fields` populated, no `cache_fields`):
   either delegates to the generic `fetch()` dispatcher for whole-model
   reads, or builds a filtered URL via `_fetch_live_filtered()`.

3. **Partial** (`decision.partial` is `True`): runs the Approach C
   algorithm in `_query_partial()` -- cache defines membership, live
   enriches by identifier, results merge by identifier field.

### Partial-fetch merge algorithm

For partial queries, `OntapBackend` follows this sequence:

1. Validate that filter keys target cache-side fields only.
2. Run the cache query (defines the set of matching records).
3. Extract identifiers from cached instances.
4. Batch-fetch live data for those identifiers (chunked at `_BATCH_SIZE`).
5. Merge each cached instance with its live counterpart by identifier.
6. Stamp `_fetched_fields` on the merged result.

---

## TypeMapping Routing

The `api_type` field on `TypeMapping` is the key that connects a model to
its backend:

```python
# In a mapping.py file:
VOLUME_MAPPING = TypeMapping(
    name="Volume",
    model_class=OntapVolume,
    api_endpoint="/api/storage/volumes?fields=*",
    api_type="ontap",  # routes to OntapBackend
    ...
)
```

When `DataSource.query(OntapVolume, cluster="prod1")` is called:

1. `_resolve_mapping(OntapVolume)` finds the `TypeMapping` in the model
   registry.
2. `mapping.api_type` (e.g., `"ontap"`) is used to look up the backend
   via `_get_backend("ontap")`.
3. The backend is lazily instantiated and cached for the `DataSource`
   lifetime.

New API types simply need a `TypeMapping` with the correct `api_type` and a
corresponding entry in `_BACKENDS`.

---

## Source Routing: Cache vs Live vs Partial

The routing layer (`data/_routing.py`) is a pure function with no I/O. It
inspects each field's `cache_strategy` to decide the path:

| `cache_strategy` | `source="auto"` | `source="cache"` | `source="live"` |
| :--- | :--- | :--- | :--- |
| `"cache"` | Cache (unless `requires_explicit_fetch`) | Cache | Live |
| `"realtime"` | Live (only if explicitly named in `fields=`) | Raises `ValueError` | Live |
| `"derived"` | Cache | Cache | Raises `ValueError` |

The `RoutingDecision` dataclass carries two tuples:

- `cache_fields` -- field paths to serve from the cache.
- `live_fields` -- field paths to fetch from the live API.

When both are populated (`decision.partial`), the backend must implement a
merge strategy.

### Cache-miss fallback

Under `source="auto"`, if the cache query returns no results,
`QueryBuilder.__iter__()` automatically retries with `source="live"`,
excluding derived fields (which only exist in the cache). This fallback
is skipped when `.where()` expressions are present.

---

## ONTAP Patterns That Do Not Generalize

When building a non-ONTAP backend, be aware of ONTAP-specific patterns in
`OntapBackend` that your backend will need to replace:

### Pipe-OR filter syntax

ONTAP REST accepts `?uuid=id1|id2|id3` to filter by multiple values in one
request. `OntapBackend` uses this in `_fetch_live_by_identifiers()` and
`_fetch_live_by_parent()`. Non-ONTAP APIs may require:

- Multiple requests (one per identifier).
- A POST-based bulk query endpoint.
- A different query parameter syntax (e.g., comma-separated, repeated
  params).

### SSH/CLI fallback

Some ONTAP models (e.g., `CloudMetadata`) are fetched via SSH CLI commands
rather than REST. This is gated by `TypeMapping.cli_command` and
`_is_cloud_cluster()`. Non-ONTAP backends are unlikely to have SSH
fallbacks.

### `fields=*` query parameter

ONTAP supports `?fields=*` to return all fields, and
`?fields=*,expensive_field` to include expensive fields. The URL builder
preserves `fields=*` when present. Other APIs may not support this syntax.

### Cloud cluster gating

`OntapBackend._is_cloud_cluster()` checks whether a cluster is a CVO
(Cloud Volumes ONTAP) instance to decide whether SSH operations are safe.
This is ONTAP-specific and not needed for other backends.

### Singleton endpoints

ONTAP has endpoints that return a single object (e.g., `/cluster`) rather
than a `{"records": [...]}` envelope. This is controlled by
`TypeMapping.response_shape = "singleton"`. Your API may have different
conventions.

---

## Gotchas

### Response envelope shapes

Different APIs use different envelope structures:

- **ONTAP**: `{"records": [...], "num_records": N, "_links": {...}}`
- **DII/AIQUM**: `{"_embedded": {"items": [...]}}` (HAL format)

Set `TypeMapping.records_path` to match your API's envelope. The
`parse_api_response()` function uses `get_nested_value()` with this path
to extract the records list.

### Pagination

`APIWrapper.get_all_records()` handles pagination via a pluggable
`NextPageExtractor`. The default `ontap_next_page_extractor` follows
`_links.next.href`. For APIs with different pagination (offset-based,
cursor-based, token-based), provide a custom extractor:

```python
def dii_next_page_extractor(response: dict[str, Any]) -> str | None:
    return response.get("next_page_url")
```

### Parent-keyed endpoints

Some endpoints require a parent identifier in the URL path (e.g.,
`/storage/volumes/{volume.uuid}/snapshots`). These are declared via:

- `TypeMapping.parent_mapping` -- name of the parent `TypeMapping`.
- `TypeMapping.parent_id_field` -- field on the parent that provides the
  placeholder value.

`OntapBackend` handles these with `build_parameterized_url()` and
grouped-by-parent batch fetching. Your backend must implement equivalent
logic if your API has nested resource endpoints.

### Derived fields

Fields with `cache_strategy="derived"` have no `api_path` and are computed
post-collection via the `post_collection` callable on `FieldMapping`. They
exist only in the cache and cannot be fetched live. Backends must not
attempt to fetch derived fields from the API.

### Batch size

The default chunk size for batched identifier fetches is 100
(`_BATCH_SIZE` in `backends.py`). Per-mapping overrides are available via
`TypeMapping(batch_size=N)` for endpoints with narrower URL length limits.

---

## Configuration and Authentication

Each API type requires its own authentication configuration. Patterns in
the existing codebase:

| API Type | Auth Mechanism | Config Method |
| :--- | :--- | :--- |
| ONTAP | HTTP Basic Auth (per-cluster credentials) | `config.get_user("clusters", cluster_name)` |
| DII | API key header | `config.get_dii_api_settings().api_ro_token` |

Your backend's `__init__` (or lazy client constructor) must resolve
credentials from `Config` and pass the appropriate `auth_header` to
`APIWrapper`.

---

## Cache Database Implications

All backends share the same SQLite cache database (`ClusterMetadataDB`).
When adding models for a new API type:

1. **Table creation is automatic.** `db_schema.py:generate_table_ddl()`
   generates `CREATE TABLE` statements from Pydantic model fields. New
   databases get tables automatically.

2. **Existing databases need migrations.** If deploying against databases
   that predate your models, bump `SCHEMA_VERSION` in `cache/db.py` and
   add an `_upgrade_to_vN()` migration method.

3. **Table names** are the lowercased model class name (e.g.,
   `DiiStoragePool` becomes `diistoragepool`).

See [Cache Models: Schema Migrations](cache-models.md) for the full
migration workflow.

---

## Related Documentation

- [ADR-0012: Unified DataSource Accessor](../decisions/0012-unified-datasource-accessor.md) (superseded)
- [ADR-0013: DataSource as a Thin Facade](../decisions/0013-datasource-as-a-thin-facade-over-the-collector.md) (current)
- [Cache Models](cache-models.md) -- model creation, migrations, and adding new API types
- [Field Mapping Framework](field-mapping.md) -- `FieldMapping` and `TypeMapping` reference
- [DataSource User Guide](../usage/data-source.md) -- consumer-facing usage documentation

### Source files

- `src/pynetappfoundry/data/backends.py` -- Backend ABC and OntapBackend
- `src/pynetappfoundry/data/source.py` -- DataSource facade and `_BACKENDS` registry
- `src/pynetappfoundry/data/_routing.py` -- RoutingDecision and `decide_path()`
- `src/pynetappfoundry/cache/field_mapping.py` -- TypeMapping and FieldMapping
- `src/pynetappfoundry/clients/openapi.py` -- APIWrapper base class
- `src/pynetappfoundry/cache/__init__.py` -- mapping bootstrap
