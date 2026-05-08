"""Endpoint-file orchestrator.

Combines the smaller parsers into a :class:`ParsedEndpoint`.
"""

from __future__ import annotations

import json
import re
from typing import Any

from tools.console_openapi.models import (
    Definition,
    FieldDef,
    ParsedEndpoint,
    ResponseBlock,
)
from tools.console_openapi.parser.asciidoc_tables import (
    assert_headers,
    parse_table,
)
from tools.console_openapi.parser.frontmatter import split_frontmatter
from tools.console_openapi.parser.operation import find_operation
from tools.console_openapi.parser.types import parse_type

PARAMS_HEADERS = ("Name", "Type", "In", "Required", "Description")
BODY_HEADERS = ("Name", "Type", "Required", "Description")
RESPONSE_HEADERS = BODY_HEADERS

_TITLE_RE = re.compile(r"^=\s+(?P<title>.+?)\s*$", re.MULTILINE)
_TOKEN_USAGE_RE = re.compile(
    r"\*Token usage:\*\s*BlueXP\s+(?P<kind>user|service)\s+token\.", re.IGNORECASE
)
_STATUS_LINE_RE = re.compile(r"Status:\s*(?P<code>\d{3}),\s*(?P<desc>.+?)\s*$", re.MULTILINE)


class EndpointParseError(ValueError):
    """Raised when an endpoint file cannot be parsed in strict mode."""


def parse_endpoint(text: str, source_file: str, service: str) -> ParsedEndpoint | None:
    """Parse an endpoint file. Returns ``None`` for non-endpoint pages.

    A non-endpoint page is one whose front-matter has ``api: true`` but which
    contains no operation line (overview/index pages).
    """
    fm, body = split_frontmatter(text)

    op = find_operation(body)
    if op is None:
        return None
    method, path = op

    title = _extract_title(body) or fm.get("summary", "")
    summary = str(fm.get("summary", title))
    permalink = str(fm.get("permalink", ""))

    description, token_usage = _extract_description_and_token(body)

    sections = _split_sections(body)

    parameters: tuple[FieldDef, ...] = ()
    if "Parameters" in sections:
        parameters = _parse_parameters_section(sections["Parameters"])

    request_body_fields: tuple[FieldDef, ...] = ()
    request_body_example: Any = None
    request_body_example_raw: str | None = None
    if "Request Body" in sections:
        rb_fields, rb_example, rb_example_raw = _parse_body_section(sections["Request Body"])
        request_body_fields = rb_fields
        request_body_example = rb_example
        request_body_example_raw = rb_example_raw

    responses = _parse_response_blocks(body)

    definitions: tuple[Definition, ...] = ()
    if "Definitions" in sections:
        definitions = _parse_definitions_section(sections["Definitions"])

    return ParsedEndpoint(
        source_file=source_file,
        service=service,
        permalink=permalink,
        summary=summary,
        title=title,
        description=description,
        method=method,
        path=path,
        token_usage=token_usage,
        parameters=parameters,
        request_body_fields=request_body_fields,
        request_body_example=request_body_example,
        request_body_example_raw=request_body_example_raw,
        responses=responses,
        definitions=definitions,
    )


def _extract_title(body: str) -> str:
    match = _TITLE_RE.search(body)
    return match.group("title") if match else ""


def _extract_description_and_token(body: str) -> tuple[str, str | None]:
    """Extract the prose paragraph between the operation line and the first ``==``.

    Also detects the ``*Token usage:*`` callout if present.
    """
    op_pattern = re.compile(r"\[\.api-doc-operation[^\n]*\n", re.IGNORECASE)
    section_pattern = re.compile(r"^==\s+", re.MULTILINE)

    op_match = op_pattern.search(body)
    if op_match is None:
        return "", None
    after_op = body[op_match.end() :]
    sec_match = section_pattern.search(after_op)
    chunk = after_op if sec_match is None else after_op[: sec_match.start()]
    lines = [line.strip() for line in chunk.splitlines() if line.strip()]
    text_lines: list[str] = []
    token_usage: str | None = None
    for line in lines:
        token_match = _TOKEN_USAGE_RE.search(line)
        if token_match:
            token_usage = token_match.group("kind").lower()
            continue
        if line == "+":
            continue
        text_lines.append(line)
    return " ".join(text_lines).strip(), token_usage


def _split_sections(body: str) -> dict[str, str]:
    """Split the body into ``{== Section Name: text}`` chunks.

    Multiple ``== Error`` blocks collapse into a single ``"Error"`` entry whose
    value contains all of them concatenated. Use :func:`_parse_response_blocks`
    rather than this helper when individual error blocks are needed.
    """
    pattern = re.compile(r"^==\s+(?P<name>.+?)\s*$", re.MULTILINE)
    matches = list(pattern.finditer(body))
    sections: dict[str, str] = {}
    for i, m in enumerate(matches):
        name = m.group("name").strip()
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(body)
        chunk = body[start:end]
        if name in sections:
            sections[name] = sections[name] + "\n" + chunk
        else:
            sections[name] = chunk
    return sections


def _parse_parameters_section(text: str) -> tuple[FieldDef, ...]:
    blocks = _find_table_blocks(text)
    if not blocks:
        return ()
    table = parse_table(blocks[0], expected_cols=5)
    assert_headers(table, PARAMS_HEADERS)
    out: list[FieldDef] = []
    for row in table.rows:
        name, type_text, in_text, required_text, desc = row
        out.append(
            FieldDef(
                name=name.strip(),
                type=parse_type(type_text),
                required=_required(required_text),
                description=_clean_description(desc),
                location=in_text.strip().lower() or None,
            )
        )
    return tuple(out)


def _parse_body_section(
    text: str,
) -> tuple[tuple[FieldDef, ...], Any, str | None]:
    blocks = _find_table_blocks(text)
    fields: tuple[FieldDef, ...] = ()
    if blocks:
        table = parse_table(blocks[0], expected_cols=4)
        assert_headers(table, BODY_HEADERS)
        fields = tuple(_field_from_row(row) for row in table.rows)
    example, example_raw = _extract_example(text)
    return fields, example, example_raw


def _parse_response_blocks(body: str) -> tuple[ResponseBlock, ...]:
    """Parse the ``== Response`` block plus every ``== Error`` block in order.

    Note: when multiple blocks share the same status code (rare in this corpus),
    the last one wins because the builder keys responses by status string. This
    is intentional — upstream's structure does not normally repeat status codes
    within a single endpoint.
    """
    pattern = re.compile(r"^==\s+(?P<name>Response|Error)\s*$", re.MULTILINE)
    matches = list(pattern.finditer(body))
    out: list[ResponseBlock] = []
    for m in matches:
        start = m.end()
        end = _next_section_offset(body, m.end())
        chunk = body[start:end]
        status_match = _STATUS_LINE_RE.search(chunk)
        if not status_match:
            continue
        status = int(status_match.group("code"))
        description = status_match.group("desc").strip()
        # Trim Definitions if it accidentally fell into this chunk
        chunk_after_status = chunk[status_match.end() :]
        # Stop at next '== ' header inside the same chunk (safety)
        next_section = re.search(r"^==\s+", chunk_after_status, re.MULTILINE)
        if next_section is not None:
            chunk_after_status = chunk_after_status[: next_section.start()]
        blocks = _find_table_blocks(chunk_after_status)
        fields: tuple[FieldDef, ...] = ()
        if blocks:
            table = parse_table(blocks[0], expected_cols=4)
            assert_headers(table, RESPONSE_HEADERS)
            fields = tuple(_field_from_row(row) for row in table.rows)
        example, example_raw = _extract_example(chunk_after_status)
        out.append(
            ResponseBlock(
                status=status,
                description=description,
                fields=fields,
                example=example,
                example_raw=example_raw,
            )
        )
    return tuple(out)


def _parse_definitions_section(text: str) -> tuple[Definition, ...]:
    """Parse every ``[#anchor]`` block in the Definitions section.

    A definition may be:
    * table-backed (4 columns) - parsed as fields,
    * a hash mapping (no table, just prose like ``Hash mapping strings to string``),
    * prose-only (no table, no recognized hash phrase).
    """
    anchor_re = re.compile(r"^\[#(?P<anchor>[^\]]+)\]\s*$", re.MULTILINE)
    matches = list(anchor_re.finditer(text))
    out: list[Definition] = []
    for i, m in enumerate(matches):
        anchor = m.group("anchor").strip()
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        chunk = text[start:end]

        title = _extract_definition_title(chunk) or anchor

        blocks = _find_table_blocks(chunk)
        if blocks:
            table = parse_table(blocks[0], expected_cols=4)
            assert_headers(table, BODY_HEADERS)
            fields = tuple(_field_from_row(row) for row in table.rows)
            out.append(Definition(anchor=anchor, title=title, fields=fields))
            continue

        # No table: classify prose
        prose = _strip_collapsible_markers(chunk).strip()
        kind = "prose"
        if re.search(r"hash mapping strings? to ", prose, re.IGNORECASE):
            kind = "hash_string_string"
        out.append(
            Definition(
                anchor=anchor,
                title=title,
                fallback_kind=kind,
                description=prose[:1000],
            )
        )
    return tuple(out)


def _extract_definition_title(chunk: str) -> str:
    """Extract the human-readable title that follows ``[.api-collapsible-fifth-title]``."""
    m = re.search(
        r"\[\.api-collapsible-fifth-title\]\s*\n(?P<title>[^\n]+)",
        chunk,
    )
    return m.group("title").strip() if m else ""


def _strip_collapsible_markers(chunk: str) -> str:
    return re.sub(r"^\[.+\]\s*$", "", chunk, flags=re.MULTILINE)


def _find_table_blocks(text: str) -> list[str]:
    lines = text.splitlines()
    out: list[str] = []
    i = 0
    while i < len(lines):
        if lines[i].strip() == "|===":
            start = i
            j = i + 1
            while j < len(lines) and lines[j].strip() != "|===":
                j += 1
            if j < len(lines):
                out.append("\n".join(lines[start : j + 1]))
                i = j + 1
                continue
        i += 1
    return out


def _next_section_offset(body: str, start: int) -> int:
    m = re.search(r"^==\s+", body[start:], re.MULTILINE)
    if m is None:
        return len(body)
    return start + m.start()


def _required(text: str) -> bool:
    return text.strip().lower() in {"true", "yes", "required"}


def _clean_description(text: str) -> str:
    """Reduce the Description cell to a single-line summary.

    Bullet sub-entries (``* example: ...``) and embedded code blocks are
    stripped; only the leading prose is kept. The full text remains available
    via the original AST should we ever need richer descriptions.
    """
    stripped = re.sub(r"^\s*\*\s+.+$", "", text, flags=re.MULTILINE)
    stripped = re.sub(r"\s+", " ", stripped).strip()
    return stripped


def _field_from_row(row: tuple[str, ...]) -> FieldDef:
    name, type_text, required_text, desc = row
    return FieldDef(
        name=name.strip(),
        type=parse_type(type_text),
        required=_required(required_text),
        description=_clean_description(desc),
    )


def _extract_example(text: str) -> tuple[Any, str | None]:
    """Extract the first ``[source,json,...]`` example block in ``text``.

    Returns ``(parsed_example_or_None, raw_text_or_None)``. ``raw_text`` is
    only set when JSON parsing fails.
    """
    m = re.search(
        r"\[source,json[^\]]*\]\s*\n(?P<json>.+?)(?:\n=====?\s*$|\n----\s*$|\Z)",
        text,
        re.DOTALL | re.MULTILINE,
    )
    if not m:
        return None, None
    raw = m.group("json").strip()
    try:
        return json.loads(raw), None
    except (ValueError, json.JSONDecodeError):
        return None, raw
