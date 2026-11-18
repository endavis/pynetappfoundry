"""CLI entry point for the console_openapi tool."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import click
import yaml

from tools.console_openapi import __version__
from tools.console_openapi.array_responses import (
    ARRAY_RESPONSES_PATH,
    array_operations,
    load_array_responses,
)
from tools.console_openapi.fetcher import DEFAULT_REPO, fetch
from tools.console_openapi.fragments import (
    FRAGMENTS_DIR,
    load_fragments,
    merge_fragments,
    strip_fragments,
)
from tools.console_openapi.lockfile import Lockfile
from tools.console_openapi.models import ParsedEndpoint
from tools.console_openapi.openapi.builder import (
    _SERVICE_BASE_PATHS,
    _enforce_invariants,
    build_spec,
)
from tools.console_openapi.overrides import (
    OVERRIDES_PATH,
    apply_overrides,
    load_overrides,
    strip_overrides,
)
from tools.console_openapi.walker import parse_service

DEFAULT_SERVICES: tuple[str, ...] = ("tenancy", "tenancyv4", "cvo", "dw")


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
@click.option(
    "--array-responses",
    "array_responses_path",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    default=ARRAY_RESPONSES_PATH,
    show_default=True,
    help="TOML list of operations whose response is a JSON array (#1021).",
)
@click.option(
    "--fragments-dir",
    "fragments_dir",
    type=click.Path(exists=True, file_okay=False, path_type=Path),
    default=FRAGMENTS_DIR,
    show_default=True,
    help="Directory of hand-written spec fragments merged into the spec (#1078).",
)
@click.option(
    "--overrides",
    "overrides_path",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    default=OVERRIDES_PATH,
    show_default=True,
    help="YAML file of schema overrides applied after the fragments (#1095).",
)
def build(
    ref: str,
    services: tuple[str, ...],
    out: Path,
    lockfile: Path,
    server_urls: tuple[str, ...],
    lenient: bool,
    repo: str,
    array_responses_path: Path,
    fragments_dir: Path,
    overrides_path: Path,
) -> None:
    """Fetch sources, parse, build the OpenAPI document, and write it to disk."""
    unmapped = [s for s in services if s not in _SERVICE_BASE_PATHS]
    if unmapped:
        raise click.BadParameter(
            f"service(s) {', '.join(unmapped)} have no entry in _SERVICE_BASE_PATHS "
            "(tools/console_openapi/openapi/builder.py); declare the service's base path first.",
            param_hint="--service",
        )
    array_ops = array_operations(load_array_responses(array_responses_path), services)
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
        array_responses=array_ops,
        fragments=load_fragments(fragments_dir),
        overrides=load_overrides(overrides_path),
    )

    out.parent.mkdir(parents=True, exist_ok=True)
    if out.suffix.lower() in {".json"}:
        out.write_text(json.dumps(spec, indent=2, sort_keys=False) + "\n", encoding="utf-8")
    else:
        out.write_text(yaml.safe_dump(spec, sort_keys=False), encoding="utf-8")
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


@cli.command("apply-fragments")
@click.option(
    "--spec",
    "spec_path",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    default=Path("tools/console_openapi/generated/console_openapi.yaml"),
    show_default=True,
    help="Spec file to update in place.",
)
@click.option(
    "--fragments-dir",
    "fragments_dir",
    type=click.Path(exists=True, file_okay=False, path_type=Path),
    default=FRAGMENTS_DIR,
    show_default=True,
    help="Directory of hand-written spec fragments.",
)
@click.option(
    "--overrides",
    "overrides_path",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    default=OVERRIDES_PATH,
    show_default=True,
    help="YAML file of schema overrides applied after the fragments (#1095).",
)
def apply_fragments(spec_path: Path, fragments_dir: Path, overrides_path: Path) -> None:
    """Re-apply the spec fragments and overrides to the committed spec, offline (#1078, #1095).

    Strips the overrides, then the fragments a previous run merged, merges the
    fragments again and applies the overrides, then rewrites the spec, so editing
    either needs no fetch of the docs repo.
    """
    spec: dict[str, Any] = yaml.safe_load(spec_path.read_text(encoding="utf-8"))
    strip_overrides(spec)
    strip_fragments(spec)
    merge_fragments(spec, load_fragments(fragments_dir))
    apply_overrides(spec, load_overrides(overrides_path))
    _enforce_invariants(spec)
    _validate(spec)
    spec_path.write_text(yaml.safe_dump(spec, sort_keys=False), encoding="utf-8")
    click.echo(f"Wrote {spec_path}")


def _validate(spec: dict[str, object]) -> None:
    """Run openapi-spec-validator if available; warn but do not fail on missing dep."""
    try:
        from openapi_spec_validator import validate
    except ImportError:
        click.echo("openapi-spec-validator not installed; skipping validation.", err=True)
        return
    validate(spec)
    click.echo("openapi-spec-validator: OK")


if __name__ == "__main__":
    cli()
