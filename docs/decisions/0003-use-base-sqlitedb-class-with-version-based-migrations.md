# ADR-0003: Use base SQLiteDB class with version-based migrations

## Status

Accepted

## Context

The project has multiple SQLite database classes (AzEventsDB, MetricDB, EmsEventsDB, ClusterMetadataDB) each with their own ad-hoc schema initialization and migration logic. This leads to:
- Inconsistent migration approaches
- Duplicated boilerplate code
- No unified version tracking

## Decision

Create a base `SQLiteDB` class that all SQLite database classes inherit from. The base class provides:
- Version tracking via `_schema_version` table
- Convention-based upgrade methods (`_upgrade_to_v{N}`)
- Automatic sequential migration on database open

### API Design

```python
class SQLiteDB(ABC):
    SCHEMA_VERSION: ClassVar[int] = 1

    def _init_db(self) -> None:          # Call in __init__
    def _create_schema(self) -> None:     # Subclass implements
    def _upgrade_to_v2(self, conn) -> None:  # Subclass implements as needed
```

## Rationale

1. **Unified migration approach**: A base class ensures consistent behavior across all database classes.

2. **Convention over configuration**: Using method naming convention (`_upgrade_to_v2`, `_upgrade_to_v3`) allows automatic discovery without decorator/registration overhead.

3. **Backwards compatibility**: Existing databases without version tables are detected and treated as v1, allowing smooth migration path.

4. **Atomic upgrades**: Each version upgrade runs within a transaction, ensuring rollback on failure.

5. **No downgrade support**: Standard practice for production databases; simplifies implementation.

### Alternatives Considered

- **Alembic/external migration tool**: Overkill for embedded SQLite; adds external dependency
- **Migration files**: More flexible but adds file management complexity
- **Schema diff approach**: Complex to implement reliably

## Consequences

- All DB classes will inherit from SQLiteDB
- Existing databases migrate smoothly with no data loss
- New columns/tables can be added through versioned upgrade methods
- Each upgrade runs in a transaction for atomicity

## Related Issues

- Issue #111: feat: add base SQLiteDB class with version-based migrations

## Related Documentation

- Database module: `src/pynetappfoundry/db/`
- Cache module: `src/pynetappfoundry/cache/`
