"""CLI entry point for the console_openapi tool."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import click
import yaml

from tools.console_openapi import __version__
from tools.console_openapi.fetcher import DEFAULT_REPO, fetch
from tools.console_openapi.lockfile import Lockfile
from tools.console_openapi.models import ParsedEndpoint
from tools.console_openapi.openapi.builder import build_spec
from tools.console_openapi.walker import parse_service

DEFAULT_SERVICES: tuple[str, ...] = ("tenancy", "tenancyv4")


@click.group()
@click.version_option(__version__)
def cli() -> None:
    """Generate an OpenAPI 3.0.3 spec from NetApp's BlueXP/Console docs."""


@cli.command("build")
@click.option("--ref", default="main", show_default=True, help="Git ref to fetch.")
@click.option(
    "--service",
    "services",
    multiple=True,
    default=DEFAULT_SERVICES,
    show_default=True,
    help="Service folders to include. Repeat for multiple.",
)
@click.option(
    "--out",
    type=click.Path(dir_okay=False, path_type=Path),
    default=Path("tools/console_openapi/generated/console_openapi.yaml"),
    show_default=True,
    help="Output spec file (.yaml or .json).",
)
@click.option(
    "--lockfile",
    type=click.Path(dir_okay=False, path_type=Path),
    default=Path("tools/console_openapi/generated/console_openapi.lock.json"),
    show_default=True,
)
@click.option(
    "--server-url",
    "server_urls",
    multiple=True,
    help="Override the default server URL(s). Repeat for multiple.",
)
@click.option("--lenient/--strict", default=False, help="Skip malformed endpoints with a warning.")
@click.option("--repo", default=DEFAULT_REPO, show_default=True)
def build(
    ref: str,
    services: tuple[str, ...],
    out: Path,
    lockfile: Path,
    server_urls: tuple[str, ...],
    lenient: bool,
    repo: str,
) -> None:
    """Fetch sources, parse, build the OpenAPI document, and write it to disk."""
    fetched = fetch(ref, repo_url=repo)
    click.echo(f"Fetched {repo} @ {fetched.resolved_sha[:12]} ({ref})")

    endpoints: list[ParsedEndpoint] = []
    total_skipped = 0
    total_errors = 0
    for service in services:
        report = parse_service(fetched.path, service, strict=not lenient)
        endpoints.extend(report.endpoints)
        total_skipped += len(report.skipped_overview)
        total_errors += len(report.errors)
        click.echo(
            f"  {service}: {len(report.endpoints)} endpoints, "
            f"{len(report.skipped_overview)} overviews, {len(report.errors)} errors"
        )

    if total_errors and not lenient:
        click.echo("Strict mode aborted on parse errors.", err=True)
        sys.exit(2)

    servers = (
        [{"url": u, "description": "Custom server URL"} for u in server_urls]
        if server_urls
        else None
    )

    spec = build_spec(
        endpoints,
        servers=servers,
        source_commit=fetched.resolved_sha,
        source_repo=repo.removesuffix(".git"),
        included_services=services,
    )

    out.parent.mkdir(parents=True, exist_ok=True)
    if out.suffix.lower() in {".json"}:
        out.write_text(json.dumps(spec, indent=2, sort_keys=False) + "\n")
    else:
        out.write_text(yaml.safe_dump(spec, sort_keys=False))
    click.echo(f"Wrote {out}")

    lock = Lockfile(
        repo=repo,
        requested_ref=ref,
        resolved_sha=fetched.resolved_sha,
        tool_version=__version__,
        services=services,
        endpoint_count=len(endpoints),
    )
    lockfile.parent.mkdir(parents=True, exist_ok=True)
    lock.write(lockfile)
    click.echo(f"Wrote {lockfile}")

    _validate(spec)


def _validate(spec: dict[str, object]) -> None:
    """Run openapi-spec-validator if available; warn but do not fail on missing dep."""
    try:
        from openapi_spec_validator import validate  # type: ignore[import-untyped]
    except ImportError:
        click.echo("openapi-spec-validator not installed; skipping validation.", err=True)
        return
    validate(spec)
    click.echo("openapi-spec-validator: OK")


if __name__ == "__main__":
    cli()
