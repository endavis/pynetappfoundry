"""Download the API specs of the installed release into the configuration directory."""

from __future__ import annotations

import click
import requests
from rich.markup import escape

from pynetappfoundry._version import __version__
from pynetappfoundry.cli.commands.config.credentials import _load_config
from pynetappfoundry.cli.errors import CliError
from pynetappfoundry.cli.utils import print_info, print_success, print_warning
from pynetappfoundry.core.config_checks import SPEC_FILES, configured_apis
from pynetappfoundry.core.settings_files import atomic_write_text
from pynetappfoundry.core.spec_source import (
    SpecSourceError,
    installed_repository,
    parse_spec,
    resolve_ref,
    spec_url,
)

_TIMEOUT = 120.0
"""Seconds: the ONTAP spec is about 12 MB."""


def _fetch(url: str, file_name: str, ref: str, owner: str, repo: str, source: str) -> str:
    """Download one spec file and return its text.

    Raises:
        SpecSourceError: The request failed, the ref is unknown or the body is not a spec.
    """
    try:
        response = requests.get(url, timeout=_TIMEOUT)
    except requests.RequestException as e:
        raise SpecSourceError(f"download failed: {type(e).__name__}") from e
    if response.status_code == 404:
        raise SpecSourceError(
            f"{owner}/{repo} has no {source} at {ref} (HTTP 404)",
            hint="A development build's commit must be pushed to GitHub first.",
        )
    if response.status_code != 200:
        raise SpecSourceError(f"download failed: HTTP {response.status_code}")
    text = response.text
    parse_spec(text, file_name)
    return text


@click.command("download-spec")
@click.option(
    "--api",
    "api_name",
    type=click.Choice([api for _, api, _, _ in SPEC_FILES]),
    default=None,
    help="API whose spec to download (default: every configured API with a missing spec).",
)
@click.option("--force", is_flag=True, help="Replace a spec that already exists.")
@click.pass_context
def download_spec(ctx: click.Context, api_name: str | None, force: bool) -> None:
    """Download the committed API specs of the installed release from GitHub.

    Each spec is written to <config>/apis/<api>/, verbatim, after it parses and
    has a 'paths' map. Without --api, every configured API whose spec is missing
    is downloaded. An existing spec is kept unless --force is given. The spec
    comes from the release tag, or for a development build from the commit its
    version names, never from a live system.

    \b
    Examples:
        nf config download-spec
        nf config download-spec --api ontap --force
    """
    _, config = _load_config(ctx)
    wanted = {api_name} if api_name else configured_apis(config)
    todo = []
    for display, api, file_name, source in SPEC_FILES:
        if api not in wanted:
            continue
        target = config.get_schema_location(api) / file_name
        if target.exists() and not force:
            print_info(f"{display} spec exists: {target} (use --force to replace it)")
            continue
        todo.append((display, file_name, source, target))
    if not todo:
        print_info("Nothing to download.")
        return

    try:
        release = resolve_ref(__version__)
        owner, repo = installed_repository()
    except SpecSourceError as e:
        raise CliError(str(e), hints=[e.hint] if e.hint else []) from e
    if release.dirty:
        print_warning(
            f"Local changes are not in the download: the spec comes from commit {release.ref}."
        )

    failures: list[str] = []
    for display, file_name, source, target in todo:
        url = spec_url(owner, repo, release.ref, source)
        try:
            text = _fetch(url, file_name, release.ref, owner, repo, source)
            atomic_write_text(target, text)
        except SpecSourceError as e:
            failures.append(f"{display}: {e}" + (f" ({e.hint})" if e.hint else ""))
        except OSError as e:
            failures.append(f"{display}: could not write {target}: {type(e).__name__}")
        else:
            print_success(f"Wrote {target}")
    if failures:
        raise CliError(
            f"{len(failures)} spec download(s) failed",
            hints=[escape(f) for f in failures],
        )
