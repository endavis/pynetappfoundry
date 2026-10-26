---
title: CLI Guide
description: The nf command-line interface, its module layout, and how to extend it
audience:
  - users
  - contributors
tags:
  - cli
  - usage
---

# CLI Guide

## Purpose

This page documents the **application's user-facing command-line
interface**: the `nf` console script shipped by the `pynetappfoundry`
package. It covers the entry point, the module layout, how to add new
commands, and how to test them. For every command and option, see the
[CLI Reference](../reference/cli.md).

This page does **not** cover `doit`, which is a contributor-only
development task runner. For `doit` tasks, see the
[Doit Tasks Reference](../development/doit-tasks-reference.md). For the
architectural rationale behind the runtime/dev split, see
[Tooling Roles and Architectural Boundaries](../development/tooling-roles.md).

## Quick reference

After installing the package, the `nf` command is available on your
`PATH`:

```bash
$ nf --help
Usage: nf [OPTIONS] COMMAND [ARGS]...

  NetApp Foundry - ONTAP administration tools.

Options:
  --version              Show the version and exit.
  -c, --config-dir PATH  Configuration directory path. Can also be set via
                         NF_CONFIG_DIR env var.
  -o, --output-dir PATH  Output directory path.
  --debug / --no-debug   Enable debug logging.
  -h, --help             Show this message and exit.

Commands:
  cache     Cluster metadata cache management.
  cifs      CIFS / SMB inspection commands.
  config    Configuration management commands.
  events    Event management commands.
  licenses  License management commands.
  metrics   Metrics commands.
  reports   Report generation commands.
  utils     Utility commands.

$ nf licenses get -f '{"env": "Prod"}'
$ nf cache status
```

Global options go before the command group: `nf -c ./config --debug cache status`.

During development, prefix invocations with `uv run` to use the project
virtual environment:

```bash
uv run nf cache status
```

## Entry point and module layout

The CLI is registered in `pyproject.toml` as a console script:

```toml
[project.scripts]
nf = "pynetappfoundry.cli:nf"
```

`pynetappfoundry.cli` re-exports the `nf` group from
`src/pynetappfoundry/cli/main.py`. When the package is installed (via `uv
sync`, `pip install`, etc.), the build backend generates an `nf`
executable that calls it.

The CLI is a package, with one subpackage per command group and one
module per command:

```text
src/pynetappfoundry/cli/
├── __init__.py        # re-exports nf
├── main.py            # the nf group, global options, group registration
├── decorators.py      # @with_config
├── utils.py           # Rich output helpers: print_info, print_error, print_table, ...
└── commands/
    ├── cache/         # check, clear, compliance, history, inspect, query, refresh, schema, show, status
    ├── cifs/          # session
    ├── config/        # init-sops, set-credential, show, validate
    ├── events/        # get, save-azure
    ├── licenses/      # check, get, savings
    ├── metrics/       # dump-dii
    ├── reports/       # html, inventory, locks, space-usage
    └── utils/         # run-cmd, sqlite-to-excel, validate
```

## How the CLI is structured

The CLI uses [click](https://click.palletsprojects.com/). The rationale is
in [ADR-9014: Use click for application CLI](../decisions/9014-use-click-for-application-cli.md).

- **`nf` is a `click.Group`** defined in `main.py`. It owns the global
  options (`--config-dir`, `--output-dir`, `--debug`) and stores them in
  `ctx.obj` for commands to read. It accepts `-h` as well as `--help`.
- **Each command group is a `click.Group`** in
  `commands/<group>/__init__.py`. It imports its commands and attaches them
  with `add_command()`.
- **Registration is explicit.** `main.py` imports every group and calls
  `nf.add_command(<group>)`. Nothing is discovered automatically.
- **`@with_config(action)`** builds a `Config` from the global options,
  parses the command's `-f, --filter` JSON, and calls the command with
  `config` and `clusters` keyword arguments. Any exception becomes a
  `click.ClickException` prefixed with `action`.
- **Commands are thin.** They parse options, read data through the data layer,
  and print with the helpers in `src/pynetappfoundry/cli/utils.py`. The logic lives in the runtime
  package.

A group, from `src/pynetappfoundry/cli/commands/licenses/__init__.py`:

```python
import click

from pynetappfoundry.cli.commands.licenses.check import check
from pynetappfoundry.cli.commands.licenses.get import get
from pynetappfoundry.cli.commands.licenses.savings import savings


@click.group()
def licenses() -> None:
    """License management commands."""
    pass


licenses.add_command(check)
licenses.add_command(get)
licenses.add_command(savings)
```

## How to add a new command

To add a command to an existing group:

1. **Create `src/pynetappfoundry/cli/commands/<group>/<command>.py`** with a
   `@click.command()` function. Add `-f, --filter` and decorate it with
   `@with_config("<action> failed")` if it acts on clusters.
2. **Register it** in `commands/<group>/__init__.py` with
   `<group>.add_command(<command>)`.
3. **Keep business logic out of the command.** Read data through the data
   layer, put reusable logic in the runtime package, and print with
   `print_info`, `print_warning`, `print_error` or `print_table` from
   `src/pynetappfoundry/cli/utils.py`.
4. **Add tests** under `tests/unit/cli/commands/<group>/` (see
   [Testing CLI commands](#testing-cli-commands)).
5. **Document it** in the [CLI Reference](../reference/cli.md).

```python
# src/pynetappfoundry/cli/commands/licenses/expiring.py
from __future__ import annotations

from typing import Any

import click

from pynetappfoundry.cli.decorators import with_config
from pynetappfoundry.cli.utils import print_info
from pynetappfoundry.core.config import Config


@click.command()
@click.option("--filter", "-f", "filter", help="JSON cluster filter.")
@click.option("--days", default=30, show_default=True, help="Look-ahead window.")
@with_config("License expiry check failed")
def expiring(config: Config, clusters: dict[str, dict[str, Any]], days: int) -> None:
    """List licenses expiring within DAYS."""
    for name in clusters:
        print_info(f"Checking {name}...")
```

To add a new command group, create `commands/<group>/__init__.py` with a
`@click.group()` function, then import it in `main.py` and register it with
`nf.add_command(<group>)`. Add the group to the `-h` / `--help` checks in
`tests/unit/cli/test_main.py`.

## Testing CLI commands

Use click's in-process `CliRunner` to invoke `nf` without spawning a
subprocess. It is faster than `subprocess.run`, has no shell-quoting
pitfalls, and gives you direct access to exit codes and captured output.
Point `-c` at a temporary config directory and patch the data access the
command makes:

```python
# tests/unit/cli/commands/cache/test_clear.py
from pathlib import Path

from click.testing import CliRunner

from pynetappfoundry.cli.main import nf


def test_clear_no_args_shows_error(tmp_path: Path) -> None:
    """clear without a cluster or --all is rejected."""
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    (config_dir / "settings.toml").write_text('[ontapapi.general]\nbase_api_path = "/api"\n')

    result = CliRunner().invoke(nf, ["-c", str(config_dir), "cache", "clear"])

    assert result.exit_code != 0
    assert "Specify a cluster name or use --all" in result.output
```

Test helper functions (`_check_cluster_licenses`, `_matches_user`, ...)
directly where that is simpler than driving them through the CLI.

What to cover for every new command:

- **Happy path** with default arguments (exit code 0, expected output).
- **Each option**, long form and short form.
- **`-h` / `--help`**: exit code 0, and the two produce the same output.
- **Error paths**: missing required arguments, invalid values, invalid
  `--filter` JSON. Click returns a non-zero exit code and writes the
  message to `result.output`.

## See also

- [CLI Reference](../reference/cli.md): every command, option and example.
- [Usage Guide](basics.md): importing the package as a library.
- [API Reference](../reference/api.md): full API documentation.
- [Doit Tasks Reference](../development/doit-tasks-reference.md): the
  contributor-only task runner. Not the same thing as this page.
- [Tooling Roles and Architectural Boundaries](../development/tooling-roles.md):
  why the runtime CLI and dev tooling are kept separate.
- [ADR-9014: Use click for application CLI](../decisions/9014-use-click-for-application-cli.md)
