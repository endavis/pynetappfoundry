"""Parse ONTAP expensive field annotations from endpoint descriptions.

ONTAP REST API specs document expensive fields in endpoint descriptions
using a ``### Expensive properties`` section with bullet-pointed field
patterns (e.g. ``* `analytics.*```).  This module extracts those patterns
and matches them against schema field names.
"""

from __future__ import annotations

import re

# Matches the ``### Expensive properties`` header (case-insensitive)
_EXPENSIVE_HEADER_RE = re.compile(r"###\s+Expensive\s+properties", re.IGNORECASE)

# Matches a bullet-pointed field pattern like ``* `analytics.*` ``
_EXPENSIVE_FIELD_RE = re.compile(r"^\s*\*\s*`([^`]+)`", re.MULTILINE)


def extract_expensive_patterns(description: str) -> list[str]:
    """Extract expensive field patterns from an endpoint description.

    Args:
        description: The full endpoint ``GET`` description text.

    Returns:
        List of field patterns (e.g. ``["analytics.*", "autosize.*",
        "is_svm_root"]``).  Empty if no expensive properties section found.
    """
    header_match = _EXPENSIVE_HEADER_RE.search(description)
    if not header_match:
        return []

    # Only scan text after the header
    section = description[header_match.end() :]

    # Stop at the next markdown header or end of string
    next_header = re.search(r"\n#{1,3}\s", section)
    if next_header:
        section = section[: next_header.start()]

    return _EXPENSIVE_FIELD_RE.findall(section)


def is_field_expensive(field_path: str, patterns: list[str]) -> bool:
    """Check whether a field matches any expensive field pattern.

    Supports exact matches and wildcard patterns (``analytics.*``
    matches ``analytics``, ``analytics.foo``, ``analytics.foo.bar``).

    Args:
        field_path: Dot-separated field path (e.g. ``"analytics.scan_progress"``).
        patterns: Expensive field patterns from :func:`extract_expensive_patterns`.

    Returns:
        True if the field matches any pattern.
    """
    for pattern in patterns:
        if pattern.endswith(".*"):
            prefix = pattern[:-2]  # strip ``.*``
            if field_path == prefix or field_path.startswith(prefix + "."):
                return True
        elif field_path == pattern:
            return True
    return False
