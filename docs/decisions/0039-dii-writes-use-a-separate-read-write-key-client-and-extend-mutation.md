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

Accepted. Implemented in issue #1003.

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

## Rationale

- **Key isolation over a runtime check.** A client that holds only the key it needs cannot send the wrong one, which extends ADR-0019 to DII. A "read client refuses writes" rule would break DII's read-style POSTs.
- **One write surface.** `Mutation` already resolves mappings by model class name, and DII mappings register under that name. A separate DII write class would copy body building, path translation and response parsing, and would leave infrafoundry#1377 with two surfaces. The differences are small: the item path, the update method, no polling, and the read-write requirement.
- **The spec decides the update method.** DII areas differ: annotations and datasources use PATCH, applications, monitors and rules use PUT. Reading the method from the spec avoids a table that goes stale.
- **Leaving out the body beats redacting by name.** Datasource credentials sit in `config.packages[].attributes` under names such as passwords, SNMP communities and keys. A name list is always incomplete, so non-GET bodies are not logged at all. Size-only logging for every method would remove today's GET debugging, and a per-call flag would change the `Query` call sites and their tests.
- **Cost.** The response bodies of read-style POSTs (`Query`, DII `/search`) are no longer logged at DEBUG; the URL and status still are.

## Consequences

- ADR-0015's read-only statement is narrowed: the DII backend and `DataSource` stay read-only, and writes are available through `Mutation` with a read-write client.
- Action and sub-resource endpoints (pause, resume, annotation values, application assets, datasource poll, test, clone and note), collection-level DELETE and the `preEncrypted` query parameter are not supported yet.
- `nf doctor --api dii` does not yet report whether a read-write key is configured.

## Related Issues

- Issue #1003: feat: add dii writes with a read-write api key
- infrafoundry#1377: one create / update / delete surface for both APIs

## Related Documentation

- [Query layer: DII writes](../usage/query-layer.md#dii-writes)
- [Config schema: diiapi.toml](../reference/config-schema.md#diiapitoml)
- [ADR-0015: DII API backend](0015-dii-backend-live-only-bare-array-envelope-offsetlimit-pagination.md) -- the read-only backend this extends
- [ADR-0019: Console runtime client architecture](0019-console-runtime-client-architecture-org-scoped-access-and-per-token-type-wrapper-isolation.md) -- per-token-type wrapper isolation
- [ADR-0036: Digital Advisor client](0036-digital-advisor-client-is-a-read-only-graphql-client-with-rotating-refresh-token-write-back.md) -- a read-only client precedent
