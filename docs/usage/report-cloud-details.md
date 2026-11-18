---
title: Report Cloud Details
description: How the inventory and HTML reports take cloud provider details from the OCCM cache, when they fall back to the ONTAP CLI path, and the Console links (including System Manager) they add
audience:
  - users
tags:
  - reports
  - occm
  - cache
---

# Report Cloud Details

`nf reports inventory` and `nf reports html` read an AWS cluster's cloud provider details from the OCCM cache first and use the ONTAP CLI path (`entry.ontap.cloud`, parsed from `virtual-machine instance show`) only when the cache cannot answer, and always for Azure, GCP and on-prem clusters. They also add NetApp Console links for every cluster the cache resolves. The decision is [ADR-0033](../decisions/0033-reports-read-cloud-details-from-the-occm-cache-first-with-a-whole-record-cli-fallback.md).

## What the reports do

- The OCCM path reads the caches only: `ClusterResolver` finds the working environment and the adapter in `src/pynetappfoundry/cache/occm_cloud_metadata.py` turns its record into one `CloudMetadata` per ONTAP node. It makes no live call.
- `src/pynetappfoundry/cli/commands/reports/_cloud_source.py` picks OCCM or CLI per cluster and opens the cache files once per report run. It opens only files that exist and never creates one. AIQUM is not read.
- Age never filters: a stale OCCM record is still used.
- On-prem clusters never read `entry.ontap.cloud` (an SSH call that times out on on-prem clusters, #547).

## Whole-record fallback

OCCM answers a cluster only when all of these hold; otherwise the whole cluster uses the CLI path, as before:

1. The resolver finds exactly one distinct working environment `publicId` for the cluster (the same `publicId` under several agents counts once: a UUID match is preferred, then a non-stale agent, then the first agent id).
2. The working environment is an AWS one (single node or HA). Azure and GCP always use the CLI path; see [Azure and GCP](#azure-and-gcp).
3. The record has an account (or subscription) id and a region.
4. Every ONTAP node name of the cluster joins to a node of the record and has a non-empty instance id.

Fields are never mixed between the two sources for one cluster. An empty optional field inside an answered record, for example an AWS instance type that is `null`, stays empty and does not trigger the fallback. The fallback is silent in the report; a resolver or adapter error logs a warning with only the cluster name and the exception type.

## Per-node joins

For each `ontapClusterProperties.nodes[]` entry named like the ONTAP node, the `awsProperties.instances[]` entry whose `id` equals its `cloudProviderId` and whose `isVsaInstance` is true. The mediator and the Console agent instance never join.

## Field mapping

The table is `CLOUD_METADATA_SOURCES` in `src/pynetappfoundry/cache/occm_cloud_metadata.py`; a measurement changes that table only. `[]` selects the joined list element. A field without a path is a gap and stays empty on the OCCM path. `provider` comes from the mapping (`AWS`), not from `cloudProviderName`. The links and `vm_name` are computed with `src/pynetappfoundry/utils/cloud.py`.

| Field | AWS | Scope | Note |
|-------|-----|-------|------|
| `instance_id` | `ontapClusterProperties.nodes[].cloudProviderId` | node | |
| `account_id` | `awsProperties.accountId` | we | |
| `image_id` | `awsProperties.instances[].imageId` | node | |
| `instance_type` | `awsProperties.instances[].instanceType` | node | |
| `cpu_platform` | | we | gap: no OCCM field |
| `region` | `awsProperties.regionName` | we | |
| `provider` | | we | derived from CLOUD_MAPPING_PROVIDER ("AWS"); cloudProviderName is spelled differently from the CLI value, which is exactly "AWS" |
| `consumer` | | we | gap: no OCCM field |
| `primary_ip` | `awsProperties.instances[].privateIpAddress` | node | |
| `metadata_version` | | we | gap: no OCCM field |
| `availability_zone` | `awsProperties.instances[].availabilityZone` | node | |
| `availability_zone_id` | | we | gap: no OCCM field |
| `fault_domain` | | we | not applicable: Azure only |
| `update_domain` | | we | not applicable: Azure only |
| `resource_group_name` | | we | not applicable: Azure only |
| `offer` | | we | gap: empty in both OCCM and the CLI for AWS (measured) |
| `sku` | | we | gap: empty in both OCCM and the CLI for AWS (measured) |
| `sku_version` | | we | gap: no OCCM field |

Derived: `vm_name` is the AWS instance id; `instance_link` and `instance_sso_link` (with the `[aws.sso]` settings) use the same builders as the CLI path.

## Azure and GCP

Azure and GCP clusters always use the CLI path (`entry.ontap.cloud`); the Console links still appear for them, because those come from the resolved working environment.

Azure was measured against the CLI and cannot be answered completely from the Console record. The record never carries the VM instance id (the node `cloudProviderId` and the HA `instanceId` are empty, and `serialNumber` is empty or differs), nor the offer and sku (`clusterProperties.productCode`, `platformLicense`, `licenseType.name` and the node `platformLicense` are empty while the CLI has them). Under the whole-record rule such a cluster could never be answered, so Azure keeps the CLI. GCP is not measured.

## Measured and unmeasured

The path table comes from the measured shape of the AWS HA list (`tests/fixtures/console_models/cvo_working_environment_shapes.json`). Not measured: GCP and AWS single node (it uses the AWS rows). How the OCCM values compare with the CLI values is recorded in the ADR.

## Console links and the Console section

The links come from the resolved working environment, whichever source answered the cloud fields, and are built by `src/pynetappfoundry/utils/console_links.py`.

- **Inventory workbook:** four columns after "NetApp Console Agent": "Console Working Environment", "Console Volumes", "Console Aggregates" and "Console System Manager". Each cell is a hyperlink (display text "Working environment", "Volumes", "Aggregates", "System Manager") or empty. The older "System Manager" column (built from the configured cluster IP) is unchanged. Aggregates exist for CVO only, so it is empty for on-prem clusters.
- **HTML report:** a "NetApp Console" section after the cloud section with the same links and an "Account scope" row listing the Console accounts the agent was discovered in (the root account shows as `default`). The cloud section gains a "Source" row: `Console (OCCM cache)` or `ONTAP CLI`.
- **System Manager link:** read from `ontapClusterProperties.systemManagerUrl` of the OCCM record by `system_manager_link` in `src/pynetappfoundry/cache/occm_cloud_metadata.py` and carried on `ConsoleWorkingEnvironmentLinks`. It is computed, not cached. The HTML "NetApp Console" section shows it as a "System Manager" row.
  - Measured: `ontapClusterProperties.systemManagerUrl` is in the AWS HA, Azure HA and Azure single node shapes; `clusterProperties.systemManagerUrl` is always empty and is never used.
  - It appears for every working environment type whose record carries the value, independent of the AWS-only cloud-details rule. GCP and on-prem values are not measured.
  - The value is used unchanged only when it is a string with an `http` or `https` scheme, a host and no whitespace or control characters; anything else gives an empty cell and no row. This blocks `javascript:` and `data:` links.
  - With no single working environment it is empty, and no live call is made.
  - The link is the address Console recorded, so it is reachable only from a network that can reach that address.
- The link builders take no account parameter, so the URLs are the plain Console URLs; the account scope is text only.
- With no single working environment found (none, or several distinct ones), the columns are empty and the section is absent.

Refresh the caches first: `nf cache refresh` and `nf cache occm refresh`. See also [Cluster Resolver](cluster-resolver.md) and [Console Agent](console-agent.md).
