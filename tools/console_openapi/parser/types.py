"""Type-expression parser for table 'Type' cells.

Handles every form observed in the target corpus:

* primitives: ``string``, ``integer`` / ``int``, ``number``, ``boolean``, ``object``
* arrays: ``array[X]``, ``array[]``
* link references: ``link:#anchor[label]``
* unions: ``Any of: X, Y, ...`` (with optional surrounding whitespace)
* hash maps: ``Hash mapping strings to string`` (and ``... to integer``)
"""

from __future__ import annotations

import re

from tools.console_openapi.models import TypeRef

_LINK_RE = re.compile(r"link:#(?P<anchor>[^\[]+)\[(?P<label>[^\]]*)\]")

_PRIMITIVES: dict[str, str] = {
    "string": "string",
    "str": "string",
    "integer": "integer",
    "int": "integer",
    "long": "integer",
    "number": "number",
    "double": "number",
    "float": "number",
    "boolean": "boolean",
    "bool": "boolean",
    "object": "object",
}

_HASH_RE = re.compile(
    r"^hash mapping strings? to (?P<value_type>[a-zA-Z]+)$",
    re.IGNORECASE,
)


def parse_type(text: str) -> TypeRef:
    """Parse a single Type cell into a :class:`TypeRef`."""
    raw = text.strip()
    cleaned = _strip_inline_links_for_classification(raw)
    return _parse(cleaned, raw)


def _strip_inline_links_for_classification(text: str) -> str:
    """Collapse whitespace runs but keep link markers intact."""
    return re.sub(r"\s+", " ", text).strip()


def _parse(text: str, raw: str) -> TypeRef:
    if text == "":
        return TypeRef(primitive="object", raw=raw)

    # Hash mapping
    hm = _HASH_RE.match(text)
    if hm:
        value = hm.group("value_type").lower()
        primitive = _PRIMITIVES.get(value, "string")
        return TypeRef(
            additional_properties=TypeRef(primitive=primitive, raw=value),
            raw=raw,
        )

    # array[...]
    if text.lower().startswith("array["):
        if not text.endswith("]"):
            return TypeRef(primitive="object", raw=raw)
        inner = text[len("array[") : -1].strip()
        if inner == "":
            return TypeRef(array_items=TypeRef(raw=""), raw=raw)
        if inner.lower().startswith("any of:"):
            return TypeRef(
                array_items=_parse_any_of(inner[len("Any of:") :].strip(), inner),
                raw=raw,
            )
        return TypeRef(array_items=_parse(inner, inner), raw=raw)

    # Any of:
    if text.lower().startswith("any of:"):
        return _parse_any_of(text[len("Any of:") :].strip(), raw)

    # link:#anchor[label]
    link_match = _LINK_RE.search(text)
    if link_match:
        return TypeRef(ref_anchor=link_match.group("anchor").strip(), raw=raw)

    # primitives (case-insensitive)
    primitive = _PRIMITIVES.get(text.lower())
    if primitive is not None:
        return TypeRef(primitive=primitive, raw=raw)

    # Unknown type. Default to a permissive object so the spec still validates;
    # surface the original text so it can be triaged from the generated output.
    return TypeRef(primitive="object", raw=raw)


def _parse_any_of(text: str, raw: str) -> TypeRef:
    """Parse the comma-separated body of an ``Any of:`` expression.

    Splits at top-level commas (not inside ``link:#...[...]`` brackets).
    """
    parts = _split_top_level_commas(text)
    members = tuple(_parse(p.strip(), p.strip()) for p in parts if p.strip())
    return TypeRef(one_of=members, raw=raw)


def _split_top_level_commas(text: str) -> list[str]:
    out: list[str] = []
    depth = 0
    buf: list[str] = []
    for ch in text:
        if ch in "[(":
            depth += 1
            buf.append(ch)
        elif ch in "])":
            depth = max(depth - 1, 0)
            buf.append(ch)
        elif ch == "," and depth == 0:
            out.append("".join(buf))
            buf = []
        else:
            buf.append(ch)
    if buf:
        out.append("".join(buf))
    return out
