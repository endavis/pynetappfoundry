---
title: "ADR-0039: DII writes use a separate read-write key client and extend Mutation"
description: DII writes go through a read-write DIIAPIClient that carries only the read-write key, and Mutation handles DII models with the item path and update method taken from the spec.
date: 2026-11-23
audience:
  - contributors
tags:
  - adr
---

# ADR-0039: DII writes use a separate read-write key client and extend Mutation

## Status

Accepted, amended by [#1185](https://github.com/endavis/pynetappfoundry/issues/1185)

Implemented in issue #1003; amended in #1185.

## Context

ADR-0015 defines the DII backend as read-only, with one credential, `api_ro_token`. Issue #1003 adds create, update and delete for five DII areas: `assets/annotations`, `assets/applications`, `monitors/monitors`, `monitors/rules` and `collector/datasources`. That needs a second credential, a write path, and a decision about where the write path lives.

Three constraints shape it:

- DII exposes read-style POSTs (`/search`, `/queries`, `/lake/query/*`, `/logs/query`, `/audit/query`), so a client cannot refuse every non-GET call to stay read-only.
- ADR-0019 keeps token types in separate wrappers so a client never holds a key it does not need.
- Datasource request bodies carry device credentials under vendor-specific attribute names, so no list of key names can find every secret in a body.

## Decision

1. **A separate read-write client.** `DIIAPIClient(config, name=None, *, read_write=False)` builds, with `read_write=True`, a client with its own session that carries only `api_rw_token`. The default client carries only `api_ro_token`. A write client without a configured key raises `DIIWriteTokenMissingError` at construction, before any request.
2. **`Mutation` is extended, not duplicated.** For a mapping with `api_type == "dii"`, `Mutation` requires a client whose `read_write` attribute is `True`, so passing the read client fails before any request. The check is duck-typed and `query/` does not import the client class. The DII item path (`<collection>/{id}` or `{dataSourceId}`) is read from `client.api_spec["paths"]`. `update` sends PATCH if the item path declares it, else PUT. `poll=True` is refused because DII has no jobs.
3. **Key resolution for named tenants.** The `[general]` `api_rw_token` belongs to the default tenant. A tenant with its own key gets no read-write key, and a tenant without one inherits both `[general]` keys. A separate read-write key per tenant is deferred.
4. **Write bodies and responses are not logged.** `APIWrapper` logs a response body at DEBUG only for GET and a byte count for other methods. Request-body and response validation errors name the failing validator and the JSON path of the field, never its value. The `X-CloudInsights-ApiKey` header is masked next to `Authorization`. `Mutation` debug lines log only the top-level body keys.
5. **`Mutation.call` for actions and sub-resources (#1185).** `Mutation(model, rw_client).call(method, path=None, *, path_params=None, body=None)` sends a POST, PUT, PATCH or DELETE at or below the model's endpoint and returns the raw response. The path must be in the spec and declare the method, placeholders must match `path_params` (values percent-encoded), POST has retry disabled, and DEBUG logs only the path template and a body description. ONTAP models are refused.
6. **Annotation request schemas are corrected in the client.** The spec declares a bare `{"type": "object"}` body for the 36 annotation value operations, but DII takes a JSON array. `DIIAPIClient._get_request_schema` substitutes an array schema, only while the spec still declares a bare object. `APIWrapper` accepts a list body.

## Rationale

- **Key isolation over a runtime check.** A client that holds only the key it needs cannot send the wrong one, which extends ADR-0019 to DII. A "read client refuses writes" rule would break DII's read-style POSTs.
- **One write surface.** `Mutation` already resolves mappings by model class name, and DII mappings register under that name. A separate DII write class would copy body building, path translation and response parsing, and would leave infrafoundry#1377 with two surfaces. The differences are small: the item path, the update method, no polling, and the read-write requirement.
- **The spec decides the update method.** DII areas differ: annotations and datasources use PATCH, applications, monitors and rules use PUT. Reading the method from the spec avoids a table that goes stale.
- **Leaving out the body beats redacting by name.** Datasource credentials sit in `config.packages[].attributes` under names such as passwords, SNMP communities and keys. A name list is always incomplete, so non-GET bodies are not logged at all. Size-only logging for every method would remove today's GET debugging, and a per-call flag would change the `Query` call sites and their tests.
- **Cost.** The response bodies of read-style POSTs (`Query`, DII `/search`) are no longer logged at DEBUG; the URL and status still are.
- **Alternatives to `Mutation.call` (#1185).** Named helpers per operation are typed, but 128 non-CRUD operations do not scale; they can be added on top of `call`. A model-free `DIIWriter(client).call(path, ...)` reaches every path but adds a second write surface, which this ADR rejects, and needs its own read-write guard. `Mutation.call` reuses the guard and keeps one surface, and every annotation target type already has a sub-resource model whose endpoint is the write path.

## Consequences

- ADR-0015's read-only statement is narrowed: the DII backend and `DataSource` stay read-only, and writes are available through `Mutation` with a read-write client.
- Remaining gaps: operations under no mapped model (`/lake`, `/logs`, `/dwh-management`, `/au/{auUuid}`, `/search`, `/query`, `/audit`), `.call` on ONTAP models, collection-level DELETE and the `preEncrypted` query parameter. Other bare-object request schemas whose payload may be an array are not checked.
- `nf doctor --api dii` reports the read-write key in its own row (#1186): skipped when unset, an error on a 401, a warning on a 403.

## Related Issues

- Issue #1185: feat: support DII action and sub-resource write endpoints in the mutation layer
- Issue #1186: `nf doctor --api dii` reports the read-write key
- Issue #1003: feat: add dii writes with a read-write api key
- infrafoundry#1377: one create / update / delete surface for both APIs

## Related Documentation

- [Query layer: DII writes](../usage/query-layer.md#dii-writes)
- [Config schema: diiapi.toml](../reference/config-schema.md#diiapitoml)
- [ADR-0015: DII API backend](0015-dii-backend-live-only-bare-array-envelope-offsetlimit-pagination.md) -- the read-only backend this extends
- [ADR-0019: Console runtime client architecture](0019-console-runtime-client-architecture-org-scoped-access-and-per-token-type-wrapper-isolation.md) -- per-token-type wrapper isolation
- [ADR-0036: Digital Advisor client](0036-digital-advisor-client-is-a-read-only-graphql-client-with-rotating-refresh-token-write-back.md) -- a read-only client precedent
