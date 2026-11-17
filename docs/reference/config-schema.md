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

pynetappfoundry uses TOML files for configuration. Configuration is organized into three types:

| Type | Purpose | Loaded Into |
|------|---------|-------------|
| **Settings files** | Global settings, credentials, API config | `config.settings[filename]` |
| **Data files** | Resource definitions (clusters, connectors, etc.) | `config.data[section]` |
| **Scopes** | A directory (marked by `scope.toml`) with its own inventory, credentials, thresholds and Console account | `config.scopes`, `config.scope_settings[scope][filename]`; its data files go into `config.data` |

### Directory Structure

```
config/
├── settings.toml        # General settings, searchable keys, SMTP, licensing
├── users.toml           # Credentials for resource types
├── ontapapi.toml        # ONTAP REST API settings
├── aiqumapi.toml        # AIQUM REST API settings
├── diiapi.toml          # Data Infrastructure Insights API settings
├── consoleapi.toml      # Console SaaS (BlueXP) API settings
├── monitoring.toml      # Monitoring thresholds (optional)
├── environments/        # Data files (clusters, connectors, etc.)
│   ├── prod.toml
│   ├── dev.toml
│   └── ...
├── Org1/                # A scope (optional), see "Scopes" below
│   ├── scope.toml       # Marker: makes this directory a scope
│   ├── clusters.toml    # Data file of the scope
│   ├── users.toml       # Credentials of the scope
│   ├── monitoring.toml  # Thresholds of the scope
│   └── consoleapi.toml  # The scope's own Console account
└── apis/                # API specifications (OpenAPI/Swagger)
    ├── ontap/
    │   └── all.json
    ├── aiqum/
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
6. A top-level directory that contains `scope.toml` is a [scope](#scopes). Its data files load into `config.data` like any other, and `config.get_scope(data_type, name)` reports which scope an object came from. Its `users.toml`, `monitoring.toml` and `consoleapi.toml` load into `config.scope_settings[scope]` and never into `config.settings`
7. A config directory without any `scope.toml` loads exactly as in steps 1 to 5

---

## Scopes

A scope partitions the config directory: one inventory, one set of credentials, one set of thresholds and at most one Console account per directory. See [ADR-0028](../decisions/0028-scope-directories-partition-the-config-dir-with-per-scope-credentials-thresholds-and-console-account.md).

### The marker: scope.toml

A top-level directory of the config directory that contains `scope.toml` is a scope. The file is validated, and every key is optional:

```toml
name = "Org1"                 # Optional; when set it must equal the directory name
description = "Example scope" # Optional
tags = ["example"]            # Optional
```

An unknown key, or a `name` that differs from the directory name, raises `ConfigurationError` naming the file. `scope.toml` is valid only directly inside a top-level directory: at the config root, nested deeper, or inside a hidden directory or `apis`, it is an error naming its path. Subdirectories inside a scope are allowed and load as part of it.

### What a scope may contain

- **Data files** (`[settings] type = "data"`), anywhere under the scope directory.
- **Three settings files**, matched by file stem: `users.toml`, `monitoring.toml` and `consoleapi.toml`.

Any other settings file in a scope (`settings.toml`, `ontapapi.toml`, `aiqumapi.toml`, `diiapi.toml`, and so on) raises `ConfigurationError` naming the file and the allowed list. Everything else stays global.

### Precedence

A scope's settings are shared root defaults that the scope overrides:

- **Credentials** (`get_user`, `get_secret`): environment variable, then the object's own entry, then the scope's `users.toml`, then the root `users.toml`. `user` and `enc` fall back independently. An object outside any scope never sees a scope's defaults.
- **Other settings** (`get_setting(..., scope="Org1")`, `get_object_setting(data_type, name, *keys)`): the scope's file is read first and a path it does not set falls back to the root. An unknown scope raises `ConfigurationError` listing the scopes.

### The Console account of a scope

A scope has at most one Console account, and it is strict:

- A scope without its own `consoleapi.toml` has no Console account. `get_console_api_settings(scope="Org1")` raises; it never falls back to the root account.
- A scope's `consoleapi.toml` may contain only a `[general]` table, validated by the same rules as the root one (see [consoleapi.toml](#consoleapitoml)).
- From the root `[general]` a scope inherits only `base_url`, `ui_base_url`, `base_api_path` and `timeout`. Credentials, `org_id`, `agent_ids`, `token_endpoint`, `audience` and `user_client_id` come only from the scope.
- The refresh token comes only from the scope's `users.toml` `[console]`, with no root fallback. The `NF_CONSOLE_USER` and `NF_CONSOLE_PASSWORD` variables apply to the root account only and are ignored for a scope.
- `Console(config, scope="Org1")`, `ConsoleAPIClient(config, scope=...)` and `ConsoleAgentClient(config, agent_id, scope=...)` use the scope's account. The OCCM `DataSource` backend uses the scope of the connector it queries.

### Console accounts and discovery

Each scope's `consoleapi.toml` is a Console service account, and the root is the default account. `Config.console_account_scopes()` lists them: `None` for the root, then the scopes that have a `consoleapi.toml`, sorted.

- The root counts as an account only with credentials: its `[general]` has `user_token`, `service_token` or `client_id`, or a root refresh token resolves (`users.toml` `[console]` or `NF_CONSOLE_PASSWORD`). A root that only carries `base_url`, `ui_base_url`, `base_api_path` or `timeout` is not an account.
- `org_id` is not needed for discovery: `ConsoleDiscovery` finds the organizations of each account. See [Console Agent](../usage/console-agent.md#discovering-organizations-agents-and-working-environments).
- `[connectors].agent_id` is still required for a connector; discovery does not fill it in.

### Unique names

Object names must be unique across the config directory, per data type. Any duplicate (two scopes, the root and a scope, the same scope twice, or two files in the root) raises `ConfigurationError` naming both files. The same name under two different data types, such as a cluster and a connector, is fine.

Write a scope's credentials with `nf config set-credential --scope`, and inspect or check a scope with `nf config show --scope` and `nf config validate --scope`. See [CLI Reference](cli.md#config).

A complete example is in `docs/example-config/Org1/`.

---

## Settings Files

### SOPS-encrypted values

These settings fields accept a `SOPS[...]` value instead of plaintext:

| File | Section | Fields |
|------|---------|--------|
| `settings.toml` | `[SMTP]` | `password` |
| `diiapi.toml` | `[general]` | `api_ro_token` |
| `consoleapi.toml` | `[general]` | `client_secret`, `service_token`, `user_token` |

Values are decrypted when the section is read, at most once per `Config` instance (the plaintext
is kept in memory only, never written back to the settings). Plaintext values still work. A value
that cannot be decrypted raises a `ConfigurationError` naming the field, file and section, for
example `Failed to decrypt the SOPS value of 'password' in settings.toml [SMTP]: ...`; it never
contains the ciphertext or the `sops` error text. `nf config validate` reports such a section as
Invalid, not as "Not configured". `nf config show` prints the ciphertext (masked by default).

Produce a value with `nf config encrypt-value`, which prompts for the secret (hidden input) and
prints only the `SOPS[...]` string. It needs `sops` and an age key (`nf config init-sops`).

These fields are `SecretStr` in the settings models (`SMTPSettings.password`,
`DIIAPISettings.api_ro_token`, `ConsoleAPISettings.service_token` / `user_token`): read the value
with `.get_secret_value()`.

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
| `password` | SecretStr | No | `""` | SMTP password for authentication. SOPS value accepted |
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

# Console refresh token (see consoleapi.toml). `user` is only a label; it is never sent.
[console]
user = "console"
enc = "SOPS[...]"  # the refresh token, SOPS-encrypted (or plaintext)
```

#### Credential Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `user` | string | Yes | Username for authentication |
| `enc` | string | Yes | Encoded password (base64 or other encoding) |

For `[console]`, `enc` holds the NetApp refresh token and `user` is a display label that is never sent. SOPS values are decrypted, and the `NF_CONSOLE_USER` / `NF_CONSOLE_PASSWORD` environment variables override the file. Write the entry with `nf config set-credential --type console --user console`; the password prompt takes the refresh token. For a scope's `users.toml`, add `--scope Org1`.

**Note:** Individual resources can override these defaults by specifying `user` and `enc` in their data file entry.

---

### ontapapi.toml

ONTAP REST API settings. Loaded into `config.settings["ontapapi"]`.

```toml
[general]
base_api_path = "/api"    # Optional: Base path for ONTAP REST API (default: "/api")
# verify_ssl = true       # Optional: validate cluster TLS certificates (default: false)
# ca_bundle = "certs/internal-ca.pem"  # Optional: validate against this CA bundle
```

#### ONTAP API Settings Fields

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `base_api_path` | string | No | `"/api"` | Base path for ONTAP REST API endpoints |
| `verify_ssl` | boolean | No | `false` | Validate the TLS certificate chain and hostname with the default CA bundle. Default for every cluster; a cluster setting overrides it |
| `ca_bundle` | string | No | - | Path to a CA bundle (relative to the config directory, `~` expanded). Cannot be combined with `verify_ssl = false` |

With either setting on, no TLS fingerprint is pinned. Precedence is cluster `ca_bundle`, cluster `verify_ssl`, global `ca_bundle`, global `verify_ssl`, then off. See [Host identity](../usage/basics.md#host-identity-ssh-host-keys-and-tls-certificates).

---

### aiqumapi.toml

Active IQ Unified Manager (AIQUM) REST API settings. Loaded into `config.settings["aiqumapi"]`. The `[general]` section is required; every field has a default. See [AIQUM API](../usage/aiqum-api.md).

```toml
[general]
base_api_path = "/api"    # Optional: Base path for the AIQUM REST API (default: "/api")
# timeout = 30.0          # Optional: request timeout in seconds (default: 30.0)
# verify_ssl = true       # Optional: validate instance certificates with the default CA bundle
# ca_bundle = "certs/internal-ca.pem"  # Optional: validate against this CA bundle
# max_parent_requests = 500  # Optional: cap on per-parent requests (0 = unlimited)
```

#### AIQUM API Settings Fields

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `base_api_path` | string | No | `"/api"` | Base path for AIQUM REST API endpoints |
| `timeout` | float | No | `30.0` | Request timeout in seconds |
| `verify_ssl` | boolean | No | `false` | Default for every instance: validate the certificate chain instead of pinning the fingerprint |
| `ca_bundle` | string | No | - | Default for every instance: CA bundle path (relative to the config directory); not allowed with `verify_ssl = false` |
| `max_parent_requests` | integer | No | `500` | Most per-parent requests one query may send when a `{key}/metrics` model is queried without `path_params`; more parents raises `ValueError` before any child request. `0` = unlimited |

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
| `api_ro_token` | SecretStr | Yes | - | Read-only API token for DII authentication. SOPS value accepted |
| `base_url` | string | Yes | - | Base URL for your DII tenant |
| `base_api_path` | string | No | `"/rest/v1"` | Base path for DII REST API endpoints |

With several tenants, `DIIAPIClient(config, name="TENANT")` reads `base_url` and the token from `[cloudinsights.TENANT]` in a data file (see [Cloud Insights](#cloud-insights)), falling back to `[general]` for either. `DIIAPIClient(config)` uses `[general]` alone.

---

### consoleapi.toml

Console SaaS (BlueXP) API settings. Loaded into `config.settings["consoleapi"]`.

Three authentication modes are supported. See `docs/example-config/apis/console/notes.txt` for how to obtain the credentials.

- **Static tokens:** `user_token` and/or `service_token`, pasted into the file.
- **OAuth refresh token (user slot):** a long-lived NetApp refresh token, stored in `users.toml` under `[console]` (see [users.toml](#userstoml)), never in `consoleapi.toml`. The client exchanges it at `token_endpoint` for a user access token (valid for 24 hours), keeps it in memory, renews it shortly before it expires, and on a 401 refetches and retries once. Setting `refresh_token` in `consoleapi.toml` is a configuration error. The refresh token and the access tokens are never logged.
- **OAuth client credentials:** `client_id` and `client_secret` of a Console service account. The client exchanges them for a service token when it is constructed, keeps the token in memory, renews it shortly before it expires, and on a 401 refetches and retries once. The secret and the tokens are never logged.

The same settings drive `ConsoleAgentClient`, which calls one Console agent's `/occm/api`; see [Console Agent](../usage/console-agent.md).

```toml
[general]
user_token = "paste-user-jwt-here"          # Optional: User JWT from the BlueXP UI
# service_token = "paste-service-account-jwt-here"  # Optional: static service-account JWT
# client_id = "your-service-account-client-id"      # Optional: OAuth client credentials
# client_secret = "your-service-account-client-secret"
base_url = "https://api.bluexp.netapp.com"  # Required: Console API base URL
# ui_base_url = "https://console.netapp.com" # Optional: Console UI host for links (not the API base_url)
org_id = "your-org-id"                      # Optional: Default organization ID
# agent_ids = ["your-agent-idclients"]      # Optional: Console agent IDs for Console.find_connector
base_api_path = "/"                          # Optional: Base API path (default: "/")
timeout = 30.0                               # Optional: Request timeout in seconds (default: 30.0)
```

#### Console API Settings Fields

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `user_token` | SecretStr | No | `null` | User JWT obtained from the BlueXP UI. SOPS value accepted |
| `service_token` | SecretStr | No | `null` | Static service-account JWT. SOPS value accepted. Lazy-validated: raises `ConsoleServiceTokenMissingError` if absent when a service-typed endpoint is called |
| `client_id` | string | No | `null` | OAuth client ID of a service account. Set together with `client_secret` |
| `client_secret` | string | No | `null` | OAuth client secret of a service account. Held as a secret value and never logged. SOPS value accepted |
| `refresh_token` | secret string | No | `null` | Not read from `consoleapi.toml`: it is resolved from `users.toml` `[console]` (`enc`, SOPS-decrypted, overridable by `NF_CONSOLE_PASSWORD`). Backs the user slot. Held as a secret value and never logged |
| `user_client_id` | string | No | `"Mu0V1ywgYteI6w1MbD15fKfVIUrNXGWC"` | OAuth client ID the refresh token is exchanged with. The default is NetApp's documented public constant. Only valid with a refresh token |
| `token_endpoint` | string | No | `"https://netapp-cloud-account.auth0.com/oauth/token"` | Token endpoint for the client-credentials and refresh-token exchanges. Only valid with client credentials or a refresh token |
| `audience` | string | No | `"https://api.cloud.netapp.com"` | Audience requested for the token. Only valid with client credentials |
| `base_url` | string | Yes | - | Host (and any proxy prefix) for the Console API. The bundled spec keys each operation by its full path (for example `/v1/management/organizations`), which is appended to it |
| `ui_base_url` | string | No | `"https://console.netapp.com"` | Console UI host that the link builders and the reports use. It is the UI host, not the API `base_url`. Reports read it without needing Console credentials |
| `org_id` | string | No | `null` | Default organization ID. Can be overridden per `Console(config, org_id=...)` call |
| `agent_ids` | list of strings | No | `[]` | Console agent IDs that `Console.find_connector` searches when called without an `agent_ids` argument. Agent IDs end in `clients`. The tenancy API lists none for a service token, so they are configured here |
| `base_api_path` | string | No | `"/"` | Fallback path prefix, used only for operations whose spec entry declares no `servers`. It has no effect with the bundled Console spec, whose operations all carry a bare-host server |
| `timeout` | float | No | `30.0` | HTTP request timeout in seconds |

Validation rules (error messages name fields, never values):

- `client_id` and `client_secret` are set together or not at all.
- Client credentials and `service_token` are mutually exclusive, so a stale pasted token cannot take precedence.
- `audience` requires client credentials, and `token_endpoint` requires client credentials or a refresh token.
- A refresh token and `user_token` are mutually exclusive: the mode is implicit, and there is no `auth_mode` setting.
- `user_client_id` requires a refresh token.
- At least one of `user_token`, a refresh token, `service_token` or client credentials is required.

Routing: operations tagged for the user token require the user slot (`user_token` or a refresh token), and operations tagged for the service token require the service slot (`service_token` or client credentials). Operations with no tag, which includes every operation the client calls today, use the user slot when one is set and the service slot otherwise. A configuration with a `user_token` therefore behaves as before. See [ADR-0019](../decisions/0019-console-runtime-client-architecture-org-scoped-access-and-per-token-type-wrapper-isolation.md).

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
| `connectors` | Console agent VMs (the inventory report reads them as agents; `agent_id` is optional) | `ConnectorConfig` |
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

# Per-cluster TLS certificate validation (override ontapapi.toml)
# verify_ssl = true           # Optional: validate with the default CA bundle
# ca_bundle = "certs/ca.pem"  # Optional: validate against this CA bundle
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
| `verify_ssl` | boolean | No | From ontapapi.toml, else `false` | Validate the REST TLS certificate chain and hostname with the default CA bundle |
| `ca_bundle` | string | No | From ontapapi.toml | Path to a CA bundle (relative to the config directory). Cannot be combined with `verify_ssl = false` |

**Special Field Behavior:**

- **`verify_ssl` / `ca_bundle`**: Precedence is cluster `ca_bundle`, cluster `verify_ssl`, global `ca_bundle` (`ontapapi.toml`), global `verify_ssl`, then off. A cluster `verify_ssl = false` turns off a global `ca_bundle`. With validation on, no TLS fingerprint is pinned.

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
| `verify_ssl` | boolean | No | - | Validate this instance's certificate chain instead of pinning; overrides `aiqumapi.toml` |
| `ca_bundle` | string | No | - | CA bundle path for this instance; overrides `aiqumapi.toml` |
| `user` | string | No | From users.toml | Override default username |
| `enc` | string | No | From users.toml | Override default encoded password |

---

### Connectors

Console agent (connector) VM definitions.

```toml
[connectors.CONNECTOR-PROD-01]
ip = "192.168.1.132"
div = "ITS"
bu = "LAR"
env = "Prod"
agent_id = "AGENT-ID"   # optional; needed to query this agent through DataSource
```

`agent_id` is the Console agent id. `DataSource` reads it when `cluster=` names this
entry for an OCCM model ([ADR-0027](../decisions/0027-occm-backend-is-live-only-and-delegates-to-the-typed-console-agent-ops.md)).
A connector without a non-blank `agent_id` raises `ValueError` naming `connectors.<name>`.

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
| `base_url` | string | No | `diiapi.toml` `[general]` | API URL for `DIIAPIClient(config, name=...)`. Never derived from `ip` |
| `user` | string | No | From users.toml | A label for the API token |
| `enc` | string | No | From users.toml | The tenant's API token (SOPS value accepted). Falls back to `diiapi.toml` `api_ro_token` |

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

# Scoped access (see Scopes): the scope's file first, then the root
inodes = config.get_setting("monitoring", "settings", "default_thresholds", "inodes", scope="Org1")

# The same, for the scope an inventory object belongs to
inodes = config.get_object_setting(
    "clusters", "ORG1-PROD-01", "monitoring", "settings", "default_thresholds", "inodes"
)

# Which scope an object came from (None for an object outside any scope)
scope = config.get_scope("clusters", "ORG1-PROD-01")
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

# The scope an object came from. "scope" is a reserved, built-in search key: it is
# never a field in the data files, and find_closest never relaxes it.
org1 = config.search("clusters", {"scope": "Org1"})
root_only = config.search("clusters", {"scope": ""})   # objects outside any scope
either = config.search("clusters", {"scope": "Org1 || Org2", "env": "Prod"})
```

On the command line the same filter works: `-f '{"scope":"Org1"}'`.

### Getting Credentials

```python
# Get credentials for a resource type
user, enc_password = config.get_user("clusters")

# Get credentials for a specific resource (with override support)
user, enc_password = config.get_user("clusters", "CLUSTER-PROD-01")
```

For an object in a [scope](#scopes), `get_user` and `get_secret` find the scope on their own from the object name, so the calls do not change. `get_user(..., scope="Org1")` reads the defaults of an explicit scope instead.

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

1. **Environment variables** - `NF_<OBJECT>_USER` and `NF_<OBJECT>_PASSWORD`
2. **Object-specific config** - `user` and `enc` fields in the object's data file entry
3. **Scope defaults** - the object's [scope](#scopes) `users.toml` for the resource type (only for an object in a scope)
4. **Default credentials** - the root `users.toml` defaults for the resource type

`user` and `enc` fall back independently through steps 2 to 4. This applies to every inventory type (`clusters`, `aiqums`, `connectors`, `cloudinsights`, `azure`, `ibm`). Write an object's entry with `nf config set-credential --type <type> --name <object> --user <user>`; `--cluster NAME` is an alias for `--type clusters --name NAME`.

**Token-style secrets** (a Cloud Insights API token, which has no username) live in the same `enc` field, and `user` is only a label. They resolve in this order (first found wins):

1. `NF_<OBJECT>_PASSWORD`
2. `enc` in the object's data file entry
3. `enc` in the object's scope `users.toml` under the type (scoped objects only)
4. `enc` in the root `users.toml` under the type
5. the client's settings file (for Cloud Insights, `diiapi.toml` `[general]` `api_ro_token`)

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
