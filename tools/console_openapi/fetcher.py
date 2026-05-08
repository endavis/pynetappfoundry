"""Shallow-clone the upstream NetAppDocs/console-automation repository.

The fetcher uses the system ``git`` binary so the tool has no Python git
dependency. The default cache lives under ``$XDG_CACHE_HOME/console-openapi``
(falling back to ``~/.cache/console-openapi``).
"""

from __future__ import annotations

import os
import subprocess  # nosec B404
from dataclasses import dataclass
from pathlib import Path

DEFAULT_REPO = "https://github.com/NetAppDocs/console-automation.git"


@dataclass(frozen=True)
class FetchResult:
    """Result of a successful fetch."""

    path: Path
    """Local path to the working tree."""

    requested_ref: str
    """The ref/tag/branch/SHA the caller asked for."""

    resolved_sha: str
    """The full commit SHA that ``requested_ref`` resolved to."""


def _cache_dir() -> Path:
    xdg = os.environ.get("XDG_CACHE_HOME")
    base = Path(xdg) if xdg else Path.home() / ".cache"
    return base / "console-openapi"


def _run(args: list[str], cwd: Path | None = None) -> str:
    result = subprocess.run(  # nosec B603
        args,
        cwd=str(cwd) if cwd else None,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def fetch(
    ref: str = "main",
    *,
    repo_url: str = DEFAULT_REPO,
    cache_dir: Path | None = None,
) -> FetchResult:
    """Clone ``repo_url`` (shallow) at ``ref`` into the cache and return its path.

    Subsequent invocations on the same cache reuse the existing clone, fetching
    only the requested ref.
    """
    target_dir = (cache_dir or _cache_dir()) / "console-automation"
    target_dir.parent.mkdir(parents=True, exist_ok=True)

    if not target_dir.exists():
        _run(
            [
                "git",
                "clone",
                "--depth=1",
                "--branch",
                ref if not _looks_like_sha(ref) else "main",
                repo_url,
                str(target_dir),
            ]
        )
        if _looks_like_sha(ref):
            _run(["git", "fetch", "--depth=1", "origin", ref], cwd=target_dir)
            _run(["git", "checkout", ref], cwd=target_dir)
    else:
        _run(["git", "fetch", "--depth=1", "origin", ref], cwd=target_dir)
        _run(["git", "checkout", "FETCH_HEAD"], cwd=target_dir)

    sha = _run(["git", "rev-parse", "HEAD"], cwd=target_dir)
    return FetchResult(path=target_dir, requested_ref=ref, resolved_sha=sha)


def _looks_like_sha(ref: str) -> bool:
    return len(ref) >= 7 and len(ref) <= 40 and all(c in "0123456789abcdef" for c in ref)
