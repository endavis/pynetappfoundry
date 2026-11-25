---
title: Find Expiring Licenses and Export Them to CSV
description: List the licenses on your ONTAP clusters, export them to CSV, and check for expiring or missing licenses with an optional email
audience:
  - users
tags:
  - how-to
  - licenses
  - ontap
---

# Find Expiring Licenses and Export Them to CSV

**Goal:** list the licenses on your ONTAP clusters with their expiry, write them to a CSV file, and run the license check that flags expiring or missing licenses.

## Before you start

- At least one cluster in the inventory with credentials: [Add an ONTAP cluster and validate it](add-ontap-cluster.md).
- A filled cache for `nf licenses get`, which reads licenses from it: [Fill the cache and query it](fill-and-query-cache.md). When a cluster is not cached, the command fetches it from the cluster.
- For `nf licenses check`, the cluster must be reachable: it always reads the cluster live.

## Steps

### 1. List the licenses

Pick the cluster with `-f`, a JSON filter on the inventory fields. Leave `-f` out for every cluster:

```bash
nf licenses get -f '{"name": "cluster1"}'
```

```
Getting licenses for cluster1...
```

Then a `Cluster Licenses` table with the columns `Cluster`, `License Description`, `Node`, `Serial #` and `Expiration`. This cluster, an ONTAP Select cluster, has 17 rows, all `No expiry`. A few of them:

```
cluster1 | NFS License | cluster1 | <serial> | No expiry
cluster1 | ONTAP Select License | node1 | <serial> | No expiry
cluster1 | ONTAP Select License | node2 | <serial> | No expiry
cluster1 | FabricPool License (If Cloud Tiering is used see Cloud Manager->Digital Wallet). | cluster1 | <serial> | No expiry
```

The others are iSCSI, SnapRestore, SnapMirror, FlexClone, SnapVault, SnapLock, Volume Encryption, NVMe-oF, Multi-tenant Encryption Key Management, S3, Autonomous Ransomware Protection and S3 SnapMirror.

What the command does with each license, as the code reads it:

- It drops a license whose owner is empty or `none`.
- It shows a license that has no expiry date with `No expiry`. It does not hide it, although `nf licenses get --help` says it filters out licenses without expiry.
- `Expiration` is the raw expiry value the cluster reports.

Add `--live` to read the licenses from the clusters instead of the cache. It is slower, because every field group is fetched over the network.

### 2. Export to CSV

```bash
nf licenses get -f '{"name": "cluster1"}' --csv
```

```
Getting licenses for cluster1...
CSV written to data/licenses_get/output/get_licenses_2026-11-25_16-11-41.csv
```

The file has the same five columns, one row per license:

```
Cluster,License Description,Node,Serial #,Expiration
cluster1,NFS License,cluster1,<serial>,No expiry
```

The file name carries a timestamp, so a rerun writes a new file. Name the file yourself with `--output`; `nf` creates missing parent directories and overwrites an existing file:

```bash
nf licenses get --csv --output licenses.csv
```

`--output` is used only together with `--csv`.

### 3. Run the license check

```bash
nf licenses check -f '{"name": "cluster1"}' --no-send-email
```

```
Checking cluster1...
No licensing issues found.
```

The check reads each cluster's licenses and nodes from the cluster, then flags:

- **Expiring licenses:** a license with an expiry date and an owner other than `none` is flagged when its expiry is less than 30 days away. Licenses whose serial number starts with `9092` (ONTAP Cloud Capacity) or `2265` (Data Tiering) use 13 days. Serial numbers starting with `3200` are labelled ONTAP Select; all others, ONTAP BYOL.
- **A license that has already expired.** It is flagged too, because its expiry is before the threshold.
- **Nodes without a license:** a node that owns no license is flagged as `No License`.
- **A cluster it could not read.** The error is printed, and the cluster is counted as an issue.

When something is flagged, the check prints `Found N licensing issues:` and one line per issue.

### 4. Know when it sends email

!!! warning "Email is sent by default"
    `nf licenses check` sends an email unless you pass `--no-send-email`. It sends one when it finds issues, and also a "No licensing issues" email when it finds none. A scheduled run mails your team every time.

Where the settings come from:

- **Recipients:** the `[licensing]` table in `<config>/settings.toml`, with `mailfrom` and `mailto`.
- **Mail server:** the `[SMTP]` table in the same file: `server`, and optionally `port` (default 25), `user`, `password` and `auth`. See [Config schema](../reference/config-schema.md#settingstoml).

```toml
[licensing]
mailfrom = "netapp-licensing@example.com"
mailto = "netapp-team@example.com"

[SMTP]
server = "smtp.example.com"
```

The subject is `<date> : Licensing issues found` (marked high priority) or `<date> : No licensing issues found`.

What happens when the settings are missing, from runs against a scratch config:

| State | Result |
| :--- | :--- |
| No `[licensing]` table | `Email settings not configured, skipping notification`, exit 0 |
| `[licensing]` present, no `[SMTP]` table | `Unexpected error: Missing configuration key 'settings.SMTP'...`, exit 1 |
| `[SMTP]` present but the server cannot be reached | Nothing is printed and the exit code is 0. The send error goes only to the log file |

So a failed send does not show in the exit code. For a scheduled run, check the mailbox and the log, and see [Run nf unattended](run-unattended.md).

## Check it worked

```bash
nf licenses get -f '{"name": "cluster1"}' --csv --output licenses.csv
```

The command prints `CSV written to licenses.csv`. Open the file: the first line is `Cluster,License Description,Node,Serial #,Expiration`. Then:

```bash
nf licenses check -f '{"name": "cluster1"}' --no-send-email
```

It ends with `No licensing issues found.`, or lists what to fix.

## If it fails

| You see | Cause | Fix |
| :--- | :--- | :--- |
| An empty `Cluster Licenses` table | No license has an owner other than `none`, or the cluster has no cached license data | Run `nf cache refresh cluster1`, then retry, or add `--live`. |
| `Could not retrieve licenses for cluster1: ...` | The cluster is unreachable, or has no credentials | Run `nf doctor`. See [Add an ONTAP cluster and validate it](add-ontap-cluster.md). |
| `Could not find user for type='clusters', object='cluster1'` | No credentials for the cluster | [Add an ONTAP cluster and validate it](add-ontap-cluster.md), step 2. |
| `Found 1 licensing issues:` followed by `cluster1 - Unknown - expires in Unknown days` | The check could not read the cluster, so the issue has no license details. The cause is the `Could not retrieve licenses` line above it | Fix that error. The command still exits 0. |
| `Email settings not configured, skipping notification` | No `[licensing]` table in `settings.toml` | Add it, or pass `--no-send-email`. |
| `Missing configuration key 'settings.SMTP'` | `[licensing]` is set but `[SMTP]` is not | Add the `[SMTP]` table. |
| The email never arrives, and nothing is printed | The SMTP server refused or could not be reached; the error is only logged | Read the log file under `data/licenses_check/logs/`. |

## Next

- [Fill the cache and query it](fill-and-query-cache.md)
- [Check recent events by severity](check-events.md)
- [Config schema: settings.toml](../reference/config-schema.md#settingstoml)
- [Usage basics: License Reporting](../usage/basics.md#license-reporting)
