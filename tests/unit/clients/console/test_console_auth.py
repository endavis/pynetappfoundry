"""Tests for the Console client-credentials token provider and settings."""

from __future__ import annotations

import logging
import threading
from typing import Any
from unittest.mock import MagicMock

import pytest
import requests
from pydantic import SecretStr, ValidationError

from pynetappfoundry.clients.console.auth import (
    ClientCredentialsTokenProvider,
    ConsoleAuthError,
)
from pynetappfoundry.core.models import ConsoleAPISettings

SECRET = "s3cr3t-value"
ENDPOINT = "https://auth.example.test/oauth/token"


class FakeClock:
    """Manually advanced clock."""

    def __init__(self) -> None:
        self.now = 1000.0

    def __call__(self) -> float:
        return self.now


def _response(
    status: int = 200,
    body: Any = None,
    json_error: bool = False,
) -> MagicMock:
    resp = MagicMock()
    resp.status_code = status
    if json_error:
        resp.json.side_effect = ValueError("not json")
    else:
        resp.json.return_value = body
    return resp


def _token_body(token: str = "tok-1", expires_in: Any = 3600) -> dict[str, Any]:
    body: dict[str, Any] = {"access_token": token, "token_type": "Bearer"}
    if expires_in is not None:
        body["expires_in"] = expires_in
    return body


def _provider(session: MagicMock, clock: FakeClock | None = None) -> ClientCredentialsTokenProvider:
    return ClientCredentialsTokenProvider(
        client_id="test-client-id",
        client_secret=SecretStr(SECRET),
        token_endpoint=ENDPOINT,
        audience="https://aud.example.test",
        timeout=12.5,
        session=session,
        clock=clock or FakeClock(),
    )


class TestClientCredentialsTokenProvider:
    """Behaviour of the token provider."""

    def test_posts_exact_body_and_timeout(self) -> None:
        session = MagicMock()
        session.post.return_value = _response(body=_token_body())
        token = _provider(session).get_token()

        assert token == "tok-1"
        session.post.assert_called_once_with(
            ENDPOINT,
            json={
                "audience": "https://aud.example.test",
                "client_id": "test-client-id",
                "client_secret": SECRET,
                "grant_type": "client_credentials",
            },
            timeout=12.5,
        )

    def test_caches_token(self) -> None:
        session = MagicMock()
        session.post.return_value = _response(body=_token_body())
        provider = _provider(session)
        provider.get_token()
        provider.get_token()
        assert session.post.call_count == 1

    def test_refetches_after_skew(self) -> None:
        clock = FakeClock()
        session = MagicMock()
        session.post.side_effect = [
            _response(body=_token_body("tok-1", 3600)),
            _response(body=_token_body("tok-2", 3600)),
        ]
        provider = _provider(session, clock)
        assert provider.get_token() == "tok-1"
        clock.now += 3600 - 61
        assert provider.get_token() == "tok-1"
        clock.now += 2
        assert provider.get_token() == "tok-2"

    def test_short_lifetime_uses_half(self) -> None:
        clock = FakeClock()
        session = MagicMock()
        session.post.side_effect = [
            _response(body=_token_body("tok-1", 30)),
            _response(body=_token_body("tok-2", 30)),
        ]
        provider = _provider(session, clock)
        provider.get_token()
        clock.now += 14
        assert provider.get_token() == "tok-1"
        clock.now += 2
        assert provider.get_token() == "tok-2"

    def test_missing_expires_in_never_expires_on_clock(self) -> None:
        clock = FakeClock()
        session = MagicMock()
        session.post.return_value = _response(body=_token_body(expires_in=None))
        provider = _provider(session, clock)
        provider.get_token()
        clock.now += 10_000_000
        provider.get_token()
        assert session.post.call_count == 1

    def test_invalidate_matching_token_forces_refetch(self) -> None:
        session = MagicMock()
        session.post.side_effect = [
            _response(body=_token_body("tok-1")),
            _response(body=_token_body("tok-2")),
        ]
        provider = _provider(session)
        provider.invalidate(provider.get_token())
        assert provider.get_token() == "tok-2"

    def test_invalidate_stale_token_keeps_newer(self) -> None:
        session = MagicMock()
        session.post.side_effect = [
            _response(body=_token_body("tok-1")),
            _response(body=_token_body("tok-2")),
        ]
        provider = _provider(session)
        provider.invalidate(provider.get_token())
        assert provider.get_token() == "tok-2"
        provider.invalidate("tok-1")
        assert provider.get_token() == "tok-2"
        assert session.post.call_count == 2

    def test_non_2xx_raises_with_oauth_error(self) -> None:
        session = MagicMock()
        session.post.return_value = _response(
            401, {"error": "access_denied", "error_description": "Unauthorized"}
        )
        with pytest.raises(ConsoleAuthError) as exc_info:
            _provider(session).get_token()
        message = str(exc_info.value)
        assert "401" in message
        assert "access_denied" in message
        assert "Unauthorized" in message
        assert SECRET not in message

    def test_non_json_body_raises(self) -> None:
        session = MagicMock()
        session.post.return_value = _response(200, json_error=True)
        with pytest.raises(ConsoleAuthError):
            _provider(session).get_token()

    @pytest.mark.parametrize("body", [{}, {"access_token": ""}, {"access_token": 5}, ["x"]])
    def test_missing_token_raises(self, body: Any) -> None:
        session = MagicMock()
        session.post.return_value = _response(200, body)
        with pytest.raises(ConsoleAuthError, match="access_token"):
            _provider(session).get_token()

    def test_connection_error_raises_chained_without_secret(self) -> None:
        session = MagicMock()
        cause = requests.ConnectionError(f"boom {SECRET}")
        session.post.side_effect = cause
        with pytest.raises(ConsoleAuthError) as exc_info:
            _provider(session).get_token()
        assert SECRET not in str(exc_info.value)
        assert exc_info.value.__cause__ is cause

    def test_secret_and_token_not_logged_or_in_repr(self, caplog: pytest.LogCaptureFixture) -> None:
        session = MagicMock()
        session.post.return_value = _response(body=_token_body("tok-visible-check"))
        provider = _provider(session)
        with caplog.at_level(logging.DEBUG):
            provider.get_token()
        assert SECRET not in caplog.text
        assert "tok-visible-check" not in caplog.text
        assert "fetched Console service token" in caplog.text
        assert SECRET not in repr(provider)
        assert "tok-visible-check" not in repr(provider)
        assert "test-client-id" in repr(provider)

    def test_concurrent_cold_cache_posts_once(self) -> None:
        session = MagicMock()
        session.post.return_value = _response(body=_token_body())
        provider = _provider(session)
        barrier = threading.Barrier(8)
        results: list[str] = []

        def worker() -> None:
            barrier.wait()
            results.append(provider.get_token())

        threads = [threading.Thread(target=worker) for _ in range(8)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert results == ["tok-1"] * 8
        assert session.post.call_count == 1


class TestConsoleAPISettingsCredentials:
    """Validation of credential combinations."""

    BASE = "https://api.example.test"

    def test_credentials_only_valid_with_defaults(self) -> None:
        s = ConsoleAPISettings(
            base_url=self.BASE, client_id="test-client-id", client_secret=SecretStr(SECRET)
        )
        assert s.uses_client_credentials
        assert s.user_token is None
        assert s.token_endpoint.startswith("https://")
        assert s.audience.startswith("https://")

    def test_user_token_only_valid(self) -> None:
        s = ConsoleAPISettings(base_url=self.BASE, user_token="user-jwt")
        assert not s.uses_client_credentials

    def test_half_credentials_rejected(self) -> None:
        with pytest.raises(ValidationError, match="together"):
            ConsoleAPISettings(base_url=self.BASE, user_token="u", client_id="test-client-id")
        with pytest.raises(ValidationError, match="together"):
            ConsoleAPISettings(base_url=self.BASE, user_token="u", client_secret=SecretStr(SECRET))

    def test_credentials_plus_service_token_rejected(self) -> None:
        with pytest.raises(ValidationError, match="mutually exclusive"):
            ConsoleAPISettings(
                base_url=self.BASE,
                service_token="svc",
                client_id="test-client-id",
                client_secret=SecretStr(SECRET),
            )

    @pytest.mark.parametrize("field", ["audience", "token_endpoint"])
    def test_endpoint_fields_without_credentials_rejected(self, field: str) -> None:
        with pytest.raises(ValidationError, match="require client_id"):
            ConsoleAPISettings.model_validate(
                {"base_url": self.BASE, "user_token": "u", field: "https://x.test"}
            )

    def test_no_source_rejected(self) -> None:
        with pytest.raises(ValidationError, match="one of user_token"):
            ConsoleAPISettings(base_url=self.BASE)

    def test_secret_not_exposed(self) -> None:
        raw = {"base_url": self.BASE, "client_id": "test-client-id", "client_secret": SECRET}
        s = ConsoleAPISettings.model_validate(raw)
        assert SECRET not in repr(s)
        assert SECRET not in str(s)
        assert SECRET not in s.model_dump_json()
        with pytest.raises(ValidationError) as exc_info:
            ConsoleAPISettings.model_validate({**raw, "service_token": "svc"})
        assert SECRET not in str(exc_info.value)
