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

`nf config validate` checks the configuration files offline ([ADR-0034](0034-config-checks-are-shared-static-functions-returning-structured-results.md)). It cannot tell whether `sops` and the age key work, whether the caches are usable, or whether an API answers with the stored credentials. Issue [#1113](https://github.com/endavis/pynetappfoundry/issues/1113) adds `nf doctor`, which checks all three and prints a fix hint for each problem. Issue [#1117](https://github.com/endavis/pynetappfoundry/issues/1117) adds a Digital Advisor live check.

## Decision

1. **Three groups of checks, one result type.** `nf doctor` runs the static checks of ADR-0034 (`run_static_checks`), the environment checks and the live checks. Every check returns `CheckResult` rows in `CheckSection`s, as in ADR-0034. `nf config validate` is unchanged and stays the offline CI check.
2. **A `doctor` package, not `core`.** The checks live in `src/pynetappfoundry/doctor/`: `environment.py` (offline) and `live.py` (live). The live checks use `clients/`, a higher layer than `core`. The modules import neither Rich nor click. The command `src/pynetappfoundry/cli/commands/doctor.py` imports them inside the function so `nf --help` stays lazy.
3. **Environment checks are offline.** They check `sops` on PATH, the age key, that every SOPS value decrypts, each cache by presence, age and schema version, and that config clusters match Console by name (item 11). A cache is opened with a `mode=ro` URI, so doctor never creates, migrates or modifies a cache file ([ADR-0018](0018-cache-schema-versioning-and-backward-compatibility-policy.md)).
4. **Live checks are read-only.** Each request is a `GET`, except the Digital Advisor probe: ONTAP `/cluster`, AIQUM `/datacenter/cluster/clusters?max_records=1`, DII `/assets/storages/count`, and for Console the organizations, the agents and each active agent's `about`. The Digital Advisor probe is a GraphQL `POST` carrying one `query` document (`query DoctorProbe { volumes(pageSize: 1) { cursor } }`), checked by `ensure_read_only`; a GraphQL query reads only, so it counts as read-only, and it is the only non-`GET` probe. The Console OAuth token request is an exception, a `POST` to the token endpoint that creates and changes no Console resource; accounts with a static token make none. A DII 403 is a warning, because tokens are scoped by API category; a 401 is an error.
5. **First-use TLS pinning stays.** The ONTAP and AIQUM probes go through the pinning adapter, which records a host's fingerprint in the local trust store on first contact, as `nf utils validate` does. A changed identity is an error that shows the reset hint.
6. **The ONTAP probe is shared.** `src/pynetappfoundry/clients/ontap/probe.py` holds `probe_cluster`, called by both `nf utils validate` and `nf doctor`. The output of `nf utils validate` does not change.
7. **Injected clients.** Each live check takes client factories (defaulting to the real classes, imported lazily), so tests build no real client and make no request.
8. **No secrets in results.** No label, error or hint holds a ciphertext, plaintext or token. A live failure is described as `HTTP <status>` or the exception class name; only `ConfigurationError`, `ConsoleAuthError` and Digital Advisor token refresh messages, which are secret-free (built from an HTTP status and fixed text), are shown. A SOPS failure reports the exception class only.
9. **Options.** `--offline` skips the live checks and never imports them. `--api` limits every group to the named APIs, plus the shared `sops` and age-key checks, which run when a selected API has SOPS values ([#1122](https://github.com/endavis/pynetappfoundry/issues/1122)). The tags live in `src/pynetappfoundry/doctor/selection.py`, keyed by result subject and config structure, so `nf config validate` and `core` are unchanged. A static row belongs to the API of its settings file (`ontapapi`, `aiqumapi`, `diiapi`, `consoleapi`, `digitaladvisorapi`), its data type (`clusters` to ONTAP, `aiqums`, `cloudinsights`, `connectors` to Console) or its spec file; `users` belongs to the four APIs that read `users.toml`. Global settings (SMTP, Licensing, Monitoring, Azure, IBM) are hidden under `--api`, and an unrecognised subject is kept. The exit code counts only the rows shown. `--scope` limits the checks to that scope. `-f/--filter` narrows the ONTAP clusters. `--json` prints one JSON document. The exit code is 1 when any result is an error; warnings do not fail.
10. **Digital Advisor refresh mode: probe, refresh only if needed.** A personal access token is only probed. With both credentials the PAT is probed first; a rejected PAT falls back to the refresh pair under the same refresh and write rules, the result is a warning with a PAT renewal hint, and the probe can then take more than one request ([#1120](https://github.com/endavis/pynetappfoundry/issues/1120)). A refresh-token pair is probed with the stored access token while the client counts it as unexpired, with no refresh and no write. The client refreshes, by a `POST` to the token endpoint, and writes the rotated tokens to `digitaladvisorapi.toml`, only when the stored access token is missing, expired or rejected by the server (one refresh and one retry); never otherwise. That write-back is the second exception to read-only, and the result row says so. If the refresh fails, or the retry is still rejected, the result is an error that points to the portal login and a fresh `refresh_token`. A failed write-back is a warning, since the stored refresh token may then be stale. Retries are off, so one probe is one request.
11. **Config clusters match Console by name.** A `[clusters]` key must equal the cluster's real name, which is Console's `clusterName`. A record Console gives no `clusterName` (seen on some Azure working environments) falls back to its working environment name for the name match, and the OK row says how many matched that way. A record with a `clusterName` never matches by working environment name. The check `src/pynetappfoundry/doctor/console_clusters.py` reads the OCCM and ONTAP caches through `mode=ro` URIs (offline, nothing written) and compares per Console account ([#1131](https://github.com/endavis/pynetappfoundry/issues/1131) added the working environment name fallback). A key with no name match gets a counterpart by cluster UUID (the ONTAP cache `uuid`), then by any management IP, node LIFs included; a counterpart is an error with a hint to rename the key. Entries with no counterpart, and Console clusters not in the config, are warnings. A missing, unreadable, newer-schema or stale OCCM cache is a warning with a refresh hint, and nothing is compared. The section runs under `--api ontap` or `console`. `--scope` keeps one account, and `-f` also narrows the comparison, so Console-only clusters are not reported under it. The rule is enforced in doctor only, not at config load ([#1127](https://github.com/endavis/pynetappfoundry/issues/1127)).
12. **Missing-spec hint, doctor stays read-only.** The missing-spec row, static or live, gives `nf config download-spec --api <api>` as its fix hint, from one function, `spec_download_hint` in `src/pynetappfoundry/core/config_checks.py`. `nf doctor` does not download the spec itself, so it makes no new write ([#1129](https://github.com/endavis/pynetappfoundry/issues/1129), [ADR-0038](0038-nf-config-download-spec-fetches-the-committed-api-specs-of-the-installed-release.md)).

## Rationale

Reusing `CheckResult` lets doctor share the checks and the rendering conventions of `nf config validate` and lets tests assert on results. Keeping the live probes read-only, and naming the three exceptions (the Console token `POST`, the Digital Advisor refresh with its write-back, and first-use pinning, which writes only the local trust store), makes the command safe to run against production. Splitting offline and live checks lets `--offline` run anywhere, including CI.

## Related Issues

- Issue #1113: `nf doctor`
- Issue #1122: `--api` limits every check
- Issue #1111: shared static config checks
- Issue #1110: configuration guide that sets up each API
- Issue #1117: Digital Advisor live check
- Issue #1051: Digital Advisor API client
- Issue #1120: Digital Advisor refresh token as a fallback for the PAT
- Issue #1127: config clusters match Console by name
- Issue #1129: the missing-spec hint names `nf config download-spec`

## Related Documentation

- [CLI reference: doctor](../reference/cli.md#doctor)
- [Configuration guide: nf doctor or nf config validate](../getting-started/configuration.md#nf-doctor-or-nf-config-validate)
- [Digital Advisor API](../usage/digital-advisor-api.md)
