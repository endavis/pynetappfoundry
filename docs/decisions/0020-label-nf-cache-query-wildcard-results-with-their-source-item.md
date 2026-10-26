---
title: "ADR-0020: Label nf cache query wildcard results with their source item"
description: Label nf cache query wildcard and filter results with the array item they came from, by name/svm.name/uuid/index, and switch their JSON shape to a list of key/value records.
date: 2026-10-26
audience:
  - contributors
tags:
  - adr
---

# ADR-0020: Label nf cache query wildcard results with their source item

## Status

Accepted

## Context

`nf cache query` resolves wildcard (`[*]`) and filter predicate (`["field=value"]`) paths by
delegating to `get_nested_value()` (`src/pynetappfoundry/utils/dict_path.py`), which returns a
flat list of values with no record of which array item each value came from. For a query like
`protocols.cifs_services[*].security.session_security`, the output was a bare list:

```
testcluster:
  protocols.cifs_services[*].security.session_security:
    [
      "none",
      "sign"
    ]
```

There was no way to tell which SVM had `none` and which had `sign`, and duplicate values (two
`"none"` entries) collapsed any remaining positional meaning once a result was piped through
`--csv` or `--json` and re-sorted. The only workaround was querying an identifying field alongside
the target field and relying on index alignment across two separate wildcard results -- fragile,
and silently wrong if either field was missing on some item (#848).

## Decision

1. **New function, old one unchanged.** `get_nested_value_with_identifiers()` is added to
   `utils/dict_path.py` for wildcard and filter predicate paths. `get_nested_value()` is
   untouched -- `cache/check.py` and `query/realtime.py` call it directly and must keep seeing
   flat lists.

2. **Identifier order: `name`, `svm.name`, `uuid`, then array index.** For each array item,
   `_resolve_identifier()` tries `name`, then `svm.name`, then `uuid`, taking the first key present
   with a non-empty, non-`None` value. An item matching none of them falls back to its array
   index, rendered as `[i]`. This order was chosen because `name` and `svm.name` are the fields a
   cluster administrator recognizes at a glance (an SVM, volume, node, or LIF name), `uuid` is
   always present on ONTAP REST objects but not human-readable, and the index is the fallback of
   last resort -- it is always available but carries no meaning across runs.

3. **`--key <path>` overrides the order for the whole query.** When a user knows which field
   identifies their items (e.g. `--key svm.name`), it replaces the default order outright for
   every wildcard or filter field in that invocation; the index fallback still applies if the
   chosen key is absent on some item.

4. **Nested wildcards compose identifiers with `/`.** `a[*].b[*].c` labels each result
   `outer_ident/inner_ident` (e.g. `svm1/vol1`), composed recursively so arbitrarily deep wildcard
   nesting still produces one flat identifier per leaf value.

5. **Duplicates are kept, never merged.** Two items that resolve to the same identifier (same
   name, or neither has one and they share an index by coincidence) appear as two separate
   `(identifier, value)` pairs. Collapsing them into a dict keyed by identifier would silently
   drop data -- the exact failure mode in the original bug report.

6. **JSON output changes to a list of `{"key", "value"}` records.** `--json` on a wildcard or
   filter field now serializes as a list of records instead of a flat array:

   ```json
   {"key": "svm1", "value": "none"}
   ```

   A list was chosen over an object keyed by identifier specifically because of point 5: an
   object would silently drop one of two items that share an identifier (or share the index
   fallback). A list of records never drops data, at the cost of not being a map scripts can
   index directly by identifier -- callers that want that can build it themselves, now
   confident no entries were lost. **This is a breaking change** for any script parsing the
   previous flat-array JSON shape for a wildcard or filter field.

7. **CSV gets a `key` column, added only when needed.** `--csv` inserts a `key` column
   immediately after `cluster`, but only when the query has at least one wildcard or filter
   field -- plain queries keep their existing column layout untouched. When a query has several
   wildcard/filter fields, the shared `key` column is sourced from the first such field (by
   position in the field list); the others are aligned to it by array position, matching the
   pre-existing (undocumented) assumption that parallel wildcard fields have the same length.

8. **Raw output is one `key<TAB>value` line per item**, `--raw`'s existing contract (one line per
   value, suitable for piping to other tools) extended with a identifier column rather than
   replaced.

9. **Text output lists `<key>: <value>` per item under the field**, matching the shape proposed
   in the issue:

   ```
   testcluster:
     protocols.cifs_services[*].security.session_security:
       svm1: none
       svm2: sign
   ```

10. **Non-wildcard queries are unaffected.** A field path without `[*]` or a filter predicate
    continues to resolve through `get_nested_value()` and render exactly as before, in every
    output format.

## Rationale

- **A list, not a dict, because collisions are not edge cases here.** SVMs, volumes, and LIFs
  routinely share names across clusters' child scopes, and the fallback-to-index path produces
  the same identifier whenever two sibling arrays happen to align. An identifier-keyed JSON
  object would need either a documented (and surprising) overwrite rule or a secondary
  disambiguation scheme; a list of records needs neither, and the cost -- one extra level of
  structure in the JSON -- is small next to "a result silently vanished."

- **The default order favors what a human recognizes over what is always present.** `uuid` is
  the one field guaranteed present on nearly every ONTAP REST object, which would make it the
  "safest" default by availability. It was placed last anyway because the point of labelling
  results is to make `nf cache query`'s output legible without a second lookup; a UUID does not
  serve that purpose as well as a name does, and the index fallback already covers the case
  where no human-readable identifier exists.

- **`--key` replaces the order outright, rather than prepending to it**, so the override behaves
  predictably: the same field is tried for every wildcard/filter field in the query, with no
  implicit scanning through the default list first for fields where the chosen key happens to be
  absent.

- **The CSV `key` column is conditional, not always present**, because every existing non-wildcard
  CSV consumer's column layout (`cluster,field1,field2,...`) must keep working -- the breaking
  change is scoped to the wildcard/filter shape, not to CSV output as a whole.

## Consequences

- Scripts that parsed `--json` output for a wildcard or filter field against the old flat-array
  shape must be updated to read `{"key", "value"}` records instead. The commit and PR carry a
  `BREAKING CHANGE:` footer with this migration note.
- Scripts that relied on querying two wildcard fields and zipping them by index (the workaround
  described in #848) can query one field with `--csv` or `--json` and get the identifier directly,
  removing the fragile alignment assumption.
- `--key` is a single override path for the whole query; a future enhancement could allow a
  per-field override (e.g. `field1:key1,field2:key2`) if that need materializes, but no such need
  is known today.

## Related Issues

- Issue #848: feat: label `nf cache query` wildcard results with the item they came from (this
  ADR)
- Issue #190: filter predicates for `nf cache query` (the filter-predicate access form this ADR
  also labels)
- Issue #592: empty wildcard/filter results display (the existing "skip empty results" behavior
  this ADR leaves unchanged)

## Related Documentation

- [CLI Reference -- Cache Management](../reference/cli.md#cache-management) -- `nf cache query`
  examples, including `--key` and the labelled wildcard/filter output shapes
