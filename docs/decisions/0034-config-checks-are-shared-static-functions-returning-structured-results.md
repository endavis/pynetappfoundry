---
title: "ADR-0034: Config checks are shared static functions returning structured results"
description: Config checks live in core/config_checks.py as static functions returning structured results that nf config validate renders.
date: 2026-11-18
audience:
  - contributors
tags:
  - adr
---

# ADR-0034: Config checks are shared static functions returning structured results

## Status

Accepted

## Context

`nf config validate` held its checks as private helpers that drew Rich tree rows directly. Issue [#1111](https://github.com/endavis/pynetappfoundry/issues/1111) widens them to AIQUM, connectors, Cloud Insights and the API spec files, and issue [#1113](https://github.com/endavis/pynetappfoundry/issues/1113) (`nf doctor`) needs the same checks without a terminal tree.

## Decision

1. **One module, no CLI imports.** The checks live in `src/pynetappfoundry/core/config_checks.py`. It imports neither Rich nor click and depends only on `Config` and the pydantic models, so it respects the runtime layering in `docs/development/ai/architectural-conventions.md`.
2. **Structured results.** Each check returns `CheckResult` rows (`subject`, `status`, `label`, `errors`, `hint`) grouped in `CheckSection`s. `run_static_checks(config, scope=None)` returns the sections in display order. The status is one of `ok`, `warning`, `error` or `skipped`. Only `error` fails validation.
3. **Local reads only.** The checks read the loaded TOML and decrypt SOPS values locally. They make no network call. No result, label, error line or hint contains a secret, plaintext or ciphertext, and a decrypt failure reports only that the credential is missing.
4. **`nf config validate` renders.** `src/pynetappfoundry/cli/commands/config/validate.py` draws the sections, prints the error panel and exits 1 when any result is an `error`. The existing sections, labels and error lines are unchanged, so output for a valid configuration is byte-identical. For an invalid one, the existing lines are unchanged and fix hints are added.
5. **Spec files are a warning.** A missing OpenAPI spec in `<config>/apis/<name>/` is a `warning` and the exit code stays 0, because the configuration itself is valid; the client raises `FileNotFoundError` only when it is built. Only configured APIs are checked, judged from the loaded TOML without decryption: ONTAP, AIQUM and DII by their `*api.toml` `[general]` (DII also by a `[cloudinsights]` tenant), Console by a root or scope `consoleapi.toml` `[general]`. OCCM is never checked. Spec files are checked in root mode only.
6. **Missing AIQUM, connector or Cloud Insights configuration is an error.** Each is a problem that already breaks the client at runtime.
7. **Reuse.** `nf doctor` ([#1113](https://github.com/endavis/pynetappfoundry/issues/1113)) calls `run_static_checks` instead of repeating the checks, and adds environment and live checks ([ADR-0035](0035-nf-doctor-runs-static-environment-and-read-only-live-checks-with-fix-hints.md)).

## Rationale

Separating what is wrong from how it is drawn lets two commands and the tests share one set of checks, and lets a test assert on a result instead of scraping a rendered tree. Keeping the module free of Rich and click keeps it usable from any front end. Making a missing spec a warning keeps `validate` exit 0 for a configuration that is correct but not yet complete, while still telling the user where to copy the file from.

## Related Issues

- Issue #1111: shared static config checks used by `nf config validate`
- Issue #1113: `nf doctor` reuses the checks ([ADR-0035](0035-nf-doctor-runs-static-environment-and-read-only-live-checks-with-fix-hints.md))
- Issue #1110: configuration guide that sets up each API

## Related Documentation

- [Configuration guide: What nf config validate checks](../getting-started/configuration.md#what-nf-config-validate-checks)
- [CLI reference: config validate](../reference/cli.md)
