---
title: "ADR-0030: OCCM cache is discovery-driven and maps working environments to agents"
description: The OCCM cache walks Console discovery to each agent, stores the on-prem working environments per agent, and derives the working environment to agent mapping from them.
date: 2026-11-17
audience:
  - contributors
tags:
  - adr
---

# ADR-0030: OCCM cache is discovery-driven and maps working environments to agents

## Status

Accepted

## Context

Issue [#1076](https://github.com/endavis/pynetappfoundry/issues/1076) asks for a cache of the Console agent (OCCM) data and a way to tell which agents manage a working environment. [ADR-0027](0027-occm-backend-is-live-only-and-delegates-to-the-typed-console-agent-ops.md) made the OCCM backend live-only, and [ADR-0029](0029-console-discovery-walks-scope-accounts-and-merges-hand-written-spec-fragments.md) deferred the working environment to agent mapping to this issue. [ADR-0026](0026-aiqum-backend-is-live-only-and-reads-the-hal-records-envelope.md) and #1055 already gave AIQUM a per-mapping JSON record cache that this decision follows.

## Decision

1. **Scope.** The cache covers the on-prem list and, since #1074, the six cloud working environment lists (`OCCM_WORKING_ENVIRONMENT_MAPPINGS`). It adds `OccmCacheDB`, `OccmCollector` and `refresh_occm_cache()`. They walk `ConsoleDiscovery` accounts, then each discovered agent (deduplicated by `agent_id`, the first account wins), then that agent's working environment lists with `fields="*"`. The cache stores the inventory and the working environment to agent mapping. Deferred to follow-up issues:
   - the reports that read the OCCM cache in place of the `CloudMetadata` CLI parsing, plus Console links in the reports (#1086, needs a CVO agent);
   - the refresh and inspect CLI, now implemented as `nf cache occm` (#1087).
2. **Backend.** OCCM becomes cache-capable per mapping, the way AIQUM did in #1055. `OccmBackend.live_only` is `False` and `is_live_only(mapping)` returns `mapping.name not in OCCM_CACHED_MAPPINGS`. A partial decision goes live for all of the requested fields, cached and live together.
3. **Failed agent.** A failing agent is logged as a warning and recorded in `failed_agents`; its earlier rows are kept. A transport or auth error (`requests.RequestException`, `tenacity.RetryError`, `ConsoleAuthError`, or an error building the client) fails the whole agent. A `TypeError` or `ValueError` (including a pydantic `ValidationError`) fails only that mapping: it is logged, recorded in `OccmSnapshot.failed_mappings` as `(agent_id, mapping)` and keeps its earlier rows. If every mapping fails, the agent is failed. An agent whose status is set and is not `active` is skipped without being contacted and recorded in `skipped_agents`; its earlier rows are kept too. Agents that are no longer discovered are pruned. A discovery failure propagates and the database is left untouched.
4. **Schema and storage.** A separate `occm_cache.db` with `SCHEMA_VERSION = 1` and three tables: `occm_collections`, `occm_records` and `occm_inventory`. Records are keyed by `agent_id` and the working environment `publicId`. The agent mapping is derived from the records of every working environment mapping (`OCCM_WORKING_ENVIRONMENT_MAPPINGS`), not stored separately.
5. **Refresh.** A library function, `refresh_occm_cache(config, scopes=None)`, and `nf cache occm refresh` (#1087). With `scopes` set, discovery covers only those accounts and `OccmCacheDB.set()` replaces the inventory and prunes agents only within those scopes; `None` keeps the whole-cache behaviour. `nf cache occm status`, `agents` and `clear` inspect and clear the cache.
6. **Refactor.** The JSON path helper moves from `src/pynetappfoundry/cache/aiqum_db.py` to `src/pynetappfoundry/cache/_json_records.py` with no behaviour change, and both caches use it.
7. **Cached record shape.** A record is stored as `item.model_dump(mode="json")` and read back with `model_class.model_validate`. Indexed `json_extract` paths are not supported; equality filters bind both the path and the value.

This supersedes [ADR-0027](0027-occm-backend-is-live-only-and-delegates-to-the-typed-console-agent-ops.md) D6 for the cached mappings. Every other mapping stays live-only.

## Rationale

- Walking discovery first means the cache needs no `[connectors]` entries: it finds every agent an account can see, and a cache read needs no Console account.
- Deriving the mapping from the records keeps one source of truth. An agent that lists a working environment manages it, and a working environment listed by two agents maps to both.
- Keeping a failed agent's rows avoids losing good data to a transient error, while pruning undiscovered agents stops stale agents from answering.
- A separate database file follows ADR-0018's scope: the ONTAP cache and its `SCHEMA_VERSION` are untouched.

## Consequences

- `source="cache"` and `source="auto"` read the OCCM cache for the on-prem working environments; `auto` on an agent that has not been collected falls back to live once.
- Cache reads of a stale agent return old data. Age never affects routing; `OccmCacheDB.is_stale` only reports it.
- Until the follow-up issues land, nothing in the package refreshes the cache outside a call to `refresh_occm_cache()`, and the reports still parse the CLI cloud metadata.

## Related Issues

- Issue #1076: feat: cache Console agent cloud infrastructure data and replace the CLI cloud metadata
- Issue #1091: Console discovery and OCCM cache refresh fail on real agents (skipped agents)
- Issue #1055: AIQUM cache (the pattern this follows)
- Issue #1074: cloud working environment lists
- Issue #1093: generated `Tags` and `AvailabilityZone` model gaps (folded into #1095 and fixed there)
- Issue #1095: generated CVO models accept real cloud working environments
- Issue #1086: reports read cloud provider details from the OCCM cache (deferred)
- Issue #1087: CLI to refresh and inspect the OCCM cache (implemented)

## Related Documentation

- [OCCM Cache](../reference/cache.md#occm-cache)
- [Console Agent: Cache](../usage/console-agent.md#cache)
- [ADR-0018](0018-cache-schema-versioning-and-backward-compatibility-policy.md)
- [ADR-0026](0026-aiqum-backend-is-live-only-and-reads-the-hal-records-envelope.md)
- [ADR-0027](0027-occm-backend-is-live-only-and-delegates-to-the-typed-console-agent-ops.md)
- [ADR-0029](0029-console-discovery-walks-scope-accounts-and-merges-hand-written-spec-fragments.md)
