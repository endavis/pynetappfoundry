---
title: "ADR-0028: Scope directories partition the config dir with per-scope credentials, thresholds and Console account"
description: A top-level directory with scope.toml partitions the config dir, with its own inventory, credentials, thresholds and Console account.
date: 2026-11-17
audience:
  - contributors
tags:
  - adr
---

# ADR-0028: Scope directories partition the config dir with per-scope credentials, thresholds and Console account

## Status

Accepted

## Context

Issue [#1080](https://github.com/endavis/pynetappfoundry/issues/1080) asks for several Console accounts and inventories in one config directory. Until now the config dir held one flat inventory, one `users.toml`, one `monitoring.toml` and one `consoleapi.toml`. A `users.toml` in a subdirectory already overwrote the root's sections, because `Config.parse_toml` keys every settings file by `file.stem` and shallow-merges with `.update`.

## Decision

1. **Scope marker.** A top-level directory of the config dir that contains `scope.toml` is a scope. The file is checked by `ScopeSettings` (`extra="forbid"`): optional `name` (must equal the directory name), `description` and `tags`. `scope.toml` at the root, nested deeper, under a non-scope directory, or inside a hidden directory or `apis` raises `ConfigurationError`. Subdirectories inside a scope are allowed.
2. **Inventory.** A scope's data files load into the shared `Config.data`. Each object's scope is kept in an index on `Config` (`get_scope(data_type, name)`); no `scope` key is injected into data dicts.
3. **D1, overridable files.** A scope may contain only `users.toml`, `monitoring.toml` and `consoleapi.toml` (by file stem), plus data files. Any other settings file in a scope raises `ConfigurationError` naming the file and the allowed list. A scope's settings files load into `Config.scope_settings[scope]`, never into `Config.settings`.
4. **Precedence.** A scope's settings are shared root defaults that the scope overrides. `get_user` and `get_secret` resolve: environment, the object's own entry, the scope's `users.toml`, the root `users.toml`, with each field falling back independently. `get_setting(..., scope=)` and `get_object_setting(data_type, name, *keys)` read the scope's file first and fall back to the root. A config dir without any `scope.toml` follows the unchanged code path.
5. **D2, Console in a scope is strict.**
   - A scope without `consoleapi.toml` has no Console account; `get_console_api_settings(scope=...)` raises and never falls back to the root account.
   - A scope inherits only `base_url`, `ui_base_url`, `base_api_path` and `timeout` from the root `[general]`. Credentials, `org_id`, `agent_ids`, `token_endpoint`, `audience` and `user_client_id` come only from the scope.
   - A scope's `consoleapi.toml` may contain only `[general]`, validated by `ConsoleAPISettings`.
   - The refresh token comes only from the scope's `users.toml [console]`; `NF_CONSOLE_*` is ignored for a scope.
   - `ConsoleAPIClient`, `ConsoleAgentClient`, `Console` and `OccmBackend` pass `scope` only when it is set. The OCCM backend uses a connector's scope account and caches clients per `(scope, agent_id)`.
6. **D3, unique names.** When either copy of an object name is in a scope (two scopes, root and scope, or the same scope twice), loading raises `ConfigurationError` naming both files. Two root copies stay last-one-wins.
7. **D4, deferred.** `nf config set-credential`, `show` and `validate` with `--scope`, searching by scope, and making root+root duplicates an error go to a follow-up issue.

## Rationale

- Loading scoped settings files into a separate store keeps them away from the stem-keyed shallow merge that would otherwise leak a scope's `users.toml` into the root.
- A small allowlist keeps everything that is global (API endpoints, TLS, SMTP) global, so a scope cannot change how another scope's clusters are reached.
- A strict Console account stops one organisation's calls from silently running with another's credentials.
- Unique names keep the name-keyed lookups (`get_user`, the cache, `DataSource`) unambiguous without changing any call site.

## Consequences

- No call site of `get_user` changes; the scope comes from the object name.
- A scoped object cannot reuse a name that exists elsewhere, so configs that already share names across directories must rename before adding `scope.toml`.
- Credentials for a scope are written by hand until the follow-up issue lands.

## Related Issues

- Issue #1080: feat: scope directories in the config dir, each with its own inventory, credentials, thresholds and Console account

## Related Documentation

- [Config schema: Scopes](../reference/config-schema.md#scopes)
- [Console Agent](../usage/console-agent.md)
- [ADR-0019](0019-console-runtime-client-architecture-org-scoped-access-and-per-token-type-wrapper-isolation.md)
- [ADR-0027](0027-occm-backend-is-live-only-and-delegates-to-the-typed-console-agent-ops.md)
