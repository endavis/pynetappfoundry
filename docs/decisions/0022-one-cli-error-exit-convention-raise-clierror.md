---
title: "ADR-0022: One CLI error-exit convention: raise CliError"
description: Commands report errors by raising CliError, a ClickException that keeps the red stdout output, instead of print_error plus ctx.exit.
date: 2026-11-10
audience:
  - contributors
tags:
  - adr
---

# ADR-0022: One CLI error-exit convention: raise CliError

## Status

Accepted

## Context

Commands left an error three ways: `print_error(...)` then `ctx.exit(n)` (the large majority), a plain `click.ClickException`, and `raise SystemExit`. The first needs two statements at every site and can be followed by code that runs when `ctx.exit` is mocked or caught. `ctx.exit` inside a broad `try/except Exception` is also caught, because `click.exceptions.Exit` is an `Exception` (`cache history snapshot --restore` printed a bogus `Failed to restore snapshot: 1`). A plain `ClickException` prints `Error: msg` on stderr, which differs from the red stdout line of `print_error`.

## Decision

1. **Commands report an error by raising `CliError`** (`src/pynetappfoundry/cli/errors.py`, a `click.ClickException`): `raise CliError(msg)` exits 1, `raise CliError(msg, exit_code=2)` exits 2. The top-level handler in `NfGroup` already passes `ClickException` through.
2. **`CliError.show()` keeps the existing output**: the red escaped message on stdout through the shared console, and the same log record. Optional `hints` (Rich markup lines) print after the message; `exc=` logs the traceback and prints it under `--debug`.
3. **`CliError` records the debug flag when it is constructed.** Click calls `show()` after the context is popped, so `is_debug_mode()` is always false there.
4. **`ctx.exit(0)` stays** for early successful exits, and the grep-style result exits of `nf cache check` and `nf cache compliance` stay as `ctx.exit(...)` (0 none, 1 matches found, 2 error). Their error paths (code 2) raise `CliError(msg, exit_code=2)`.
5. **Existing plain `ClickException` raises are kept** (decorators, CIFS session, locks, reports); switching them would move their output from stderr to stdout.
6. **A `CliError` raised inside a broad `except Exception` is re-raised first** (`except CliError: raise`).

## Rationale

- One statement per error exit, and control flow ends at the raise.
- Exit codes and output text stay the same, so scripts that read them are unaffected.
- It builds on click's own error path, so nothing outside the command layer changes.

## Consequences

- New commands raise `CliError` for errors instead of `print_error` plus `ctx.exit(1)`.
- `print_exception` takes a `debug` argument and logs with `exc_info=exc`, so it can be called from `show()`.
- One output change: `cache history snapshot --restore` on an incompatible schema no longer prints the extra `Failed to restore snapshot: 1`; the exit code stays 1.

## Related Issues

- Issue #942: one CLI exit convention via CliError
- Issue #904: CLI error handling and exit convention (parent)

## Related Documentation

- [CLI Reference: Exit Codes](../reference/cli.md#exit-codes)
- [CLI usage: adding a command](../usage/cli.md)
