# ADR-0007: Deep URL-tree structure with automatic model and mapping discovery

## Status

Accepted

## Decision

Restructure the `cache/` module from a monolithic `models.py` (793 lines, 30+ Pydantic models) and flat `mappings/` directory into a deep directory tree mirroring ONTAP REST API URL paths, with co-located models and mappings. Use `CacheModel.__init_subclass__` auto-registration and a `ModelRegistry` singleton for automatic discovery.

### Directory Structure

Models live at `cache/<api-path>/model.py` and mappings at `cache/<api-path>/mapping.py`, mirroring the ONTAP REST API URL hierarchy:

- `cache/storage/volumes/model.py` + `mapping.py` (maps to `/storage/volumes`)
- `cache/cluster/nodes/model.py` + `mapping.py` (maps to `/cluster/nodes`)
- `cache/protocols/nfs/services/model.py` (maps to `/protocols/nfs/services`)

### Three-Layer Import Hierarchy

Imports flow upward only (DAG guaranteed, no circular deps):

1. **Layer 1**: `_base.py` (CacheModel, HasUUID, schema versioning) and `_registry.py` (ModelRegistry)
2. **Layer 2**: Leaf `model.py` files (import only from `_base.py`)
3. **Layer 3**: Container models (`storage/model.py`, `network/model.py`, `protocols/model.py`, `_metadata.py`) import leaf models

### Auto-Registration

- `CacheModel.__init_subclass__` auto-registers every subclass in `ModelRegistry` at class-definition time
- Deferred import of `_registry` inside `__init_subclass__` avoids circular deps with `_base.py`
- Each `mapping.py` explicitly calls `model_registry.register_mapping()` at module level
- `__init__.py` chain triggers all imports, so registration happens as a side effect
- `CachedClusterMetadata` uses `register=False` (top-level container, not a data type)

## Rationale

1. **Locality** - Adding a new ONTAP type requires touching only one directory (model + mapping + `__init__.py`), not 4+ scattered files (models.py, mappings/, `__init__.py` re-exports, collector imports).

2. **Discoverability** - The directory tree mirrors ONTAP REST API paths, making it obvious where to find or add a model.

3. **Automatic registration** - The `ModelRegistry` singleton enables tooling to discover all models and mappings without hardcoded lists, supporting future features like dynamic inspection and plugin systems.

4. **Import stability** - Consumer code uses `from pynetappfoundry.cache import VolumeInfo` (unchanged), while internal imports use direct paths to leaf modules, avoiding circular deps.

5. **Scalability** - The three-layer hierarchy prevents circular imports by construction. New models slot in at Layer 2 with no risk of breaking the import DAG.

## Related Issues

- Issue #257: refactor: deep URL-tree structure with automatic model and mapping discovery

## Related Documentation

- [Cache System Reference](../reference/cache.md)
- [Field Mapping Framework Developer Guide](../development/field-mapping.md)
