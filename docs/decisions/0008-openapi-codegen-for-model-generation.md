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

### Round-trip invariant and TOML-as-authority (Issue #601)

**Regeneration is a no-op for existing endpoints.**  Running
`doit generate_models --api=<api>` against an endpoint whose output
already exists on disk must produce byte-identical `mapping.py` and
`model.py` files (after `ruff format`).  This invariant is enforced by
`tests/unit/codegen/test_roundtrip.py` for three representative ONTAP
endpoints (`/storage/volumes`, `/storage/aggregates`, `/svm/peers`).  A
failure there means either the generator has drifted or the on-disk
file contains an un-mirrored hand edit — both must be resolved before
codegen is safe to run against the full tree.

**TOML is authoritative for per-field strategy.**  The sibling
`<name>.toml` overlay owns `cache_strategy` and `requires_explicit_fetch`
at runtime — the runtime overlay loader
(`src/pynetappfoundry/cache/overlay_loader.py`) re-applies these values
from the TOML at registry-load time and takes precedence over anything
written into the emitted Python.  The generator mirrors those values
into `mapping.py` so the file is self-describing and round-trippable;
to change the strategy for a field, edit the TOML — the Python will
pick it up on the next regen.

**`identifier_field` is auto-inferred; nested cases need a manual
edit.**  The generator infers `TypeMapping.identifier_field` from a
collection endpoint's sibling item endpoint path parameter
(e.g. `/storage/volumes` + `/storage/volumes/{uuid}` →
`identifier_field="uuid"`).  Multi-param item endpoints are left as
`None` — composite identifiers are not auto-inferred.  One ONTAP
endpoint (`/svm/migrations/volumes`) uses a nested response-field
identifier (`"volume.uuid"`) that cannot be derived from the spec; the
`mapping.py` for that endpoint must be hand-edited after regen.
Regeneration will wipe the manual override, so the edit must be
re-applied (or mirrored into the generator if more nested identifiers
appear in future specs).

Issue: #601

### Shared-schema naming, registry duplicate guard, non-ONTAP support (Issue #603)

**Shared-schema naming rule.**  When an OpenAPI response schema is
``$ref``-ed by more than one endpoint *after* the generator's
same-module-path deduplication pass, the generator derives the class
name from the URL path rather than the schema name.  Example: DII's
``Count`` schema is referenced by 7 distinct ``/foo/count`` endpoints
(``/assets/storages/count``, ``/assets/fabrics/count``, …).  Naming
every generated class ``DiiCount`` would cause 6 of 7 mappings to be
shadowed in ``ModelRegistry``; URL-path-derived naming produces
distinct classes (``DiiAssetsStoragesCount``,
``DiiAssetsFabricsCount``, …) so every endpoint is reachable via
``DataSource.query(<ModelClass>, …)``.

The detection lives in
:func:`tools.codegen.adapters.detect_shared_schemas` and runs after
:func:`tools.codegen.openapi_codegen._deduplicate_endpoints` — ONTAP
collection+item pairs share a schema but only one survives dedup, so
detecting shared schemas post-dedup correctly returns ``set()`` for
ONTAP and preserves byte-identical output (round-trip invariant).
``_path_to_class_name`` accepts a keyword-only ``shared_schemas``
parameter; callers thread it through ``generate_model``,
``generate_mapping``, ``generate_init``, ``generate_toml_overlay``,
and ``write_endpoint_files``.

**Registry duplicate-registration warning.**
``ModelRegistry.register_mapping()`` now emits a ``logger.warning``
when the same class name is registered with a **different**
``model_class`` (the collision shape the shared-schema rule prevents).
Registration still proceeds last-wins for backward compatibility — the
warning surfaces regressions in CI/logs without making registry
import a hard failure.  Legitimate re-registrations that target the
same ``model_class`` (e.g. the overlay-loader pass that replaces a
mapping's ``fields`` tuple) do not warn.

**Non-ONTAP infrastructure fixes.**  The same PR also corrects six
ONTAP-specific assumptions that blocked non-ONTAP codegen:

* ``?fields=*`` query suffix is only appended for ``api_type="ontap"``
  (DII, AIQUM, OCCM do not honor it).
* ``_ensure_init_files`` now seeds both the ``cache/<api>/`` and
  ``models/<api>/`` trees, including api-type roots and cache leaves,
  so ``pkgutil.walk_packages`` can discover mappings on a freshly
  generated tree.
* ``parent_mapping`` is only emitted when the parent path's module
  tree generates a mapping whose class name matches the computed
  ``parent_class`` (via the ``shared_schemas``-aware derivation) —
  orphan child endpoints get ``parent_mapping`` omitted rather than
  dangling.
* ``parent_id_field`` dispatches on ``api_type``
  (``_PARENT_ID_FIELD_BY_API`` — ONTAP/AIQUM → ``"uuid"``, DII/OCCM
  → ``"id"``).
* Generated mappings emit a ``# ruff: noqa: N802`` header when any
  ``_transform_*`` helper has a mixedCase suffix (DII's
  ``applicationRoles`` → ``_transform_applicationRoles``).
* ``doit generate_models`` post-processes the generated tree with
  ``ruff format`` then ``ruff check --fix``, which drops any
  ``# ruff: noqa: E501`` header the formatter made redundant.

**Round-trip invariant extended.**  The regression test
``tests/unit/codegen/test_roundtrip.py`` now parametrizes over both
ONTAP and DII endpoints: three ONTAP (``/storage/volumes``,
``/storage/aggregates``, ``/svm/peers``) plus two DII
(``/assets/storages`` — unique schema; ``/assets/storages/count`` —
shared-schema disambiguation).  The two DII endpoints are committed
alongside the generator fix so the test has on-disk expectations to
diff against; the remaining DII surface is generated under #600.

Issue: #603

### Spec acquisition strategies (Issue #697)

The original ADR assumes the vendor publishes an OpenAPI spec we can drop
into ``docs/example-config/apis/<name>/openapi3.json``.  In practice, that
assumption holds for some APIs and not others.  The supported strategies are:

1. **Vendor-published OpenAPI/Swagger** (preferred).  ONTAP, AIQUM, and DII
   all publish machine-readable specs that we copy in-tree as
   ``all.json`` / ``openapi3.json``.  ``doit convert_specs`` normalizes
   them to OpenAPI 3.0 for the codegen pipeline.

2. **Connector-scraped Swagger 1.2** (legacy).  The OCCM (Cloud Manager
   Connector) API is documented through the Connector's local Swagger UI
   only.  The current ``docs/example-config/apis/occm/`` tree was built
   by hand-walking ``http://<connector_ip>/occm/api/api-docs/`` per
   ``notes.txt``.  Re-acquisition is a manual chore.

3. **Parser-derived from prose docs** (new).  The BlueXP / NetApp Console
   SaaS layer (``api.bluexp.netapp.com``) has no machine-readable spec
   at all — only AsciiDoc reference pages auto-generated from a
   proprietary internal tool, published in ``NetAppDocs/console-automation``.
   ``tools/console_openapi/`` parses those AsciiDoc files into an
   OpenAPI 3.1 spec.  Per-operation ``servers`` blocks encode the
   discovered base URLs (``https://api.bluexp.netapp.com`` for the v3
   ``tenancy`` paths; ``https://api.bluexp.netapp.com/v1/management`` for
   the v4 ``tenancyv4`` paths).  The generated spec was validated end-to-end
   against the live SaaS using a user JWT: 9 endpoints' response shapes
   matched their declared schemas with zero validation errors.

   The parser is build-time only — it is not shipped in the wheel.  The
   generated artifact (``tools/console_openapi/generated/console_openapi.yaml``)
   is checked in alongside a lockfile pinning the upstream source commit.

   **Codegen integration is deferred.**  Wiring the Console spec into
   ``doit generate_models --api=console`` will require either (a) an
   OpenAPI 3.1 → 3.0 downgrade pass in ``convert_specs`` or (b) a
   codegen update to consume 3.1 directly.  Tracked as a separate
   follow-up.

Issue: #697

## Related Issues

- Issue #301: feat: field annotations, OpenAPI codegen, and SQL cache storage
- Issue #402: refactor: move ONTAP API models from cache/ to models/ package
- Issue #444: refactor: evaluate nested models to replace flat model pattern (see ADR-0011)
- Issue #601: bug(codegen): pipeline drops identifier_field and cache_strategy=realtime on regen
- Issue #603: bug(codegen): shared response schemas cause registry collisions; non-ONTAP support gaps
- Issue #697: feat: add BlueXP/Console SaaS docs to OpenAPI 3.1 parser

## Related Documentation

- [ADR-0004: Declarative field mapping framework](0004-declarative-field-mapping-framework.md)
- [ADR-0007: URL-tree model registry](0007-url-tree-model-registry.md)
- [Cache Model Architecture](../development/cache-models.md)
- [Adding Backends](../development/adding-backends.md)
