---
title: Fill the Cache and Query It
description: Fill the local cluster cache, check how fresh it is, and read single fields from it for one cluster or many
audience:
  - users
tags:
  - how-to
  - cache
  - ontap
---

# Fill the Cache and Query It

**Goal:** fill the local cache for your ONTAP clusters, confirm it is fresh, and read single fields from it as text, JSON or CSV without contacting the clusters again.

## Before you start

- At least one cluster in the inventory with credentials, confirmed by `nf doctor`: [Add an ONTAP cluster and validate it](add-ontap-cluster.md).
- `nf` can reach the cluster. Only `nf cache refresh` (and `--live`) contacts it; `status` and `query` read the local cache.

## Steps

### 1. See what is cached

```bash
nf cache status
```

A cluster that was never refreshed shows `Not cached`:

```
┃ Cluster         ┃ Cached ┃ Age (days) ┃   Status   ┃ Cache Version ┃
│ cluster1        │   No   │          - │ Not cached │ -             │
...
Summary:
  Configured clusters: 54
  Cached: 52
  Stale (>30 days): 0

Missing cache for: cluster1, cluster54
```

### 2. Refresh the cache

One cluster, with the time each phase took (`-v`):

```bash
nf cache refresh cluster1 -v
```

```
Refreshing cache for 1 cluster(s)...
Log file: data/cache-refresh/logs/cache-refresh_2026-11-25_16-10-32.log

[1/1] cluster1
  |- Cluster info           0.5s (api)
  |- Network                0.7s (api)
  |- Mediator               0.7s (api)
  |- Protocols              0.8s (api)
  |- Nodes                  0.8s (api)
  |- Relationships          0.9s (api)
  |- Storage                1.6s (api)
  |- Licenses               1.8s (api)
  |- Cloud metadata         0.0s (cli)
  `- Total: 6.5s OK

Successfully refreshed 1 cluster(s)
```

Without `-v`, an in-place spinner shows each phase while it runs. The run always writes a log file; its path is on the `Log file:` line.

To refresh every configured cluster, or only the ones matching a filter:

```bash
nf cache refresh --all
nf cache refresh --all -f '{"env": "Prod"}'
nf cache refresh --all --parallel-clusters 8
```

- `--all` (`-a`) takes no cluster name.
- `-f` works only together with `--all`. Without it, `nf cache refresh cluster1 -f ...` stops with `--filter can only be used with --all`.
- `--parallel-clusters` sets how many clusters are processed at once. The default is 4; `1` makes the run strictly sequential.
- A filter that matches nothing prints `No clusters match filter: ...` and exits 0.

### 3. Check how fresh it is

```bash
nf cache status
```

```
                             Cache Status
┏━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┓
┃ Cluster         ┃ Cached ┃ Age (days) ┃   Status   ┃ Cache Version ┃
┡━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━━━━┩
│ cluster2        │  Yes   │          7 │   Fresh    │ 3.0           │
│ …               │        │            │            │               │
│ cluster1        │  Yes   │          0 │   Fresh    │ 3.0           │
│ cluster54       │   No   │          - │ Not cached │ -             │
└─────────────────┴────────┴────────────┴────────────┴───────────────┘
Summary:
  Configured clusters: 54
  Cached: 53
  Stale (>30 days): 0

Missing cache for: cluster54
Run 'nf cache refresh --all' to populate the cache.
```

A cache older than 30 days is `Stale`. Change that limit with `--ttl` (days). With `--ttl 7`, a cluster cached 10 days ago shows as stale (output from a scratch config with three clusters):

```bash
nf cache status --ttl 7
```

```
│ cluster1 │  Yes   │          0 │   Fresh    │ 3.0           │
│ cluster2 │  Yes   │         10 │   Stale    │ 3.0           │
│ cluster3 │   No   │          - │ Not cached │ -             │
...
Summary:
  Configured clusters: 3
  Cached: 2
  Stale (>7 days): 1
```

`Stale` is only a label. `nf cache query` still returns stale data; refresh it with step 2.

### 4. Query a field

Give `nf cache query` a cluster and one or more field paths. Dots walk into nested fields:

```bash
nf cache query cluster1 cluster.version.full
```

```
cluster1:
  cluster.version.full: NetApp Release 9.18.1P8HF1: Fri Oct 23 20:43:35 UTC 2026
```

List the valid paths with `nf cache schema --flat`. It prints one path per line, such as `nodes[N].name`, `nodes[N].serial_number` and `storage.volumes[N].size`. Paths are exact: the node model is `nodes[N].model_` (trailing underscore), and volumes live under `storage.volumes`, not `volumes`.

### 5. Read every item of a list with `[*]`

```bash
nf cache query cluster1 'nodes[*].name' 'nodes[*].serial_number'
```

The output below is from a scratch cache with two nodes, seeded with placeholder serial numbers:

```
cluster1:
  nodes[*].name:
    node1: node1
    node2: node2
  nodes[*].serial_number:
    node1: SN0001
    node2: SN0002
```

Each item is labelled by its `name`, then `svm.name`, then `uuid`, then its position in the list. Pick the label field yourself with `--key`:

```bash
nf cache query cluster1 'storage.volumes["svm.name=svm1"].size' --key uuid
```

```
cluster1:
  storage.volumes["svm.name=svm1"].size:
    11111111-1111-1111-1111-111111111111: 1073741824
    22222222-2222-2222-2222-222222222222: 2147483648
```

Quote paths that contain `[*]` or `["..."]` so the shell does not expand them.

### 6. Select items with a filter predicate

A predicate in `["field=value"]` keeps only the items whose field matches. Use `||` inside it to match several values:

```bash
nf cache query cluster1 'storage.volumes["state=online"].size'
```

```
cluster1:
  storage.volumes["state=online"].size:
    vol1: 1073741824
```

```bash
nf cache query cluster1 'storage.volumes["state=online || state=offline"].name' --raw
```

```
vol1	vol1
vol2	vol2
```

### 7. Query many clusters

```bash
nf cache query --all cluster.version.full --csv
```

```
cluster,cluster.version.full
cluster2,NetApp Release 9.16.1P12: Wed Mar 11 12:37:44 UTC 2026
cluster3,NetApp Release 9.16.1P16HF1: Fri Oct 23 13:26:11 UTC 2026
cluster4,NetApp Release 9.16.1P12: Wed Mar 11 12:37:44 UTC 2026
```

`--all` queries every cluster that is in the cache. A cluster that is not cached is left out without a message, so compare the row count with `nf cache status`. Select clusters by their inventory fields instead with `-f`:

```bash
nf cache query -f '{"env": "Prod"}' cluster.version.full --json
```

With a wildcard or predicate field, `--csv` adds a `key` column and one row per item. From the scratch cache, with two clusters:

```bash
nf cache query --all 'nodes[*].name' 'nodes[*].serial_number' --csv
```

```
cluster,key,nodes[*].name,nodes[*].serial_number
cluster1,node1,node1,SN0001
cluster1,node2,node2,SN0002
cluster2,node1,node1,SN0003
```

### 8. Pick an output format

| Flag | Output |
| :--- | :--- |
| none | Cluster name, then each field with its value |
| `--json` | One JSON object keyed by cluster and field |
| `--csv` | A header row, then one row per cluster (or per item with `[*]` or a predicate) |
| `--raw` | Values only, for scripts. One cluster only; with `--all` or `-f` it stops with `--raw is only valid when querying a single cluster`. For `[*]` and predicate fields it prints `key<TAB>value` per item |

```bash
nf cache query cluster1 cluster.version.full --json
```

```
{"cluster1": {"cluster.version.full": "NetApp Release 9.18.1P8HF1: Fri Oct 23 20:43:35 UTC 2026"}}
```

```bash
nf cache query cluster1 cluster.version.full --raw
```

```
NetApp Release 9.18.1P8HF1: Fri Oct 23 20:43:35 UTC 2026
```

### 9. Bypass the cache for one query

`--live` reads the fields from the cluster instead of the cache. It returns the same shape as a cached query:

```bash
nf cache query cluster1 cluster.version.full --live
```

```
cluster1:
  cluster.version.full: NetApp Release 9.18.1P8HF1: Fri Oct 23 20:43:35 UTC 2026
```

Only the field groups you ask for are fetched, and `nf` warns when a query touches more than three of them. It needs working credentials, because it contacts the cluster.

### 10. Refresh after an upgrade

The cache is a local SQLite file, `<config>/.cache/cluster_metadata.db`. When you upgrade `nf`, the first command that opens it upgrades its schema in place. Whether cached data survives depends on the release:

- Some upgrades only add a column and keep your data.
- Others drop and recreate tables and clear the cached entries ([ADR-0018](../decisions/0018-cache-schema-versioning-and-backward-compatibility-policy.md)). Afterwards `nf cache status` shows those clusters as `Not cached`.

The upgrade is silent; `nf` prints nothing about it. So after upgrading, run `nf cache status`, and refresh whatever shows `Not cached`:

```bash
nf cache refresh --all
```

The `Cache Version` column is the version of the cached data model (`3.0` in the output above), not the SQLite schema version. If you downgrade `nf`, opening a cache written by a newer release fails with `Database version N is newer than supported version M. Downgrade not supported.` Delete `<config>/.cache/cluster_metadata.db` and refresh. To empty the cache on purpose, use `nf cache clear cluster1` or `nf cache clear --all --force`. See [Cache System: Schema Versioning and Migrations](../reference/cache.md#schema-versioning-and-migrations).

## Check it worked

```bash
nf cache status
```

Every cluster you refreshed reads `Yes`, age `0` and `Fresh`, and the summary's `Cached` count rises. Then read a field back:

```bash
nf cache query cluster1 cluster.version.full
```

## If it fails

| You see | Cause | Fix |
| :--- | :--- | :--- |
| `Cluster 'cluster9' not found in configuration.` followed by `Available clusters: ...` | The name is not in the inventory | Use one of the listed names. |
| `Specify a cluster name or use --all to refresh all clusters.` | `nf cache refresh` with no argument | Name a cluster or add `--all`. |
| `--filter can only be used with --all` | `-f` with a cluster name | Use `nf cache refresh --all -f '...'`. |
| `No cached data for cluster 'cluster3', skipping.` then `No results found.` (exit 1) | The cluster has never been refreshed | `nf cache refresh cluster3`. |
| `cluster1: Path 'nodes[*].model' not found at 'nodes[0].model': key not found` (exit 0 when another field in the query is found, 1 when none is) | The path does not exist; the field is `model_` | Look the path up with `nf cache schema --flat`. |
| `cluster1: Path 'volumes["state=online"].size' not found at 'volumes': key not found` (exit 1) | The path starts at the wrong level; volumes are under `storage` | Use `storage.volumes["state=online"].size`. |
| `Must specify CLUSTER, --all, or --filter/-f` or `Must specify at least one FIELD to query` | The command is missing its target or its field | Give a cluster (or `--all`) and at least one field. |
| `--raw is only valid when querying a single cluster` | `--raw` with `--all` or `-f` | Name one cluster, or use `--json` or `--csv`. |
| `Could not find user for type='clusters', object='cluster1'` | No credentials for the cluster, hit by `refresh` or `--live` | [Add an ONTAP cluster and validate it](add-ontap-cluster.md), step 2. |
| `Database version N is newer than supported version M. Downgrade not supported.` | The cache was written by a newer `nf` | Delete `<config>/.cache/cluster_metadata.db`, then refresh. |

## Next

- [Cache System](../reference/cache.md): storage layout, schema versions and the Python API
- [Usage basics: Cluster Metadata Caching](../usage/basics.md#cluster-metadata-caching)
- [Find expiring licenses and export them to CSV](check-licenses.md)
- [Run nf unattended](run-unattended.md): refresh the cache on a schedule
