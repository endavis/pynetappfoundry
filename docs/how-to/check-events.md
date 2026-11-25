---
title: Check Recent Events by Severity
description: Pull EMS events from your ONTAP clusters, filter by severity or event name, and read them from a CSV file
audience:
  - users
tags:
  - how-to
  - events
  - ontap
---

# Check Recent Events by Severity

**Goal:** pull the EMS events of one or more ONTAP clusters, filtered by severity or event name, into a CSV file you can open or search.

## Before you start

- At least one cluster in the inventory with credentials: [Add an ONTAP cluster and validate it](add-ontap-cluster.md).
- The cluster must be reachable. `nf events get` reads events from the cluster; it does not use the cache.

## Steps

### 1. Get the most recent errors

```bash
nf events get -f '{"name": "cluster1"}' -s error -l 5 --sort -time
```

```
Getting events for cluster1...
Events written to ems_output.csv
Total events: 5
```

- `-f` selects clusters by their inventory fields. Leave it out for every cluster.
- `-s` (`--severity`) is one of `emergency`, `alert`, `error`, `notice`, `informational`, `debug`. It sends that level as the filter. Without `-s`, the filter is `*`, so events of every severity are returned.
- `-l` (`--limit`) is the number of events to get. The default is 50, and the limit applies to each cluster separately.
- `--sort -time` puts the newest first. The default is `--sort time`, oldest first.

!!! warning "The newest events need `--sort -time`"
    The limit is applied after the sort. With the default sort, `-l 100` returns the 100 oldest events, not the 100 most recent. Add `--sort -time` to get the latest.

### 2. Read the CSV

The console prints only the count. The events are in the file, which `--output` names. It defaults to `ems_output.csv` in the directory you ran the command from. It is not placed under `data/`.

The header is:

```
cluster,node,time,name,severity,message
```

One row, from the run above:

```
cluster1,node2,2026-11-25 15:56:37+00:00,fabricpool.nearly.full,error,Total; cluster-wide FabricPool space usage of object stores from capacity-licensed providers has nearly reached the licensed limit. Cluster id: <uuid>. Current usage: 105.8TB; licensed capacity: 120TB.
```

To make each message fit one CSV field, `nf` removes the `<event name>: ` prefix, replaces commas with semicolons and newlines with spaces. A message that reads `Total, cluster-wide` on the cluster reads `Total; cluster-wide` in the file.

### 3. Choose the file

```bash
nf events get -f '{"name": "cluster1"}' -s error --output cluster1-errors.csv
```

The file is overwritten on every run that finds events. Another run to the default name replaces `ems_output.csv`: the run below, for example, leaves the 3 informational events there and the earlier 5 errors are gone.

```bash
nf events get -f '{"name": "cluster1"}' -s informational -l 3
```

```
Getting events for cluster1...
Events written to ems_output.csv
Total events: 3
```

`nf events get --help` shows `-o events.csv` in its examples. That is wrong: `-o` is the global `--output-dir` option. Use `--output` for the file.

### 4. Look for specific events

`-n` (`--name`) takes an event name and can be repeated:

```bash
nf events get -n vsa.mlx.nic.detach -n vsa.mlx.nic.attach
```

Combine it with `-s` and `-l` to narrow further.

## Check it worked

The console ends with `Total events: N`, with `N` at most the limit times the number of clusters. Open the CSV and confirm the `severity` column holds only the level you asked for:

```bash
head -3 ems_output.csv
```

## If it fails

| You see | Cause | Fix |
| :--- | :--- | :--- |
| Only `Getting events for cluster1...`, and no file written | The cluster returned no events matching the filters | Widen the severity, drop `-n`, or raise `-l`. A file from an earlier run is left as it was. |
| `Could not retrieve events for cluster1: Could not find user for type='clusters', object='cluster1'...` | No credentials for the cluster | [Add an ONTAP cluster and validate it](add-ontap-cluster.md), step 2. |
| `Could not retrieve events for cluster1: ...` for another reason | The cluster is unreachable or rejected the request | Run `nf doctor`. |
| `Error: Invalid value for '--severity' / '-s': 'bogus' is not one of ...` (exit 2) | The severity is not one of the six levels | Use a listed level. |
| A cluster could not be read, yet the exit code is 0 | `nf events get` reports a per-cluster error and carries on | Read the output for `Could not retrieve events`, and do not rely on the exit code alone. |
| Events are old | The default sort is oldest first | Add `--sort -time`. |

## Next

- [Fill the cache and query it](fill-and-query-cache.md)
- [Find expiring licenses and export them to CSV](check-licenses.md)
- [Run nf unattended](run-unattended.md)
- [Usage basics: Event Monitoring](../usage/basics.md#event-monitoring)
