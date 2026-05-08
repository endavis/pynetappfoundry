"""Targeted unit tests for ``_ensure_path_params`` upstream-bug repairs."""

from __future__ import annotations

from tools.console_openapi.openapi.builder import _ensure_path_params


def test_synthesizes_missing_path_param() -> None:
    op: dict = {}
    _ensure_path_params("/folders/{folder_id}/folders", op)
    params = op["parameters"]
    assert len(params) == 1
    p = params[0]
    assert p["name"] == "folder_id"
    assert p["in"] == "path"
    assert p["required"] is True
    assert p["schema"] == {"type": "string"}
    assert p["x-synthesized"] is True


def test_demotes_stray_path_param_to_query() -> None:
    op: dict = {
        "parameters": [
            {
                "name": "stale_id",
                "in": "path",
                "required": True,
                "schema": {"type": "string"},
            }
        ]
    }
    _ensure_path_params("/things", op)
    params = op["parameters"]
    assert len(params) == 1
    p = params[0]
    assert p["in"] == "query"
    assert p["required"] is False
    assert p.get("x-demoted-from-path") is True


def test_leaves_correct_declarations_untouched() -> None:
    op: dict = {
        "parameters": [
            {
                "name": "folder_id",
                "in": "path",
                "required": True,
                "schema": {"type": "string"},
            }
        ]
    }
    _ensure_path_params("/folders/{folder_id}/folders", op)
    params = op["parameters"]
    assert len(params) == 1
    p = params[0]
    assert "x-synthesized" not in p
    assert "x-demoted-from-path" not in p
    assert p["required"] is True


def test_synthesize_and_demote_in_same_op() -> None:
    op: dict = {
        "parameters": [
            {
                "name": "ghost",
                "in": "path",
                "required": True,
                "schema": {"type": "string"},
            }
        ]
    }
    _ensure_path_params("/orgs/{org_id}/things", op)
    by_name = {p["name"]: p for p in op["parameters"]}
    assert by_name["ghost"]["in"] == "query"
    assert by_name["ghost"].get("x-demoted-from-path") is True
    assert by_name["org_id"]["in"] == "path"
    assert by_name["org_id"]["required"] is True
    assert by_name["org_id"].get("x-synthesized") is True


def test_no_template_no_params_is_noop() -> None:
    op: dict = {}
    _ensure_path_params("/health", op)
    assert "parameters" not in op
