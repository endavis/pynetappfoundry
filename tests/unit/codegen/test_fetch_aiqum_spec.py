"""Tests for the AIQUM spec fetcher's UI-session login flow (no network)."""

from __future__ import annotations

import http.cookiejar
import io
import json
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

import pytest

from tools.scripts import fetch_aiqum_spec as mod

SPEC_YAML = b"swagger: '2.0'\ninfo:\n  title: AIQUM\n  version: '9.18'\npaths:\n  /a: {}\n"


class FakeResponse:
    def __init__(self, body: bytes = b"", status: int = 200) -> None:
        self._body = body
        self.status = status
        self.headers = {"Content-Type": "application/yaml"}

    def read(self) -> bytes:
        return self._body


class FakeOpener:
    """Stands in for OpenerDirector: records requests, serves canned responses."""

    def __init__(
        self,
        *,
        login_error: urllib.error.HTTPError | None = None,
        spec_error: urllib.error.HTTPError | None = None,
        cookie: str | None = "tok123",
    ) -> None:
        self.jar = http.cookiejar.CookieJar()
        self.handlers: list[Any] = [urllib.request.HTTPCookieProcessor(self.jar)]
        self.requests: list[urllib.request.Request] = []
        self.login_error = login_error
        self.spec_error = spec_error
        self.cookie = cookie

    def _set_cookie(self, value: str) -> None:
        self.jar.set_cookie(
            http.cookiejar.Cookie(
                0, "UM-CSRF", value, None, False, "h", False, False, "/", True,
                False, None, False, None, None, {},
            )
        )  # fmt: skip

    def open(self, req: urllib.request.Request) -> FakeResponse:
        self.requests.append(req)
        path = urllib.parse.urlparse(req.full_url).path
        if path == "/login":
            if self.login_error:
                raise self.login_error
            if self.cookie is not None:
                self._set_cookie(self.cookie)
            return FakeResponse()
        if path == "/docs/api/v2.yaml":
            if self.spec_error:
                raise self.spec_error
            return FakeResponse(SPEC_YAML)
        return FakeResponse()

    def paths(self) -> list[str]:
        return [urllib.parse.urlparse(r.full_url).path for r in self.requests]


def _http_error(code: int) -> urllib.error.HTTPError:
    return urllib.error.HTTPError("https://h/x", code, "err", {}, io.BytesIO(b""))  # type: ignore[arg-type]


def _patch(monkeypatch: pytest.MonkeyPatch, opener: FakeOpener) -> None:
    monkeypatch.setattr(mod, "_build_opener", lambda no_verify: opener)


def test_login_is_form_post_with_headers(monkeypatch: pytest.MonkeyPatch) -> None:
    opener = FakeOpener()
    _patch(monkeypatch, opener)
    mod.fetch_spec("h", "admin", "p@ss word")
    login = opener.requests[0]
    assert login.get_method() == "POST"
    assert login.full_url == "https://h/login"
    assert login.data == b"username=admin&password=p%40ss+word"
    assert login.get_header("Content-type") == "application/x-www-form-urlencoded"
    assert login.get_header("Um-request-csrf-token") == "true"


def test_spec_get_carries_csrf_cookie(monkeypatch: pytest.MonkeyPatch) -> None:
    opener = FakeOpener(cookie="tok123")
    _patch(monkeypatch, opener)
    mod.fetch_spec("h", "u", "p")
    spec_req = opener.requests[1]
    assert spec_req.full_url == "https://h/docs/api/v2.yaml"
    assert spec_req.get_header("Um-csrf-token") == "tok123"
    assert spec_req.get_header("Accept") == "application/yaml, application/json"
    assert spec_req.get_header("Authorization") is None


def test_spec_get_without_cookie_omits_csrf_header(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    opener = FakeOpener(cookie=None)
    _patch(monkeypatch, opener)
    mod.fetch_spec("h", "u", "p")
    assert opener.requests[1].get_header("Um-csrf-token") is None


def test_yaml_parsed_and_logout_called(monkeypatch: pytest.MonkeyPatch) -> None:
    opener = FakeOpener()
    _patch(monkeypatch, opener)
    spec = mod.fetch_spec("h", "u", "p")
    assert spec["swagger"] == "2.0"
    assert spec["info"]["version"] == "9.18"
    assert opener.paths() == ["/login", "/docs/api/v2.yaml", "/logout"]


def test_timestamps_stay_strings_and_spec_is_json_serializable(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    body = (
        b"swagger: '2.0'\n"
        b"paths:\n  /a: {}\n"
        b"definitions:\n  D:\n    example: 2021-01-01T00:00:00Z\n    day: 2021-01-01\n"
    )

    class _Opener(FakeOpener):
        def open(self, req: urllib.request.Request) -> FakeResponse:
            if urllib.parse.urlparse(req.full_url).path == "/docs/api/v2.yaml":
                self.requests.append(req)
                return FakeResponse(body)
            return super().open(req)

    _patch(monkeypatch, _Opener())
    spec = mod.fetch_spec("h", "u", "p")
    assert spec["definitions"]["D"]["example"] == "2021-01-01T00:00:00Z"
    assert spec["definitions"]["D"]["day"] == "2021-01-01"
    assert json.dumps(spec)


def test_logout_called_when_spec_get_fails(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    opener = FakeOpener(spec_error=_http_error(500))
    _patch(monkeypatch, opener)
    with pytest.raises(SystemExit):
        mod.fetch_spec("h", "u", "p")
    assert opener.paths()[-1] == "/logout"
    assert "HTTP 500" in capsys.readouterr().err


def test_login_failure_exits_without_password(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    opener = FakeOpener(login_error=_http_error(401))
    _patch(monkeypatch, opener)
    with pytest.raises(SystemExit) as exc:
        mod.fetch_spec("h", "admin", "s3cretPW")
    assert exc.value.code == 1
    err = capsys.readouterr().err
    assert "401" in err
    assert "s3cretPW" not in err
    assert opener.paths() == ["/login"]


def test_build_opener_has_cookie_processor() -> None:
    opener = mod._build_opener(no_verify=False)
    handlers: list[Any] = getattr(opener, "handlers", [])
    assert any(isinstance(h, urllib.request.HTTPCookieProcessor) for h in handlers)
