---
title: Report Cloud Details
description: How the inventory and HTML reports take cloud provider details from the OCCM cache, when they fall back to the ONTAP CLI path, and the Console links they add
audience:
  - users
tags:
  - reports
  - occm
  - cache
---

# Report Cloud Details

`nf reports inventory` and `nf reports html` read a cluster's cloud provider details from the OCCM cache first and use the ONTAP CLI path (`entry.ontap.cloud`, parsed from `virtual-machine instance show`) only when the cache cannot answer. They also add NetApp Console links. The decision is [ADR-0033](../decisions/0033-reports-read-cloud-details-from-the-occm-cache-first-with-a-whole-record-cli-fallback.md).

## What the reports do

- The OCCM path reads the caches only: `ClusterResolver` finds the working environment and the adapter in `src/pynetappfoundry/cache/occm_cloud_metadata.py` turns its record into one `CloudMetadata` per ONTAP node. It makes no live call.
- `src/pynetappfoundry/cli/commands/reports/_cloud_source.py` picks OCCM or CLI per cluster and opens the cache files once per report run. It opens only files that exist and never creates one. AIQUM is not read.
- Age never filters: a stale OCCM record is still used.
- On-prem clusters never read `entry.ontap.cloud` (an SSH call that times out on on-prem clusters, #547).

## Whole-record fallback

OCCM answers a cluster only when all of these hold; otherwise the whole cluster uses the CLI path, as before:

1. The resolver finds exactly one distinct working environment `publicId` for the cluster (the same `publicId` under several agents counts once: a UUID match is preferred, then a non-stale agent, then the first agent id).
2. The working environment is an AWS or Azure one (single node or HA). GCP is not measured and always uses the CLI path.
3. The record has an account (or subscription) id and a region.
4. Every ONTAP node name of the cluster joins to a node of the record and has a non-empty instance id.

Fields are never mixed between the two sources for one cluster. An empty optional field inside an answered record, for example an Azure HA instance type that is `null`, stays empty and does not trigger the fallback. The fallback is silent in the report; a resolver or adapter error logs a warning with only the cluster name and the exception type.

## Per-node joins

- **AWS** (single node and HA): for each `ontapClusterProperties.nodes[]` entry named like the ONTAP node, the `awsProperties.instances[]` entry whose `id` equals its `cloudProviderId` and whose `isVsaInstance` is true. The mediator and the Console agent instance never join.
- **Azure** (single node and HA): `instance_id` is the node's `cloudProviderId`. The per-node values come from `haProperties.node{N}Info`, where N is the number at the end of the ONTAP node name (`utils.cloud.get_node_number`); a single-node cluster uses `node1Info`. The join of the node number to the `node{N}Info` slot is not yet measured against the CLI values.

## Field mapping

The table is `CLOUD_METADATA_SOURCES` in `src/pynetappfoundry/cache/occm_cloud_metadata.py`; a measurement changes that table only. `[]` selects the joined list element, `{N}` the node number. A field without a path is a gap and stays empty on the OCCM path. `provider` comes from the mapping (`AWS` or `Azure`), not from `cloudProviderName`. The links and `vm_name` are computed with `src/pynetappfoundry/utils/cloud.py`.

| Field | AWS | Azure | Scope | Note |
|-------|-----|-------|-------|------|
| `instance_id` | `ontapClusterProperties.nodes[].cloudProviderId` | `ontapClusterProperties.nodes[].cloudProviderId` | node | |
| `account_id` | `awsProperties.accountId` | `providerProperties.subscriptionId` | we | |
| `image_id` | `awsProperties.instances[].imageId` | | node | Azure: not measured (amiId?) |
| `instance_type` | `awsProperties.instances[].instanceType` | `providerProperties.instanceType`, `clusterProperties.instanceType` | node | |
| `cpu_platform` | | | we | gap: no OCCM field |
| `region` | `awsProperties.regionName` | `providerProperties.regionName` | we | |
| `provider` | | | we | derived: CLOUD_MAPPING_PROVIDER, not cloudProviderName |
| `consumer` | | | we | gap: no OCCM field |
| `primary_ip` | `awsProperties.instances[].privateIpAddress` | `haProperties.node{N}Info.primaryIp` | node | |
| `metadata_version` | | | we | gap: no OCCM field |
| `availability_zone` | `awsProperties.instances[].availabilityZone` | | node | Azure: gap (the CLI value is a zone, node{N}Info.availabilityZone is null) |
| `availability_zone_id` | | | we | gap: no OCCM field |
| `fault_domain` | | `haProperties.node{N}Info.availabilitySet.faultDomain` | node | AWS: gap |
| `update_domain` | | `haProperties.node{N}Info.availabilitySet.updateDomain` | node | AWS: gap |
| `resource_group_name` | | `providerProperties.resourceGroup.name` | we | AWS: not applicable |
| `offer` | | | we | gap: candidate clusterProperties.productCode, unmeasured |
| `sku` | | | we | gap: candidate clusterProperties.platformLicense, unmeasured |
| `sku_version` | | | we | gap: no OCCM field |

Derived: `vm_name` is the AWS instance id, or for Azure `haProperties.node{N}Info.instanceName` with `build_vm_name` as the fallback; `instance_link`, `instance_sso_link` (AWS, with the `[aws.sso]` settings) and `resource_group_link` use the same builders as the CLI path.

## Measured and unmeasured

The path table comes from the measured shapes of the AWS HA, Azure HA and Azure single-node lists (`tests/fixtures/console_models/cvo_working_environment_shapes.json`). Not measured: GCP, AWS single node (it uses the AWS rows), and the Azure node-number join. How the OCCM values compare with the CLI values is recorded in the ADR.

## Console links and the Console section

The links come from the resolved working environment, whichever source answered the cloud fields, and are built by `src/pynetappfoundry/utils/console_links.py`.

- **Inventory workbook:** three columns after "NetApp Console Agent": "Console Working Environment", "Console Volumes" and "Console Aggregates". Each cell is a hyperlink (display text "Working environment", "Volumes", "Aggregates") or empty. Aggregates exist for CVO only, so it is empty for on-prem clusters.
- **HTML report:** a "NetApp Console" section after the cloud section with the same links and an "Account scope" row listing the Console accounts the agent was discovered in (the root account shows as `default`). The cloud section gains a "Source" row: `Console (OCCM cache)` or `ONTAP CLI`.
- The link builders take no account parameter, so the URLs are the plain Console URLs; the account scope is text only.
- With no single working environment found (none, or several distinct ones), the columns are empty and the section is absent.

Refresh the caches first: `nf cache refresh` and `nf cache occm refresh`. See also [Cluster Resolver](cluster-resolver.md) and [Console Agent](console-agent.md).
