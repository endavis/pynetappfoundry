---
title: Field Mapping Framework
description: Declarative framework for mapping API/CLI data to cache models
audience:
  - contributors
tags:
  - development
  - cache
  - mapping
---

# Field Mapping Framework

The declarative field mapping framework maps API and CLI responses to cache model objects using data-driven definitions instead of hand-written parsing methods. While originally built for ONTAP, the framework is API-agnostic and supports any REST API through configurable response envelopes and API type tags.

**ADRs:** [ADR-0004](../decisions/0004-declarative-field-mapping-framework.md), [ADR-0006](../decisions/0006-generalize-field-mapping-for-multi-api.md)

## Architecture

```
TypeMapping (one per API object type)
├── api_endpoint    → REST API URL with ?fields= params
├── cli_command     → CLI show command name (optional, default "")
├── model_class     → Pydantic model (e.g., VolumeInfo)
├── records_path    → Dot-path to records in response envelope (default "records")
├── api_type        → API client/registry tag (default "ontap")
└── fields          → tuple of FieldMapping entries
    ├── FieldMapping(cache_attr, api_path, ...)
    ├── FieldMapping(cache_attr, api_path, ...)
    └── ...

Generic parsers read these definitions at runtime:
  parse_api_response()  → list[model_class]
  parse_cli_records()   → list[model_class]  (for CLI-only types)
```

> **Note:** All API-collected types (volumes, aggregates, nodes) use API-only
> field mappings — no `cli_field` entries. CLI parsing is reserved for types
> that genuinely require it (e.g., cloud metadata). Collection uses
> all-or-nothing semantics: every API phase must succeed or the entire
> collection is aborted.

## Key Components

All components live in `src/pynetappfoundry/cache/field_mapping.py`.

### FieldMapping

Maps a single field across three domains: API response, CLI output, and cache model attribute.

| Attribute | Type | Description |
|-----------|------|-------------|
| `cache_attr` | `str` | Model attribute name on the target Pydantic model. |
| `api_path` | `str \| None` | Dot-path for API extraction (e.g., `"svm.name"`, `"aggregates[0].name"`). |
| `cli_field` | `str \| None` | Hyphenated CLI field name (e.g., `"vserver"`). |
| `default` | `Any` | Default value when the field is missing. Default: `""`. |
| `transform` | `Callable \| None` | Custom API extraction function receiving the full record dict. Overrides `api_path`. |
| `cli_transform` | `Callable \| None` | Custom CLI extraction function receiving the full record dict. Overrides `cli_field`. |
| `cache_strategy` | `Literal["cache", "realtime", "derived"]` | How the field is collected and stored. Default: `"cache"`. See [Cache Model Architecture](cache-models.md#field-strategies). |
| `requires_explicit_fetch` | `bool` | Whether this field requires explicit `?fields=` inclusion (ONTAP expensive fields). Default: `False`. |
| `post_collection` | `Callable \| None` | Callable to compute derived field values after collection. Only used when `cache_strategy="derived"`. |

### TypeMapping

Defines a complete API object type mapping.

| Attribute | Type | Description |
|-----------|------|-------------|
| `name` | `str` | Human-readable type name (e.g., `"OntapVolume"`). |
| `model_class` | `type[BaseModel]` | Pydantic model class for the cache object. |
| `api_endpoint` | `str` | REST API endpoint including query params. |
| `cli_command` | `str` | CLI show command name. Default: `""` (empty, optional). |
| `fields` | `tuple[FieldMapping, ...]` | Tuple of field mapping definitions. |
| `id_field` | `str` | Field used for log identification. Default: `"name"`. |
| `records_path` | `str` | Dot-notation path to records list in the API response envelope. Default: `"records"`. Supports nested paths like `"_embedded.items"`. |
| `api_type` | `str` | Tag identifying which API client/unit registry to use. Default: `"ontap"`. |
| `parent_mapping` | `str \| None` | Name of the parent TypeMapping for parameterized endpoints. |
| `parent_id_field` | `str \| None` | Field on the parent model providing the placeholder value. |

Helper methods:

- `api_expected_fields()` — derives top-level API keys from all `api_path` values (used for missing-field logging).
- `cli_expected_fields()` — derives CLI field names from all `cli_field` values.
- `explicit_fetch_fields()` — returns `cache_attr` names for fields with `requires_explicit_fetch=True`.
- `cached_fields()` — returns fields with `cache_strategy="cache"`.
- `realtime_fields()` — returns fields with `cache_strategy="realtime"`.
- `derived_fields()` — returns fields with `cache_strategy="derived"`.

### Generic Parsers

| Function | Input | Output |
|----------|-------|--------|
| `parse_api_response()` | Full API response dict (records extracted via `records_path`) | `list[BaseModel]` |
| `parse_cli_records()` | List of CLI record dicts | `list[BaseModel]` |
| `parse_api_record()` | Single API record dict | `BaseModel` |
| `parse_cli_record()` | Single CLI record dict | `BaseModel` |

### CLI Value Coercion

`_coerce_cli_value(value, default)` handles ONTAP CLI conventions:

| CLI Value | Coercion Rule |
|-----------|---------------|
| `"-"` or `""` | Returns the field's default value |
| `"85%"` | Strips `%` suffix, converts to `int` (when default is `int`) |
| `"true"`, `"yes"`, `"on"` | Converts to `True` (when default is `bool`) |
| `"false"`, `"no"`, `"off"` | Converts to `False` (when default is `bool`) |
| Any other string | Returned as-is (when default is `str`) |

## How to Add a Mapping for a New Type

### Step 1: Create the mapping module

Create `src/pynetappfoundry/cache/<api-type>/<api-path>/mapping.py` co-located with the model:

```python
"""<Type> type mapping definition."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.<api_type>.<api_path>.model import <TypeModel>

<TYPE>_MAPPING = TypeMapping(
    name="<Type>",
    model_class=<TypeModel>,
    api_endpoint="/api/endpoint?fields=*",
    cli_command="<type> show",
    fields=(
        FieldMapping(
            cache_attr="uuid",
            api_path="uuid",
        ),
        FieldMapping(
            cache_attr="name",
            api_path="name",
        ),
        # ... more fields
    ),
)

model_registry.register_mapping("<Type>", <TYPE>_MAPPING)
```

> **Note:** For API-collected types, use `api_path` only — do not add
> `cli_field`. The `cli_field` and `cli_transform` attributes are reserved
> for types that require CLI parsing (see [CLI Fields](#cli-fields) below).

#### Non-ONTAP API example

For APIs with different response envelopes, set `records_path` and `api_type`:

```python
"""AIQUM datacenter cluster mapping."""

from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from mypackage.models import AiqumCluster

AIQUM_CLUSTER_MAPPING = TypeMapping(
    name="AiqumCluster",
    model_class=AiqumCluster,
    api_endpoint="/datacenter/cluster/clusters",
    records_path="_embedded.items",  # AIQUM uses HAL-style envelopes
    api_type="aiqum",
    fields=(
        FieldMapping(cache_attr="name", api_path="name"),
        FieldMapping(cache_attr="uuid", api_path="uuid"),
        FieldMapping(cache_attr="version", api_path="version.full"),
    ),
)
```

The `cli_command` defaults to `""` (empty) since non-ONTAP APIs typically have no CLI equivalent.

### Step 2: Export from the package's `__init__.py`

Add the import and `__all__` entry in `src/pynetappfoundry/cache/<api-type>/<api-path>/__init__.py`:

```python
from pynetappfoundry.cache.<api_type>.<api_path>.mapping import <TYPE>_MAPPING
from pynetappfoundry.cache.<api_type>.<api_path>.model import <TypeModel>

__all__ = ["<TYPE>_MAPPING", "<TypeModel>"]
```

### Step 3: Update the collector

Replace hand-written parsing in the collector with the generic parsers:

```python
from pynetappfoundry.cache.field_mapping import parse_api_response
from pynetappfoundry.cache.<api_type>.<api_path>.mapping import <TYPE>_MAPPING

# API parsing
items = parse_api_response(<TYPE>_MAPPING, response, log_prefix, log_missing_fn)
```

For CLI-only types, use `parse_cli_records` instead:

```python
from pynetappfoundry.cache.field_mapping import parse_cli_records

items = parse_cli_records(<TYPE>_MAPPING, records, log_prefix, log_missing_fn)
```

### Step 4: Register in the inspect command

Add the type to the `INSPECT_TYPES` dict in `src/pynetappfoundry/cli/commands/cache/inspect.py`:

```python
INSPECT_TYPES: dict[str, tuple[TypeMapping, str]] = {
    "volume": (VOLUME_MAPPING, "storage.volumes"),
    "<type>": (<TYPE>_MAPPING, "<cache.dotted.path>"),
}
```

### Step 5: Write tests

Create `tests/unit/cache/mappings/test_<type>.py` with tests covering:

- API record parsing (including nested and missing fields)
- Transform functions (if any)
- Expected field lists (`api_expected_fields()`)

For CLI-only types, also test:

- CLI record parsing (including coercion edge cases)
- `cli_expected_fields()`

## Hand-Written Mappings

Most mappings are now codegen-generated (e.g., `ONTAPVOLUME_MAPPING`, `ONTAPNODERESPONSE_MAPPING`). Two hand-written mappings remain for types that don't map to standard REST GET endpoints:

| Type | Mapping | Model | Notes |
|------|---------|-------|-------|
| Cluster | `CLUSTER_MAPPING` | `ClusterInfo` | Hand-written. Single-object endpoint (no `records` list), uses `parse_api_record()` directly. `is_ha` derived post-collection. |
| CloudMetadata | `CLOUD_METADATA_MAPPING` | `CloudMetadata` | Hand-written. CLI-only (no API endpoint). Computed link fields built as post-processing in collector. |

## Reference: Field Mapping Patterns

The `VOLUME_MAPPING` in `src/pynetappfoundry/cache/ontap/storage/volumes/mapping.py` is the canonical example. It demonstrates all API field mapping patterns:

### Simple field (direct path)

```python
FieldMapping(
    cache_attr="name",
    api_path="name",
)
```

A straightforward top-level API field.

### Nested API field (dot-path)

```python
FieldMapping(
    cache_attr="svm",
    api_path="svm.name",
)
```

The API response has `{"svm": {"name": "vs1"}}`. The dot-path `"svm.name"` is resolved by `get_nested_value()` from `utils/dict_path.py`.

### Array index access

```python
FieldMapping(
    cache_attr="aggregate",
    api_path="aggregates[0].name",
)
```

The API response has `{"aggregates": [{"name": "aggr1"}]}`. The bracket notation `"aggregates[0].name"` extracts the first aggregate's name.

### Wildcard array access

```python
FieldMapping(
    cache_attr="ha_partner_uuids",
    api_path="ha.partners[*].uuid",
    default=[],
)
```

The API response has `{"ha": {"partners": [{"uuid": "a"}, {"uuid": "b"}]}}`. The wildcard `[*]` syntax extracts a value from every item in the array, returning a list. This is handled by `get_nested_value()` from `utils/dict_path.py`. Use `default=[]` for wildcard fields since the result is always a list.

### Custom transform (API)

```python
FieldMapping(
    cache_attr="aggregates",
    default=[],
    transform=_api_aggregates_list,
)
```

When a field needs logic beyond simple path extraction, provide a `transform` function. The function receives the full record dict and returns the extracted value. Note that `api_path` is omitted since the transform handles all extraction.

### Field with default

```python
FieldMapping(
    cache_attr="autosize_grow_threshold",
    api_path="autosize.grow_threshold",
    default=0,
)
```

The `default=0` is the fallback when the field is missing from the API response.

## Transform Functions

### When to use `transform` vs `api_path`

Use `api_path` when the value can be extracted with a simple dot-path (including array indices). Use `transform` when you need:

- Custom logic (filtering, aggregation, conditional extraction)
- Access to multiple fields in the same record
- Type conversions beyond what dot-path extraction provides

### Writing a transform function

Transform functions receive the full record dict and return the extracted value:

```python
def _api_aggregates_list(record: dict[str, Any]) -> list[str]:
    """Extract all aggregate names from API response."""
    return [
        a.get("name", "")
        for a in record.get("aggregates", [])
        if isinstance(a, dict) and a.get("name")
    ]
```

If a transform raises an exception, the framework logs a `TRANSFORM_FAILURE` at error level and **re-raises the exception**. Transform failures are treated as code bugs — they are not silently replaced with defaults.

## CLI Fields

The `cli_field` and `cli_transform` attributes on `FieldMapping` are available for types that require CLI parsing. Currently, all API-collected types (volumes, aggregates, nodes) are API-only and do not use CLI fields.

### When to use `cli_field`

Use `cli_field` when the type is collected via CLI (not API) and the CLI output has a direct field name. The `_coerce_cli_value()` function handles ONTAP CLI conventions (see [CLI Value Coercion](#cli-value-coercion)).

### When to use `cli_transform`

Use `cli_transform` when CLI parsing needs custom logic:

- The CLI field needs splitting (e.g., comma-separated lists)
- Multiple CLI fields contribute to one model attribute
- Custom parsing beyond coercion is needed
