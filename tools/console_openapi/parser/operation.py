"""Operation-line parser.

The auto-generated docs encode the HTTP verb and path on a single line, e.g.::

    [.api-doc-operation .api-doc-operation-post]#POST# [.api-doc-code-block]#`/path/{id}`#

Presence of this line is what distinguishes endpoint pages from overview pages
that also have ``api: true`` in their front-matter.
"""

from __future__ import annotations

import re

_OP_VERB_RE = re.compile(
    r"\[\.api-doc-operation\s+\.api-doc-operation-(?P<verb>[a-z]+)\]\#(?P<verb2>[A-Z]+)\#"
)
_OP_PATH_RE = re.compile(r"\[\.api-doc-code-block\]\#`(?P<path>[^`]+)`\#")


def find_operation(body: str) -> tuple[str, str] | None:
    """Locate the operation line and return ``(verb_upper, path)``.

    Returns ``None`` when no operation line is present.
    """
    for line in body.splitlines():
        verb_match = _OP_VERB_RE.search(line)
        path_match = _OP_PATH_RE.search(line)
        if verb_match and path_match:
            return verb_match.group("verb2").upper(), path_match.group("path")
    return None
