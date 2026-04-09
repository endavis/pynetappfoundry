# ADR-0012: Unified DataSource Accessor for All Cluster Reads

## Status

Accepted

## Context

The project has at least four parallel read paths today, each with its own input convention, output shape, and override mechanism:

- **`LazyClusterMetadata`** (`src/pynetappfoundry/cache/_lazy.py`) — lazy per-field-group cache reader with on-demand fetch fallback, backed by `FieldGroupFetcher` (`cache/_fetcher.py`). Returns Pydantic models.
- **`QuerySet`** (`src/pynetappfoundry/query/queryset.py`) — live REST collection reader that shares `parse_api_response()` with the cache path. Returns Pydantic models. Accepts filters as kwargs with a dunder-to-dot rewrite in `_attr_to_api_path` (e.g. `svm__name="vs1"` becomes `svm.name=vs1`).
- **`fetch_realtime`** and siblings (`src/pynetappfoundry/query/realtime.py`) — live REST realtime reader. Deliberately bypasses model construction via `_parse_realtime_record` and returns dotted-string-keyed `dict`s.
- **`nf cache check`** / **`nf cache query`** CLIs — direct cache readers.

Each surface has diverged in three dimensions:

1. **Input shape** — kwargs with dunder rewrite (`QuerySet`), dotted-string dicts (`fetch_realtime`), positional args (cache CLIs).
2. **Output shape** — Pydantic models (cache, `QuerySet`) vs dotted-key `dict`s (realtime).
3. **Source override** — only the CLI `--live` flag (from issue #472) exists today, and only for a narrow slice.

Meanwhile, issue #485 is mid-migration and is adding more call sites against the old shapes. Every command that lands before convergence has to be migrated again afterward. Issues #487 (filter input ergonomics) and #488 (realtime output shape) were closed as superseded once it became clear that fixing them in isolation would not address the convention drift across the four surfaces.

This ADR builds on:

- ADR-0001 (SQLite metadata cache) — establishes the cache substrate.
- ADR-0004 (declarative field mapping framework) — provides `FieldMapping`, `TypeMapping`, and `parse_api_response()`, which both cache and live REST already share.
- ADR-0006 (multi-API field mapping) — introduced the `TypeMapping.api_type` tag that this ADR uses as a backend registry key.
- ADR-0010 (ClusterEntry and namespace access pattern) — defines the cache-vs-live-fetch routing that this ADR extends and partially supersedes.

## Decision

Introduce `DataSource` as the single accessor for all cluster reads. All new read code uses it; the existing surfaces become thin shims during migration and are cleaned up afterward. The design locks in ten points:

### 1. Return shape: Pydantic model instances

Every read — from cache, live REST collection, or live REST realtime — returns Pydantic model instances declared by `FieldMapping`/`TypeMapping`. Cache and live REST already share `parse_api_response()` from `cache/field_mapping.py`, so this is a no-op for them. Realtime data hydrates the same model with only the fetched fields populated; the rest fall back to the defaults declared on the model (`""`, `0`, `False`, `default_factory=...`) per the convention in `src/pynetappfoundry/models/_base.py`. This works because every field on generated `Ontap*` models has a literal default.

### 2. Fetched-fields tracking on `OntapModel`

Add a `_fetched_fields: set[str]` instance attribute on `OntapModel` (`src/pynetappfoundry/models/_base.py`), populated at construction time by the accessor with dotted-path identifiers. A `was_fetched(path: str) -> bool` helper exposes the set. It is empty by default, so code that constructs models directly (tests, fixtures) does not need to populate it. This gives diff, compare, and audit code a real signal to distinguish "field was fetched and happened to be empty" from "field was never fetched" — a distinction the realtime functions lack today (issue #488).

### 3. Input shape: dotted-string paths

`DataSource.query(OntapVolume).filter({"svm.name": "vs1", "autosize.mode": "grow"})` is the canonical form: a positional `dict[str, Any]` whose keys are dotted API paths. `**kwargs` (`filter(name="vol1", state="online")`) remains supported for top-level scalar fields as a convenience. The dunder-to-dot rewrite from today's `QuerySet.filter._attr_to_api_path` is **not** carried forward into `DataSource`. Existing `QuerySet` keeps the rewrite for backwards compatibility during migration and has it removed during Phase 4. This resolves issue #487.

String filter expressions beyond equality land via `DataSource.QueryBuilder.where(*expressions: str)` (issue #512) — e.g. `.where("size > 1000000000", "state != 'offline'")` — which the cache backend concatenates with the dict-derived equality fragments and hands to `ClusterMetadataDB.query_with_filters` as a single ANDed list. v1 supports `.where()` on the cache path only; live and partial-fetch paths raise `NotImplementedError`. The typed field-reference DSL (e.g. `OntapVolume.svm.name == "vs1"`) remains deferred as issue #497 and will eventually compile down to the same string-expression shape that `.where()` already accepts.

### 4. Per-call source override

`DataSource` accepts `source="auto" | "cache" | "live"` on every read:

- `auto` (default) honors the per-field `cache_strategy` declared on `FieldMapping`.
- `cache` raises if asked for a `realtime` field.
- `live` bypasses the cache entirely.

The CLI `--live` flag from issue #472 becomes a passthrough to `source="live"`, which generalizes the existing narrow override to every read path.

### 5. `requires_explicit_fetch` handling

Fields marked `requires_explicit_fetch=True` in their `FieldMapping` are **not** served by `source="auto"` unless explicitly named in the `fields=[...]` parameter, or `source="live"` is set. This preserves the existing semantics where bulk collection skips expensive fields (ADR-0004 evolution).

### 6. `cache_strategy="derived"` handling

Derived fields are served from cache (post-collection compute, persisted). No special routing — the accessor reads them alongside regular cached fields.

### 7. Backend registry keyed by `TypeMapping.api_type`

`DataSource` maintains an internal `dict[str, Backend]` keyed by the existing `TypeMapping.api_type` field (default `"ontap"`). Adding a new backend (AIQUM, OCCM, DII, Azure events) means writing one `Backend` subclass and registering it against the `api_type` string. **No new field on `FieldMapping` or `TypeMapping`.** v1 ships with one backend, `OntapBackend`, that wraps the existing cache path (`FieldGroupFetcher`, `LazyClusterMetadata`) and the existing live REST paths (`QuerySet`, `fetch_realtime`).

### 8. Sync only

v1 is synchronous to match the existing cache layer and CLI. Async is a future ADR if a real async caller appears.

### 9. Reads only

v1 covers reads. `Mutation` (`src/pynetappfoundry/query/mutation.py`) stays as-is. Cache invalidation on writes is its own design problem and is deferred to a future ADR.

### 10. Existing surfaces become thin shims during migration

`LazyClusterMetadata`, `QuerySet`, `fetch_realtime`, and the `nf cache check` / `nf cache query` CLIs become thin shims over `DataSource` in Phase 3. Public surfaces are preserved during migration so existing call sites move incrementally, and cleanup happens in Phase 4.

## Rationale

The four existing read paths have diverged across input shape, output shape, and source-override mechanism, and issue #485 keeps adding new call sites against the old shapes. A single accessor that routes on `FieldMapping` metadata is the smallest change that both stops the drift and unblocks multi-API backends, because `FieldMapping` and `parse_api_response()` already do most of the work.

### Consequences

**Positive:**

- One read API and one model shape across every surface. Mypy and IDE support work uniformly.
- Metadata-driven backend extensibility — adding AIQUM/OCCM/DII/Azure events means dropping a `FieldMapping` and registering a `Backend`, nothing else.
- Resolves issues #487 (filter input ergonomics) and #488 (realtime output shape) in one coherent move instead of fixing each surface separately.
- Simpler migration story for issue #485: new call sites target `DataSource` directly and stop accumulating against the old shapes.
- The `_fetched_fields` mechanism gives diff, audit, and compare code a signal it lacks today.

**Negative:**

- Temporary code duplication during the shim phase (Phase 3) while old and new paths both exist.
- One more abstraction layer to understand.
- Potential routing-layer latency over today's direct paths. Phase 2 must benchmark the spike against the same workload before committing to the design.
- Larger blast radius if the design is wrong — the spike (Phase 2) exists specifically to de-risk this.

**Neutral:**

- ADR-0010 (ClusterEntry namespace access pattern) is partially superseded. The cache-vs-live fetch routing it describes moves into `DataSource`. `ClusterEntry` retains its config/identity role and continues to hold credentials and the cluster name.

### Alternatives Considered

- **Keep four separate paths (status quo).** Rejected: issues #487/#488/#485 keep recurring as separate decisions. Each new endpoint multiplies the surfaces and the convention drift.
- **Build a thicker abstraction (full Repository pattern with query building, ORM, etc.).** Rejected for a structural reason, not an effort one: this project is an external-API reader, not a database client. A query builder over four backends with non-overlapping query capabilities (ONTAP REST, AIQUM, OCCM/Connector, DII) has only three options, all bad: (a) be the lowest common denominator and expose less than `QuerySet` already does; (b) leak the abstraction so the user has to know which queries work on which source — defeating the point of unifying; or (c) re-implement each backend's filter grammar in Python and keep it in sync as the underlying APIs evolve. `FieldMapping` already does the only abstraction that earns its keep here — translating model attribute names ↔ API field paths — and the rest of an ORM (transactions, schema migration, DDL) has no analogue in this domain.
- **Fix issues #487 and #488 separately on each existing surface.** Rejected: does not address the "more new commands keep being added" problem in #485, and leaves the convention drift in place.
- **Wrap each model in a `Tracked[T]` generic instead of an instance attribute on the base class.** Rejected: more cognitive overhead, breaks the "looks like a normal model" promise, and Pydantic generics have rough edges with `extra="allow"`.
- **Typed filter expressions via generated field-reference objects** (e.g. `ds.query(OntapVolume).filter(OntapVolume.svm.name == "vs1")` instead of `filter({"svm.name": "vs1"})`). **Deferred, not rejected.** The dict-based input shape locked in by this ADR is forward-compatible: a typed DSL would be a front door that compiles down to the same dict shape `DataSource` already accepts. Worth revisiting after the Phase 2 spike, when real call sites can show whether stringly-typed keys are tripping people up. Tracked as issue #497.

### Implementation Phases

This ADR is Phase 1 of a four-phase plan. The full plan is in issue #495.

- **Phase 1 — ADR (this PR).** Pure docs. Locks in the design points above.
- **Phase 2 — Spike.** End-to-end implementation against one model (`OntapVolume`, chosen because it exercises cached, derived, realtime, and `requires_explicit_fetch` fields). New code under `src/pynetappfoundry/data/` plus the `_fetched_fields` attribute on `OntapModel`. No existing surface is migrated yet.
- **Phase 3 — Shim migration.** Five follow-up issues, one per existing surface (`LazyClusterMetadata`, cache CLIs, `QuerySet`, realtime functions, remaining #485 call sites). Each surface becomes a thin shim over `DataSource`. This phase absorbs the remainder of issue #485.

  **Phase 3 progress:**

  **Phase 3 prerequisites:**

  - Issue #512 — `DataSource.QueryBuilder.where(*expressions)` for SQL-like
    filter expressions on the cache path — landed independently of the
    shim migrations to unblock Phase 3e (`nf cache check` shim, issue
    #509), whose `--where` flag requires non-equality filter expressions
    that `filter({...})` cannot express.

  - Phase 3a — `OntapBackend.query()` partial-fetch (issue #500, merged in PR #501).
  - Phase 3b — `LazyClusterMetadata` migrated to a `DataSource` shim (issue #502). `_load_field_group()` now routes every per-model read through `DataSource.query(source="cache")`, reassembling the results into the corresponding `CachedClusterMetadata` sub-model. `FieldGroupFetcher` is retained as an opt-in fallback for the live-only call site (`ClusterEntry._build_live_metadata`) and will be removed in Phase 4.
  - Phase 3c — `QuerySet` migrated to a `DataSource` shim (issue #506). A new keyword-only `config: Config | None = None` ctor kwarg opts each `QuerySet` instance into routing terminal methods (`all`, `first`, `get`, `count`, `__iter__`) through `DataSource.query(source="live")`. Order/limit flow through the filter dict as raw query-param entries (no new public methods on `DataSource.QueryBuilder`); `count()` drops down to a new private `OntapBackend._count_live()` helper that hits `call_endpoint` with `return_records=false`. The legacy direct-client path remains as the `config=None` fallback for call sites without a `Config` in scope (notably `query/related.py`) and is removed in Phase 4.
  - Phase 3d — `query/realtime.py` migrated to a `DataSource` shim (issue #508). The four public functions (`fetch_realtime`, `fetch_realtime_collection`, `watch_realtime`, `compare_realtime`) no longer hand-build live REST URLs or parse raw response dicts; they construct a `DataSource(config)` and route through `DataSource.get(..., source="live")` (single-resource paths) or `DataSource.query(..., source="live").filter(...).fields(...)` (collection path). Output shape is preserved as dotted-key `dict[str, Any]` via a private `_model_to_dotted_dict()` projector (Phase 4 replaces it with Pydantic model instances per ADR-0012 §1). The public signatures now take positional `config: Config, cluster: str` after `model_class`, replacing the legacy `client:` parameter — possible without a migration layer because no production code calls these functions. `watch_realtime` builds a single `DataSource` before its polling loop and reuses it across all iterations. The old helpers `_parse_realtime_record()` and `_realtime_api_fields()` are removed; `_attr_to_api_path()` is retained to translate kwarg-style filters in `fetch_realtime_collection`. The resulting `?fields=` query string is more verbose than the pre-shim version (e.g. `metric.iops.read,metric.iops.write` rather than the deduped-to-`metric` shortcut) but functionally equivalent — ONTAP honors both.

- **Phase 4 — Cleanup.** Remove the dunder-to-dot rewrite from `QuerySet`, remove the dotted-key `dict` shape from realtime functions, remove `FieldGroupFetcher` (now unused once every reader is a `DataSource` shim), remove the back-compat `db_path` / `registry` / `fetcher` kwargs on `LazyClusterMetadata`, drop `cluster_entry._build_fetcher` / `_build_live_metadata`, write the `docs/usage/data-source.md` user guide, and update `docs/usage/query-layer.md` to position `QuerySet` as the lower-level surface.

### Links to Documentation

The user-facing guide for `DataSource` (`docs/usage/data-source.md`) does **not** exist yet — it will be created in Phase 4. This ADR will be updated with the doc link when that PR lands.

## Related Issues

- Issue #495: feat: unified DataSource for all cluster reads (parent of this ADR)
- Issue #487: filter input ergonomics (closed, superseded by #495)
- Issue #488: realtime output shape (closed, superseded by #495)
- Issue #485: CLI migration onto cache + on-demand fetch (paused pending this work)
- Issue #472: feat: add Config.no_cache flag and --live CLI option (origin of `--live`)

## Related Documentation

- [ADR-0001: Use SQLite for cluster metadata caching](0001-use-sqlite-for-cluster-metadata-caching.md)
- [ADR-0004: Declarative field mapping framework](0004-declarative-field-mapping-framework.md)
- [ADR-0006: Generalize field mapping for multi-API](0006-generalize-field-mapping-for-multi-api.md)
- [ADR-0010: ClusterEntry and namespace access pattern](0010-clusterentry-and-namespace-access-pattern.md) (partially superseded by this ADR)
- [ADR-0011: Nested models to replace flat model pattern](0011-nested-models-to-replace-flat-model-pattern.md)
- Source: `src/pynetappfoundry/cache/field_mapping.py`
- Source: `src/pynetappfoundry/cache/_registry.py`
- Source: `src/pynetappfoundry/cache/_lazy.py`
- Source: `src/pynetappfoundry/cache/_fetcher.py`
- Source: `src/pynetappfoundry/core/cluster_entry.py`
- Source: `src/pynetappfoundry/query/queryset.py`
- Source: `src/pynetappfoundry/query/realtime.py`
- Source: `src/pynetappfoundry/models/_base.py`
