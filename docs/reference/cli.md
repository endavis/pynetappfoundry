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
| `--debug / --no-debug` | Enable debug logging |
| `--help` | Show help and exit |

### Cluster Filter Convention

Most commands accept `-f, --filter` to narrow the set of clusters they act on.
The filter is a JSON object matched against cluster metadata fields such as
`bu` (business unit) and `env` (environment):

```bash
-f '{"bu":"Business","env":"Prod"}'
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
| `-o, --output PATH` | CSV output file path (default: timestamped file in output dir) |
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
| `locks` | Generate client lock reports (Excel) |
| `space-usage` | Generate space usage reports (Excel) |

All `reports` subcommands accept `-f, --filter` to scope the report to a
subset of clusters.

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
| `-o, --output PATH` | Output to CSV file instead of console |
| `--sort [time|-time]` | Sort order (default: `time` ascending; `-time` for descending) |
| `-l, --limit INTEGER` | Maximum number of events to retrieve (default: 50) |

`nf events get` shows `Time`, `Node`, `Severity`, `Name`, and `Message` in the console table. CSV output includes `cluster`, `node`, `time`, `name`, `severity`, and `message` columns.

**`events save-azure` options:**

| Option | Description |
|--------|-------------|
| `-f, --filter TEXT` | JSON cluster filter |

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
| `-d, --date TEXT` | Required date in `YYYY-MM-DD` format; queries `(date - 1 day)` through `(date + 2 days)` in UTC |

`metrics dump-dii` writes one SQLite database per cluster per date (`{cluster}_{date}_metrics.db`) and stores each SVM/volume pair in its own table (`{vserver_name}-{volume_name}`).

### cache

Cluster metadata cache management. The cache stores discoverable ONTAP cluster information that doesn't change frequently.

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
| `set-credential` | Set encrypted credentials for a cluster or resource type |

**`config show` options:**

| Option | Description |
|--------|-------------|
| `-s, --section TEXT` | Show only a specific section (e.g. `clusters`, `settings`, `users`) |
| `--unmask` | Show passwords and tokens unmasked (use with caution) |

**`config validate` options:**

No options beyond `--help`. Checks that all configuration files parse and
contain valid values.

**`config init-sops` options:**

| Option | Description |
|--------|-------------|
| `--key-path PATH` | Path to store the age private key (default: `~/.sops/age/keys.txt`) |
| `--force` | Overwrite existing key file |

**`config set-credential` options:**

| Option | Description |
|--------|-------------|
| `--cluster TEXT` | Set credentials for a specific cluster (per-cluster override) |
| `--type` | Set default credentials for all resources of a type: `aiqums`, `azure`, `cloudinsights`, `clusters`, `connectors`, `ibm` |
| `--user TEXT` | Username (required) |
| `--password TEXT` | Password (will prompt if not provided) |
| `--no-encrypt` | Store password as plain text (not recommended) |

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

**`utils run-cmd`**: takes a single quoted ONTAP CLI command as its argument,
and accepts `-f, --filter` to select clusters.

**`utils sqlite-to-excel`**: takes a `DB_PATH` argument and an optional
`-o, --output PATH` for the destination Excel file (defaults to the same name
as the database with a `.xlsx` extension).

## Examples

### License Management

```bash
# Get licenses for all clusters (cache-backed, fast)
nf licenses get

# Get licenses for a filtered set of clusters
nf licenses get -f '{"bu":"Business","env":"Prod"}'

# Write licenses to a CSV file
nf licenses get --csv -o licenses.csv

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
nf events get -o events.csv

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

### Configuration

```bash
# Display the full loaded configuration (secrets masked)
nf config show

# Show only the clusters section
nf config show -s clusters

# Reveal passwords and tokens (use with caution)
nf config show --unmask

# Validate all configuration files
nf config validate

# Initialize SOPS + age encryption for credential storage
nf config init-sops

# Initialize SOPS with a custom key path, overwriting any existing key
nf config init-sops --key-path ~/.my-keys/age.txt --force

# Set encrypted credentials for a specific cluster
nf config set-credential --cluster mycluster --user admin

# Set default credentials for all clusters
nf config set-credential --type clusters --user admin

# Store a password without encryption (not recommended)
nf config set-credential --cluster mycluster --user admin --no-encrypt
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
nf utils sqlite-to-excel cluster1_2025-04-13_metrics.db -o metrics-report.xlsx
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
nf cache query cluster1 cloud.provider cluster.ontap_version

# Query all cached clusters
nf cache query --all cloud.instance_type

# Query with cluster filter
nf cache query -f '{"env":"Prod"}' cloud.provider cloud.region

# Query with JSON output (for scripting)
nf cache query cluster1 cloud.instance_type --json

# Query with raw output (values only, single cluster)
nf cache query cluster1 cluster.ontap_version --raw

# Query array elements
nf cache query cluster1 nodes[0].name

# Query all array items with wildcard [*]
nf cache query cluster1 nodes[*].name

# Wildcard with raw output (one value per line, for scripting)
nf cache query cluster1 nodes[*].name --raw

# CSV output
nf cache query --all cloud.provider cloud.region --csv

# CSV with wildcards (expands to multiple rows)
nf cache query cluster1 nodes[*].name nodes[*].serial_number --csv

# Filter predicate (select items by field value)
nf cache query cluster1 'volumes["name=vol1"].size'

# OR filter (match multiple values)
nf cache query cluster1 'volumes["name=vol1 || name=vol2"].size'

# Glob pattern (match by substring or pattern, * and ? supported)
nf cache query cluster1 'volumes["name=*PROD*"].size'

# Single-quoted predicate (alternative syntax)
nf cache query cluster1 "volumes['state=online'].name"

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
| 1 | General error |
| 2 | Configuration error |
| 3 | Connection error |
| 4 | Authentication error |
