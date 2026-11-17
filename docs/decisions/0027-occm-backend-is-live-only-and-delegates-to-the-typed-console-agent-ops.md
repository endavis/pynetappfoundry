---
title: "ADR-0027: OCCM backend is live-only and delegates to the typed Console agent ops"
description: The OCCM DataSource backend is live-only, calls the typed Console agent ops, takes the agent from the cluster argument, and filters in memory.
date: 2026-11-17
audience:
  - contributors
tags:
  - adr
---

# ADR-0027: OCCM backend is live-only and delegates to the typed Console agent ops

## Status

Accepted

## Context

Issue [#1050](https://github.com/endavis/pynetappfoundry/issues/1050) adds a Console agent (OCCM) backend to `DataSource`. `ConsoleAgentClient` already exposes typed ops (`ConsoleAgentOps`) generated from the audited `tools/console_openapi/client_ops.toml` ([ADR-0019](0019-console-runtime-client-architecture-org-scoped-access-and-per-token-type-wrapper-isolation.md)), and [ADR-0013](0013-datasource-as-a-thin-facade-over-the-collector.md) section 9 makes a backend a thin delegator to the fetch layer.

Read-only probes against a lab Console agent through Console SaaS, using `ops.list_onprem_working_environments`:

| Probe | Call | Result |
| :--- | :--- | :--- |
| P1 | default | 1 item. Non-null keys: `aff`, `description`, `discoverUserEmail`, `location`, `name`, `publicId`, `tenantId`, `workingEnvironmentType` |
| P2 | `fields="*"` | Accepted. All 23 model fields are present, adding the 15 listed under D8. |
| P3 | `fields="name,publicId"` | Accepted. Same 8 keys as P1. |
| P4 | `tenant_id=<the item's own tenantId>` | 0 items. The server does not filter on the item's `tenantId` value. |

## Decision

1. **D1, typed ops.** The backend calls `ConsoleAgentClient.ops.<method>` (`ConsoleAgentOps` in `src/pynetappfoundry/clients/console/generated/agent_ops.py`), never raw paths. `_OPS` in `src/pynetappfoundry/data/occm_backend.py` maps `mapping.api_endpoint` to the op name.
2. **D2, name.** `api_type = "occm"`, registered in `_BACKENDS`.
3. **D3, mapping.** One hand-written `TypeMapping`, built from `ResponseBody.model_fields` so it cannot drift from the model. It is not generated.
4. **D4, model class.** The generated `models/console/cvo/get_onprem_working_environments.ResponseBody` is used directly. It is a plain `BaseModel`: no `F` DSL and no `_fetched_fields` stamp, so filters are dicts.
5. **D5, target.** If `cluster` is a key of `[connectors]`, the backend reads that entry's optional `agent_id` and raises `ValueError` naming `connectors.<name>` when it is missing or blank. Any other value is the agent id itself. Credentials come from `consoleapi.toml` and `users.toml [console]` through `ConsoleAgentClient`.
6. **D6, live-only.** `live_only = True`: `auto` goes live and `source="cache"` raises `ValueError`. Superseded for the cached mappings by [ADR-0030](0030-occm-cache-is-discovery-driven-and-maps-working-environments-to-agents.md) (#1076): `live_only = False` and the mappings in `OCCM_CACHED_MAPPINGS` are served from the OCCM cache. Every other mapping stays live-only.
7. **D7, endpoints.** Superseded by #1074: the on-prem list plus six cloud lists (`/occm/api/vsa`, `aws/ha`, `azure/vsa`, `azure/ha`, `gcp/vsa` and `gcp/ha` `working-environments`), each through its own `list_*_working_environments` op and its own mapping built by `src/pynetappfoundry/cache/occm/_working_environments.py`. Measured against live Console agents (read-only, scrubbed; see the #1074 comments): AWS HA, Azure single node and Azure HA return only 8 default keys (`cloudProviderName`, `creatorUserEmail`, `isHA`, `name`, `publicId`, `svmName`, `tenantId`, `workingEnvironmentType`); every other field needs `fields=`. AWS single node, GCP single node and GCP HA were empty everywhere, so their explicit-fetch set is inferred from those 8 keys. The generated `Tags` model drops a dict's keys and the `AvailabilityZone` model rejects a string; those gaps are #1093. `get()` by `publicId` filters the list in memory.
8. **D8, envelope and filters.**
   - The response is a bare array with no paging, so `records_path=""`.
   - 15 fields are `requires_explicit_fetch=True` (P2): `actionsRequired`, `capacityFeatures`, `cbsProperties`, `cloudSyncProperties`, `clusterProperties`, `complianceProperties`, `cronJobSchedules`, `interClusterLifs`, `monitoringProperties`, `ontapClusterProperties`, `replicationProperties`, `reservedSize`, `snapshotPolicies`, `status`, `svms`. They are sent as a `fields=` CSV when named in `.fields()` or when a filter key starts with one of them.
   - `tenantId` is filtered in memory only; the `tenant_id` query parameter is never sent (P4).
   - Equality filters are applied in memory on dotted paths. `where()`, `path_params` and `parent_filters` are unsupported.

## Rationale

- Typed ops keep dispatch inside the audited manifest and return validated models, so the backend has no parsing of its own.
- The server-side `tenant_id` filter does not match the item's own `tenantId` (P4), so an in-memory filter is the only correct one.
- P2 and P3 show the agent omits the 15 heavy fields unless asked, which is why they are `requires_explicit_fetch`.

## Consequences

- The backend is small and has no cache, no pagination and no codegen.
- Each new OCCM endpoint needs a manifest op, an `_OPS` entry and a hand-written mapping.
- Filtering is client-side, so a large agent inventory is fetched whole.

## Related Issues

- Issue #1050: feat: add a Console agent (OCCM) DataSource backend
- Issue #1074: feat: add the cloud working-environment lists to the occm DataSource backend

## Related Documentation

- [DataSource User Guide: OCCM](../usage/data-source.md#occm-console-agent)
- [Console Agent](../usage/console-agent.md#datasource)
- [Adding a New API Backend](../development/adding-backends.md)
- [Config schema](../reference/config-schema.md)
