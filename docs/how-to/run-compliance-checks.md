---
title: Run Compliance Checks Against Your Fleet
description: Write compliance rules, run them against the cached cluster metadata with nf cache compliance, and read the results and exit codes
audience:
  - users
tags:
  - how-to
  - compliance
  - cache
---

# Run Compliance Checks Against Your Fleet

**Goal:** write a rules file, run `nf cache compliance` against every cached cluster, and use the exit code to see whether any rule found a violation.

## Before you start

- Clusters in the inventory: [Add an ONTAP cluster and validate it](add-ontap-cluster.md).
- A filled cache. The checks read the local cache and send no request to a cluster. Fill it with `nf cache refresh --all`, and see [Basic Usage: Cluster Metadata Caching](../usage/basics.md#cluster-metadata-caching). Check it with `nf cache status`.

## Steps

### 1. Find the model and field to test

A rule names a cache `model` and a `where` expression on a field of it. List every queryable path, and look for the field. The path is the `model` plus the field, and `[N]` marks a list:

```bash
nf cache schema --flat | grep -E "^  (nodes\[N\]\.state|storage\.volumes\[N\]\.autosize\.mode):"
```

```
  nodes[N].state: str
  storage.volumes[N].autosize.mode: str
```

So `nodes[N].state` is the field `state` of the model `nodes`, and `storage.volumes[N].autosize.mode` is the field `autosize.mode` of the model `storage.volumes`.

### 2. Write the rules file

Create `<config>/checks/compliance.toml`. The file must be named `compliance.toml`, and each rule is a top-level table whose key is the rule name:

```toml
[vol_autosize]
description = "Volumes must have autosize set to grow_shrink"
model = "storage.volumes"
where = "autosize.mode != 'grow_shrink'"
severity = "warning"

[node_down]
description = "All cluster nodes must be up"
model = "nodes"
where = "state != 'up'"
severity = "error"
```

A rule reports every record that matches its `where` expression, so write the expression for the bad state. `model` and `where` are required. `severity` is `info`, `warning` (the default) or `error`, in lower case. `enabled = false` keeps a rule in the file without running it. See [Compliance Checks](../usage/compliance-checks.md#writing-where-expressions) for the `where` syntax.

### 3. Change a rule for one cluster (optional)

A cluster's entry can override fields of a rule, disable it, or add a rule that only that cluster runs. Raising the severity of `vol_autosize` on `cluster1`, in its data file:

```toml
[clusters.cluster1.checks.compliance.vol_autosize]
severity = "error"
```

To skip a rule on one cluster, set `enabled = false` in the same table.

### 4. Run it

```bash
nf cache compliance --all
```

```
                            Compliance Check Results
┏━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Cluster  ┃ Rule         ┃ Severity ┃ Matches ┃ Description                   ┃
┡━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ cluster1 │ vol_autosize │ error    │ 2       │ Volumes must have autosize    │
│          │              │          │         │ set to grow_shrink            │
│ cluster1 │ node_down    │ error    │ 1       │ All cluster nodes must be up  │
│ cluster3 │ vol_autosize │ warning  │ 1       │ Volumes must have autosize    │
│          │              │          │         │ set to grow_shrink            │
└──────────┴──────────────┴──────────┴─────────┴───────────────────────────────┘
```

Each row is one rule on one cluster. `Matches` counts the records that broke the rule. `cluster1` shows `error` for `vol_autosize` because of the override in step 3. `cluster2` has no row because it broke no rule. This run exited 1.

Narrow the run with these options:

| Option | Use it to |
| :--- | :--- |
| `CLUSTER` | Check one cached cluster: `nf cache compliance cluster1`. |
| `--all` | Check every cached cluster. |
| `-f JSON` | Check the clusters that match a filter, such as `-f '{"env":"Prod"}'` or `-f '{"scope":"bu1"}'`. |
| `-k RULE` | Run one rule. |
| `-s LEVEL` | Show only results at this severity or above: `info`, `warning` or `error`. |

One of `CLUSTER`, `--all` or `-f` is required. Without one, the command prints `Must specify CLUSTER, --all, or --filter/-f` and exits 2.

### 5. Read the matches

The table counts the matches. To see which records matched, use `--json`. Each result carries the whole record in `matches`, which is long, so the output below keeps only the `name` of each match:

```bash
nf cache compliance cluster1 --json
```

```json
[
  {
    "rule_name": "vol_autosize",
    "description": "Volumes must have autosize set to grow_shrink",
    "model": "storage.volumes",
    "severity": "error",
    "cluster_name": "cluster1",
    "match_count": 2,
    "matches": [
      {"name": "vol_logs"},
      {"name": "vol_data_01"}
    ]
  },
  {
    "rule_name": "node_down",
    "description": "All cluster nodes must be up",
    "model": "nodes",
    "severity": "error",
    "cluster_name": "cluster1",
    "match_count": 1,
    "matches": [
      {"name": "cluster1-02"}
    ]
  }
]
```

For a spreadsheet, `--csv` prints one line per result and no matches:

```bash
nf cache compliance --all --csv
```

```
cluster,rule,severity,match_count,description
cluster1,vol_autosize,error,2,Volumes must have autosize set to grow_shrink
cluster1,node_down,error,1,All cluster nodes must be up
cluster3,vol_autosize,warning,1,Volumes must have autosize set to grow_shrink
```

### 6. Use the exit code

| Exit code | Meaning |
| :--- | :--- |
| `0` | No violation, after the `-s` filter. Nothing is printed. |
| `1` | One or more violations. They are printed. |
| `2` | An error: no cluster selected, an invalid or failing rule, or no usable config. Violations from valid rules are still printed. |

Treat `1` and `2` as failures in a schedule. See [Run nf unattended](run-unattended.md).

## Check it worked

The run in step 4 exits 1 because it found violations. Run one rule on one cluster to see a single row:

```bash
nf cache compliance --all -k node_down
```

```
                          Compliance Check Results
┏━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Cluster  ┃ Rule      ┃ Severity ┃ Matches ┃ Description                  ┃
┡━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ cluster1 │ node_down │ error    │ 1       │ All cluster nodes must be up │
└──────────┴───────────┴──────────┴─────────┴──────────────────────────────┘
```

A cluster with no violation prints nothing and exits 0. `cluster2` is one:

```bash
nf cache compliance cluster2
echo "exit $?"
```

```
exit 0
```

A row for each rule you expect, with the severity you set, shows that the rules file loaded.

## If it fails

| `nf cache compliance` shows | Cause | Fix |
| :--- | :--- | :--- |
| `No compliance rules defined in configuration.` (exit 0) | No file named `compliance.toml`, or its tables are not at the top level. A `[compliance.vol_autosize]` table in `settings.toml` is not read. | Create `<config>/checks/compliance.toml` as in step 2. |
| `Compliance rule 'compliance' [load]: model: Field required; where: Field required; vol_autosize: Extra inputs are not permitted` (exit 2) | The rules are under a `[compliance.<name>]` table inside `compliance.toml`, so the table `compliance` is read as one rule | Remove the `compliance.` prefix: write `[vol_autosize]`. |
| `Compliance rule 'node_down' [load]: where: Field required; wher: Extra inputs are not permitted` (exit 2) | A misspelled key, or a missing `where` | Fix the key. Valid rules still run. | <!-- codespell:ignore wher -->
| `Compliance rule 'vol_autosize' [load]: severity: Input should be 'info', 'warning' or 'error'` (exit 2) | `severity` is not one of the three, or is not lower case | Use `info`, `warning` or `error`. |
| `No cached clusters found. Use 'nf cache refresh' to populate.` | The cache is empty | `nf cache refresh --all` |
| No output and exit 0 for a cluster you expected to violate a rule | The cluster name has no cache, or its records do not match the `where` expression. A name that does not exist is not an error. | `nf cache status` lists the cached clusters. `nf cache schema --flat` lists the field paths. |
| `Must specify CLUSTER, --all, or --filter/-f` (exit 2) | No cluster selection | Add `--all`, a cluster name or `-f`. |

An invalid rule is never silent. Its reason is printed to stderr and the run exits 2, while the other rules still run. `-k RULE` limits the reported errors to that rule.

## Next

- [Compliance Checks](../usage/compliance-checks.md): the `where` syntax, more worked rules and a CI example
- [Query Layer](../usage/query-layer.md): the filter grammar
- [Run nf unattended](run-unattended.md): run the checks on a schedule
- [Use scopes to separate environments](use-scopes.md): check one scope with `-f '{"scope":"bu1"}'`
