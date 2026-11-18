---
title: "ADR-0033: Reports read cloud details from the OCCM cache first with a whole-record CLI fallback"
description: The inventory and HTML reports take cloud details from the OCCM cache through the cluster resolver and fall back to the ONTAP CLI path for the whole cluster when the cache cannot answer it completely.
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
2. **Whole-record fallback.** OCCM answers a cluster only when the account and region are present and every ONTAP node name joins to a node of the record with a non-empty instance id. Otherwise the whole cluster uses the CLI path (`entry.ontap.cloud`), as before. Per-field merging was rejected: it needs the CLI `CloudMetadata` for every cluster OCCM answers (on an ONTAP cache miss that is the SSH call #547 removed) and mixes snapshots of different ages. Gap fields (`cpu_platform`, `consumer`, `availability_zone_id`, `sku_version`, `metadata_version`, the Azure availability zone, the AWS fault and update domains, `offer`, `sku`) are empty on the OCCM path. An empty optional field inside an answered record stays empty and does not trigger the fallback.
3. **One path table.** `CLOUD_METADATA_SOURCES` maps every `CloudMetadata` data field to its OCCM paths for AWS and Azure (the `LINK_RULES` pattern): a measurement changes that table only. A test checks every path against the generated models and the measured shapes fixture.
4. **Provider from the mapping.** `provider` is `AWS` or `Azure` from the working environment mapping (`CLOUD_MAPPING_PROVIDER`), not from `cloudProviderName`. GCP has no row and always uses the CLI path (unmeasured).
5. **Per-node joins.** AWS joins `ontapClusterProperties.nodes[].cloudProviderId` to the `awsProperties.instances[]` VSA instance (never the mediator or the agent instance). Azure takes `instance_id` from `cloudProviderId` and the per-node values from `haProperties.node{N}Info`, N being the number at the end of the ONTAP node name; a single node uses `node1Info`. The Azure N to `node{N}Info` join is not yet measured; the value-agreement measurement below confirms it.
6. **Links on a hand-written dataclass.** The Console links (working environment, Volumes, and Aggregates for CVO) are a computed `ConsoleWorkingEnvironmentLinks` carried on the report-side result, not a field of `CloudMetadata` (a cached table: a new field needs a `SCHEMA_VERSION` bump, [ADR-0018](0018-cache-schema-versioning-and-backward-compatibility-policy.md)) and not of a generated model ([ADR-0024](0024-generated-models-carry-only-api-data-computed-values-live-in-separate-hand-written-models.md)). They come from the resolved working environment whichever source answered the cloud fields. The link builders take no account parameter, so the HTML shows the agent's account scopes as text.
7. **Reports.** The inventory workbook gains three trailing columns after "NetApp Console Agent": "Console Working Environment", "Console Volumes" and "Console Aggregates". The HTML cloud section gains a "Source" row and a "NetApp Console" section.

### Value-agreement measurement

Read-only and scrubbed: answers are categories (equal, equal ignoring case, equal after format, different, OCCM empty, CLI empty, both empty, path absent), aggregated as all, some or none per cloud type. No counts, identifiers, names or addresses. To be filled before merge; a disagreement changes `CLOUD_METADATA_SOURCES` before merge.

- TODO(measured): `account_id` against `awsProperties.accountId` and `providerProperties.subscriptionId`.
- TODO(measured): `region` against `awsProperties.regionName`, `providerProperties.regionName` and `providerProperties.resourceGroup.location`.
- TODO(measured): `provider` against `cloudProviderName`.
- TODO(measured): Azure `resource_group_name` against `providerProperties.resourceGroup.name`.
- TODO(measured): Azure `instance_type` per node against `providerProperties.instanceType`, else `clusterProperties.instanceType`.
- TODO(measured): the set of `ontapClusterProperties.nodes[].name` against the ONTAP node names.
- TODO(measured): AWS `nodes[].cloudProviderId` against the CLI `instance_id` of the same node.
- TODO(measured): AWS joined instance `instanceType`, `imageId`, `privateIpAddress` and `availabilityZone` against the CLI `instance_type`, `image_id`, `primary_ip` and `availability_zone`.
- TODO(measured): Azure `nodes[].cloudProviderId` against the CLI `instance_id`.
- TODO(measured): Azure HA: whether node names end in a node number, and `haProperties.node{N}Info` `instanceName`, `primaryIp`, `availabilitySet.faultDomain` and `updateDomain` against the CLI `vm_name`, `primary_ip`, `fault_domain` and `update_domain`.
- TODO(measured): Azure single node: whether `node2Info` is empty, equal to `node1Info` or distinct, and whether `node1Info` agrees with the CLI.
- TODO(measured): Azure: whether the CLI `availability_zone` is empty.
- TODO(measured): candidates for the gap fields: `offer` against `clusterProperties.productCode`, `sku` against `clusterProperties.platformLicense` and `licenseType.name`, Azure `image_id` against `clusterProperties.amiId`.
- TODO(measured): whether one cluster matches more than one cloud `publicId`, and whether one `publicId` appears under more than one agent.
- TODO(measured, manual): with the Console UI on a different account than the working environment's, whether `<ui>/storage/cloud-volumes-ontap/<publicId>` opens it, prompts to switch or fails.

## Rationale

- OCCM data is already cached and needs no SSH, so the reports stop paying the 10 second SSH timeout and the CLI parsing for clusters the Console manages.
- Answering a cluster completely or not at all keeps one report row from mixing two snapshots and avoids a hidden CLI call per cluster.
- One table of paths keeps measured facts in one place and lets a measurement correct them without touching the join code.
- A computed link dataclass avoids a cache schema migration for data that can always be rebuilt from the `publicId`.

## Consequences

- A cluster whose OCCM record is incomplete, ambiguous or of an unmeasured cloud keeps today's CLI behavior, including the SSH call for cloud clusters.
- On the OCCM path some fields the CLI path fills are empty (the gap fields); a measurement can add paths for them.
- The inventory workbook has three more columns; consumers that read the last column by position see the Console columns there.
- The Azure node-number join and GCP remain unmeasured until the measurement and a GCP agent exist.

## Related Issues

- Issue #1086: reports read cloud provider details from the OCCM cache
- Issue #1077: NetApp Console links in the reports
- Issue #1097: resolve one cluster across the ONTAP, AIQUM and OCCM caches
- Issue #547: skip the cloud metadata SSH call on on-prem clusters

## Related Documentation

- [Report Cloud Details](../usage/report-cloud-details.md)
- [Cluster Resolver](../usage/cluster-resolver.md)
- [ADR-0030](0030-occm-cache-is-discovery-driven-and-maps-working-environments-to-agents.md)
- [ADR-0032](0032-cross-cache-cluster-resolution-is-uuid-first-with-a-name-fallback-over-one-linking-table.md)
