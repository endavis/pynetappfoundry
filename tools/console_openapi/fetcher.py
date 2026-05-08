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
_GIT_TIMEOUT_SECONDS = 120


class FetchError(RuntimeError):
    """Raised when a git operation fails or times out."""


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
    try:
        result = subprocess.run(  # nosec B603
            args,
            cwd=str(cwd) if cwd else None,
            check=True,
            capture_output=True,
            text=True,
            timeout=_GIT_TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired as exc:
        raise FetchError(
            f"git command timed out after {_GIT_TIMEOUT_SECONDS}s: {' '.join(args)}"
        ) from exc
    return result.stdout.strip()


def fetch(
    ref: str = "main",
    *,
    repo_url: str = DEFAULT_REPO,
    cache_dir: Path | None = None,
) -> FetchResult:
    """Clone ``repo_url`` (shallow) at ``ref`` into the cache and return its path.

    Subsequent invocations on the same cache reuse the existing clone, fetching
    only the requested ref. The cache is initialized as an empty repo when the
    target directory doesn't exist; the same ``fetch + checkout FETCH_HEAD``
    pattern is used in both branches so SHAs unreachable from the default
    branch still resolve correctly.
    """
    target_dir = (cache_dir or _cache_dir()) / "console-automation"
    target_dir.parent.mkdir(parents=True, exist_ok=True)

    if not target_dir.exists():
        target_dir.mkdir(parents=True)
        _run(["git", "init", "--quiet"], cwd=target_dir)
        _run(["git", "remote", "add", "origin", repo_url], cwd=target_dir)

    _run(["git", "fetch", "--depth=1", "origin", ref], cwd=target_dir)
    _run(["git", "checkout", "--quiet", "FETCH_HEAD"], cwd=target_dir)

    sha = _run(["git", "rev-parse", "HEAD"], cwd=target_dir)
    return FetchResult(path=target_dir, requested_ref=ref, resolved_sha=sha)


def _looks_like_sha(ref: str) -> bool:
    return len(ref) >= 7 and len(ref) <= 40 and all(c in "0123456789abcdef" for c in ref)
