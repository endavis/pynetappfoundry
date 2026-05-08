# ADR-0017: where-expressions are cache-only (rationale)

## Status

Accepted

## Context

ADR-0012 §49 and ADR-0015 §17 both state that `.where()`-string expressions and the non-equality typed DSL operators that compile to them (`<`, `>`, `!=`, `.in_()`, `.is_null()`, etc.) are supported only on the cache path. Live and partial-fetch paths reject them at chain time (`ValueError`) for cases the chain knows about, and at iteration (`NotImplementedError`) as defense-in-depth. Issue #618 (already merged) added the early `ValueError` validation so callers fail fast at construction rather than at iteration.

Neither existing ADR captures **why** the live paths are not expected to grow comparison support. The position keeps getting re-litigated whenever a caller hits the asymmetry, so this ADR records the rationale once and points future challenges at it.

## Decision

`.where()`-string expressions and the non-equality typed DSL operators that compile to them are supported only on the cache path. Live and partial-fetch paths reject them at chain time (`ValueError`) for cases the chain knows about, and at iteration (`NotImplementedError`) as defense-in-depth. The DII backend rejects them regardless of `source=` since it has no cache substrate.

## Rationale

The position is **"not yet implemented; no fundamental objection."** Specifically:

- There is no architectural objection to extending where-expression evaluation to live and partial-fetch paths. The current position is "no one has done the work," not "we have decided this is wrong."
- Translating where-expressions to ONTAP/DII filter syntax is an implementable problem. A well-designed PR that handles all current backends (and accepts the per-backend translation cost) would be accepted.
- The cache path is privileged today simply because SQLite already evaluates the full expression grammar. Adding a second evaluator for each live backend is work that nobody has chosen to do.

Because the position is "not yet implemented" rather than "rejected," issue #618 added early `ValueError` at chain time as the operational consequence: callers fail fast when constructing an incompatible query rather than discovering the gap mid-iteration. The early validation surfaces the asymmetry without committing to closing it.

This is intentionally an honest "soft" position rather than a hard architectural one. The cache-only constraint is a description of current implementation reality, not a principled rejection of the feature.

## Conditions for revisiting

A repeated, demonstrated pattern of caller pain — where the early-validation messages aren't enough and callers need real expression evaluation on live paths — is the most likely catalyst for revisiting this position.

This ADR does not enumerate an exhaustive list of triggers. Any future challenge to this position gets its own ADR with its own context and decision.

## Related Issues

- Issue #619: docs: ADR documenting why where-expressions are cache-only (this ADR)
- Issue #618: feat: early validation for where()/typed-DSL + incompatible source mode (operational consequence of this position)
- Issue #512: feat: `.where()` SQL-like cache filter expressions (original feature)
- Issue #497: feat: typed field-reference DSL (deferred typed front door that compiles to the same shape)

## Related Documentation

- [ADR-0012: Unified DataSource Accessor](0012-unified-datasource-accessor.md) -- §49 states the cache-only position for `.where()`
- [ADR-0015: DII backend live-only](0015-dii-backend-live-only-bare-array-envelope-offsetlimit-pagination.md) -- §17 states the cache-only position for the DII backend
- [DataSource user guide](../usage/data-source.md) -- "Cache-only constraint" section documents the user-facing behavior
