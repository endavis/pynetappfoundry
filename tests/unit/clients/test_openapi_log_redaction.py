"""Tests that APIWrapper.call_endpoint redacts Authorization in the debug log."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from pynetappfoundry.clients.openapi import APIWrapper, ResponseValidationError
from pynetappfoundry.core.models import ValidationConfig

TOKEN = "tok-redaction-check"


@pytest.fixture
def wrapper(tmp_path: Path) -> APIWrapper:
    spec = {
        "swagger": "2.0",
        "basePath": "/api/v1",
        "paths": {"/users": {"get": {"responses": {"200": {"description": "ok"}}}}},
    }
    spec_path = tmp_path / "spec.json"
    spec_path.write_text(json.dumps(spec))
    return APIWrapper(
        api_json_file=str(spec_path),
        base_url="https://api.example.test",
        auth_header={"Authorization": f"Bearer {TOKEN}"},
        timeout=5.0,
    )


def _ok_response() -> MagicMock:
    resp = MagicMock()
    resp.status_code = 200
    resp.json.return_value = {}
    return resp


def test_session_authorization_not_logged(
    wrapper: APIWrapper, caplog: pytest.LogCaptureFixture
) -> None:
    with (
        patch.object(wrapper.session, "request", return_value=_ok_response()),
        caplog.at_level(logging.DEBUG),
    ):
        wrapper.call_endpoint("/users", "GET")
    assert TOKEN not in caplog.text
    assert "***" in caplog.text


def test_additional_authorization_not_logged_and_still_sent(
    wrapper: APIWrapper, caplog: pytest.LogCaptureFixture
) -> None:
    with (
        patch.object(wrapper.session, "request", return_value=_ok_response()) as mock_request,
        caplog.at_level(logging.DEBUG),
    ):
        wrapper.call_endpoint(
            "/users",
            "GET",
            additional_headers={"authorization": "Bearer extra-tok", "X-Custom": "kept"},
        )
    assert "extra-tok" not in caplog.text
    assert "kept" in caplog.text
    sent_headers = mock_request.call_args.kwargs["headers"]
    assert sent_headers["authorization"] == "Bearer extra-tok"


# --- #1003: DII key masking, request-body errors and write-response logging ---------------

SENTINEL = "SENTINEL-PW-1003"
DII_KEY = "dii-key-redaction-check"


@pytest.fixture
def things_wrapper(tmp_path: Path) -> APIWrapper:
    body_schema = {
        "content": {
            "application/json": {
                "schema": {
                    "type": "object",
                    "properties": {
                        "password": {"type": "integer"},
                        "mode": {"type": "string", "enum": ["a", "b"]},
                        "code": {"type": "string", "maxLength": 3},
                    },
                }
            }
        }
    }
    ok = {"responses": {"200": {"description": "ok"}}}
    spec = {
        "swagger": "2.0",
        "basePath": "/api/v1",
        "paths": {
            "/things": {"get": ok, "post": {"requestBody": body_schema, **ok}},
            "/things/{id}": {
                "patch": ok,
                "put": ok,
                "delete": ok,
                "parameters": [{"name": "id", "in": "path", "required": True}],
            },
        },
    }
    spec_path = tmp_path / "things.json"
    spec_path.write_text(json.dumps(spec))
    return APIWrapper(
        api_json_file=str(spec_path),
        base_url="https://api.example.test",
        auth_header={"X-CloudInsights-ApiKey": DII_KEY},
        timeout=5.0,
    )


def _sentinel_response() -> MagicMock:
    resp = MagicMock()
    resp.status_code = 200
    resp.json.return_value = {"password": SENTINEL}
    resp.text = json.dumps({"password": SENTINEL})
    resp.content = resp.text.encode()
    return resp


def test_dii_api_key_header_masked_and_still_sent(
    things_wrapper: APIWrapper, caplog: pytest.LogCaptureFixture
) -> None:
    caplog.set_level(logging.DEBUG)
    with patch.object(things_wrapper.session, "request", return_value=_ok_response()) as req:
        things_wrapper.call_endpoint("/things", "GET")
    assert DII_KEY not in caplog.text
    assert "***" in caplog.text
    assert req.call_args.kwargs["headers"]["X-CloudInsights-ApiKey"] == DII_KEY


@pytest.mark.parametrize(
    ("body", "expected"),
    [
        ({"password": SENTINEL}, "'type' failed at password"),
        ({"mode": SENTINEL}, "'enum' failed at mode"),
        ({"code": SENTINEL}, "'maxLength' failed at code"),
    ],
)
def test_validate_body_error_names_field_not_value(
    things_wrapper: APIWrapper,
    caplog: pytest.LogCaptureFixture,
    body: dict[str, Any],
    expected: str,
) -> None:
    caplog.set_level(logging.DEBUG)
    assert things_wrapper.validate_body("/things", "POST", body) is False
    assert SENTINEL not in caplog.text
    assert expected in caplog.text


def test_strict_validate_response_error_omits_value(things_wrapper: APIWrapper) -> None:
    schema = {
        "type": "object",
        "properties": {"password": {"type": "integer"}},
    }
    with (
        patch.object(things_wrapper, "_get_response_schema", return_value=schema),
        pytest.raises(ResponseValidationError) as exc,
    ):
        things_wrapper.validate_response(
            "/things",
            "POST",
            200,
            {"password": SENTINEL},
            validation_config=ValidationConfig(enabled=True, strict=True),
        )
    assert SENTINEL not in str(exc.value)
    assert SENTINEL not in exc.value.validation_error
    assert "'type' failed at password" in exc.value.validation_error


def test_non_strict_validate_response_warning_omits_value(
    things_wrapper: APIWrapper, caplog: pytest.LogCaptureFixture
) -> None:
    schema = {"type": "object", "properties": {"password": {"type": "integer"}}}
    caplog.set_level(logging.DEBUG)
    with patch.object(things_wrapper, "_get_response_schema", return_value=schema):
        ok = things_wrapper.validate_response(
            "/things",
            "POST",
            200,
            {"password": SENTINEL},
            validation_config=ValidationConfig(enabled=True, strict=False),
        )
    assert ok is False
    assert SENTINEL not in caplog.text
    assert "'type' failed at password" in caplog.text


@pytest.mark.parametrize(
    ("method", "path", "path_params"),
    [
        ("POST", "/things", None),
        ("PATCH", "/things/{id}", {"id": "1"}),
        ("PUT", "/things/{id}", {"id": "1"}),
        ("DELETE", "/things/{id}", {"id": "1"}),
    ],
)
def test_write_response_body_not_logged(
    things_wrapper: APIWrapper,
    caplog: pytest.LogCaptureFixture,
    method: str,
    path: str,
    path_params: dict[str, str] | None,
) -> None:
    caplog.set_level(logging.DEBUG)
    with patch.object(things_wrapper.session, "request", return_value=_sentinel_response()):
        things_wrapper.call_endpoint(path, method, path_params=path_params)
    assert SENTINEL not in caplog.text
    assert f"bytes (body not logged for {method})" in caplog.text


def test_get_response_body_still_logged(
    things_wrapper: APIWrapper, caplog: pytest.LogCaptureFixture
) -> None:
    caplog.set_level(logging.DEBUG)
    with patch.object(things_wrapper.session, "request", return_value=_sentinel_response()):
        things_wrapper.call_endpoint("/things", "GET")
    assert "Response Text:" in caplog.text
    assert SENTINEL in caplog.text
