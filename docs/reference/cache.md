# Cache System

The cache system stores ONTAP cluster metadata locally to enable fast lookups without
repeatedly querying clusters. This document covers the cache architecture, schema
versioning, history tracking, and maintenance.

## Overview

The cache system consists of three main components:

1. **ClusterMetadataDB** - Main cache storing current cluster metadata
2. **CacheHistoryDB** - History database tracking changes over time
3. **MetadataCollector** - Collects metadata from ONTAP clusters

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  ONTAP Cluster  │────▶│ MetadataCollector│────▶│ ClusterMetadata │
└─────────────────┘     └──────────────────┘     │       DB        │
                                │                └─────────────────┘
                                │
                                ▼
                        ┌──────────────────┐
                        │  CacheHistoryDB  │
                        └──────────────────┘
```

## Database Files

Both databases are SQLite files stored in the config directory:

| Database | File | Purpose |
|----------|------|---------|
| ClusterMetadataDB | `{config_dir}/.cache/cluster_metadata.db` | Current cache |
| CacheHistoryDB | `{config_dir}/.cache/cache_history.db` | Change history |

## Schema Architecture

### CachedClusterMetadata Model

The `CachedClusterMetadata` Pydantic model defines the structure of cached data:

```python
class CachedClusterMetadata(BaseModel):
    # Cache metadata
    cluster_name: str
    cached_at: datetime
    cache_version: str = "1.1"  # Schema version

    # Data categories
    cloud: list[CloudMetadata]      # Cloud provider info per node
    cluster: ClusterInfo            # Cluster identity
    nodes: list[NodeInfo]           # Node information
    network: NetworkInfo            # LIFs, broadcast domains
    storage: StorageInfo            # Aggregates, SVMs, cloud targets
    licenses: LicenseInfo           # License information
    ha: HAInfo                      # HA configuration
    relationships: RelationshipsInfo # SnapMirror, peering
```

### Schema Version Tracking

The cache uses semantic versioning to track schema compatibility:

```python
# Current schema version
METADATA_SCHEMA_VERSION = "1.1"

# Minimum version that can be loaded without migration
METADATA_SCHEMA_MIN_COMPATIBLE = "1.0"
```

**Version Format:** `MAJOR.MINOR`

- **MAJOR** - Increment for breaking changes (removed fields, type changes)
- **MINOR** - Increment for backward-compatible changes (new optional fields)

### Schema Version History

| Version | Changes |
|---------|---------|
| 1.0 | Initial schema |
| 1.1 | Changed `cloud` from single `CloudMetadata` to `list[CloudMetadata]` for multi-node support |

## History Tracking

### How It Works

Every time `nf cache refresh` runs:

1. Load the previous snapshot from history (if exists)
2. Check schema compatibility
3. Collect new metadata from the cluster
4. Compute diff between old and new metadata
5. If changes detected (or initial capture), record in history
6. Update the main cache

### Change Records

Each history record contains:

| Field | Type | Description |
|-------|------|-------------|
| `id` | INTEGER | Auto-incrementing ID |
| `cluster_name` | TEXT | Cluster identifier |
| `changed_at` | TEXT | ISO timestamp of change |
| `before_json` | TEXT | Previous metadata (NULL for initial) |
| `after_json` | TEXT | New metadata snapshot |
| `summary_json` | TEXT | List of changes (added/removed/modified) |

### Diff Summary Format

Changes are tracked as a list of change entries:

```json
[
  {
    "category": "nodes",
    "type": "added",
    "entity": "node2"
  },
  {
    "category": "storage.aggregates",
    "type": "modified",
    "entity": "aggr1",
    "field": "used_size",
    "old": 1000000000,
    "new": 1500000000
  },
  {
    "category": "network.data_lifs",
    "type": "removed",
    "entity": "lif1"
  }
]
```

## CLI Commands

### Refresh Cache

```bash
# Refresh single cluster
nf cache refresh cluster1

# Refresh all clusters
nf cache refresh --all

# Refresh with filter
nf cache refresh --all -f '{"env": "Prod"}'

# Verbose mode (show phase-by-phase progress)
nf cache refresh --all -v
```

### View History

```bash
# List all change history
nf cache history list

# List history for specific cluster
nf cache history list cluster1

# Filter by date range
nf cache history list --since 2024-01-01 --until 2024-06-30

# Show more records
nf cache history list -n 50 --offset 20
```

### View Change Details

```bash
# Show full change details
nf cache history show 5

# Output as JSON
nf cache history show 5 --json

# Show formatted diff
nf cache history diff 5

# Filter diff to specific category
nf cache history diff 5 -c nodes
nf cache history diff 5 -c storage.aggregates
```

### Point-in-Time Snapshots

```bash
# View cache state at specific date
nf cache history snapshot cluster1 --date 2024-01-15

# Get full JSON snapshot
nf cache history snapshot cluster1 -d 2024-06-01T12:00:00 --json

# Restore cache to previous state
nf cache history snapshot cluster1 -d 2024-01-15 --restore
```

## Schema Compatibility

### Compatibility Checking

When loading historical snapshots, the system checks schema compatibility:

```python
from pynetappfoundry.cache import is_schema_compatible

# Check if a snapshot version can be loaded
if is_schema_compatible(snapshot_data.get("cache_version")):
    metadata = CachedClusterMetadata.model_validate(snapshot_data)
else:
    # Handle incompatible version
    pass
```

### What Happens with Incompatible Schemas

| Operation | Incompatible Schema Behavior |
|-----------|------------------------------|
| `cache refresh` | Treats as initial capture, logs warning |
| `history snapshot --restore` | Rejects with error message |
| `history show --json` | Returns raw JSON (no validation) |
| `history diff` | Shows summary from stored data |

## Keeping Schemas in Sync

### When to Update Schema Version

Update `METADATA_SCHEMA_VERSION` when modifying `CachedClusterMetadata`:

| Change Type | Version Update | Example |
|-------------|----------------|---------|
| Add optional field | Increment MINOR | Add `new_field: str = ""` |
| Add required field | Increment MAJOR | Add `new_field: str` (no default) |
| Remove field | Increment MAJOR | Delete existing field |
| Rename field | Increment MAJOR | `old_name` → `new_name` |
| Change field type | Increment MAJOR | `count: int` → `count: str` |
| Change nested model | Depends on change | Follow same rules recursively |

### Schema Update Checklist

When modifying the cache schema:

1. **Update the model** in `src/pynetappfoundry/cache/models.py`

2. **Update version constant**:
   ```python
   METADATA_SCHEMA_VERSION = "1.2"  # or "2.0" for breaking changes
   ```

3. **Update minimum compatible version** (if breaking):
   ```python
   METADATA_SCHEMA_MIN_COMPATIBLE = "1.2"
   ```

4. **Document the change** in the Schema Version History table (in models.py docstring and this document)

5. **Update collector** if new fields need to be populated:
   - `src/pynetappfoundry/cache/collector.py`

6. **Update diff logic** if new fields should be tracked:
   - `src/pynetappfoundry/cache/diff.py`

7. **Add tests** for new fields:
   - `tests/unit/cache/test_models.py`
   - `tests/unit/cache/test_diff.py`

8. **Run full test suite**:
   ```bash
   doit check
   ```

### Migration Strategies

For breaking schema changes, consider these strategies:

#### Option 1: Clean Break (Recommended for Major Changes)

Set `METADATA_SCHEMA_MIN_COMPATIBLE` to the new version. Old snapshots
become read-only (viewable via `--json` but not restorable).

```python
METADATA_SCHEMA_VERSION = "2.0"
METADATA_SCHEMA_MIN_COMPATIBLE = "2.0"
```

#### Option 2: Migration Function (For Recoverable Changes)

Add migration logic when loading old snapshots:

```python
def migrate_snapshot(data: dict, from_version: str) -> dict:
    """Migrate snapshot data to current schema."""
    major, minor = parse_schema_version(from_version)

    if major == 1 and minor < 1:
        # Migrate 1.0 → 1.1: wrap single cloud in list
        if "cloud" in data and not isinstance(data["cloud"], list):
            data["cloud"] = [data["cloud"]] if data["cloud"] else []

    data["cache_version"] = METADATA_SCHEMA_VERSION
    return data
```

#### Option 3: Dual Schema Support

Maintain compatibility with multiple versions using Pydantic's
`model_validator`:

```python
@model_validator(mode="before")
@classmethod
def handle_legacy_schema(cls, data: dict) -> dict:
    version = data.get("cache_version", "1.0")
    if version == "1.0":
        # Transform 1.0 format to current format
        pass
    return data
```

## Troubleshooting

### Common Issues

#### "Incompatible schema version" Error

**Cause:** Trying to restore a snapshot created with an older schema version.

**Solution:**
- Use `--json` to view the raw data
- Manually extract needed information
- Or refresh the cache to create a new snapshot

#### History Not Recording Changes

**Cause:** Cache refresh completed but no history entry created.

**Explanation:** History is only recorded when:
- It's the initial capture (no previous snapshot)
- Changes are detected between old and new metadata

If metadata is identical, no history entry is created.

#### Large History Database

**Cause:** Many clusters with frequent changes.

**Solution:** History is append-only by design. To manage size:
- Query with `--limit` and `--offset` for pagination
- Consider periodic archival of old records (manual process)

### Debugging

Enable debug logging to see cache operations:

```bash
# Verbose refresh shows phase timings
nf cache refresh cluster1 -v

# Check log file for detailed information
# Log path is shown at start of refresh
```

## API Reference

### Core Classes

```python
from pynetappfoundry.cache import (
    # Database classes
    ClusterMetadataDB,
    CacheHistoryDB,

    # Collector
    MetadataCollector,

    # Models
    CachedClusterMetadata,
    CloudMetadata,
    ClusterInfo,
    NodeInfo,
    # ... other models

    # Schema versioning
    METADATA_SCHEMA_VERSION,
    METADATA_SCHEMA_MIN_COMPATIBLE,
    is_schema_compatible,
    parse_schema_version,

    # Diff utilities
    compute_diff,
    format_diff_summary,
)
```

### ClusterMetadataDB

```python
db = ClusterMetadataDB(config=config)

# Store metadata
db.set("cluster1", metadata)

# Retrieve metadata
metadata = db.get("cluster1")  # Returns CachedClusterMetadata or None

# List all clusters
clusters = db.list_clusters()  # Returns list of cluster names

# Delete cluster
db.delete("cluster1")

# Always close when done
db.close()
```

### CacheHistoryDB

```python
db = CacheHistoryDB(config=config)

# Record a change
change_id = db.record_change(
    cluster_name="cluster1",
    before_json=old_metadata.model_dump_json() if old_metadata else None,
    after_json=new_metadata.model_dump_json(),
    summary=changes,  # List of change dicts from compute_diff()
)

# Get latest snapshot
snapshot = db.get_latest_snapshot("cluster1")
# Returns: {"after_json": "...", "changed_at": "..."}

# Get snapshot at specific date
snapshot = db.get_snapshot_at_date("cluster1", "2024-01-15")

# Query history
records = db.get_change_history(
    cluster_name="cluster1",  # Optional filter
    limit=50,
    offset=0,
    since="2024-01-01",  # Optional date filter
    until="2024-06-30",  # Optional date filter
)

# Get specific change
record = db.get_change_by_id(5)

# Get total count
count = db.get_history_count(cluster_name="cluster1")

db.close()
```

### MetadataCollector

```python
collector = MetadataCollector(
    api_client=api_client,      # ONTAPAPIClient instance
    cli_client=cli_client,      # ONTAPCLI instance (optional)
    progress_callback=callback,  # Optional progress updates
    aws_sso_config=sso_config,  # Optional AWS SSO config
)

# Collect all metadata for a cluster
metadata = collector.collect_all("cluster1")
```

### Diff Functions

```python
from pynetappfoundry.cache import compute_diff, format_diff_summary

# Compute changes between two snapshots
changes = compute_diff(old_metadata, new_metadata)
# Returns: List[ChangeEntry]

# Format for display
formatted = format_diff_summary(changes)
# Returns: Rich-formatted string
```
