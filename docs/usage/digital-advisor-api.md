---
title: Digital Advisor API
description: Query Active IQ Digital Advisor with DigitalAdvisorAPIClient
audience:
  - users
tags:
  - digitaladvisor
  - api
  - graphql
---

# Digital Advisor API

`DigitalAdvisorAPIClient` runs read-only GraphQL queries against Active IQ Digital Advisor (`https://gql.aiq.netapp.com/graphql`). It does not use the OpenAPI layer: Digital Advisor publishes no OpenAPI file, and NetApp is phasing its REST API out. REST is used for one thing only, the token refresh.

## Setup

- **Settings:** `<config>/apis/digitaladvisor/digitaladvisorapi.toml` with a `[general]` section (see [Config schema: digitaladvisorapi.toml](../reference/config-schema.md#digitaladvisorapitoml) and `docs/example-config/apis/digitaladvisor/digitaladvisorapi.toml`).
- **Credentials**, one or both (the PAT is used first):
    - a **personal access token** (valid 1-90 days, no refresh): `nf config set-credential --setting digitaladvisorapi.personal_access_token`;
    - a **refresh token**: `nf config set-credential --setting digitaladvisorapi.refresh_token`. The client gets the access token itself. With both set, the refresh token backs up the PAT.
- **Check:** `nf config validate` shows a "Digital Advisor API" row. `nf doctor --api digitaladvisor` sends one read-only query to prove the token. With a refresh token it refreshes and writes the rotated tokens back only when the stored access token is missing, expired or rejected. With both credentials a rejected PAT gives a WARNING with a PAT renewal hint when the refresh token works.

## Queries

```python
from pynetappfoundry.clients.digitaladvisor import DigitalAdvisorAPIClient
from pynetappfoundry.core.config import Config

client = DigitalAdvisorAPIClient(Config(config_dir="config"))

data = client.query("query { __typename }")
```

`query(document, variables=None)` returns the response's `data`. An unknown id comes back as `data.<field> = None`, which is returned, not raised. A document the server rejects (HTTP 400, `GRAPHQL_VALIDATION_FAILED`) raises `DigitalAdvisorQueryError`, which carries the error codes and messages (never variables or tokens).

`paginate(document, variables, connection, records_key, page_size=None)` follows the cursor of a connection. The document must declare `$pageSize` and `$after` and pass them to the connection. It stops on an empty page, when the record count reaches `totalCount` (`clusters` has none), on an empty or repeated cursor, or after 1000 pages (it logs an error then).

### Typed methods

- `list_systems(*, product_types, system_states, include_all_states, include_storage_grid_nodes, filters=None, fields=None)`
- `list_volumes(*, filters=None, fields=None)`

They return plain dicts. The default selection is the scalar fields the service was probed for. `fields` replaces it; each name must be a plain GraphQL name, otherwise `ValueError`. `filters` accepts only the filter names the service listed. The GraphQL types of the `volumes` filters (and the `$pageSize: Int` and `$after: String` variables) are inferred from their names; a wrong one comes back as a `GRAPHQL_VALIDATION_FAILED` error. The enum values for `product_types` and `system_states` are not built in: look them up in the [schema](#schema).

There is no `list_clusters`; clusters are served by the [DataSource](#datasource) backend.

## DataSource

`DigitalAdvisorCluster`, `DigitalAdvisorSystem` and `DigitalAdvisorVolume` (in `src/pynetappfoundry/models/digitaladvisor/`) are served by the live-only Digital Advisor backend ([ADR-0037](../decisions/0037-digital-advisor-backend-is-live-only-and-generates-curated-graphql-selections-from-its-models.md)). There is no cache: `source="auto"` goes live and `source="cache"` raises `ValueError`.

```python
from pynetappfoundry.data import DataSource
from pynetappfoundry.models.digitaladvisor import DigitalAdvisorSystem

ds = DataSource(config)
for system in ds.query(DigitalAdvisorSystem, cluster="digitaladvisor").filter(clusterId="<cluster id>"):
    print(system.hostName, system.site.city if system.site else None)
```

- `cluster=` is only a label: there is one account in `digitaladvisorapi.toml`, so any value works and it is not used for targeting.
- **Query arguments.** A `.filter()` key that names a root-query argument is sent to the service as a typed GraphQL variable. `systems` and `clusters` accept `customerId`, `siteId`, `clusterId`, `watchlistId` and `clusterIds`; `volumes` accepts `clusterId`, `vserverId` and `aggregateId`. `systems` also accepts `operatingMode` (`[SystemOperatingMode!]`, values `SEVEN_MODE` and `CLUSTER_MODE`), and both `systems` and `clusters` accept `platformTypes` (`[SystemPlatformType!]`, for example `["ONTAP"]`). For `systems` the service argument is named `platformType`; the filter key is `platformTypes` because `platformType` is a field of the System record, and `.filter(platformType="ONTAP")` stays an in-memory equality filter on that field. Both take a list of enum values.
- **`systems` defaults.** The service requires four arguments. The backend sends `productTypes=["FILER"]`, `systemStates=["ACTIVE"]`, `includeAllStates=False` and `includeStorageGridNodes=False`. These defaults are chosen, not measured: how `includeAllStates` interacts with `systemStates` is not known. Override any of them with `.filter(systemStates=["ACTIVE", "INACTIVE"])`.
- **In-memory filters.** Any other key is an equality filter on a dotted path of the record, for example `.filter({"site.city": "Example City"})`. A top-level key that is neither a query argument nor a model field raises `ValueError` before any request. `ds.get(..., id=...)` filters the listed records in memory: by `id` for clusters and volumes, by `serialNumber` for systems.
- **Curated fields, no personal data.** The models hold the scalar fields and the nested objects chosen for them, and the selection sent to the service is generated from those models. Contact people (`contactPerson`, `salesRepresentative`, `csm`, `retentionSpecialist`, `solutionEngineerSpecialist`, `sam`) and a site's `streetAddress` and `postalCode` are never requested, and the backend refuses to select them. Unbounded lists such as a cluster's `systems`, `vservers` and `shelves` are out of scope.
- `.fields("hostName")` narrows the selection to those top-level fields, plus the identifier field and the fields you filter on in memory. A nested object comes with its whole curated sub-selection.
- Dates are kept as strings: the wire format was not measured. A field the service returns as a number (a GraphQL `Float`) is a Python `float`.
- Client errors, such as `DigitalAdvisorQueryError` for a rejected query, are raised unchanged.

## Token rotation

With a refresh token the client keeps the access token (a JWT valid for one hour) fresh. It reads only the `exp` claim, without verifying the signature, and refreshes 60 seconds before it. If `exp` cannot be read, it uses the token until the server answers `UNAUTHENTICATED`; it then refreshes once and retries once. Claims and tokens are never logged.

Every refresh returns a **new refresh token**. The client writes both new tokens back to `digitaladvisorapi.toml` `[general]` in one atomic write that keeps comments. They are SOPS-encrypted when the stored `refresh_token` is, and plain text otherwise. If the write fails, the client logs an error naming the file and the exception type, and the call goes on with the in-memory tokens. The next run then starts from the older stored token.

Refreshing works for 90 days from the portal login. After that the refresh fails with a `DigitalAdvisorAuthError` that says so: log in to the portal again and store the new token with `set-credential`.

Limitation: two processes that refresh at the same moment are not coordinated, and the later write wins.

A personal access token is used as is. When the server rejects it, `DigitalAdvisorAuthError` says it has probably expired.

### PAT with a refresh-token fallback

With both `personal_access_token` and `refresh_token` set, the PAT is sent first. A working PAT means no token request and no config write. When the server rejects the PAT, the client logs one warning (names only, no token) and switches to the refresh pair for the rest of its life. That path works as in refresh-only mode: the stored access token first, then a refresh and write-back only if it is missing, expired or rejected. A query sends at most three GraphQL requests. If both fail, `DigitalAdvisorAuthError` names the renewal step for each credential.

## Rate limit and retries

The service allows 300 requests per 5 minutes per IP and sends no rate-limit headers. The client keeps a sliding window of 300 requests per 300 seconds. A 429, 502, 503, 504 or connection error is retried up to 5 times with exponential backoff (5 s, doubling, at most 120 s); a `Retry-After` header is honoured. The last failure raises `DigitalAdvisorError`. A 400 is never retried.

## Read only

`ensure_read_only` runs before any request and rejects a `mutation` or `subscription`. Digital Advisor's schema has mutations (creating and revoking tokens); the client never sends them.

## Schema

```bash
nf config download-schema
```

downloads the GraphQL schema by introspection, with no credentials, to `<config>/apis/digitaladvisor/schema.json`. No NetApp schema ships with the package. The client does not read the file at run time: it is reference data for writing queries and for the `DataSource` backend. The server validates every query itself. See [CLI Reference](../reference/cli.md#config).

See also [ADR-0036](../decisions/0036-digital-advisor-client-is-a-read-only-graphql-client-with-rotating-refresh-token-write-back.md).
