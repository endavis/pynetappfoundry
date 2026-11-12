---
title: "ADR-0015: DII backend: live-only, bare-array envelope, offset/limit pagination"
description: Add a live-only DII backend to the DataSource framework that parses DII's bare-array response envelope and offset/limit pagination directly, with no local cache.
date: 2026-04-16
audience:
  - contributors
tags:
  - adr
---

# ADR-0015: DII backend: live-only, bare-array envelope, offset/limit pagination

## Status

Accepted

## Decision

Add a DII (Data Infrastructure Insights) backend to the DataSource framework. DiiBackend is a live-only backend: all queries hit the DII REST API directly with no local cache database. Four design points distinguish it from OntapBackend:

1. **Live-only operation.** DII has no cache substrate. Cache-only routing decisions raise `NotImplementedError`. The `source="auto"` and `source="live"` modes both go through the live API; `source="cache"` is unsupported.

2. **Bare-array response envelope.** DII endpoints return bare JSON arrays (not the `{"records": [...]}` envelope ONTAP uses or the `{"_embedded": {"items": [...]}}` HAL format). DiiBackend calls `call_endpoint()` directly and iterates the array, parsing each record via `parse_api_record()`. `TypeMapping.records_path` is set to `""` (empty string) for all DII mappings except those amended below (#918).

3. **Offset/limit pagination.** DII uses `offset` + `limit` query parameters for pagination, not ONTAP's `_links.next.href` HAL convention. The DII API client handles pagination at the client layer.

4. **Deferred `where_expressions`.** SQL-like cache filter expressions are not supported since there is no cache. As of issue #618, the public `QueryBuilder` surface rejects `.where()` and non-equality typed DSL operators with `ValueError` at chain time; `DiiBackend.query()` still raises `NotImplementedError` if `where_expressions` is passed directly. See [ADR-0017](0017-where-expressions-are-cache-only-rationale.md) for the rationale behind the cache-only restriction.

The full DII surface (191 endpoints) is generated via the existing OpenAPI codegen pipeline (ADR-0008), producing 191 model files under `models/dii/` and 191 mapping files under `cache/dii/`. DiiBackend is registered in `_BACKENDS` under the key `"dii"`, consistent with the backend registry pattern from ADR-0013.

## Rationale

DII is the first non-ONTAP backend in the DataSource framework. It validates the multi-API generalization from ADR-0006 and the backend registry design from ADR-0013. A live-only backend is the simplest starting point: it avoids cache schema migrations, derived-field hooks, and partial-fetch merge logic. Cache support can be added later if DII data proves stable enough to snapshot.

The bare-array envelope is a DII-specific quirk that the existing `parse_api_response()` function does not handle (it expects a dict with a `records_path` key). DiiBackend bypasses it by calling `call_endpoint()` and iterating the raw array. This is a pragmatic choice that avoids complicating the shared response parser with a special case for empty `records_path`.

## Amendment (#915): envelope responses

Some DII endpoints (`/lake/query/...`, `/monitors/alerts/query`) return an envelope `{offset, count, limit, <records>}` instead of a bare array.

- **Detection** is by content, not endpoint: a dict with `offset`, an integer `count` and exactly one list under `rows`, `results` or `values` (`extract_envelope_records()` in `src/pynetappfoundry/clients/dii/api.py`).
- **Return contract:** on the paging path `get_all_pages` returns the concatenated records list and drops the envelope metadata. With a caller-supplied `offset`/`limit`, or an endpoint that does not paginate, it returns the raw envelope; `DiiBackend.query()` extracts the records from it.
- **Stop rule:** stop when `offset + len(records) >= total`, where total is `objectCount`, else `count`. Both are totals (spec description and a live check, 2026-11-09). Fallbacks are an empty page, a short page when no total exists, and `DII_MAX_PAGES`. A short page alone does not stop the loop when a total exists, because the server may clamp the page size.
- **The offset advances by `len(records)`**, so a clamped page skips nothing.
- **HTTP errors propagate** rather than being swallowed, for example the alert `offset` ceiling of about 1,500 noted in the NetApp MCP docs.
- `sort` must appear in `tags`/`metrics`; that is the caller's concern.

## Amendment (#918): records_path

Four generated mappings set a non-empty `records_path`, and `DiiBackend` ignored it, so `/users` (`{"users": [...]}`) and `/users/invites` (`{"invites": [...]}`) returned `[]`.

- **Branch order in `DiiBackend.query()`:** a bare list is used as-is, even when `records_path` is set; `None` yields no records; a dict with a non-empty `records_path` has its records read from that path; otherwise the envelope check (`extract_envelope_records()`) runs; anything else logs the "unexpected response type" warning and returns `[]`. An explicit `records_path` is checked before content sniffing, which stays the fallback for `records_path=""`.
- **Path syntax:** `get_nested_value()` from `src/pynetappfoundry/utils/dict_path.py`, so dotted paths work.
- **Failure mode:** if the path is missing or does not resolve to a list, the backend logs a WARNING naming the mapping and `records_path`, and returns `[]`. No exception is raised.
- **Mappings:** `/users` (`users`) and `/users/invites` (`invites`) are wrapper responses and now return populated records.
- **`au/*` mappings:** `/au/oneTimeToken` and `/au/installCommand/{platform}` return a single `InstallCommand` object. Codegen picked its first array property (`additionalInstructionsForManualInstallation`) as `records_path`, so these mappings now return `ExtraInstallInstruction` records and omit fields such as `token` and `installCommand`. This codegen artifact is fixed by the #919 amendment below.

## Amendment (#919): single-object responses (`records_path = "."`)

`GET /au/oneTimeToken` and `GET /au/installCommand/{platform}` return one `InstallCommand` object, not a record list.

- **Sentinel:** `records_path = "."` means the whole dict response is one record. It is DII-only and not part of the shared `TypeMapping` contract. `DiiBackend.query()` checks it before the non-empty `records_path` branch and returns `[response]`. A list response keeps list behaviour. Mappings with `records_path=""` and named paths behave as before.
- **Codegen:** `_SINGLE_OBJECT_ENDPOINTS` in `tools/codegen/adapters.py` lists the two paths for `api_type="dii"`. For them the model is generated from the whole `InstallCommand` schema (`token`, `installCommand`, `imageZipUrl` and so on, with `additionalInstructionsForManualInstallation` as a nested list). `_detect_records_path` and every other endpoint are unchanged.
- **ONTAP (#925):** ONTAP single-object responses use the shared `TypeMapping.response_shape = "singleton"`, set by an api_type codegen rule. DII keeps the `"."` sentinel.

## Amendment (#935): single-object responses use `response_shape`

The #919 `records_path = "."` sentinel is replaced by the shared `TypeMapping.response_shape = "singleton"` that ONTAP has used since #925.

- **Codegen:** `_SINGLE_OBJECT_ENDPOINTS` in `tools/codegen/adapters.py` now sets `response_shape="singleton"` for the two DII paths. `generate_mapping` omits `records_path` for them, so the default `"records"` applies.
- **Backend:** `DiiBackend.query()` branches on `mapping.response_shape == "singleton"` and returns `[response]`. The branch order is: list, `None`, dict with `singleton`, dict with a non-empty `records_path`, envelope, warning. The singleton branch must precede the `records_path` branch, because the default `records_path="records"` would otherwise route the dict to the named-path lookup and return `[]`.
- **Removed:** the `"."` sentinel constant in `src/pynetappfoundry/data/dii_backend.py` and its copy in `tools/codegen/adapters.py`. It was added after `v0.1.0` and never released.

## Amendment (#985): placeholder endpoints are fetched per parent or rejected

`DiiBackend.query()` used to send `mapping.api_endpoint` as is, so a mapping with `{id}` in its path requested a literal `/assets/fabrics/{id}/ports`.

- **Wired mappings** (those with `parent_mapping`): the parents come from a recursive `DiiBackend.query` of the parent mapping, after `validate_parent_chain` has checked the chain. `get_all_pages` then runs once per parent with the endpoint template and `path_params`, so spec-driven pagination and validation still apply. `get_all_pages` and `_page_envelope` forward `path_params` to every `call_endpoint`. `iter_parent_ids` (new in `src/pynetappfoundry/cache/fetchers.py`, shared with `iter_parent_urls`) resolves the identifiers, skipping a parent without one (`SKIP_PARENT`); a failing parent is logged as `CHILD_FETCH_FAILED` and skipped.
- **Unwired mappings** (a placeholder, no `parent_mapping`): `query()` raises `ValueError` naming the placeholder(s). No client is built and nothing is requested. The codegen declines to wire these on purpose, because DII lacks the parent collection endpoints; supplying their values is separate work.
- No request is ever made with `{` or `}` in the path.

## Related Issues

- Issue #600: feat: add DII API backend to DataSource
- Issue #893: bug: DII backend fetches only the first page (offset/limit pagination in DIIAPIClient.get_all_pages)
- Issue #915: bug: DII envelope endpoints (lake/query, alerts) return empty from DiiBackend and are not paged
- Issue #918: bug: DiiBackend ignores records_path, so /users and /users/invites return empty
- Issue #919: codegen models single-object responses as their first array property
- Issue #925: ONTAP single-object responses use `TypeMapping.response_shape` via a codegen rule; DII kept `"."` until #935
- Issue #935: refactor: replace DII `records_path="."` sentinel with `response_shape="singleton"`
- Issue #985: bug: DiiBackend live queries request endpoints with unfilled path placeholders
- Issue #533: feat: DataSource non-ONTAP backends (partially addressed; DII is the first non-ONTAP backend)
- Issue #618: feat: early validation for where()/typed-DSL + incompatible source mode

## Related Documentation

- [ADR-0006: Generalize field mapping for multi-API](0006-generalize-field-mapping-for-multi-api.md) -- multi-API TypeMapping generalization that DII relies on
- [ADR-0008: OpenAPI codegen for model generation](0008-openapi-codegen-for-model-generation.md) -- codegen pipeline that generated the 191 DII models and mappings
- [ADR-0013: DataSource as a Thin Facade](0013-datasource-as-a-thin-facade-over-the-collector.md) -- backend registry and routing architecture
- [ADR-0017: where-expressions are cache-only (rationale)](0017-where-expressions-are-cache-only-rationale.md) -- rationale for the cache-only restriction on `.where()` and non-equality typed DSL operators
- [Adding a New API Backend](../development/adding-backends.md) -- developer guide updated with DII-specific section
