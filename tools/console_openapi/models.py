"""Intermediate AST produced by the parser, consumed by the OpenAPI builder.

These models describe parsed AsciiDoc content in a form that is decoupled from
OpenAPI itself. The builder maps them into OpenAPI 3.0.3 structures.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field, model_validator


class Frozen(BaseModel):
    """Base for frozen, strict Pydantic models."""

    model_config = ConfigDict(frozen=True, extra="forbid")


class TypeRef(Frozen):
    """Parsed representation of a type expression from a docs table cell.

    One and only one of the optional fields is set.
    """

    primitive: str | None = None
    """Primitive type name: 'string', 'integer', 'number', 'boolean', 'object'."""

    ref_anchor: str | None = None
    """Local AsciiDoc anchor (without the leading '#') for a definition reference."""

    array_items: TypeRef | None = None
    """When set, this type is an array whose items have the given type."""

    one_of: tuple[TypeRef, ...] | None = None
    """When set, this type is a oneOf union of the given types."""

    additional_properties: TypeRef | None = None
    """When set, this type is an object with additionalProperties of the given type."""

    raw: str = ""
    """Original cell text, preserved for diagnostics."""

    @model_validator(mode="after")
    def _exactly_one_kind(self) -> TypeRef:
        kinds = (
            self.primitive,
            self.ref_anchor,
            self.array_items,
            self.one_of,
            self.additional_properties,
        )
        set_count = sum(1 for k in kinds if k is not None)
        if set_count > 1:
            raise ValueError(
                "TypeRef must have at most one of {primitive, ref_anchor, "
                "array_items, one_of, additional_properties} set; "
                f"got {set_count}"
            )
        return self


class FieldDef(Frozen):
    """One row of a parameters / body / response / definition table."""

    name: str
    type: TypeRef
    required: bool
    description: str
    location: str | None = None
    """Parameter location ('header', 'query', 'path', 'cookie'), only for parameters."""


class Definition(Frozen):
    """A named ``[#anchor]`` schema from the ``== Definitions`` block."""

    anchor: str
    """The anchor name as written in the source (used to resolve link references)."""

    title: str
    """Human-readable title shown next to the anchor in the docs."""

    fields: tuple[FieldDef, ...] = ()
    """Fields parsed from a 4-column definition table; empty if none was provided."""

    fallback_kind: str | None = None
    """Set when the definition has no table; e.g. 'hash_string_string', 'prose'."""

    description: str = ""
    """Free-text description (only useful for fallback definitions)."""


class ResponseBlock(Frozen):
    """A single ``== Response`` or ``== Error`` block."""

    status: int
    description: str
    fields: tuple[FieldDef, ...] = ()
    example: Any = None
    """Parsed JSON example, or None if no example block was provided."""

    example_raw: str | None = None
    """Raw example text when JSON parsing failed; None otherwise."""


class ParsedEndpoint(Frozen):
    """An endpoint file parsed into its constituent sections."""

    source_file: str
    """Path of the source ``.adoc`` file relative to the repo root."""

    service: str
    """Top-level service folder, e.g. 'tenancy', 'tenancyv4'."""

    permalink: str
    summary: str
    title: str
    description: str
    method: str
    path: str
    token_usage: str | None = None
    """e.g. 'user', 'service'; parsed from '*Token usage:*' callout."""

    parameters: tuple[FieldDef, ...] = ()
    request_body_fields: tuple[FieldDef, ...] = ()
    request_body_example: Any = None
    request_body_example_raw: str | None = None
    responses: tuple[ResponseBlock, ...] = ()
    definitions: tuple[Definition, ...] = ()


class ParseError(Frozen):
    """Recoverable parser failure recorded in the build report."""

    source_file: str
    section: str
    message: str


class ParseReport(Frozen):
    """Aggregated result of a parse run."""

    endpoints: tuple[ParsedEndpoint, ...] = Field(default_factory=tuple)
    skipped_overview: tuple[str, ...] = Field(default_factory=tuple)
    """Paths of files that have ``api: true`` but no operation line."""

    errors: tuple[ParseError, ...] = Field(default_factory=tuple)
