"""Where the committed API specs come from: the repository at the installed release.

Pure helpers with no network and no click: they map the installed version to a git
ref, find the GitHub repository, build the raw file URL and check a downloaded spec.
The command that downloads lives in ``cli/commands/config/download_spec.py``; the
decision is recorded in ADR-0038.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from importlib import metadata
from typing import Any
from urllib.parse import urlparse

import yaml

from pynetappfoundry.core.config_checks import CONFIGURATION_DOC

TAG_PREFIX = "v"
"""Release tags are ``v<version>``: ``[tool.commitizen] tag_format`` in pyproject.toml."""

FALLBACK_VERSION = "0.0.0"
"""The version hatch-vcs reports when it finds no tag and no commit."""

RAW_HOST = "https://raw.githubusercontent.com"
"""Host that serves a file of a public repository at a tag or commit."""

DISTRIBUTION = "pynetappfoundry"

_SHA_SEGMENT = re.compile(r"g([0-9a-f]{7,40})")
_DIRTY_SEGMENT = re.compile(r"d\d{8}")


class SpecSourceError(Exception):
    """The spec source cannot be determined or the downloaded spec is unusable."""

    def __init__(self, message: str, hint: str | None = None) -> None:
        super().__init__(message)
        self.hint = hint


@dataclass(frozen=True)
class ReleaseRef:
    """The git ref of the installed release.

    Attributes:
        ref: A release tag (``v1.2.3``) or a commit sha.
        dirty: The build had local changes, so the commit's spec may differ.
    """

    ref: str
    dirty: bool = False


def resolve_ref(version: str) -> ReleaseRef:
    """Map an installed version string to the git ref that holds its specs.

    Args:
        version: A hatch-vcs version, such as ``1.2.3`` or ``1.2.4.dev3+gabc1234.d20260101``.

    Raises:
        SpecSourceError: The version names neither a release nor a commit.
    """
    public, _, local = version.partition("+")
    segments = local.split(".") if local else []
    for segment in segments:
        match = _SHA_SEGMENT.fullmatch(segment)
        if match:
            dirty = any(_DIRTY_SEGMENT.fullmatch(s) for s in segments)
            return ReleaseRef(match.group(1), dirty)
    if ".dev" in public or version == FALLBACK_VERSION:
        raise SpecSourceError(
            f"Cannot determine the commit of installed version {version}",
            hint=(
                "Install a release, or copy the spec file by hand; "
                f"see {CONFIGURATION_DOC} (Spec files)."
            ),
        )
    return ReleaseRef(f"{TAG_PREFIX}{public}")


def github_repository(urls: list[str] | None) -> tuple[str, str]:
    """Return ``(owner, repo)`` from the distribution's ``Project-URL`` entries.

    Args:
        urls: The ``Project-URL`` metadata values, each ``"<label>, <url>"``.

    Raises:
        SpecSourceError: There is no ``Repository`` entry, or it is not a GitHub URL.
    """
    url = None
    for entry in urls or []:
        label, _, value = entry.partition(",")
        if label.strip().lower() == "repository":
            url = value.strip()
            break
    if url is None:
        raise SpecSourceError(
            "The installed package has no Repository project URL",
            hint=f"Copy the spec file by hand; see {CONFIGURATION_DOC} (Spec files).",
        )
    parsed = urlparse(url)
    parts = [p for p in parsed.path.split("/") if p]
    if parsed.hostname != "github.com" or len(parts) != 2:
        raise SpecSourceError(
            f"The Repository project URL is not a GitHub repository: {url}",
            hint=f"Copy the spec file by hand; see {CONFIGURATION_DOC} (Spec files).",
        )
    repo = parts[1].removesuffix(".git")
    return parts[0], repo


def installed_repository() -> tuple[str, str]:
    """Return ``(owner, repo)`` of the installed distribution.

    Raises:
        SpecSourceError: The distribution is not installed or has no GitHub repository URL.
    """
    try:
        urls = metadata.metadata(DISTRIBUTION).get_all("Project-URL")
    except metadata.PackageNotFoundError as e:
        raise SpecSourceError(
            f"The {DISTRIBUTION} distribution is not installed",
            hint=f"Copy the spec file by hand; see {CONFIGURATION_DOC} (Spec files).",
        ) from e
    return github_repository(urls)


def spec_url(owner: str, repo: str, ref: str, source: str) -> str:
    """Return the raw URL of repository file ``source`` at ``ref``."""
    return f"{RAW_HOST}/{owner}/{repo}/{ref}/{source}"


def parse_spec(text: str, file_name: str) -> dict[str, Any]:
    """Parse a downloaded spec and check that it has a ``paths`` map.

    ``.yaml`` and ``.yml`` files are parsed as YAML, everything else as JSON.

    Raises:
        SpecSourceError: The text does not parse, is not a mapping, or has no ``paths`` map.
    """
    try:
        if file_name.lower().endswith((".yaml", ".yml")):
            loader = getattr(yaml, "CSafeLoader", yaml.SafeLoader)
            spec = yaml.load(text, Loader=loader)  # nosec B506  # CSafeLoader or SafeLoader, both safe
        else:
            spec = json.loads(text)
    except (ValueError, yaml.YAMLError) as e:
        raise SpecSourceError(f"{file_name} is not valid {type(e).__name__} content") from e
    if not isinstance(spec, dict) or not isinstance(spec.get("paths"), dict):
        raise SpecSourceError(f"{file_name} is not an OpenAPI spec: no 'paths' map")
    return spec
