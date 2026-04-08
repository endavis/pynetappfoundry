# ADR-0006: Generalize field mapping framework for multi-API data collection

## Status

Accepted

## Decision

Extend the declarative field mapping framework (ADR-0004) from ONTAP-only to multi-API by adding three changes to `TypeMapping`:

1. **`records_path: str = "records"`** — configurable dot-notation path to the records list in the API response envelope. Defaults to `"records"` (preserving ONTAP behavior). Supports nested paths like `"_embedded.items"` for APIs with deeper envelopes.
2. **`api_type: str = "ontap"`** — tag for routing to the correct API client and unit registry. Defaults to `"ontap"` (preserving existing behavior).
3. **`cli_command` made optional** — changed from required positional to `cli_command: str = ""`. Non-ONTAP APIs typically have no CLI equivalent.

The `parse_api_response()` function now uses `get_nested_value(response, mapping.records_path)` instead of `response.get("records", [])`, enabling it to extract records from any response envelope structure.

## Rationale

With DII, AIQUM, BlueXP, and StorageGrid planned as future data sources, the mapping framework needed to become API-agnostic so all APIs share the same declarative collection pattern. This avoids per-API SDK fragmentation and keeps a unified collection layer.

The changes are non-breaking — all existing ONTAP mappings work without modification because the new fields have defaults that preserve current behavior.

## Pagination Support

Issue #260 added `get_all_records()` to `APIWrapper`, enabling automatic pagination across all API types. The method uses a configurable `PaginationConfig` and pluggable `NextPageExtractor` callable, defaulting to ONTAP's `_links.next.href` HAL convention. This complements the field mapping framework by ensuring all records are collected before mapping is applied.

Issue #263 integrated `get_all_records()` into `MetadataCollector._cached_api_call()`, making pagination the default for all collection endpoints. A `paginate` keyword argument allows single-object endpoints (e.g., `/cluster`) to opt out.

## Related Issues

- Issue #263: feat: integrate get_all_records() into MetadataCollector._cached_api_call()
- Issue #260: feat: add configurable pagination support to APIWrapper
- Issue #259: feat: generalize field mapping framework for multi-API data collection
- Issue #258: feat: multi-API data collection strategy (superseded by #259)
- Issue #495: feat: unified DataSource for all cluster reads (ADR-0012 — builds on the multi-API generalization here by introducing a per-`api_type` backend registry)

## Related Documentation

- [Field Mapping Framework Developer Guide](../development/field-mapping.md)
- [ADR-0012: Unified DataSource accessor for all cluster reads](0012-unified-datasource-accessor.md) — introduces the per-`api_type` backend registry
