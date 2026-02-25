# ADR-0007: Deep URL-tree structure with automatic model and mapping discovery

## Status

Accepted

## Decision

Restructure the `cache/` module from a monolithic `models.py` (793 lines, 30+ Pydantic models) and flat `mappings/` directory into a deep directory tree mirroring ONTAP REST API URL paths, with co-located models and mappings. Use `CacheModel.__init_subclass__` auto-registration and a `ModelRegistry` singleton for automatic discovery.

### Directory Structure

Models live at `cache/<api-type>/<api-path>/model.py` and mappings at `cache/<api-type>/<api-path>/mapping.py`, namespaced by API type and mirroring the REST API URL hierarchy:

- `cache/ontap/storage/volumes/model.py` + `mapping.py` (maps to `/storage/volumes`)
- `cache/ontap/cluster/nodes/model.py` + `mapping.py` (maps to `/cluster/nodes`)
- `cache/ontap/protocols/nfs/services/model.py` (maps to `/protocols/nfs/services`)

The `<api-type>` namespace (`ontap/`, `aiqum/`, etc.) prevents path collisions when multiple APIs share endpoint paths like `/cluster`.

### Cache Field and Container Naming

The URL-tree convention extends beyond directory layout to cache field names and container groupings on `CachedClusterMetadata`. Every list field on a container model must use the API resource name from the endpoint path, and every container must correspond to a real ONTAP API top-level namespace.

**Field naming rule:** Convert the API endpoint path to a dotted cache path by replacing `/` with `.` and `-` with `_`. The final segment becomes the field name on the parent container.

| API Endpoint | Cache Path | Container Field |
|---|---|---|
| `/network/ip/interfaces` | `network.ip_interfaces` | `NetworkInfo.ip_interfaces` |
| `/network/ethernet/broadcast-domains` | `network.ethernet_broadcast_domains` | `NetworkInfo.ethernet_broadcast_domains` |
| `/storage/volumes` | `storage.volumes` | `StorageInfo.volumes` |
| `/protocols/nfs/export-policies` | `protocols.nfs_export_policies` | `ProtocolsInfo.nfs_export_policies` |

**Container rule:** Container models (`NetworkInfo`, `StorageInfo`, etc.) group fields that share the same API top-level namespace. A model must not hold fields from a different namespace (e.g., `/name-services/dns` must not live under `NetworkInfo`).

**Model class naming rule:** Model class names should reflect the API resource. For example, `NetworkIpInterface` (not `NetworkLIF`), `NetworkEthernetBroadcastDomain` (not `BroadcastDomain`).

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

2. **Discoverability** - The directory tree, cache field names, and container groupings all mirror ONTAP REST API paths, making it obvious where to find or add a model and how it maps to the API.

3. **Automatic registration** - The `ModelRegistry` singleton enables tooling to discover all models and mappings without hardcoded lists, supporting future features like dynamic inspection and plugin systems.

4. **Explicit imports** - Consumer code imports models from their URL-tree path (e.g., `from pynetappfoundry.cache.ontap.storage.volumes import VolumeInfo`), making the origin of each model immediately clear. Infrastructure (DB, collector, diff, registry) is imported from `pynetappfoundry.cache`.

5. **Scalability** - The three-layer hierarchy prevents circular imports by construction. New models slot in at Layer 2 with no risk of breaking the import DAG.

## Related Issues

- Issue #257: refactor: deep URL-tree structure with automatic model and mapping discovery
- Issue #295: refactor: align cache field names and containers with ONTAP API endpoint hierarchy
- Issue #314: refactor: namespace cache models under api-type directories

## Related Documentation

- [Cache System Reference](../reference/cache.md)
- [Field Mapping Framework Developer Guide](../development/field-mapping.md)
