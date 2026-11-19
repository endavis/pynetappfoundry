---
title: "ADR-0035: nf doctor runs static, environment and read-only live checks with fix hints"
description: nf doctor adds environment and read-only live checks to the static config checks, each with a fix hint.
date: 2026-11-19
audience:
  - contributors
tags:
  - adr
---

# ADR-0035: nf doctor runs static, environment and read-only live checks with fix hints

## Status

Accepted

## Context

`nf config validate` checks the configuration files offline ([ADR-0034](0034-config-checks-are-shared-static-functions-returning-structured-results.md)). It cannot tell whether `sops` and the age key work, whether the caches are usable, or whether an API answers with the stored credentials. Issue [#1113](https://github.com/endavis/pynetappfoundry/issues/1113) adds `nf doctor`, which checks all three and prints a fix hint for each problem.

## Decision

1. **Three groups of checks, one result type.** `nf doctor` runs the static checks of ADR-0034 (`run_static_checks`), the environment checks and the live checks. Every check returns `CheckResult` rows in `CheckSection`s, as in ADR-0034. `nf config validate` is unchanged and stays the offline CI check.
2. **A `doctor` package, not `core`.** The checks live in `src/pynetappfoundry/doctor/`: `environment.py` (offline) and `live.py` (live). The live checks use `clients/`, a higher layer than `core`. The modules import neither Rich nor click. The command `src/pynetappfoundry/cli/commands/doctor.py` imports them inside the function so `nf --help` stays lazy.
3. **Environment checks are offline.** They check `sops` on PATH, the age key, that every SOPS value decrypts, and each cache by presence, age and schema version. A cache is opened with a `mode=ro` URI, so doctor never creates, migrates or modifies a cache file ([ADR-0018](0018-cache-schema-versioning-and-backward-compatibility-policy.md)).
4. **Live checks are read-only.** Each request is a `GET`: ONTAP `/cluster`, AIQUM `/datacenter/cluster/clusters?max_records=1`, DII `/assets/storages/count`, and for Console the organizations, the agents and each active agent's `about`. The one exception is the Console OAuth token request, a `POST` to the token endpoint that creates and changes no Console resource; accounts with a static token make none. A DII 403 is a warning, because tokens are scoped by API category; a 401 is an error.
5. **First-use TLS pinning stays.** The ONTAP and AIQUM probes go through the pinning adapter, which records a host's fingerprint in the local trust store on first contact, as `nf utils validate` does. A changed identity is an error that shows the reset hint.
6. **The ONTAP probe is shared.** `src/pynetappfoundry/clients/ontap/probe.py` holds `probe_cluster`, called by both `nf utils validate` and `nf doctor`. The output of `nf utils validate` does not change.
7. **Injected clients.** Each live check takes client factories (defaulting to the real classes, imported lazily), so tests build no real client and make no request.
8. **No secrets in results.** No label, error or hint holds a ciphertext, plaintext or token. A live failure is described as `HTTP <status>` or the exception class name; only `ConfigurationError` and `ConsoleAuthError` messages, which are secret-free, are shown. A SOPS failure reports the exception class only.
9. **Options.** `--offline` skips the live checks and never imports them. `--api` limits the live and cache checks to the named APIs. `--scope` limits the checks to that scope. `-f/--filter` narrows the ONTAP clusters. `--json` prints one JSON document. The exit code is 1 when any result is an error; warnings do not fail.

## Rationale

Reusing `CheckResult` lets doctor share the checks and the rendering conventions of `nf config validate` and lets tests assert on results. Keeping the live probes read-only, and naming the two exceptions (the token `POST` and first-use pinning, which writes only the local trust store), makes the command safe to run against production. Splitting offline and live checks lets `--offline` run anywhere, including CI.

## Related Issues

- Issue #1113: `nf doctor`
- Issue #1111: shared static config checks
- Issue #1110: configuration guide that sets up each API

## Related Documentation

- [CLI reference: doctor](../reference/cli.md#doctor)
- [Configuration guide: nf doctor or nf config validate](../getting-started/configuration.md#nf-doctor-or-nf-config-validate)
