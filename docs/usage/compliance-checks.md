---
title: Compliance Checks
description: Configure and run config-driven compliance checks against cached cluster metadata
audience:
  - users
tags:
  - compliance
  - cache
  - cli
---

# Compliance Checks

`nf cache compliance` evaluates declarative compliance rules against cached
cluster metadata. Rules are defined in TOML, target a cache model, and use a
filter expression — any record that matches the filter is reported as a
violation.

This page covers the configuration file format, per-cluster overrides, the
CLI, and worked examples you can copy directly into your own
`checks/compliance.toml`.

## Overview

Compliance checks are designed for **scheduled, repeatable** policy enforcement
across many clusters. They read entirely from the local cache database, so
they are fast, deterministic, and safe to run from CI.

| | `nf cache compliance` | `nf cache check` |
|--|--|--|
| Source | TOML config (`[compliance]`) | Ad-hoc CLI flags |
| Scope | Many rules, many clusters | One filter, one model |
| Output | Table / JSON / CSV with severity | Raw matches |
| Exit code | 0 / 1 / 2 (CI-friendly) | 0 on success |
| Use case | Scheduled audits, CI gates | Interactive investigation |

Use `nf cache check` when you are exploring; promote a stable expression into
`[compliance]` once you want it enforced everywhere.

## Quick start

Add a `[compliance]` section to your settings TOML (typically
`~/.config/pynetappfoundry/settings.toml` or the project-local equivalent):

```toml
[compliance.vol_autosize]
description = "Volumes must have autosize set to grow_shrink"
model = "storage.volumes"
where = "autosize.mode != 'grow_shrink'"
severity = "warning"
```

Then run it against every cached cluster:

```bash
nf cache compliance --all
```

If any volume on any cached cluster has the wrong autosize mode, the command
exits with status `1` and prints a table of violations.

## Configuration file format

Each compliance rule is a table under `[compliance]`. The table key becomes
the rule name; the table values populate a
[`ComplianceRule`](../reference/api.md) Pydantic model.

```toml
[compliance.<rule_name>]
description = "Human-readable description"   # optional, default ""
model       = "storage.volumes"               # REQUIRED — cache model path
where       = "autosize.mode != 'grow_shrink'" # REQUIRED — filter expression
severity    = "warning"                       # optional, default "warning"
enabled     = true                            # optional, default true
```

| Field | Required | Default | Description |
|-------|----------|---------|-------------|
| (rule name) | yes | — | Taken from the TOML key, e.g. `[compliance.vol_autosize]` becomes rule `vol_autosize`. |
| `description` | no | `""` | Human-readable description shown in output. |
| `model` | **yes** | — | Cache model path (run `nf cache schema --flat` to discover paths). |
| `where` | **yes** | — | Filter expression — any matching record is a violation. See [Writing `where` expressions](#writing-where-expressions). |
| `severity` | no | `"warning"` | One of `info`, `warning`, `error`. |
| `enabled` | no | `true` | Set to `false` to keep a rule definition without running it. |

Invalid rule entries are skipped with a logged warning rather than failing
the whole run, so a typo in one rule will not block the others.

A reserved key `[compliance.settings]` is ignored by the loader and may be
used for future tuning knobs.

## Per-cluster overrides

Cluster-specific behaviour lives under each cluster entry, using the path
`[clusters.<NAME>.checks.compliance.<rule_name>]`. The merge logic in
`compliance/config.py` (`merge_rules`) supports three patterns.

### 1. Override individual fields

Only the fields you set are applied; everything else is inherited from the
global rule.

```toml
[compliance.vol_autosize]
model    = "storage.volumes"
where    = "autosize.mode != 'grow_shrink'"
severity = "warning"

[clusters.prod-cluster1.checks.compliance.vol_autosize]
severity = "error"   # raise severity for this cluster only
```

### 2. Disable a global rule for one cluster

```toml
[clusters.lab-cluster1.checks.compliance.vol_autosize]
enabled = false
```

The rule still exists in the global config and runs everywhere else.

### 3. Add a cluster-specific rule

A rule that exists only on one cluster must include `model` **and** `where`,
otherwise it is skipped with a warning.

```toml
[clusters.prod-cluster1.checks.compliance.tenant_a_volumes_online]
description = "Tenant A volumes must be online"
model       = "storage.volumes"
where       = "state != 'online'"
severity    = "error"
```

## CLI usage

```text
Usage: nf cache compliance [OPTIONS] [CLUSTER]

  Run compliance checks against cached cluster metadata.
```

| Option | Description |
|--------|-------------|
| `CLUSTER` (positional) | Run checks against a single cached cluster by name. |
| `--all` | Run checks against every cached cluster. Mutually exclusive with `CLUSTER`. |
| `-f, --filter TEXT` | JSON object filter for cluster selection, e.g. `'{"bu":"Business","env":"Prod"}'`. Matches against cluster entry metadata. |
| `-k, --check TEXT` | Run only the named compliance rule (the TOML key). |
| `-s, --severity [info\|warning\|error]` | Minimum severity to report. `warning` hides `info`; `error` hides everything below. |
| `--json` | Emit results as JSON. |
| `--csv` | Emit results as CSV with a header row. |
| `--help` | Show the inline help and exit. |

### Examples

```bash
# Single cluster, all rules
nf cache compliance cluster1

# All cached clusters
nf cache compliance --all

# Filter clusters and run a specific rule
nf cache compliance -f '{"env":"Prod"}' -k vol_autosize

# Errors only
nf cache compliance --all -s error

# JSON for scripting
nf cache compliance --all --json

# CSV for spreadsheets / Splunk ingest
nf cache compliance --all --csv > violations.csv
```

### Example output

Table (default):

```text
Severity  Cluster        Rule           Matches  Description
error     prod-cluster1  vol_autosize   12       Volumes must have autosize set to grow_shrink
warning   prod-cluster2  node_down      1        All nodes must be up
```

JSON (`--json`):

```json
[
  {
    "rule_name": "vol_autosize",
    "description": "Volumes must have autosize set to grow_shrink",
    "model": "storage.volumes",
    "severity": "error",
    "cluster_name": "prod-cluster1",
    "match_count": 12,
    "matches": [{"name": "vol_data_01", "autosize": {"mode": "off"}}]
  }
]
```

CSV (`--csv`):

```csv
severity,cluster,rule,match_count,description
error,prod-cluster1,vol_autosize,12,Volumes must have autosize set to grow_shrink
warning,prod-cluster2,node_down,1,All nodes must be up
```

## Exit codes

| Code | Meaning |
|------|---------|
| `0`  | No violations matched (after severity filtering). |
| `1`  | One or more violations found. |
| `2`  | Error — bad config, unknown cluster, query engine failure, etc. |

Both `1` and `2` should be treated as failures in CI: see
[CI integration](#ci-integration).

## Writing `where` expressions

The `where` field is a filter expression interpreted by the cache query
engine. Each rule expression is a single comparison of the form:

```text
<dotted.field.path> <operator> <value>
```

Supported operators (from `cache/query_engine.py`):

| Operator | Example |
|----------|---------|
| `=`      | `name = 'vol1'` |
| `!=`     | `autosize.mode != 'grow_shrink'` |
| `<` `<=` `>` `>=` | `size > 1073741824` |
| `in (...)` | `state in ('offline', 'mixed')` |
| `not in (...)` | `state not in ('online')` |

Value types:

- **Strings** — single-quoted: `'grow_shrink'`
- **Integers / floats** — bare: `1073741824`, `0.85`
- **Booleans** — `true`, `false`
- **Null** — `null` (for missing or unset fields)
- **Tuples** — `('a', 'b', 'c')` for `in` / `not in`

Field paths are dotted and may traverse nested JSON, e.g.
`autosize.grow_threshold` or `snapshot_policy.name`. Run
`nf cache schema --flat` to list every queryable path for every model.

For the full grammar — boolean composition, escaping, quoting rules — see
the [Query Layer](query-layer.md) page.

## Worked examples

The model paths and field names below were verified with
`nf cache schema --flat` against the current schema. Copy them into your
`[compliance]` section as a starting point.

### Volume autosize must be `grow_shrink`

```toml
[compliance.vol_autosize]
description = "Volumes must have autosize.mode set to grow_shrink"
model       = "storage.volumes"
where       = "autosize.mode != 'grow_shrink'"
severity    = "warning"
```

Verified field: `storage.volumes[N].autosize.mode`.

### Nodes must be up

```toml
[compliance.node_down]
description = "All cluster nodes must be in the 'up' state"
model       = "nodes"
where       = "state != 'up'"
severity    = "error"
```

Verified field: `nodes[N].state`.

### Volumes must use the `default` snapshot policy

```toml
[compliance.vol_snapshot_policy]
description = "Volumes must use the 'default' snapshot policy"
model       = "storage.volumes"
where       = "snapshot_policy.name != 'default'"
severity    = "warning"
```

Verified field: `storage.volumes[N].snapshot_policy.name`. To catch volumes
with no policy attached at all, add a second rule using `null`:

```toml
[compliance.vol_snapshot_policy_missing]
description = "Volumes must have a snapshot policy attached"
model       = "storage.volumes"
where       = "snapshot_policy.name = null"
severity    = "error"
```

### Per-cluster override: stricter on production

Reuse the global `vol_autosize` rule but raise its severity to `error` on a
specific production cluster:

```toml
[compliance.vol_autosize]
description = "Volumes must have autosize.mode set to grow_shrink"
model       = "storage.volumes"
where       = "autosize.mode != 'grow_shrink'"
severity    = "warning"

[clusters.prod-cluster1.checks.compliance.vol_autosize]
severity = "error"
```

`prod-cluster1` will now report violations as `error` (and trip stricter
CI gates), while every other cluster keeps the global `warning` severity.

## CI integration

`nf cache compliance` is designed to be a one-line CI gate. The command
exits non-zero on violations (`1`) **and** on errors (`2`), so a simple
GitHub Actions step is enough:

```yaml
name: Compliance

on:
  schedule:
    - cron: "0 6 * * *"   # daily at 06:00 UTC
  workflow_dispatch:

jobs:
  compliance:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v6
      - run: uv sync
      - name: Refresh cache
        run: uv run nf cache refresh --all
      - name: Run compliance checks
        run: uv run nf cache compliance --all
```

If `nf cache compliance --all` exits `1` (violations) or `2` (error), the
job fails and the workflow turns red. Pipe `--json` or `--csv` into an
artifact upload step if you want to publish the report.

## Related

- [`nf cache check`](../reference/cli.md#cache) — interactive,
  one-shot variant for ad-hoc investigation.
- [Query Layer](query-layer.md) — full grammar for `where` expressions.
- A standalone HTML compliance report is tracked as follow-up
  [issue #463](https://github.com/endavis/pynetappfoundry/issues/463).
