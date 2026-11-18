---
title: Cluster Resolver
description: Find one ONTAP cluster in the ONTAP, AIQUM and OCCM caches and read what each holds, from the caches alone
audience:
  - users
tags:
  - cache
  - aiqum
  - occm
---

# Cluster Resolver

`ClusterResolver` answers two questions from the caches alone, with no live call and no Console account:

- `resolve(name)`: where does each cache hold this cluster? It returns the ONTAP cache key, the AIQUM instances and cluster keys, and the Console agents with their working environment `publicId`.
- `read(name)`: what do they hold? It returns each source's cached data with its snapshot age.

The three caches are keyed differently (cluster name, AIQUM instance, agent id plus `publicId`); the resolver is the join. The decision is in [ADR-0032](../decisions/0032-cross-cache-cluster-resolution-is-uuid-first-with-a-name-fallback-over-one-linking-table.md).

## Usage

```python
from pynetappfoundry.cache import ClusterResolver

with ClusterResolver.from_config(config) as resolver:
    location = resolver.resolve("lab-cluster")
    if location.found:
        for hit in location.aiqum:
            print(hit.instance, hit.cluster_key, hit.matched_by)
        for hit in location.occm:
            print(hit.agent_id, hit.agent_name, hit.scopes, hit.mapping, hit.public_id)

    data = resolver.read("lab-cluster", ttl_days=30)
    if data.ontap is not None:
        print(data.ontap.cached_at, data.ontap.is_stale)
```

`from_config` opens only the cache files that already exist and never creates one. The context manager closes them. To use databases you already hold, pass them: `ClusterResolver(ontap_db=..., aiqum_db=..., occm_db=...)`; any of them can be `None`.

## Absent versus error

A missing cache file, no rows or no match is absent: `None` for the ONTAP part, an empty tuple for the AIQUM and OCCM parts, and `found` is `False` when everything is absent. An invalid cluster name raises `ValueError`, even when the ONTAP cache is absent. `sqlite3` errors propagate.

## How a cluster is matched

The ONTAP cache supplies the cluster UUID. The UUID is authoritative:

- A record that holds a UUID matches only an equal UUID. The same name with a different UUID does not match.
- A record without a UUID, or any record when the ONTAP UUID is unknown (for example the ONTAP cache is absent), matches by exact, case-sensitive name. The name is the cached ONTAP `cluster.name` when present, which can differ from the inventory key, else the name you passed.
- Each AIQUM and OCCM hit carries `matched_by`, `"uuid"` or `"name"`.

The fields compared are in one table, `LINK_RULES`, in `src/pynetappfoundry/cache/cluster_resolver.py`.

## Several instances and agents

Every AIQUM instance and every agent is searched, and every hit returned, sorted. A working environment listed by two agents appears once per agent. `OccmLocation.scopes` lists the Console accounts the agent was discovered in (`None` is the root account) and `agent_name` comes from the cached discovery.

## The reader and staleness

`read` returns `ClusterData`:

- `ontap`: the `CachedClusterMetadata`, including its CLI-parsed `CloudMetadata`.
- `aiqum`: per instance, the `AiqumCluster` with only its own SVMs and volumes.
- `occm`: the generated working-environment model of each hit. The ONTAP `CloudMetadata` and the OCCM cloud records are both returned; neither is chosen here. The reports choose: see [Report Cloud Details](report-cloud-details.md).

Each part has `cached_at` and `is_stale` (older than `ttl_days`). Age is reported and never filters: stale data is still returned. For OCCM, `cached_at` is the oldest collection of the agent.

## Refresh the caches first

A source that was never refreshed is absent. Refresh them with `nf cache refresh`, `nf cache aiqum refresh` and `nf cache occm refresh`.

## See also

- [Cache reference: Cross-cache resolution](../reference/cache.md#cross-cache-resolution)
- [Console Agent](console-agent.md)
- [ADR-0032](../decisions/0032-cross-cache-cluster-resolution-is-uuid-first-with-a-name-fallback-over-one-linking-table.md)
