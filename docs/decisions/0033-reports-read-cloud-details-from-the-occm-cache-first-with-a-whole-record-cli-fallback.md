---
title: "ADR-0033: Reports read cloud details from the OCCM cache first with a whole-record CLI fallback"
description: The inventory and HTML reports take AWS cloud details from the OCCM cache through the cluster resolver and fall back to the ONTAP CLI path for the whole cluster when the cache cannot answer it completely; Azure and GCP keep the CLI path.
date: 2026-11-18
audience:
  - contributors
tags:
  - adr
---

# ADR-0033: Reports read cloud details from the OCCM cache first with a whole-record CLI fallback

## Status

Accepted

## Context

Issue [#1086](https://github.com/endavis/pynetappfoundry/issues/1086) asks the inventory and HTML reports to read cloud provider details from the OCCM cache instead of parsing `virtual-machine instance show` over SSH, and to add NetApp Console links. [ADR-0030](0030-occm-cache-is-discovery-driven-and-maps-working-environments-to-agents.md) deferred this work and [ADR-0032](0032-cross-cache-cluster-resolution-is-uuid-first-with-a-name-fallback-over-one-linking-table.md) returns both the ONTAP `CloudMetadata` and the OCCM cloud records without choosing one. The OCCM record is a different shape from `CloudMetadata`: per working environment and per node lists, no cluster-level equivalent for several fields (CPU platform, consumer, availability zone ids, offer, SKU).

## Decision

1. **OCCM first, through the resolver.** The reports resolve one cluster with `ClusterResolver` (ADR-0032) and take its OCCM record when there is exactly one distinct working environment `publicId`. The OCCM path makes no live call. The report layer (`src/pynetappfoundry/cli/commands/reports/_cloud_source.py`) picks the source and opens the cache files once per run; the cache layer (`src/pynetappfoundry/cache/occm_cloud_metadata.py`) holds pure functions from one record to `CloudMetadata`.
2. **Whole-record fallback.** OCCM answers a cluster only when the account and region are present and every ONTAP node name joins to a node of the record with a non-empty instance id. Otherwise the whole cluster uses the CLI path (`entry.ontap.cloud`), as before. Per-field merging was rejected: it needs the CLI `CloudMetadata` for every cluster OCCM answers (on an ONTAP cache miss that is the SSH call #547 removed) and mixes snapshots of different ages. Gap fields (`cpu_platform`, `consumer`, `availability_zone_id`, `sku_version`, `metadata_version`, the fault and update domains, `offer`, `sku`) are empty on the OCCM path. An empty optional field inside an answered record stays empty and does not trigger the fallback.
3. **AWS only.** The OCCM path answers the two AWS working environment mappings. Azure and GCP clusters always use the CLI path; their Console links still come from the OCCM record. The measurement below found no Console field for the Azure VM instance id and none for the Azure offer and SKU the CLI reports, so under decision 2 no Azure cluster could be answered, and answering Azure with those fields empty would show less than the CLI path does today. GCP is unmeasured.
4. **One path table.** `CLOUD_METADATA_SOURCES` maps every `CloudMetadata` data field to its OCCM paths (the `LINK_RULES` pattern): a measurement changes that table only. A test checks every path against the generated models and the measured shapes fixture, and another checks the table in [Report Cloud Details](../usage/report-cloud-details.md) against it.
5. **Provider from the mapping.** `provider` is `AWS` from the working environment mapping (`CLOUD_MAPPING_PROVIDER`), not from `cloudProviderName`, which is spelled differently from the CLI value.
6. **Per-node join.** `ontapClusterProperties.nodes[].cloudProviderId` joins each ONTAP node to its `awsProperties.instances[]` VSA instance (never the mediator or the agent instance).
7. **Links on a hand-written dataclass.** The Console links (working environment, Volumes, and Aggregates for CVO) are a computed `ConsoleWorkingEnvironmentLinks` carried on the report-side result, not a field of `CloudMetadata` (a cached table: a new field needs a `SCHEMA_VERSION` bump, [ADR-0018](0018-cache-schema-versioning-and-backward-compatibility-policy.md)) and not of a generated model ([ADR-0024](0024-generated-models-carry-only-api-data-computed-values-live-in-separate-hand-written-models.md)). They come from the resolved working environment whichever source answered the cloud fields. The link builders take no account parameter, so the HTML shows the agent's account scopes as text.
8. **Reports.** The inventory workbook gains three trailing columns after "NetApp Console Agent": "Console Working Environment", "Console Volumes" and "Console Aggregates". The HTML cloud section gains a "Source" row and a "NetApp Console" section.

### Value-agreement measurement

Measured 2026-11-18 against live Console agents and the ONTAP cache, read-only (GET only, on a copy of the cache) and scrubbed: answers are categories aggregated as all or some per cloud type, with no counts, identifiers, names or addresses. CVO clusters of three types matched: AWS HA, Azure HA and Azure single node. No cluster matched more than one cloud `publicId`, and no `publicId` appeared under more than one agent.

AWS HA, compared with the CLI value of the same node:

| Field | OCCM path | Result |
| :--- | :--- | :--- |
| `account_id` | `awsProperties.accountId` | all equal |
| `region` | `awsProperties.regionName` | all equal |
| `provider` | `cloudProviderName` | all different; the CLI value is always exactly `AWS` |
| node names | `ontapClusterProperties.nodes[].name` | the set always equals the ONTAP node names |
| `instance_id` | `nodes[].cloudProviderId` | all equal; the joined instance is always found |
| `instance_type`, `image_id`, `primary_ip`, `availability_zone` | joined instance `instanceType`, `imageId`, `privateIpAddress`, `availabilityZone` | all equal |
| `offer`, `sku` | `instances[].productCode`, `clusterProperties.productCode`, `platformLicense`, `licenseType.name`, `nodes[].platformLicense` | all empty on both sides |

Azure HA and single node:

- Equal to the CLI: `account_id` (`providerProperties.subscriptionId`), `region` (`providerProperties.regionName` and `resourceGroup.location`), `provider` (`cloudProviderName`, the CLI value is always exactly `Azure`), `instance_type` (`providerProperties.instanceType`; `clusterProperties.instanceType` is always empty), the node-name set, and the fault and update domains (`haProperties.node{N}Info.availabilitySet`, N being the number at the end of the node name; single node uses `node1Info`).
- `resource_group_name` (`providerProperties.resourceGroup.name`): equal, sometimes only ignoring case.
- HA `node{N}Info.instanceName` and `primaryIp` equal the CLI `vm_name` and `primary_ip`, and the other slot never does. On single node both are empty and `node2Info` is empty.
- **No source for the instance id:** `nodes[].cloudProviderId` and `node{N}Info.instanceId` are always empty; `node{N}Info.serialNumber` is different or empty.
- **No source for offer, SKU or SKU version:** `clusterProperties.productCode`, `platformLicense`, `licenseType.name` and `nodes[].platformLicense` are empty while the CLI has values. `image_id` (`clusterProperties.amiId`) and `availability_zone` are empty on both sides.
- `build_vm_name` reproduces the CLI `vm_name` for both types.

Node IP and System Manager URL, all three types:

- The CLI `primary_ip` is always the `ip` of the node's node-management LIF whose `privateIp` flag is true; there is always exactly one such LIF. `privateIp` is a boolean flag, not an address. A rule that takes any non-data LIF with `privateIp` true is ambiguous.
- `ontapClusterProperties.systemManagerUrl` is always set: an `https` URL with a path, whose host is the cluster-management LIF `ip` (a public address on the AWS HA clusters measured, a private one on Azure). It is never a node's `primary_ip`. `clusterProperties.systemManagerUrl` is always empty. A System Manager link from it is issue [#1105](https://github.com/endavis/pynetappfoundry/issues/1105).

Not measured: GCP (no GCP working environment), and whether the Console link opens a working environment from a different account (a manual UI check).

## Rationale

- OCCM data is already cached and needs no SSH, so the reports stop paying the 10 second SSH timeout and the CLI parsing for AWS clusters the Console manages.
- Answering a cluster completely or not at all keeps one report row from mixing two snapshots and avoids a hidden CLI call per cluster.
- Limiting the OCCM path to AWS keeps every report value the CLI path gives today: for Azure the Console record lacks the instance id, offer and SKU.
- One table of paths keeps measured facts in one place and lets a measurement correct them without touching the join code.
- A computed link dataclass avoids a cache schema migration for data that can always be rebuilt from the `publicId`.

## Consequences

- AWS clusters with a complete OCCM record no longer need the CLI cloud metadata. Azure, GCP and AWS clusters with an incomplete, ambiguous or missing OCCM record keep today's CLI behavior, including the SSH call for cloud clusters.
- On the OCCM path some fields the CLI path fills are empty (the gap fields); for AWS the measured CLI values of `offer` and `sku` were empty too.
- The inventory workbook has three more columns; consumers that read the last column by position see the Console columns there.
- If the Console starts to carry the Azure VM id, the measured Azure paths above (including the node-management LIF rule for the IP) are the starting point for adding Azure.

## Related Issues

- Issue #1086: reports read cloud provider details from the OCCM cache
- Issue #1077: NetApp Console links in the reports
- Issue #1097: resolve one cluster across the ONTAP, AIQUM and OCCM caches
- Issue #547: skip the cloud metadata SSH call on on-prem clusters
- Issue #1105: link System Manager from the OCCM record in the reports

## Related Documentation

- [Report Cloud Details](../usage/report-cloud-details.md)
- [Cluster Resolver](../usage/cluster-resolver.md)
- [ADR-0030](0030-occm-cache-is-discovery-driven-and-maps-working-environments-to-agents.md)
- [ADR-0032](0032-cross-cache-cluster-resolution-is-uuid-first-with-a-name-fallback-over-one-linking-table.md)
