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
5. **Endpoints with `{placeholder}` segments raise `ValueError`** before any client is built; they are not queryable yet ([#1054](https://github.com/endavis/pynetappfoundry/issues/1054)).
6. **Models come from the generator.** `models/aiqum/**` and `cache/aiqum/**` are generated from the 9.18 spec with `doit generate_models --api=aiqum`, and `aiqum` is part of the `generate_models_check` drift check. The codegen single-object rule applies to `aiqum` as well as `ontap`, and a field key that starts with a digit gets an `n` prefix on the Python attribute (`n95th_percentile`) while `api_path` keeps the original key.

## Rationale

- A live-only backend matches the facts: nothing in AIQUM is cached by this package, so routing through the cache would only produce a pointless first miss.
- A class-level flag keeps the routing rule in one place instead of one special case per backend.
- Reusing `get_all_records` means paging needs no AIQUM-specific code.
- Generating the models keeps them in step with the spec, as for ONTAP and DII.

## Consequences

- An AIQUM collector (cache population) is deferred to [#1055](https://github.com/endavis/pynetappfoundry/issues/1055).
- DII tenant wiring is [#1053](https://github.com/endavis/pynetappfoundry/issues/1053).
- [ADR-0015](0015-dii-backend-live-only-bare-array-envelope-offsetlimit-pagination.md) section 1 contradicted the code for `auto`; [#1052](https://github.com/endavis/pynetappfoundry/issues/1052) corrected it and applied `live_only` to DII.

## Related Issues

- Issue [#1049](https://github.com/endavis/pynetappfoundry/issues/1049): add an AIQUM DataSource backend
- Issue [#1052](https://github.com/endavis/pynetappfoundry/issues/1052), [#1053](https://github.com/endavis/pynetappfoundry/issues/1053), [#1054](https://github.com/endavis/pynetappfoundry/issues/1054), [#1055](https://github.com/endavis/pynetappfoundry/issues/1055): follow-ups

## Related Documentation

- [AIQUM API](../usage/aiqum-api.md)
- [Adding a New API Backend](../development/adding-backends.md)
- [DataSource User Guide](../usage/data-source.md)
- [ADR-0013: DataSource as a Thin Facade](0013-datasource-as-a-thin-facade-over-the-collector.md)
