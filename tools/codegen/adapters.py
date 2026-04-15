"""OpenAPI spec adapters for parsing endpoints and schemas.

Parses OpenAPI 3.0 specs (all API specs are pre-converted to OpenAPI 3.0
by the ``doit convert_specs`` task) and produces normalized
:class:`ParsedEndpoint` and :class:`ParsedField` dataclasses.

Uses ``datamodel-code-generator`` for ``$ref`` resolution and type mapping,
then extracts the resolved field structure for nested model generation.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from datamodel_code_generator.parser.openapi import OpenAPIParser

from tools.codegen.expensive_fields import extract_expensive_patterns, is_field_expensive


@dataclass
class ParsedField:
    """A single resolved field from an API schema.

    Attributes:
        name: Field name as it appears in the schema (e.g. ``"name"``).
        api_path: Dot-path from the root schema (e.g. ``"svm.name"``).
        python_type: Python type string (e.g. ``"str"``, ``"int"``,
            ``"list[str]"``).
        is_uuid: Whether this field has ``format: uuid`` in the spec.
        is_list: Whether this field is an array type.
        is_object: Whether this field is a nested object (has sub-fields).
        description: Field description from the spec.
        introduced_version: ONTAP version when the field was introduced
            (from ``x-ntap-introduced``).
        requires_explicit_fetch: Whether this field is expensive to fetch.
        default: Default value appropriate for the Python type.
        enum_values: Enum values if the field is an enum type.
        sub_fields: Child fields for nested objects.
    """

    name: str
    api_path: str
    python_type: str = "str"
    is_uuid: bool = False
    is_list: bool = False
    is_object: bool = False
    description: str = ""
    introduced_version: str = ""
    requires_explicit_fetch: bool = False
    default: Any = ""
    enum_values: list[str] = field(default_factory=list)
    sub_fields: list[ParsedField] = field(default_factory=list)


@dataclass
class ParsedEndpoint:
    """A parsed API endpoint with its response schema fields.

    Attributes:
        path: API path (e.g. ``"/storage/volumes"``).
        method: HTTP method (e.g. ``"get"``).
        schema_name: Name of the response schema (e.g. ``"volume"``).
        description: Endpoint description text.
        records_path: Path to the records array in the response envelope.
        fields: Flattened list of all fields in the response schema.
        expensive_patterns: Raw expensive field patterns from description.
        has_parent: Whether this endpoint has path parameters (e.g.
            ``/svm/svms/{svm.uuid}/...``).
        parent_path: The parent resource path segment if parameterized.
        tags: API tags for grouping.
        identifier_field: Inferred single-field identifier used to address
            a collection item (e.g. ``"uuid"`` for ``/storage/volumes``
            whose sibling item endpoint is ``/storage/volumes/{uuid}``).
            ``None`` when no sibling item endpoint exists or when the item
            endpoint has multiple path parameters.  Composite identifiers
            are not inferred; nested response-field identifiers (e.g.
            ``"volume.uuid"``) must be set via a manual edit after codegen.
    """

    path: str
    method: str = "get"
    schema_name: str = ""
    description: str = ""
    records_path: str = "records"
    fields: list[ParsedField] = field(default_factory=list)  # tree structure
    expensive_patterns: list[str] = field(default_factory=list)
    has_parent: bool = False
    parent_path: str = ""
    tags: list[str] = field(default_factory=list)
    identifier_field: str | None = None


# OpenAPI type → (python_type, default_value)
_TYPE_MAP: dict[str, tuple[str, Any]] = {
    "string": ("str", ""),
    "integer": ("int", 0),
    "number": ("float", 0.0),
    "boolean": ("bool", False),
}


def _resolve_ref(spec: dict[str, Any], ref: str) -> dict[str, Any]:
    """Resolve a JSON ``$ref`` pointer within a spec.

    Args:
        spec: The full OpenAPI spec dict.
        ref: A ``$ref`` string like ``"#/components/schemas/Volume"``.

    Returns:
        The resolved schema dict, or empty dict if resolution fails.
    """
    parts = ref.lstrip("#/").split("/")
    node: Any = spec
    for part in parts:
        if not isinstance(node, dict) or part not in node:
            return {}
        node = node[part]
    return node if isinstance(node, dict) else {}


def _flatten_schema(
    spec: dict[str, Any],
    schema: dict[str, Any],
    prefix: str,
    expensive_patterns: list[str],
    visited: set[str] | None = None,
    depth: int = 0,
    max_depth: int = 5,
) -> list[ParsedField]:
    """Recursively parse an OpenAPI schema into a tree of dot-path fields.

    Nested objects are represented as ``ParsedField`` nodes with
    ``sub_fields`` holding their children — the tree structure is
    preserved (children are **not** promoted to the parent list).

    Args:
        spec: The full OpenAPI spec (for ``$ref`` resolution).
        schema: The schema dict to parse.
        prefix: Current dot-path prefix.
        expensive_patterns: Expensive field patterns for annotation.
        visited: Set of ``$ref`` strings already visited (cycle guard).
        depth: Current recursion depth.
        max_depth: Maximum recursion depth to prevent unbounded nesting.

    Returns:
        List of :class:`ParsedField` instances (tree structure).
    """
    if depth > max_depth:
        return []

    if visited is None:
        visited = set()

    # Resolve $ref
    ref = schema.get("$ref")
    if ref:
        if ref in visited:
            return []
        visited = visited | {ref}
        schema = _resolve_ref(spec, ref)

    # Handle allOf (merge all schemas)
    if "allOf" in schema:
        merged_props: dict[str, Any] = {}
        for sub in schema["allOf"]:
            resolved = sub
            if "$ref" in sub:
                resolved = _resolve_ref(spec, sub["$ref"])
            merged_props.update(resolved.get("properties", {}))
        schema = {**schema, "properties": merged_props}

    properties = schema.get("properties", {})
    fields: list[ParsedField] = []

    for name, prop in properties.items():
        # Skip internal/link fields
        if name.startswith("_"):
            continue

        api_path = f"{prefix}.{name}" if prefix else name
        resolved_prop = prop
        if "$ref" in prop:
            if prop["$ref"] in visited:
                continue
            visited = visited | {prop["$ref"]}
            resolved_prop = _resolve_ref(spec, prop["$ref"])

        # Handle allOf in property
        if "allOf" in resolved_prop:
            merged: dict[str, Any] = {}
            for sub in resolved_prop["allOf"]:
                r = sub
                if "$ref" in sub:
                    r = _resolve_ref(spec, sub["$ref"])
                merged.update(r)
            resolved_prop = merged

        prop_type = resolved_prop.get("type", "")
        prop_format = resolved_prop.get("format", "")
        description = resolved_prop.get("description", "")
        introduced = resolved_prop.get("x-ntap-introduced", "")
        enum_values = resolved_prop.get("enum", [])
        is_expensive = is_field_expensive(api_path, expensive_patterns)

        if prop_type == "object" and "properties" in resolved_prop:
            # Nested object — recurse
            sub_fields = _flatten_schema(
                spec,
                resolved_prop,
                api_path,
                expensive_patterns,
                visited,
                depth + 1,
                max_depth,
            )
            fields.append(
                ParsedField(
                    name=name,
                    api_path=api_path,
                    python_type="object",
                    is_object=True,
                    description=description,
                    introduced_version=str(introduced) if introduced else "",
                    requires_explicit_fetch=is_expensive,
                    sub_fields=sub_fields,
                )
            )
        elif prop_type == "array":
            items = resolved_prop.get("items", {})
            if "$ref" in items:
                items = _resolve_ref(spec, items["$ref"])

            items_type = items.get("type", "string")
            if items_type == "object" and "properties" in items:
                # Array of objects — recurse into items
                sub_fields = _flatten_schema(
                    spec,
                    items,
                    api_path,
                    expensive_patterns,
                    visited,
                    depth + 1,
                    max_depth,
                )
                py_type = "list[dict[str, Any]]"
                fields.append(
                    ParsedField(
                        name=name,
                        api_path=api_path,
                        python_type=py_type,
                        is_list=True,
                        is_object=True,
                        description=description,
                        introduced_version=str(introduced) if introduced else "",
                        requires_explicit_fetch=is_expensive,
                        default=[],
                        sub_fields=sub_fields,
                    )
                )
            else:
                item_py = _TYPE_MAP.get(items_type, ("str", ""))[0]
                py_type = f"list[{item_py}]"
                fields.append(
                    ParsedField(
                        name=name,
                        api_path=api_path,
                        python_type=py_type,
                        is_list=True,
                        description=description,
                        introduced_version=str(introduced) if introduced else "",
                        requires_explicit_fetch=is_expensive,
                        default=[],
                    )
                )
        else:
            # Scalar field
            is_uuid = prop_format == "uuid"
            py_type_str, default = _TYPE_MAP.get(prop_type, ("str", ""))
            if is_uuid:
                py_type_str = "OntapUUID"
            fields.append(
                ParsedField(
                    name=name,
                    api_path=api_path,
                    python_type=py_type_str,
                    is_uuid=is_uuid,
                    description=description,
                    introduced_version=str(introduced) if introduced else "",
                    requires_explicit_fetch=is_expensive,
                    default=default,
                    enum_values=enum_values,
                )
            )

    return fields


def _detect_records_path(
    spec: dict[str, Any],
    response_schema: dict[str, Any],
) -> tuple[str, dict[str, Any]]:
    """Detect the records path and item schema from a response schema.

    Looks for common patterns:
    - ONTAP: ``{records: [{...}], num_records: int}``
    - Direct array response

    Args:
        spec: Full OpenAPI spec for ``$ref`` resolution.
        response_schema: The 200 response schema.

    Returns:
        Tuple of (records_path, item_schema).
    """
    if "$ref" in response_schema:
        response_schema = _resolve_ref(spec, response_schema["$ref"])

    props = response_schema.get("properties", {})

    # ONTAP pattern: {records: [items], num_records: int}
    if "records" in props:
        records_prop = props["records"]
        if records_prop.get("type") == "array":
            items = records_prop.get("items", {})
            if "$ref" in items:
                items = _resolve_ref(spec, items["$ref"])
            return "records", items

    # Direct array response
    if response_schema.get("type") == "array":
        items = response_schema.get("items", {})
        if "$ref" in items:
            items = _resolve_ref(spec, items["$ref"])
        return "", items

    # Fallback: look for first array property
    for prop_name, prop_val in props.items():
        if prop_name.startswith("_"):
            continue
        if prop_val.get("type") == "array":
            items = prop_val.get("items", {})
            if "$ref" in items:
                items = _resolve_ref(spec, items["$ref"])
            return prop_name, items

    return "records", response_schema


def _extract_schema_name_from_ref(ref: str) -> str:
    """Extract the schema name from a ``$ref`` string.

    Args:
        ref: A ``$ref`` like ``"#/components/schemas/volume"``.

    Returns:
        The schema name (e.g. ``"volume"``).
    """
    return ref.rsplit("/", 1)[-1]


def _detect_parent_path(path: str) -> tuple[bool, str]:
    """Detect if an endpoint path is parameterized (has a parent resource).

    Args:
        path: API path like ``"/svm/svms/{svm.uuid}/web"``.

    Returns:
        Tuple of (has_parent, parent_path_segment).
    """
    # Find segments with {placeholders}
    segments = path.strip("/").split("/")
    for i, seg in enumerate(segments):
        if "{" in seg:
            parent = "/" + "/".join(segments[:i])
            return True, parent
    return False, ""


def _build_identifier_map(all_paths: list[str]) -> dict[str, str]:
    """Build a ``{collection_path: identifier_param_name}`` lookup.

    Scans every path in the spec for item endpoints of the form
    ``/foo/bar/{param}`` and pairs them with their collection path
    ``/foo/bar``.  Only item endpoints with **exactly one** path
    parameter qualify — composite identifiers and deeply-parameterized
    paths are skipped so the caller can fall back to manual editing for
    those edge cases.

    The inner name of ``{param}`` is returned, e.g. ``/storage/volumes``
    paired with ``/storage/volumes/{uuid}`` yields ``"uuid"``.

    Args:
        all_paths: Every path string defined in the OpenAPI spec.

    Returns:
        Mapping from collection path to single identifier parameter name.
        Collections without a qualifying sibling item endpoint are absent
        from the returned dict.
    """
    identifiers: dict[str, str] = {}
    path_set = set(all_paths)
    for path in all_paths:
        # We're looking for paths of the form `/foo/bar/{param}`
        # whose parent `/foo/bar` also exists and has no other params.
        segments = path.strip("/").split("/")
        if not segments or "{" not in segments[-1] or "}" not in segments[-1]:
            continue
        # Count path parameters in the whole path.  Multi-param item
        # endpoints are skipped — those imply composite identifiers
        # (which we don't auto-infer) or parameterized parents (already
        # handled by `has_parent`).
        total_params = sum(1 for s in segments if "{" in s)
        if total_params != 1:
            continue
        param_name = segments[-1].strip("{}")
        collection_segments = segments[:-1]
        if not collection_segments:
            continue
        collection_path = "/" + "/".join(collection_segments)
        if collection_path not in path_set:
            continue
        # If multiple item endpoints somehow map to the same collection
        # (shouldn't happen in well-formed specs), first one wins and
        # subsequent candidates are ignored.
        identifiers.setdefault(collection_path, param_name)
    return identifiers


def parse_openapi_spec(
    spec_path: Path,
    api_type: str = "ontap",
) -> list[ParsedEndpoint]:
    """Parse an OpenAPI 3.0 spec file into normalized endpoints.

    Args:
        spec_path: Path to the OpenAPI 3.0 JSON spec.
        api_type: API type tag (``"ontap"``, ``"aiqum"``, ``"dii"``,
            ``"occm"``).  Controls expensive field detection (ONTAP only).

    Returns:
        List of :class:`ParsedEndpoint` for all GET endpoints with
        response schemas.
    """
    with open(spec_path, encoding="utf-8") as f:
        spec = json.load(f)

    # Run datamodel-code-generator parser for $ref resolution and type cross-reference.
    # The resolved models are available for future type validation enhancements.
    _parse_with_datamodel_codegen(spec_path)

    endpoints: list[ParsedEndpoint] = []
    paths = spec.get("paths", {})

    for path, methods in paths.items():
        if not isinstance(methods, dict):
            continue

        get_op = methods.get("get")
        if not get_op or not isinstance(get_op, dict):
            continue

        description = get_op.get("description", "")
        tags = get_op.get("tags", [])

        # Extract expensive field patterns (ONTAP only)
        expensive_patterns: list[str] = []
        if api_type == "ontap":
            expensive_patterns = extract_expensive_patterns(description)

        # Find the 200 response schema
        responses = get_op.get("responses", {})
        ok_response = responses.get("200", {})
        content = ok_response.get("content", {})
        json_content = content.get("application/json", content.get("application/hal+json", {}))
        response_schema = json_content.get("schema", {})

        if not response_schema:
            continue

        # Detect records path and item schema
        records_path, item_schema = _detect_records_path(spec, response_schema)

        if not item_schema or not item_schema.get("properties"):
            continue

        # Extract schema name
        schema_name = ""
        records_prop = response_schema
        if "$ref" in response_schema:
            records_prop = _resolve_ref(spec, response_schema["$ref"])
        records_items = records_prop.get("properties", {}).get("records", {}).get("items", {})
        if "$ref" in records_items:
            schema_name = _extract_schema_name_from_ref(records_items["$ref"])
        elif "$ref" in response_schema:
            schema_name = _extract_schema_name_from_ref(response_schema["$ref"])

        # Flatten the item schema into fields
        fields = _flatten_schema(spec, item_schema, "", expensive_patterns)

        if not fields:
            continue

        # Detect parent path
        has_parent, parent_path = _detect_parent_path(path)

        endpoints.append(
            ParsedEndpoint(
                path=path,
                method="get",
                schema_name=schema_name,
                description=description,
                records_path=records_path,
                fields=fields,
                expensive_patterns=expensive_patterns,
                has_parent=has_parent,
                parent_path=parent_path,
                tags=tags,
            )
        )

    # Second pass: infer ``identifier_field`` for collection endpoints by
    # matching them against sibling item endpoints (``/foo`` + ``/foo/{x}``).
    # The spec contains many item endpoints that are never generated (they
    # don't have list response schemas), so we scan *all* paths from the
    # spec — not just the parsed endpoints — when building the lookup.
    identifier_map = _build_identifier_map(list(paths.keys()))
    for ep in endpoints:
        param = identifier_map.get(ep.path)
        if param is not None:
            ep.identifier_field = param

    return endpoints


def _parse_with_datamodel_codegen(spec_path: Path) -> dict[str, Any]:
    """Use datamodel-code-generator to parse and resolve schemas.

    This leverages the library's ``$ref`` resolution and type mapping
    capabilities.  The results are used to cross-reference type information
    when our own flattening logic needs confirmation.

    Args:
        spec_path: Path to the OpenAPI 3.0 JSON spec.

    Returns:
        Dict mapping model name to parsed model info.
    """
    try:
        parser = OpenAPIParser(
            source=spec_path,
        )
        parser.parse()

        models: dict[str, Any] = {}
        for result in parser.results:
            name = getattr(result, "name", None)
            if name and hasattr(result, "fields"):
                field_info = {}
                for f in result.fields:
                    dt = f.data_type
                    ref_name = None
                    if hasattr(dt, "reference") and dt.reference:
                        ref_name = dt.reference.name
                    prim_type = getattr(dt, "type", None)
                    field_info[f.name] = {
                        "type_hint": getattr(f, "type_hint", ""),
                        "required": f.required,
                        "reference": ref_name,
                        "primitive_type": str(prim_type) if prim_type else None,
                    }
                models[name] = {"fields": field_info}
        return models
    except Exception:
        # Non-fatal: we can still generate from our own parsing
        return {}
