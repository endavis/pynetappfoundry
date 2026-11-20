---
title: CLI Reference
description: Command-line interface documentation
audience:
  - users
tags:
  - reference
  - cli
---

# CLI Reference

Complete reference for the `nf` command-line interface.

## Global Options

All commands support these global options:

| Option | Description |
|--------|-------------|
| `--version` | Show version and exit |
| `-c, --config-dir PATH` | Configuration directory path |
| `-o, --output-dir PATH` | Output directory path |
| `--debug / --no-debug` | Enable debug logging and print full tracebacks for unexpected errors |
| `--help` | Show help and exit |

### Cluster Filter Convention

Most commands accept `-f, --filter` to narrow the set of clusters they act on.
The filter is a JSON object matched against cluster metadata fields such as
`bu` (business unit) and `env` (environment):

```bash
-f '{"bu":"Business","env":"Prod"}'
```

The built-in `scope` key matches the [scope](config-schema.md#scopes) a cluster
belongs to; `""` means a cluster outside any scope:

```bash
-f '{"scope":"Org1"}'
-f '{"scope":"Org1","env":"Prod"}'
```

## Commands

### licenses

License management commands.

```bash
nf licenses [OPTIONS] COMMAND [ARGS]...
```

**Subcommands:**

| Command | Description |
|---------|-------------|
| `get` | Get license information from clusters |
| `check` | Check clusters for licensing issues |
| `savings` | Calculate license savings information |

**`licenses get` options:**

| Option | Description |
|--------|-------------|
| `-f, --filter TEXT` | JSON cluster filter, e.g. `'{"bu":"Business","env":"Prod"}'` |
| `--csv` | Output to CSV file instead of console table |
| `--output PATH` | CSV output file path (default: timestamped file in output dir) |
| `--live` | Bypass the cache and fetch licenses live from each cluster |

!!! note "About `--live`"
    The `--live` flag bypasses the metadata cache and fetches every license
    field group directly from each cluster over the network. This is
    **significantly slower** than the default cache-backed path. Currently
    `licenses get` is the only command that supports `--live`; all other
    commands in this reference read from the cache.

**`licenses check` options:**

| Option | Description |
|--------|-------------|
| `-f, --filter TEXT` | JSON cluster filter |
| `--send-email / --no-send-email` | Send email notification (default: enabled) |

**`licenses savings` options:**

| Option | Description |
|--------|-------------|
| `-f, --filter TEXT` | JSON cluster filter |

### reports

Report generation commands.

```bash
nf reports [OPTIONS] COMMAND [ARGS]...
```

**Subcommands:**

| Command | Description |
|---------|-------------|
| `html` | Generate HTML reports with hierarchical tree view |
| `inventory` | Generate the inventory spreadsheet (Excel) |
| `locks` | Generate client lock reports (Excel) |
| `space-usage` | Generate space usage reports (Excel) |

All `reports` subcommands accept `-f, --filter` to scope the report to a
subset of clusters.

`inventory` and `html` read AWS cloud provider details from the OCCM cache first and fall back to
the ONTAP CLI path per cluster (Azure and GCP always use the CLI path); see [Report Cloud Details](../usage/report-cloud-details.md).

### events

Event management commands.

```bash
nf events [OPTIONS] COMMAND [ARGS]...
```

**Subcommands:**

| Command | Description |
|---------|-------------|
| `get` | Get EMS events from clusters |
| `save-azure` | Save Azure maintenance events to database |

**`events get` options:**

| Option | Description |
|--------|-------------|
| `-f, --filter TEXT` | JSON cluster filter |
| `-s, --severity` | Filter by severity: `emergency`, `alert`, `error`, `notice`, `informational`, `debug` |
| `-n, --name TEXT` | Filter by event name (repeatable) |
| `--output PATH` | Output to CSV file instead of console |
| `--sort [time|-time]` | Sort order (default: `time` ascending; `-time` for descending) |
| `-l, --limit INTEGER` | Maximum number of events to retrieve (default: 50) |

`nf events get` shows `Time`, `Node`, `Severity`, `Name`, and `Message` in the console table. CSV output includes `cluster`, `node`, `time`, `name`, `severity`, and `message` columns.

**`events save-azure` options:**

| Option | Description |
|--------|-------------|
| `-f, --filter TEXT` | JSON cluster filter |

### cifs

CIFS / SMB inspection commands.

```bash
nf cifs [OPTIONS] COMMAND [ARGS]...
```

**Subcommands:**

| Command | Description |
|---------|-------------|
| `session` | List active CIFS/SMB sessions across in-scope clusters |
| `find-user` | (Legacy) Find CIFS sessions for a user via the netapp_ontap SDK |

**`cifs session` options:**

| Option | Description |
|--------|-------------|
| `-f, --filter TEXT` | JSON cluster filter |
| `-u, --user TEXT` | Match `user` or `mapped_unix_user`. Substring by default; glob when `*`, `?`, or `[` is present |
| `-i, --ip TEXT` | Match `client_ip`. Exact IP, glob (`10.1.2.*`), or CIDR (`10.1.2.0/24`) |
| `--case-sensitive / --case-insensitive` | Match the `--user` pattern case-sensitively (default: case-insensitive) |
| `-c, --csv PATH` | Write results to a CSV file *in addition to* the table. If PATH is a directory, writes `cifs_sessions_<YYYYMMDD-HHMMSS>.csv` inside it |

CIFS sessions are transient and never cached; every invocation queries each in-scope cluster live via the ONTAP REST API (there is no `--live` flag because there is no cache to bypass). The Rich table renders without column truncation regardless of terminal width; the CSV export uses the same headers.

### metrics

Metrics commands.

```bash
nf metrics [OPTIONS] COMMAND [ARGS]...
```

**Subcommands:**

| Command | Description |
|---------|-------------|
| `dump-dii` | Dump per-volume DII metrics into SQLite |

**`metrics dump-dii` options:**

| Option | Description |
|--------|-------------|
| `-f, --filter TEXT` | JSON cluster filter |
| `-d, --date TEXT` | **Required.** Anchor date in `YYYY-MM-DD` format. The query window is centered on this date in UTC (see `--window-days`) |
| `--interval TEXT` | Aggregation interval forwarded to DII (default: `60s`; accepts e.g. `5m`, `1h`) |
| `--window-days INTEGER` | Total UTC days in the query window centered on `--date` (default: `3`, yielding `(date - 1 day)` through `(date + 2 days)`) |

`metrics dump-dii` writes one SQLite database per cluster per date (`{cluster}_{date}_metrics.db`) and stores each SVM/volume pair in its own table (`{vserver_name}-{volume_name}`).

### cache

Cluster metadata cache management. The cache stores discoverable ONTAP cluster information that doesn't change frequently. `nf cache aiqum` manages the separate AIQUM cache.

```bash
nf cache [OPTIONS] COMMAND [ARGS]...
```

**Subcommands:**

| Command | Description |
|---------|-------------|
| `refresh` | Refresh the metadata cache for cluster(s) |
| `show` | Display cached metadata for a cluster |
| `query` | Query specific fields from cached metadata |
| `check` | Query cached model data with filtering |
| `compliance` | Run config-driven compliance checks against cached data |
| `schema` | Display the cache metadata schema |
| `status` | Show cache status for all clusters |
| `clear` | Clear the metadata cache |
| `history` | View cache change history (see below) |
| `inspect` | Inspect cache, CLI, and API data for a single object |
| `occm` | Refresh and inspect the Console agent (OCCM) cache (see below) |
| `aiqum` | Manage the AIQUM cache (see below) |

**`cache history` sub-subcommands:**

| Command | Description |
|---------|-------------|
| `list` | List change history events (optionally filtered by cluster, limit, or date range) |
| `show` | Show full details of a specific change by change ID |
| `diff` | Show a human-readable formatted diff for a specific change |
| `snapshot` | Get the cache state for a cluster at a specific date (optionally `--restore`) |

```bash
# List recent changes for a cluster
nf cache history list cluster1 -n 50

# Show the formatted diff for change #5
nf cache history diff 5

# Snapshot a cluster's cached state as of a given date
nf cache history snapshot cluster1 -d 2024-06-01
```

**`cache occm` sub-subcommands:**

| Command | Description |
|---------|-------------|
| `refresh [--scope NAME]` | Discover the Console agents and refresh the OCCM cache; `--scope` limits it to one configured Console account scope and leaves the other scopes' cache untouched. Exits 1 if any agent failed (the cache is still written) |
| `status [--ttl DAYS]` | Per-agent table: discovery status, mappings, records, oldest `cached_at`, age and Fresh, Stale or Not collected |
| `agents [PUBLIC_ID]` | The agents that manage a working environment, or every working environment and its agents |
| `clear [AGENT_ID] [--all] [--force]` | Clear one agent's cached rows, or everything with `--all`; asks for confirmation unless `--force` |

```bash
nf cache occm refresh --scope prod
nf cache occm status --ttl 7
nf cache occm agents <publicId>
nf cache occm clear --all -f
```

**`cache aiqum` sub-subcommands:**

| Command | Description |
|---------|-------------|
| `refresh` | Collect an AIQUM instance (or `-a, --all` configured instances) into the cache |
| `status` | Show cached instances and mappings with Fresh, Stale, Not cached or Orphaned status (`-t, --ttl` days, default 30) |
| `clear` | Clear one instance or `-a, --all` (`-f, --force` skips the prompt) |

```bash
# Refresh every configured AIQUM instance
nf cache aiqum refresh --all

# Show the AIQUM cache status, stale after 7 days
nf cache aiqum status --ttl 7

# Clear one instance without confirmation
nf cache aiqum clear aiqum1 -f
```

`cache inspect` takes a cluster name and an object name, and accepts
`-t, --type` to choose the object type (default: `volume`; other values include
`aggregate`, `broadcast_domain`, `cloud_metadata`, `cluster_peer`, `license`,
`network_lif`, `node`, `svm`).

### config

Configuration management commands. View and validate pynetappfoundry
configuration, bootstrap SOPS encryption, and store encrypted credentials.

```bash
nf config [OPTIONS] COMMAND [ARGS]...
```

**Subcommands:**

| Command | Description |
|---------|-------------|
| `show` | Display current configuration (sensitive values masked by default) |
| `validate` | Validate configuration files |
| `init-sops` | Initialize SOPS encryption with age for credential storage |
| `set-credential` | Set encrypted credentials for a cluster, resource type or settings secret |
| `download-schema` | Download an API's GraphQL schema into the config directory |
| `download-spec` | Download the committed API specs of the installed release into the config directory |

**`config show` options:**

| Option | Description |
|--------|-------------|
| `-s, --section TEXT` | Show only a specific section (e.g. `clusters`, `settings`, `users`) |
| `--scope TEXT` | Show only this [scope](config-schema.md#scopes)'s own files, not a merged view: its objects, its `users`, `monitoring` and `consoleapi` files (`enc` masked) and its `scope.toml` description and tags. Keys the scope does not set fall back to the root. `-s` selects one of those sections. An unknown scope exits 1 |
| `--unmask` | Show passwords and tokens unmasked (use with caution) |

Without `--scope` the summary adds a `Scopes:` line when the config has scopes.

**`config validate` options:**

| Option | Description |
|--------|-------------|
| `--scope TEXT` | Check this scope instead of the root settings: its clusters, AIQUM, connectors and Cloud Insights tenants with their credentials, its `users.toml` sections (errors are keyed `<scope>/users...`), its `monitoring.toml` and its Console account (`Not configured (optional)` when it has no `consoleapi.toml` `[general]`). It checks no spec file. An unknown scope exits 1 |

Checks that all configuration files parse and
contain valid values. A settings section that is absent is reported as not
configured; one that is present but invalid, or whose `SOPS[...]` value cannot be
decrypted, is reported as Invalid. Without `--scope` the root settings are checked,
including a root Console row (`Console: Not configured (optional)` without an account; a
broken account fails validation).

When a Console account has a `client_id` but no `client_secret` and `users.toml` `[console]`
holds a token, validate adds a hint: the secret was probably stored as a refresh token. It
gives the exact `nf config set-credential --setting consoleapi.client_secret` command, with
`--scope NAME` for a scope.

Validate also checks, in root mode, the `aiqumapi.toml` `[general]` section (an error when the `[aiqums]`
inventory exists without it), each `[aiqums]`, `[connectors]` and `[cloudinsights]` entry, the credentials
of each AIQUM and Cloud Insights tenant, and the spec file of every configured API in `<config>/apis/`.
These sections appear only when they have rows. A missing credential or an invalid entry is an error
(exit 1); a missing spec file is a warning (exit 0) whose hint is `nf config download-spec --api API`. An
error is followed by a fix hint, for example `nf config set-credential --type aiqums --name NAME --user USER`.
No check calls the network or prints a secret. To also check the environment and API
access, use [`nf doctor`](#doctor). See
[Configuration: What `nf config validate` checks](../getting-started/configuration.md#what-nf-config-validate-checks).

**`config init-sops` options:**

| Option | Description |
|--------|-------------|
| `--key-path PATH` | Path to store the age private key (default: `~/.sops/age/keys.txt`) |
| `--force` | Overwrite existing key file |

**`config set-credential` options:**

| Option | Description |
|--------|-------------|
| `--cluster TEXT` | Set credentials for a specific cluster. Alias for `--type clusters --name TEXT` |
| `--type` | Set default credentials for all resources of a type: `aiqums`, `azure`, `cloudinsights`, `clusters`, `connectors`, `console`, `ibm` (`console` stores the Console refresh token, not the client secret; `--user` is only a label and the password prompt takes the token. Store the client secret with `--setting consoleapi.client_secret`) |
| `--setting TARGET` | Store one SOPS-encrypted settings secret: `consoleapi.client_secret`, `consoleapi.service_token`, `consoleapi.user_token`, `diiapi.api_ro_token`, `digitaladvisorapi.personal_access_token`, `digitaladvisorapi.access_token`, `digitaladvisorapi.refresh_token` or `settings.smtp_password`. Prompts for the value (hidden, with confirmation) or takes `--password`, encrypts it and writes `<field> = "SOPS[...]"` into the right file and table, keeping comments. Cannot be combined with `--cluster`, `--type`, `--name`, `--user` or `--no-encrypt`; needs `sops` (no plain text fallback). If more than one non-data file carries the target's stem, it refuses and lists them |
| `--name TEXT` | With `--type`, set credentials for that one inventory object, written to its data file entry. An unknown name lists the available ones. For a token-style secret, `--user` is only a label and the password prompt takes the token. Not valid with `--cluster` or `--type console` |
| `--scope TEXT` | With `--type` alone, write to `<config>/<scope>/users.toml` (created if missing) instead of the root `users.toml`. With `--cluster` or `--name`, it must equal the object's own scope; a mismatch fails, names the object's real scope (or the root) and writes nothing. An unknown scope lists the available ones. With `--setting`, only `consoleapi.*` targets accept it: the value goes to `<config>/<scope>/consoleapi.toml` `[general]`, created if missing |
| `--user TEXT` | Username (required with `--cluster` and `--type`, not allowed with `--setting`) |
| `--password TEXT` | Password, or with `--setting` the value (will prompt, hidden, if not provided) |
| `--no-encrypt` | Store password as plain text (not recommended) |

Without `--scope`, `--type console` writes the root Console account's refresh token. With `--scope Org1` it writes the refresh token to the `[console]` section of the scope's own `users.toml`; a warning is printed when that scope has no Console account (a `[general]` table in its own `consoleapi.toml`), and the token is still written.

`--setting` prints the file, table and key it wrote and `Value: (encrypted)`, never the value. It warns when the counterpart is missing: `client_secret` without `client_id`, SMTP `password` without `user`, or a newly created `consoleapi.toml` (it still needs `client_id` and `org_id`). A missing file is created, a root API settings file in `<config>/apis/<name>/` and a scope file in the scope directory; an unknown scope is rejected.

`nf config encrypt-value` was removed in favour of `--setting` (see [ADR-0031](../decisions/0031-one-command-stores-every-sops-secret-and-encrypt-value-is-removed.md)).

**`config download-schema` options:**

| Option | Description |
|--------|-------------|
| `--api` | API whose schema to download. Only `digitaladvisor` (the default) |

Sends the GraphQL introspection query with no `Authorization` header (introspection needs no credentials, so this works before any token is set) and writes `<config>/apis/digitaladvisor/schema.json`, replacing an existing file. It prints the path and the number of types. `graphql_url` and `timeout` come from `digitaladvisorapi.toml` `[general]` when set, otherwise the defaults. A network error, a non-2xx status or a response without `data.__schema` exits 1 and writes nothing. See [Digital Advisor API](../usage/digital-advisor-api.md#schema).

**`config download-spec` options:**

| Option | Description |
|--------|-------------|
| `--api` | `ontap`, `aiqum`, `dii` or `console`. Without it, every configured API whose spec is missing |
| `--force` | Replace a spec that already exists |

Downloads the committed spec from GitHub at the installed release (the tag `v<version>`, or for a development build the commit its version names) and writes it verbatim to `<config>/apis/ontap/all.json`, `<config>/apis/aiqum/all.json`, `<config>/apis/dii/all.json` or `<config>/apis/console/console_openapi.yaml`. `--api` handles that API even when it is not configured. An existing file is skipped without `--force`; when nothing is to be done it says so and exits 0. The download must parse (YAML for `.yaml`, else JSON) and have a `paths` map before it is written. A version with no release or commit, an unknown ref (a development build's commit that was not pushed), an HTTP error, a network error or an unusable body exits 1 and writes nothing for that API; the other APIs are still downloaded. It never writes `apis/occm/`. See [Configuration guide: Spec files](../getting-started/configuration.md#spec-files) and [ADR-0038](../decisions/0038-nf-config-download-spec-fetches-the-committed-api-specs-of-the-installed-release.md).

### doctor

Check the configuration, the environment and API access, with a fix hint for each problem.

```bash
nf doctor [OPTIONS]
```

It runs three groups of checks and shows each result as `ok`, `warning`, `error` or `skipped`:

1. **Config:** the static checks of `nf config validate`, with section titles prefixed `Config:`.
2. **Environment (offline):** `sops` on PATH, the age key, that every `SOPS[...]` value decrypts (no value is printed), each cache (ONTAP, AIQUM, OCCM) by presence, age (stale after 30 days) and schema version, and that your `[clusters]` names match Console's. Caches are opened read-only: doctor never creates or migrates one.
3. **Live:** one read-only `GET` per configured API: ONTAP `/cluster` (and that the configured name matches), AIQUM `/datacenter/cluster/clusters?max_records=1`, DII `/assets/storages/count`, Digital Advisor one GraphQL query (`volumes(pageSize: 1) { cursor }`), and for Console a token per account, the organizations, the agents and each active agent's `about`. The Console OAuth token request is a `POST` to the token endpoint (it changes no Console resource); accounts with a static token make none. The Digital Advisor query is a `POST` that reads only. A personal access token is only probed; with both credentials a rejected PAT falls back to the refresh pair and the row is a WARNING with a PAT renewal hint; a refresh-token pair is probed with the stored access token, and only a missing, expired or rejected one is refreshed, with the rotated tokens written to `digitaladvisorapi.toml` (the row says so). No Digital Advisor row appears when it is not configured. The first contact with an ONTAP or AIQUM host records its TLS fingerprint in the local trust store, as `nf utils validate` does.

**`doctor` options:**

| Option | Description |
|--------|-------------|
| `--offline` | Skip the live checks: no network request is made |
| `--api TEXT` | Limit every check to these APIs: `ontap`, `aiqum`, `dii`, `console`, `digitaladvisor` (comma-separated, case-insensitive). Each API keeps its settings, credentials, SOPS values, cache and live check, plus the shared `sops` and age-key checks when it has SOPS values. SMTP, Licensing, Monitoring, Azure and IBM rows are hidden. An unknown name exits 2 |
| `--scope TEXT` | Check only this scope's settings, objects and Console account. An unknown scope exits 1 |
| `-f, --filter TEXT` | JSON cluster filter for the ONTAP live and cache checks and the Console cluster comparison |
| `--json` | Print one JSON document: `sections` (each with `title`, `group` and `results`), `summary` and `offline` |

**Console cluster names:** a `[clusters.NAME]` key must equal the cluster's name in Console; when Console reports no cluster name for a working environment (seen on some Azure working environments), the working environment name is used instead. With `--api ontap` or `--api console` (or neither), the "Console clusters" section compares the config with the OCCM cache, per Console account, offline. A key Console knows under another name (found by cluster UUID, then by any management IP, node LIFs included) is an `error`, with a hint to rename the key. A key not found in Console, and a Console cluster not in your config, are `warning`s. A missing or stale OCCM cache is a `warning` with the hint `nf cache occm refresh`; nothing is compared then. With `-f`, Console-only clusters are not reported.

Exit code 1 when any result is an `error`; warnings do not fail. No output contains a credential, a token or a ciphertext. A DII `403` is a warning (the token authenticated but lacks the Assets read scope); a `401` is an error.

```bash
nf doctor
nf doctor --offline
nf doctor --api console --scope Org1
nf doctor --offline --api console
nf doctor --api digitaladvisor
nf doctor --json
```

Use `nf config validate` for an offline check in CI. See [ADR-0035](../decisions/0035-nf-doctor-runs-static-environment-and-read-only-live-checks-with-fix-hints.md) and [Configuration: nf doctor or nf config validate](../getting-started/configuration.md#nf-doctor-or-nf-config-validate).

### utils

Utility commands.

```bash
nf utils [OPTIONS] COMMAND [ARGS]...
```

**Subcommands:**

| Command | Description |
|---------|-------------|
| `validate` | Validate cluster connectivity and configuration |
| `run-cmd` | Run an ONTAP CLI command on matching clusters via SSH |
| `sqlite-to-excel` | Convert a SQLite database to an Excel workbook |

**`utils validate` options:**

| Option | Description |
|--------|-------------|
| `-f, --filter TEXT` | JSON cluster filter |
| `--ssh / --no-ssh` | Also validate SSH connectivity (default: disabled) |

For a broader check with fix hints, see [`nf doctor`](#doctor).

**`utils run-cmd`**: takes a single quoted ONTAP CLI command as its argument,
and accepts `-f, --filter` to select clusters.

**`utils sqlite-to-excel`**: takes a `DB_PATH` argument and an optional
`--output PATH` for the destination Excel file (defaults to the same name
as the database with a `.xlsx` extension).

## Examples

### License Management

```bash
# Get licenses for all clusters (cache-backed, fast)
nf licenses get

# Get licenses for a filtered set of clusters
nf licenses get -f '{"bu":"Business","env":"Prod"}'

# Write licenses to a CSV file
nf licenses get --csv --output licenses.csv

# Bypass the cache and fetch licenses live from each cluster (slow)
nf licenses get --live

# Check clusters for license issues and send email notifications
nf licenses check

# Run the license check without sending email
nf licenses check --no-send-email

# Calculate potential license savings across a filtered fleet
nf licenses savings -f '{"env":"Prod"}'
```

### Report Generation

```bash
# Generate the HTML tree report for all clusters
nf reports html

# Generate the HTML tree report for a filtered subset
nf reports html -f '{"bu":"Business","env":"Prod"}'

# Generate the client locks Excel workbook
nf reports locks

# Generate the space-usage Excel workbook
nf reports space-usage -f '{"env":"Prod"}'
```

### Event Monitoring

```bash
# Get the most recent 50 events across all clusters (default)
nf events get

# Get only error-severity events
nf events get -s error

# Filter by one or more event names
nf events get -n vsa.mlx.nic.detach -n vsa.mlx.nic.attach

# Sort descending by time and limit to 200 events
nf events get --sort -time -l 200

# Write events to CSV instead of the console
nf events get --output events.csv

# Record Azure maintenance events to the database
nf events save-azure -f '{"env":"Prod"}'
```

### Metrics Collection

```bash
# Dump DII metrics for a 3-day window centered on 2025-04-13 for all clusters
nf metrics dump-dii --date 2025-04-13

# Dump the same 3-day window for a filtered set of clusters
nf metrics dump-dii --date 2025-04-13 -f '{"env":"Prod"}'
```

### CIFS Inspection

```bash
# List all active CIFS sessions across the cached clusters
nf cifs session

# Find sessions for a specific user (substring, case-insensitive)
nf cifs session -u jdoe

# Glob match against fully-qualified domain user
nf cifs session -u 'DOMAIN\jdoe'

# Find every session originating from a CIDR range, scoped to Prod
nf cifs session -i 10.1.2.0/24 -f '{"env":"Prod"}'

# Combine user + IP filters
nf cifs session -u '*jdoe*' -i 10.1.2.0/24

# Render the table and additionally export to CSV
nf cifs session -u jdoe --csv ./jdoe-sessions.csv
```

### Configuration

```bash
# Display the full loaded configuration (secrets masked)
nf config show

# Show only the clusters section
nf config show -s clusters

# Reveal passwords and tokens (use with caution)
nf config show --unmask

# Show one scope's own files, or only its users section
nf config show --scope Org1
nf config show --scope Org1 -s users

# Validate all configuration files
nf config validate

# Validate one scope (clusters, users, monitoring and Console account)
nf config validate --scope Org1

# Initialize SOPS + age encryption for credential storage
nf config init-sops

# Initialize SOPS with a custom key path, overwriting any existing key
nf config init-sops --key-path ~/.my-keys/age.txt --force

# Set encrypted credentials for a specific cluster
nf config set-credential --cluster mycluster --user admin

# Set default credentials for all clusters
nf config set-credential --type clusters --user admin

# Set credentials for one AIQUM, or store one Cloud Insights tenant's API token
nf config set-credential --type aiqums --name aiqum1 --user admin
nf config set-credential --type cloudinsights --name tenant1 --user token

# Store the Console refresh token (the user is a label; the prompt takes the token)
nf config set-credential --type console --user console

# Write a scope's own defaults (its own users.toml) and its Console refresh token
nf config set-credential --type clusters --scope Org1 --user admin
nf config set-credential --type console --scope Org1 --user console

# Store a password without encryption (not recommended)
nf config set-credential --cluster mycluster --user admin --no-encrypt

# Store a settings secret, encrypted, in the right file (no pasting)
nf config set-credential --setting consoleapi.client_secret
nf config set-credential --setting consoleapi.client_secret --scope Org1
nf config set-credential --setting diiapi.api_ro_token
nf config set-credential --setting settings.smtp_password
```

### Utilities

```bash
# Validate connectivity and configuration for all clusters
nf utils validate

# Also validate SSH connectivity (required for `utils run-cmd`)
nf utils validate --ssh

# Run an ONTAP CLI command across matching clusters
nf utils run-cmd "vol show" -f '{"env":"Prod"}'

# Convert a SQLite database produced by `metrics dump-dii` to Excel
nf utils sqlite-to-excel cluster1_2025-04-13_metrics.db

# Convert with a custom output path
nf utils sqlite-to-excel cluster1_2025-04-13_metrics.db --output metrics-report.xlsx
```

### Cache Management

```bash
# Refresh cache for a single cluster
nf cache refresh cluster1

# Refresh cache for all configured clusters
nf cache refresh --all

# Refresh with verbose progress output
nf cache refresh --all -v

# List all cached clusters
nf cache show

# Show all cached data for a cluster
nf cache show cluster1

# Show only a specific section
nf cache show cluster1 -s nodes

# Output cached data as JSON
nf cache show cluster1 --json

# Query specific fields using dot notation
nf cache query cluster1 cloud.instance_type

# Query multiple fields
nf cache query cluster1 cloud.provider cluster.version.full

# Query all cached clusters
nf cache query --all cloud.instance_type

# Query with cluster filter
nf cache query -f '{"env":"Prod"}' cloud.provider cloud.region

# Query with JSON output (for scripting)
nf cache query cluster1 cloud.instance_type --json

# Query with raw output (values only, single cluster)
nf cache query cluster1 cluster.version.full --raw

# Query array elements
nf cache query cluster1 nodes[0].name

# Query all array items with wildcard [*] -- each result is labelled with
# an identifier for the item it came from (name, svm.name, uuid, or the
# array index as a fallback, in that order)
nf cache query cluster1 nodes[*].name
# test-cluster:
#   nodes[*].name:
#     node-01: node-01
#     node-02: node-02

# Choose the identifier field explicitly (overrides the default order
# for every wildcard/filter field in the query)
nf cache query cluster1 protocols.cifs_services[*].security.session_security --key svm.name

# Wildcard with raw output (one "key<TAB>value" line per item, for scripting)
nf cache query cluster1 nodes[*].name --raw

# Wildcard with JSON output: a list of {"key", "value"} records per field
# (not a flat array -- see ADR-0020; this is a breaking change from
# versions that returned a flat list for wildcard/filter fields)
nf cache query cluster1 nodes[*].name --json
# {"cluster1": {"nodes[*].name": [{"key": "node-01", "value": "node-01"}, ...]}}

# CSV output (no identifier column for plain, non-wildcard fields)
nf cache query --all cloud.provider cloud.region --csv

# CSV with wildcards: a "key" column is added after "cluster", sourced
# from the first wildcard/filter field when there are several
nf cache query cluster1 nodes[*].name nodes[*].serial_number --csv

# Filter predicate (select items by field value) -- matches are labelled
# with an identifier the same way wildcard results are
nf cache query cluster1 'volumes["name=vol1"].size'

# OR filter (match multiple values)
nf cache query cluster1 'volumes["name=vol1 || name=vol2"].size'

# Glob pattern (match by substring or pattern, * and ? supported)
nf cache query cluster1 'volumes["name=*PROD*"].size'

# Single-quoted predicate (alternative syntax)
nf cache query cluster1 "volumes['state=online'].name"

# Dotted field in a filter predicate -- the field left of "=" is resolved
# as a dotted path inside each item; a missing intermediate key is no match
nf cache query cluster1 'volumes["svm.name=svm1"].name'
nf cache query --all 'protocols.cifs_services["security.session_security=none"].svm.name'

# SVM web services (vserver services web), collected through the private CLI
# passthrough -- which SVMs have sysmgr or saml enabled? --key service_key
# labels each result vserver/name (e.g. svm1/sysmgr)
nf cache query --all 'storage.svm_web_services["name=sysmgr || name=saml"].enabled' --key service_key

# Nested wildcards compose identifiers with '/' (e.g. svm1/vol1)
nf cache query cluster1 'storage.svms[*].volumes[*].size' --json

# View cache schema as tree
nf cache schema

# View schema as flat list of queryable paths
nf cache schema --flat

# Output JSON schema
nf cache schema --json

# Check cache status
nf cache status

# Check with custom staleness threshold
nf cache status --ttl 7

# Clear cache for a cluster
nf cache clear cluster1

# Clear all cached data
nf cache clear --all

# Clear without confirmation
nf cache clear --all -f

# Check: find volumes where autosize mode is not grow_shrink
nf cache check cluster1 storage.volumes \
    -w "autosize.mode != 'grow_shrink'" \
    -F name,svm.name,autosize.mode

# Check all clusters for a model filter
nf cache check --all storage.volumes \
    -w "autosize.mode != 'grow_shrink'"

# Check with cluster filter and data filter
nf cache check -f '{"env":"Prod"}' storage.volumes \
    -w "autosize.mode != 'grow_shrink'" \
    -F name,svm.name,autosize.mode

# Count matching records only
nf cache check --all storage.volumes \
    -w "size > 1073741824" --count

# JSON output for scripting
nf cache check --all nodes -w "model_ = 'FAS8200'" --json

# CSV output
nf cache check --all storage.volumes \
    -w "state = 'online'" --csv

# Query cloud console links
nf cache query cluster1 cloud[0].instance_link

# Query AWS SSO link (requires aws.toml config)
nf cache query cluster1 cloud[0].instance_sso_link

# Query Azure resource group link
nf cache query cluster1 cloud[0].resource_group_link
```

### Compliance Checks

```bash
# Run all compliance checks for a single cluster
nf cache compliance cluster1

# Run compliance checks for all cached clusters
nf cache compliance --all

# Filter clusters and run a specific check
nf cache compliance -f '{"env":"Prod"}' -k vol_autosize

# Only show errors (filter by minimum severity)
nf cache compliance --all -s error

# JSON output for scripting
nf cache compliance --all --json

# CSV output
nf cache compliance --all --csv
```

See also: [Compliance Checks user guide](../usage/compliance-checks.md) for the full TOML format, per-cluster overrides, and worked examples.

### Cloud Resource Links

The cache includes computed URL fields for quick access to cloud provider consoles:

| Field | Description |
|-------|-------------|
| `cloud[*].instance_link` | Direct URL to the instance in AWS EC2 or Azure portal |
| `cloud[*].instance_sso_link` | AWS SSO shortcut URL with account context (AWS only) |
| `cloud[*].resource_group_link` | URL to the Azure resource group (Azure only) |

#### AWS SSO Configuration

To enable SSO shortcut links that include account context, create `config/aws.toml`:

```toml
[sso]
subdomain = "mycompany"  # -> mycompany.awsapps.com

[sso.account_roles]
"123456789012" = "ProdAdminAccess"
"234567890123" = "DevReadOnly"
```

The `account_roles` mapping associates AWS account IDs with SSO role names. Account IDs are discovered automatically during cache refresh.

### Cache Schema Changes

When the cache schema is updated (e.g., new fields added):

- **Existing cache data remains valid** - Pydantic fills in default values for new fields
- **No clear required** - Old entries continue to work
- **Refresh required for new data** - Run `nf cache refresh <cluster>` to populate new fields

New fields will have empty/default values until the cluster is refreshed.

## Environment Variables

| Variable | Description |
|----------|-------------|
| `NF_CONFIG_DIR` | Default configuration directory |
| `NF_OUTPUT_DIR` | Default output directory |
| `NF_DEBUG` | Enable debug mode (1/true) |

## Exit Codes

| Code | Description |
|------|-------------|
| 0 | Success |
| 1 | Error, including unexpected errors caught by the top-level handler, `ClickException` and aborted prompts. For `nf cache check` and `nf cache compliance`: matches or violations found |
| 2 | Usage error (bad option or argument). For `nf cache check` and `nf cache compliance`: an error occurred |

Commands report an error by raising `CliError`, which prints the red message
and exits with the code above (1 by default, 2 for the grep-style commands).
See [ADR-0022](../decisions/0022-one-cli-error-exit-convention-raise-clierror.md).

## Error Handling

`nf` wraps every command in a top-level handler. An exception a command does not
handle prints `Unexpected error: <message>`, is logged with its traceback to the
log file, and exits with code 1. Re-run with `--debug` to print the full
traceback to the console. Click's own errors (usage errors, `Abort`) keep their
normal messages and exit codes.
