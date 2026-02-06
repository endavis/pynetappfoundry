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
    cache_version: str = "1.0"  # Schema version

    # Data categories
    cloud: list[CloudMetadata]       # Cloud provider info per node
    cluster: ClusterInfo             # Cluster identity
    nodes: list[NodeInfo]            # Node information
    network: NetworkInfo             # LIFs, broadcast domains, DNS, subnets
    storage: StorageInfo             # Aggregates, SVMs, volumes, LUNs, etc.
    licenses: LicenseInfo            # License information
    ha: HAInfo                       # HA configuration
    relationships: RelationshipsInfo # SnapMirror, cluster/SVM peering
    protocols: ProtocolsInfo         # Export policies, CIFS, NFS, S3
```

### Schema Version Tracking

The cache uses semantic versioning to track schema compatibility:

```python
# Current schema version
METADATA_SCHEMA_VERSION = "1.0"

# Minimum version that can be loaded without migration
METADATA_SCHEMA_MIN_COMPATIBLE = "1.0"
```

**Version Format:** `MAJOR.MINOR`

- **MAJOR** - Increment for breaking changes (removed fields, type changes)
- **MINOR** - Increment for backward-compatible changes (new optional fields)

### Schema Version History

| Version | Changes |
|---------|---------|
| 1.0 | Initial schema with comprehensive model coverage |

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
    "field": "disk_count",
    "old": 12,
    "new": 24
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
   METADATA_SCHEMA_VERSION = "1.1"  # or "2.0" for breaking changes
   ```

3. **Update minimum compatible version** (if breaking):
   ```python
   METADATA_SCHEMA_MIN_COMPATIBLE = "1.1"
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

For future breaking schema changes, consider these strategies:

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
    # Add migration steps as needed
    data["cache_version"] = METADATA_SCHEMA_VERSION
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

## Model Reference

All models use `ConfigDict(extra="allow")` for forward compatibility with new API fields.

### Cloud & Cluster

| Model | Key Fields | Description |
|-------|------------|-------------|
| `CloudMetadata` | node, instance_id, provider, region, instance_type | Cloud provider metadata per node |
| `ClusterInfo` | cluster_name, cluster_uuid, ontap_version, model, contact, location | Core cluster identity |
| `NodeInfo` | uuid, name, serial_number, system_id, model, is_epsilon, location | Cluster node information |

### Network

| Model | Key Fields | Description |
|-------|------------|-------------|
| `NetworkLIF` | name, ip_address, netmask, home_node, home_port, role, svm | Logical interface |
| `BroadcastDomain` | uuid, name, ipspace, mtu, ports | Broadcast domain configuration |
| `IPSubnetInfo` | uuid, name, ipspace, broadcast_domain, subnet, gateway, ip_ranges | IP subnet |
| `DNSInfo` | uuid, svm, scope, domains, servers, timeout, attempts | DNS configuration |

**Container:** `NetworkInfo` holds `intercluster_lifs`, `data_lifs`, `management_lifs`, `broadcast_domains`, `ipspaces`, `dns`, `subnets`.

### Storage

| Model | Key Fields | Description |
|-------|------------|-------------|
| `AggregateInfo` | uuid, name, node, state, type, total_size, disk_count, disk_type, raid_type | Storage aggregate |
| `SVMInfo` | uuid, name, state, subtype, root_volume, allowed_protocols, language | Storage VM |
| `VolumeInfo` | uuid, name, svm, state, type, style, size, junction_path, export_policy, snapshot_policy | Volume |
| `QtreeInfo` | id, name, svm, volume, path, security_style, export_policy | Qtree |
| `CloudTargetInfo` | uuid, name, provider_type, server, container, owner, scope | Cloud object store target |
| `FlexCacheInfo` | uuid, name, svm, path, size, origins, global_file_locking_enabled | FlexCache volume |
| `SnapshotPolicyInfo` | uuid, name, svm, enabled, scope, schedules | Snapshot policy |
| `ScheduleInfo` | uuid, name, type, scope, svm, cron, interval | Job schedule |
| `LunInfo` | uuid, name, svm, volume, size, os_type, serial_number, enabled | LUN |
| `IgroupInfo` | uuid, name, svm, protocol, os_type, initiators | Initiator group |
| `QosPolicyInfo` | uuid, name, svm, scope, policy_class | QoS policy |

**Container:** `StorageInfo` holds `aggregates`, `svms`, `cloud_targets`, `volumes`, `qtrees`, `snapshot_policies`, `schedules`, `luns`, `igroups`, `qos_policies`, `flexcaches`.

### Protocols

| Model | Key Fields | Description |
|-------|------------|-------------|
| `ExportPolicyInfo` | id, name, svm, rules | NFS export policy |
| `ExportRuleInfo` | index, clients, protocols, ro_rule, rw_rule, superuser | Export rule |
| `CIFSShareInfo` | name, path, svm, comment, oplocks, encryption | CIFS/SMB share |
| `CIFSServiceInfo` | svm, name, enabled, ad_domain, netbios_aliases | CIFS service config |
| `NFSServiceInfo` | svm, enabled, protocol_v3/v4/v41_enabled | NFS service config |
| `S3BucketInfo` | uuid, name, svm, type, size, versioning_state | S3 bucket |

**Container:** `ProtocolsInfo` holds `export_policies`, `cifs_shares`, `nfs_services`, `cifs_services`, `s3_buckets`.

### Licensing & HA

| Model | Key Fields | Description |
|-------|------------|-------------|
| `LicenseFeature` | name, state, scope | Feature license |
| `CapacityLicense` | name, licensed_capacity, used_capacity | Capacity license |
| `HAInfo` | is_ha, partner_node, ha_state, mediator_address | HA configuration |

**Container:** `LicenseInfo` holds `feature_licenses`, `capacity_licenses`.

### Relationships

| Model | Key Fields | Description |
|-------|------------|-------------|
| `SnapMirrorRelationship` | uuid, source_path, destination_path, relationship_type, state | SnapMirror relationship |
| `ClusterPeer` | uuid, name, remote_cluster_name, peer_addresses, authentication_state | Cluster peer |
| `SVMPeerInfo` | uuid, name, svm, peer_svm, peer_cluster, state, applications | SVM peer |

**Container:** `RelationshipsInfo` holds `snapmirror_destinations`, `cluster_peers`, `svm_peers`.

### Collection Phases

The `MetadataCollector` collects data in these phases (each runs API calls in parallel):

| Phase | REST API Endpoints |
|-------|-------------------|
| `CLOUD` | Cloud provider metadata (CLI-based) |
| `CLUSTER` | `/cluster` |
| `NODES` | `/cluster/nodes` |
| `NETWORK` | `/network/ip/interfaces`, `/network/ethernet/broadcast-domains`, `/cluster/peers` (for ipspaces), `/name-services/dns`, `/network/ip/subnets` |
| `STORAGE` | `/storage/aggregates`, `/svm/svms`, `/cloud/targets`, `/storage/volumes`, `/storage/qtrees`, `/storage/snapshot-policies`, `/cluster/schedules`, `/storage/luns`, `/protocols/san/igroups`, `/storage/qos/policies`, `/storage/flexcache/flexcaches` |
| `LICENSES` | `/cluster/licensing/licenses`, `/cluster/licensing/capacity-pools` |
| `HA` | `/cluster/nodes` (HA fields) |
| `RELATIONSHIPS` | `/snapmirror/relationships`, `/cluster/peers`, `/svm/peers` |
| `PROTOCOLS` | `/protocols/nfs/export-policies`, `/protocols/cifs/shares`, `/protocols/nfs/services`, `/protocols/cifs/services`, `/protocols/s3/buckets` |

## API Reference

### Core Classes

```python
from pynetappfoundry.cache import (
    # Database classes
    ClusterMetadataDB,
    CacheHistoryDB,

    # Collector
    MetadataCollector,

    # Top-level model
    CachedClusterMetadata,

    # Cloud & Cluster
    CloudMetadata, ClusterInfo, NodeInfo,

    # Network
    NetworkInfo, NetworkLIF, BroadcastDomain, IPSubnetInfo, DNSInfo,

    # Storage
    StorageInfo, AggregateInfo, SVMInfo, VolumeInfo, QtreeInfo,
    CloudTargetInfo, FlexCacheInfo, SnapshotPolicyInfo,
    SnapshotScheduleInfo, ScheduleInfo,

    # SAN
    LunInfo, IgroupInfo, QosPolicyInfo,

    # Protocols
    ProtocolsInfo, ExportPolicyInfo, ExportRuleInfo,
    CIFSShareInfo, CIFSServiceInfo, NFSServiceInfo, S3BucketInfo,

    # Licensing & HA
    LicenseInfo, LicenseFeature, CapacityLicense, HAInfo,

    # Relationships
    RelationshipsInfo, SnapMirrorRelationship, ClusterPeer, SVMPeerInfo,

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
