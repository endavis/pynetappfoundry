---
title: AIQUM API
description: Call Active IQ Unified Manager with AIQUMAPIClient
audience:
  - users
tags:
  - aiqum
  - api
---

# AIQUM API

`AIQUMAPIClient` calls the REST API of one Active IQ Unified Manager (AIQUM) instance, using Basic authentication and the OpenAPI spec `all.json` from the `aiqum` folder of the config's `apis` directory.

## Setup

- **Inventory:** add the instance to a data file as `[aiqums.NAME]` with an `ip` (see [Config schema: AIQUMs](../reference/config-schema.md#aiqums)).
- **Credentials:** put `user` and `enc` under `[aiqums]` in `users.toml` (see [Config schema: users.toml](../reference/config-schema.md#userstoml)).
- **Settings:** create `aiqumapi.toml` in the config directory with a `[general]` section (see [Config schema: aiqumapi.toml](../reference/config-schema.md#aiqumapitoml)). A missing `[general]` raises `ConfigurationError`.
- **Spec:** `all.json` in the `aiqum` folder of the `apis` directory (see `docs/example-config/apis/aiqum/notes.txt`).

## Usage

```python
from pynetappfoundry import AIQUMAPIClient, Config

config = Config(script_name="aiqum-demo")
client = AIQUMAPIClient("aiqum1", config)

# One page
clusters = client.call_endpoint("/datacenter/cluster/clusters")

# Every page: the HAL _links.next.href links are followed and records merged
all_clusters = client.get_all_records("/datacenter/cluster/clusters", "GET")
```

Write calls are not idempotent, and POST is retried by default. Turn retries off for them:

```python
from pynetappfoundry.core.models import RetryConfig

client.call_endpoint(
    "/admin/datasources/clusters",
    method="POST",
    body={"address": "10.1.1.1", "username": "admin", "password": "..."},
    retry_config=RetryConfig(enabled=False),
)
client.call_endpoint(
    "/admin/datasources/clusters/{key}",
    method="DELETE",
    path_params={"key": "<cluster-key>"},
    retry_config=RetryConfig(enabled=False),
)
```

Request bodies are sent unvalidated: the Swagger 2 `all.json` keeps bodies in `parameters[in=body]`, and body validation reads only OpenAPI 3 `requestBody`.

## TLS

The client turns certificate chain validation off and pins the instance's certificate fingerprint on first use, the same way `ONTAPAPIClient` does by default. CA validation (`verify_ssl`, `ca_bundle`) does not apply to AIQUM. See [Host identity](basics.md#host-identity-ssh-host-keys-and-tls-certificates).

## Spec gap

The published AIQUM spec omits `/management-server/admin/options`. Calls to it still work, unvalidated, and log a spec-lookup error. It needs `Content-Type: application/vnd.netapp.v1.hal+json`:

```python
client.call_endpoint(
    "/management-server/admin/options",
    additional_headers={"Content-Type": "application/vnd.netapp.v1.hal+json"},
)
```

`doit fetch_spec --api=aiqum` currently gets HTTP 401 from AIQUM 9.18, whose docs endpoint does not accept Basic auth. This is a follow-up item.
