"""Convert assembled OCCM Swagger 1.2 spec to Swagger 2.0.

The OCCM spec is assembled from per-resource Swagger 1.2 declarations
into a single JSON file by fetch_occm_spec.py. This script converts
that assembled format into standard Swagger 2.0 that swagger2openapi
can then convert to OpenAPI 3.0.

Swagger 1.2 -> 2.0 mapping:
    - paramType -> in (query/path/body/header/formData)
    - type on operation -> responses.200.schema
    - $ref without prefix -> $ref with #/definitions/ prefix
    - models -> definitions
    - nickname -> operationId
    - apis[].operations[] -> paths[method]
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

# Swagger 1.2 paramType -> Swagger 2.0 'in' value
_PARAM_TYPE_MAP = {
    "query": "query",
    "path": "path",
    "body": "body",
    "header": "header",
    "form": "formData",
}

# Java generic patterns from OCCM's Scala backend
_LIST_RE = re.compile(r"^List\[(.+)]$")
_MAP_RE = re.compile(r"^Map\[string,(.+)]$")

# Primitive types in Swagger
_PRIMITIVE_TYPES = frozenset({"string", "integer", "number", "boolean"})


def _is_java_class_name(type_name: str) -> bool:
    """Check if a type name is a fully qualified Java class (e.g., com.netapp.foo.Bar)."""
    return "." in type_name and not type_name.startswith("#/")


def _resolve_java_type(type_name: str) -> dict[str, Any]:
    """Resolve a Java generic type name to a Swagger 2.0 schema.

    Handles:
        List[X]                -> {type: array, items: {schema for X}}
        Map[string,X]          -> {type: object, additionalProperties: {schema for X}}
        Map[string,List[X]]    -> nested resolution
        Map[string,Object]     -> {type: object}
        Object                 -> {type: object}
        com.netapp.foo.Bar     -> {type: object} (dangling Java class ref)
        primitive              -> {type: primitive}
        ModelName              -> {$ref: #/definitions/ModelName}
    """
    if type_name == "Object":
        return {"type": "object"}

    # Fully qualified Java class names -> opaque object
    if _is_java_class_name(type_name):
        return {"type": "object"}

    list_match = _LIST_RE.match(type_name)
    if list_match:
        inner = list_match.group(1)
        return {"type": "array", "items": _resolve_java_type(inner)}

    map_match = _MAP_RE.match(type_name)
    if map_match:
        inner = map_match.group(1)
        return {"type": "object", "additionalProperties": _resolve_java_type(inner)}

    if type_name in _PRIMITIVE_TYPES:
        return {"type": type_name}

    # It's a model reference
    return {"$ref": f"#/definitions/{type_name}"}


def _convert_ref(ref: str) -> dict[str, Any] | str:
    """Convert a Swagger 1.2 $ref to Swagger 2.0 format.

    Returns a schema dict for Java generics/classes, or a $ref string for normal refs.
    """
    if ref.startswith("#/"):
        return ref

    # Java generic types or fully qualified class names
    if "[" in ref or _is_java_class_name(ref):
        return _resolve_java_type(ref)

    return f"#/definitions/{ref}"


def _convert_type_to_schema(
    type_info: dict[str, Any],
) -> dict[str, Any]:
    """Convert a Swagger 1.2 type/items to a Swagger 2.0 schema object."""
    schema: dict[str, Any] = {}

    if "$ref" in type_info:
        resolved = _convert_ref(type_info["$ref"])
        if isinstance(resolved, dict):
            # Java generic resolved to inline schema
            schema = resolved
        else:
            schema["$ref"] = resolved
    elif type_info.get("type") == "array":
        schema["type"] = "array"
        items = type_info.get("items", {})
        if "$ref" in items:
            resolved = _convert_ref(items["$ref"])
            if isinstance(resolved, dict):
                schema["items"] = resolved
            else:
                schema["items"] = {"$ref": resolved}
        elif "type" in items:
            schema["items"] = {"type": items["type"]}
            if "format" in items:
                schema["items"]["format"] = items["format"]
    else:
        t = type_info.get("type", "string")
        # Check if type itself is a Java generic
        if "[" in t:
            schema = _resolve_java_type(t)
        elif t == "Object":
            schema["type"] = "object"
        else:
            schema["type"] = t
            if "format" in type_info:
                schema["format"] = type_info["format"]
            if "enum" in type_info:
                schema["enum"] = type_info["enum"]

    return schema


def _convert_parameter(param: dict[str, Any]) -> dict[str, Any]:
    """Convert a Swagger 1.2 parameter to Swagger 2.0."""
    converted: dict[str, Any] = {
        "name": param["name"],
        "in": _PARAM_TYPE_MAP.get(param.get("paramType", "query"), "query"),
        "required": param.get("required", False),
    }

    if param.get("description"):
        converted["description"] = param["description"]

    if converted["in"] == "body":
        body_type = param.get("type", "object")
        if body_type == "file":
            # File upload params are formData in Swagger 2.0, not body
            converted["in"] = "formData"
            converted["type"] = "file"
        elif body_type in _PRIMITIVE_TYPES | {"array"}:
            converted["schema"] = _convert_type_to_schema(param)
        elif "[" in body_type or _is_java_class_name(body_type):
            converted["schema"] = _resolve_java_type(body_type)
        else:
            converted["schema"] = {"$ref": f"#/definitions/{body_type}"}
    else:
        # Non-body params use type directly
        p_type = param.get("type", "string")
        if p_type in ("string", "integer", "number", "boolean"):
            converted["type"] = p_type
        else:
            # Non-standard type for non-body param, treat as string
            converted["type"] = "string"
        if "format" in param:
            converted["format"] = param["format"]
        if "enum" in param:
            converted["enum"] = param["enum"]
        if param.get("allowMultiple"):
            converted["type"] = "array"
            converted["items"] = {"type": p_type}
            converted["collectionFormat"] = "multi"

    return converted


def _convert_operation(
    operation: dict[str, Any],
) -> dict[str, Any]:
    """Convert a Swagger 1.2 operation to Swagger 2.0."""
    converted: dict[str, Any] = {}

    if operation.get("nickname"):
        converted["operationId"] = operation["nickname"]

    if operation.get("summary"):
        converted["summary"] = operation["summary"]

    if operation.get("notes"):
        converted["description"] = operation["notes"]

    if operation.get("deprecated") == "true":
        converted["deprecated"] = True

    # Parameters
    params = operation.get("parameters", [])
    if params:
        converted["parameters"] = [_convert_parameter(p) for p in params]

    # Response
    return_type = operation.get("type", "void")
    if return_type == "void":
        converted["responses"] = {
            "200": {"description": "Success"},
        }
    elif return_type == "array":
        items = operation.get("items", {})
        schema: dict[str, Any] = {"type": "array"}
        if "$ref" in items:
            resolved = _convert_ref(items["$ref"])
            if isinstance(resolved, dict):
                schema["items"] = resolved
            else:
                schema["items"] = {"$ref": resolved}
        else:
            schema["items"] = {"type": items.get("type", "object")}
        converted["responses"] = {
            "200": {"description": "Success", "schema": schema},
        }
    elif return_type in _PRIMITIVE_TYPES:
        converted["responses"] = {
            "200": {"description": "Success", "schema": {"type": return_type}},
        }
    elif "[" in return_type or _is_java_class_name(return_type):
        # Java generic or class return type (e.g., List[X], com.netapp.foo.Bar)
        converted["responses"] = {
            "200": {"description": "Success", "schema": _resolve_java_type(return_type)},
        }
    else:
        converted["responses"] = {
            "200": {
                "description": "Success",
                "schema": {"$ref": f"#/definitions/{return_type}"},
            },
        }

    # Produces/consumes inherited from resource level, not set per-operation
    return converted


def _convert_model(model: dict[str, Any]) -> dict[str, Any]:
    """Convert a Swagger 1.2 model to a Swagger 2.0 definition."""
    converted: dict[str, Any] = {"type": "object"}

    if model.get("description"):
        converted["description"] = model["description"]

    if model.get("required"):
        converted["required"] = model["required"]

    props = model.get("properties", {})
    if props:
        converted_props: dict[str, Any] = {}
        for prop_name, prop_def in props.items():
            converted_props[prop_name] = _convert_type_to_schema(prop_def)
            if prop_def.get("description"):
                converted_props[prop_name]["description"] = prop_def["description"]
        converted["properties"] = converted_props

    return converted


def convert(spec: dict[str, Any]) -> dict[str, Any]:
    """Convert an assembled OCCM Swagger 1.2 spec to Swagger 2.0.

    Args:
        spec: The assembled OCCM spec from fetch_occm_spec.py.

    Returns:
        A Swagger 2.0 spec dict.
    """
    swagger2: dict[str, Any] = {
        "swagger": "2.0",
        "info": {
            "title": "OCCM API",
            "version": spec.get("apiVersion", "unknown"),
        },
        "basePath": "/occm/api",
        "schemes": ["http", "https"],
        "produces": ["application/json"],
        "consumes": ["application/json"],
        "paths": {},
        "definitions": {},
    }

    # Merge all resource paths and models
    for _resource_path, resource in spec.get("apis", {}).items():
        # Convert endpoints
        for api in resource.get("apis", []):
            path = api.get("path", "")
            if not path:
                continue

            # Swagger 2.0 paths use {param} style (same as 1.2)
            if path not in swagger2["paths"]:
                swagger2["paths"][path] = {}

            for operation in api.get("operations", []):
                method = operation.get("method", "GET").lower()
                swagger2["paths"][path][method] = _convert_operation(
                    operation,
                )

                # Add produces/consumes from resource if specified
                if resource.get("produces"):
                    swagger2["paths"][path][method].setdefault(
                        "produces",
                        resource["produces"],
                    )
                if resource.get("consumes"):
                    swagger2["paths"][path][method].setdefault(
                        "consumes",
                        resource["consumes"],
                    )

        # Convert models to definitions
        for model_name, model_def in resource.get("models", {}).items():
            if model_name not in swagger2["definitions"]:
                swagger2["definitions"][model_name] = _convert_model(model_def)

    # Post-process: fix "file" type refs and stub missing definitions
    _fix_file_types(swagger2)
    _stub_missing_definitions(swagger2)

    return swagger2


def _fix_file_types(spec: dict[str, Any]) -> None:
    """Replace #/definitions/file refs with {type: file} (Swagger 2.0 file upload).

    Also replaces refs to 'Object' with {type: object}.
    """
    inline_types = {"file": "file", "Object": "object"}

    def walk(obj: Any) -> None:
        if isinstance(obj, dict):
            ref = obj.get("$ref", "")
            if ref:
                def_name = ref.replace("#/definitions/", "")
                if def_name in inline_types:
                    del obj["$ref"]
                    obj["type"] = inline_types[def_name]
                    return
            for v in obj.values():
                walk(v)
        elif isinstance(obj, list):
            for v in obj:
                walk(v)

    walk(spec)


def _stub_missing_definitions(spec: dict[str, Any]) -> None:
    """Create stub definitions for any $ref targets that don't exist.

    The OCCM spec has dangling references to models that aren't defined
    in any resource (e.g., models only used internally by the Scala backend).
    We create empty object stubs so swagger2openapi doesn't choke.
    """
    definitions = spec.get("definitions", {})
    missing: set[str] = set()

    def find_refs(obj: Any) -> None:
        if isinstance(obj, dict):
            ref = obj.get("$ref", "")
            if ref.startswith("#/definitions/"):
                def_name = ref.replace("#/definitions/", "")
                if def_name not in definitions:
                    missing.add(def_name)
            for v in obj.values():
                find_refs(v)
        elif isinstance(obj, list):
            for v in obj:
                find_refs(v)

    find_refs(spec)

    for name in sorted(missing):
        definitions[name] = {
            "type": "object",
            "description": "Stub: referenced but not defined in the OCCM spec.",
        }

    if missing:
        print(f"  Stubbed {len(missing)} missing definitions: {', '.join(sorted(missing))}")


def main() -> None:
    """CLI entrypoint for standalone usage."""
    if len(sys.argv) < 2:
        print(
            "Usage: python swagger12_to_20.py <input.json> [output.json]",
            file=sys.stderr,
        )
        sys.exit(1)

    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2]) if len(sys.argv) > 2 else None

    with open(input_path) as f:
        spec = json.load(f)

    result = convert(spec)

    if output_path:
        output_path.write_text(json.dumps(result, indent=2) + "\n")
        print(f"Swagger 2.0 written to {output_path}")
    else:
        print(json.dumps(result, indent=2))

    paths = result.get("paths", {})
    definitions = result.get("definitions", {})
    print(f"Paths: {len(paths)}, Definitions: {len(definitions)}", file=sys.stderr)


if __name__ == "__main__":
    main()
