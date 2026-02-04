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

## Commands

### licenses

License management commands.

```bash
nf licenses [OPTIONS] COMMAND [ARGS]...
```

**Subcommands:**

| Command | Description |
|---------|-------------|
| `list` | List licenses for clusters |
| `export` | Export licenses to file |
| `check` | Check license compliance |

### reports

Report generation commands.

```bash
nf reports [OPTIONS] COMMAND [ARGS]...
```

**Subcommands:**

| Command | Description |
|---------|-------------|
| `space` | Generate space utilization report |
| `aggregate` | Generate aggregate report |
| `volume` | Generate volume report |
| `performance` | Generate performance report |

### events

Event management commands.

```bash
nf events [OPTIONS] COMMAND [ARGS]...
```

**Subcommands:**

| Command | Description |
|---------|-------------|
| `fetch` | Fetch events from clusters |
| `list` | List stored events |
| `export` | Export events to file |
| `clear` | Clear event database |

### metrics

Metrics collection commands.

```bash
nf metrics [OPTIONS] COMMAND [ARGS]...
```

**Subcommands:**

| Command | Description |
|---------|-------------|
| `collect` | Collect metrics from clusters |
| `query` | Query stored metrics |
| `export` | Export metrics to file |

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
| `schema` | Display the cache metadata schema |
| `status` | Show cache status for all clusters |
| `clear` | Clear the metadata cache |

### utils

Utility commands.

```bash
nf utils [OPTIONS] COMMAND [ARGS]...
```

**Subcommands:**

| Command | Description |
|---------|-------------|
| `config` | Configuration management |
| `test-connection` | Test cluster connectivity |
| `version` | Show detailed version info |

## Examples

### License Management

```bash
# List all licenses
nf licenses list

# List licenses for specific cluster
nf licenses list --cluster cluster1

# Export to Excel
nf licenses export --format xlsx -o licenses.xlsx

# Check compliance
nf licenses check --cluster cluster1
```

### Report Generation

```bash
# Space report for all clusters
nf reports space --all-clusters

# Volume report with filtering
nf reports volume --cluster cluster1 --svm svm1

# Export report to HTML
nf reports space --format html -o space-report.html
```

### Event Monitoring

```bash
# Fetch last 24 hours of events
nf events fetch --hours 24

# Fetch events for specific cluster
nf events fetch --cluster cluster1 --hours 48

# List error events
nf events list --severity error

# Export to CSV
nf events export --format csv -o events.csv
```

### Metrics Collection

```bash
# Collect all metrics
nf metrics collect --all-clusters

# Query specific metric
nf metrics query --metric volume_used --cluster cluster1

# Export metrics
nf metrics export --format json -o metrics.json
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
```

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
