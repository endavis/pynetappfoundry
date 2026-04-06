# ADR-0010: ClusterEntry and namespace access pattern

## Status

Accepted

## Context

The previous cache integration approach used `_enrich_with_cache()` in `Config.__init__()` to eagerly open the SQLite cache database and merge cached metadata into every cluster's config dict. This had several problems:

- **Startup latency**: The cache DB was opened and queried at Config init time, even when scripts never accessed cached data.
- **Coupling**: Static TOML configuration and dynamic cache data were mixed into the same flat dict, making it unclear which keys came from config files vs. the cache.
- **No namespace isolation**: All cached fields lived in the same dict, risking key collisions as more API types (OCCM, AIQUM, DII) were added.

## Decision

Replace `_enrich_with_cache()` with `ClusterEntry` — a `MutableMapping[str, Any]` wrapper that provides:

1. **Dict-like backward compatibility** for TOML config keys (`__getitem__`, `get`, `keys`, `items`, etc.), so existing code that treats cluster data as a plain dict continues to work unchanged.
2. **Lazy `@cached_property` namespace accessors** (`.ontap`, `.occm`, `.aiqum`, `.dii`) that open the cache database only on first access, fetch the relevant `CachedClusterMetadata`, close the DB, and cache the result.
3. **Attribute fallback** via `__getattr__` delegating to the underlying config dict.

Integration point: `Config._wrap_clusters()` replaces each raw cluster dict with a `ClusterEntry` instance after TOML parsing completes.

## Rationale

1. **Lazy loading** — The cache DB is never opened unless a namespace property is actually accessed, eliminating unnecessary startup latency.
2. **Clean separation** — TOML config keys are accessed via dict interface; cached metadata is accessed via named properties. No mixing.
3. **Namespace isolation** — Each API type gets its own `@cached_property`, preventing key collisions and making it explicit which API the data belongs to.
4. **Extensibility** — Adding a new API type requires only a new `@cached_property` on `ClusterEntry`.
5. **Backward compatible** — `MutableMapping` interface means existing dict-based code works without changes.

### Alternatives Considered

- **Keep eager loading (`_enrich_with_cache()`)**: Rejected — imposed startup latency, tightly coupled config and cache data, no namespace isolation.
- **Merge all namespaces into a flat dict**: Rejected — collision risk between API types, no isolation, unclear data provenance.
- **Separate cache accessor object (not dict-like)**: Rejected — would break existing code that treats cluster data as a dict.

## Consequences

### Positive

- Faster startup for scripts that don't access cached data
- Clean separation between static config (TOML) and dynamic cache (SQLite)
- Extensible namespace pattern for future API types (OCCM, AIQUM, DII)
- Full backward compatibility with existing dict-based access patterns

### Negative

- Two access patterns coexist: dict syntax for config keys, property syntax for cached namespaces
- Developers must know that `.ontap` triggers a DB read on first access

## Related Issues

- Issue #320: feat: replace `_enrich_with_cache` with ClusterEntry lazy cache accessors
- Issue #301: feat: field annotations, OpenAPI codegen, and SQL cache storage
- Issue #352: refactor: lazy `_reconstruct_metadata` to avoid loading all model tables on every `get()`
- Issue #464: refactor: convert `nf licenses get` to use cache + on-demand fetch (pilot migration to ClusterEntry namespace access)

## Related Documentation

- `ClusterEntry` implementation: `src/pynetappfoundry/core/cluster_entry.py`
- `LazyClusterMetadata` implementation: `src/pynetappfoundry/cache/_lazy.py`
- Config integration: `src/pynetappfoundry/core/config.py` (`_wrap_clusters()`)
- [ADR-0004: Declarative field mapping framework](0004-declarative-field-mapping-framework.md)
- [ADR-0009: Per-model SQL table storage](0009-sql-table-storage.md)
- [Cache reference](../reference/cache.md)
- [Cache models development guide](../development/cache-models.md)
