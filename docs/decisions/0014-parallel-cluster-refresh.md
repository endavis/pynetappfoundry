# ADR-0014: Parallel Cluster Refresh

## Status

Accepted

## Decision

`nf cache refresh --all` accepts a `--parallel-clusters N` flag (default `4`,
minimum `1`). When `N > 1`, clusters are collected concurrently using a
`ThreadPoolExecutor`; when `N == 1`, the command executes the historical
strictly-sequential code path unchanged.

The implementation follows a **workers collect, main thread persists** split:

- `_collect_cluster()` — worker-safe. Builds API/CLI clients, reads the
  previous history snapshot, runs `MetadataCollector.collect_all()`, and (in
  verbose mode) captures its own phase output into a Rich `Console(record=True)`
  buffer. Returns a `_CollectResult` dataclass; never touches `ClusterMetadataDB`
  or `CacheHistoryDB` for writes.
- `_persist_cluster()` — main-thread only. Computes the diff via
  `compute_diff()`, records history via `history_db.record_change()`, and
  writes the cache via `db.set()`. All database writes for every cluster flow
  through this function on the main thread.

For verbose parallel mode, each worker's captured buffer is flushed as a
single block on the main thread when its future completes, keeping per-cluster
output coherent. Cluster blocks may appear in any completion order; the
internal structure of each block (phase lines, summary) is preserved.

## Rationale

1. **SQLite single connection is not thread-safe.** `ClusterMetadataDB` keeps
   a single shared connection (`src/pynetappfoundry/cache/db.py:301`). Sharing
   it across threads is unsupported. Serialising every write on the main
   thread preserves the existing substrate with no cache-layer changes.

2. **Cluster collection is already independent.** Each cluster has its own
   API/CLI clients, its own configuration lookup, and no inter-cluster derived
   fields. Inter-phase ordering inside a cluster is already handled by the
   inner parallelism in `MetadataCollector._collect_all_parallel()`
   (`src/pynetappfoundry/cache/collector.py:605`), with `CLOUD` running
   sequentially after parallel phases. Outer cluster-level parallelism adds
   no new coordination.

3. **Workload is I/O-bound.** Per-cluster wall time is dominated by REST API
   calls and SSH round trips. Threads (not processes) are the right tool.

4. **4 × default expected speedup.** With 66+ clusters at ~1–2s each, a full
   refresh takes 66–132s sequentially. Four parallel workers reduce that to
   ~12–24s without increasing cache-layer surface area.

5. **`N == 1` preserves historical behaviour.** The sequential path remains
   in `_process_cluster()` unchanged, so users who want the old ordering or
   who hit an unforeseen parallelism bug can opt out with no behavioural
   difference. Existing tests on the sequential path continue to pass.

6. **Inner collector concurrency is unchanged.** `max_workers=8` inside
   `MetadataCollector` is retained. At default settings peak concurrency is
   roughly `4 × 8 = 32` worker threads, which is comfortable for a CLI tool
   against one API server per cluster.

### Consequences

**Positive:**

- 4 × default speedup on `nf cache refresh --all` with no cache-schema or
  collector changes.
- No new DB-threading surface area — the cache substrate is unchanged.
- Failure of one cluster does not block others; each future is independent
  and its failure is reported in the existing failure summary.
- Opt-out (`--parallel-clusters 1`) is a stable fallback.

**Negative:**

- In parallel verbose mode, cluster blocks complete in non-deterministic
  order (by wall-clock). The per-cluster block is internally coherent, but
  the overall ordering is not the configuration order.
- Peak connection count per host is higher; clusters that share an egress
  proxy or have per-client rate limits may need to lower `--parallel-clusters`.
- Log lines from parallel workers interleave in the log file; per-cluster
  context is carried via a `[cluster_name]` prefix on refresh-level logs.

**Neutral:**

- Single-cluster invocations (`nf cache refresh c1`) always use the
  sequential path regardless of the flag — no change in behaviour.
- `N` is clamped to `min(N, len(clusters_to_refresh))` so a large `N` with
  a small fleet does not oversubscribe the executor.

### Alternatives Considered

- **Share the SQLite connection across threads.** Rejected: requires changing
  `ClusterMetadataDB` and all downstream code to use a connection-per-thread
  or a lock-wrapped connection. Touches the cache substrate for a benefit
  (parallel writes) that is not needed — writes are short and fast compared
  to the collection phase.
- **One connection per worker thread.** Rejected: still requires substrate
  changes, and SQLite's write serialisation means concurrent writers don't
  gain throughput anyway.
- **Process pool instead of thread pool.** Rejected: the workload is I/O
  bound, processes add pickling overhead for the `Config` object and
  API/CLI clients, and would complicate the single-connection DB writes.
- **Keep the existing sequential behaviour.** Rejected: 66+ clusters at
  1–2s each is a real operational pain point (issue #149).

## Related Issues

- Issue #149: feat: parallelize cluster refresh in `nf cache refresh --all`

## Related Documentation

- [ADR-0001: Use SQLite for cluster metadata caching](0001-use-sqlite-for-cluster-metadata-caching.md)
- [ADR-0003: Use base SQLiteDB class with version-based migrations](0003-use-base-sqlitedb-class-with-version-based-migrations.md)
- [Cache System Reference](../reference/cache.md)
- CLI command: `nf cache refresh --all [--parallel-clusters N]`
- Source: `src/pynetappfoundry/cli/commands/cache/refresh.py` (`_collect_cluster`, `_persist_cluster`)
- Source: `src/pynetappfoundry/cache/collector.py` (inner per-phase parallelism)
- Source: `src/pynetappfoundry/cache/db.py` (single SQLite connection)
