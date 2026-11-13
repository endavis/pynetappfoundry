"""End-to-end tests against the committed AsciiDoc fixtures."""

from __future__ import annotations

from pathlib import Path
from typing import Any

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


def _delete_folder_endpoint(service: str) -> Any:
    text, src = _load("delete_204_with_error.adoc")
    ep = parse_endpoint(text, source_file=src, service="fixture")
    assert ep is not None
    assert ep.path == "/folders/{folder_id}"
    return ep.model_copy(update={"service": service})


def test_tenancyv4_endpoint_is_keyed_by_full_path() -> None:
    ep = _delete_folder_endpoint("tenancyv4")
    spec = build_spec([ep], included_services=("tenancyv4",))
    assert list(spec["paths"]) == ["/v1/management/folders/{folder_id}"]
    op = spec["paths"]["/v1/management/folders/{folder_id}"]["delete"]
    assert "v1_management" in op["operationId"]
    assert op["servers"][0]["url"] == "https://api.bluexp.netapp.com"


def test_tenancy_endpoint_keeps_documented_key() -> None:
    ep = _delete_folder_endpoint("tenancy")
    spec = build_spec([ep], included_services=("tenancy",))
    assert list(spec["paths"]) == ["/folders/{folder_id}"]
    op = spec["paths"]["/folders/{folder_id}"]["delete"]
    assert op["servers"][0]["url"] == "https://api.bluexp.netapp.com"


def test_same_relative_path_in_two_services_does_not_collide() -> None:
    v3 = _delete_folder_endpoint("tenancy")
    v4 = _delete_folder_endpoint("tenancyv4")
    spec = build_spec([v3, v4], included_services=("tenancy", "tenancyv4"))
    assert set(spec["paths"]) == {"/folders/{folder_id}", "/v1/management/folders/{folder_id}"}


def test_conflict_message_shows_full_path() -> None:
    ep = _delete_folder_endpoint("tenancyv4")
    other = ep.model_copy(update={"source_file": "fixtures/conflict.adoc", "summary": "other"})
    with pytest.raises(BuildError, match="/v1/management/folders/"):
        build_spec([ep, other], included_services=("tenancyv4",))


def test_info_records_service_base_paths() -> None:
    ep = _delete_folder_endpoint("tenancyv4")
    spec = build_spec([ep], included_services=("tenancy", "tenancyv4"))
    assert spec["info"]["x-service-base-paths"] == {"tenancy": "", "tenancyv4": "/v1/management"}


def test_unmapped_service_gets_no_prefix() -> None:
    ep = _delete_folder_endpoint("fixture")
    spec = build_spec([ep], included_services=("fixture",))
    assert list(spec["paths"]) == ["/folders/{folder_id}"]
    assert spec["info"]["x-service-base-paths"] == {"fixture": ""}


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


# --- cvo: Status: Default, body hoisting, x-agent-id, base path (#1009) -----


def _cvo_ep(service: str = "cvo") -> Any:
    text, src = _load("cvo_status_default.adoc")
    ep = parse_endpoint(text, source_file=src, service=service)
    assert ep is not None
    return ep


def test_status_default_parses_as_default() -> None:
    ep = _cvo_ep()
    assert [r.status for r in ep.responses] == ["default"]
    assert ep.responses[0].description == "Error"


def test_numeric_status_is_unchanged() -> None:
    text, src = _load("happy_post_with_definitions.adoc")
    ep = parse_endpoint(text, source_file=src, service="fixture")
    assert ep is not None
    assert ep.responses[0].status == 200


def test_cvo_operation_key_and_default_response() -> None:
    spec = build_spec([_cvo_ep()], included_services=("cvo",))
    op = spec["paths"]["/occm/api/occm/system/about"]["post"]
    assert list(op["responses"]) == ["default"]
    assert spec["info"]["x-service-base-paths"]["cvo"] == "/occm/api"


def test_cvo_bodies_are_hoisted_into_components() -> None:
    spec = build_spec([_cvo_ep()], included_services=("cvo",))
    op = spec["paths"]["/occm/api/occm/system/about"]["post"]
    schemas = spec["components"]["schemas"]
    resp = op["responses"]["default"]["content"]["application/json"]["schema"]
    req = op["requestBody"]["content"]["application/json"]["schema"]
    assert resp == {"$ref": "#/components/schemas/cvo.cvo_status_default.ResponseBody"}
    assert req == {"$ref": "#/components/schemas/cvo.cvo_status_default.RequestBody"}
    body = schemas["cvo.cvo_status_default.ResponseBody"]
    assert "agentId" in body["properties"]
    assert body["x-source-file"] == "fixtures/cvo_status_default.adoc"
    inner = body["properties"]["serverTimeZone"]["$ref"].rsplit("/", 1)[-1]
    assert inner in schemas


def test_non_cvo_service_bodies_stay_inline() -> None:
    spec = build_spec([_cvo_ep("fixture")], included_services=("fixture",))
    op = spec["paths"]["/occm/system/about"]["post"]
    schema = op["responses"]["default"]["content"]["application/json"]["schema"]
    assert "properties" in schema
    assert not any(k.endswith(".ResponseBody") for k in spec["components"]["schemas"])


def test_body_without_properties_is_not_hoisted() -> None:
    from tools.console_openapi.openapi.builder import _hoist

    schemas: dict[str, Any] = {}
    schema = {"type": "object", "properties": {}}
    assert _hoist(_cvo_ep(), "ResponseBody", schema, schemas) is schema
    assert schemas == {}


def test_hoist_name_collision_raises_build_error() -> None:
    from tools.console_openapi.openapi.builder import _hoist

    schemas: dict[str, Any] = {"cvo.cvo_status_default.ResponseBody": {}}
    with pytest.raises(BuildError, match="exists"):
        _hoist(_cvo_ep(), "ResponseBody", {"properties": {"a": {"type": "string"}}}, schemas)


def test_cvo_operation_gets_one_required_agent_id_header() -> None:
    spec = build_spec([_cvo_ep()], included_services=("cvo",))
    op = spec["paths"]["/occm/api/occm/system/about"]["post"]
    headers = [p for p in op["parameters"] if p["name"] == "x-agent-id"]
    assert len(headers) == 1
    assert headers[0]["in"] == "header"
    assert headers[0]["required"] is True
    assert headers[0]["x-synthesized"] is True


def test_agent_id_header_absent_on_other_services() -> None:
    spec = build_spec([_cvo_ep("fixture")], included_services=("fixture",))
    op = spec["paths"]["/occm/system/about"]["post"]
    assert "x-agent-id" not in {p["name"] for p in op.get("parameters", [])}


def test_agent_id_header_not_duplicated_when_documented() -> None:
    from tools.console_openapi.models import FieldDef, TypeRef

    ep = _cvo_ep()
    declared = FieldDef(
        name="X-Agent-Id",
        type=TypeRef(raw="string", primitive="string"),
        required=True,
        description="",
        location="header",
    )
    ep = ep.model_copy(update={"parameters": (*ep.parameters, declared)})
    spec = build_spec([ep], included_services=("cvo",))
    op = spec["paths"]["/occm/api/occm/system/about"]["post"]
    assert [p["name"] for p in op["parameters"] if p["name"].lower() == "x-agent-id"] == [
        "X-Agent-Id"
    ]


def test_cvo_and_tenancyv4_users_paths_coexist() -> None:
    cvo = _cvo_ep().model_copy(update={"path": "/users", "method": "GET"})
    v4 = _cvo_ep("tenancyv4").model_copy(update={"path": "/users", "method": "GET"})
    spec = build_spec([cvo, v4], included_services=("tenancyv4", "cvo"))
    assert "/occm/api/users" in spec["paths"]
    assert "/v1/management/users" in spec["paths"]


def test_cvo_fixture_spec_validates() -> None:
    from openapi_spec_validator import validate

    validate(build_spec([_cvo_ep()], included_services=("cvo",)))


# --- cvo: response fields are optional (#1018) ------------------------------


def _required_ep(service: str = "cvo") -> Any:
    text, src = _load("cvo_response_required.adoc")
    ep = parse_endpoint(text, source_file=src, service=service)
    assert ep is not None
    return ep


def _schema_by_suffix(spec: dict[str, Any], suffix: str) -> dict[str, Any]:
    matches = [v for k, v in spec["components"]["schemas"].items() if k.endswith(suffix)]
    assert len(matches) == 1, suffix
    schema: dict[str, Any] = matches[0]
    return schema


def test_cvo_response_body_required_is_renamed() -> None:
    spec = build_spec([_cvo_ep()], included_services=("cvo",))
    body = spec["components"]["schemas"]["cvo.cvo_status_default.ResponseBody"]
    assert "required" not in body
    assert body["x-documented-required"] == ["serverTimeZone", "version"]


def test_cvo_loosening_follows_refs_and_spares_request_only() -> None:
    spec = build_spec([_required_ep()], included_services=("cvo",))
    for suffix in ("Response200Body", "Outer", "Inner", "Shared"):
        schema = _schema_by_suffix(spec, f".{suffix}")
        assert "required" not in schema, suffix
        assert schema["x-documented-required"], suffix
    for suffix in ("RequestBody", "ReqOnly"):
        schema = _schema_by_suffix(spec, f".{suffix}")
        assert schema["required"], suffix
        assert "x-documented-required" not in schema, suffix


def test_non_cvo_service_keeps_required() -> None:
    spec = build_spec([_required_ep("fixture")], included_services=("fixture",))
    for schema in spec["components"]["schemas"].values():
        assert "x-documented-required" not in schema
    assert _schema_by_suffix(spec, "Outer")["required"] == ["inner", "shared"]


def test_cvo_response_required_fixture_spec_validates() -> None:
    from openapi_spec_validator import validate

    validate(build_spec([_required_ep()], included_services=("cvo",)))


# --- tenancy / tenancyv4: hoisted and loosened (#1027) ----------------------


@pytest.mark.parametrize("service", ["tenancy", "tenancyv4"])
def test_tenancy_bodies_are_hoisted(service: str) -> None:
    spec = build_spec([_required_ep(service)], included_services=(service,))
    schemas = spec["components"]["schemas"]
    stem = "cvo_response_required"
    assert f"{service}.{stem}.RequestBody" in schemas
    assert f"{service}.{stem}.Response200Body" in schemas


@pytest.mark.parametrize("service", ["tenancy", "tenancyv4"])
def test_tenancy_responses_are_loosened_and_requests_keep_required(service: str) -> None:
    spec = build_spec([_required_ep(service)], included_services=(service,))
    for suffix in ("Response200Body", "Outer", "Inner", "Shared"):
        schema = _schema_by_suffix(spec, f".{suffix}")
        assert "required" not in schema, suffix
        assert schema["x-documented-required"], suffix
    for suffix in ("RequestBody", "ReqOnly"):
        schema = _schema_by_suffix(spec, f".{suffix}")
        assert schema["required"], suffix
        assert "x-documented-required" not in schema, suffix
