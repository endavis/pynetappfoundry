"""Doit tasks for the console_openapi build-time tool."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any


def task_console_openapi_refresh() -> dict[str, Any]:
    """Regenerate tools/console_openapi/generated/console_openapi.yaml from upstream docs."""
    return {
        "actions": [
            [
                sys.executable,
                "-m",
                "tools.console_openapi.cli",
                "build",
            ]
        ],
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
    """Verify the checked-in spec matches a fresh build (CI no-op test)."""
    out = Path("tools/console_openapi/generated/console_openapi.yaml")
    return {
        "actions": [
            [sys.executable, "-m", "tools.console_openapi.cli", "build", "--out", str(out)],
            ["git", "--no-pager", "diff", "--exit-code", "--", str(out.parent)],
        ],
        "verbosity": 2,
    }
