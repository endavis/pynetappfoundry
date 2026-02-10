---
title: Unit Registry
description: Standalone unit registry for ONTAP API field measurements
audience:
  - contributors
tags:
  - development
  - units
  - conversion
---

# Unit Registry

The unit registry maps ONTAP API fields to their units of measurement and provides conversion utilities. It is standalone and decoupled from the cache layer — any code consuming API data can use it.

**Issue:** [#251](https://github.com/endavis/pynetappfoundry/issues/251)

## Architecture

```
UnitRegistry (one per API type: ONTAP, DII, AIQUM)
└── entries: dict[(endpoint, field_path) → UnitEntry]
    ├── UnitEntry("/storage/volumes", "size", BYTES, source)
    ├── UnitEntry("/storage/volumes", "autosize.maximum", BYTES, source)
    └── ...

Unit definitions (shared across all registries)
├── Dimension enum (STORAGE, PERCENTAGE, DURATION, RATE)
└── Unit frozen dataclass (name, symbol, dimension, factor)
    ├── BYTES, KIB, MIB, GIB, TIB, PIB  (binary storage)
    ├── KB, MB, GB, TB, PB               (decimal storage)
    ├── PERCENT                           (percentage)
    ├── SECONDS, MINUTES, HOURS, DAYS    (duration)
    └── BYTES_PER_SEC, KB_PER_SEC, MB_PER_SEC  (rate)
```

Each API type maintains its own `UnitRegistry` instance to avoid endpoint collisions across different APIs.

## Quick Start

### Looking up a field's unit

```python
from pynetappfoundry.units import ontap_registry

# Look up the unit for a volume's size field
entry = ontap_registry.get("/storage/volumes", "size")
if entry:
    print(entry.unit.name)      # "bytes"
    print(entry.unit.symbol)    # "B"
    print(entry.unit.dimension) # Dimension.STORAGE
    print(entry.source)         # "ONTAP REST API: field value is in bytes"
```

### Converting between units

```python
from pynetappfoundry.units import convert, BYTES, GIB, MIB, TIB

# Bytes to GiB
size_gib = convert(1073741824, BYTES, GIB)  # 1.0

# GiB to MiB
size_mib = convert(2, GIB, MIB)  # 2048.0

# TiB to GiB
size_gib = convert(1, TIB, GIB)  # 1024.0
```

### Formatting values for display

```python
from pynetappfoundry.units import format_value, GIB, PERCENT, KB_PER_SEC

format_value(1.5, GIB)            # "1.50 GiB"
format_value(90, PERCENT)          # "90.00%"
format_value(500, KB_PER_SEC)      # "500.00 KB/s"
format_value(2, GIB, precision=0)  # "2 GiB"
```

### Converting an API value using the registry

```python
from pynetappfoundry.units import ontap_registry, convert, GIB

# Get the volume size from an API response
api_size = 10995116277760  # raw value from ONTAP API

# Look up its unit
entry = ontap_registry.get("/storage/volumes", "size")
if entry:
    # Convert from the API's unit (bytes) to GiB
    size_gib = convert(api_size, entry.unit, GIB)
    print(f"Volume size: {size_gib:.2f} GiB")  # "Volume size: 10240.00 GiB"
```

### Listing all entries for an endpoint

```python
from pynetappfoundry.units import ontap_registry

# Get all unit entries for volumes
for entry in ontap_registry.get_by_endpoint("/storage/volumes"):
    print(f"  {entry.api_field_path}: {entry.unit.symbol}")
# Output:
#   autosize.grow_threshold: %
#   autosize.maximum: B
#   autosize.minimum: B
#   autosize.shrink_threshold: %
#   size: B
#   tiering.min_cooling_days: d
```

## Key Components

All components live in `src/pynetappfoundry/units/`.

### Dimension

Enum grouping compatible units. Units within the same dimension can be converted to each other.

| Value | Description | Base Unit |
|-------|-------------|-----------|
| `STORAGE` | Byte-based sizes | `BYTES` (factor=1.0) |
| `PERCENTAGE` | Percentage values | `PERCENT` (factor=1.0) |
| `DURATION` | Time measurements | `SECONDS` (factor=1.0) |
| `RATE` | Throughput rates | `BYTES_PER_SEC` (factor=1.0) |

### Unit

Frozen dataclass representing a unit of measurement.

| Attribute | Type | Description |
|-----------|------|-------------|
| `name` | `str` | Machine-readable identifier (e.g., `"bytes"`, `"gib"`) |
| `symbol` | `str` | Display suffix (e.g., `"B"`, `"GiB"`, `"%"`) |
| `dimension` | `Dimension` | The dimension this unit belongs to |
| `factor` | `float` | Multiplier relative to the base unit of its dimension |

The `factor` represents how many base units equal one of this unit. For example, `GIB.factor = 1073741824.0` because 1 GiB = 1,073,741,824 bytes.

**Conversion formula:** `result = value * from_unit.factor / to_unit.factor`

### Available Units

| Dimension | Unit Constant | Symbol | Factor |
|-----------|--------------|--------|--------|
| Storage (binary) | `BYTES` | B | 1 |
| | `KIB` | KiB | 1,024 |
| | `MIB` | MiB | 1,048,576 |
| | `GIB` | GiB | 1,073,741,824 |
| | `TIB` | TiB | 1,099,511,627,776 |
| | `PIB` | PiB | 1,125,899,906,842,624 |
| Storage (decimal) | `KB` | KB | 1,000 |
| | `MB` | MB | 1,000,000 |
| | `GB` | GB | 1,000,000,000 |
| | `TB` | TB | 1,000,000,000,000 |
| | `PB` | PB | 1,000,000,000,000,000 |
| Percentage | `PERCENT` | % | 1 |
| Duration | `SECONDS` | s | 1 |
| | `MINUTES` | min | 60 |
| | `HOURS` | h | 3,600 |
| | `DAYS` | d | 86,400 |
| Rate | `BYTES_PER_SEC` | B/s | 1 |
| | `KB_PER_SEC` | KB/s | 1,000 |
| | `MB_PER_SEC` | MB/s | 1,000,000 |

You can also look up units by name at runtime:

```python
from pynetappfoundry.units import get_unit, ALL_UNITS

gib = get_unit("gib")        # Returns the GIB Unit instance
print(sorted(ALL_UNITS.keys()))  # All available unit names
```

### UnitEntry

Frozen dataclass mapping an API field to its unit.

| Attribute | Type | Description |
|-----------|------|-------------|
| `endpoint` | `str` | API endpoint base path (e.g., `"/storage/volumes"`). No query params. |
| `api_field_path` | `str` | Dot-notation path in the API response (e.g., `"autosize.maximum"`) |
| `unit` | `Unit` | The unit for this field |
| `source` | `str` | Traceability — where the unit information came from |

### UnitRegistry

Registry class with lookup by `(endpoint, api_field_path)`.

| Method | Description |
|--------|-------------|
| `register(entry)` | Register a single entry. Raises `ValueError` on conflict. |
| `register_many(entries)` | Register a tuple of entries. |
| `get(endpoint, field_path)` | Look up an entry. Returns `None` if not found. |
| `get_by_endpoint(endpoint)` | All entries for an endpoint, sorted by field path. |
| `all_entries()` | All entries, sorted by `(endpoint, field_path)`. |

### Conversion Functions

| Function | Description |
|----------|-------------|
| `convert(value, from_unit, to_unit)` | Convert between units in the same dimension. Raises `IncompatibleUnitsError` if dimensions differ. |
| `format_value(value, unit, precision=2)` | Format a value with its unit symbol (e.g., `"1.50 GiB"`, `"90.00%"`). |

## Registered ONTAP Fields

The `ontap_registry` is pre-populated with entries for all currently mapped fields that have measurement units:

| Endpoint | Field Path | Unit | Source |
|----------|-----------|------|--------|
| `/cluster/nodes` | `controller.memory_size` | BYTES | OpenAPI: "Memory available on the node, in bytes" |
| `/storage/aggregates` | `space.block_storage.size` | BYTES | ONTAP REST API |
| `/storage/volumes` | `autosize.grow_threshold` | PERCENT | ONTAP REST API |
| `/storage/volumes` | `autosize.maximum` | BYTES | ONTAP REST API |
| `/storage/volumes` | `autosize.minimum` | BYTES | ONTAP REST API |
| `/storage/volumes` | `autosize.shrink_threshold` | PERCENT | ONTAP REST API |
| `/storage/volumes` | `size` | BYTES | ONTAP REST API |
| `/storage/volumes` | `tiering.min_cooling_days` | DAYS | ONTAP REST API |

## How to Add Unit Entries for a New Mapping

When adding field mappings for a new ONTAP type that has measurement fields:

### Step 1: Add entries to `ontap_units.py`

Add `UnitEntry` instances to the `_populate()` function in `src/pynetappfoundry/units/ontap_units.py`:

```python
# Inside _populate():
UnitEntry(
    endpoint="/snapmirror/relationships",
    api_field_path="throttle",
    unit=KB_PER_SEC,
    source="ONTAP REST API: 'Throttle in KB/s'",
),
```

The `endpoint` must be the base path without query parameters (e.g., `/snapmirror/relationships`, not `/snapmirror/relationships?fields=*`).

### Step 2: Add tests

Add test cases to `tests/unit/units/test_ontap_units.py`:

```python
def test_snapmirror_throttle_is_kb_per_sec(self) -> None:
    entry = ontap_registry.get("/snapmirror/relationships", "throttle")
    assert entry is not None
    assert entry.unit is KB_PER_SEC
```

Update `test_exact_entry_count` to reflect the new total.

### Step 3: Run checks

```bash
doit check
```

## Adding a Registry for a New API Type

To add unit support for DII, AIQUM, or another API:

1. Create `src/pynetappfoundry/units/<api>_units.py` following the `ontap_units.py` pattern
2. Define and populate a new `UnitRegistry` instance (e.g., `dii_registry`)
3. Export from `src/pynetappfoundry/units/__init__.py`
4. Add tests in `tests/unit/units/test_<api>_units.py`

## Source Files

| File | Purpose |
|------|---------|
| `src/pynetappfoundry/units/__init__.py` | Public API, re-exports |
| `src/pynetappfoundry/units/dimensions.py` | `Dimension` enum, `Unit` dataclass, unit constants |
| `src/pynetappfoundry/units/conversion.py` | `convert()`, `format_value()`, `IncompatibleUnitsError` |
| `src/pynetappfoundry/units/registry.py` | `UnitEntry`, `UnitRegistry` |
| `src/pynetappfoundry/units/ontap_units.py` | ONTAP registry instance with pre-populated entries |
