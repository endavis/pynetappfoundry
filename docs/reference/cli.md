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
