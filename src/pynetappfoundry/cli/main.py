"""Main CLI entry point for pynetappfoundry."""

from __future__ import annotations

import logging
from typing import Any

import click

from pynetappfoundry._version import __version__
from pynetappfoundry.cli.commands.cache import cache
from pynetappfoundry.cli.commands.cifs import cifs
from pynetappfoundry.cli.commands.config import config
from pynetappfoundry.cli.commands.events import events
from pynetappfoundry.cli.commands.licenses import licenses
from pynetappfoundry.cli.commands.metrics import metrics
from pynetappfoundry.cli.commands.reports import reports
from pynetappfoundry.cli.commands.utils import utils
from pynetappfoundry.cli.utils import console, is_debug_mode, print_exception


class NfGroup(click.Group):
    """Click group that turns unexpected exceptions into a clean exit code 1."""

    def invoke(self, ctx: click.Context) -> Any:
        """Invoke the command, handling unexpected exceptions at the top level.

        Click's own control-flow exceptions (usage errors, ``Abort``, ``Exit``)
        and ``EOFError`` are re-raised so click handles them as usual.
        """
        try:
            return super().invoke(ctx)
        except (click.ClickException, click.exceptions.Abort, click.exceptions.Exit, EOFError):
            raise
        except Exception as e:
            print_exception(f"Unexpected error: {e}", e)
            if not is_debug_mode():
                console.print("[dim]Re-run with --debug for the full traceback.[/dim]")
            ctx.exit(1)


@click.group(cls=NfGroup, context_settings={"help_option_names": ["-h", "--help"]})
@click.version_option(version=__version__)
@click.option(
    "--config-dir",
    "-c",
    type=click.Path(),
    default="config",
    envvar="NF_CONFIG_DIR",
    help="Configuration directory path. Can also be set via NF_CONFIG_DIR env var.",
)
@click.option(
    "--output-dir",
    "-o",
    type=click.Path(),
    default="",
    help="Output directory path.",
)
@click.option(
    "--debug/--no-debug",
    default=False,
    help="Enable debug logging.",
)
@click.pass_context
def nf(ctx: click.Context, config_dir: str, output_dir: str, debug: bool) -> None:
    """NetApp Foundry - ONTAP administration tools.

    A CLI for managing NetApp ONTAP clusters, including license management,
    space reporting, event tracking, and more.
    """
    # Configure logging - CLI uses Rich for console output, so logging goes to file only
    # Set root logger to WARNING to suppress library noise
    # Add NullHandler to prevent "no handler found" warnings
    logging.getLogger().setLevel(logging.WARNING)
    logging.getLogger().addHandler(logging.NullHandler())

    # Enable DEBUG for pynetappfoundry loggers when debug mode is on
    if debug:
        logging.getLogger("pynetappfoundry").setLevel(logging.DEBUG)

    ctx.ensure_object(dict)
    ctx.obj["config_dir"] = config_dir
    ctx.obj["output_dir"] = output_dir
    ctx.obj["debug"] = debug


# Explicit registration (infrafoundry pattern)
nf.add_command(cache)
nf.add_command(cifs)
nf.add_command(config)
nf.add_command(events)
nf.add_command(licenses)
nf.add_command(metrics)
nf.add_command(reports)
nf.add_command(utils)


if __name__ == "__main__":
    nf()
