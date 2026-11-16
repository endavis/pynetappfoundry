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
- **Credentials:** put `user` and `enc` on the instance (`nf config set-credential --type aiqums --name NAME --user USER`), or under `[aiqums]` in `users.toml` as the default for every instance (see [Config schema: Credential Resolution Order](../reference/config-schema.md#credential-resolution-order)).
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

## DataSource

The generated `Aiqum*` models (for example `AiqumCluster`, `AiqumSvm`, `AiqumVolume`, `AiqumDatasource`) can be queried through `DataSource`. `cluster=` is the key of the instance in the `[aiqums]` inventory:

```python
from pynetappfoundry.data import DataSource
from pynetappfoundry.models.aiqum.datacenter.storage.volumes.model import AiqumVolume

ds = DataSource(config)
volumes = ds.query(AiqumVolume, cluster="aiqum1").filter({"svm.name": "vs1"})
```

- **Live only.** AIQUM has no local cache. `source="auto"` (the default) and `source="live"` query the instance; `source="cache"` raises `ValueError`. `.where()` and non-equality filters raise `ValueError` ([ADR-0026](../decisions/0026-aiqum-backend-is-live-only-and-reads-the-hal-records-envelope.md)).
- **Filters** become query parameters on the request.
- **Paging is automatic.** The `_links.next.href` links are followed and the `records` merged.
- **Endpoints with a `{placeholder}`** (the `{key}/metrics` models, such as `/datacenter/storage/volumes/{key}/metrics`) are queried with `path_params` (one request). Without it, a model with a parent (the `{key}/metrics` models) is fetched once per parent: the parent collection is queried on the same instance, unfiltered, then one request is sent per parent with its `key` percent-encoded, and *filters* go to those child requests only. The cost scales with the parent count, so more parents than `max_parent_requests` (`aiqumapi.toml`, default 500, `0` = unlimited) raises `ValueError` before any child request; pass `path_params` or raise the cap. A parent without a `key` is skipped (`SKIP_PARENT`) and a failing child request is logged as `CHILD_FETCH_FAILED` and skipped; an error on the parent query propagates. Filtering the parents is not supported yet ([#1061](https://github.com/endavis/pynetappfoundry/issues/1061)). A placeholder model with no parent raises `ValueError` naming the placeholder ([#1057](https://github.com/endavis/pynetappfoundry/issues/1057)).

```python
from pynetappfoundry.models.aiqum.datacenter.storage.volumes.metrics.model import (
    AiqumVolumeMetricsSampleResponse,
)

metrics = ds.query(
    AiqumVolumeMetricsSampleResponse, cluster="aiqum1", path_params={"key": volume.key}
).filter({"interval": "1h"})
```

Each value is converted with `str()` and percent-encoded, so a key containing `,`, `:`, `=` or `/` is safe to pass as is. An unknown key, a missing placeholder, or an empty value, `.` or `..` raises `ValueError` before any request ([#1054](https://github.com/endavis/pynetappfoundry/issues/1054)).

The models are generated with `doit generate_models --api=aiqum`.

## TLS

By default the client turns certificate chain validation off and pins the instance's certificate fingerprint on first use, the same way `ONTAPAPIClient` does by default. An instance whose certificate is issued by a CA can opt into CA validation instead, with `verify_ssl` and `ca_bundle`. With validation on, nothing is pinned or recorded.

```toml
# in a data file, per instance
[aiqums.AIQUM-PROD]
ip = "192.168.1.150"
ca_bundle = "certs/internal-ca.pem"   # validate against this CA bundle
# verify_ssl = true                   # or validate against the default CA bundle

# config/apis/aiqum/aiqumapi.toml, default for every instance
[general]
# verify_ssl = true
# ca_bundle = "certs/internal-ca.pem"
```

Precedence, first match wins: the instance's `ca_bundle`, the instance's `verify_ssl`, the global `ca_bundle`, the global `verify_ssl`, then pin only. The rules are the same as for ONTAP clusters, and the ONTAP `verify_ssl` / `ca_bundle` keys do not affect AIQUM. A bad value raises `ConfigurationError` when the client is built, before credentials are read. See [CA validation](basics.md#ca-validation-optional) and [Host identity](basics.md#host-identity-ssh-host-keys-and-tls-certificates).

## Spec gap

The published AIQUM spec omits `/management-server/admin/options`. Calls to it still work, unvalidated, and log a spec-lookup error. It needs `Content-Type: application/vnd.netapp.v1.hal+json`:

```python
client.call_endpoint(
    "/management-server/admin/options",
    additional_headers={"Content-Type": "application/vnd.netapp.v1.hal+json"},
)
```

AIQUM 9.18 serves its spec only to a UI login session, not to Basic auth. `doit fetch_spec --api=aiqum` therefore logs in through the UI session (`POST /login`), downloads the spec, then logs out.
