"""Assemble an OpenAPI 3.1 document from parsed endpoints."""

from __future__ import annotations

import re
from collections import defaultdict
from typing import Any

from tools.console_openapi.models import (
    Definition,
    FieldDef,
    ParsedEndpoint,
    ResponseBlock,
    TypeRef,
)


class BuildError(ValueError):
    """Raised when the assembled OpenAPI document violates an invariant."""


_AUTH_HEADER_NAMES = {"authorization"}
_DEFAULT_SERVERS: tuple[dict[str, str], ...] = (
    {
        "url": "https://api.bluexp.netapp.com",
        "description": "BlueXP / NetApp Console SaaS API (current)",
    },
    {
        "url": "https://cloudmanager.cloud.netapp.com",
        "description": "BlueXP / NetApp Console SaaS API (legacy hostname)",
    },
)
# Per-service server base URLs. Verified empirically against the live SaaS:
# v3 ``tenancy`` paths are served from the host root (e.g. ``/tenancy/account``);
# v4 ``tenancyv4`` paths are served under ``/v1/management`` (e.g.
# ``/v1/management/organizations``). Discovered from the Console UI's
# bootstrap configuration ``tenancyServiceInformation.urlV4``.
_SERVICE_SERVERS: dict[str, list[dict[str, str]]] = {
    "tenancy": [
        {
            "url": "https://api.bluexp.netapp.com",
            "description": "BlueXP IAM v3 (tenancy)",
        }
    ],
    "tenancyv4": [
        {
            "url": "https://api.bluexp.netapp.com/v1/management",
            "description": "BlueXP IAM v4 (tenancyv4)",
        }
    ],
}


def build_spec(
    endpoints: list[ParsedEndpoint],
    *,
    servers: list[dict[str, str]] | None = None,
    source_commit: str | None = None,
    source_repo: str = "https://github.com/NetAppDocs/console-automation",
    included_services: tuple[str, ...] = (),
    title: str = "NetApp BlueXP / Console SaaS API",
    version: str = "1.0.0-derived",
) -> dict[str, Any]:
    """Build the combined OpenAPI 3.1 document and return it as a Python dict."""
    components_schemas: dict[str, Any] = {}
    paths: dict[str, dict[str, Any]] = defaultdict(dict)
    operation_ids: set[str] = set()

    schema_keys_by_endpoint: list[dict[str, str]] = []

    for ep in endpoints:
        local_resolver = _build_local_resolver(ep, components_schemas)
        schema_keys_by_endpoint.append(local_resolver)

    for ep, resolver in zip(endpoints, schema_keys_by_endpoint, strict=True):
        op_obj = _build_operation(ep, resolver, operation_ids)
        _ensure_path_params(ep.path, op_obj)
        path_obj = paths[ep.path]
        verb = ep.method.lower()
        if verb in path_obj:
            existing = path_obj[verb]
            if existing == op_obj:
                continue
            raise BuildError(
                f"Conflicting operation for {ep.method} {ep.path}: "
                f"{existing.get('x-source-file')!r} vs {ep.source_file!r}"
            )
        path_obj[verb] = op_obj

    info: dict[str, Any] = {
        "title": title,
        "version": version,
        "description": _info_description(included_services),
        "x-included-source-folders": list(included_services),
        "x-source-repository": source_repo,
    }
    if source_commit is not None:
        info["x-source-commit"] = source_commit

    spec: dict[str, Any] = {
        "openapi": "3.1.0",
        "info": info,
        "servers": list(servers if servers is not None else _DEFAULT_SERVERS),
        "paths": dict(paths),
        "components": {
            "schemas": components_schemas,
            "securitySchemes": {
                "BearerAuth": {
                    "type": "http",
                    "scheme": "bearer",
                    "bearerFormat": "JWT",
                    "description": (
                        "BlueXP / NetApp Console JWT access token. Use a "
                        "user token or a service-account token depending on the "
                        "operation's x-token-type extension."
                    ),
                },
            },
        },
    }

    _enforce_invariants(spec)
    return spec


def _info_description(included_services: tuple[str, ...]) -> str:
    return (
        "Derived OpenAPI 3.1 specification for NetApp's BlueXP / Console SaaS API.\n\n"
        "**This spec is unofficial.** It is generated from the AsciiDoc sources "
        "published at https://github.com/NetAppDocs/console-automation. NetApp does "
        "not publish a machine-readable spec for this API surface.\n\n"
        f"Included service folders: {', '.join(included_services)}.\n\n"
        "Service folders containing prose tutorials with curl examples (e.g. ``cm/``) "
        "are intentionally excluded; they require a different parser and would need "
        "to be added separately."
    )


def _build_local_resolver(ep: ParsedEndpoint, components_schemas: dict[str, Any]) -> dict[str, str]:
    """Register every definition for ``ep`` and return ``{anchor: component_key}``."""
    resolver: dict[str, str] = {}
    file_stem = _file_stem(ep.source_file)
    for d in ep.definitions:
        key = _component_key(ep.service, file_stem, d.anchor)
        components_schemas[key] = _definition_schema(d, ep, resolver_inflight=resolver)
        resolver[d.anchor] = key
    # Pass two: now that all anchors of this file have been registered,
    # rebuild any schema that referenced its siblings to ensure $refs resolve.
    for d in ep.definitions:
        components_schemas[resolver[d.anchor]] = _definition_schema(
            d, ep, resolver_inflight=resolver
        )
    return resolver


def _definition_schema(
    d: Definition,
    ep: ParsedEndpoint,
    *,
    resolver_inflight: dict[str, str],
) -> dict[str, Any]:
    base: dict[str, Any] = {
        "x-source-file": ep.source_file,
        "x-source-anchor": d.anchor,
        "title": d.title,
    }
    if d.fallback_kind == "hash_string_string":
        return {
            **base,
            "type": "object",
            "additionalProperties": {"type": "string"},
            "description": d.description or "Hash mapping strings to string.",
        }
    if d.fallback_kind == "prose":
        return {
            **base,
            "type": "object",
            "description": d.description or "Definition without a structured table.",
        }
    schema: dict[str, Any] = {
        **base,
        "type": "object",
        "properties": {},
    }
    required: list[str] = []
    for f in d.fields:
        schema["properties"][f.name] = _field_schema(f, ep, resolver_inflight)
        if f.required:
            required.append(f.name)
    if required:
        schema["required"] = required
    return schema


def _field_schema(f: FieldDef, ep: ParsedEndpoint, resolver: dict[str, str]) -> dict[str, Any]:
    schema = _type_to_schema(f.type, ep, resolver)
    if f.description:
        schema = {**schema, "description": f.description}
    return schema


def _type_to_schema(t: TypeRef, ep: ParsedEndpoint, resolver: dict[str, str]) -> dict[str, Any]:
    if t.ref_anchor is not None:
        if t.ref_anchor in resolver:
            return {"$ref": f"#/components/schemas/{resolver[t.ref_anchor]}"}
        return {"type": "object", "x-unresolved-anchor": t.ref_anchor}
    if t.array_items is not None:
        items_schema = (
            _type_to_schema(t.array_items, ep, resolver) if t.array_items.raw != "" else {}
        )
        return {"type": "array", "items": items_schema}
    if t.one_of is not None:
        return {"oneOf": [_type_to_schema(m, ep, resolver) for m in t.one_of]}
    if t.additional_properties is not None:
        return {
            "type": "object",
            "additionalProperties": _type_to_schema(t.additional_properties, ep, resolver),
        }
    if t.primitive is not None:
        return {"type": t.primitive}
    return {"type": "object"}


def _ensure_path_params(path: str, op: dict[str, Any]) -> None:
    """Reconcile declared path parameters with the path template.

    Two upstream bugs are repaired here:
    * Missing declarations: when ``{name}`` appears in the path but no
      parameter is declared, synthesize a permissive ``string`` parameter
      tagged with ``x-synthesized: true``.
    * Stray declarations: when a ``in: path`` parameter is declared whose
      name does not appear in the template, demote it to ``in: query`` and
      tag with ``x-demoted-from-path: true`` rather than dropping it
      entirely (preserves the upstream-documented behavior in case a client
      was relying on it).
    """
    template_re = re.compile(r"\{([^}]+)\}")
    template_names = set(template_re.findall(path))
    params = list(op.get("parameters", []))
    declared_path = {p["name"] for p in params if p.get("in") == "path"}

    for p in params:
        if p.get("in") == "path" and p["name"] not in template_names:
            p["in"] = "query"
            p["required"] = False
            p["x-demoted-from-path"] = True

    missing = template_names - declared_path
    for name in missing:
        params.append(
            {
                "name": name,
                "in": "path",
                "required": True,
                "schema": {"type": "string"},
                "description": (
                    "Synthesized from the path template; the upstream "
                    "documentation does not declare this parameter."
                ),
                "x-synthesized": True,
            }
        )
    if params:
        op["parameters"] = params


def _build_operation(
    ep: ParsedEndpoint, resolver: dict[str, str], operation_ids: set[str]
) -> dict[str, Any]:
    op: dict[str, Any] = {
        "operationId": _allocate_operation_id(ep, operation_ids),
        "summary": ep.summary or ep.title,
        "tags": [ep.service],
        "x-source-file": ep.source_file,
    }
    if ep.description:
        op["description"] = ep.description

    parameters: list[dict[str, Any]] = []
    seen_keys: set[tuple[str, str]] = set()
    for p in ep.parameters:
        if p.location == "header" and p.name.lower() in _AUTH_HEADER_NAMES:
            continue
        location = (p.location or "query").lower()
        key = (p.name, location)
        if key in seen_keys:
            continue
        seen_keys.add(key)
        parameters.append(_parameter_object(p, ep, resolver))
    if parameters:
        op["parameters"] = parameters

    if ep.request_body_fields or ep.request_body_example is not None or ep.request_body_example_raw:
        op["requestBody"] = _request_body(ep, resolver)

    op["responses"] = _responses(ep, resolver)

    op["security"] = [{"BearerAuth": []}]
    if ep.token_usage is not None:
        op["x-token-type"] = ep.token_usage

    service_servers = _SERVICE_SERVERS.get(ep.service)
    if service_servers:
        op["servers"] = service_servers

    return op


def _allocate_operation_id(ep: ParsedEndpoint, used: set[str]) -> str:
    base = _operation_id_base(ep)
    candidate = base
    suffix = 2
    while candidate in used:
        candidate = f"{base}_{suffix}"
        suffix += 1
    used.add(candidate)
    return candidate


def _operation_id_base(ep: ParsedEndpoint) -> str:
    method = ep.method.lower()
    path_part = re.sub(r"\{([^}]+)\}", r"by_\1", ep.path)
    path_part = re.sub(r"[^A-Za-z0-9]+", "_", path_part).strip("_")
    return f"{ep.service}_{method}_{path_part}"


def _parameter_object(p: FieldDef, ep: ParsedEndpoint, resolver: dict[str, str]) -> dict[str, Any]:
    location = p.location or "query"
    if location not in {"query", "path", "header", "cookie"}:
        location = "query"
    obj: dict[str, Any] = {
        "name": p.name,
        "in": location,
        "schema": _type_to_schema(p.type, ep, resolver),
    }
    if location == "path" or p.required:
        obj["required"] = True
    if p.description:
        obj["description"] = p.description
    return obj


def _request_body(ep: ParsedEndpoint, resolver: dict[str, str]) -> dict[str, Any]:
    schema: dict[str, Any] = {"type": "object", "properties": {}}
    required: list[str] = []
    for f in ep.request_body_fields:
        schema["properties"][f.name] = _field_schema(f, ep, resolver)
        if f.required:
            required.append(f.name)
    if required:
        schema["required"] = required
    media: dict[str, Any] = {"schema": schema}
    if ep.request_body_example is not None:
        media["example"] = ep.request_body_example
    elif ep.request_body_example_raw is not None:
        media["x-example-raw"] = ep.request_body_example_raw
    body: dict[str, Any] = {
        "required": any(f.required for f in ep.request_body_fields),
        "content": {"application/json": media},
    }
    return body


def _responses(ep: ParsedEndpoint, resolver: dict[str, str]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for r in ep.responses:
        out[str(r.status)] = _response_object(r, ep, resolver)
    if not out:
        out["default"] = {"description": "Unspecified response."}
    return out


def _response_object(
    r: ResponseBlock, ep: ParsedEndpoint, resolver: dict[str, str]
) -> dict[str, Any]:
    obj: dict[str, Any] = {"description": r.description or "Response."}
    if r.status == 204:
        return obj
    has_body = bool(r.fields) or r.example is not None or r.example_raw is not None
    if not has_body:
        return obj
    schema: dict[str, Any] = {"type": "object", "properties": {}}
    required: list[str] = []
    for f in r.fields:
        schema["properties"][f.name] = _field_schema(f, ep, resolver)
        if f.required:
            required.append(f.name)
    if required:
        schema["required"] = required
    media: dict[str, Any] = {"schema": schema}
    if r.example is not None:
        media["example"] = r.example
    elif r.example_raw is not None:
        media["x-example-raw"] = r.example_raw
    obj["content"] = {"application/json": media}
    return obj


def _component_key(service: str, file_stem: str, anchor: str) -> str:
    parts = [service, file_stem, anchor]
    sanitized = ".".join(_sanitize_segment(p) for p in parts)
    return sanitized


def _sanitize_segment(s: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9_-]+", "_", s).strip("_")
    return cleaned or "x"


def _file_stem(path: str) -> str:
    stem = path.rsplit("/", 1)[-1]
    if stem.endswith(".adoc"):
        stem = stem[: -len(".adoc")]
    return stem


def _enforce_invariants(spec: dict[str, Any]) -> None:
    """Verify post-build invariants. Raises :class:`BuildError` on violation."""
    schemas = spec["components"]["schemas"]
    paths = spec["paths"]
    valid_refs = {f"#/components/schemas/{k}" for k in schemas}

    unresolved: list[str] = []

    def _walk(obj: Any, where: str) -> None:
        if isinstance(obj, dict):
            ref = obj.get("$ref")
            if isinstance(ref, str) and ref.startswith("#/") and ref not in valid_refs:
                unresolved.append(f"{where}: {ref}")
            for k, v in obj.items():
                _walk(v, f"{where}.{k}")
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                _walk(item, f"{where}[{i}]")

    _walk(paths, "paths")
    _walk(schemas, "components.schemas")
    if unresolved:
        raise BuildError(f"Unresolved $ref(s): {unresolved[:5]} (total {len(unresolved)})")

    seen_op_ids: set[str] = set()
    template_re = re.compile(r"\{([^}]+)\}")
    for path, path_obj in paths.items():
        templated = set(template_re.findall(path))
        for verb, op in path_obj.items():
            op_id = op.get("operationId")
            if op_id in seen_op_ids:
                raise BuildError(f"Duplicate operationId: {op_id}")
            seen_op_ids.add(op_id)
            params = op.get("parameters") or []
            path_params_present = {p["name"] for p in params if p.get("in") == "path"}
            missing = templated - path_params_present
            if missing:
                raise BuildError(
                    f"{verb.upper()} {path}: path template variables without parameter "
                    f"definitions: {sorted(missing)}"
                )
            for p in params:
                if p.get("in") == "header" and p.get("name", "").lower() in _AUTH_HEADER_NAMES:
                    raise BuildError(
                        f"{verb.upper()} {path}: 'Authorization' header parameter leaked"
                    )
                if p.get("in") == "path" and not p.get("required"):
                    raise BuildError(
                        f"{verb.upper()} {path}: path parameter '{p.get('name')}' is not required"
                    )
