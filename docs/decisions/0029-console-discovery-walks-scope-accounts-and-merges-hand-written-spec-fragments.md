---
title: "ADR-0029: Console discovery walks scope accounts and merges hand-written spec fragments"
description: Console discovery walks each scope's Console account to its organizations, working environments and agents, and the Console spec merges hand-written fragments for the agents-mgmt endpoints.
date: 2026-11-17
audience:
  - contributors
tags:
  - adr
---

# ADR-0029: Console discovery walks scope accounts and merges hand-written spec fragments

## Status

Accepted

## Context

Issue [#1078](https://github.com/endavis/pynetappfoundry/issues/1078) asks the Console client to work with several organizations. [ADR-0028](0028-scope-directories-partition-the-config-dir-with-per-scope-credentials-thresholds-and-console-account.md) already lets each config scope carry its own Console account (`consoleapi.toml` plus a refresh token), and #1080 passes the scope through `ConsoleAPIClient`, `ConsoleAgentClient`, `Console` and `OccmBackend`. What is missing is a way to find out which organizations, working environments and agents each account can see. The Console `/agents-mgmt` endpoints that list and read agents are not in the NetAppDocs sources the spec is built from, so they have no generated client.

## Decision

1. **Accounts are scopes.** Each scope's `consoleapi.toml` is a service account, and the root is the default account. No organization id is configured: an account's organizations are discovered. `Config.console_account_scopes()` lists the accounts: the root first (as `None`), then the scopes that have a `consoleapi.toml`, sorted.
2. **The root counts as an account only with credentials.** Its `[general]` has `user_token`, `service_token` or `client_id`, or a root refresh token resolves. A root that only carries the keys scopes inherit (`base_url` and the like) is not an account.
3. **Discovery walk.** `ConsoleDiscovery` takes each account in turn, builds that account's `ConsoleAPIClient`, lists its organizations, and for each organization lists its resources and its agents. Organization resources of type `ON_PREM` are the working environments; their `public_id` is the resource's `rawId`. Every object carries the scope that listed it and the organization it was listed under, so an organization is only ever reached with the account that sees it.
4. **Error policy.** Errors from an account's own calls propagate. A failing account is not skipped, because a partial inventory would look complete.
5. **Spec fragments.** The two `/agents-mgmt` operations come from a hand-written fragment, `tools/console_openapi/fragments/agents_mgmt.yaml`, with fields taken from live lab probes and tagged `x-evidence: live`. The builder merges fragments after the docs paths and records them in `info.x-fragments`; `doit console_openapi_fragments` strips and re-merges them in the committed spec without network access. The new operations then go through `client_ops.toml`, codegen and the drift checks like any other. A test checks that the committed spec matches the fragments. The operations carry no `x-token-type`, so either token works and the user token is preferred.
   **Overrides and prose anchors (#1095).** Docs anchors with no fields table are emitted without a `type`, so the generated model is `RootModel[Any]` and accepts any JSON value. `tools/console_openapi/overrides.yaml` retypes the few schemas the docs get wrong (tag maps, cron integer lists, Azure availability zones), each marked `evidence: live` or `inferred` and recorded in its node as `x-override`. They are applied after the fragments and re-applied offline by `doit console_openapi_fragments`; see [Console OpenAPI tool: Spec overrides](../../tools/console_openapi/README.md#spec-overrides).
6. **Deferred.**
   - Mapping a working environment to its agent is implemented in #1076 ([ADR-0030](0030-occm-cache-is-discovery-driven-and-maps-working-environments-to-agents.md)). Discovery lists the three kinds side by side and does not reconcile agents against `[connectors]`.
   - Implemented in #1083, using the OCCM cache ([ADR-0030](0030-occm-cache-is-discovery-driven-and-maps-working-environments-to-agents.md)), with no live discovery at query time:
     - A connector without a non-blank `agent_id` resolves to the cached agent whose `name` equals the connector name (exact, case-sensitive) in the connector's own scope, deduplicated by `agent_id`. Status does not filter. No match, an empty cache or several distinct ids raises `ValueError`.
     - A raw agent id passed as `cluster=` uses the scope of the cached agent with that id: root when uncached or cached under the root, the scope when cached under one scope, `ValueError` when cached under several scopes without the root.
     - `Console(config, scope=S)` with no `org_id` (argument or `consoleapi.toml`) calls `list_organizations()` once and uses the only organization; zero or several raise `ValueError`.
     - `list-connectors` measurement (#1083, read-only, against organizations with several agents including inactive ones; only key names, types and status values were recorded):
       - The response is `{occms: [...]}` with no other top-level key and no cursor-like key. A `limit=1` query parameter does not change the result. The endpoint is not paginated: one call returns every agent, so `list_agents` needs no paging.
       - Each `occms[]` item has `agent`, `automaticCallbackUris`, `isServiceManager3`, `manualOverrideUris`, `primaryCallbackUri` and `status`.
       - Observed values: `occms[].status` was always `active`, while `occms[].agent.status` was `active` or `inactive`. The agent status is the one that tells inactive agents apart. `ConsoleAgentInfo.from_occm` already prefers `agent.status` and falls back to the item `status` only when it is missing, which is what the #1091 skip of non-active agents relies on.

## Rationale

- Reusing scopes as accounts adds no new configuration: the per-scope credential rules of ADR-0028 already stop one organization's calls from running with another's credentials.
- A fragment keeps live-probed endpoints in the same generated pipeline as the documented ones, instead of a second hand-written client, and keeps the committed spec reproducible offline.
- Requiring credentials for the root avoids reporting an empty "root account" in a config that only uses scopes.

## Consequences

- Users must copy the updated `console_openapi.yaml` into `<config_dir>/apis/console/` again to get the new operations.
- A fragment's fields are only as good as its probes. Each fragment operation must say `x-evidence: live`, and every scalar is nullable because the live responses carry nulls.
- The upstream docs rebuild (`console_openapi_refresh`) merges the fragments too, so the two paths give the same spec.

## Related Issues

- Issue #1078: feat: support multiple Console organizations through discovered service accounts
- Issue #1080: feat: scope directories in the config dir (see ADR-0028)
- Issue #1076: map working environments to agents (implemented, see ADR-0030)
- Issue #1083: connector and pagination follow-ups (implemented)
- Issue #1093: generated `Tags` and `AvailabilityZone` model gaps (fixed in #1095)
- Issue #1095: fix: generated CVO models reject real cloud working environments

## Related Documentation

- [Console Agent: Discovering organizations, agents and working environments](../usage/console-agent.md#discovering-organizations-agents-and-working-environments)
- [Console OpenAPI tool: Spec fragments](../../tools/console_openapi/README.md#spec-fragments)
- [ADR-0019](0019-console-runtime-client-architecture-org-scoped-access-and-per-token-type-wrapper-isolation.md)
- [ADR-0028](0028-scope-directories-partition-the-config-dir-with-per-scope-credentials-thresholds-and-console-account.md)
