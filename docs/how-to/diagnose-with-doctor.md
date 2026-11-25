---
title: Diagnose a Failing Setup with nf doctor
description: Run nf doctor, read each check section, and fix the common failures from the hint under them
audience:
  - users
tags:
  - how-to
  - doctor
  - troubleshooting
---

# Diagnose a Failing Setup with nf doctor

**Goal:** run `nf doctor`, find which check failed and why, and fix it from the hint printed under the failing row.

## Before you start

- A config directory, even a partly working one: [Set up a config directory and SOPS secrets](sops-secrets.md).
- Nothing else. `nf doctor --offline` makes no network request, so you can run it before any API works.

## Steps

### 1. Run the offline checks first

```bash
nf doctor --offline
```

`nf doctor` runs three groups of checks and shows each result as `ok`, `warning`, `error` or `skipped`. `--offline` runs the first two:

| Group | Section titles | What it checks |
| :--- | :--- | :--- |
| Config | `Config: Clusters`, `Config: Users`, `Config: Settings`, `Config: Cluster Credentials`, `Config: Spec Files` and others | The same static checks as `nf config validate`: the files parse, each object has credentials, and each configured API has its settings and spec file. |
| Environment | `SOPS`, `Caches`, `Console clusters` | `sops` is on `PATH`, the age key exists, every stored `SOPS[...]` value decrypts, no secret field holds a plaintext value (a warning), each cache (ONTAP, AIQUM, OCCM) exists and is not stale, and your cluster names match Console's, read from the OCCM cache. No value, token or ciphertext is printed. |
| Live | One section per API: `ONTAP`, `AIQUM`, `DII`, `Console`, `Digital Advisor` | One read-only request per configured API. See the setup guide for each API for the request. |

### 2. Read the result

Each row ends with its status, and a failing row has a hint under it. Warnings do not fail the run. Any error makes `nf doctor` exit 1, and the errors are listed again in a `Doctor Errors` box at the end, with the hints after it.

| Exit code | Meaning |
| :--- | :--- |
| `0` | No error. Warnings may be present. |
| `1` | At least one error, or an unknown `--scope`. |
| `2` | A bad option value, such as an unknown `--api`. |

### 3. Narrow the run

| Option | Use it to |
| :--- | :--- |
| `--offline` | Skip the live checks, so no request is sent. |
| `--api NAME` | Limit every check to one API or more (`ontap`, `aiqum`, `dii`, `console`, `digitaladvisor`, comma-separated). Each API keeps its settings, credentials, SOPS values, cache and live check, plus the shared `sops` and age-key checks. |
| `--scope NAME` | Check only one scope's settings, objects and Console account. See [Use scopes to separate environments](use-scopes.md). |
| `-f JSON` | Limit the ONTAP live and cache checks to the clusters that match, such as `-f '{"name": "cluster1"}'`. |
| `--json` | Print one JSON document instead of the tree. |

The options combine, for example `nf doctor --offline --api ontap`. `--json` has three top-level keys: `sections` (each with `title`, `group` and `results`), `summary` and `offline`. Use it to read the result in a script:

```bash
nf doctor --offline --json
```

```json
{
  "sections": [
    {
      "title": "Config: Clusters",
      "group": "static",
      "results": [
        {
          "subject": "clusters.cluster3",
          "status": "ok",
          "label": "cluster3",
          "errors": [],
          "hint": null
        },
...
  "summary": {"ok": 14, "warning": 0, "error": 0, "skipped": 5},
  "offline": true
}
```

The `summary` line above is shortened from the indented form that `nf doctor --json` prints. In `group`, the Config sections are `static` and the `SOPS` and `Caches` sections are `environment`.

### 4. Fix the first error, then run again

Fix the topmost error before the rest: a missing `ontapapi.toml` or an age key that is not found causes errors further down. Run `nf doctor --offline` after each fix, and the live check last.

## Check it worked

A healthy run ends with `0 error`, and exits 0. This is `nf doctor --offline` on a setup with three clusters, one of them in a scope, and a cache filled by `nf cache refresh`:

```
nf doctor
├── Config: Clusters
│   ├── cluster3
│   ├── cluster1
│   └── cluster2
├── Config: Users
│   └── clusters
├── Config: Settings
│   ├── ONTAP API
│   ├── DII API: Not configured (optional)
│   ├── Digital Advisor API: Not configured (optional)
│   ├── SMTP: Not configured (optional)
│   ├── Console: Not configured (optional)
│   └── Licensing: Not configured (optional)
├── Config: Cluster Credentials
│   ├── cluster3: bu1-admin
│   ├── cluster1: admin
│   └── cluster2: admin
├── Config: Spec Files
│   └── ONTAP spec
├── SOPS
│   ├── sops is installed
│   ├── age key: key file ~/.sops/age/keys.txt
│   ├── settings.users.clusters.enc: decrypts
│   └── scope.bu1.users.clusters.enc: decrypts
└── Caches
    └── ONTAP cache: v12, 3 entries, oldest entry 0 day(s) old

Summary: 14 ok, 0 warning, 0 error, 5 skipped (offline)
```

The age key line shows the path of your own key. `skipped` rows are the optional APIs that are not configured, and the live checks that `--offline` did not run.

Then the live check, which sends one read-only request per configured API:

```bash
nf doctor --api ontap -f '{"name": "cluster1"}'
```

Here `cluster1` is not reachable from where `nf` runs. The config and SOPS sections are cut:

```
...
├── Caches
│   └── ONTAP cache: v12, 3 entries, oldest entry 0 day(s) old
└── ONTAP
    └── cluster1: unreachable (ConnectTimeout)
        └── Check the address, the network path and any proxy.

Summary: 14 ok, 0 warning, 1 error, 0 skipped
╭─────────────────────────────── Doctor Errors ────────────────────────────────╮
│ - ONTAP: cluster1: unreachable (ConnectTimeout)                              │
╰──────────────────────────────────────────────────────────────────────────────╯
Doctor found 1 error(s)
ONTAP: Check the address, the network path and any proxy.
```

That run exited 1. When every API answers, each live row ends with `connected` and the exit code is 0. The output of a working setup is in each API's setup guide, such as [Add an ONTAP cluster and validate it](add-ontap-cluster.md#check-it-worked).

## If it fails

The fix is the hint printed under the failing row. These are the failures you are most likely to meet. Failures that belong to one API are in that API's guide.

| `nf doctor` shows | Cause | Fix |
| :--- | :--- | :--- |
| `cluster1: Missing credentials` | No user or password for the cluster in its entry, `users.toml` or the environment | `nf config set-credential --cluster cluster1 --user USER`. For a scope, see [Use scopes](use-scopes.md#if-it-fails). |
| `ONTAP API: Not configured` (warning), then `cluster1: Missing configuration key 'ontapapi'...` under `ONTAP` | `<config>/apis/ontap/ontapapi.toml` does not exist | Create it with a `[general]` table, as in [Add an ONTAP cluster](add-ontap-cluster.md#3-add-the-ontap-api-settings). Its hint, `See nf config validate`, points at the same warning. |
| `ONTAP spec: missing <path>` | The API spec file is not downloaded | `nf config download-spec --api ontap`. Use `aiqum`, `dii` or `console` for the others. |
| `age key missing: key file <path>` | No key at the path shown | `nf config init-sops`, or set `SOPS_AGE_KEY_FILE` to your key. |
| `<field>: SOPS value does not decrypt (SOPSError)` | The key in use did not encrypt the stored value | Point `SOPS_AGE_KEY_FILE` at the right key, or store the value again with `nf config set-credential`. |
| `<field>: plaintext (not SOPS-encrypted)` (warning) | A secret field holds a plaintext value | Run the `nf config set-credential` command in the hint. See [SOPS: If it fails](sops-secrets.md#if-it-fails). |
| `ONTAP cache: not found (<path>)` (warning) | The cache has not been filled | `nf cache refresh --all`. |
| `cluster1: unreachable (ConnectTimeout)` | The `ip` is wrong, or the network path or a proxy blocks it | Check the `ip`, routing and any proxy. |
| `cluster1: HTTP 401` or `HTTP 403` | The API rejected the credentials, or the account cannot read the endpoint | Store the credentials again, or use an account with read access. See the API's guide. |
| `cluster1: identity changed` | The host's TLS certificate changed since it was first recorded | Follow the reset hint printed below it, after confirming the change is expected. |
| `Unknown scope 'nope' (available scopes: bu1).` (exit 1) | The scope has no `scope.toml`, or the name is misspelled | See [Use scopes](use-scopes.md#if-it-fails). |
| `Invalid value for --api: unknown API 'bogus'; choose from ontap, aiqum, dii, console, digitaladvisor` (exit 2) | A misspelled API name | Use one of the names listed. |

For the live failures of each API, see the "If it fails" table in [AIQUM](setup-aiqum.md#if-it-fails), [DII](setup-dii.md#if-it-fails), [Digital Advisor](setup-digital-advisor.md#if-it-fails) and [Console](setup-console.md#if-it-fails).

## Next

- [CLI reference: doctor](../reference/cli.md#doctor): every option
- [Use scopes to separate environments](use-scopes.md)
- [Run nf unattended](run-unattended.md): use the exit code of `nf doctor` or `nf config validate` in a schedule
- [ADR-0035](../decisions/0035-nf-doctor-runs-static-environment-and-read-only-live-checks-with-fix-hints.md): why `nf doctor` is built this way
