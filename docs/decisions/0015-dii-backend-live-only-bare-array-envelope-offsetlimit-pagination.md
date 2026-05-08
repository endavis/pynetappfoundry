# ADR-0015: DII backend: live-only, bare-array envelope, offset/limit pagination

## Status

Accepted

## Decision

Add a DII (Data Infrastructure Insights) backend to the DataSource framework. DiiBackend is a live-only backend: all queries hit the DII REST API directly with no local cache database. Four design points distinguish it from OntapBackend:

1. **Live-only operation.** DII has no cache substrate. Cache-only routing decisions raise `NotImplementedError`. The `source="auto"` and `source="live"` modes both go through the live API; `source="cache"` is unsupported.

2. **Bare-array response envelope.** DII endpoints return bare JSON arrays (not the `{"records": [...]}` envelope ONTAP uses or the `{"_embedded": {"items": [...]}}` HAL format). DiiBackend calls `call_endpoint()` directly and iterates the array, parsing each record via `parse_api_record()`. `TypeMapping.records_path` is set to `""` (empty string) for all DII mappings.

3. **Offset/limit pagination.** DII uses `offset` + `limit` query parameters for pagination, not ONTAP's `_links.next.href` HAL convention. The DII API client handles pagination at the client layer.

4. **Deferred `where_expressions`.** SQL-like cache filter expressions are not supported since there is no cache. As of issue #618, the public `QueryBuilder` surface rejects `.where()` and non-equality typed DSL operators with `ValueError` at chain time; `DiiBackend.query()` still raises `NotImplementedError` if `where_expressions` is passed directly. See [ADR-0017](0017-where-expressions-are-cache-only-rationale.md) for the rationale behind the cache-only restriction.

The full DII surface (191 endpoints) is generated via the existing OpenAPI codegen pipeline (ADR-0008), producing 191 model files under `models/dii/` and 191 mapping files under `cache/dii/`. DiiBackend is registered in `_BACKENDS` under the key `"dii"`, consistent with the backend registry pattern from ADR-0013.

## Rationale

DII is the first non-ONTAP backend in the DataSource framework. It validates the multi-API generalization from ADR-0006 and the backend registry design from ADR-0013. A live-only backend is the simplest starting point: it avoids cache schema migrations, derived-field hooks, and partial-fetch merge logic. Cache support can be added later if DII data proves stable enough to snapshot.

The bare-array envelope is a DII-specific quirk that the existing `parse_api_response()` function does not handle (it expects a dict with a `records_path` key). DiiBackend bypasses it by calling `call_endpoint()` and iterating the raw array. This is a pragmatic choice that avoids complicating the shared response parser with a special case for empty `records_path`.

## Related Issues

- Issue #600: feat: add DII API backend to DataSource
- Issue #533: feat: DataSource non-ONTAP backends (partially addressed; DII is the first non-ONTAP backend)
- Issue #618: feat: early validation for where()/typed-DSL + incompatible source mode

## Related Documentation

- [ADR-0006: Generalize field mapping for multi-API](0006-generalize-field-mapping-for-multi-api.md) -- multi-API TypeMapping generalization that DII relies on
- [ADR-0008: OpenAPI codegen for model generation](0008-openapi-codegen-for-model-generation.md) -- codegen pipeline that generated the 191 DII models and mappings
- [ADR-0013: DataSource as a Thin Facade](0013-datasource-as-a-thin-facade-over-the-collector.md) -- backend registry and routing architecture
- [ADR-0017: where-expressions are cache-only (rationale)](0017-where-expressions-are-cache-only-rationale.md) -- rationale for the cache-only restriction on `.where()` and non-equality typed DSL operators
- [Adding a New API Backend](../development/adding-backends.md) -- developer guide updated with DII-specific section
