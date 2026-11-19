"""Download an API's GraphQL schema into the configuration directory."""

from __future__ import annotations

import json
from typing import Any

import click
import requests
from rich.markup import escape

from pynetappfoundry.cli.commands.config.credentials import _load_config
from pynetappfoundry.cli.errors import CliError
from pynetappfoundry.cli.utils import print_success
from pynetappfoundry.core.settings_files import atomic_write_text

_DEFAULT_GRAPHQL_URL = "https://gql.aiq.netapp.com/graphql"
_DEFAULT_TIMEOUT = 70.0


@click.command("download-schema")
@click.option(
    "--api",
    "api_name",
    type=click.Choice(["digitaladvisor"]),
    default="digitaladvisor",
    show_default=True,
    help="API whose GraphQL schema to download.",
)
@click.pass_context
def download_schema(ctx: click.Context, api_name: str) -> None:
    """Download an API's GraphQL schema by introspection.

    The schema is written to <config>/apis/<api>/schema.json, replacing any
    existing file. Introspection needs no credentials, so this works before any
    token is configured. The URL and timeout come from digitaladvisorapi.toml
    [general] when set, otherwise the defaults.

    \b
    Examples:
        nf config download-schema
        nf config download-schema --api digitaladvisor
    """
    # Imported here: ``clients/__init__`` imports every client, and ``nf --help``
    # must stay cheap.
    from pynetappfoundry.clients.digitaladvisor.api import fetch_schema
    from pynetappfoundry.clients.digitaladvisor.auth import DigitalAdvisorError

    _, config = _load_config(ctx)
    general: Any = config.settings.get("digitaladvisorapi", {}).get("general", {})
    if not isinstance(general, dict):
        general = {}
    url = general.get("graphql_url", _DEFAULT_GRAPHQL_URL)
    timeout = general.get("timeout", _DEFAULT_TIMEOUT)
    if (
        not isinstance(url, str)
        or isinstance(timeout, bool)
        or not isinstance(timeout, (int, float))
    ):
        raise CliError(
            "digitaladvisorapi.toml [general] has an invalid graphql_url or timeout",
            hints=["graphql_url must be a string and timeout a number of seconds."],
        )

    try:
        data = fetch_schema(url, float(timeout))
    except (requests.RequestException, DigitalAdvisorError) as e:
        raise CliError(
            f"Schema download failed: {type(e).__name__}: {e}"
            if isinstance(e, DigitalAdvisorError)
            else f"Schema download failed: {type(e).__name__}",
            hints=[f"Check graphql_url ({escape(url)}) and your network access."],
            exc=e,
        ) from e

    target = config.get_schema_location(api_name) / "schema.json"
    try:
        atomic_write_text(target, json.dumps({"data": data}, indent=2) + "\n")
    except OSError as e:
        raise CliError(f"Could not write {target}: {type(e).__name__}", exc=e) from e

    types = data["__schema"].get("types", [])
    count = len(types) if isinstance(types, list) else 0
    print_success(f"Wrote {target} ({count} types)")
