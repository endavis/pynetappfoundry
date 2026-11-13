"""Tests for the Console client operation generator (#735)."""

from __future__ import annotations

import copy
from pathlib import Path
from typing import Any

import pytest

from tools.console_openapi import client_codegen as cg

_AGENT_ID = {
    "name": "x-agent-id",
    "in": "header",
    "schema": {"type": "string"},
    "x-synthesized": True,
}


def _op(op_id: str, **extra: Any) -> dict[str, Any]:
    return {
        "operationId": op_id,
        "summary": f"Summary of {op_id}",
        "responses": {"200": {"content": {"application/json": {"schema": {"type": "object"}}}}},
        **extra,
    }


def _ref(name: str) -> dict[str, Any]:
    return {"$ref": f"#/components/schemas/{name}"}


def _spec() -> dict[str, Any]:
    ok_ref = {
        "200": {"content": {"application/json": {"schema": _ref("cvo.get-thing.ResponseBody")}}}
    }
    return {
        "paths": {
            "/v1/things/{thing_id}": {
                "get": _op(
                    "user_get",
                    **{"x-token-type": "user"},
                    parameters=[
                        {"name": "thing_id", "in": "path", "schema": {"type": "string"}},
                        {"name": "orderBy", "in": "query", "schema": {"type": "string"}},
                        {"name": "continue", "in": "query", "schema": {"type": "string"}},
                    ],
                ),
                "delete": {
                    "operationId": "thing_delete",
                    "responses": {"204": {"description": "gone"}},
                    "parameters": [
                        {"name": "thing_id", "in": "path", "schema": {"type": "string"}}
                    ],
                },
            },
            "/v1/service": {"get": _op("service_get", **{"x-token-type": "service"})},
            "/v1/any": {"get": _op("any_get")},
            "/agent/things": {
                "get": _op(
                    "agent_list",
                    parameters=[
                        {"name": "fields", "in": "query", "schema": _ref("cvo.x.Expands")},
                        _AGENT_ID,
                    ],
                    responses=ok_ref,
                ),
                "post": _op(
                    "agent_create",
                    parameters=[_AGENT_ID],
                    requestBody={
                        "content": {
                            "application/json": {"schema": _ref("cvo.post-thing.RequestBody")}
                        }
                    },
                    responses={
                        "201": {
                            "content": {
                                "application/json": {"schema": _ref("cvo.post-thing.ResponseBody")}
                            }
                        }
                    },
                ),
                "put": _op("agent_put"),
            },
        }
    }


@pytest.fixture
def models_root(tmp_path: Path) -> Path:
    root = tmp_path / "models"
    (root / "cvo").mkdir(parents=True)
    (root / "cvo" / "post_thing.py").write_text(
        "class RequestBody(BaseModel):\n    pass\n\nclass ResponseBody(BaseModel):\n    pass\n",
        encoding="utf-8",
    )
    (root / "cvo" / "get_thing.py").write_text(
        "class ResponseBody(BaseModel):\n    pass\n", encoding="utf-8"
    )
    return root


def _entry(
    op_id: str, client: str = "console", name: str | None = None, **extra: Any
) -> dict[str, Any]:
    return {"operation_id": op_id, "client": client, "name": name or op_id, **extra}


def _render(
    entries: list[dict[str, Any]], models_root: Path, spec: dict[str, Any] | None = None
) -> dict[str, str]:
    return cg.render_all(entries, spec or _spec(), models_root)


def test_user_token_type_literal(models_root: Path) -> None:
    src = _render([_entry("user_get", name="get_it", only_query=["orderBy"])], models_root)
    assert '_dispatch("user", **kwargs)' in src["tenancy_ops.py"]


def test_service_token_type_literal(models_root: Path) -> None:
    assert (
        '_dispatch("service", **kwargs)'
        in _render([_entry("service_get")], models_root)["tenancy_ops.py"]
    )


def test_untagged_token_type_is_none(models_root: Path) -> None:
    assert (
        "_dispatch(None, **kwargs)" in _render([_entry("any_get")], models_root)["tenancy_ops.py"]
    )


def test_agent_operation_with_token_type_raises(models_root: Path) -> None:
    spec = _spec()
    spec["paths"]["/agent/things"]["get"]["x-token-type"] = "user"
    with pytest.raises(cg.CodegenError, match="one credential"):
        _render(
            [_entry("agent_list", "agent", query={"fields": {"style": "csv"}})], models_root, spec
        )


def test_synthesized_agent_id_header_is_dropped(models_root: Path) -> None:
    src = _render(
        [
            _entry(
                "agent_list",
                "agent",
                "list_things",
                response="list",
                query={"fields": {"style": "csv"}},
            )
        ],
        models_root,
    )["agent_ops.py"]
    assert "x-agent-id" not in src
    assert "x_agent_id" not in src


def test_other_header_parameter_raises(models_root: Path) -> None:
    spec = _spec()
    spec["paths"]["/v1/any"]["get"]["parameters"] = [
        {"name": "X-Other", "in": "header", "schema": {"type": "string"}}
    ]
    with pytest.raises(cg.CodegenError, match="header parameter"):
        _render([_entry("any_get")], models_root, spec)


def test_path_params_quoted_and_snake_cased(models_root: Path) -> None:
    src = _render([_entry("user_get", only_query=["orderBy"])], models_root)["tenancy_ops.py"]
    assert 'kwargs["path_params"] = {"thing_id": quote(thing_id, safe="")}' in src
    assert "order_by: str | None = None" in src
    assert '"orderBy": order_by' in src


def test_query_keyword_gets_suffix(models_root: Path) -> None:
    src = _render([_entry("user_get")], models_root)["tenancy_ops.py"]
    assert "continue_: str | None = None" in src
    assert '"continue": continue_' in src


def test_query_params_are_keyword_only(models_root: Path) -> None:
    src = _render([_entry("user_get", only_query=["orderBy"])], models_root)["tenancy_ops.py"]
    assert "thing_id: str, *, order_by" in src


def test_ref_query_param_without_overlay_raises(models_root: Path) -> None:
    with pytest.raises(cg.CodegenError, match="not a plain string"):
        _render([_entry("agent_list", "agent")], models_root)


def test_unknown_overlay_style_raises(models_root: Path) -> None:
    with pytest.raises(cg.CodegenError, match="unknown style"):
        _render([_entry("agent_list", "agent", query={"fields": {"style": "pipe"}})], models_root)


def test_overlay_for_unknown_query_param_raises(models_root: Path) -> None:
    with pytest.raises(cg.CodegenError, match="unknown query parameters"):
        _render([_entry("any_get", query={"nope": {"style": "csv"}})], models_root)


def test_csv_overlay_and_list_response(models_root: Path) -> None:
    src = _render(
        [
            _entry(
                "agent_list",
                "agent",
                "list_things",
                response="list",
                query={"fields": {"style": "csv"}},
            )
        ],
        models_root,
    )["agent_ops.py"]
    assert "fields: str | Sequence[str] | None = None" in src
    assert "csv_param(fields)" in src
    assert "-> list[get_thing.ResponseBody]" in src
    assert "expect_list" in src


def test_inline_response_is_a_dict(models_root: Path) -> None:
    src = _render([_entry("any_get", name="get_any")], models_root)["tenancy_ops.py"]
    assert "-> dict[str, Any]" in src
    assert 'return expect_object(response, "get_any")' in src


def test_bodiless_response_returns_none(models_root: Path) -> None:
    src = _render([_entry("thing_delete", name="del_thing")], models_root)["tenancy_ops.py"]
    assert "-> None" in src
    assert "response =" not in src


def test_mutations_default_to_no_retry(models_root: Path) -> None:
    src = _render(
        [
            _entry("agent_create", "agent", "create_thing"),
            _entry("agent_put", "agent", "put_thing"),
        ],
        models_root,
    )["agent_ops.py"]
    assert src.count('kwargs["retry_config"] = RetryConfig(enabled=False)') == 2
    assert 'kwargs["body"] = body.model_dump(exclude_none=True)' in src


def test_get_keeps_wrapper_retry(models_root: Path) -> None:
    assert "RetryConfig" not in _render([_entry("any_get")], models_root)["tenancy_ops.py"]


def test_retry_true_removes_no_retry(models_root: Path) -> None:
    src = _render([_entry("agent_put", "agent", "put_thing", retry=True)], models_root)[
        "agent_ops.py"
    ]
    assert "RetryConfig" not in src


def test_missing_model_module_raises(models_root: Path) -> None:
    (models_root / "cvo" / "post_thing.py").unlink()
    with pytest.raises(cg.CodegenError, match="does not exist"):
        _render([_entry("agent_create", "agent")], models_root)


def test_missing_model_class_raises(models_root: Path) -> None:
    (models_root / "cvo" / "get_thing.py").write_text("X = 1\n", encoding="utf-8")
    with pytest.raises(cg.CodegenError, match="does not define"):
        _render(
            [_entry("agent_list", "agent", response="list", query={"fields": {"style": "csv"}})],
            models_root,
        )


def test_unknown_operation_id_raises(models_root: Path) -> None:
    with pytest.raises(cg.CodegenError, match="not in the spec"):
        _render([_entry("nope")], models_root)


def test_duplicate_name_raises(models_root: Path) -> None:
    with pytest.raises(cg.CodegenError, match="Duplicate"):
        _render([_entry("any_get", name="same"), _entry("service_get", name="same")], models_root)


def test_load_manifest_rejects_unknown_key(tmp_path: Path) -> None:
    path = tmp_path / "m.toml"
    path.write_text(
        '[[operation]]\noperation_id = "a"\nclient = "console"\nname = "a"\nbogus = 1\n',
        encoding="utf-8",
    )
    with pytest.raises(cg.CodegenError, match="Unknown manifest keys"):
        cg.load_manifest(path)


def test_load_manifest_rejects_unknown_client(tmp_path: Path) -> None:
    path = tmp_path / "m.toml"
    path.write_text(
        '[[operation]]\noperation_id = "a"\nclient = "x"\nname = "a"\n', encoding="utf-8"
    )
    with pytest.raises(cg.CodegenError, match="Unknown client"):
        cg.load_manifest(path)


def test_render_is_deterministic(models_root: Path) -> None:
    entries = [_entry("user_get", only_query=["orderBy"]), _entry("any_get", name="get_any")]
    spec = _spec()
    assert _render(entries, models_root, spec) == _render(
        copy.deepcopy(entries), models_root, copy.deepcopy(spec)
    )


def test_generate_writes_files(tmp_path: Path, models_root: Path) -> None:
    import yaml

    spec = tmp_path / "spec.yaml"
    spec.write_text(yaml.safe_dump(_spec()), encoding="utf-8")
    manifest = tmp_path / "m.toml"
    manifest.write_text(
        '[[operation]]\noperation_id = "any_get"\nclient = "console"\nname = "get_any"\n',
        encoding="utf-8",
    )
    out = tmp_path / "out"

    written = cg.generate(out, spec, manifest, models_root)

    assert {p.name for p in written} == {"__init__.py", "tenancy_ops.py"}
    assert "class ConsoleTenancyOps" in (out / "tenancy_ops.py").read_text(encoding="utf-8")


def test_real_manifest_resolves_against_committed_spec() -> None:
    """Drift guard: every manifest entry still resolves against the spec and models tree."""
    files = cg.render_all(cg.load_manifest(), cg.load_spec())
    assert set(files) == {"__init__.py", "agent_ops.py", "tenancy_ops.py"}
    assert "def create_onprem_working_environment" in files["agent_ops.py"]
    assert ") -> dict[str, Any]:" not in files["tenancy_ops.py"]


def test_real_manifest_types_onprem_working_environments_as_list() -> None:
    """The list shape comes from the spec, not a manifest overlay (#1021)."""
    manifest = cg.load_manifest()
    entry = next(e for e in manifest if e["name"] == "list_onprem_working_environments")
    assert "response" not in entry
    src = cg.render_all(manifest, cg.load_spec())["agent_ops.py"]
    assert "-> list[get_onprem_working_environments.ResponseBody]:" in src


def _array_spec(items: dict[str, Any]) -> dict[str, Any]:
    spec = _spec()
    spec["paths"]["/agent/things"]["get"]["responses"] = {
        "200": {"content": {"application/json": {"schema": {"type": "array", "items": items}}}}
    }
    return spec


def _array_entry(**extra: Any) -> dict[str, Any]:
    return _entry("agent_list", "agent", "list_things", query={"fields": {"style": "csv"}}, **extra)


def test_spec_array_of_refs_renders_typed_list(models_root: Path) -> None:
    spec = _array_spec(_ref("cvo.get-thing.ResponseBody"))
    src = _render([_array_entry()], models_root, spec)["agent_ops.py"]
    assert "-> list[get_thing.ResponseBody]:" in src
    assert "expect_list" in src


def test_spec_array_with_inline_items_renders_any_list(models_root: Path) -> None:
    spec = _array_spec({"type": "string"})
    src = _render([_array_entry()], models_root, spec)["agent_ops.py"]
    assert "-> list[Any]:" in src
    assert 'expect_list(response, "list_things")' in src


def test_redundant_list_overlay_on_spec_array_raises(models_root: Path) -> None:
    spec = _array_spec(_ref("cvo.get-thing.ResponseBody"))
    with pytest.raises(cg.CodegenError, match="redundant"):
        _render([_array_entry(response="list")], models_root, spec)


def test_object_overlay_on_spec_array_raises(models_root: Path) -> None:
    spec = _array_spec(_ref("cvo.get-thing.ResponseBody"))
    with pytest.raises(cg.CodegenError, match="contradicts"):
        _render([_array_entry(response="object")], models_root, spec)


def _status_spec(response_ref: str, request_ref: str | None = None) -> dict[str, Any]:
    op = _op(
        "thing_get",
        responses={
            "200": {"content": {"application/json": {"schema": _ref(response_ref)}}},
        },
    )
    if request_ref:
        op["requestBody"] = {"content": {"application/json": {"schema": _ref(request_ref)}}}
    return {"paths": {"/v1/things": {"post": op}}}


@pytest.fixture
def tenancy_models(models_root: Path) -> Path:
    (models_root / "tenancyv4").mkdir()
    (models_root / "tenancyv4" / "get_thing.py").write_text(
        "class Response200Body(BaseModel):\n    pass\n\nclass RequestBody(BaseModel):\n    pass\n",
        encoding="utf-8",
    )
    return models_root


def test_numeric_status_response_body_is_typed(tenancy_models: Path) -> None:
    spec = _status_spec("tenancyv4.get-thing.Response200Body")
    src = _render([_entry("thing_get")], tenancy_models, spec)["tenancy_ops.py"]
    assert "-> get_thing.Response200Body" in src
    assert "get_thing.Response200Body.model_validate(expect_object(" in src


@pytest.mark.parametrize("cls", ["Response200Bodyx", "Foo", "Response20Body"])
def test_unrecognized_response_class_raises(tenancy_models: Path, cls: str) -> None:
    spec = _status_spec(f"tenancyv4.get-thing.{cls}")
    with pytest.raises(cg.CodegenError, match="Cannot map"):
        _render([_entry("thing_get")], tenancy_models, spec)


def test_request_ref_to_numeric_status_class_raises(tenancy_models: Path) -> None:
    ref = "tenancyv4.get-thing.Response200Body"
    spec = _status_spec(ref, ref)
    with pytest.raises(cg.CodegenError, match="Cannot map"):
        _render([_entry("thing_get")], tenancy_models, spec)
