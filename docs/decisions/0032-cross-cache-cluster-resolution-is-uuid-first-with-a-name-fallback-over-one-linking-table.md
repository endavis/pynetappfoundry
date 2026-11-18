---
title: "ADR-0032: Cross-cache cluster resolution is UUID-first with a name fallback over one linking table"
description: The cluster resolver links the ONTAP, AIQUM and OCCM caches by cluster UUID first and by exact name second, through one table of linking fields.
date: 2026-11-18
audience:
  - contributors
tags:
  - adr
---

# ADR-0032: Cross-cache cluster resolution is UUID-first with a name fallback over one linking table

## Status

Accepted

## Context

Issue [#1097](https://github.com/endavis/pynetappfoundry/issues/1097) asks for one read-only call that finds a cluster in the ONTAP, AIQUM and OCCM caches. The three caches are keyed differently: cluster name, AIQUM instance, and Console agent id plus working environment `publicId`. Nothing joined them. [ADR-0026](0026-aiqum-backend-is-live-only-and-reads-the-hal-records-envelope.md) and [ADR-0030](0030-occm-cache-is-discovery-driven-and-maps-working-environments-to-agents.md) describe the AIQUM and OCCM caches; [ADR-0029](0029-console-discovery-walks-scope-accounts-and-merges-hand-written-spec-fragments.md) describes the agent scopes.

## Decision

1. **One linking table.** `LINK_RULES` in `src/pynetappfoundry/cache/cluster_resolver.py` maps each cached record type (`AiqumCluster` and the seven OCCM working environment mappings) to a `LinkRule`: the dotted record paths that hold the cluster UUID, and the paths that hold the cluster name. A measurement result changes that table only. The initial rules come from the generated models: AIQUM `uuid` and `name`; on-prem `ontapClusterProperties.clusterUuid` then `clusterProperties.clusterUuid`; the six cloud lists `ontapClusterProperties.clusterUuid` only (their `clusterProperties` has no `clusterUuid`). A test checks that every path resolves against the model, so codegen drift fails.
2. **UUID first, name as fallback.** The ONTAP UUID comes only from the ONTAP cache. When it is known, a record that holds a UUID matches only on an equal UUID, and a record with a different UUID never matches by name. A record without a UUID, or any record when the ONTAP UUID is unknown, matches by exact, case-sensitive name. The name used is the cached ONTAP `cluster.name` when present, else the input name. Each hit reports `matched_by` (`uuid` or `name`). Name paths are tried in order: `ontapClusterProperties.clusterName`, then `clusterProperties.clusterName`, and for the six cloud lists only, the working environment's own `name` last, because the measurement below found it equal to the ONTAP cluster name on every UUID-matched cloud record. The on-prem working environment `name` is not a fallback: it is a display name and was not measured against the cluster name.
3. **Absent is not an error.** A missing cache file, no rows or no match returns `None` or an empty tuple. An invalid cluster name raises `ValueError`, even when the ONTAP cache is absent. `sqlite3` errors propagate.
4. **Every instance and agent is returned.** All AIQUM instances and every agent and working environment mapping is searched and each hit returned, sorted, with the agent name and the scopes from [#1083](https://github.com/endavis/pynetappfoundry/issues/1083).
5. **No file is created.** `ClusterResolver.from_config` opens only cache files that already exist, through the new `default_path` of each database class.
6. **Reader.** `ClusterResolver.read` returns each source's cached data with `cached_at` and `is_stale`; age never filters. Both the ONTAP `CloudMetadata` and the OCCM cloud records are returned, neither is chosen here; the reports choose ([#1086](https://github.com/endavis/pynetappfoundry/issues/1086), [ADR-0033](0033-reports-read-cloud-details-from-the-occm-cache-first-with-a-whole-record-cli-fallback.md)).
7. **Not links.** `clusterProperties.systemId` and `serialNumber` identify a system or a node, not the cluster. `ConsoleInfo.connector` in the ONTAP cache is written by nothing. The discovery `ConsoleWorkingEnvironment` has no cluster UUID or name.
8. **Cache layer only.** The module reads the three cache databases and imports nothing from `pynetappfoundry.data` or `pynetappfoundry.clients`, so it cannot make a live call.

### Linking-key measurement (#1097, read-only, scrubbed)

Field paths and always, sometimes or never answers only; no counts, identifiers, names or addresses. Two sources: a multi-agent environment with AWS HA, Azure single-node and Azure HA working environments, several AIQUM instances and the ONTAP cache refreshed with the current code; and a lab with one cluster, one AIQUM instance and one on-prem working environment.

- **ONTAP cache:** `cluster.uuid` was always populated, and `cluster.name` always equalled the inventory key (both sources).
- **Cloud working environments** (AWS HA, Azure, Azure HA; the other cloud types had no records):
  - `ontapClusterProperties` was always present; `clusterProperties.clusterUuid` and `clusterProperties.clusterName` were never set.
  - `ontapClusterProperties.clusterUuid` and `.clusterName` were always set on AWS HA and Azure, and only sometimes on Azure HA. The working environment's own `name` was always set.
  - Where `ontapClusterProperties.clusterUuid` was set, it was always the UUID of a cached ONTAP cluster. On those UUID-matched records, `ontapClusterProperties.clusterName` and the working environment `name` always equalled the ONTAP `cluster.name`.
  - So the cloud UUID path is right, and the working environment `name` became the last cloud name fallback, for the Azure HA records whose `ontapClusterProperties` is only partly populated.
- **On-prem working environments:** none in the multi-agent environment. In the lab, the `ontapClusterProperties.clusterUuid` of the on-prem working environment equalled the ONTAP cluster UUID and matched by UUID. Whether `ontapClusterProperties.clusterUuid` and `clusterProperties.clusterUuid` always agree, and whether the on-prem `name` equals the cluster name, is not measured; the rule keeps both UUID paths and does not use the on-prem `name`.
- **AIQUM:** `uuid` and `name` were always set. The AIQUM `uuid` was only sometimes a cached ONTAP UUID, because the AIQUM instances monitor clusters the ONTAP cache does not hold. Where it matched, the AIQUM `name` always equalled the ONTAP `cluster.name`. In the lab the AIQUM `uuid` equalled the ONTAP UUID.
- Reading AIQUM clusters into the `AiqumCluster` model can fail on an instance that returns a `null` `contact` or `location`. Matching uses the raw records and is not affected; the model fix is [#1102](https://github.com/endavis/pynetappfoundry/issues/1102).

## Rationale

- The UUID does not change when a cluster is renamed or listed under a different inventory key; the name does. Making the UUID authoritative avoids joining two different clusters that share a name.
- A single table keeps the measured facts in one place and lets a measurement change the rule without touching the matching code.
- Returning every instance and agent matches how the caches already behave: a cluster can be monitored by two AIQUM instances and managed under two agents.
- Reporting age and never filtering follows [ADR-0026](0026-aiqum-backend-is-live-only-and-reads-the-hal-records-envelope.md): the caller decides what is too old.

## Consequences

- A refresh of each cache is needed first: `nf cache refresh`, `nf cache aiqum refresh` and `nf cache occm refresh`. A source that was never refreshed is simply absent.
- A cluster whose records carry no UUID is matched by name, which can miss a renamed cluster.
- A future `cluster show` command can sit on the resolver.

## Related Issues

- Issue #1097: feat: resolve one cluster across the ONTAP, AIQUM and OCCM caches
- Issue #1083: resolve Console agents by name and owning account
- Issue #1086: reports read cloud provider details from the OCCM cache
- Issue #1087: refresh and inspect CLI for the OCCM cache
- Issue #1072: AIQUM cache CLI
- Issue #1074: cloud working environment lists in the OCCM cache

## Related Documentation

- [Cluster Resolver](../usage/cluster-resolver.md)
- [Cache Reference: Cross-cache resolution](../reference/cache.md#cross-cache-resolution)
- [ADR-0026](0026-aiqum-backend-is-live-only-and-reads-the-hal-records-envelope.md)
- [ADR-0029](0029-console-discovery-walks-scope-accounts-and-merges-hand-written-spec-fragments.md)
- [ADR-0030](0030-occm-cache-is-discovery-driven-and-maps-working-environments-to-agents.md)
