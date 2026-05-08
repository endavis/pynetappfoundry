"""End-to-end tests against the committed AsciiDoc fixtures."""

from __future__ import annotations

from pathlib import Path

import pytest

from tools.console_openapi.openapi.builder import BuildError, build_spec
from tools.console_openapi.parser.endpoint import parse_endpoint

FIXTURES = Path(__file__).parent.parent.parent / "fixtures" / "console_openapi"


def _load(name: str) -> tuple[str, str]:
    path = FIXTURES / name
    return path.read_text(encoding="utf-8"), f"fixtures/{name}"


def test_overview_returns_none() -> None:
    text, src = _load("overview_no_operation.adoc")
    assert parse_endpoint(text, source_file=src, service="fixture") is None


def test_happy_post_parses() -> None:
    text, src = _load("happy_post_with_definitions.adoc")
    ep = parse_endpoint(text, source_file=src, service="fixture")
    assert ep is not None
    assert ep.method == "POST"
    assert ep.path == "/tenancy/resource/discover"
    assert ep.token_usage == "user"
    assert any(p.name == "authorization" for p in ep.parameters)
    assert {f.name for f in ep.request_body_fields} >= {
        "workspacePublicId",
        "agentId",
        "metadata",
    }
    assert ep.responses[0].status == 200
    assert any(d.anchor == "metadata" for d in ep.definitions)


def test_happy_post_builds_valid_spec() -> None:
    text, src = _load("happy_post_with_definitions.adoc")
    ep = parse_endpoint(text, source_file=src, service="fixture")
    assert ep is not None
    spec = build_spec([ep], included_services=("fixture",))

    op = spec["paths"]["/tenancy/resource/discover"]["post"]
    # Authorization header is suppressed in favor of BearerAuth security
    assert op["security"] == [{"BearerAuth": []}]
    param_names = {p["name"] for p in op.get("parameters", [])}
    assert "authorization" not in {n.lower() for n in param_names}
    # Request body schema $ref points to the registered metadata schema
    body_props = op["requestBody"]["content"]["application/json"]["schema"]["properties"]
    assert "$ref" in body_props["metadata"]
    assert op["x-token-type"] == "user"


def test_204_response_omits_content() -> None:
    text, src = _load("delete_204_with_error.adoc")
    ep = parse_endpoint(text, source_file=src, service="fixture")
    assert ep is not None
    spec = build_spec([ep], included_services=("fixture",))
    responses = spec["paths"]["/folders/{folder_id}"]["delete"]["responses"]
    assert "content" not in responses["204"]
    assert "content" in responses["400"]


def test_path_param_required_invariant() -> None:
    text, src = _load("delete_204_with_error.adoc")
    ep = parse_endpoint(text, source_file=src, service="fixture")
    assert ep is not None
    spec = build_spec([ep], included_services=("fixture",))
    op = spec["paths"]["/folders/{folder_id}"]["delete"]
    folder_param = next(p for p in op["parameters"] if p["name"] == "folder_id")
    assert folder_param["in"] == "path"
    assert folder_param["required"] is True


def test_anyof_and_primitives() -> None:
    text, src = _load("anyof_and_primitives.adoc")
    ep = parse_endpoint(text, source_file=src, service="fixture")
    assert ep is not None
    spec = build_spec([ep], included_services=("fixture",))
    schema = spec["paths"]["/permissions"]["get"]["responses"]["200"]["content"][
        "application/json"
    ]["schema"]
    items = schema["properties"]["items"]
    assert items["type"] == "array"
    assert "oneOf" in items["items"]
    assert schema["properties"]["empty"] == {"type": "array", "items": {}}
    assert schema["properties"]["count"]["type"] == "integer"
    assert schema["properties"]["active"]["type"] == "boolean"
    assert schema["properties"]["score"]["type"] == "number"


def test_prose_and_hash_definitions() -> None:
    text, src = _load("prose_and_hash_definitions.adoc")
    ep = parse_endpoint(text, source_file=src, service="fixture")
    assert ep is not None
    spec = build_spec([ep], included_services=("fixture",))
    schemas = spec["components"]["schemas"]
    tags_key = next(k for k in schemas if k.endswith(".tags"))
    target_key = next(k for k in schemas if k.endswith(".targetSchema"))
    assert schemas[tags_key]["type"] == "object"
    assert schemas[tags_key]["additionalProperties"] == {"type": "string"}
    assert schemas[target_key]["type"] == "object"
    assert "Reference to an external schema" in schemas[target_key]["description"]


def test_duplicate_operation_conflict_raises() -> None:
    text, src = _load("delete_204_with_error.adoc")
    ep = parse_endpoint(text, source_file=src, service="fixture")
    assert ep is not None
    # Manufacture a conflicting endpoint that has the same verb+path but
    # different parameters; the builder must fail.
    from tools.console_openapi.models import FieldDef, ParsedEndpoint, TypeRef

    other = ParsedEndpoint(
        source_file="fixtures/conflict.adoc",
        service="fixture",
        permalink="x",
        summary="x",
        title="x",
        description="x",
        method="DELETE",
        path="/folders/{folder_id}",
        parameters=(
            FieldDef(
                name="folder_id",
                type=TypeRef(primitive="string"),
                required=True,
                description="",
                location="path",
            ),
            FieldDef(
                name="extra",
                type=TypeRef(primitive="boolean"),
                required=False,
                description="",
                location="query",
            ),
        ),
    )
    with pytest.raises(BuildError):
        build_spec([ep, other], included_services=("fixture",))


def test_spec_is_openapi_validatable() -> None:
    pytest.importorskip("openapi_spec_validator")
    from openapi_spec_validator import validate

    eps = []
    for name in (
        "happy_post_with_definitions.adoc",
        "delete_204_with_error.adoc",
        "anyof_and_primitives.adoc",
        "prose_and_hash_definitions.adoc",
    ):
        text, src = _load(name)
        ep = parse_endpoint(text, source_file=src, service="fixture")
        assert ep is not None
        eps.append(ep)
    spec = build_spec(eps, included_services=("fixture",))
    validate(spec)
