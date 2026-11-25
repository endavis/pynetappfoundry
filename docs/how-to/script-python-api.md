---
title: Script Against the Python API
description: Load the config in Python, find clusters, read cached cluster data through ClusterEntry.ontap, and query with DataSource
audience:
  - users
tags:
  - how-to
  - python
  - api
---

# Script Against the Python API

**Goal:** write a Python script that loads the config, finds clusters, and reads their data from the cache, with a live read when you ask for one.

## Before you start

- `pynetappfoundry` installed in the environment that runs the script: `uv add pynetappfoundry` or `pip install pynetappfoundry`.
- Clusters in the inventory: [Add an ONTAP cluster and validate it](add-ontap-cluster.md).
- A filled cache, for the reads below: `nf cache refresh --all`. Check it with `nf cache status`. See [Basic Usage: Cluster Metadata Caching](../usage/basics.md#cluster-metadata-caching).
- Run the script from the directory that holds `config/`, or pass the config directory to `Config`.

## Steps

### 1. Load the config and find clusters

`Config()` reads `./config`. `Config("path/to/config")` reads another directory. It also creates `data/db`, `data/files` and `data/output` in the current directory. Clusters are in `config.data["clusters"]`, keyed by name. Each is a `ClusterEntry`, which behaves as a dict of its config keys:

```python
from typing import cast

from pynetappfoundry import Config
from pynetappfoundry.core.cluster_entry import ClusterEntry

config = Config()
print(sorted(config.data["clusters"]))

cluster = cast(ClusterEntry, config.data["clusters"]["cluster1"])
print(cluster["ip"], cluster.get("env"))
```

```
['cluster1', 'cluster2', 'cluster3']
192.0.2.10 Prod
```

To find clusters by their descriptive keys, use `config.search`. The built-in `scope` key matches the [scope](use-scopes.md) an object belongs to, and `config.get_scope` reports it:

```python
prod = config.search("clusters", {"env": "Prod"})
print(sorted(prod))
print(sorted(config.search("clusters", {"scope": "bu1"})))
print(config.get_scope("clusters", "cluster3"), config.get_scope("clusters", "cluster1"))
```

```
['cluster1', 'cluster3']
['cluster3']
bu1 None
```

See [Config schema: Searching Resources](../reference/config-schema.md#searching-resources) for the search syntax.

### 2. Read cluster data through ClusterEntry.ontap

`cluster.ontap` is the preferred way to read one cluster. It serves the cache that `nf cache refresh` fills. When the cluster has no cache, it fetches live instead. It returns `None` only when there is no config to fetch with.

```python
metadata = cluster.ontap
if metadata is not None:
    print(metadata.cluster.name)
    for node in metadata.nodes:
        print(node.name, node.state)
    for vol in metadata.storage.volumes:
        print(vol.name, vol.autosize.mode)
```

```
cluster1
cluster1-01 up
cluster1-02 down
vol_logs grow
vol_data_02 grow_shrink
vol_data_01 off
```

Each field group, such as `nodes` or `storage`, loads when you first read it. To skip the cache and fetch every group live, use `Config(no_cache=True)`. That needs a reachable cluster and valid credentials.

### 3. Query with DataSource

Use `DataSource` for new code that reads more than a whole cluster: it filters, projects fields, and returns typed models from the cache or the live API. Pass `source="cache"` to read only the cache, with no request:

```python
from pynetappfoundry.data.source import DataSource
from pynetappfoundry.models.ontap.storage.volumes.model import OntapVolume

ds = DataSource(config)

for vol in ds.query(OntapVolume, cluster="cluster1", source="cache").filter(state="online"):
    print(vol.name, vol.size, vol.autosize.mode)
```

```
vol_logs 1073741824 grow
vol_data_02 1073741824 grow_shrink
vol_data_01 1073741824 off
```

`.filter()` takes keyword arguments for top-level fields, or a dict for dotted paths such as `{"autosize.mode": "off"}`. `.where()` takes a SQL-like expression and works only on the cache. `.fields()` limits the fields that are filled in:

```python
rows = list(
    ds.query(OntapVolume, cluster="cluster1", source="cache")
    .where("autosize.mode != 'grow_shrink'")
    .fields("name", "uuid", "size")
)
print(len(rows), [r.name for r in rows])

vol = ds.get(OntapVolume, cluster="cluster1", id=rows[0].uuid, source="cache")
print(vol.name if vol is not None else None)
```

```
2 ['vol_logs', 'vol_data_01']
vol_logs
```

Loop over the clusters from step 1 to cover a group of them:

```python
for name in sorted(config.search("clusters", {"env": "Prod"})):
    off = ds.query(OntapVolume, cluster=name, source="cache").filter({"autosize.mode": "off"})
    print(name, sum(1 for _ in off))
```

```
cluster1 1
cluster3 1
```

### 4. Choose where the data comes from

Every `DataSource` call takes `source=`:

| `source=` | Reads from | Use it when |
| :--- | :--- | :--- |
| `"auto"` (default) | The cache for cached fields, and the live API when the cache has no result | You want data whether or not the cache is filled |
| `"cache"` | The cache only | The script must be fast, repeatable and offline |
| `"live"` | The live API only | You need the cluster's current state |

`.where()` is cache-only. With `source="live"`, it raises before any request is sent:

```python
try:
    list(ds.query(OntapVolume, cluster="cluster1", source="live").where("size > 1"))
except ValueError as exc:
    print("ValueError:", exc)
```

```
ValueError: where(): where-expressions are not supported with source='live' on OntapBackend. The live REST path bypasses the cache substrate that evaluates where-strings. Use source='cache' to apply where-expressions against the local cache. See ADR-0012 §49.
```

When to use which surface:

| Surface | Use it for |
| :--- | :--- |
| `cluster.ontap` | Reading one cluster's cached data as attributes |
| `DataSource` | Filtered or projected reads of one model, over many clusters, from the cache or live |
| `ONTAPAPIClient` | A REST call that no model covers, such as a write. See [ONTAP Access Patterns](../usage/ontap-access-patterns.md) |

## Check it worked

Save the snippets from steps 1 to 3 in one file, such as `report.py`, and run it from the directory that holds `config/`:

```bash
uv run python report.py
```

The output is the blocks above, in order. A cluster that is not cached falls back to a live read in step 2, which needs a reachable cluster. Run `nf cache status` to see which clusters are cached.

The cache reads above (`source="cache"`, and `cluster.ontap` on a cached cluster) need no network. The live parts, which are `source="live"`, the `"auto"` fallback and `Config(no_cache=True)`, need a reachable cluster and valid credentials, and are not shown with output here.

## If it fails

| You see | Cause | Fix |
| :--- | :--- | :--- |
| `KeyError: 'cluster1'` from `config.data["clusters"]` | The cluster is not in the config you loaded | Check the directory `Config` reads, and the `[settings] type = "data"` marker. `nf config show -s clusters` lists what loads. |
| A connection error, or a slow read | The cluster has no cache, so the read went live | `nf cache refresh cluster1`, or `nf doctor --api ontap` if the cluster is unreachable. |
| `ValueError: where(): where-expressions are not supported with source='live'` | `.where()` on a live read | Use `source="cache"`, or `.filter()`. |
| No rows from `ds.query(..., source="cache")` | The cluster name is not cached | `nf cache status` lists the cached clusters. |
| `ConfigurationError` from `Config()` | A config file does not load, for example a `scope.toml` whose `name` differs from its directory | `nf config validate` names the file. |

## Next

- [DataSource](../usage/data-source.md): filters, typed expressions, single instances and every source mode
- [Query Layer](../usage/query-layer.md): `QuerySet`, writes and job tracking
- [ONTAP Access Patterns](../usage/ontap-access-patterns.md): choosing between access surfaces
- [Config schema: Python API](../reference/config-schema.md#accessing-configuration-in-code): the `Config` methods
