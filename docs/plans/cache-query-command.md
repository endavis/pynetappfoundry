# Plan: Add `nf cache query` Command

## Summary

Create a new `nf cache query` command to query specific fields from cached cluster metadata using dot notation. Supports querying single clusters, all clusters, or a filtered subset.

## CLI Interface

```bash
# Single cluster, single field
nf cache query cluster1 cloud.instance_type
# Output:
# cluster1:
#   cloud.instance_type: m5.xlarge

# Single cluster, multiple fields
nf cache query cluster1 cloud.instance_type cluster.ontap_version
# Output:
# cluster1:
#   cloud.instance_type: m5.xlarge
#   cluster.ontap_version: 9.14.1

# All cached clusters
nf cache query --all cloud.instance_type
# Output:
# cluster1:
#   cloud.instance_type: m5.xlarge
# cluster2:
#   cloud.instance_type: r5.xlarge

# Filtered clusters (using existing -f pattern)
nf cache query -f '{"bu":"Business"}' cloud.provider cloud.region
# Output:
# prod-cluster:
#   cloud.provider: AWS
#   cloud.region: us-east-1

# JSON output
nf cache query cluster1 cloud.instance_type --json
# Output: {"cluster1": {"cloud.instance_type": "m5.xlarge"}}

# Raw output (single cluster only, for scripting)
nf cache query cluster1 cluster.ontap_version --raw
# Output: 9.14.1

# Array access
nf cache query cluster1 nodes[0].name
# Output:
# cluster1:
#   nodes[0].name: node-01
```

## Files to Create/Modify

| File | Action |
|------|--------|
| `src/pynetappfoundry/utils/dict_path.py` | Create |
| `src/pynetappfoundry/cli/commands/cache/query.py` | Create |
| `src/pynetappfoundry/cli/commands/cache/__init__.py` | Modify |
| `tests/unit/utils/test_dict_path.py` | Create |
| `tests/unit/cli/commands/cache/test_query.py` | Create |

## Implementation Details

### 1. `utils/dict_path.py`

Utility for nested dict/list access via dot notation:

- `PathNotFoundError` - custom exception with path, position, and reason
- `get_nested_value(data, path)` - traverse dict with dot notation, supports `nodes[0].name` syntax
- Regex pattern: `^([a-zA-Z_][a-zA-Z0-9_]*)\[(\d+)\]$` for array indices

### 2. `cli/commands/cache/query.py`

New Click command following existing patterns:

```python
@click.command()
@click.argument("cluster", required=False)
@click.argument("fields", nargs=-1, required=True)
@click.option("--filter", "-f", "filter", help='JSON filter: \'{"bu":"Business", "env":"Prod"}\'')
@click.option("--all", "query_all", is_flag=True, help="Query all cached clusters.")
@click.option("--json", "output_json", is_flag=True, help="Output as JSON.")
@click.option("--raw", is_flag=True, help="Output values only, no field names (single cluster only).")
@click.pass_context
def query(ctx, cluster, fields, filter, query_all, output_json, raw):
```

**Cluster selection logic:**
1. If `cluster` specified: query that single cluster
2. If `--all`: query all cached clusters
3. If `--filter/-f`: parse JSON, get filtered clusters from config, query cached data for those
4. Error if none of the above (must specify cluster, --all, or --filter)

**Behavior:**
- `--raw` only valid with single cluster (error otherwise)
- `--json` outputs nested JSON: `{"cluster_name": {"field": value, ...}, ...}`
- Default outputs grouped by cluster with indented fields
- Skips clusters that have no cached data (with warning)
- Error if field path not found (shows which cluster/field failed)

### 3. `cache/__init__.py`

Add import and register command:
```python
from pynetappfoundry.cli.commands.cache.query import query
cache.add_command(query)
```

## Testing

### `test_dict_path.py`
- Simple field access: `cloud.instance_type`
- Array index access: `nodes[0].name`
- Deeply nested: `a.b.c.d`
- Missing field raises `PathNotFoundError`
- Index out of range raises `PathNotFoundError`
- Non-dict access raises `PathNotFoundError`

### `test_query.py`
- Single cluster, single field query
- Single cluster, multiple field query
- `--all` queries all cached clusters
- `--filter` with JSON filter
- `--json` output format
- `--raw` output format (single cluster)
- `--raw` with multiple clusters errors
- Invalid field path error
- Missing cluster error
- No cluster/--all/--filter specified error
- No config directory error

## Verification

1. Run `doit check` to verify all tests pass
2. Manual testing:
   ```bash
   # Single cluster
   nf cache query <cluster> cloud.provider
   nf cache query <cluster> cloud.provider cluster.ontap_version
   nf cache query <cluster> cloud.instance_type --raw
   nf cache query <cluster> nodes[0].name --json

   # Multiple clusters
   nf cache query --all cloud.provider cloud.region
   nf cache query -f '{"env":"prod"}' cloud.instance_type
   nf cache query --all cloud.provider --json

   # Error cases
   nf cache query <cluster> invalid.path  # should error
   nf cache query --all cloud.provider --raw  # should error (raw with multi)
   nf cache query cloud.provider  # should error (no cluster specified)
   ```

## Status

**Implemented**: PR #131 merged, closes #130

## Related Documentation

- [CLI Reference - Cache Commands](../reference/cli.md#cache)
- [Usage Guide - Cluster Metadata Caching](../usage/basics.md#cluster-metadata-caching)
- [ADR-0001: Use SQLite for cluster metadata caching](../decisions/0001-use-sqlite-for-cluster-metadata-caching.md)
