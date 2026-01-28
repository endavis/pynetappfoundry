---
title: ONTAP Access Patterns
description: Guide to choosing between the three ONTAP access methods
audience:
  - users
  - contributors
tags:
  - ontap
  - api
  - ssh
  - sdk
---

# ONTAP Access Patterns

pynetappfoundry provides three different ways to interact with ONTAP clusters. Each pattern has specific use cases, advantages, and trade-offs. This guide helps you choose the right approach for your task.

## Overview

| Pattern | Connection | Best For |
|---------|------------|----------|
| `netapp_ontap` SDK | HTTPS REST | Structured data retrieval, reports, typed objects |
| `ONTAPCLI` | SSH | Ad-hoc CLI commands, operations not in REST API |
| `APIWrapper` | HTTPS REST | Custom queries, OpenAPI-based workflows, DII integration |

## Pattern Details

### 1. netapp_ontap SDK (Recommended for Most Tasks)

NetApp's official Python SDK provides ORM-like objects for ONTAP resources. This is the **preferred pattern** for most operations.

**When to Use:**

- Generating reports (licenses, space usage, cluster health)
- Retrieving structured data (volumes, aggregates, nodes)
- Operations that benefit from typed objects and IDE autocompletion
- When you need reliable, well-tested API interactions

**Advantages:**

- Official NetApp support and documentation
- Type-safe objects with clear attributes
- Handles pagination automatically
- Well-defined error handling

**Limitations:**

- Requires `netapp-ontap` package
- Some advanced CLI operations not available via REST
- Less flexible for custom queries

**Example Usage:**

```python
from netapp_ontap import HostConnection
from netapp_ontap.resources import Volume, Cluster

# Connect to cluster
config = Config()
cluster = config.clusters["mycluster"]
user = config.get_user("clusters", cluster.name)

with HostConnection(
    cluster.ip,
    username=user.user,
    password=user.get_password(),
    verify=False  # For self-signed certs
):
    # Get cluster info
    cluster_info = Cluster()
    cluster_info.get()
    print(f"Cluster: {cluster_info.name}, Version: {cluster_info.version.full}")

    # List all volumes
    for volume in Volume.get_collection():
        volume.get()  # Fetch full details
        print(f"Volume: {volume.name}, Size: {volume.size}")
```

**Commands Using This Pattern:**

- `nf licenses get/check/savings` - License management
- `nf events get/save-azure` - EMS event retrieval
- `nf reports locks/space-usage/html` - Report generation
- `nf utils validate` - Cluster validation

**Configuration Required:**

```toml
# In clusters data file (e.g., clusters.toml)
[mycluster]
name = "mycluster"
ip = "192.168.1.100"

# In users data file (e.g., users.toml)
[clusters.mycluster]
user = "admin"
password = "base64_encoded_password"
```

---

### 2. ONTAPCLI (SSH Access)

Direct SSH connection using Paramiko for executing ONTAP CLI commands.

**When to Use:**

- Running CLI commands not available via REST API
- Ad-hoc administrative tasks
- Debugging or troubleshooting
- Commands that require interactive prompts
- When you need raw CLI output

**Advantages:**

- Access to all CLI commands (including advanced/hidden)
- Familiar CLI syntax for ONTAP administrators
- Can handle interactive prompts
- Useful for automation of CLI-only operations

**Limitations:**

- Slower than REST (SSH overhead)
- Output parsing required (text-based)
- Connection management overhead
- Less structured error handling

**Example Usage:**

```python
from pynetappfoundry.clients.ontap.cli import ONTAPCLI

# Connect via SSH
config = Config()
cluster = config.clusters["mycluster"]
user = config.get_user("clusters", cluster.name)

cli = ONTAPCLI(
    name=cluster.name,
    host_or_ip=cluster.ip,
    username=user.user,
    password=user.get_password()
)

try:
    cli.connect()

    # Run a command
    output = cli.run_command("volume show -fields size,used")
    print(output)

    # Run and parse output
    volumes = cli.run_command_and_parse("volume show")
    for vol in volumes:
        print(f"Volume: {vol['Vserver']}/{vol['Volume']}")

finally:
    cli.disconnect()
```

**Commands Using This Pattern:**

- `nf utils run-cmd` - Execute arbitrary CLI commands

**Configuration Required:**

Same as netapp_ontap SDK (cluster IP and credentials).

---

### 3. APIWrapper / ONTAPAPIClient (Custom REST)

Custom OpenAPI-based REST client that works with any OpenAPI/Swagger specification.

**When to Use:**

- Querying Data Infrastructure Insights (DII) API
- Custom REST endpoints not covered by the SDK
- When you need fine-grained control over requests
- Working with OpenAPI 2.0 (Swagger) specifications
- Building extensible API integrations

**Advantages:**

- Works with any OpenAPI-compliant API
- Request body validation against schema
- Endpoint discovery and parameter suggestions
- Configurable SSL verification and timeouts
- Reusable for multiple API types (ONTAP, DII, custom)

**Limitations:**

- No response validation (yet)
- Requires OpenAPI specification files
- More setup than SDK for simple operations
- Returns raw dictionaries (no typed objects)

**Example Usage:**

```python
from pynetappfoundry.clients.ontap.api import ONTAPAPIClient

# Using ONTAPAPIClient (ONTAP-specific wrapper)
config = Config()
cluster = config.clusters["mycluster"]

client = ONTAPAPIClient(cluster, config)

# Call an endpoint
response = client.call_endpoint(
    path="/storage/volumes",
    method="GET",
    query_params={"fields": "name,size,state"}
)

for volume in response.get("records", []):
    print(f"Volume: {volume['name']}")
```

```python
from pynetappfoundry.clients.dii.api import DIIAPIClient

# Using DIIAPIClient for Data Infrastructure Insights
config = Config()
dii_config = config.diis["production"]

client = DIIAPIClient(dii_config, config)

# Query storage assets
response = client.call_endpoint(
    path="/assets/storages",
    method="GET"
)
```

**Commands Using This Pattern:**

- `nf metrics dump-dii` - Query DII metrics

**Configuration Required:**

```toml
# In settings.toml
[ontapapi.general]
base_api_path = "/api"

[ontapapi.schema]
location = "/path/to/apis/ontap"
filename = "all.json"

[diiapi.general]
base_api_path = "/rest/v1"

[diiapi.schema]
location = "/path/to/apis/dii"
filename = "all.json"
```

---

## Decision Matrix

Use this matrix to choose the right pattern:

| Scenario | Recommended Pattern | Reason |
|----------|---------------------|--------|
| Generate a report | `netapp_ontap` SDK | Typed objects, pagination handling |
| List volumes/aggregates | `netapp_ontap` SDK | Clean API, well-documented |
| Check license status | `netapp_ontap` SDK | LicensePackage resource available |
| Run CLI-only command | `ONTAPCLI` | No REST equivalent |
| Debug cluster issue | `ONTAPCLI` | Full CLI access |
| Query DII metrics | `APIWrapper` | DII uses different API |
| Custom REST endpoint | `APIWrapper` | Flexible, schema-validated |
| Bulk data export | `netapp_ontap` SDK | Handles pagination |
| Interactive troubleshooting | `ONTAPCLI` | Familiar CLI interface |

## Configuration Flow

All patterns share a common configuration flow:

```
┌─────────────────┐
│  settings.toml  │ ← API settings (paths, timeouts, SSL)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  clusters.toml  │ ← Cluster definitions (name, IP)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   users.toml    │ ← Credentials (username, encoded password)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Config class   │ ← Unified access to all configuration
└────────┬────────┘
         │
         ├──► netapp_ontap SDK (HostConnection)
         ├──► ONTAPCLI (SSH connection)
         └──► APIWrapper (REST client)
```

## Best Practices

1. **Prefer the SDK** - Use `netapp_ontap` for standard operations. It's well-tested and maintained by NetApp.

2. **Use SSH sparingly** - Reserve `ONTAPCLI` for operations that genuinely require CLI access.

3. **Validate SSL in production** - Set `verify=True` or provide a CA bundle for production environments.

4. **Handle credentials securely** - Use the Config class's credential management rather than hardcoding passwords.

5. **Close connections** - Always use context managers or try/finally to ensure connections are closed.

## See Also

- [Configuration Schema](../reference/config-schema.md) - Complete configuration reference
- [Usage Guide](basics.md) - General usage patterns
- [CLI Reference](../reference/cli.md) - Available CLI commands
