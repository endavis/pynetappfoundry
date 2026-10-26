---
title: "ADR-0021: Collect CLI-only ONTAP data through the private CLI REST passthrough"
description: Collect ONTAP data that has no public REST endpoint through the private CLI REST passthrough, with hand-written models at the URL-tree path, an optional fetch, and a derived diff key.
date: 2026-10-26
audience:
  - contributors
tags:
  - adr
---

# ADR-0021: Collect CLI-only ONTAP data through the private CLI REST passthrough

## Status

Accepted

## Context

Some ONTAP state has no public REST endpoint. Per-SVM web services (`vserver services web`: `sysmgr`, `saml`, ... and whether each is enabled) are one example. The ONTAP models here are generated from the REST spec ([ADR-0008](0008-openapi-codegen-for-model-generation.md)), and the spec does not describe `/api/private/cli`, so codegen cannot produce models for such data (#866).

The project already collects one CLI-only dataset, cloud metadata (`virtual-machine instance show`), over SSH, with a hand-written model and a text parser.

ONTAP also exposes CLI commands through its private CLI REST passthrough: `GET /api/private/cli/<command path>?fields=...` returns JSON `records` with the CLI's field names as keys.

## Decision

1. **Collect CLI-only ONTAP data through the private CLI REST passthrough**, not SSH, when the command is available there. The `TypeMapping.api_endpoint` is the passthrough path (for example `/private/cli/vserver/services/web?fields=vserver,name,enabled`), so the generic `fetch()` → `get_all_records()` → `parse_api_response()` path collects it.
2. **Hand-write the model and mapping at the URL-tree path** ([ADR-0007](0007-url-tree-model-registry.md)): `models/ontap/private/cli/<command path>/model.py` and `cache/ontap/private/cli/<command path>/mapping.py`.
3. **Treat the fetch as optional.** If the call fails, the collector logs at debug level and stores an empty list, as it already does for `cloud_targets`.
4. **Give records without a unique field a derived key field** for `nf cache diff`, filled by a model validator. `OntapSvmWebService.service_key` is `vserver/name`.

## Rationale

- **REST over SSH.** The passthrough reuses the REST client, its credentials, pagination and parallel collection, and returns JSON. SSH would need credentials for SSH on every cluster and a text parser per command, as cloud metadata does.
- **URL-tree placement.** Codegen writes only paths in the spec and never deletes files, so a hand-written model under `private/cli/` cannot be overwritten. The path still says where the data comes from, as ADR-0007 intends.
- **Optional fetch.** Access to the private CLI depends on the user's role. One missing dataset should not abort the refresh of everything else.
- **Derived key field, not a property.** `nf cache diff` requires its key to be a model field (`test_all_key_fields_exist_on_model`). Deriving it in a validator keeps it consistent with `vserver` and `name` even when it is loaded from the cache.

## Consequences

- A new CLI-only dataset is a model, a mapping and a collector entry, with no SSH dependency.
- Private CLI field names are the CLI's (`vserver`, not `svm.name`), so the default query labels (`name`, `svm.name`, `uuid`) do not identify the SVM. Queries pass `--key service_key` (or `--key vserver`).
- The private CLI is not a versioned public API. If a later ONTAP release renames a field, the mapping falls back to the field's default without an error, so hand-written models need checking by hand on ONTAP upgrades.
- Existing SSH collection (cloud metadata) is unchanged.

## Related Issues

- Issue #866: collect SVM web services (vserver services web) into the cache

## Related Documentation

- [Cache Model Architecture: Hand-written private CLI models](../development/cache-models.md#hand-written-private-cli-models)
- [Cache System Reference](../reference/cache.md)
- [CLI Reference: Cache Management](../reference/cli.md#cache-management)
