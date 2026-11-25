---
title: Set Up the DII API
description: Connect to Data Infrastructure Insights with a read-only token, add tenants, and add the optional read-write key
audience:
  - users
tags:
  - how-to
  - configuration
  - dii
---

# Set Up the DII API

**Goal:** connect `nf` to a Data Infrastructure Insights (DII, formerly Cloud Insights) tenant with a read-only API token. Then optionally add more tenants and a read-write key for writes.

## Before you start

- A config directory, and SOPS set up if you want encrypted tokens: [Set up a config directory and SOPS secrets](sops-secrets.md).
- The tenant URL, such as `https://<tenant>.cloudinsights.netapp.com`.
- A DII API access token. `nf doctor` reads `/assets/storages/count`, so the token needs read access to the Assets API category.

## Steps

### 1. Add the DII API settings

Create `<config>/apis/dii/diiapi.toml`:

```toml
[general]
base_url = "https://tenant1.cloudinsights.netapp.com"
```

`base_api_path` defaults to `/rest/v1`. See [Config schema: diiapi.toml](../reference/config-schema.md#diiapitoml).

### 2. Store the read-only token

```bash
nf config set-credential --setting diiapi.api_ro_token
```

It prompts for the token without echoing it, encrypts it, and writes it to `diiapi.toml`:

```
Setting diiapi.api_ro_token stored
  File: config/apis/dii/diiapi.toml
  Table: general
  Key: api_ro_token
  Value: (encrypted)
```

### 3. Download the API spec

```bash
nf config download-spec --api dii
```

```
Wrote config/apis/dii/all.json
```

### 4. More than one tenant (optional)

With one tenant, steps 1 to 3 are enough. For several tenants, add each to a data file, such as `<config>/environments/tenants.toml`:

```toml
[settings]
type = "data"

[cloudinsights.tenant1]
ip = "tenant1.cloudinsights.netapp.com"
base_url = "https://tenant1.cloudinsights.netapp.com"
```

Then store each tenant's token. `--user` is only a label; the prompt takes the token:

```bash
nf config set-credential --type cloudinsights --name tenant1 --user token
```

A tenant without its own `base_url` or token uses the one in `diiapi.toml` `[general]`. Once a data file defines any tenant, `nf doctor` checks each tenant instead of `[general]`.

### 5. Add a read-write key (optional)

Reads only ever use the read-only token. Only DII writes need a separate read-write key. Store it for the `[general]` tenant:

```bash
nf config set-credential --setting diiapi.api_rw_token
```

Or for one tenant, as `rw_enc` on its entry:

```bash
nf config set-credential --type cloudinsights --name tenant1 --read-write
```

Which key a tenant uses:

- A tenant's own `rw_enc` always wins.
- A tenant with its own read-only token does not inherit the `[general]` read-write key.
- A tenant with no token of its own inherits both `[general]` keys.

## Check it worked

```bash
nf config validate
```

Among its lines:

```
│   ├── DII API
...
    └── DII spec

Configuration is valid
```

Then the live check. It sends one read-only `GET /assets/storages/count` per tenant, and repeats it with the read-write key when one is set:

```bash
nf doctor --api dii
```

The output below comes from a working setup with one tenant in `[general]` and a read-write key. It exits 0:

```
nf doctor
├── Config: Settings
│   └── DII API
├── Config: Spec Files
│   └── DII spec
└── DII
    ├── general: connected
    └── general read-write key: connected

Summary: 4 ok, 0 warning, 0 error, 0 skipped
```

With tenants in a data file, each tenant gets its own rows, named after the tenant instead of `general`. With no read-write key, the read-write row reports `not set` and is skipped, since the key is optional.

## If it fails

| `nf doctor` shows | Cause | Fix |
| :--- | :--- | :--- |
| `Cloud Insights 'tenant1' has no API token or base_url configured` | A tenant has neither its own token or `base_url` nor a `[general]` one | Store the token with `nf config set-credential --type cloudinsights --name tenant1 --user token`, and set `base_url` on the tenant or in `diiapi.toml`. |
| `DII spec: missing` | `<config>/apis/dii/all.json` does not exist | `nf config download-spec --api dii` |
| `tenant1: unreachable (ConnectionError)` | The `base_url` is wrong, or the network path or a proxy blocks it | Check `base_url`, DNS and any proxy. |
| `tenant1: HTTP 401` (error) | The tenant rejected the token | Store the token again. |
| `tenant1: HTTP 403` (warning) | The token is valid but lacks read access to the Assets API category | Give the token Assets read access in DII. |
| `tenant1 read-write key: HTTP 401` (error) | The read-write key was rejected | Store it again with the `--read-write` or `diiapi.api_rw_token` command above. |
| `tenant1 read-write key: HTTP 403` (warning) | The read-write key authenticated but cannot read Assets; a key scoped to write categories only does this | Expected for a write-only key. Otherwise, check its scopes. |
| `<field>: SOPS value does not decrypt (SOPSError)` | The key cannot decrypt the stored token | See [SOPS: If it fails](sops-secrets.md#if-it-fails). |

## Next

- [Add an ONTAP cluster and validate it](add-ontap-cluster.md)
- [Config schema: Cloud Insights](../reference/config-schema.md#cloud-insights): every tenant field
- [API Examples: DII API Client](../examples/api.md#dii-api-client): call DII from Python
