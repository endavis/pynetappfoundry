"""Helpers shared by the JSON-record cache databases (AIQUM #1055, OCCM #1076)."""

from __future__ import annotations


def json_path(key: str) -> str | None:
    """Build the quoted SQLite JSON path for a dotted filter *key*.

    Returns ``None`` when a segment contains a double quote: SQLite JSON paths
    have no escape for it, and no cached field is named that way, so such a key
    can match nothing.
    """
    segments = key.split(".")
    if any('"' in seg for seg in segments):
        return None
    return "$" + "".join(f'."{seg}"' for seg in segments)
