"""Tests that APIWrapper.call_endpoint redacts Authorization in the debug log."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from pynetappfoundry.clients.openapi import APIWrapper

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
