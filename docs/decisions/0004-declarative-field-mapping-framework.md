# ADR-0004: Declarative field mapping framework for ONTAP collection

## Status

Accepted

## Context

The collector module contained hand-written parsing methods for each ONTAP object type (volumes, aggregates, etc.). Each method manually extracted fields from API responses and CLI output, leading to:

- Significant boilerplate — every new type required custom parsing functions for both API and CLI sources
- Inconsistent field handling — some types missed "expensive" API fields (e.g., `autosize.*`, `files.*`, `nas.path`) because they weren't explicitly requested
- No single source of truth — API endpoints and CLI commands were scattered across collector methods, making it hard to verify coverage or reuse them in tooling like the `cache inspect` command
- API/CLI parity gaps — differences between API and CLI parsing for the same type were hard to spot

## Decision

Use a declarative field mapping framework based on two frozen dataclasses — `FieldMapping` and `TypeMapping` — to map ONTAP REST API and CLI responses to cache model objects. Generic parser functions (`parse_api_response`, `parse_cli_records`, `parse_api_record`, `parse_cli_record`) replace hand-written parsing methods.

Each ONTAP object type is defined as a `TypeMapping` constant co-located with its model in `src/pynetappfoundry/cache/<api-path>/mapping.py` (restructured from `cache/mappings/<type>.py` in issue #257), declaring:

- The REST API endpoint (including required `?fields=` params)
- The CLI show command
- A tuple of `FieldMapping` entries mapping each field across API path, CLI field name, and cache model attribute
- Optional transform functions for fields that need custom extraction logic

The pilot migration (VolumeInfo) was completed in PR #189.

## Rationale

1. **Reduces boilerplate** — new types only need a mapping definition, not custom parsing methods.

2. **Ensures API/CLI parity** — both sources produce the same model using the same field definitions, making gaps immediately visible.

3. **Centralizes API endpoints and CLI commands** — `TypeMapping.api_endpoint` and `TypeMapping.cli_command` are the single source of truth, used by the collector, `cache inspect` command, and future tooling.

4. **Makes field requirements explicit** — expensive API fields (e.g., `autosize.*`, `files.*`, `nas.path`) are declared in the mapping rather than hidden in endpoint query strings.

5. **Leverages existing utilities** — nested API path traversal uses `get_nested_value()` from `utils/dict_path.py`, and CLI value coercion handles ONTAP conventions (`-` for missing, `%` suffix, boolean strings).

### Alternatives Considered

- **Keep hand-written parsers**: Simpler per-type, but doesn't scale and makes parity hard to verify.
- **Code generation from a schema**: More automated, but ONTAP's CLI/API asymmetry makes a pure schema approach fragile. *Later adopted for model and mapping generation via ADR-0008, while the declarative framework itself remained the foundation. The CLI/API asymmetry concern was addressed by generating only the API side and keeping CLI mappings manual where needed.*
- **Third-party ORM/mapping library**: Adds external dependency for a domain-specific problem that's well-served by two small dataclasses.

## Evolution: Field Annotations for Cache Strategy (Issue #301)

In issue #301, the framework was extended with field-level annotations to support
different data collection and storage strategies:

### FieldMapping Extensions

```python
cache_strategy: Literal["cache", "realtime", "derived"] = "cache"
requires_explicit_fetch: bool = False
post_collection: Callable[[Any], Any] | None = None
```

| Strategy | Collected? | Persisted? | How accessed |
|----------|-----------|-----------|--------------|
| `cache` | Yes, during bulk collection | Yes, in DB | Read from cache |
| `realtime` | No | No | Fetched on-demand per object |
| `derived` | No | Yes | Computed from other fields post-collection |

### TypeMapping Extensions

```python
parent_mapping: str | None = None    # For parameterized endpoints
parent_id_field: str | None = None   # Placeholder value field on parent

# Computed methods
def explicit_fetch_fields(self) -> list[str]: ...
def explicit_fetch_api_fields(self) -> list[str]: ...  # Issue #317
def build_collection_url(self) -> str: ...              # Issue #317
def cached_fields(self) -> tuple[FieldMapping, ...]: ...
def realtime_fields(self) -> tuple[FieldMapping, ...]: ...
def derived_fields(self) -> tuple[FieldMapping, ...]: ...
```

### Dynamic URL Building (Issue #317)

`build_collection_url()` makes `requires_explicit_fetch` the single source of truth
for expensive ONTAP fields. Instead of hardcoding expensive field names in
`api_endpoint` (e.g., `?fields=*,analytics,autosize,...`), the mapping stores only
`?fields=*` and `build_collection_url()` dynamically appends the expensive fields
by inspecting `requires_explicit_fetch` on each `FieldMapping`. This eliminates the
dual source of truth and ensures TOML overlays that change `requires_explicit_fetch`
are automatically reflected in collection URLs.

### OntapUUID Dedicated Type

A validated `Annotated[str, AfterValidator(...)]` type for all UUID fields,
defined in `_base.py`.  Validates format at model construction, allows empty
strings (ONTAP returns `""` for optional UUID fields), remains a plain `str`
at runtime.

These extensions enable the OpenAPI codegen tool (ADR-0008) to generate
annotated mappings from API specs, with per-field customization via TOML overlays.

## Consequences

- All ONTAP models and mappings are now generated from OpenAPI specs via the codegen tool (ADR-0008). Hand-written models have been fully replaced.
- The `cache inspect` command automatically works with any registered mapping.
- Adding a new type means running codegen against the spec and customizing the TOML overlay.
- Field annotations drive collection behavior: `parse_api_record()` skips non-cache fields during bulk collection, and `parse_api_response()` applies `post_collection` transforms for derived fields.
- The `collection_endpoint` property on `TypeMapping` strips `{id}` placeholders for bulk collection URLs, eliminating the need for hardcoded endpoint strings in the collector.

## Related Issues

- Issue #188: feat: add declarative field mapping framework
- Issue #191: refactor: migrate AggregateInfo to field mapping framework
- Issue #210: refactor: migrate NodeInfo to field mapping framework
- Issue #215: refactor: migrate SnapMirrorRelationship to field mapping framework
- Issue #217: refactor: migrate CloudMetadata to field mapping framework
- Issue #216: refactor: migrate ClusterPeer to field mapping framework
- Issue #214: refactor: migrate HAInfo to field mapping framework
- Issue #237: refactor: all-or-nothing collection with no CLI fallback
- Issue #447: refactor: simplify or remove FieldMapping after nested model migration
- Issue #259: feat: generalize field mapping framework for multi-API data collection
- Issue #209: refactor: migrate ClusterInfo to field mapping framework
- Issue #257: refactor: deep URL-tree structure with automatic model and mapping discovery
- Issue #192: refactor: migrate SVMInfo to field mapping framework
- Issue #205: refactor: migrate DNSInfo to field mapping framework
- Issue #213: refactor: migrate LicenseInfo/LicenseFeature to field mapping framework
- Issue #211: refactor: migrate NetworkLIF to field mapping framework
- Issue #212: refactor: migrate BroadcastDomain to field mapping framework
- Issue #301: feat: field annotations, OpenAPI codegen, and SQL cache storage
- Issue #312: fix: remove hardcoded collector endpoints and wire cache_strategy into parsing
- Issue #317: feat: collector ?fields= expansion for expensive ONTAP fields
- Issue #444: refactor: evaluate nested models to replace flat model pattern (see ADR-0011)
- Issue #478: doc: document the QuerySet query layer and fluent builder (consumes `TypeMapping` / `cache_attr` / realtime field annotations)
- Issue #479: doc: refresh cache architecture documentation
- Issue #495: feat: unified DataSource for all cluster reads (ADR-0012 — `FieldMapping`/`TypeMapping` become the metadata foundation for the unified `DataSource` accessor)

## Related Documentation

- [Field Mapping Framework Developer Guide](../development/field-mapping.md)
- [Query Layer guide](../usage/query-layer.md)
- [Cache System Reference](../reference/cache.md) — Field Mapping section
- [ADR-0012: Unified DataSource accessor for all cluster reads](0012-unified-datasource-accessor.md) — makes `FieldMapping`/`TypeMapping` the metadata foundation for the unified accessor
