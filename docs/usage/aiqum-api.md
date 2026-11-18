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

- **Three collections can be cached; everything else is live only.** `AiqumCluster`, `AiqumSvm` and `AiqumVolume` are collected by `refresh_aiqum_cache(config, "aiqum1")` into `{config_dir}/.cache/aiqum_cache.db` (`AiqumCacheDB`). Collection is all or nothing per instance and replaces the previous snapshot. For those three models `source="cache"` reads the snapshot, `source="auto"` (the default) reads the snapshot and falls back to the live API when the cache returns nothing, and `source="live"` always queries the instance. Once an instance has been collected, `auto` returns snapshot data; use `source="live"` for current data. `AiqumCacheDB.is_stale("aiqum1")` reports snapshot age (30 days by default) but never affects routing. Every other model, including the metrics and per-parent models, is live only: `auto` queries the instance and `source="cache"` raises `ValueError` ([ADR-0026](../decisions/0026-aiqum-backend-is-live-only-and-reads-the-hal-records-envelope.md)).
- **The cache has CLI commands** ([#1072](https://github.com/endavis/pynetappfoundry/issues/1072)). `nf cache aiqum refresh INSTANCE` (or `--all` for every `[aiqums]` instance) collects and replaces the snapshot, continuing past a failing instance and exiting non-zero naming the failures. `nf cache aiqum status [--ttl DAYS]` lists each instance and mapping with its `cached_at` and Fresh, Stale, Not cached or Orphaned status. `nf cache aiqum clear INSTANCE|--all [-f]` deletes the snapshot after a confirmation prompt.
- **Cache filters match exactly.** On the cache path a `.filter()` value is compared as given, so the `*` wildcard of the live `name` filter does not apply. `.where()` and non-equality filters raise `ValueError`, and `path_params` and `parent_filters` cannot be combined with the cache.
- **Filters** become query parameters on the request.
- **Paging is automatic.** The `_links.next.href` links are followed and the `records` merged.
- **Endpoints with a `{placeholder}`** (the `{key}/metrics` models, such as `/datacenter/storage/volumes/{key}/metrics`) are queried with `path_params` (one request). Without it, a model with a parent (the `{key}/metrics` models) is fetched once per parent: the parent collection is queried on the same instance, unfiltered, then one request is sent per parent with its `key` percent-encoded, and *filters* go to those child requests only. The cost scales with the parent count, so more parents than `max_parent_requests` (`aiqumapi.toml`, default 500, `0` = unlimited) raises `ValueError` before any child request; pass `path_params` or raise the cap. A parent without a `key` is skipped (`SKIP_PARENT`) and a failing child request is logged as `CHILD_FETCH_FAILED` and skipped; an error on the parent query propagates. To narrow the parents, pass `parent_filters` to `query()` (see below). A placeholder model with no parent raises `ValueError` naming the placeholder ([#1057](https://github.com/endavis/pynetappfoundry/issues/1057)).

```python
from pynetappfoundry.models.aiqum.datacenter.storage.volumes.metrics.model import (
    AiqumVolumeMetricsSampleResponse,
)

metrics = ds.query(
    AiqumVolumeMetricsSampleResponse, cluster="aiqum1", path_params={"key": volume.key}
).filter({"interval": "1h"})
```

Each value is converted with `str()` and percent-encoded, so a key containing `,`, `:`, `=` or `/` is safe to pass as is. An unknown key, a missing placeholder, or an empty value, `.` or `..` raises `ValueError` before any request ([#1054](https://github.com/endavis/pynetappfoundry/issues/1054)).

#### Filtering the parents

`parent_filters` are query parameters for the parent collection request of a per-parent query, so metrics are fetched only for the matching parents. `.filter()` entries still go to the child requests only. `max_parent_requests` applies to the filtered parents.

```python
metrics = ds.query(
    AiqumVolumeMetricsSampleResponse,
    cluster="aiqum1",
    parent_filters={"svm.name": "vs1"},
).filter({"interval": "1h"})
```

- A value matches exactly; end it with `*` for a prefix match (`{"name": "vol*"}`). Without the `*`, a prefix returns no parents.
- An unknown parameter makes AIQUM return `400`, so a misspelled parent filter raises instead of fetching every parent.
- `parent_filters={"key": k}` takes the single-object route ([#1060](https://github.com/endavis/pynetappfoundry/issues/1060)): one parent request.
- `parent_filters` with `path_params`, or on a model that is not per-parent, or on a backend other than AIQUM, raises `ValueError` at `query()` time.
- Narrow the parents with `parent_filters`, not `.filter()`. The `{key}/metrics` endpoint ignores query parameters it does not declare (lab-verified on AIQUM 9.18: `?cluster.name=<bogus>` and `?not_a_param=x` both returned 200 with full data), so a `.filter({"cluster.name": ...})` on a metrics query has no effect ([#1061](https://github.com/endavis/pynetappfoundry/issues/1061)).

### Fetch one object by key

`get()` and a single `{"key": <value>}` filter fetch one object from `<collection>/{key}`, for example `/datacenter/storage/volumes/{key}`. This is one request, and the bare object comes back as a single instance. A key that does not exist returns `None`. Any other HTTP error is raised.

```python
volume = ds.get(AiqumVolume, cluster="aiqum1", id=volume_key)  # None if absent
same = ds.query(AiqumVolume, cluster="aiqum1").filter({"key": volume_key}).first()
```

The key is percent-encoded. The item route is used only when the instance's spec has a GET operation for it. With any other filter, a non-string value, an empty, `.` or `..` value, or `path_params`, the request goes to the collection as before ([#1060](https://github.com/endavis/pynetappfoundry/issues/1060)).

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
