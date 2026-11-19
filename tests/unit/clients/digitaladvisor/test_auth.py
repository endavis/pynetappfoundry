"""Tests for Digital Advisor token handling (#1051)."""

from __future__ import annotations

import logging
from unittest.mock import MagicMock

import pytest
import requests

from pynetappfoundry.clients.digitaladvisor.auth import (
    DigitalAdvisorAuthError,
    RefreshingTokenProvider,
    StaticTokenProvider,
    TokenPersistError,
    jwt_expiry,
)
from tests.unit.clients.digitaladvisor.helpers import FakeClock, make_jwt, response, session_with

URL = "https://token.example.test/v1/tokens/accessToken"


def _provider(
    session: MagicMock,
    clock: FakeClock,
    *,
    access: str | None = None,
    persist: MagicMock | None = None,
) -> RefreshingTokenProvider:
    return RefreshingTokenProvider(
        refresh_token="placeholder-refresh-old",
        access_token=access,
        token_url=URL,
        timeout=5.0,
        persist=persist,
        session=session,
        clock=clock,
    )


def _new_pair(clock: FakeClock, n: int = 1) -> tuple[str, str]:
    return make_jwt(clock.now + 3600, {"sub": f"placeholder-{n}"}), f"placeholder-refresh-{n}"


def test_jwt_expiry_reads_exp() -> None:
    assert jwt_expiry(make_jwt(1234.0)) == 1234.0


@pytest.mark.parametrize(
    "token", ["not-a-jwt", "a.!!!.c", "a.bm90LWpzb24.c", make_jwt(None), "a.WzFd.c"]
)
def test_jwt_expiry_returns_none_on_bad_input(token: str) -> None:
    assert jwt_expiry(token) is None


def test_jwt_expiry_never_logs(caplog: pytest.LogCaptureFixture) -> None:
    token = make_jwt(5.0, {"email": "placeholder@example.test"})
    with caplog.at_level(logging.DEBUG):
        jwt_expiry(token)
        jwt_expiry("a.!!!.c")
    assert caplog.text == ""


def test_static_provider() -> None:
    p = StaticTokenProvider("placeholder-pat")
    assert p.get_token() == "placeholder-pat"
    assert p.refreshable is False
    p.invalidate("placeholder-pat")
    assert p.get_token() == "placeholder-pat"
    assert "placeholder-pat" not in repr(p)


def test_refreshes_when_no_access_token() -> None:
    clock = FakeClock()
    access, refresh = _new_pair(clock)
    session = session_with(response(200, {"access_token": access, "refresh_token": refresh}))
    provider = _provider(session, clock)

    assert provider.get_token() == access
    assert session.post.call_args.kwargs["json"] == {"refresh_token": "placeholder-refresh-old"}
    assert session.post.call_args.args[0] == URL


def test_reuses_valid_access_token_without_post() -> None:
    clock = FakeClock()
    stored = make_jwt(clock.now + 3600)
    session = session_with()
    assert _provider(session, clock, access=stored).get_token() == stored
    session.post.assert_not_called()


def test_refreshes_inside_the_skew_window() -> None:
    clock = FakeClock()
    stored = make_jwt(clock.now + 30)  # less than the 60 s skew away
    access, refresh = _new_pair(clock)
    session = session_with(response(200, {"access_token": access, "refresh_token": refresh}))
    assert _provider(session, clock, access=stored).get_token() == access


def test_undecodable_expiry_is_used_until_rejected() -> None:
    clock = FakeClock()
    session = session_with()
    assert _provider(session, clock, access="opaque-token").get_token() == "opaque-token"
    session.post.assert_not_called()


def test_rotated_refresh_token_used_next_and_persisted_once_each() -> None:
    clock = FakeClock()
    a1, r1 = _new_pair(clock, 1)
    a2, r2 = _new_pair(clock, 2)
    session = session_with(
        response(200, {"access_token": a1, "refresh_token": r1}),
        response(200, {"access_token": a2, "refresh_token": r2}),
    )
    persist = MagicMock()
    provider = _provider(session, clock, persist=persist)

    assert provider.get_token() == a1
    provider.invalidate(a1)
    assert provider.get_token() == a2

    assert session.post.call_args_list[1].kwargs["json"] == {"refresh_token": r1}
    assert [c.args for c in persist.call_args_list] == [(a1, r1), (a2, r2)]


def test_persist_failure_is_logged_without_values(caplog: pytest.LogCaptureFixture) -> None:
    clock = FakeClock()
    access, refresh = _new_pair(clock)
    session = session_with(response(200, {"access_token": access, "refresh_token": refresh}))
    persist = MagicMock(side_effect=RuntimeError(f"secret {access} {refresh}"))
    provider = _provider(session, clock, persist=persist)

    with caplog.at_level(logging.DEBUG):
        assert provider.get_token() == access

    assert any(r.levelno == logging.ERROR for r in caplog.records)
    assert access not in caplog.text
    assert refresh not in caplog.text
    assert "RuntimeError" in caplog.text


def test_persist_error_message_is_logged_verbatim(caplog: pytest.LogCaptureFixture) -> None:
    clock = FakeClock()
    access, refresh = _new_pair(clock)
    session = session_with(response(200, {"access_token": access, "refresh_token": refresh}))
    persist = MagicMock(side_effect=TokenPersistError("could not write to /x/y.toml (OSError)"))
    with caplog.at_level(logging.ERROR):
        _provider(session, clock, persist=persist).get_token()
    assert "/x/y.toml (OSError)" in caplog.text


@pytest.mark.parametrize("status", [400, 401, 403])
def test_rejected_refresh_explains_the_login_window(status: int) -> None:
    clock = FakeClock()
    provider = _provider(session_with(response(status, {"error": "x"})), clock)
    with pytest.raises(DigitalAdvisorAuthError) as exc:
        provider.get_token()
    assert "90 days" in str(exc.value)
    assert "set-credential" in str(exc.value)
    assert "placeholder-refresh-old" not in str(exc.value)


def test_other_failure_status_raises() -> None:
    provider = _provider(session_with(response(500, {})), FakeClock())
    with pytest.raises(DigitalAdvisorAuthError, match="HTTP 500"):
        provider.get_token()


@pytest.mark.parametrize(
    "body",
    [{"access_token": "a"}, {"refresh_token": "r"}, {"access_token": "", "refresh_token": "r"}, []],
)
def test_response_missing_a_token_raises(body: object) -> None:
    provider = _provider(session_with(response(200, body)), FakeClock())
    with pytest.raises(DigitalAdvisorAuthError, match="no access_token and refresh_token"):
        provider.get_token()


def test_connection_error_names_only_the_type() -> None:
    err = requests.ConnectionError("placeholder-refresh-old leaked in text")
    provider = _provider(session_with(err), FakeClock())
    with pytest.raises(DigitalAdvisorAuthError) as exc:
        provider.get_token()
    assert "ConnectionError" in str(exc.value)
    assert "placeholder-refresh-old" not in str(exc.value)


def test_repr_holds_no_token() -> None:
    provider = _provider(session_with(), FakeClock(), access="placeholder-access")
    assert "placeholder" not in repr(provider)
    assert URL in repr(provider)
