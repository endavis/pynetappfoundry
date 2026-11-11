---
title: "ADR-0008: OpenAPI codegen for model and mapping generation"
description: Build a codegen tool that parses OpenAPI 3.0 specs to generate Pydantic model classes, FieldMapping/TypeMapping declarations, and TOML config overlays, with its own `$ref` resolution rather than `datamodel-code-generator`.
date: 2026-02-16
audience:
  - contributors
tags:
  - adr
---

# ADR-0008: OpenAPI codegen for model and mapping generation

## Status

Accepted

## Decision

Build a codegen tool (`tools/codegen/`) that parses OpenAPI 3.0 specs and generates:

1. **Pydantic model classes** — flat `CacheModel` subclasses with every field the API returns, following ADR-0007 naming conventions
2. **FieldMapping + TypeMapping declarations** — with `cache_strategy`, `requires_explicit_fetch`, and `parent_mapping` annotations (ADR-0004 extensions)
3. **TOML config overlays** — per-field customization files that are preserved across re-runs

The cache-coupled pipeline (`tools/codegen/`) does its own `$ref` resolution
and type mapping in `adapters.py`; it does **not** use `datamodel-code-generator`.
The adapter layer handles spec normalization, expensive field detection
(ONTAP-specific), and the custom generation of flat models and mappings.
`datamodel-code-generator` is used only by the separate Console pipeline
(see "Codegen integration for Console (Issue #699)" below) — a vestigial
import in `tools/codegen/openapi_codegen.py` was removed as dead code in
PR #693.

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

4. **In-house `$ref` resolution** — `tools/codegen/adapters.py` walks the spec
   itself, handling `$ref` chains, `allOf` merging, and type mapping. This
   was originally meant to be `datamodel-code-generator`; that import was
   removed as dead code in PR #693. The Console pipeline (Issue #699) uses
   `datamodel-code-generator` end-to-end for a different purpose — emitting
   plain Pydantic v2 modules — but the cache-coupled pipeline's flat-model
   shape never benefited from it.

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
* Generated mappings declare array-of-objects fields with
  ``item_model=<SubModel>`` instead of per-list ``_transform_*`` helpers
  (#900), so the N802 ``noqa`` header for mixedCase helper names no longer
  applies.
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
   OpenAPI 3.0.3 spec.  Per-operation ``servers`` blocks encode the
   discovered base URLs (``https://api.bluexp.netapp.com`` for the v3
   ``tenancy`` paths; ``https://api.bluexp.netapp.com/v1/management`` for
   the v4 ``tenancyv4`` paths).  The generated spec was validated end-to-end
   against the live SaaS using a user JWT: 9 endpoints' response shapes
   matched their declared schemas with zero validation errors.

   The parser is build-time only — it is not shipped in the wheel.  The
   generated artifact (``tools/console_openapi/generated/console_openapi.yaml``)
   is checked in alongside a lockfile pinning the upstream source commit.

Issue: #697

### Codegen integration for Console (Issue #699)

1. **Decision: split pipeline.** Console uses ``datamodel-code-generator``
   directly (not ``tools/codegen/``). Rationale: Console's SaaS domain
   (orgs, projects, folders, partnerships) is not a per-cluster cache
   entity; the cache-coupled pipeline's field strategies, TOML overlays,
   and ``OntapModel`` base do not apply. The doit task lives at
   ``tools/doit/console_openapi_tasks.py:task_console_models`` and
   produces a tree under ``src/pynetappfoundry/models/console/``
   (subdivided into ``tenancy/`` and ``tenancyv4/`` packages).

2. **Spec version: 3.0.3.** The parser was updated to emit OpenAPI 3.0.3
   instead of 3.1 (option (a) above, applied at the parser rather than
   in ``convert_specs``). The spec uses no 3.1-only constructs, so the
   downgrade is a one-line change in ``tools/console_openapi/openapi/builder.py``
   and gives wider tool support — most importantly,
   ``datamodel-code-generator`` consumes 3.0.3 directly without an
   intermediate conversion step.

3. **Storage: committed.** ``src/pynetappfoundry/models/console/`` is
   committed in-tree (~21k lines), matching the YAML precedent. CI
   verifies regeneration is a no-op via ``doit console_models_check``,
   which the ``console-models`` job in ``ci.yml`` runs. It clears the output
   directory, re-runs the generator with its formatters pinned, and fails
   if ``git status --porcelain --untracked-files=all`` reports any
   modified, deleted or new file there. The hand-authored compact types
   live outside the tree, in ``src/pynetappfoundry/models/console_types.py`` (Issue #825).

4. **Caching Console data is not foreclosed by the split.** Three
   patterns are supported under the current cache architecture
   (ADR-0001, ADR-0010, ADR-0018):

   - **(a) Runtime-only typed access.** Instantiate the generated model
     from a request, hold it for the duration, never persist. No cache
     integration needed.

   - **(b) Embed a Console entity inside an existing per-cluster
     record.** Concrete cluster-scoped attributes that fit this pattern:
     which org owns the cluster, which marketplace subscription it
     consumes, which connector manages it, which folder/project it lives
     in. E.g.
     ``CloudMetadata.organization: Organization | None;
     marketplace_subscription: Subscription | None``.
     ``CachedClusterMetadata`` field types do not have to be
     ``OntapModel``-derived — they just have to be JSON-serializable
     Pydantic. Add the field, bump ``SCHEMA_VERSION``, write the
     ``_upgrade_to_vN()`` migration per ADR-0018.

   - **(c) New top-level Console-shaped cache entity.** E.g. a
     ``CachedConsoleAccountMetadata`` keyed by org/account id, holding
     subscriptions and folders, with clusters carrying a reference.
     Hand-authored alongside ``CachedClusterMetadata``, consuming the
     generated Console types as value types. Genuinely new territory;
     not in scope for #699.

   **Type source vs. cache placement is decoupled.** A cluster-scoped
   attribute's type can come from any of: Console (this PR's
   ``models/console/``), OCCM (existing ``models/occm/``),
   DII/AIQUM/ONTAP (existing ``models/<api>/``), or hand-authored. The
   cache layer cares only that the field type is valid Pydantic. This
   decoupling is new to the project — before #699, all generated types
   arrived bundled with cache-strategy machinery; pattern (b) above is
   the first time "have a typed value" and "decide whether to cache it"
   are independent decisions.

   What is **not** supported by this split is automatic per-field
   ``cache_strategy`` annotations across all 222 Console endpoints. By
   design: the project does not intend to cache 222 Console endpoints.
   The handful that are cached get hand-authored using pattern (b) or
   (c). If that calculus changes (many Console entities to cache, all
   needing per-field strategies), the split should be revisited — at
   which point ADR-0011 ("nested models to replace flat model pattern")
   would also be in play.

5. **Out of scope (separate work):** typed client / API surface around
   the generated models; the patterns (b) / (c) cache integrations
   themselves — those are per-need follow-ups, not preconditions for
   this PR.

Issue: #699

### Class-name collision resolution (Issue #894)

The shared-schema rule (#603) falls back to a singularized, `str.capitalize()`d URL-path name.
`/au/acquisitionUnit/{auUuid}` (schema `AcquisitionUnit`, shared) and `/au/acquisitionUnits`
both became `DiiAuAcquisitionunit`, so the second registration silently replaced the first in the
model registry. `resolve_class_name_collisions()` in `tools/codegen/generators.py` now runs in
`openapi_codegen.run()` after shared-schema detection and before the endpoint filter. It computes
the normal class names, and for each group of endpoints sharing a name it assigns every member an
exact path-based name (camelCase kept, no singularize or dedup). It returns a map keyed by module
path parts, which `_path_to_class_name(class_name_overrides=...)` consults right after
`_CLASS_NAME_OVERRIDES` and which is threaded through the model, init, mapping and TOML
generators and `write_endpoint_files`.

- Only colliding classes are renamed; every other name is unchanged. The two renames are
  `DiiAuAcquisitionunit` to `DiiAuAcquisitionUnit` (item) and `DiiAuAcquisitionUnits` (collection).
- A collision that exact names do not resolve, or one involving a `_CLASS_NAME_OVERRIDES` entry,
  raises `ValueError` pointing at `_CLASS_NAME_OVERRIDES`.
- `tests/unit/cache/test_registry.py::TestNoDuplicateRegistrations` and the spec-level uniqueness
  test in `tests/unit/codegen/test_roundtrip.py` guard against regressions.

### ONTAP single-object responses (Issue #925)

`_detect_records_path` fell back to the first array property, so an ONTAP endpoint whose 200 response
is one object (for example `GET /cluster/software`) was modelled as its first array (`nodes`).

- **Rule:** for `api_type="ontap"`, `_is_single_object_response()` in `tools/codegen/adapters.py` is
  true when the 200 schema is not an array and has no `records` property of type array. Such an
  endpoint is modelled from the whole response schema and gets `ParsedEndpoint.response_shape =
  "singleton"`. The DII `_SINGLE_OBJECT_ENDPOINTS` table is checked first and is unchanged (`"."`);
  the `_detect_records_path` first-array fallback stays for aiqum and occm.
- **Emission:** `generate_mapping` writes `response_shape="singleton"` and no `records_path=` for these
  endpoints; envelope endpoints emit neither.
- **Dedup rank:** `_deduplicate_endpoints` first ranks an envelope above a singleton, so a collection
  URL is not replaced by its single-object item endpoint. Leaf count decides only within a shape
  (#925 added the tie-break; #934 made shape rank first).
- **Targeted regeneration:** only 11 endpoints were regenerated: `/cluster/software`,
  `/security/anti-ransomware`, `/support/autosupport`, `/cluster/metrocluster`,
  `/security/authentication/cluster/nis`, `/protocols/file-security/permissions/{svm.uuid}/{path}`,
  `/storage/snaplock/litigations/{id}`, `/protocols/fpolicy`, `/protocols/vscan`,
  `/cluster/counter/tables` and `/storage/flexcache/origins`.
- **Deferred:** `ems` and `filters` mappings are left alone. The other array-less ONTAP singletons
  (about 27) are not regenerated. Six endpoints that become parseable under the rule are not emitted.
  A full regeneration would now overwrite the hand-written `/cluster` mapping.
- **Litigations caveat:** fixed by #934, see the next section.

Issue: #925

### Envelope beats singleton in dedup (Issue #934)

Under #925's tie-break an item endpoint with more leaves still won. `/storage/snaplock/litigations/{id}`
(8 leaves) beat `/storage/snaplock/litigations` (7), and `/storage/snaplock/file-fingerprints/{id}`
(13) beat its collection (5). `build_collection_url` strips `/{id}`, so a fetch hit the collection
envelope and parsed it as one object.

- **Rule:** shape ranks first, so an envelope sibling beats a singleton item regardless of leaf counts.
  Within one shape the most leaf fields still wins.
- **Regeneration:** only `/storage/snaplock/litigations` and `/storage/snaplock/file-fingerprints`.
  The collection schemas are named `*_get`, so `_CLASS_NAME_OVERRIDES` pins `OntapSnaplockLitigation`
  and `OntapSnaplockFileFingerprint`. Without the pins the public classes would be renamed and the
  `operations` and `files` children would point `parent_mapping` at a class that no longer exists.
- **Field losses:** the collection schemas are narrower than the item schemas. Litigations loses
  `path`, and its nested operation model loses `num_files_failed`, `num_files_processed`,
  `num_files_skipped`, `num_inodes_ignored`, `path`, `state` and `type_`. File fingerprints loses
  `algorithm`, `data_fingerprint`, `file_size`, `file_type`, `metadata_fingerprint`, `path`, `scope` and
  `state`. Neither model is a cached table, so no migration is needed.
- **Not done:** no rule stops the generator emitting singleton endpoints whose path ends in a
  placeholder with no collection sibling. Measured against the spec it hits 8 endpoints, 6 of them
  already committed (including the `litigations/operations` child), so it belongs with a full
  regeneration. `/protocols/file-security/permissions/{svm.uuid}/{path}` stays committed with two
  literal placeholders and is unfetchable; it needs its own decision. **Resolved by #952** (next
  section). Correction: that mapping has no parent, so it did not request literal placeholders; it
  requested the stripped `/protocols/file-security/permissions?fields=*`, which has no GET.

Issue: #934

### Unfillable path placeholders (Issue #952)

A parent mapping fills only the first `{placeholder}` of a child's path
(`build_parameterized_url`), and a mapping with no parent fetches `build_collection_url`, which
strips every `/{x}` segment. A generated ONTAP endpoint that neither can turn into a real GET was
committed and could never be fetched. Measured against the spec, 29 committed mappings were in that
state.

- **Generator rule:** `is_fetchable_endpoint` in `tools/codegen/generators.py` accepts an endpoint
  with no placeholder, or with a resolvable parent link (`resolve_parent_link`) and exactly one
  placeholder. `_drop_unfetchable_endpoints` in `tools/codegen/openapi_codegen.py` drops every other
  ONTAP endpoint after class-name collision resolution and before the `--endpoints` filter, and
  prints `skipped (unfillable placeholder): <path>`. The rule applies only when `api_type ==
  "ontap"`.
- **Filter bug fixed:** `run()` built `parent_field_names` from the filtered endpoint list, so an
  `--endpoints=` run emitted children with no `parent_mapping`. The parent lookups are now built
  from the full deduped list before the filter.
- **Wired by regeneration (9):** the five `/protocols/fpolicy/{svm.uuid}/*` children get
  `parent_mapping="OntapFpolicy"` and the four `/protocols/vscan/{svm.uuid}/*` children get
  `parent_mapping="OntapVscan"`, both with `parent_id_field="svm.uuid"`.
- **Deleted (18):** the mapping and model packages of endpoints that need two placeholders filled,
  take user input (`{path}`, `{user}`), or have no list endpoint for their id. Among them are
  `protocols/file_security/permissions`, `protocols/cifs/shares/acls`,
  `protocols/san/lun_maps/reporting_nodes`, `security/roles/privileges`, the two S3 bucket children,
  `storage/snaplock/litigations/operations` and `protocols/ndmp/svms/passwords`. ACLs, reporting
  nodes, privileges and litigation operations remain reachable as nested fields on their parent
  models. Multi-placeholder parent fill, which would let about 10 of them return, is #955.
- **Known exceptions (none):** `OntapEmsFilterRuleResponse` (parent needed #932) is resolved by #932
  and `OntapExportRule` (parent `OntapExportPolicy` was rule-shaped with no `id`) by #956 (see their
  sections).
- **Guard:** `tests/unit/cache/test_mapping_fetch_url_resolvable.py` checks that every registered
  ONTAP mapping's fetch URL resolves given its parent, apart from the named exceptions, and that the
  exception list and the deleted list stay current.

Issue: #952

### Export policy reshaped (Issue #956)

`/protocols/nfs/export-policies` returns policy records (`id`, `name`, `svm`, `rules[]`), but
`OntapExportPolicy` was generated rule-shaped, so every cached row held only defaults and the diff
override keyed on `index` collapsed every policy to key `0`. Regenerating the two export-policy
endpoints fixes it.

- **Model:** `OntapExportPolicy{id, name, svm, rules: list[OntapExportPolicyRule]}` with
  `identifier_field="id"`. The former top-level rule fields moved into `OntapExportPolicyRule`, and
  `OntapExportPolicyClient` became `OntapExportPolicyRuleClient`. Query and compliance paths change
  from `protocols.nfs_export_policies.<rule-field>` to
  `protocols.nfs_export_policies.rules[].<rule-field>`. **BREAKING.**
- **Child wiring:** `OntapExportRule` gains `parent_mapping="OntapExportPolicy"` and
  `parent_id_field="id"`; it stays live-only with no table. It is removed from the #952 known
  exceptions in the guard test.
- **Diff:** the override is `("id", "{svm.name}/{name}")`.
- **Cache:** `SCHEMA_VERSION` 8 to 9; `_upgrade_to_v9` drops and recreates `ontapexportpolicy` and
  clears the envelope (ADR-0018). Run `nf cache refresh` afterwards. `METADATA_SCHEMA_VERSION`
  stays `"2.1"`, so old snapshots still load and the first diff reports the policies as added once.

Issue: #956

### EMS filter collection (Issue #932)

`OntapEmsFilter` was generated from the item endpoint `/support/ems/filters/{name}` with
`records_path="rules"`, so it modelled a rule, not a filter. The collection schema is named
`ems_filter_response`, which the generator would turn into `OntapEmsFilterResponse`, a rename.

- **Override:** `"/support/ems/filters": "OntapEmsFilter"` in `_CLASS_NAME_OVERRIDES`. A general
  `_response`-stripping rule was rejected: it would rename other collections on their next
  regeneration.
- **Model:** the collection wins dedup, so `OntapEmsFilter{access_control_role, name, rules:
  list[OntapEmsFilterRule], system_defined}` with `identifier_field="name"`. **BREAKING:** the fields
  `index`, `message_criteria`, `parameter_criteria` and `type_` are removed from `OntapEmsFilter`;
  `OntapEmsFilterMessageCriteria` and `OntapEmsFilterParameterCriteria` are replaced by
  `OntapEmsFilterRuleMessageCriteria` and `OntapEmsFilterRuleParameterCriteria` under
  `OntapEmsFilterRule`.
- **Child wiring:** `OntapEmsFilterRuleResponse` gains `parent_mapping="OntapEmsFilter"` and
  `parent_id_field="name"`, and is removed from the #952 known exceptions in the guard test.
- **Targeted regeneration:** only `/support/ems/filters` and `/support/ems/filters/{name}/rules`.
- **Cache:** EMS filters are not a cached table, so `SCHEMA_VERSION` is unchanged.

Issue: #932

## Related Issues

- Issue #301: feat: field annotations, OpenAPI codegen, and SQL cache storage
- Issue #402: refactor: move ONTAP API models from cache/ to models/ package
- Issue #444: refactor: evaluate nested models to replace flat model pattern (see ADR-0011)
- Issue #601: bug(codegen): pipeline drops identifier_field and cache_strategy=realtime on regen
- Issue #603: bug(codegen): shared response schemas cause registry collisions; non-ONTAP support gaps
- Issue #697: feat: add BlueXP/Console SaaS docs to OpenAPI 3.1 parser
- Issue #699: feat: generate Pydantic models from Console OpenAPI spec
- Issue #894: bug: codegen class-name collisions drop model registry mappings
- Issue #925: bug: codegen models ONTAP single-object responses as their first array property
- Issue #934: bug: ONTAP item-endpoint mappings with no fetchable parent (snaplock litigations, file_security permissions)
- Issue #952: bug: generated ONTAP mappings with unfilled path placeholders are unfetchable
- Issue #932: refactor: codegen naming for support/ems/filters collection (deferred from #925)
- Issue #956: bug: OntapExportPolicy model is rule-shaped with no id, so OntapExportRule cannot be wired as its child

## Related Documentation

- [ADR-0004: Declarative field mapping framework](0004-declarative-field-mapping-framework.md)
- [ADR-0007: URL-tree model registry](0007-url-tree-model-registry.md)
- [Cache Model Architecture](../development/cache-models.md)
- [Adding Backends](../development/adding-backends.md)
