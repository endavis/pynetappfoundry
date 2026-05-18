"""Audit src/pynetappfoundry/ for legacy netapp_ontap / HostConnection call sites.

Scans for five pattern categories and classifies each hit as either a
``candidate`` (must be migrated) or ``legitimate`` (file is in the allowlist).

Usage::

    doit audit_legacy           # print Rich table (informational)
    doit audit_legacy --strict  # non-zero exit when any candidate exists
    doit audit_legacy --json    # machine-readable JSON

"""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from rich.console import Console
from rich.table import Table

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
_SRC_ROOT = _PROJECT_ROOT / "src" / "pynetappfoundry"

# Files whose legacy hits are known-intentional.  Paths are posix-form
# relative to _SRC_ROOT (e.g. "clients/ontap/cli.py").
_ALLOWLIST: frozenset[str] = frozenset(
    {
        "cli/commands/cache/refresh.py",
        "cli/commands/cache/inspect.py",
        "cli/commands/utils/run_cmd.py",
        "cli/commands/utils/validate.py",
        "clients/ontap/api.py",
        "clients/ontap/cli.py",
        "query/queryset.py",
    }
)

# ---------------------------------------------------------------------------
# Pattern catalogue
# (id, label, compiled regex)
# ---------------------------------------------------------------------------

_PATTERNS: list[tuple[str, str, re.Pattern[str]]] = [
    (
        "A",
        "Legacy SDK import",
        re.compile(r"(?:from netapp_ontap\b|import netapp_ontap\b)"),
    ),
    (
        "B",
        "HostConnection( call",
        re.compile(r"\bHostConnection\s*\("),
    ),
    (
        "C",
        "ONTAPAPIClient( without config=",
        re.compile(r"\bONTAPAPIClient\s*\("),
    ),
    (
        "D",
        "QuerySet( without config=",
        re.compile(r"\bQuerySet\s*\("),
    ),
    (
        "E",
        "Legacy cache fetch in CLI",
        re.compile(r"^from pynetappfoundry\.cache\s+import\s+\bfetch\b"),
    ),
]

# IDs where the comment-line guard applies (first non-whitespace char is '#')
_COMMENT_GUARDED = frozenset({"B", "C", "D"})

# IDs where the forward-window config= check applies
_CONFIG_GUARDED = frozenset({"C", "D"})

# IDs that are restricted to the cli/ subtree
_CLI_ONLY = frozenset({"E"})


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------


@dataclass
class LegacyMatch:
    """A single regex hit from the source scan."""

    file: str  # posix-form path relative to _SRC_ROOT
    line: int  # 1-based
    pattern: str  # pattern ID ("A" … "E")
    match: str  # the matched line text (stripped)


# ---------------------------------------------------------------------------
# Multi-line paren-balanced config= checker
# ---------------------------------------------------------------------------


def _has_config_within_call(lines: list[str], start_idx: int) -> bool:
    """Return True if ``config=`` appears inside the call starting at *start_idx*.

    Walks forward from *start_idx* line by line, counting ``(`` and ``)`` to
    track paren depth.  For each line, if ``config=`` appears on the line AND
    the depth is > 0 at any point on that line, return True.  Return False once
    depth reaches 0 (end of call) without having found ``config=``.

    Parameters
    ----------
    lines:
        All lines of the file (0-indexed list, already split).
    start_idx:
        0-based index of the line containing the opening ``(``.
    """
    depth = 0
    for i in range(start_idx, len(lines)):
        text = lines[i]
        # Check config= presence on this line before draining depth to 0.
        # We scan character-by-character but track whether config= was seen
        # while still inside the call.
        line_had_open = False
        for ch in text:
            if ch == "(":
                depth += 1
                line_had_open = True
            elif ch == ")":
                if depth > 0:
                    depth -= 1
                if depth == 0 and (line_had_open or i > start_idx):
                    # Call closed on this line — check if config= was on it
                    return bool(re.search(r"\bconfig\s*=", text))
        # Line did not close the call — check for config= while still open
        if depth > 0 and re.search(r"\bconfig\s*=", text):
            return True
    return False


# ---------------------------------------------------------------------------
# Core scanning
# ---------------------------------------------------------------------------


def scan_file(path: Path) -> list[LegacyMatch]:
    """Scan *path* for legacy patterns.  Returns a list of :class:`LegacyMatch`.

    Pure function — only I/O is ``path.read_text()``.
    """
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return []

    lines = text.splitlines()
    # posix path relative to _SRC_ROOT for allowlist checks
    try:
        rel = path.relative_to(_SRC_ROOT).as_posix()
    except ValueError:
        rel = path.as_posix()

    # cli/ sub-tree flag (needed for pattern E)
    is_cli = rel.startswith("cli/")

    results: list[LegacyMatch] = []

    for idx, raw_line in enumerate(lines):
        line_no = idx + 1

        for pat_id, _, regex in _PATTERNS:
            # Pattern E only applies under cli/
            if pat_id in _CLI_ONLY and not is_cli:
                continue

            # Comment-line and class-definition guard for B/C/D.
            # Class definitions (e.g. `class ONTAPAPIClient(APIWrapper):` or
            # subclass declarations like `class Foo(QuerySet):`) are not
            # constructor calls and should not be flagged.
            if pat_id in _COMMENT_GUARDED:
                stripped = raw_line.lstrip()
                if stripped.startswith("#") or stripped.startswith("class "):
                    continue

            if not regex.search(raw_line):
                continue

            # Forward-window config= suppression for C/D
            if pat_id in _CONFIG_GUARDED and _has_config_within_call(lines, idx):
                continue

            results.append(
                LegacyMatch(
                    file=rel,
                    line=line_no,
                    pattern=pat_id,
                    match=raw_line.strip(),
                )
            )

    return results


def scan_tree(root: Path) -> tuple[list[LegacyMatch], list[LegacyMatch]]:
    """Recursively scan *root* and split hits into (candidates, legitimate).

    A hit is *legitimate* when its file path (posix-form relative to
    ``_SRC_ROOT``) is in :data:`_ALLOWLIST`.  Otherwise it is a *candidate*.
    """
    candidates: list[LegacyMatch] = []
    legitimate: list[LegacyMatch] = []

    for py_file in sorted(root.rglob("*.py")):
        if "__pycache__" in py_file.parts:
            continue

        for match in scan_file(py_file):
            # Normalise path for allowlist lookup — must be posix-form
            # relative to _SRC_ROOT regardless of how scan_file produced it.
            try:
                norm = py_file.relative_to(_SRC_ROOT).as_posix()
            except ValueError:
                norm = match.file

            if norm in _ALLOWLIST:
                legitimate.append(match)
            else:
                candidates.append(match)

    return candidates, legitimate


# ---------------------------------------------------------------------------
# Output renderers
# ---------------------------------------------------------------------------


def render_table(
    candidates: list[LegacyMatch],
    legitimate: list[LegacyMatch],
    console: Console,
) -> None:
    """Print a Rich table summarising audit results to *console*."""
    table = Table(title="Legacy Pattern Audit", show_lines=True)
    table.add_column("Status", style="bold", width=12)
    table.add_column("File", style="cyan")
    table.add_column("Line", justify="right", width=6)
    table.add_column("Pat", width=4)
    table.add_column("Match")

    for m in sorted(candidates, key=lambda x: (x.file, x.line)):
        table.add_row("[red]CANDIDATE[/red]", m.file, str(m.line), m.pattern, m.match)

    for m in sorted(legitimate, key=lambda x: (x.file, x.line)):
        table.add_row("[green]OK[/green]", m.file, str(m.line), m.pattern, m.match)

    console.print()
    console.print(table)
    console.print()

    if candidates:
        console.print(
            f"[bold red]CANDIDATES:[/bold red] {len(candidates)} non-allowlisted "
            f"legacy hit(s) across "
            f"{len({m.file for m in candidates})} file(s)."
        )
    else:
        console.print("[bold green]No non-allowlisted legacy hits found.[/bold green]")
    console.print()


def render_json(
    candidates: list[LegacyMatch],
    legitimate: list[LegacyMatch],
    strict: bool,
) -> None:
    """Emit machine-readable JSON to stdout."""
    # Count per-pattern
    pattern_counts: dict[str, int] = {pid: 0 for pid, _, _ in _PATTERNS}
    for m in candidates:
        pattern_counts[m.pattern] = pattern_counts.get(m.pattern, 0) + 1

    payload: dict[str, Any] = {
        "schema_version": 1,
        "strict": strict,
        "candidates": [
            {"file": m.file, "line": m.line, "pattern": m.pattern, "match": m.match}
            for m in sorted(candidates, key=lambda x: (x.file, x.line))
        ],
        "legitimate": [
            {"file": m.file, "line": m.line, "pattern": m.pattern, "match": m.match}
            for m in sorted(legitimate, key=lambda x: (x.file, x.line))
        ],
        "summary": {
            "candidate_count": len(candidates),
            "legitimate_count": len(legitimate),
            "allowlist_count": len(_ALLOWLIST),
            "patterns": pattern_counts,
        },
    }
    print(json.dumps(payload, indent=2))


# ---------------------------------------------------------------------------
# Task action
# ---------------------------------------------------------------------------


def _run_audit(strict: bool = False, json_output: bool = False) -> bool:
    """Scan the source tree and report legacy hits.

    Parameters
    ----------
    strict:
        Return ``False`` (non-zero exit) when any candidate is found.
    json_output:
        Emit JSON to stdout instead of the Rich table.

    Returns
    -------
    bool
        ``True`` on success (strict=False always; strict=True only when no
        candidates).
    """
    candidates, legitimate = scan_tree(_SRC_ROOT)

    if json_output:
        render_json(candidates, legitimate, strict)
    else:
        console = Console(file=sys.stdout)
        render_table(candidates, legitimate, console)

    return not (strict and bool(candidates))


def task_audit_legacy() -> dict[str, Any]:
    """Scan source tree for legacy netapp_ontap / HostConnection call sites."""
    return {
        "actions": [_run_audit],
        "params": [
            {
                "name": "strict",
                "long": "strict",
                "type": bool,
                "default": False,
                "help": "Exit non-zero if any non-allowlisted candidate is found",
            },
            {
                "name": "json_output",
                "long": "json",
                "type": bool,
                "default": False,
                "help": "Emit machine-readable JSON instead of the Rich table",
            },
        ],
        "verbosity": 2,
    }
