"""Main CLI entry point for pynetappfoundry."""

from __future__ import annotations

import click

from pynetappfoundry._version import __version__
from pynetappfoundry.cli.commands.cache import cache
from pynetappfoundry.cli.commands.config import config
from pynetappfoundry.cli.commands.events import events
from pynetappfoundry.cli.commands.licenses import licenses
from pynetappfoundry.cli.commands.metrics import metrics
from pynetappfoundry.cli.commands.reports import reports
from pynetappfoundry.cli.commands.utils import utils


@click.group()
@click.version_option(version=__version__)
@click.option(
    "--config-dir",
    "-c",
    type=click.Path(),
    default="config",
    help="Configuration directory path.",
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
    ctx.ensure_object(dict)
    ctx.obj["config_dir"] = config_dir
    ctx.obj["output_dir"] = output_dir
    ctx.obj["debug"] = debug


# Explicit registration (infrafoundry pattern)
nf.add_command(cache)
nf.add_command(config)
nf.add_command(events)
nf.add_command(licenses)
nf.add_command(metrics)
nf.add_command(reports)
nf.add_command(utils)


if __name__ == "__main__":
    nf()
