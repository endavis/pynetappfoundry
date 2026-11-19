"""Shared fakes for the Digital Advisor client tests (placeholders only)."""

from __future__ import annotations

import base64
import json
from collections.abc import Callable
from typing import Any
from unittest.mock import MagicMock

import requests


def make_jwt(exp: float | None, extra: dict[str, Any] | None = None) -> str:
    """Build a dummy JWT with the given ``exp`` and no signature."""

    def enc(obj: dict[str, Any]) -> str:
        return base64.urlsafe_b64encode(json.dumps(obj).encode()).decode().rstrip("=")

    claims: dict[str, Any] = dict(extra or {})
    if exp is not None:
        claims["exp"] = exp
    return f"{enc({'alg': 'none'})}.{enc(claims)}.sig"


def response(
    status: int = 200, body: Any = None, headers: dict[str, str] | None = None
) -> requests.Response:
    """Build a canned ``requests.Response``."""
    resp = requests.Response()
    resp.status_code = status
    resp.headers.update(headers or {})
    if body is not None:
        resp._content = json.dumps(body).encode()
    else:
        resp._content = b"not json"
    return resp


def session_with(*outcomes: requests.Response | BaseException) -> MagicMock:
    """A session whose ``post`` returns or raises the outcomes in order."""
    session = MagicMock(spec=requests.Session)
    session.post.side_effect = list(outcomes)
    return session


class FakeClock:
    """A manual clock with a recording sleep."""

    def __init__(self, now: float = 1000.0) -> None:
        self.now = now
        self.sleeps: list[float] = []

    def __call__(self) -> float:
        return self.now

    def sleep(self, seconds: float) -> None:
        self.sleeps.append(seconds)
        self.now += seconds


def gql(data: dict[str, Any]) -> requests.Response:
    return response(200, {"data": data})


def unauthenticated() -> requests.Response:
    return response(200, {"errors": [{"message": "no", "extensions": {"code": "UNAUTHENTICATED"}}]})


SleepFn = Callable[[float], None]
