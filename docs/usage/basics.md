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

pynetappfoundry uses TOML files for configuration. By default, it looks for a `config/` directory relative to your current working directory.

### Configuration Structure

```
config/
├── settings.toml        # Global settings and searchable keys
├── users.toml           # Credentials for clusters and services
├── environments/        # Data files for clusters, connectors, etc.
│   ├── prod.toml
│   └── dev.toml
└── apis/                # API specifications
    ├── ontap/
    │   └── all.json     # ONTAP OpenAPI spec
    └── dii/
        └── all.json     # Data Infrastructure Insights spec
```

### Settings File (settings.toml)

Defines searchable keys and global settings:

```toml
[clusters]
searchable_keys = ["div", "bu", "cloud", "app", "env", "subapp", "region"]

[SMTP]
server = "smtp.example.com"
port = 25

[licensing]
mailfrom = "netapp-licensing@example.com"
mailto = "netapp-team@example.com"
```

### Users File (users.toml)

Stores credentials for different resource types:

```toml
[clusters]
user = "admin"
enc = "encoded_password"
```

### Data Files

Data files define clusters, connectors, and other resources. They must include `[settings] type = "data"`:

```toml
[settings]
type = "data"

[clusters.CLUSTER-PROD-01]
ip = "192.168.1.173"
div = "ITS"
bu = "LAR"
app = "Storage"
env = "Prod"
tags = ["active", "nfs"]
region = "USCU"

[clusters.CLUSTER-DEV-01]
ip = "192.168.2.173"
div = "ITS"
bu = "LAR"
app = "Storage"
env = "Dev"
tags = ["active"]
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

### Loading Configuration

```python
from pynetappfoundry import Config

# Load from default config/ directory
config = Config()

# Load from custom directory
config = Config(config_dir="/path/to/config")

# With output directory
config = Config(
    config_dir="config",
    output_dir="output",
    script_name="my_script"
)
```

### Searching for Clusters

The Config class supports flexible searching:

```python
# Get all clusters
all_clusters = config.search("clusters", {})

# Search by environment
prod_clusters = config.search("clusters", {"env": "Prod"})

# Search with multiple criteria
specific = config.search("clusters", {
    "bu": "Engineering",
    "env": "Prod"
})

# Use OR operator
dev_or_test = config.search("clusters", {
    "env": "Dev || Test"
})

# Use AND operator for list fields
active_nfs = config.search("clusters", {
    "tags": "active && nfs"
})
```

### Using the ONTAP API Client

```python
from pynetappfoundry import Config, ONTAPAPIClient

config = Config()

# Get cluster info from config
clusters = config.search("clusters", {"name": "CLUSTER-PROD-01"})
cluster = list(clusters.values())[0]

# Create API client (requires cluster object with 'name' and 'ip')
class ClusterInfo:
    def __init__(self, data):
        self.name = data["name"]
        self.ip = data["ip"]

client = ONTAPAPIClient(ClusterInfo(cluster), config)

# Call API endpoints
result = client.call_endpoint("/storage/volumes", "GET")
```

### CLI Client for SSH Access

```python
from pynetappfoundry import Config, ONTAPCLI

config = Config()

# Create CLI client
cli = ONTAPCLI(config, "CLUSTER-PROD-01")

# Run CLI commands
output = cli.run_command("volume show")
```

### Metrics Database

```python
from pynetappfoundry import Config, MetricDB

config = Config(script_name="metrics_collector")

# Initialize metrics database
db = MetricDB(config)

# Create table and store metrics
db.create_table("cluster_metrics")
db.upsert_data("cluster_metrics", {
    "timestamp": "2024-03-15T10:00:00",
    "read_ops": 100.0,
    "write_ops": 50.0,
    "read_latency": 1.5,
    "write_latency": 2.0,
    "read_throughput": 1000.0,
    "write_throughput": 500.0,
})
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
nf reports space --cluster CLUSTER-PROD-01

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

## Error Handling

The library uses `ConfigurationError` for configuration-related errors:

```python
from pynetappfoundry import Config, ConfigurationError

config = Config()

try:
    user, password = config.get_user("clusters", "unknown-cluster")
except ConfigurationError as e:
    print(f"Configuration error: {e}")
```

## Next Steps

- [CLI Reference](../reference/cli.md) - Complete CLI documentation
- [API Reference](../reference/api.md) - Python API documentation
- [Examples](../examples/README.md) - More usage examples
