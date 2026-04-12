# ADR-0013: DataSource as a Thin Facade Over the Collector

## Status

Proposed

Supersedes [ADR-0012: Unified DataSource Accessor for All Cluster Reads](0012-unified-datasource-accessor.md).

## Context

ADR-0012 introduced `DataSource` as the single read accessor for all cluster data and committed to ten design points. Phase 2 shipped a spike against `OntapVolume`; Phase 3 migrated several commands onto shims; Phase 4 cleanup has not started. During Phase 3 we hit a pattern the spike did not anticipate: **every real consumer migration exposed a gap in `DataSource`'s ability to handle ONTAP's actual endpoint diversity.** The fixes so far:

- PR #522/#527 — `fields=*` preservation in the live URL builder
- PR #528/#529 — cache-miss → live fallback on `source="auto"`
- Issue #524 — blocked on singleton endpoints (flat-dict responses)

A coverage audit (parent issue #530) then enumerated ten distinct gaps, of which six are structural: singleton endpoint shapes (#531), SSH/CLI backends (#532), non-ONTAP backends (#533), composite/non-UUID identifiers (#535), path-parameter endpoints (#536, ~60 mappings), and post-query hooks for derived fields (#537). The common thread: **`OntapBackend` in `src/pynetappfoundry/data/backends.py` is re-implementing, on the live side, problems that `MetadataCollector` (`src/pynetappfoundry/cache/collector.py`) already solves on the write side.** The collector handles singletons (`paginate=False`), parent-keyed endpoints (`{volume.uuid}` substitution), post-collection hooks (`compute_is_ha`), SSH-backed models (`CloudMetadata`), derived fields, composite identifiers, and chunking. `OntapBackend` is being patched, gap by gap, to acquire the same capabilities.

Phase 3 also revealed one real consumer pattern that `DataSource` handles well and the collector does not: **partial fetches that merge cached "stable" fields with live "realtime" fields on the same model**. A query for `OntapVolume` that needs `name`, `uuid`, `svm.name` (cached) and `metric.iops.read`, `metric.latency.*` (realtime) is served today by `_query_partial`: cache read for the stable fields, a thin live fetch restricted to the realtime field paths, and a merge by identifier. An audit (`grep cache_strategy="realtime"` across all mappings) confirms that 846 of 863 realtime fields are inline sub-fields of standard collection endpoints; 17 live on 4 parent-keyed mappings; **none** live on singleton endpoints or dedicated `*/metrics` endpoints. The realtime path has a genuinely narrower problem shape than the whole-model path.

Separately, the cache has an explicit design property worth preserving: `CachedClusterMetadata.cached_at` (`src/pynetappfoundry/cache/_metadata.py:78`) carries a single cluster-level "as of" timestamp, populated when `nf cache refresh` runs. The cache is a **snapshot**: the intent is that a cluster's cached state reflects one point in time, not a patchwork of per-field or per-model refresh times. ADR-0012 did not address this; the cache-miss fallback and live-path behavior in the spike were ambiguous about whether live fetches should persist back into the cache.

This ADR revises ADR-0012 with the learnings from the gap audit, the realtime-field audit, and the snapshot-consistency requirement.

## Decision

`DataSource` remains the single read accessor for all cluster data. Its public surface (`DataSource.query()`, `DataSource.get()`, `source="auto"|"cache"|"live"`, `QueryBuilder.filter()/.where()/.fields()`, Pydantic return shape, `_fetched_fields` tracking) is unchanged from ADR-0012. The **implementation strategy** changes. Ten points replace the ten from ADR-0012:

### 1. The collector owns "how to fetch a whole model"

Every problem shape that `OntapBackend` has been growing flags for — singletons, parent-keyed endpoints, composite identifiers, post-fetch hooks, SSH/CLI, non-envelope responses — is owned by `MetadataCollector`. `OntapBackend` is no longer a parallel live-fetch implementation; it is a **thin delegate** that invokes the collector's fetch function for the requested type. One place knows how to talk to ONTAP per model type; one place grows when new quirks appear.

### 2. Fetch is separated from persist

`MetadataCollector` today interleaves "fetch from ONTAP" with "write to cache substrate." Those are split: a pure `fetch_<type>(cluster, config) → list[Model]` function per model type (or a dispatch table keyed by `TypeMapping`), and a separate `persist_<type>(cluster, instances)` step. Both `nf cache refresh` (which calls fetch + persist) and `DataSource` live reads (which call fetch only) go through the same fetch functions. No duplicate implementations.

### 3. Cache is a single-point-in-time snapshot

The cache for a given cluster reflects one refresh event. `CachedClusterMetadata.cached_at` is the authoritative "as of" timestamp; there is no per-model or per-field staleness tracking and none will be added. Consumers that care about freshness introspect `cached_at`. `DataSource` exposes a helper (`DataSource(config).snapshot_time(cluster) → datetime | None`) so consumers do not have to reach into internals.

### 4. Live fetches never persist

`source="live"` invokes the collector's pure fetch function and returns the result directly to the caller. It does **not** write to the cache substrate. Cache-miss fallback under `source="auto"` also does not persist. Snapshot consistency is preserved: the only thing that updates the cache is an explicit `nf cache refresh`. Users who want fresh data in the cache run the refresh; users who want fresh data in their current call use `source="live"`.

### 5. Post-fetch hooks run on every fetch

Derived-field hooks (e.g. `compute_is_ha` from ADR-0012 §6) move from "runs after collection, before persist" to "runs on the pure fetch function's output, always." Both `source="live"` and `source="cache"` return models with derived fields populated. This closes the `ClusterInfo.is_ha=False` live-read gap without any consumer-visible change.

**Cross-model hook dependencies — `FieldMapping.depends_on` (issues #541, #547).** Cross-model hook dependencies are declared on the `FieldMapping` itself via `depends_on: tuple[type[BaseModel], ...] = ()`. The generic `fetch()` dispatcher iterates every derived field's `depends_on` tuple and, for each dependency absent from the shared `results_cache`, recursively calls `fetch()` to populate it (keyed by the dependency's `__name__`). Callers that pre-populate the cache — notably `MetadataCollector`, which threads a shared `_results_cache` through `collect_all()` — short-circuit the recursive fan-out. Phase 2 (#541) introduced the mechanism as a hook-name-specific branch for `compute_is_ha`; issue #547 generalized it when the second cross-model derived field (`compute_is_cloud`, used to gate the SSH-backed cloud-metadata fetch for on-prem clusters) landed. Both `compute_is_ha` and `compute_is_cloud` now declare `depends_on=(OntapNodeResponse,)` and share the same generic fan-out path. The collector's existing `_evaluate_derived_fields()` step is preserved unchanged so the ~80 mappings with intra-record derived fields keep their current evaluation path; only cross-model dependencies go through `depends_on`.

### 6. Source modes are defined in terms of the snapshot

- **`auto`** (default): read the cache snapshot for cached (stable and derived) fields. For models with `cache_strategy="realtime"` fields requested, merge in a thin live-fetch (see §7). If the cache substrate is empty for this cluster (bootstrap case), fall back to a pure live fetch via the collector's fetch function — non-persisting.
- **`cache`**: read the snapshot. Raise if the caller asks for a `cache_strategy="realtime"` field. No fallback.
- **`live`**: invoke the collector's pure fetch function. No cache interaction, no persist. Post-fetch hooks still run.

### 7. Realtime-field live path stays in `DataSource`

The partial-fetch merge path for `cache_strategy="realtime"` fields is genuinely narrower than the whole-model path: 846 of 863 realtime fields are inline sub-fields of standard collection endpoints, so a restricted-field live query (`?fields=metric.iops.read,metric.latency.*&uuid=<id>`) is sufficient. This path stays in `DataSource` (or its delegating backend) as a dedicated thin fetcher. The 17 realtime fields on 4 parent-keyed mappings (`storage/volumes/snapshots`, `snapmirror/relationships/transfers`, `application/consistency_groups/snapshots`, `svm/migrations/volumes`) need path-parameter substitution — the realtime path inherits a narrow, scoped subset of Gap 6 for those four cases. This is a small, concrete piece of code, not generic path-param support.

**§7 amendment (issue #544 — parent-keyed partial-fetch).** Partial-fetch (cache + realtime live merge) on the four parent-keyed mappings is now supported via a grouped-by-parent algorithm in `OntapBackend._query_partial()`. The implementation:

1. Parses the `{placeholder}` from `TypeMapping.api_endpoint` (e.g. `{volume.uuid}`) to discover the child→parent reference field.
2. Groups cached children by parent UUID using `_resolve_dotted_attr` on the parsed reference field.
3. For each parent group, builds a resolved URL via `TypeMapping.build_parameterized_url`, adds pipe-OR identifier filters chunked at `_BATCH_SIZE`, and fetches live data per parent.
4. Merges live results into cached instances by `identifier_field`, the same way the non-parent-keyed path does.

For models without a child→parent back-reference (e.g. `OntapSvmMigrationVolume`, whose child records have no attribute pointing back to the parent `svm_migration.uuid`), the algorithm falls back to querying the parent model from cache, then iterates all discovered parents. ONTAP's per-parent endpoint naturally returns only the children belonging to that parent, so identifier-based merge handles deduplication.

All four affected mappings now declare `identifier_field`:

- `OntapSnapshot` — `identifier_field="uuid"`
- `OntapSnapmirrorTransfer` — `identifier_field="uuid"`
- `OntapConsistencyGroupSnapshotResponse` — `identifier_field="uuid"`
- `OntapSvmMigrationVolume` — `identifier_field="volume.uuid"` (dotted; no top-level uuid)

Resolved by #544.

### 8. `.get()` is a convenience over `.query()`

`DataSource.get(model, cluster=X, id=...)` is internally `.query(model, cluster=X).filter({identifier_field: id})` followed by first-or-`None`. Same routing, same backend, same realtime merge. The independent `OntapBackend.get()` method is removed; composite-identifier translation (Gap 5, issue #535) happens at the query-filter layer, not at the backend.

### 9. Backend ABC preserved, meaning changed

`DataSource._BACKENDS` keyed by `TypeMapping.api_type` is preserved from ADR-0012 §7, but its role changes. Backends no longer implement "how to fetch X from an API end-to-end"; they are thin delegators to per-domain fetch layers. `OntapBackend` delegates to `MetadataCollector`. A future `AIQUMBackend` delegates to an AIQUM-specific collector. Adding a new API is still "write one backend class and register it," but the backend class is ~50 lines of delegation rather than a parallel implementation of all the collector's logic.

### 10. Existing ADR-0012 design points retained verbatim

- §1 (return shape: Pydantic instances) — unchanged.
- §2 (`_fetched_fields` tracking) — unchanged.
- §3 (dotted-string filter input, `.where()` string expressions) — unchanged.
- §5 (`requires_explicit_fetch` handling) — unchanged.
- §8 (sync only) — unchanged.
- §9 (reads only) — unchanged.

## Rationale

The 2023 spike committed to a plausible hypothesis: `DataSource` would own both read paths (cache and live) as parallel implementations against a shared `FieldMapping`/`TypeMapping` substrate, and the collector would remain a separate concern that "just happened" to write to the cache. Phase 3's gap audit made it clear the two are not parallel: the collector handles ~20× more endpoint diversity than `OntapBackend`, and every gap `OntapBackend` has been fixing is one the collector already solved. The choice is whether to keep patching `OntapBackend` toward feature-parity with the collector (Gaps 1/5/6/7/10, each its own PR) or to acknowledge the collector as the canonical fetch layer and make `OntapBackend` a thin facade over it. The facade approach absorbs five gaps for free, preserves the single-entry-point user experience from ADR-0012, and avoids adding any more flags to `TypeMapping`.

The snapshot-consistency requirement (§3/§4) is not a new constraint — it's how `CachedClusterMetadata.cached_at` has worked since ADR-0001 — but ADR-0012 was ambiguous about it. Making it explicit forces the "fetch vs persist" split in §2 and prevents future implementations from silently re-warming individual cache rows, which would degrade the snapshot guarantee without any consumer noticing.

### Consequences

**Positive:**

- Five of ten coverage gaps (#531, #532, #535, #536, #537) are absorbed into the collector, which already solves them. Each becomes a small delegation PR rather than a parallel implementation PR.
- `TypeMapping` stops growing flags. `response_shape`, `identifier_field` composite handling, path-parameter substitution, SSH dispatch — all stay where they already live in the collector.
- Snapshot-consistency is explicit and enforceable. Reviewers have a clear rule ("live fetches never persist") instead of case-by-case judgment.
- Derived fields work on live reads (§5), which was a known limitation of the ADR-0012 design.
- The `.get()` / `.query()` duplication in `OntapBackend` disappears.

**Negative:**

- Phase 3 work already merged (Phases 3a–3f) was written against the ADR-0012 model. Migrating to the ADR-0013 model means rewriting `OntapBackend` and the shims that depend on its public shape. Phase 3 shims are unchanged at the `DataSource` public API level — consumers do not see the change — but `OntapBackend` internals are rewritten.
- The collector must be refactored to split fetch from persist. This is ~500 lines of restructuring in `collector.py` and touches every `collect_*` method. Not trivial, but contained to one module.
- Open PRs/issues from the ADR-0012 gap-fix sequence (#531, #535, #536, #537) are closed as "absorbed into ADR-0013" rather than implemented as designed. The plans posted on those issues become historical.

**Neutral:**

- `_fetched_fields` tracking, `QueryBuilder` chaining, source modes, and Pydantic return shape are unchanged. Every command migration from Phase 3 (`nf cache check/query`, `licenses check/savings`, `reports locks/html/space_usage`, `utils validate`) continues to work with no consumer-side changes.
- ADR-0010 partial supersession from ADR-0012 is preserved.

### Alternatives Considered

- **Keep patching `OntapBackend` (ADR-0012 status quo).** Rejected after the gap audit. Six issues in the pipeline, each re-implementing collector logic in a second place. Phase 4 cleanup becomes harder, not easier, as more code accumulates.
- **Cache-first only, no live fallback.** Rejected. Some consumers genuinely need fresh data without a full refresh (realtime metrics, diagnostic commands, the `--live` flag from #472). A pure-read cache breaks those use cases.
- **Split the abstraction into `DataReader` (cache) and `DataFetcher` (live).** Rejected. Two entry points defeats the ADR-0012 unification goal, and most consumers (the `source="auto"` default) genuinely want both transparently. The collector-as-backend approach gives one entry point and one mental model.
- **Extend the collector to do field-level partial fetches.** Rejected as scope creep. The collector's job is "produce a complete row." The realtime merge is structurally different (thin, fast, inline sub-fields) and belongs in `DataSource` as a dedicated path, not in the collector.
- **Per-model or per-field staleness timestamps.** Rejected explicitly. The user's stated preference is snapshot consistency: one cluster-level `cached_at`, no tracking. Simpler mental model, simpler cache schema, and no new code paths.

### Implementation Phases

This ADR is **Phase 1** of a three-phase plan. A new parent issue supersedes #495's Phase 3/4 plans.

- **Phase 1 — ADR (this PR).** Pure docs. Locks in the design points above. Mark ADR-0012 as Superseded. Close #531, #535, #536, #537 as "absorbed into ADR-0013"; close #530 once the new parent issue is filed. Keep #532 and #533 open as deferred (SSH and non-ONTAP backends are still Phase 4+ work, but they plug into the collector, not into `OntapBackend`).
- **Phase 2 — Collector fetch/persist split.** Refactor `MetadataCollector` so every `collect_<type>` method splits into a pure `fetch_<type>` and a `persist_<type>`. `nf cache refresh` chains them; `DataSource` live reads call `fetch_<type>` only. Hook invocation (`compute_is_ha` and siblings) moves to the fetch layer. No `DataSource` consumer changes.
- **Phase 3 — `OntapBackend` rewrite.** Rewrite `OntapBackend` as a thin delegator over the collector's fetch layer, with a dedicated realtime live-fetch path for the partial-fetch merge case (§7). Remove `OntapBackend.get()`. Update `DataSource.get()` to be a `.query()` convenience wrapper. Verify every Phase 3 shim (from ADR-0012 Phase 3a–3f) still passes its tests — no consumer changes expected.
- **Phase 4 — `nf reports html` home_node fix (#524).** Unblocked by Phase 3. Migrates the last non-shim `QuerySet(...)` call sites through the new backend, including `ClusterInfo` via the collector's singleton-aware fetch.

### Links to Documentation

- [DataSource User Guide](../usage/data-source.md) — unchanged at the public-API level. Update §"Source modes" to reflect the explicit no-persist guarantee.

## Related Issues

- Issue #495: feat: unified DataSource for all cluster reads (parent of ADR-0012; this ADR revises its Phase 3/4 plan)
- Issue #530: epic: DataSource coverage gap expansion (closed by this ADR; gap audit informs the new design)
- Issue #524: bug: `nf reports html` shows Unknown for LIF home node (unblocked by Phase 3 of this ADR)
- Issue #531: feat: DataSource singleton endpoint support — closed, absorbed into ADR-0013
- Issue #535: feat: DataSource composite and non-UUID identifiers — closed, absorbed into ADR-0013
- Issue #536: feat: DataSource path-parameter endpoints — closed, absorbed into ADR-0013
- Issue #537: feat: DataSource post-query hooks for derived fields — closed, absorbed into ADR-0013
- Issue #532: feat: DataSource SSH/CLI backend — deferred, retargeted to plug into collector
- Issue #533: feat: DataSource non-ONTAP backends — deferred, retargeted to plug into collector
- Issue #534: feat: audit Pydantic models without TypeMappings — unchanged
- Issue #538: feat: DataSource pagination/chunking edge cases — re-scoped to the realtime live-fetch path only

## Related Documentation

- [ADR-0001: Use SQLite for cluster metadata caching](0001-use-sqlite-for-cluster-metadata-caching.md)
- [ADR-0004: Declarative field mapping framework](0004-declarative-field-mapping-framework.md)
- [ADR-0006: Generalize field mapping for multi-API](0006-generalize-field-mapping-for-multi-api.md)
- [ADR-0010: ClusterEntry and namespace access pattern](0010-clusterentry-and-namespace-access-pattern.md) (partially superseded by ADR-0012, retained under ADR-0013)
- [ADR-0011: Nested models to replace flat model pattern](0011-nested-models-to-replace-flat-model-pattern.md)
- [ADR-0012: Unified DataSource Accessor for All Cluster Reads](0012-unified-datasource-accessor.md) (superseded by this ADR)
- Source: `src/pynetappfoundry/cache/collector.py` (canonical fetch layer under this ADR)
- Source: `src/pynetappfoundry/cache/_metadata.py` (snapshot model, `cached_at` timestamp)
- Source: `src/pynetappfoundry/data/source.py` (public facade, unchanged at the API level)
- Source: `src/pynetappfoundry/data/backends.py` (rewritten as thin delegator in Phase 3)
