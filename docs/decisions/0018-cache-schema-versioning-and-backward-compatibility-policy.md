# ADR-0018: Cache schema versioning and backward-compatibility policy

## Status

Accepted

## Context

[ADR-0001](0001-use-sqlite-for-cluster-metadata-caching.md) established SQLite as the cache substrate for cluster metadata, and [ADR-0003](0003-use-base-sqlitedb-class-with-version-based-migrations.md) established the version-based migration mechanism (the `_schema_version` table and the convention-based `_upgrade_to_v{N}()` methods on the shared `SQLiteDB` base class). Together they document the **mechanism** but not the **contract**: what migrations may do, what users must accept, and what downgrade means.

The cache is a derived store. Its on-disk shape changes whenever cached models are refactored — the v3 → v4 migration that accompanied the nested-model refactor ([ADR-0011](0011-nested-models-to-replace-flat-model-pattern.md)) dropped and recreated every per-model table, losing cached data on upgrade. That precedent has not been written down anywhere as policy, so each new cache-touching change re-litigates "what are we allowed to do here?"

This ADR records the contract behind the mechanism so future cache-schema changes (and reviewers) have something to point to.

Scope: this ADR covers the on-disk SQLite schema version (`SCHEMA_VERSION` in `cache/db.py`, currently `5`). The snapshot-level `METADATA_SCHEMA_VERSION` (`cache/_base.py`) is a separate mechanism with its own contract documented in [Cache System Reference](../reference/cache.md); it is out of scope here.

## Decision

1. **Compatibility contract: rebuild-tolerant.** The cache is a derived store. Deleting `{config_dir}/.cache/cluster_metadata.db` and running `nf cache refresh` is an acceptable contributor or user fallback for any migration concern. The project does not promise formal cross-upgrade preservation of cached data.

2. **Column lifecycle.**
   - **Add a column:** bump `SCHEMA_VERSION` and write an idempotent `_upgrade_to_v{N}()` that runs `ALTER TABLE … ADD COLUMN`. Idempotency is required because earlier migration chains may have recreated the table with the current DDL, so the migration must check `PRAGMA table_info` before issuing the `ALTER`.
   - **Rename or remove a column:** drop and recreate the affected table(s). Cached data for that table is lost on upgrade. The v3 → v4 migration ([ADR-0011](0011-nested-models-to-replace-flat-model-pattern.md), issue #444) is the precedent. Clear the affected envelope row(s) so collectors detect missing data and trigger a refresh.
   - Deprecate-in-place is **not** the default. Cache rebuild is preferred over carrying dead columns forward.

3. **Migration atomicity.** Each version upgrade runs in a transaction (already established by [ADR-0003](0003-use-base-sqlitedb-class-with-version-based-migrations.md)). Interrupted migrations roll back and the database stays at the prior version. Migrations must be safe to re-run from any prior version; the migration chain is replayed in sequence on every open.

4. **Downgrade: not supported.** Opening a database whose recorded version exceeds the code's `SCHEMA_VERSION` raises `SchemaUpgradeError` (`db/base.py`). Users who downgrade `pynetappfoundry` must manually delete the cache database. This matches the no-downgrade stance already taken by [ADR-0003](0003-use-base-sqlitedb-class-with-version-based-migrations.md).

5. **Visibility: internal.** `SCHEMA_VERSION` is an implementation detail. It is not surfaced in CLI output, log messages, or release notes. Users observe migration effects only as side effects (e.g. an empty cache after a destructive migration). Adding migration logging is a possible future enhancement, not part of this contract.

6. **Out of scope.** `METADATA_SCHEMA_VERSION` (snapshot-level) is a separate mechanism with its own contract documented in [Cache System Reference](../reference/cache.md). This ADR covers only the on-disk SQLite schema version.

## Rationale

- **The cache is derived, so promising preservation costs more than it gives.** Cached data can be reconstructed from the live ONTAP API at any time via `nf cache refresh`. Promising cross-upgrade preservation would constrain contributors (forcing in-place column transforms, multi-step migrations, compatibility shims) for negligible user benefit. Users who want preservation can refresh.

- **Drop-and-recreate is simpler than transforming 50+ models in place.** When a refactor changes the shape of cached models (as ADR-0011 did), the on-disk transform problem grows with the model count. The v3 → v4 migration validated the trade-off: a single destructive migration plus a `nf cache refresh` is cheaper to write, review, and maintain than a per-model in-place column transform.

- **No-downgrade is the standard practice for embedded migration frameworks.** [ADR-0003](0003-use-base-sqlitedb-class-with-version-based-migrations.md) already takes this position to keep the migration framework simple. Carrying down-migrations would double the maintenance burden for a fallback (cache delete) that already exists.

- **Internal visibility matches the scope of the contract.** Surfacing `SCHEMA_VERSION` in CLI output or release notes would invite users to expect a stability guarantee the project does not provide. Keeping it internal aligns visibility with the actual contract.

## Consequences

- Contributors may propose data-destructive cache migrations without a preservation justification. The bar is "is this the right shape going forward?" not "can we preserve the data?"

- Users have no formal cache-continuity guarantee across upgrades. They get continuity when migrations happen to be additive (`ALTER TABLE … ADD COLUMN`) and lose cached data when migrations are destructive (drop and recreate). In all cases, `nf cache refresh` restores the cache.

- Migration logging is not required by this contract but may be added as a future enhancement (e.g. a one-line log when a migration runs, surfacing the destructive case to the user).

- The "Cache Schema Pitfalls" section in `AGENTS.md` remains the operational checklist for contributors adding fields to cached models. This ADR provides its policy basis.

## Related Issues

- Issue #620: doc: ADR codifying cache-schema versioning and backward-compat policy (this ADR)
- Issue #444: refactor: nested-model layout for cached ONTAP models (v3 → v4 destructive precedent)
- Issue #111: feat: add base SQLiteDB class with version-based migrations (the migration mechanism)
- Issue #32: feat: add cluster metadata cache for ONTAP clusters (the original cache decision)

## Related Documentation

- [ADR-0001: Use SQLite for cluster metadata caching](0001-use-sqlite-for-cluster-metadata-caching.md) -- the cache substrate decision
- [ADR-0003: Use base SQLiteDB class with version-based migrations](0003-use-base-sqlitedb-class-with-version-based-migrations.md) -- the migration mechanism
- [ADR-0009: Per-Model SQL Table Storage for Cache Layer](0009-sql-table-storage.md) -- the per-model table layout that migrations evolve
- [ADR-0011: Nested models to replace flat model pattern](0011-nested-models-to-replace-flat-model-pattern.md) -- the v3 → v4 destructive migration precedent
- [Cache System Reference](../reference/cache.md) -- "SQLite database schema versioning" section, plus the snapshot-level `METADATA_SCHEMA_VERSION` contract that this ADR explicitly does not cover
- `AGENTS.md` "Cache Schema Pitfalls" -- operational checklist for contributors adding fields to cached models
