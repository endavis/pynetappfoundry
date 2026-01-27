---
title: Basic Usage
description: Getting started with pynetappfoundry
audience:
  - users
tags:
  - usage
  - tutorial
---

# Basic Usage

This guide covers the basic usage patterns for pynetappfoundry.

## Configuration

pynetappfoundry uses a configuration directory to store cluster credentials and settings.

### Default Locations

- **Linux/macOS:** `~/.config/pynetappfoundry/`
- **Windows:** `%APPDATA%\pynetappfoundry\`

### Configuration Files

```
~/.config/pynetappfoundry/
├── config.json          # Main configuration
├── clusters/            # Cluster-specific configs
│   ├── cluster1.json
│   └── cluster2.json
└── output/              # Default output directory
```

## Command Line Interface

The `nf` command provides access to all CLI functionality.

### Global Options

```bash
nf --help                    # Show help
nf --version                 # Show version
nf --config-dir PATH         # Custom config directory
nf --output-dir PATH         # Custom output directory
nf --debug                   # Enable debug logging
```

### Available Commands

```bash
nf licenses                  # License management
nf reports                   # Report generation
nf events                    # Event management
nf metrics                   # Metrics collection
nf utils                     # Utility commands
```

## Python API

### Basic Client Usage

```python
from pynetappfoundry import Config, ONTAPAPIClient

# Load configuration
config = Config()

# Create API client for a cluster
client = ONTAPAPIClient(config, "cluster1")

# Use the client
volumes = client.get_volumes()
```

### CLI Client for SSH Access

```python
from pynetappfoundry import Config, ONTAPCLI

# Load configuration
config = Config()

# Create CLI client
cli = ONTAPCLI(config, "cluster1")

# Run CLI commands
output = cli.run_command("volume show")
```

### Event Database

```python
from pynetappfoundry import EmsEventsDB

# Initialize events database
db = EmsEventsDB("events.db")

# Query events
events = db.get_events(cluster="cluster1", severity="error")
```

### Metrics Collection

```python
from pynetappfoundry import MetricDB

# Initialize metrics database
db = MetricDB("metrics.db")

# Store and query metrics
db.store_metric("cluster1", "volume_used", 1024)
metrics = db.get_metrics("cluster1")
```

## Common Workflows

### License Reporting

```bash
# List licenses for all clusters
nf licenses list

# Export licenses to Excel
nf licenses export --format xlsx --output licenses.xlsx
```

### Space Reporting

```bash
# Generate space report
nf reports space --cluster cluster1

# Generate aggregate report
nf reports aggregate --all-clusters
```

### Event Monitoring

```bash
# Fetch recent events
nf events fetch --hours 24

# List events by severity
nf events list --severity error
```

## Next Steps

- [CLI Reference](../reference/cli.md) - Complete CLI documentation
- [API Reference](../reference/api.md) - Python API documentation
- [Examples](../examples/README.md) - More usage examples
