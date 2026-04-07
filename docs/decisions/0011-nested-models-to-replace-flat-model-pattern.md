# ADR-0011: Nested models to replace flat model pattern

## Status

Accepted

## Context

All Pydantic models use a flat field naming convention where nested API paths are encoded in the attribute name (e.g., `ip.address` → `ip_address`, `location.home_node.name` → `location_home_node_name`). This was originally driven by the cache storage layer (SQLite flat rows, ADR-0001/ADR-0009).

However, this design has caused systemic issues:

- **75 broken sub-model transforms** — `SubModel(**item)` fails because raw API dicts are nested but models expect flat keys. The `FieldMapping` translation layer handles top-level fields via `get_nested_value()` but was never extended to sub-objects.
- **User-hostile API** — users writing scripts must learn `iface.ip_address` instead of `iface.ip.address`, which doesn't match ONTAP API docs or responses.
- **Unnecessary complexity** — the `FieldMapping` translation layer, codegen flattening logic, and verbose field names (`location_broadcast_domain_name`) all exist solely to bridge the flat-nested gap.
- **Codegen constraints** — `datamodel-code-generator` output was rejected (ADR-0008) because it produces nested models. Custom flattening logic was built instead.

## Decision

Replace flat Pydantic models with **nested models that mirror the API structure**. Models will use nested sub-objects matching the ONTAP REST API response shape:

```python
# Before (flat)
class OntapSvmIpInterface(OntapModel):
    ip_address: str = ""
    ip_netmask: str = ""
    location_home_node_name: str = ""

# After (nested)
class OntapSvmIpInterface(OntapModel):
    class Ip(OntapModel):
        address: str = ""
        netmask: str = ""
    class Location(OntapModel):
        class HomeNode(OntapModel):
            name: str = ""
        home_node: HomeNode = HomeNode()
    ip: Ip = Ip()
    location: Location = Location()
```

Access becomes `iface.ip.address` — matching the API docs.

### Cache Serialization

The cache layer is the only consumer that needs flat representation. This will be handled by a flatten/nest adapter at the cache boundary:

- **Write**: nested model → flat dict for SQLite storage
- **Read**: flat dict from SQLite → nested model

This keeps the internal concern (storage format) separate from the public API (model structure).

### Sub-Model Transforms

With nested models, `SubModel(**item)` works directly because the raw API dict structure matches the model structure. The 75 broken transforms (issue #443) are fixed by the architecture change itself, not by individual patches.

### FieldMapping Impact

The `api_path` field on `FieldMapping` becomes simpler or unnecessary for most fields, since model attribute names match API paths directly. `FieldMapping` may still be needed for:

- `cache_strategy` annotations (cache/realtime/derived)
- `requires_explicit_fetch` flags
- Fields where API path differs from model path (edge cases)
- CLI field mapping (CLI output structure differs from REST API)

### Codegen Impact

The codegen tool (ADR-0008) can leverage `datamodel-code-generator` more directly for nested model generation. The custom flattening logic in `adapters.py` can be removed or simplified.

## Rationale

1. **Matches user mental model** — dot notation mirrors the API docs, reducing learning curve for script authors.
2. **Eliminates the transform bug class** — nested models make `SubModel(**item)` correct by construction. The 75 broken transforms and the need for `flatten_api_record` disappear.
3. **Simplifies codegen** — generating nested models from OpenAPI specs is the natural output; flattening was the custom part.
4. **Separates concerns** — cache serialization is an internal detail that shouldn't dictate the public model API.
5. **Reduces field name verbosity** — `iface.location.home_node.name` is self-documenting; `iface.location_home_node_name` is a learned convention.

### Alternatives Considered

- **Fix all 75 transforms with `flatten_api_record`** (issue #443): Patches the symptom without addressing the root cause. Adds more translation infrastructure instead of removing the need for it.
- **Keep flat models, improve codegen**: Still leaves the user-facing API mismatched from the ONTAP API and doesn't eliminate the transform bug class.

## Consequences

- All existing model consumers must migrate to nested access patterns
- Cache read/write layer needs flatten/nest adapters
- Codegen tool needs updates to produce nested models
- ADR-0004 (FieldMapping) may need amendments for simplified field mapping
- ADR-0008 (codegen) will be amended for nested model generation
- Issue #443 (fix 75 transforms) becomes unnecessary — superseded by this change

## Related Issues

- Issue #444: refactor: evaluate nested models to replace flat model pattern
- Issue #443: refactor: fix all sub-model transforms to use declarative field mapping (superseded)
- Issue #440: fix: HTML report bugs - missing data, title formatting, cloud section placement (catalyst)
- Issue #447: refactor: simplify or remove FieldMapping after nested model migration
- Issue #479: doc: refresh cache architecture documentation

## Related Documentation

- [Field Mapping Framework Developer Guide](../development/field-mapping.md)
- [Cache System Reference](../reference/cache.md) — Nested Models Pattern section
