# ADR-0005: UUID index for cache cross-references

## Status

Accepted

## Context

Cache model objects store UUIDs that reference other cached objects (e.g., `SnapMirrorRelationship.policy_uuid` references a policy, `transfer_schedule_uuid` references a `ScheduleInfo`). There was no way to resolve a UUID to its corresponding cache object without manually searching through every list in every category of `CachedClusterMetadata`.

As more types migrate to the field mapping framework and store foreign-key UUIDs, consumers (reports, CLI commands, the config layer) need a fast, simple way to go from a UUID string to the object it represents.

## Decision

Add a `uuid_index` cached property on `CachedClusterMetadata` that builds a flat `dict[str, HasUUID]` keyed by UUID across all 18 model types that have a `uuid: str` field.

Key design choices:

- **Flat dict** (not per-type indices) — ONTAP generates RFC 4122 UUIDs at the cluster level, not scoped per object type, so a flat index is safe and simpler. Per-type indices would require callers to know the type before lookup.
- **`cached_property`** (not `@property`) — the cache is a snapshot (immutable by convention), so the index is built once on first access and cached for the lifetime of the object.
- **Introspection-based discovery** (not explicit enumeration) — automatically walks all model fields and nested BaseModel containers, indexing any list item that satisfies the `HasUUID` protocol. New UUID-bearing types are picked up automatically with zero maintenance.
- **`HasUUID` Protocol** (not `type: ignore`) — the project has nearly zero `type: ignore` usage. A `runtime_checkable` Protocol maintains type safety.

## Rationale

1. **O(1) lookup** — resolving a UUID is a single dict lookup instead of O(n) iteration across all lists.
2. **Type-agnostic** — callers don't need to know which list an object lives in.
3. **Invisible to serialization** — `cached_property` is not included in Pydantic's `model_dump()` or `model_dump_json()`.
4. **Negligible cost** — object count per cluster is small (thousands at most), so build cost is negligible.

## Consequences

- Consumers can resolve foreign-key UUID references with `cached.uuid_index.get(uuid_str)`.
- New UUID-bearing model types are automatically discovered — no manual registration needed.
- The index is read-only and reflects the state of the cache at construction time.

## Related Issues

- Issue #254: feat: add UUID index to CachedClusterMetadata for cross-reference lookups

## Related Documentation

- [Cache System Reference](../reference/cache.md)
