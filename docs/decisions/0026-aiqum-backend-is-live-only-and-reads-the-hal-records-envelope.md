---
title: "ADR-0026: AIQUM backend is live-only and reads the HAL records envelope"
description: The AIQUM DataSource backend is live-only, reads the HAL records envelope with link paging, and takes the instance from the cluster argument.
date: 2026-11-16
audience:
  - contributors
tags:
  - adr
---

# ADR-0026: AIQUM backend is live-only and reads the HAL records envelope

## Status

Accepted

## Context

Issue [#1049](https://github.com/endavis/pynetappfoundry/issues/1049) adds an AIQUM (Active IQ Unified Manager) backend to `DataSource`. AIQUM has no local cache database, and its list endpoints return a HAL envelope, `{_links, num_records, records, total_records}`, with `_links.next.href` paging. This was confirmed against an AIQUM 9.18 lab with read-only GETs: the volumes, SVMs and events endpoints all return that envelope, and the events endpoint pages (`total_records=24`, `_links.next` present). `docs/development/adding-backends.md` previously described an `_embedded.items` envelope, which is wrong.

## Decision

1. **`AiqumBackend` is live-only** and registered as `"aiqum"` in `_BACKENDS`. `source="auto"` goes live and `source="cache"` raises `ValueError` when `query()` is called. Cache-only routing decisions, `where()` and non-equality DSL operators are rejected.
2. **New `Backend.live_only` flag.** `QueryBuilder` reads it off the backend class: `auto` is routed as `live` (so no cache-miss second call), and `cache` is rejected at `query()` time. It is set on `AiqumBackend` and, since [#1052](https://github.com/endavis/pynetappfoundry/issues/1052), on `DiiBackend`.
3. **HAL `records` envelope.** Records are fetched with `AIQUMAPIClient.get_all_records`, which follows `_links.next.href`, and read at `mapping.records_path` (`"records"`). A mapping with `response_shape="singleton"` is fetched with `call_endpoint` and the dict is wrapped as `[response]`. Filters become query parameters.
4. **The `cluster=` argument is the `[aiqums]` instance name**, with one cached `AIQUMAPIClient` per name.
5. **Endpoints with `{placeholder}` segments take caller-supplied `path_params`** ([#1054](https://github.com/endavis/pynetappfoundry/issues/1054)). `AiqumBackend` sets `supports_path_params = True` and reuses the DII validation and encoding rules from the shared `src/pynetappfoundry/data/_path_params.py`: an unknown key, a missing placeholder, or an empty, `.` or `..` value raises `ValueError` before any client is built, and each value is `str()`-ed and percent-encoded with `quote(text, safe="")`. Without `path_params`, a placeholder mapping that has a `parent_mapping` is fetched once per parent ([#1057](https://github.com/endavis/pynetappfoundry/issues/1057)): the parent mapping is queried live on the same instance (unfiltered unless `parent_filters` is given, see below), then one singleton `call_endpoint` per parent with its `key` percent-encoded into `path_params`, and filters go to the child requests only. The loop is the shared `src/pynetappfoundry/data/_per_parent.py` `fetch_per_parent`, also used by `DiiBackend`. A parent without a `key` is skipped (`SKIP_PARENT`), a failing child request is logged as `CHILD_FETCH_FAILED` and skipped, and a parent query error propagates. `AIQUMAPISettings.max_parent_requests` (`aiqumapi.toml [general]`, default 500, `0` = unlimited) caps the child requests: more parents raises `ValueError` before any child request, telling the caller to pass `path_params` or raise the cap. A placeholder mapping with no `parent_mapping` still raises `ValueError` naming the placeholder. The generated placeholder mappings are the ten `{key}/metrics` singletons; the codegen single-object rule means there is no mapping for `/datacenter/storage/volumes/{key}`. The parents can be filtered with `ds.query(..., parent_filters={...})` ([#1061](https://github.com/endavis/pynetappfoundry/issues/1061)): a new `Backend.supports_parent_filters` flag (`True` on AIQUM) and a keyword-only `parent_filters` argument on `AiqumBackend.query` (the abstract `Backend.query` signature is unchanged). The values become query parameters on the parent collection request, `max_parent_requests` applies to the filtered parents, and `{"key": k}` takes the item route of item 7. `parent_filters` with `path_params`, on a mapping that is not per-parent, or on a backend without the flag raises `ValueError`. Lab probes (AIQUM 9.18, read-only) show the parent collection narrows server-side (`cluster.name`, `svm.name`), `name` matches exactly with `*` as a wildcard, and an unknown parameter returns 400. The child `{key}/metrics` endpoint ignores undeclared query parameters (200 with full data), so `.filter()` keys it does not declare have no effect; use `parent_filters` to narrow parents. No code rejects such child keys.
6. **Models come from the generator.** `models/aiqum/**` and `cache/aiqum/**` are generated from the 9.18 spec with `doit generate_models --api=aiqum`, and `aiqum` is part of the `generate_models_check` drift check. The codegen single-object rule applies to `aiqum` as well as `ontap`, and a field key that starts with a digit gets an `n` prefix on the Python attribute (`n95th_percentile`) while `api_path` keeps the original key.
7. **A single-key lookup is fetched from `<collection>/{key}`** ([#1060](https://github.com/endavis/pynetappfoundry/issues/1060)). Codegen has no mapping for the item endpoints: `_deduplicate_endpoints` folds `<collection>/{key}` into the collection module (the module path drops `{...}` segments) and the collection envelope wins the tie-break over the single-object response, while `_build_identifier_map` still sets `identifier_field="key"` on the collection mapping. `AiqumBackend.query()` routes to `<collection>/{key}` when the endpoint has no placeholders, no `path_params` are given, the filters are exactly `{identifier_field: <str>}` with a value that is not `""`, `.` or `..`, and the client's runtime spec (`client.api_spec`) has a GET operation for that path. No `TypeMapping` field is added. The key is `quote(v, safe="")`-encoded, the bare object is wrapped as `[response]`, a 404 gives no record (`get()` returns `None`), and any other HTTP error propagates. Anything else falls through to the collection request. Per-object singleton mappings were rejected: they collide with the collection on module path, duplicate 25 identical models, risk renaming existing `Aiqum*` classes through shared-schema detection, and `get()` would still not use them. `?key=` stays the path for the 24 collections that declare a key filter, but the three that do not (`/admin/datasources/clusters`, `/storage-provider/access-endpoints`, `/storage-provider/active-directories-mappings`) may return the wrong record through it, which the item route avoids.

## Rationale

- A live-only backend matches the facts: nothing in AIQUM is cached by this package, so routing through the cache would only produce a pointless first miss.
- A class-level flag keeps the routing rule in one place instead of one special case per backend.
- Reusing `get_all_records` means paging needs no AIQUM-specific code.
- Generating the models keeps them in step with the spec, as for ONTAP and DII.
- Per-parent fetching reuses the DII loop rather than a second copy, so skip and log behaviour stay identical. The cap defaults to 500 because lab calls to `{key}/metrics` returned 200 in about 5 to 27 ms each (AIQUM 9.18, read-only), so the cap exists to stop an accidental unbounded fan-out, not to ration normal use.
- Keeping `quote(str(v), safe="")` for AIQUM matches DII and cannot change the requested path. It was checked against an AIQUM 9.18 lab with read-only GETs: a real volume key (90 characters, containing `,`, `-`, `:` and `=`) returned 200 from `GET /api/datacenter/storage/volumes/{key}/metrics` with the keys `_links`, `duration`, `end_time`, `num_samples`, `samples`, `start_time`, `summary` and `volume`, in all four forms tried: fully encoded (`safe=""`), raw, `safe=":=,"`, and encoded plus `?interval=1h`. The server accepts all of them, so there is no reason to loosen the encoding.
- The item route was checked against an AIQUM 9.18 lab with read-only GETs. `GET <collection>/{quote(key, safe="")}` returns 200 with a bare object (no `records` envelope) whose `key` equals the request, for volumes, SVMs and clusters. A well-formed nonexistent key and a garbage key (`volumes/garbage`) both return 404 with `{"error": {"code", "message", "target"}}`. `GET volumes?key=<nonexistent>` returns 200 with 0 records, so the item route gives a clearer miss. Keys contain `,`, `-`, `:` and `=`, so encoding is required.

## Consequences

- An AIQUM collector (cache population) is deferred to [#1055](https://github.com/endavis/pynetappfoundry/issues/1055).
- Per-parent fetching for AIQUM placeholder mappings ([#1057](https://github.com/endavis/pynetappfoundry/issues/1057)) costs one request per parent plus the parent query, bounded by `max_parent_requests`. Filtering the parents (to fetch metrics for a subset without `path_params`) is done with `parent_filters` ([#1061](https://github.com/endavis/pynetappfoundry/issues/1061)).
- DII tenant wiring is [#1053](https://github.com/endavis/pynetappfoundry/issues/1053).
- [ADR-0015](0015-dii-backend-live-only-bare-array-envelope-offsetlimit-pagination.md) section 1 contradicted the code for `auto`; [#1052](https://github.com/endavis/pynetappfoundry/issues/1052) corrected it and applied `live_only` to DII.

## Related Issues

- Issue [#1049](https://github.com/endavis/pynetappfoundry/issues/1049): add an AIQUM DataSource backend
- Issue [#1052](https://github.com/endavis/pynetappfoundry/issues/1052), [#1053](https://github.com/endavis/pynetappfoundry/issues/1053), [#1054](https://github.com/endavis/pynetappfoundry/issues/1054), [#1055](https://github.com/endavis/pynetappfoundry/issues/1055), [#1057](https://github.com/endavis/pynetappfoundry/issues/1057): follow-ups
- Issue [#1054](https://github.com/endavis/pynetappfoundry/issues/1054): AIQUM DataSource path parameters
- Issue [#1057](https://github.com/endavis/pynetappfoundry/issues/1057): AIQUM per-parent fetch for `{key}/metrics` mappings
- Issue [#1060](https://github.com/endavis/pynetappfoundry/issues/1060): fetch single AIQUM objects by key
- Issue [#1061](https://github.com/endavis/pynetappfoundry/issues/1061): AIQUM parent filtering for per-parent metrics queries

## Related Documentation

- [AIQUM API](../usage/aiqum-api.md)
- [Adding a New API Backend](../development/adding-backends.md)
- [DataSource User Guide](../usage/data-source.md)
- [ADR-0013: DataSource as a Thin Facade](0013-datasource-as-a-thin-facade-over-the-collector.md)
