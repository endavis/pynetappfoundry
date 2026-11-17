---
title: "ADR-0031: One command stores every SOPS secret and encrypt-value is removed"
description: nf config set-credential --setting stores every SOPS-encrypted secret in the right settings file with tomlkit, and nf config encrypt-value is removed.
date: 2026-11-17
audience:
  - contributors
tags:
  - adr
---

# ADR-0031: One command stores every SOPS secret and encrypt-value is removed

## Status

Accepted

## Context

Issue [#1089](https://github.com/endavis/pynetappfoundry/issues/1089) asks for one way to store every SOPS-encrypted secret. Until now `nf config encrypt-value` printed a `SOPS[...]` string that the user pasted into a settings file by hand, while `nf config set-credential` wrote only `users.toml` and data file entries. A Console client secret was easy to store in the wrong place: `set-credential --type console` stores a refresh token, not a client secret. [ADR-0028](0028-scope-directories-partition-the-config-dir-with-per-scope-credentials-thresholds-and-console-account.md) added per-scope Console accounts, which made the file to edit harder to name.

## Decision

1. **One command.** `nf config set-credential --setting <file>.<field> [--scope NAME]` prompts for the value (hidden, with confirmation) or takes it from `--password`, encrypts it with the age key and writes `<field> = "SOPS[...]"` into the right file and table. There is no plain text fallback: without `sops` the command fails and points to `nf config init-sops`.
2. **Targets come from the loader.** The valid targets are exactly the fields `Config` decrypts at read time, in `SOPS_SETTING_TARGETS` in `src/pynetappfoundry/core/config.py`: `consoleapi.client_secret`, `consoleapi.service_token` and `consoleapi.user_token` (table `[general]`), `diiapi.api_ro_token` (`[general]`) and `settings.smtp_password` (`[SMTP] password`).
3. **Scope limits come from the loader.** Only targets whose file stem is in `SCOPE_OVERRIDABLE_SETTINGS` accept `--scope`, so only `consoleapi.*`. An unknown scope is rejected.
4. **Strict options.** `--setting` cannot be combined with `--cluster`, `--type`, `--name`, `--user` or `--no-encrypt`; each raises an error before anything is prompted or written. `--user` is no longer required by Click; the command checks it for the `--cluster` and `--type` modes.
5. **File choice.** The writer applies the loader's rule: non-data `*.toml` files are matched by stem, root targets skip scope directories and scope targets look only under the scope. No match creates `<stem>.toml` (with the table); more than one match is refused, because the loader merges them and the file to write is ambiguous.
6. **Writes keep formatting.** Every config write uses `tomlkit`, which keeps comments and unrelated keys. The two existing `tomli_w` writers in `set-credential` move to the same writer. `tomli_w` stays a dependency for `tools/codegen/generators.py`.
7. **`encrypt-value` is removed (BREAKING).** This supersedes option B(a) of #1025, which kept it as the way to produce a value. The migration is `nf config set-credential --setting <file>.<field> [--scope NAME]`.
8. **`validate` follows.** `nf config validate` gets a root Console row ("Console: Not configured (optional)" without an account), so a broken root Console account now fails it. When an account has `client_id` but no `client_secret` and `users.toml [console]` holds a token, it adds a hint with the exact `--setting` command.

## Rationale

- Deriving the targets from the fields the loader decrypts keeps the command and the loader from drifting apart.
- Reusing `SCOPE_OVERRIDABLE_SETTINGS` and the loader's file rule means the command never writes a file the loader would reject or ignore.
- No plain text fallback is right for a command whose only job is to store a secret.
- `tomlkit` removes the data loss the old writers had: comments in hand-edited files were dropped on every write.

## Consequences

- Scripts that ran `nf config encrypt-value` must use `set-credential --setting`.
- `nf config validate` now fails for a broken root Console account that it used to skip.
- `tomlkit` is a new runtime dependency.
- A scope or root with two non-data files of the same stem cannot be written with `--setting` until one is removed.

## Related Issues

- Issue #1089: feat: store every secret through set-credential --setting and remove encrypt-value
- Issue #1081: scope-aware config CLI (ADR-0028)
- Issue #1025: SOPS-encrypted settings values

## Related Documentation

- [Configuration Schema](../reference/config-schema.md)
- [CLI Reference](../reference/cli.md)
- [ADR-0028](0028-scope-directories-partition-the-config-dir-with-per-scope-credentials-thresholds-and-console-account.md)
