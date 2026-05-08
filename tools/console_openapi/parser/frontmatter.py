"""YAML front-matter parser for AsciiDoc endpoint files."""

from __future__ import annotations

from typing import Any

import yaml

_DELIM = "---"


def split_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    """Split ``---``-delimited YAML front-matter from the rest of the file.

    Returns ``(frontmatter_dict, body_text)``. If no front-matter is present,
    returns ``({}, text)``.
    """
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].rstrip("\r\n") != _DELIM:
        return {}, text

    end_idx: int | None = None
    for i in range(1, len(lines)):
        if lines[i].rstrip("\r\n") == _DELIM:
            end_idx = i
            break
    if end_idx is None:
        return {}, text

    fm_text = "".join(lines[1:end_idx])
    body = "".join(lines[end_idx + 1 :])
    data = yaml.safe_load(fm_text) or {}
    if not isinstance(data, dict):
        return {}, body
    return data, body
