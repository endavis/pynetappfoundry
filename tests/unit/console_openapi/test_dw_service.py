"""Tests for the ``dw`` (licenses and subscriptions) service (#1034).

Covers the widened token-usage wording, nullable type cells, the empty base
path, the ``drop_headers`` manifest overlay and the committed spec's ``dw`` entry.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest
from openapi_spec_validator import validate

from tools.console_openapi import cli as cli_module
from tools.console_openapi import client_codegen as cg
from tools.console_openapi.openapi.builder import _SERVICE_BASE_PATHS, build_spec
from tools.console_openapi.parser.endpoint import parse_endpoint

FIXTURES = Path(__file__).parent.parent.parent / "fixtures" / "console_openapi"
_PATH = "/license/account/{accountId}/subscriptions/preferred"

_TOKEN_TEMPLATE = (
    "= Op\n\n"
    "[.api-doc-operation .api-doc-operation-get]#GET# [.api-doc-code-block]#`/license/x`#\n\n"
    "Summary.\n\n{line}\n\n"
    "== Response\n\n```\nStatus: 200, Default Response\n```\n\n"
    "[cols=4*,options=header]\n|===\n|Name\n|Type\n|Required\n|Description\n\n"
    "|a\n|string\n|False\na|\n\n|===\n"
)


@pytest.mark.parametrize(
    ("line", "expected"),
    [
        ("*Token usage:* NetApp Console user token.", "user"),
        ("*Token usage:* NetApp Console service token.", "service"),
        ("*Token usage:* BlueXP user token.", "user"),
        ("*Token usage:* Either a NetApp Console user token or service token.", None),
        ("*Token usage:* NetApp Console service token with the following scopes: %scopes%.", None),
        ("*Token usage:* BlueXP service token with the following scopes: tenancy:internal.", None),
        ("*Token usage:* Both a BlueXP user token and service token. More.", None),
    ],
)
def test_token_usage_wording(line: str, expected: str | None) -> None:
    ep = parse_endpoint(
        _TOKEN_TEMPLATE.format(line=line), source_file="fixtures/t.adoc", service="dw"
    )
    assert ep is not None
    assert ep.token_usage == expected


def _dw_ep() -> Any:
    name = "dw_nullable_and_token.adoc"
    text = (FIXTURES / name).read_text(encoding="utf-8")
    ep = parse_endpoint(text, source_file=f"fixtures/{name}", service="dw")
    assert ep is not None
    return ep


def test_dw_fixture_builds_valid_spec() -> None:
    spec = build_spec([_dw_ep()], included_services=("dw",))
    validate(spec)
    op = spec["paths"][_PATH]["get"]
    assert "x-token-type" not in op
    assert "x-agent-id" not in {p["name"] for p in op.get("parameters", [])}
    ref = op["responses"]["200"]["content"]["application/json"]["schema"]["$ref"]
    assert ref == "#/components/schemas/dw.dw_nullable_and_token.Response200Body"
    body = spec["components"]["schemas"]["dw.dw_nullable_and_token.Response200Body"]
    assert body["properties"]["endDate"]["type"] == "integer"
    assert body["properties"]["endDate"]["nullable"] is True
    assert body["properties"]["term"]["nullable"] is True
    assert "nullable" not in body["properties"]["subscriptionId"]


def test_dw_response_has_no_required_list() -> None:
    spec = build_spec([_dw_ep()], included_services=("dw",))
    body = spec["components"]["schemas"]["dw.dw_nullable_and_token.Response200Body"]
    assert "required" not in body
    assert "x-documented-required" not in body


def test_dw_is_a_default_service_with_a_base_path() -> None:
    assert "dw" in cli_module.DEFAULT_SERVICES
    for service in cli_module.DEFAULT_SERVICES:
        assert service in _SERVICE_BASE_PATHS
    assert _SERVICE_BASE_PATHS["dw"] == ""


# --- drop_headers overlay -----------------------------------------------------


def _spec_with_header(required: bool) -> dict[str, Any]:
    return {
        "paths": {
            "/v1/any": {
                "get": {
                    "operationId": "any_get",
                    "summary": "Any",
                    "parameters": [
                        {
                            "name": "X-Service-Request-Id",
                            "in": "header",
                            "required": required,
                            "schema": {"type": "string"},
                        }
                    ],
                    "responses": {
                        "200": {"content": {"application/json": {"schema": {"type": "object"}}}}
                    },
                }
            }
        }
    }


def _entry(**extra: Any) -> dict[str, Any]:
    return {"operation_id": "any_get", "client": "console", "name": "any_get", **extra}


def _index(spec: dict[str, Any]) -> dict[str, tuple[str, str, dict[str, Any]]]:
    return cg._index_operations(spec)


def test_drop_headers_drops_an_optional_header(tmp_path: Path) -> None:
    spec = _spec_with_header(required=False)
    entry = _entry(drop_headers=["x-service-request-id"])
    op = cg.resolve_operation(entry, _index(spec), tmp_path)
    assert op.path_params == ()
    assert op.query_params == ()


def test_drop_headers_required_header_raises(tmp_path: Path) -> None:
    spec = _spec_with_header(required=True)
    with pytest.raises(cg.CodegenError, match="cannot drop required header"):
        cg.resolve_operation(_entry(drop_headers=["X-Service-Request-Id"]), _index(spec), tmp_path)


def test_drop_headers_absent_header_raises(tmp_path: Path) -> None:
    spec = _spec_with_header(required=False)
    spec["paths"]["/v1/any"]["get"]["parameters"] = []
    with pytest.raises(cg.CodegenError, match="unknown header parameters"):
        cg.resolve_operation(_entry(drop_headers=["X-Nope"]), _index(spec), tmp_path)


def test_header_without_overlay_still_raises(tmp_path: Path) -> None:
    spec = _spec_with_header(required=False)
    with pytest.raises(cg.CodegenError, match="unsupported header parameter"):
        cg.resolve_operation(_entry(), _index(spec), tmp_path)


def test_load_manifest_rejects_non_list_drop_headers(tmp_path: Path) -> None:
    path = tmp_path / "m.toml"
    path.write_text(
        '[[operation]]\noperation_id = "a"\nclient = "console"\nname = "a"\n'
        'drop_headers = "X-Service-Request-Id"\n',
        encoding="utf-8",
    )
    with pytest.raises(cg.CodegenError, match="drop_headers must be a list"):
        cg.load_manifest(path)


def test_real_manifest_resolves_preferred_subscriptions() -> None:
    index = _index(cg.load_spec())
    entry = next(e for e in cg.load_manifest() if e["name"] == "list_preferred_subscriptions")
    op = cg.resolve_operation(entry, index)
    assert op.token_type is None
    assert op.is_list is True
    assert op.path == _PATH
    assert op.response is not None
    assert op.response.cls == "Response200Body"
    assert [p.wire for p in op.query_params] == ["cloudProvider"]
