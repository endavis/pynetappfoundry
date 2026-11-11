---
title: "ADR-0024: Generated models carry only API data; computed values live in separate hand-written models"
description: Generated models carry only API data; values computed from other collected data live in separate hand-written models.
date: 2026-11-11
audience:
  - contributors
tags:
  - adr
---

# ADR-0024: Generated models carry only API data; computed values live in separate hand-written models

## Status

Accepted

## Context

`ClusterInfo` mixes two kinds of fields. Most come from `GET /cluster`. `is_ha` and `is_cloud` do not: they are derived from the collected nodes by `post_collection` hooks in `src/pynetappfoundry/cache/ontap/cluster/mapping.py`. Issue #967 moves `/cluster` onto the code generator ([ADR-0008](0008-openapi-codegen-for-model-generation.md)), and a generated model is rewritten from the OpenAPI spec on every regeneration, so a hand-added derived field cannot live on it. The derivation is hooked into the fetch dispatcher through `FieldMapping.depends_on` ([ADR-0013](0013-datasource-as-a-thin-facade-over-the-collector.md)).

## Decision

1. **A generated model carries only API data.** No generated `model.py` holds a field that is computed from other objects.
2. **Computed values live in a separate hand-written model.** `ClusterTraits` (`src/pynetappfoundry/models/ontap/cluster/traits/model.py`) holds `is_ha` and `is_cloud`. Its mapping, `CLUSTERTRAITS_MAPPING` in `src/pynetappfoundry/cache/ontap/cluster/traits/mapping.py`, has no generated header and registers as `"ClusterTraits"`.
3. **A `TypeMapping` with `response_shape="computed"` describes such a model.** It has an empty `api_endpoint` and `cli_command`, no parent, and at least one field; every field is `cache_strategy="derived"` with a `post_collection` hook. `fetchers.fetch` makes no request for it: it builds an empty instance and runs the hooks against the dependencies declared in `depends_on`. `computed` is opt-in because an empty endpoint on any other mapping would otherwise issue `GET ""`.
4. **The traits are collected and cached as their own group.** `CachedClusterMetadata.cluster_traits` is stored in the `clustertraits` table. The snapshot version is 2.2 (`MIN_COMPATIBLE` stays 2.0) and SQLite schema v10 creates the table and backfills it from `clusterinfo`.
5. **Readers use `ClusterTraits`.** The cloud gates in the HTML and inventory reports and `OntapBackend._is_cloud_cluster` read it. Part B of #967 removed the two fields from `cluster` when `/cluster` became the generated `OntapCluster` (snapshot version 3.0, SQLite schema v11).
6. **The CVO detection helpers moved with the hooks** to `src/pynetappfoundry/cache/ontap/cluster/traits/mapping.py` and are no longer re-exported from `src/pynetappfoundry/cache/ontap/cluster/mapping.py`, which is generated (Part B of #967).

## Rationale

- Regeneration can overwrite a generated model freely, because nothing hand-written lives in it.
- The split makes it visible which values the API returns and which this project computes.
- Reusing `depends_on` and the derived-field machinery keeps one derivation path for collection, `DataSource` and the cache.

## Consequences

- Each computed value needs a small hand-written model and mapping, and a cache table.
- Callers read `is_ha` and `is_cloud` from `cluster_traits`, not `cluster`.
- A user's existing cache keeps its values through the v10 backfill and needs no refresh.

## Related Issues

- Issue #967: refactor: generate /cluster and move is_ha/is_cloud into a hand-written computed-values model

## Related Documentation

- [Cache Models](../development/cache-models.md)
- [Field Mapping](../development/field-mapping.md)
- [Cache Reference](../reference/cache.md)
