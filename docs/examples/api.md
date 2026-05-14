---
title: API Examples
description: Detailed Python API usage examples
audience:
  - users
tags:
  - examples
  - api
---

# API Examples

Detailed examples for using the pynetappfoundry Python API.

## Configuration

### Basic Configuration

```python
from pynetappfoundry import Config

# Load from default location
config = Config()

# Load from custom directory
config = Config(
    config_dir="/path/to/config",
    output_dir="/path/to/output",
    script_name="my_script",
)
```

### Searching Data

```python
from pynetappfoundry import Config

config = Config()

# Simple search
clusters = config.search("clusters", {"env": "Prod"})

# Multiple conditions (AND)
clusters = config.search("clusters", {"bu": "Engineering", "env": "Prod"})

# OR conditions
clusters = config.search("clusters", {"env": "Prod || Dev"})

# AND conditions on list fields (tags)
clusters = config.search("clusters", {"tags": "active && critical"})

# Get all clusters
all_clusters = config.get_clusters({})

# Find closest match (relaxes criteria progressively)
closest = config.find_closest("clusters", {
    "bu": "Engineering",
    "env": "Prod",
    "region": "us-east-1",
})
```

### Getting Settings

```python
# Get ONTAP API settings
ontap_settings = config.get_ontap_api_settings()
print(f"Base path: {ontap_settings.base_api_path}")
print(f"Timeout: {ontap_settings.timeout}")

# Get DII API settings
dii_settings = config.get_dii_api_settings()
print(f"Base URL: {dii_settings.base_url}")

# Get arbitrary settings
value = config.get_setting("SMTP", "server")
```

## ONTAP API Client

### Creating a Client

```python
from types import SimpleNamespace
from pynetappfoundry import Config, ONTAPAPIClient

config = Config()

# Get cluster details from config
clusters = config.search("clusters", {"name": "my-cluster"})
cluster_data = list(clusters.values())[0]

# Create cluster object (needs name and ip attributes)
cluster = SimpleNamespace(**cluster_data)

# Create the client
client = ONTAPAPIClient(cluster, config)
```

### Discovering Endpoints

```python
# List all available endpoints
endpoints = client.list_endpoints()
for path, method, summary in endpoints:
    print(f"{method:6} {path}")
    if summary:
        print(f"       {summary}")

# Get detailed parameter info for an endpoint
params = client.suggest_parameters("/storage/volumes", "GET")
print(f"Path: {params['path']}")
print(f"Method: {params['method']}")
print(f"Summary: {params['summary']}")
print(f"Path params: {params['path_params']}")
print(f"Query params: {params['query_params']}")
```

### Calling Endpoints

```python
# GET request with query parameters
volumes = client.call_endpoint(
    "/storage/volumes",
    "GET",
    query_params={
        "fields": "name,size,space.used,space.available",
        "max_records": 100,
    },
)

for vol in volumes.get("records", []):
    name = vol["name"]
    size = vol.get("size", 0)
    used = vol.get("space", {}).get("used", 0)
    print(f"{name}: {used / size * 100:.1f}% used")

# GET with path parameters
volume = client.call_endpoint(
    "/storage/volumes/{uuid}",
    "GET",
    path_params={"uuid": "abc123-def456"},
)

# POST request with body
result = client.call_endpoint(
    "/storage/volumes",
    "POST",
    body={
        "name": "new_volume",
        "svm": {"name": "svm1"},
        "size": 107374182400,  # 100GB
    },
)

# PATCH request
result = client.call_endpoint(
    "/storage/volumes/{uuid}",
    "PATCH",
    path_params={"uuid": "abc123-def456"},
    body={"size": 214748364800},  # 200GB
)

# DELETE request
client.call_endpoint(
    "/storage/volumes/{uuid}",
    "DELETE",
    path_params={"uuid": "abc123-def456"},
)
```

### Retry Configuration

```python
from pynetappfoundry.core.models import RetryConfig

# Custom retry configuration
retry_config = RetryConfig(
    enabled=True,
    max_attempts=5,
    initial_wait=1.0,
    max_wait=60.0,
    exponential_base=2,
    retryable_status_codes=[429, 500, 502, 503, 504],
    retry_on_connection_error=True,
)

# Apply at client creation
client = ONTAPAPIClient(
    cluster, config,
    retry_config=retry_config,
)

# Or override per-call
result = client.call_endpoint(
    "/storage/volumes",
    "GET",
    retry_config=RetryConfig(max_attempts=10),
)
```

### Response Validation

```python
from pynetappfoundry.core.models import ValidationConfig

# Enable response validation
validation_config = ValidationConfig(
    enabled=True,
    strict=False,  # Log warnings instead of raising exceptions
    validate_success_only=True,  # Only validate 2xx responses
)

client = ONTAPAPIClient(
    cluster, config,
    validation_config=validation_config,
)

# Strict validation (raises ResponseValidationError on mismatch)
strict_config = ValidationConfig(enabled=True, strict=True)
result = client.call_endpoint(
    "/cluster",
    "GET",
    validation_config=strict_config,
)
```

## ONTAP CLI (SSH)

### Basic Usage

```python
from pynetappfoundry import ONTAPCLI

# Create CLI connection
cli = ONTAPCLI(
    name="my-cluster",
    host_or_ip="192.168.1.100",
    username="admin",
    password="password",
)

try:
    # Run a command
    output = cli.run_command("volume show")
    for line in output:
        print(line)

    # Run and parse output
    data = cli.run_command_and_parse("volume show")
    for vol_name, vol_data in data.items():
        print(f"{vol_name}: {vol_data}")

    # Parse show commands with separators
    records, descriptions = cli.run_a_show_command_and_parse_seperator(
        "volume show"
    )
    for record in records:
        print(record)

finally:
    cli.disconnect()
```

### Using with Config Credentials

```python
from pynetappfoundry import Config, ONTAPCLI

config = Config()

# Get cluster info
clusters = config.search("clusters", {"name": "my-cluster"})
cluster = list(clusters.values())[0]

# Get credentials from config
username, password = config.get_user("clusters", cluster["name"])

cli = ONTAPCLI(
    name=cluster["name"],
    host_or_ip=cluster["ip"],
    username=username,
    password=password,
)
```

## DII API Client

### Basic Usage

```python
from pynetappfoundry import Config, DIIAPIClient

config = Config()

# Create DII client (uses settings from diiapi.toml)
client = DIIAPIClient(config)

# List endpoints
endpoints = client.list_endpoints()

# Call an endpoint
result = client.call_endpoint(
    "/assets/storages",
    "GET",
    query_params={"limit": 100},
)
```

## Error Handling

### Connection Errors

```python
import requests
from pynetappfoundry import Config, ONTAPAPIClient
from pynetappfoundry.clients.openapi import ResponseValidationError

config = Config()
cluster = ...  # Get cluster object

try:
    client = ONTAPAPIClient(cluster, config)
    result = client.call_endpoint("/cluster", "GET")
except requests.ConnectionError as e:
    print(f"Connection failed: {e}")
except requests.HTTPError as e:
    print(f"HTTP error: {e}")
except ResponseValidationError as e:
    print(f"Response validation failed: {e}")
    print(f"Path: {e.path_template}, Status: {e.status_code}")
```

### CLI Errors

```python
from pynetappfoundry import ONTAPCLI
from pynetappfoundry.clients.ontap.cli import CLICommandError

cli = ONTAPCLI(...)

try:
    output = cli.run_command("invalid command")
except CLICommandError as e:
    print(f"CLI error: {e.message}")
finally:
    cli.disconnect()
```

## Complete Script Example

```python
#!/usr/bin/env python3
"""Example script: List volumes over 80% used."""

from types import SimpleNamespace
from pynetappfoundry import Config, ONTAPAPIClient

def main():
    config = Config()

    # Get all production clusters
    clusters = config.search("clusters", {"env": "Prod"})

    for name, data in clusters.items():
        print(f"\n=== {name} ===")

        # Create client
        cluster = SimpleNamespace(**data)
        client = ONTAPAPIClient(cluster, config)

        # Get volumes
        try:
            result = client.call_endpoint(
                "/storage/volumes",
                "GET",
                query_params={"fields": "name,space.used,space.size"},
            )
        except Exception as e:
            print(f"  Error: {e}")
            continue

        # Check each volume
        for vol in result.get("records", []):
            space = vol.get("space", {})
            used = space.get("used", 0)
            size = space.get("size", 1)
            pct = (used / size) * 100

            if pct > 80:
                print(f"  WARNING: {vol['name']} is {pct:.1f}% used")

if __name__ == "__main__":
    main()
```
