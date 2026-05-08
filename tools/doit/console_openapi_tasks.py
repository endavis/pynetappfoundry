"""Doit tasks for the console_openapi build-time tool."""

from __future__ import annotations

from pathlib import Path
from typing import Any


def _run_refresh(ref: str) -> list[list[str]]:
    """Build the argv for the refresh action with the user-supplied ref."""
    cmd = ["uv", "run", "python", "-m", "tools.console_openapi.cli", "build"]
    if ref:
        cmd.extend(["--ref", ref])
    return [cmd]


def task_console_openapi_refresh() -> dict[str, Any]:
    """Regenerate tools/console_openapi/generated/console_openapi.yaml from upstream docs."""

    def action(ref: str) -> None:
        import subprocess  # nosec B404

        cmd = _run_refresh(ref)[0]
        subprocess.run(cmd, check=True)  # nosec B603

    return {
        "actions": [action],
        "verbosity": 2,
        "params": [
            {
                "name": "ref",
                "long": "ref",
                "short": "r",
                "default": "main",
                "help": "Git ref to fetch.",
            },
        ],
    }


def task_console_openapi_check() -> dict[str, Any]:
    """Verify the checked-in spec matches a fresh build.

    This task performs a network git-clone of the upstream docs repo and
    a full rebuild, so it is **not** wired into ``doit check`` (which is
    designed to run quickly and offline). Run it explicitly in CI.
    """
    out = Path("tools/console_openapi/generated/console_openapi.yaml")
    return {
        "actions": [
            ["uv", "run", "python", "-m", "tools.console_openapi.cli", "build", "--out", str(out)],
            ["git", "--no-pager", "diff", "--exit-code", "--", str(out.parent)],
        ],
        "verbosity": 2,
    }
