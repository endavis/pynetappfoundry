---
title: Field Mapping Framework
description: Declarative framework for mapping ONTAP API/CLI data to cache models
audience:
  - contributors
tags:
  - development
  - cache
  - mapping
---

# Field Mapping Framework

The declarative field mapping framework maps ONTAP REST API and CLI responses to cache model objects using data-driven definitions instead of hand-written parsing methods.

**ADR:** [ADR-0017](../decisions/0017-declarative-field-mapping-framework.md)

## Architecture

```
TypeMapping (one per ONTAP object type)
├── api_endpoint    → REST API URL with ?fields= params
├── cli_command     → CLI show command name
├── model_class     → Pydantic model (e.g., VolumeInfo)
└── fields          → tuple of FieldMapping entries
    ├── FieldMapping(cache_attr, api_path, cli_field, ...)
    ├── FieldMapping(cache_attr, api_path, cli_field, ...)
    └── ...

Generic parsers read these definitions at runtime:
  parse_api_response()  → list[model_class]
  parse_cli_records()   → list[model_class]
```

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

### TypeMapping

Defines a complete ONTAP object type mapping.

| Attribute | Type | Description |
|-----------|------|-------------|
| `name` | `str` | Human-readable type name (e.g., `"Volume"`). |
| `model_class` | `type[BaseModel]` | Pydantic model class for the cache object. |
| `api_endpoint` | `str` | REST API endpoint including query params. |
| `cli_command` | `str` | CLI show command name. |
| `fields` | `tuple[FieldMapping, ...]` | Tuple of field mapping definitions. |
| `id_field` | `str` | Field used for log identification. Default: `"name"`. |

Helper methods:

- `api_expected_fields()` — derives top-level API keys from all `api_path` values (used for missing-field logging).
- `cli_expected_fields()` — derives CLI field names from all `cli_field` values.

### Generic Parsers

| Function | Input | Output |
|----------|-------|--------|
| `parse_api_response()` | Full API response dict (with `"records"` key) | `list[BaseModel]` |
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

Create `src/pynetappfoundry/cache/mappings/<type>.py`:

```python
"""<Type> type mapping definition."""

from __future__ import annotations

from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.models import <TypeModel>

<TYPE>_MAPPING = TypeMapping(
    name="<Type>",
    model_class=<TypeModel>,
    api_endpoint="/api/endpoint?fields=*",
    cli_command="<type> show",
    fields=(
        FieldMapping(
            cache_attr="uuid",
            api_path="uuid",
            cli_field="instance-uuid",
        ),
        FieldMapping(
            cache_attr="name",
            api_path="name",
            cli_field="<type>",
        ),
        # ... more fields
    ),
)
```

### Step 2: Export from the mappings package

Add the import and `__all__` entry in `src/pynetappfoundry/cache/mappings/__init__.py`:

```python
from pynetappfoundry.cache.mappings.<type> import <TYPE>_MAPPING

__all__ = ["VOLUME_MAPPING", "<TYPE>_MAPPING"]
```

### Step 3: Update the collector

Replace hand-written parsing in the collector with the generic parsers:

```python
from pynetappfoundry.cache.field_mapping import parse_api_response, parse_cli_records
from pynetappfoundry.cache.mappings import <TYPE>_MAPPING

# API parsing
items = parse_api_response(<TYPE>_MAPPING, response, log_prefix, log_missing_fn)

# CLI parsing
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
- CLI record parsing (including coercion edge cases)
- Transform functions (if any)
- Expected field lists (`api_expected_fields()`, `cli_expected_fields()`)

## Migrated Types

| Type | Mapping | Model | Fields | Notes |
|------|---------|-------|--------|-------|
| Volume | `VOLUME_MAPPING` | `VolumeInfo` | 21 | Pilot migration. Uses transforms for aggregate list extraction. |
| Aggregate | `AGGREGATE_MAPPING` | `AggregateInfo` | 28 | Deeply nested API paths (`block_storage.primary.*`). Explicit `?fields=*,is_spare_low,sidl_enabled`. |
| Node | `NODE_MAPPING` | `NodeInfo` | 20 | Wildcard `[*]` syntax for list fields. `field_validator` for int→str coercion. 14 API-only fields. |

## Reference: Field Mapping Patterns

The `VOLUME_MAPPING` in `src/pynetappfoundry/cache/mappings/volume.py` is the canonical example. It demonstrates all field mapping patterns:

### Simple field (direct path)

```python
FieldMapping(
    cache_attr="name",
    api_path="name",
    cli_field="volume",
)
```

Both API and CLI have a straightforward top-level field.

### Nested API field (dot-path)

```python
FieldMapping(
    cache_attr="svm",
    api_path="svm.name",
    cli_field="vserver",
)
```

The API response has `{"svm": {"name": "vs1"}}`. The dot-path `"svm.name"` is resolved by `get_nested_value()` from `utils/dict_path.py`.

### Array index access

```python
FieldMapping(
    cache_attr="aggregate",
    api_path="aggregates[0].name",
    cli_field="aggregate",
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
    cli_transform=_cli_aggregates_list,
)
```

When a field needs logic beyond simple path extraction, provide a `transform` function. The function receives the full record dict and returns the extracted value. Note that `api_path` and `cli_field` are omitted since the transforms handle all extraction.

### Field with default and coercion

```python
FieldMapping(
    cache_attr="autosize_grow_threshold",
    api_path="autosize.grow_threshold",
    cli_field="autosize-grow-threshold-percent",
    default=0,
)
```

The `default=0` serves two purposes: it's the fallback when the field is missing, and it tells `_coerce_cli_value()` to treat the CLI value as an integer (stripping any `%` suffix).

## Transform Functions

### When to use `transform` vs `api_path`

Use `api_path` when the value can be extracted with a simple dot-path (including array indices). Use `transform` when you need:

- Custom logic (filtering, aggregation, conditional extraction)
- Access to multiple fields in the same record
- Type conversions beyond what dot-path extraction provides

### When to use `cli_transform` vs `cli_field`

Use `cli_field` when the CLI output has a direct field name and `_coerce_cli_value()` handles the type conversion. Use `cli_transform` when:

- The CLI field needs splitting (e.g., comma-separated lists)
- Multiple CLI fields contribute to one model attribute
- Custom parsing beyond coercion is needed

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

If a transform raises an exception, the framework catches it, logs a debug message, and uses the field's `default` value.
