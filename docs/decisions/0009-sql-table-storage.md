# ADR-0009: Per-Model SQL Table Storage for Cache Layer

## Status

Accepted

## Context

The cluster metadata cache stored all data as a single JSON blob in the
`cluster_metadata` table (`metadata_json TEXT` column). This prevented
SQL-level queries, per-field updates, and granular storage.

Since no production consumers depend on the v1 schema, this is a clean-slate
rebuild of the storage layer.

## Decision

Replace the JSON blob with **per-model SQL tables** generated from Pydantic
model field definitions:

- **DDL generation** (`db_schema.py`): Walk `CachedClusterMetadata.model_fields`
  to discover storable models. Map Python types to SQL column types. Generate
  `CREATE TABLE` statements at import time via a `TABLE_REGISTRY`.
- **Raw `sqlite3`**: No ORM. Parameterised queries only.
- **`_row_id` PK**: Every table uses `_row_id INTEGER PRIMARY KEY AUTOINCREMENT`
  to avoid collisions when UUID fields are empty (common for test fixtures and
  new clusters).
- **Container models** (e.g. `StorageInfo`, `NetworkInfo`) do **not** get their
  own tables — their child list fields are stored directly.
- **Sub-models stored as JSON**: Nested list/dict fields within a model (e.g.
  `OntapNodeResponse.cluster_interfaces`) are serialised to JSON TEXT columns.
  They lack independent identity and don't need separate tables.
- **`_extra_json` column**: Every model table has this column to preserve
  `extra="allow"` fields from newer ONTAP versions.
- **`_uuid_index` table**: ~~Cross-model UUID lookup, populated on `set()`.~~
  Removed in schema v3 — never queried in production. UUID resolution uses
  the in-memory `CachedClusterMetadata.uuid_index` cached property
  (see [ADR-0005](0005-uuid-index-for-cache-cross-references.md)).
- **v1 → v2 migration**: Reads JSON blobs, decomposes into new tables, rebuilds
  the envelope table without `metadata_json`.

### Alternatives Considered

- **SQLModel / SQLAlchemy**: Rejected. SQLModel is 0.0.x, 20-40x slower for
  bulk inserts, and conflicts with Pydantic `extra="allow"` inheritance.
- **Keep JSON blob + add indexed views**: Would not enable per-field updates
  or eliminate full-blob serialization on every write.

## Consequences

### Positive

- Enables SQL-level queries via `query_model()` with parameterised filters
- `is_stale()` reads only the envelope row — no full metadata deserialisation
- Per-field indexing possible (e.g. `CREATE INDEX ON ontapvolume (name)`)
- `export_json()` / `import_json()` provide backward-compatible JSON I/O
- `_extra_json` preserves forward compatibility with newer ONTAP versions

### Negative

- More complex `set()` / `get()` — decompose into ~29 tables on write,
  reconstruct from ~29 tables on read
- Column names must be quoted to handle SQLite reserved words (e.g. `"index"`)
- Schema migrations needed when models add/remove fields

## Related Issues

- Issue #309: feat: per-model SQL table storage for cache layer
- Issue #301: feat: field annotations, OpenAPI codegen, and SQL cache storage
- Issue #479: doc: refresh cache architecture documentation

## Related Documentation

- Cache module: `src/pynetappfoundry/cache/`
- [Cache System Reference](../reference/cache.md) — Storage Architecture section documents the per-model SQL table layout
- ADR-0001: [Use SQLite for cluster metadata caching](0001-use-sqlite-for-cluster-metadata-caching.md)
- ADR-0003: [Base SQLiteDB class with version-based migrations](0003-use-base-sqlitedb-class-with-version-based-migrations.md)
