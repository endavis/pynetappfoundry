---
title: Configuration Schema Reference
description: Complete reference for pynetappfoundry TOML configuration files
audience:
  - users
  - developers
tags:
  - reference
  - configuration
---

# Configuration Schema Reference

This document provides a complete reference for all pynetappfoundry configuration files, including all valid sections, fields, types, and defaults.

## Overview

pynetappfoundry uses TOML files for configuration. Configuration is organized into two types:

| Type | Purpose | Loaded Into |
|------|---------|-------------|
| **Settings files** | Global settings, credentials, API config | `config.settings[filename]` |
| **Data files** | Resource definitions (clusters, connectors, etc.) | `config.data[section]` |

### Directory Structure

```
config/
├── settings.toml        # General settings, searchable keys, SMTP, licensing
├── users.toml           # Credentials for resource types
├── ontapapi.toml        # ONTAP REST API settings
├── diiapi.toml          # Data Infrastructure Insights API settings
├── consoleapi.toml      # Console SaaS (BlueXP) API settings
├── monitoring.toml      # Monitoring thresholds (optional)
├── environments/        # Data files (clusters, connectors, etc.)
│   ├── prod.toml
│   ├── dev.toml
│   └── ...
└── apis/                # API specifications (OpenAPI/Swagger)
    ├── ontap/
    │   └── all.json
    ├── dii/
    │   └── all.json
    └── console/
        └── console_openapi.yaml
```

### How Configuration Loading Works

1. All `.toml` files in the config directory are loaded recursively
2. Files with `[settings] type = "data"` are treated as **data files**
3. All other files are treated as **settings files**
4. Settings files are stored by filename: `settings.toml` → `config.settings["settings"]`
5. Data files populate `config.data` by section: `[clusters.NAME]` → `config.data["clusters"]["NAME"]`

---

## Settings Files

### settings.toml

General application settings. Loaded into `config.settings["settings"]`.

```toml
# Searchable keys configuration for each resource type
# These define which fields can be used in search queries

[clusters]
searchable_keys = ["div", "bu", "cloud", "app", "env", "subapp", "region"]

[aiqums]
searchable_keys = ["div", "bu", "cloud", "app", "env", "subapp", "region"]

[connectors]
searchable_keys = ["div", "bu", "cloud", "app", "env", "subapp", "region"]

[cloudinsights]
searchable_keys = ["div", "bu", "cloud", "app", "env", "subapp", "region"]

# SMTP settings for email notifications
[SMTP]
server = "smtp.example.com"     # Required: SMTP server hostname
port = 25                        # Optional: SMTP port (default: 25)
user = "smtp_user"               # Optional: SMTP username
password = "smtp_password"       # Optional: SMTP password
auth = "False"                   # Optional: Enable authentication (default: "False")

# Licensing notification settings
[licensing]
mailfrom = "netapp-licensing@example.com"  # Required: Sender email address
mailto = "netapp-team@example.com"          # Required: Recipient email address
```

#### SMTP Settings Fields

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `server` | string | Yes | - | SMTP server hostname |
| `port` | integer | No | `25` | SMTP server port |
| `user` | string | No | `""` | SMTP username for authentication |
| `password` | string | No | `""` | SMTP password for authentication |
| `auth` | string | No | `"False"` | Enable SMTP authentication (`"True"` or `"False"`) |

#### Licensing Settings Fields

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `mailfrom` | string | Yes | - | Sender email address for license notifications |
| `mailto` | string | Yes | - | Recipient email address for license notifications |

---

### users.toml

Credentials for different resource types. Loaded into `config.settings["users"]`.

```toml
# Default credentials for ONTAP clusters
[clusters]
user = "admin"
enc = "encoded_password_here"

# Credentials for AIQUM instances (if different from clusters)
[aiqums]
user = "aiqum_admin"
enc = "encoded_password_here"
```

#### Credential Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `user` | string | Yes | Username for authentication |
| `enc` | string | Yes | Encoded password (base64 or other encoding) |

**Note:** Individual resources can override these defaults by specifying `user` and `enc` in their data file entry.

---

### ontapapi.toml

ONTAP REST API settings. Loaded into `config.settings["ontapapi"]`.

```toml
[general]
base_api_path = "/api"    # Optional: Base path for ONTAP REST API (default: "/api")
```

#### ONTAP API Settings Fields

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `base_api_path` | string | No | `"/api"` | Base path for ONTAP REST API endpoints |

---

### diiapi.toml

Data Infrastructure Insights (DII) API settings. Loaded into `config.settings["diiapi"]`.

```toml
[general]
api_ro_token = "your-api-token-here"      # Required: Read-only API token
base_url = "https://your-tenant.cloudinsights.netapp.com"  # Required: DII tenant URL
base_api_path = "/rest/v1"                 # Optional: Base API path (default: "/rest/v1")
```

#### DII API Settings Fields

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `api_ro_token` | string | Yes | - | Read-only API token for DII authentication |
| `base_url` | string | Yes | - | Base URL for your DII tenant |
| `base_api_path` | string | No | `"/rest/v1"` | Base path for DII REST API endpoints |

---

### consoleapi.toml

Console SaaS (BlueXP) API settings. Loaded into `config.settings["consoleapi"]`.

v1 supports static tokens only. See `docs/example-config/apis/console/notes.txt` for how to obtain the tokens.

```toml
[general]
user_token = "paste-user-jwt-here"          # Required: User JWT from the BlueXP UI
# service_token = "paste-service-account-jwt-here"  # Optional: service-account JWT
base_url = "https://api.bluexp.netapp.com"  # Required: Console API base URL
org_id = "your-org-id"                      # Optional: Default organization ID
base_api_path = "/"                          # Optional: Base API path (default: "/")
timeout = 30.0                               # Optional: Request timeout in seconds (default: 30.0)
```

#### Console API Settings Fields

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `user_token` | string | Yes | - | User JWT obtained from the BlueXP UI |
| `service_token` | string | No | `null` | Service-account JWT. Lazy-validated: raises `ConsoleServiceTokenMissingError` if absent when a service-typed endpoint is called |
| `base_url` | string | Yes | - | Base URL for the Console API |
| `org_id` | string | No | `null` | Default organization ID. Can be overridden per `Console(config, org_id=...)` call |
| `base_api_path` | string | No | `"/"` | Base path for Console API endpoints |
| `timeout` | float | No | `30.0` | HTTP request timeout in seconds |

---

### monitoring.toml (Optional)

Monitoring thresholds and settings. Loaded into `config.settings["monitoring"]`.

```toml
[settings]
default_thresholds = { inodes = 80, aggregate = 90, volume = 90 }
DR = { inodes = 90, aggregate = 90, volume = 90 }
```

---

## Data Files

Data files define resources like clusters, connectors, and AIQUM instances. They **must** include `[settings] type = "data"` to be recognized as data files.

### Common Structure

```toml
[settings]
type = "data"    # Required: Marks this as a data file

[clusters.CLUSTER-NAME]
# Cluster configuration...

[aiqums.AIQUM-NAME]
# AIQUM configuration...

[connectors.CONNECTOR-NAME]
# Connector configuration...
```

### Supported Resource Types

| Section | Description | Pydantic Model |
|---------|-------------|----------------|
| `clusters` | ONTAP clusters | `ClusterConfig` |
| `aiqums` | Active IQ Unified Manager instances | `AIQUMConfig` |
| `connectors` | Cloud Insights connectors | `ConnectorConfig` |
| `cloudinsights` | Cloud Insights tenants | `CloudInsightsConfig` |
| `azure` | Azure resources | `AzureConfig` |

**Note:** These are the only resource types recognized by the config loader. Data in other sections will be ignored.

### Dynamic Fields

The configuration system is **dynamic** - you can add custom fields beyond those documented here. All Pydantic models use `extra="allow"`, meaning additional fields are accepted and preserved. This allows you to:

- Add organization-specific metadata (e.g., `cost_center`, `owner_email`)
- Store custom tags for your workflows
- Extend resources with fields needed by your scripts

```toml
[clusters.CLUSTER-PROD-01]
ip = "192.168.1.173"
env = "Prod"
# Custom fields - not validated but preserved
cost_center = "CC-12345"
owner_email = "admin@example.com"
maintenance_window = "Sunday 02:00-06:00"
```

---

### Clusters

ONTAP cluster definitions.

```toml
[clusters.CLUSTER-PROD-01]
ip = "192.168.1.173"          # Required: Cluster management IP
name = "CLUSTER-PROD-01"      # Optional: Defaults to section key
div = "ITS"                   # Optional: Division
bu = "LAR"                    # Optional: Business unit
app = "Storage"               # Optional: Application
env = "Prod"                  # Optional: Environment
subapp = "Primary"            # Optional: Sub-application
tags = ["active", "nfs"]      # Optional: Tags for filtering
region = "USCU"               # Optional: Region
cloud = ""                    # Optional: Cloud provider

# Per-cluster credentials (override users.toml)
user = "cluster_admin"        # Optional: Override default user
enc = "cluster_password"      # Optional: Override default password
```

#### Cluster Fields

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `ip` | string | Yes | - | Cluster management IP address |
| `name` | string | No | Section key | Cluster name (auto-set from TOML key) |
| `div` | string | No | `""` | Division identifier |
| `bu` | string | No | `""` | Business unit identifier |
| `app` | string | No | `""` | Application identifier |
| `env` | string | No | `""` | Environment (Prod, Dev, Test, etc.) |
| `subapp` | string | No | `""` | Sub-application identifier |
| `tags` | list[string] | No | `[]` | Tags for filtering and categorization |
| `region` | string | No | `""` | Geographic region |
| `cloud` | string | No | `""` | Cloud provider - use `"azure"` for Azure-hosted clusters |
| `user` | string | No | From users.toml | Override default username |
| `enc` | string | No | From users.toml | Override default encoded password |

**Special Field Behavior:**

- **`cloud`**: When set to `"azure"` (case-insensitive), enables Azure-specific features like scheduled maintenance event checking via the `nf events azevents` command.
- **`name`**: Auto-populated from the TOML section key if not specified (e.g., `[clusters.MY-CLUSTER]` sets `name = "MY-CLUSTER"`).

---

### AIQUMs

Active IQ Unified Manager instance definitions.

```toml
[aiqums.AIQUM-PROD]
ip = "192.168.1.150"
div = "ITS"
bu = "LAR"
env = "Prod"
```

#### AIQUM Fields

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `ip` | string | Yes | - | AIQUM management IP address |
| `name` | string | No | Section key | Instance name (auto-set from TOML key) |
| `div` | string | No | `""` | Division identifier |
| `bu` | string | No | `""` | Business unit identifier |
| `env` | string | No | `""` | Environment |

---

### Connectors

Cloud Insights connector definitions.

```toml
[connectors.CONNECTOR-PROD-01]
ip = "192.168.1.132"
div = "ITS"
bu = "LAR"
env = "Prod"
```

#### Connector Fields

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `ip` | string | Yes | - | Connector IP address |
| `name` | string | No | Section key | Connector name (auto-set from TOML key) |
| `div` | string | No | `""` | Division identifier |
| `bu` | string | No | `""` | Business unit identifier |
| `env` | string | No | `""` | Environment |

---

### Cloud Insights

Cloud Insights tenant definitions.

```toml
[cloudinsights.TENANT-PROD]
ip = "tenant.cloudinsights.netapp.com"
div = "ITS"
bu = "LAR"
env = "Prod"
```

#### Cloud Insights Fields

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `ip` | string | Yes | - | Tenant URL or identifier |
| `name` | string | No | Section key | Tenant name (auto-set from TOML key) |
| `div` | string | No | `""` | Division identifier |
| `bu` | string | No | `""` | Business unit identifier |
| `env` | string | No | `""` | Environment |

---

### Azure

Azure resource definitions.

```toml
[azure.AZURE-PROD]
ip = ""
div = "ITS"
bu = "LAR"
env = "Prod"
subscription_id = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
resource_group = "rg-netapp-prod"
```

#### Azure Fields

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `ip` | string | No | `""` | IP address (if applicable) |
| `name` | string | No | Section key | Resource name (auto-set from TOML key) |
| `div` | string | No | `""` | Division identifier |
| `bu` | string | No | `""` | Business unit identifier |
| `env` | string | No | `""` | Environment |
| `subscription_id` | string | No | `""` | Azure subscription ID |
| `resource_group` | string | No | `""` | Azure resource group name |

---

## Accessing Configuration in Code

### Using Accessor Methods (Recommended)

```python
from pynetappfoundry import Config, ConfigurationError

config = Config(config_dir="config")

# Get SMTP settings (returns SMTPSettings object)
smtp = config.get_smtp_settings()
print(f"SMTP server: {smtp.server}:{smtp.port}")

# Get ONTAP API settings (returns ONTAPAPISettings object)
ontap = config.get_ontap_api_settings()
print(f"ONTAP API path: {ontap.base_api_path}")

# Get DII API settings (returns DIIAPISettings object)
dii = config.get_dii_api_settings()
print(f"DII URL: {dii.base_url}")

# Get licensing settings (returns LicensingSettings or None)
licensing = config.get_licensing_settings()
if licensing:
    print(f"License notifications to: {licensing.mailto}")

# Generic setting access with clear error messages
base_path = config.get_setting("ontapapi", "general", "base_api_path")

# With default value (no error if missing)
custom = config.get_setting("custom", "key", default="fallback")
```

### Searching Resources

```python
# Get all clusters
all_clusters = config.search("clusters", {})

# Search by single field
prod_clusters = config.search("clusters", {"env": "Prod"})

# Search by multiple fields
specific = config.search("clusters", {"bu": "LAR", "env": "Prod"})

# OR operator (match any)
dev_or_test = config.search("clusters", {"env": "Dev || Test"})

# AND operator for list fields (match all tags)
active_nfs = config.search("clusters", {"tags": "active && nfs"})
```

### Getting Credentials

```python
# Get credentials for a resource type
user, enc_password = config.get_user("clusters")

# Get credentials for a specific resource (with override support)
user, enc_password = config.get_user("clusters", "CLUSTER-PROD-01")
```

---

## Environment Variables

pynetappfoundry supports environment variables for overriding configuration values, particularly useful for CI/CD pipelines, containers, and secure credential management.

### Available Environment Variables

| Variable | Purpose | Example |
|----------|---------|---------|
| `NF_CONFIG_DIR` | Override the config directory path | `NF_CONFIG_DIR=/etc/pynetappfoundry` |
| `NF_<CLUSTER>_USER` | Override username for a specific cluster | `NF_CLUSTER_PROD_01_USER=admin` |
| `NF_<CLUSTER>_PASSWORD` | Override password for a specific cluster | `NF_CLUSTER_PROD_01_PASSWORD=base64encoded` |

### Cluster Name Conversion

Cluster names are converted to environment variable format by:
1. Replacing hyphens (`-`) with underscores (`_`)
2. Converting to uppercase
3. Prefixing with `NF_`

| Cluster Name | User Env Var | Password Env Var |
|--------------|--------------|------------------|
| `cluster-prod-01` | `NF_CLUSTER_PROD_01_USER` | `NF_CLUSTER_PROD_01_PASSWORD` |
| `my-cluster` | `NF_MY_CLUSTER_USER` | `NF_MY_CLUSTER_PASSWORD` |
| `simple` | `NF_SIMPLE_USER` | `NF_SIMPLE_PASSWORD` |

### Credential Resolution Order

Credentials are resolved in the following order (first found wins):

1. **Environment variables** - `NF_<CLUSTER>_USER` and `NF_<CLUSTER>_PASSWORD`
2. **Object-specific config** - `user` and `enc` fields in the cluster's data file entry
3. **Default credentials** - `users.toml` defaults for the resource type

### Example Usage

```bash
# Set credentials via environment variables
export NF_CLUSTER_PROD_01_USER=admin
export NF_CLUSTER_PROD_01_PASSWORD=$(echo -n 'mypassword' | base64)

# Override config directory
export NF_CONFIG_DIR=/path/to/custom/config

# Run command - credentials will be used automatically
nf licenses get -f '{"name": "cluster-prod-01"}'
```

### Docker/Container Usage

```dockerfile
ENV NF_CONFIG_DIR=/app/config
ENV NF_CLUSTER_PROD_01_USER=admin
ENV NF_CLUSTER_PROD_01_PASSWORD=YWRtaW5fcGFzc3dvcmQ=
```

### Security Notes

- Environment variables take precedence over config files, allowing secure injection of credentials
- Passwords must be base64 encoded (same format as the `enc` field in config files)
- Use container secrets or CI/CD secret management for production deployments

---

## Configuration CLI Commands

pynetappfoundry provides commands to inspect and validate your configuration.

### nf config show

Display the current loaded configuration.

```bash
# Show all configuration
nf config show

# Show only a specific section
nf config show -s clusters
nf config show -s settings
nf config show -s users

# Show with passwords unmasked (use with caution)
nf config show --unmask
```

**Options:**

| Option | Description |
|--------|-------------|
| `-s, --section` | Show only a specific section (clusters, settings, users, etc.) |
| `--unmask` | Show passwords and tokens unmasked (default: masked with `********`) |

### nf config validate

Validate configuration files and check for common issues.

```bash
nf config validate
```

**Checks performed:**

- Configuration directory exists and is readable
- Cluster definitions are valid against Pydantic models
- User credentials are properly formatted
- ONTAP API settings are configured
- All clusters have valid credentials configured
- Optional settings (DII API, SMTP, Licensing) are valid if present

**Example output:**

```
Validating configuration in: /path/to/config

Configuration Validation
├── Clusters
│   ├── cluster-prod-01
│   └── cluster-dev-01
├── Users
│   └── clusters
├── Settings
│   ├── ONTAP API
│   ├── DII API: Not configured (optional)
│   ├── SMTP: Not configured (optional)
│   └── Licensing: Not configured (optional)
└── Cluster Credentials
    ├── cluster-prod-01: admin
    └── cluster-dev-01: admin

Configuration is valid
```

---

## Complete Example

### Minimal Configuration

A minimal working configuration requires:

**config/settings.toml:**
```toml
[clusters]
searchable_keys = ["env"]
```

**config/users.toml:**
```toml
[clusters]
user = "admin"
enc = "YWRtaW5fcGFzc3dvcmQ="
```

**config/ontapapi.toml:**
```toml
[general]
base_api_path = "/api"
```

**config/environments/clusters.toml:**
```toml
[settings]
type = "data"

[clusters.my-cluster]
ip = "192.168.1.100"
env = "Prod"
```

### Full Configuration

See the `example-config/` directory in the repository for a complete working example with all features configured.

---

## Error Messages

When configuration is missing or invalid, pynetappfoundry provides clear error messages:

```
ConfigurationError: Missing configuration key 'ontapapi.general'.
Available keys at 'ontapapi': ['other_section'].
Check your configuration files.
```

```
ConfigurationError: Invalid SMTP configuration: 1 validation error for SMTPSettings
server
  Field required [type=missing, input_value={}, input_type=dict]
Ensure settings.toml has a valid [SMTP] section with 'server', 'port', 'user', 'password', and 'auth' fields.
```
