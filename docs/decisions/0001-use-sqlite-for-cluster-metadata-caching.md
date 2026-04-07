# ADR-0001: Use SQLite for cluster metadata caching

## Status

Accepted

## Decision

Use **SQLite** as the storage backend for caching ONTAP cluster metadata that doesn't change frequently. The cache is stored at `{config_dir}/.cache/cluster_metadata.db` and is manually refreshed via CLI commands (`nf cache refresh`).

## Rationale

1. **SQLite is reliable and portable**: Single-file database requires no external dependencies or services, works across all platforms (Windows, macOS, Linux).

2. **Consistent with existing patterns**: The project already uses SQLite for metrics and events storage in the `db/` module.

3. **Manual refresh model**: Cluster metadata (instance IDs, node serials, licenses, etc.) changes infrequently. Automatic refresh would add complexity and potential for stale data issues. Manual refresh via `nf cache refresh` gives users explicit control.

4. **REST API first with CLI fallback**: Some metadata (like cloud VM instance info) is only available via CLI. The collector tries REST API first for performance, then falls back to CLI for unavailable endpoints.

5. **Pydantic models for type safety**: All cached data uses Pydantic models ensuring validation and serialization consistency.

### Alternatives Considered

- **JSON files**: Simpler but no query capability, harder to manage multiple clusters
- **Redis/external cache**: Overkill for local CLI tool, adds deployment complexity
- **Automatic refresh with TTL**: Adds complexity, harder to reason about data freshness

## Evolution

The storage format evolved from a single JSON blob (schema v1) to per-model SQL
tables (schema v2) in [ADR-0009](0009-sql-table-storage.md). The SQLite backend
and manual refresh model remain unchanged; only the internal table structure
changed to enable SQL-level queries and per-field indexing.

## Related Issues

- Issue #32: feat: add cluster metadata cache for ONTAP clusters
- Issue #38: refactor: move cluster metadata cache to config directory
- Issue #130: feat: add nf cache query command
- Issue #479: doc: refresh cache architecture documentation

## Related Documentation

- Cache module: `src/pynetappfoundry/cache/`
- [Cache System Reference](../reference/cache.md)
- CLI commands: `nf cache refresh`, `nf cache show`, `nf cache query`, `nf cache schema`, `nf cache status`, `nf cache clear`
- CLI Reference: [docs/reference/cli.md](../reference/cli.md#cache)
- Usage Guide: [docs/usage/basics.md](../usage/basics.md#cluster-metadata-caching)
