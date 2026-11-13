"""Tests for the cvo array-response list and its wrapping in the spec (#1021)."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import pytest
import yaml
from openapi_spec_validator import validate

from tools.console_openapi.array_responses import (
    ARRAY_RESPONSES_PATH,
    array_operations,
    load_array_responses,
)
from tools.console_openapi.openapi.builder import BuildError, build_spec
from tools.console_openapi.parser.endpoint import parse_endpoint

_ROOT = Path(__file__).resolve().parents[3]
_SPEC_PATH = _ROOT / "tools/console_openapi/generated/console_openapi.yaml"
_SWAGGER_PATH = _ROOT / "docs/example-config/apis/occm/openapi3.json"
_FIXTURES = Path(__file__).parent.parent.parent / "fixtures" / "console_openapi"
_ABOUT = ("POST", "/occm/api/occm/system/about")
_RESPONSE_REF = "#/components/schemas/cvo.cvo_status_default.ResponseBody"
_LIVE = {"/occm/api/onprem/working-environments", "/occm/api/tenants"}
# Swagger arrays whose generated operation has no documented response body to wrap.
_BODILESS = {
    "cvo_get_occm_api_aws_ha_metadata_key_pairs",
    "cvo_get_occm_api_vsa_metadata_key_pairs",
    "cvo_get_occm_api_replication_metadata_snapshot_labels_by_workingEnvironmentId_by_svmName_by_volumeName",
}


def _write(tmp_path: Path, text: str) -> Path:
    path = tmp_path / "array_responses.toml"
    path.write_text(text, encoding="utf-8")
    return path


def _cvo_ep() -> Any:
    text = (_FIXTURES / "cvo_status_default.adoc").read_text(encoding="utf-8")
    ep = parse_endpoint(text, source_file="fixtures/cvo_status_default.adoc", service="cvo")
    assert ep is not None
    return ep


# --- A. loader ---------------------------------------------------------------


def test_loader_parses_and_filters_services(tmp_path: Path) -> None:
    path = _write(
        tmp_path, '[cvo]\n"GET /occm/api/a" = "live"\n"GET /occm/api/b/{id}" = "swagger"\n'
    )
    data = load_array_responses(path)
    assert data == {"cvo": {"GET /occm/api/a": "live", "GET /occm/api/b/{id}": "swagger"}}
    assert array_operations(data, ("cvo",)) == {("GET", "/occm/api/a"), ("GET", "/occm/api/b/{id}")}
    assert array_operations(data, ("tenancy",)) == frozenset()


@pytest.mark.parametrize(
    "text",
    [
        '[nope]\n"GET /x" = "live"\n',
        '[cvo]\n"FETCH /occm/api/a" = "live"\n',
        '[cvo]\n"GET /v1/x" = "live"\n',
        '[cvo]\n"GET /occm/api/a" = "maybe"\n',
    ],
)
def test_loader_rejects_bad_entries(tmp_path: Path, text: str) -> None:
    with pytest.raises(BuildError):
        load_array_responses(_write(tmp_path, text))


# --- B. builder --------------------------------------------------------------


def test_builder_wraps_listed_response() -> None:
    spec = build_spec([_cvo_ep()], included_services=("cvo",), array_responses={_ABOUT})
    op = spec["paths"][_ABOUT[1]]["post"]
    assert op["responses"]["default"]["content"]["application/json"]["schema"] == {
        "type": "array",
        "items": {"$ref": _RESPONSE_REF},
    }
    assert op["requestBody"]["content"]["application/json"]["schema"] == {
        "$ref": "#/components/schemas/cvo.cvo_status_default.RequestBody"
    }
    component = spec["components"]["schemas"]["cvo.cvo_status_default.ResponseBody"]
    assert "x-documented-required" in component
    assert "required" not in component
    validate(spec)


def test_builder_unknown_operation_raises() -> None:
    with pytest.raises(BuildError, match="unknown operation"):
        build_spec(
            [_cvo_ep()],
            included_services=("cvo",),
            array_responses={("GET", "/occm/api/nope")},
        )


def test_builder_operation_without_body_raises() -> None:
    text = (_FIXTURES / "delete_204_with_error.adoc").read_text(encoding="utf-8")
    ep = parse_endpoint(text, source_file="fixtures/delete_204_with_error.adoc", service="fixture")
    assert ep is not None
    with pytest.raises(BuildError, match="no hoisted body"):
        build_spec(
            [ep],
            included_services=("fixture",),
            array_responses={("DELETE", "/folders/{folder_id}")},
        )


def test_builder_default_matches_no_array_responses() -> None:
    plain = build_spec([_cvo_ep()], included_services=("cvo",))
    empty = build_spec([_cvo_ep()], included_services=("cvo",), array_responses=())
    assert plain == empty


# --- C. consistency with the committed artifacts ------------------------------


@pytest.fixture(scope="module")
def cvo_list() -> dict[str, str]:
    return load_array_responses(ARRAY_RESPONSES_PATH)["cvo"]


@pytest.fixture(scope="module")
def committed_spec() -> dict[str, Any]:
    with _SPEC_PATH.open(encoding="utf-8") as f:
        spec: dict[str, Any] = yaml.safe_load(f)
    return spec


@pytest.fixture(scope="module")
def swagger() -> dict[str, Any]:
    data: dict[str, Any] = json.loads(_SWAGGER_PATH.read_text(encoding="utf-8"))
    return data


def _norm(path: str) -> str:
    return re.sub(r"\{[^}]+\}", "{}", path)


def _success_schema(op: dict[str, Any]) -> Any:
    responses = op.get("responses", {})
    codes = sorted(c for c in responses if str(c).startswith("2")) or (
        ["default"] if "default" in responses else []
    )
    if not codes:
        return None
    media = responses[codes[0]].get("content", {}).get("application/json", {})
    return media.get("schema")


def _cvo_gets(spec: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        path: item["get"]
        for path, item in spec["paths"].items()
        if "get" in item and "cvo" in item["get"].get("tags", [])
    }


def test_spec_arrays_equal_the_list(
    cvo_list: dict[str, str], committed_spec: dict[str, Any]
) -> None:
    arrays: set[str] = set()
    for path, item in committed_spec["paths"].items():
        for method, op in item.items():
            if method not in {"get", "post", "put", "patch", "delete"}:
                continue
            if "cvo" not in op.get("tags", []):
                continue
            schema = _success_schema(op)
            if isinstance(schema, dict) and schema.get("type") == "array":
                arrays.add(f"{method.upper()} {path}")
                assert schema["items"]["$ref"].endswith(".ResponseBody"), path
    assert arrays == set(cvo_list), (
        f"missing {sorted(set(cvo_list) - arrays)}, extra {sorted(arrays - set(cvo_list))}"
    )


def test_list_matches_swagger_arrays(
    cvo_list: dict[str, str], committed_spec: dict[str, Any], swagger: dict[str, Any]
) -> None:
    swagger_arrays = {
        _norm(path)
        for path, item in swagger["paths"].items()
        if "get" in item
        and item["get"]["responses"]
        .get("200", {})
        .get("content", {})
        .get("application/json", {})
        .get("schema", {})
        .get("type")
        == "array"
    }
    with_body: set[str] = set()
    bodiless: set[str] = set()
    for path, op in _cvo_gets(committed_spec).items():
        if _norm(path.removeprefix("/occm/api")) not in swagger_arrays:
            continue
        schema = _success_schema(op)
        if isinstance(schema, dict) and ("$ref" in schema or schema.get("type") == "array"):
            with_body.add(f"GET {path}")
        else:
            bodiless.add(op["operationId"])
    assert with_body == set(cvo_list), (
        f"missing {sorted(with_body - set(cvo_list))}, extra {sorted(set(cvo_list) - with_body)}"
    )
    assert bodiless == _BODILESS


def test_live_entries_are_the_confirmed_ones(cvo_list: dict[str, str]) -> None:
    assert {k.removeprefix("GET ") for k, v in cvo_list.items() if v == "live"} == _LIVE
