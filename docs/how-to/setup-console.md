---
title: Set Up Console and Its Agents
description: Configure a Console (BlueXP) account at the root or per scope, add its agents, and check them with nf doctor
audience:
  - users
tags:
  - how-to
  - configuration
  - console
---

# Set Up Console and Its Agents

**Goal:** give `nf` a Console (BlueXP) account, either one for the whole config directory or one per scope, and confirm that the token works and each Console agent (connector, also called OCCM) answers.

## Before you start

- A config directory, and SOPS set up for an encrypted secret or token: [Set up a config directory and SOPS secrets](sops-secrets.md).
- One way to authenticate:
    - a **service account**: its client id and client secret, created in Console. This is best for unattended runs.
    - a **refresh token**: generate one at <https://services.cloud.netapp.com/refresh-token>. It acts as your user and renews itself.
- For accounts per scope: the scope directories, each with a `scope.toml` marker. See [Config schema: Scopes](../reference/config-schema.md#scopes).

## Steps

### 1. Choose where the account lives

- **One account:** `<config>/apis/console/consoleapi.toml`, the root account.
- **One account per scope:** `<config>/<scope>/consoleapi.toml`, such as `<config>/bu1/consoleapi.toml`. A scope never falls back to the root account. Its file may contain only a `[general]` table.

A directory is a scope only when it contains `scope.toml`, which may be empty. Without the marker, the directory's `consoleapi.toml` loads as a root settings file instead.

### 2. Add the settings

Create the `consoleapi.toml` from step 1:

```toml
[general]
base_url = "https://api.bluexp.netapp.com"
client_id = "<service account client id>"   # service account only
# org_id = "<organization id>"              # optional
```

`base_url` is required. A scope inherits `base_url`, `ui_base_url`, `base_api_path` and `timeout` from a root `consoleapi.toml` when one exists, and nothing else. See [Config schema: consoleapi.toml](../reference/config-schema.md#consoleapitoml) for every key.

### 3. Store the secret

For a service account, store the client secret. Add `--scope bu1` for a scope's account:

```bash
nf config set-credential --setting consoleapi.client_secret --scope bu1
```

```
Setting consoleapi.client_secret stored in scope 'bu1'
  File: config/bu1/consoleapi.toml
  Table: general
  Key: client_secret
  Value: (encrypted)
```

For a refresh token, store it in `users.toml` `[console]`, never in `consoleapi.toml`. `--user` is only a label, and the password prompt takes the token. Add `--scope bu1` for a scope:

```bash
nf config set-credential --type console --user console
```

```
Password encrypted successfully.
Refresh token stored
  File: config/users.toml
  User: console
  Refresh token: (encrypted)
  This is the refresh token, not the client secret. Store the client secret
with: nf config set-credential --setting consoleapi.client_secret
```

Use one mode per account. `client_id` and `client_secret` must be set together, and a refresh token cannot be combined with a static `user_token`.

### 4. Download the API spec

```bash
nf config download-spec --api console
```

```
Wrote config/apis/console/console_openapi.yaml
```

Every account, root or scope, uses this one spec.

### 5. Add the agents (optional)

`nf doctor` checks every agent that Console lists for the account, so it needs no entries. To query an agent through `DataSource` by name, add it to a data file:

```toml
[settings]
type = "data"

[connectors.agent1]
ip = "192.0.2.30"
# agent_id = "<agent id ending in 'clients'>"
```

Without `agent_id`, the agent is found by name in the OCCM cache, so run `nf cache occm refresh` first. See [Config schema: Connectors](../reference/config-schema.md#connectors).

## Check it worked

`nf config validate` checks the root account. Check a scope's account with `--scope`:

```bash
nf config validate --scope bu1
```

```
├── Scope settings (bu1)
│   ├── Monitoring: Not configured (optional)
│   └── Console
...
Configuration is valid
```

Then the live check. For each account it gets a token, lists the account's organizations, and sends one read-only request to each active agent:

```bash
nf doctor --api console
```

The output below comes from a working setup with service accounts in two scopes, `bu1` and `bu2`, and no root account. It is shortened to the first agents of each scope, and it exits 0:

```
nf doctor
...
├── Config: Spec Files
│   └── Console spec
├── SOPS
│   ├── sops is installed
│   ├── age key: key file ~/.sops/age/keys.txt
│   ├── scope.bu1.consoleapi.general.client_secret: decrypts
│   └── scope.bu2.consoleapi.general.client_secret: decrypts
...
└── Console (live)
    ├── bu1: token works, 1 organization(s)
    ├── bu1/org1/agent2: reachable
    ├── bu2: token works, 1 organization(s)
    └── bu2/org2/agent3: inactive in Console; not
        probed
        └── Start the agent in Console, then re-run.
```

Rows are named `<account>/<organization>/<agent>`, where the account is the scope name, or `root` for the root account. An agent that is stopped in Console is skipped with a warning rather than probed. With clusters in the inventory, a `Console clusters` section also reports how many of each account's clusters match Console by name.

## If it fails

| `nf config validate` or `nf doctor` shows | Cause | Fix |
| :--- | :--- | :--- |
| `No Console account configured` | No root account with credentials, and no scope with a `consoleapi.toml` | Add the settings from step 2. For a scope, check that its directory has `scope.toml`. |
| `Unknown scope 'bu1'` | The directory has no `scope.toml` marker | Add `<config>/bu1/scope.toml`; it may be empty. |
| `client_id and client_secret must be set together` | Only one of the two is set | Store the secret as in step 3. |
| `Console spec: missing` | `<config>/apis/console/console_openapi.yaml` does not exist | `nf config download-spec --api console` |
| `bu1: HTTP 401` | Console rejected the credentials | Check `client_id`, and store the secret or refresh token again. |
| `bu1: unreachable (ConnectionError)` | The network path or a proxy blocks `base_url` | Check DNS, routing and any proxy. |
| `bu1/org1/agent1: inactive in Console; not probed` (warning) | The agent is stopped in Console | Start the agent in Console, then re-run. |
| `bu1/org1/agent1: HTTP <code>`, other than 401 or 403 | `nf` reaches an agent through Console (`base_url`, with the agent id in a header), so this is Console reporting that the request to the agent failed | Check in Console that the agent is running and connected, then re-run. |
| `<field>: SOPS value does not decrypt (SOPSError)` | The key cannot decrypt the stored secret | See [SOPS: If it fails](sops-secrets.md#if-it-fails). |

## Next

- [Console Agent](../usage/console-agent.md): call Console and its agents from Python
- [Config schema: Scopes](../reference/config-schema.md#scopes)
- [Add an ONTAP cluster and validate it](add-ontap-cluster.md)
