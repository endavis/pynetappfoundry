---
title: Examples
description: Code examples for pynetappfoundry
audience:
  - users
tags:
  - examples
  - tutorial
---

# Examples

This section contains example code demonstrating common use cases for pynetappfoundry.

## Quick Start

### Initialize Configuration

```python
from pynetappfoundry import Config

# Load configuration from default location (~/.config/pynetappfoundry)
config = Config()

# Or specify a custom config directory
config = Config(config_dir="/path/to/config")
```

### Search for Clusters

```python
from pynetappfoundry import Config

config = Config()

# Search by environment
prod_clusters = config.search("clusters", {"env": "Prod"})
for name, details in prod_clusters.items():
    print(f"{name}: {details['ip']}")

# Search by multiple criteria
filtered = config.search("clusters", {"bu": "Engineering", "env": "Dev"})

# Search with OR conditions
clusters = config.search("clusters", {"env": "Prod || Dev"})

# Search with AND conditions on tags
clusters = config.search("clusters", {"tags": "active && critical"})
```

### Create an ONTAP API Client

```python
from pynetappfoundry import Config, ONTAPAPIClient

config = Config()

# Get a cluster from search results
clusters = config.search("clusters", {"name": "my-cluster"})
cluster = list(clusters.values())[0]

# Create the API client
# Note: cluster must have 'name' and 'ip' attributes
from types import SimpleNamespace
cluster_obj = SimpleNamespace(**cluster)

client = ONTAPAPIClient(cluster_obj, config)
```

### Call ONTAP REST API Endpoints

```python
# List available endpoints
endpoints = client.list_endpoints()
for path, method, summary in endpoints[:5]:
    print(f"{method} {path}: {summary}")

# Get parameter hints for an endpoint
params = client.suggest_parameters("/storage/volumes", "GET")
print(f"Query params: {params['query_params']}")

# Call an endpoint
volumes = client.call_endpoint(
    "/storage/volumes",
    "GET",
    query_params={"fields": "name,size,space.used"},
)
for vol in volumes.get("records", []):
    print(f"Volume: {vol['name']}, Size: {vol.get('size', 'N/A')}")
```

### Run CLI Commands via SSH

```python
from pynetappfoundry import Config, ONTAPCLI

config = Config()
clusters = config.search("clusters", {"name": "my-cluster"})
cluster = list(clusters.values())[0]

# Create CLI client
cli = ONTAPCLI(
    name=cluster["name"],
    host_or_ip=cluster["ip"],
    username="admin",
    password="password",
)

# Run a command
output = cli.run_command("volume show -fields size,used")
for line in output:
    print(line)

# Don't forget to disconnect
cli.disconnect()
```

## CLI Examples

### Utility Commands

```bash
# Run CLI command on clusters matching filter
nf utils run-cmd "vol show" --filter '{"bu":"Engineering"}'

# Validate configuration
nf config validate

# Show loaded configuration
nf config show
```

### Report Generation

```bash
# Generate reports (if implemented)
nf reports --help
```

## More Examples

- [API Examples](api.md) - Detailed API usage examples including retry and validation
