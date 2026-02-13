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
- **Code generation from a schema**: More automated, but ONTAP's CLI/API asymmetry makes a pure schema approach fragile.
- **Third-party ORM/mapping library**: Adds external dependency for a domain-specific problem that's well-served by two small dataclasses.

## Consequences

- All new ONTAP object types should use the mapping framework instead of hand-written parsers.
- Existing hand-written parsers can be migrated incrementally (one type at a time).
- The `cache inspect` command automatically works with any registered mapping.
- Adding a new type follows a documented, repeatable process.

## Related Issues

- Issue #188: feat: add declarative field mapping framework
- Issue #191: refactor: migrate AggregateInfo to field mapping framework
- Issue #210: refactor: migrate NodeInfo to field mapping framework
- Issue #215: refactor: migrate SnapMirrorRelationship to field mapping framework
- Issue #217: refactor: migrate CloudMetadata to field mapping framework
- Issue #216: refactor: migrate ClusterPeer to field mapping framework
- Issue #214: refactor: migrate HAInfo to field mapping framework
- Issue #237: refactor: all-or-nothing collection with no CLI fallback
- Issue #259: feat: generalize field mapping framework for multi-API data collection
- Issue #209: refactor: migrate ClusterInfo to field mapping framework
- Issue #257: refactor: deep URL-tree structure with automatic model and mapping discovery
- Issue #192: refactor: migrate SVMInfo to field mapping framework
- Issue #205: refactor: migrate DNSInfo to field mapping framework
- Issue #213: refactor: migrate LicenseInfo/LicenseFeature to field mapping framework
- Issue #211: refactor: migrate NetworkLIF to field mapping framework
- Issue #212: refactor: migrate BroadcastDomain to field mapping framework

## Related Documentation

- [Field Mapping Framework Developer Guide](../development/field-mapping.md)
