---
title: "ADR-0037: Digital Advisor backend is live-only and generates curated GraphQL selections from its models"
description: The Digital Advisor backend is live-only and generates curated GraphQL selections, with no personal data, from its models.
date: 2026-11-19
audience:
  - contributors
tags:
  - adr
---

# ADR-0037: Digital Advisor backend is live-only and generates curated GraphQL selections from its models

## Status

Accepted

## Context

Issue [#1116](https://github.com/endavis/pynetappfoundry/issues/1116) adds a `DataSource` backend over the Digital Advisor GraphQL client of [ADR-0036](0036-digital-advisor-client-is-a-read-only-graphql-client-with-rotating-refresh-token-write-back.md). The schema is large, many of its objects hold personal data (contact people, street addresses), and the `systems` query requires four arguments. Every other backend has its own ADR (0015 DII, 0026 AIQUM, 0027 OCCM).

## Decision

1. **Live-only.** `DigitalAdvisorBackend` sets `live_only = True`, as the DII backend does. There is no cache database, so no migration and no `SCHEMA_VERSION` change. `source="auto"` goes live and `source="cache"` raises `ValueError`.
2. **The backend builds the documents; the client is unchanged.** Each document is generated from the Pydantic models: a nested model field becomes a `{ ... }` sub-selection. It goes through `DigitalAdvisorAPIClient.paginate()`, so `query()` still runs `ensure_read_only`. Widening `list_systems(fields=)` to nested selection sets would change [ADR-0036](0036-digital-advisor-client-is-a-read-only-graphql-client-with-rotating-refresh-token-write-back.md) section 9 and enlarge a public input surface. Generating from the models gives one source of truth for the model fields, the selection and the personal-data check.
3. **Curated fields, no personal data.** The models hold the scalars and the nested objects chosen for them. `PERSONAL_DATA_FIELDS` (`contactPerson`, `salesRepresentative`, `csm`, `retentionSpecialist`, `solutionEngineerSpecialist`, `sam`, `streetAddress`, `postalCode`) is a second guard: `selection_set()` raises `ValueError` before any request when a model holds one. Every generated name is also checked against `^[A-Za-z_][A-Za-z0-9_]*$`. Unbounded nested lists (`Cluster.systems`, `vservers`, `shelves`, `risks` and the like) are out of scope.
4. **Query arguments through `.filter()`.** Each mapping has a fixed allowlist of root-query arguments; a `.filter()` key in it is sent as a typed GraphQL variable, never interpolated. Any other key is an in-memory equality filter on a dotted path. A top-level key that is neither an argument nor a model field raises `ValueError` before any request. The allowlists hold only names that are not record fields, so a key is never ambiguous. `platformType` and `operatingMode` are excluded until their types are fixed ([#1124](https://github.com/endavis/pynetappfoundry/issues/1124)).
5. **`systems` defaults are chosen, not measured.** The service requires `productTypes`, `systemStates`, `includeAllStates` and `includeStorageGridNodes`. The backend sends `["FILER"]`, `["ACTIVE"]`, `False` and `False`. The semantics of `includeAllStates` against `systemStates` are not known. Each default can be overridden through `.filter()`.
6. **`cluster=` is a label.** `digitaladvisorapi.toml` is root-only, so there is one account; the value is ignored.
7. **Models and mappings.** The models extend `OntapModel` with the GraphQL camelCase field names, so filter paths equal API paths. Every field is optional; a `DateTime` stays a string because the wire format was not measured. The mappings are hand-written from `model_fields`, as for OCCM, and registered through the generated mapping index.

## Rationale

Generating the selection from the models keeps what is declared, what is fetched and what is checked for personal data in one place, and leaves the reviewed client unchanged. Live-only matches the service: it has no collection endpoint worth caching and no change feed.

## Related Issues

- Issue #1116: feat: add an Active IQ Digital Advisor DataSource backend
- Issue #1124: Digital Advisor platformType and operatingMode filter types
- Issue #1051: feat: add an Active IQ Digital Advisor API client
- [ADR-0036](0036-digital-advisor-client-is-a-read-only-graphql-client-with-rotating-refresh-token-write-back.md), [ADR-0027](0027-occm-backend-is-live-only-and-delegates-to-the-typed-console-agent-ops.md)

## Related Documentation

- [Digital Advisor API: DataSource](../usage/digital-advisor-api.md#datasource)
- [Adding a Backend](../development/adding-backends.md)
- [DataSource User Guide](../usage/data-source.md#digital-advisor)
