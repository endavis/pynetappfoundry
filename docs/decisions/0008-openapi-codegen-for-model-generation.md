# ADR-0008: OpenAPI codegen for model and mapping generation

## Status

Accepted

## Decision

Build a codegen tool (`tools/codegen/`) that parses OpenAPI 3.0 specs and generates:

1. **Pydantic model classes** — flat `CacheModel` subclasses with every field the API returns, following ADR-0007 naming conventions
2. **FieldMapping + TypeMapping declarations** — with `cache_strategy`, `requires_explicit_fetch`, and `parent_mapping` annotations (ADR-0004 extensions)
3. **TOML config overlays** — per-field customization files that are preserved across re-runs

The tool uses `datamodel-code-generator` as a library for `$ref` resolution and type mapping from OpenAPI schemas.  Our adapter layer handles spec normalization, expensive field detection (ONTAP-specific), and the custom generation of flat models and mappings.

### Architecture

```
OpenAPI 3.0 spec (JSON)
  → adapters.py (parse endpoints, resolve $refs, flatten schemas)
  → expensive_fields.py (extract ONTAP expensive field patterns)
  → generators.py (produce model.py, mapping.py, __init__.py, TOML overlay)
  → openapi_codegen.py (CLI entry point)
```

All API specs are pre-converted to OpenAPI 3.0 by `doit convert_specs` before codegen runs.

### Spec Support

| API | Expensive Fields | Records Path |
|-----|-----------------|--------------|
| ONTAP | Parsed from endpoint descriptions | `records` |
| DII | None | Varies |
| AIQUM | None | `records` |
| OCCM | None | Varies |

### TOML Overlay Workflow

Each generated endpoint gets an overlay file where field strategies can be customized:

```toml
[fields.statistics_iops_total]
cache_strategy = "realtime"

[fields.is_ha]
cache_strategy = "derived"
```

Re-running codegen preserves user edits, adds new fields with defaults, and warns about removed fields in a `_removed_fields` key.

## Rationale

1. **Eliminates hand-written models** — the ONTAP spec has 1100+ schemas and 550 endpoints.  Hand-writing models is error-prone and doesn't scale.

2. **Single source of truth** — the OpenAPI spec defines the API contract.  Generating from it ensures models stay in sync with the API.

3. **Customizable via TOML** — field strategies (cache/realtime/derived) vary by use case.  TOML overlays separate generation from customization.

4. **`datamodel-code-generator` for $ref resolution** — the library handles complex `$ref` chains, `allOf` merging, and type mapping.  Our code flattens the resolved schemas into the project's flat model pattern.

5. **Multi-API support** — the same tool works for ONTAP, DII, AIQUM, and OCCM specs with per-API-type configuration (expensive field detection, records path detection).

### Alternatives Considered

- **Pure `datamodel-code-generator` output**: Generates nested models that don't match the project's flat `CacheModel` + `FieldMapping` pattern.
- **Hand-written $ref resolver**: Simpler but fragile for edge cases (`allOf`, circular refs, deeply nested schemas).
- **No codegen (continue hand-writing)**: Doesn't scale to 30+ model types with 50+ fields each.

## Amendments

### Model output path change (Issue #402)

Codegen now generates `model.py` files to `models/ontap/` instead of `cache/ontap/`.
Mapping files (`mapping.py`, `__init__.py`, TOML overlays) remain under `cache/ontap/`.
Generated models inherit from `OntapModel` (defined in `models._base`) instead of
`CacheModel`.

## Related Issues

- Issue #301: feat: field annotations, OpenAPI codegen, and SQL cache storage
- Issue #402: refactor: move ONTAP API models from cache/ to models/ package
- Issue #444: refactor: evaluate nested models to replace flat model pattern (see ADR-0011)

## Related Documentation

- [ADR-0004: Declarative field mapping framework](0004-declarative-field-mapping-framework.md)
- [ADR-0007: URL-tree model registry](0007-url-tree-model-registry.md)
- [Cache Model Architecture](../development/cache-models.md)
