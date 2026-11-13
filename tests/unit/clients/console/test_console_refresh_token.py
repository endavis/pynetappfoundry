"""Tests for the Console refresh-token grant (#736, ADR-0019)."""

from __future__ import annotations

import logging
import threading
import time
from pathlib import Path
from typing import Any, cast
from unittest.mock import MagicMock

import pytest
import requests
from pydantic import SecretStr, ValidationError

import pynetappfoundry.clients.console as console_pkg
from pynetappfoundry.clients.console.agent import AGENT_ID_HEADER, ConsoleAgentClient
from pynetappfoundry.clients.console.api import ConsoleAPIClient, ConsoleUserTokenMissingError
from pynetappfoundry.clients.console.auth import (
    ClientCredentialsTokenProvider,
    ConsoleAuthError,
    RefreshTokenProvider,
)
from pynetappfoundry.core.models import ConsoleAPISettings
from pynetappfoundry.models.console_types import Organization

REFRESH = "placeholder-refresh-token"
ACCESS = "placeholder-access-token"
CLIENT_SECRET = "placeholder-client-secret"
ENDPOINT = "https://auth.example.test/oauth/token"
BASE_URL = "https://api.example.test"
DEFAULT_CLIENT_ID = "Mu0V1ywgYteI6w1MbD15fKfVIUrNXGWC"
AGENT_ID = "agent-placeholder-0001"
ORG = {"id": "org-1", "name": "Org", "resourceClass": "tenancyv4", "resourceType": "organization"}


class FakeClock:
    """Manually advanced clock."""

    def __init__(self) -> None:
        self.now = 1000.0

    def __call__(self) -> float:
        return self.now


def _response(status: int = 200, body: Any = None) -> MagicMock:
    resp = MagicMock()
    resp.status_code = status
    resp.json.return_value = body
    return resp


def _ok(token: str = "tok-1", expires_in: Any = 3600, **extra: Any) -> MagicMock:
    body: dict[str, Any] = {"access_token": token, "token_type": "Bearer", **extra}
    if expires_in is not None:
        body["expires_in"] = expires_in
    return _response(200, body)


def _provider(session: MagicMock, clock: FakeClock | None = None) -> RefreshTokenProvider:
    return RefreshTokenProvider(
        refresh_token=SecretStr(REFRESH),
        client_id="test-client-id",
        token_endpoint=ENDPOINT,
        timeout=12.5,
        session=session,
        clock=clock or FakeClock(),
    )


def _token_session(*tokens: str) -> MagicMock:
    session = MagicMock()
    session.post.side_effect = [_ok(t) for t in tokens]
    return session


def _http_error(status: int) -> requests.HTTPError:
    resp = requests.Response()
    resp.status_code = status
    return requests.HTTPError(f"{status}", response=resp)


def _settings(**overrides: Any) -> ConsoleAPISettings:
    values: dict[str, Any] = {
        "base_url": BASE_URL,
        "base_api_path": "/",
        "refresh_token": REFRESH,
    }
    values.update(overrides)
    return ConsoleAPISettings(**values)


def _config(settings: ConsoleAPISettings, tmp_path: Path) -> MagicMock:
    config = MagicMock()
    config.get_console_api_settings.return_value = settings
    config.get_schema_location.return_value = tmp_path
    return config


class TestRefreshTokenProvider:
    def test_exported(self) -> None:
        assert console_pkg.RefreshTokenProvider is RefreshTokenProvider
        assert "RefreshTokenProvider" in console_pkg.__all__

    def test_posts_exact_body_without_audience(self) -> None:
        session = _token_session("tok-1")
        token = _provider(session).get_token()

        assert token == "tok-1"
        session.post.assert_called_once_with(
            ENDPOINT,
            json={
                "grant_type": "refresh_token",
                "refresh_token": REFRESH,
                "client_id": "test-client-id",
            },
            timeout=12.5,
        )
        assert "audience" not in session.post.call_args.kwargs["json"]

    def test_caches_until_skewed_expiry_then_refetches(self) -> None:
        clock = FakeClock()
        session = _token_session("tok-1", "tok-2")
        provider = _provider(session, clock)

        assert provider.get_token() == "tok-1"
        clock.now += 3600 - 61
        assert provider.get_token() == "tok-1"
        assert session.post.call_count == 1
        clock.now += 2
        assert provider.get_token() == "tok-2"
        assert session.post.call_count == 2

    def test_invalidate_matching_token_refetches(self) -> None:
        session = _token_session("tok-1", "tok-2")
        provider = _provider(session)
        provider.get_token()
        provider.invalidate("tok-1")
        assert provider.get_token() == "tok-2"

    def test_invalidate_stale_token_keeps_cache(self) -> None:
        session = _token_session("tok-1", "tok-2")
        provider = _provider(session)
        provider.get_token()
        provider.invalidate("other-token")
        assert provider.get_token() == "tok-1"
        assert session.post.call_count == 1

    def test_response_refresh_token_is_ignored(self) -> None:
        session = MagicMock()
        session.post.side_effect = [
            _ok("tok-1", refresh_token="placeholder-rotated-refresh"),
            _ok("tok-2"),
        ]
        provider = _provider(session)
        provider.get_token()
        provider.invalidate("tok-1")
        provider.get_token()
        assert session.post.call_args_list[1].kwargs["json"]["refresh_token"] == REFRESH

    def test_invalid_grant_raises_with_oauth_fields(self) -> None:
        session = MagicMock()
        session.post.return_value = _response(
            403,
            {"error": "invalid_grant", "error_description": "Unknown or invalid refresh token."},
        )
        with pytest.raises(ConsoleAuthError) as exc_info:
            _provider(session).get_token()
        text = str(exc_info.value)
        assert "403" in text
        assert "invalid_grant" in text
        assert "Unknown or invalid refresh token." in text
        assert REFRESH not in text

    def test_connection_error_is_chained_without_secrets(self) -> None:
        session = MagicMock()
        session.post.side_effect = requests.ConnectionError(f"boom {REFRESH}")
        with pytest.raises(ConsoleAuthError) as exc_info:
            _provider(session).get_token()
        assert isinstance(exc_info.value.__cause__, requests.ConnectionError)
        assert REFRESH not in str(exc_info.value)

    def test_missing_access_token_raises(self) -> None:
        session = MagicMock()
        session.post.return_value = _response(200, {"expires_in": 3600})
        with pytest.raises(ConsoleAuthError, match="no access_token"):
            _provider(session).get_token()

    def test_no_expiry_reported_never_expires(self) -> None:
        clock = FakeClock()
        session = MagicMock()
        session.post.return_value = _ok("tok-1", expires_in=None)
        provider = _provider(session, clock)
        provider.get_token()
        clock.now += 10**6
        provider.get_token()
        assert session.post.call_count == 1

    def test_secrets_not_in_repr_or_logs(self, caplog: pytest.LogCaptureFixture) -> None:
        session = _token_session(ACCESS)
        provider = _provider(session)
        with caplog.at_level(logging.DEBUG):
            provider.get_token()
        assert "fetched Console user token (expires in 3600s)" in caplog.text
        assert REFRESH not in caplog.text
        assert ACCESS not in caplog.text
        assert REFRESH not in repr(provider)
        assert ACCESS not in repr(provider)
        assert "test-client-id" in repr(provider)
        assert ENDPOINT in repr(provider)

    def test_access_token_not_in_error_text(self) -> None:
        session = MagicMock()
        session.post.return_value = _response(500, {"access_token": ACCESS, "error": "server"})
        with pytest.raises(ConsoleAuthError) as exc_info:
            _provider(session).get_token()
        assert ACCESS not in str(exc_info.value)

    def test_concurrent_cold_cache_posts_once(self) -> None:
        session = MagicMock()

        def slow_post(*args: Any, **kwargs: Any) -> MagicMock:
            time.sleep(0.05)
            return _ok("tok-1")

        session.post.side_effect = slow_post
        provider = _provider(session)
        results: list[str] = []

        def worker() -> None:
            results.append(provider.get_token())

        threads = [threading.Thread(target=worker) for _ in range(8)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert results == ["tok-1"] * 8
        assert session.post.call_count == 1

    def test_client_credentials_provider_unchanged(self, caplog: pytest.LogCaptureFixture) -> None:
        session = _token_session("tok-1")
        provider = ClientCredentialsTokenProvider(
            client_id="cid",
            client_secret=SecretStr(CLIENT_SECRET),
            token_endpoint=ENDPOINT,
            audience="https://aud.example.test",
            timeout=5.0,
            session=session,
            clock=FakeClock(),
        )
        with caplog.at_level(logging.INFO):
            provider.get_token()
        assert session.post.call_args.kwargs["json"] == {
            "audience": "https://aud.example.test",
            "client_id": "cid",
            "client_secret": CLIENT_SECRET,
            "grant_type": "client_credentials",
        }
        assert "fetched Console service token (expires in 3600s)" in caplog.text
        assert CLIENT_SECRET not in repr(provider)


class TestRefreshTokenSettings:
    def test_refresh_token_alone_is_valid(self) -> None:
        s = _settings()
        assert s.uses_refresh_token is True
        assert s.user_client_id == DEFAULT_CLIENT_ID
        assert s.refresh_token is not None
        assert s.refresh_token.get_secret_value() == REFRESH

    def test_no_refresh_token_does_not_use_it(self) -> None:
        s = ConsoleAPISettings(base_url=BASE_URL, user_token="user-jwt")
        assert s.uses_refresh_token is False
        assert s.refresh_token is None

    def test_with_user_token_rejected(self) -> None:
        with pytest.raises(ValidationError, match="mutually exclusive"):
            _settings(user_token="user-jwt")

    def test_custom_token_endpoint_valid(self) -> None:
        assert _settings(token_endpoint=ENDPOINT).token_endpoint == ENDPOINT

    def test_audience_without_client_credentials_rejected(self) -> None:
        with pytest.raises(ValidationError, match="require client_id and client_secret"):
            _settings(audience="https://aud.example.test")

    def test_user_client_id_without_refresh_token_rejected(self) -> None:
        with pytest.raises(ValidationError, match="user_client_id requires a refresh token"):
            ConsoleAPISettings(base_url=BASE_URL, user_token="user-jwt", user_client_id="x")

    def test_user_client_id_with_refresh_token_valid(self) -> None:
        assert _settings(user_client_id="custom-client").user_client_id == "custom-client"

    def test_with_client_credentials_valid(self) -> None:
        s = _settings(client_id="cid", client_secret=CLIENT_SECRET)
        assert s.uses_refresh_token and s.uses_client_credentials

    def test_token_endpoint_without_refresh_or_credentials_still_rejected(self) -> None:
        with pytest.raises(ValidationError, match="require client_id and client_secret"):
            ConsoleAPISettings(base_url=BASE_URL, user_token="u", token_endpoint=ENDPOINT)

    def test_one_of_message_mentions_refresh_token(self) -> None:
        with pytest.raises(ValidationError, match="a refresh token"):
            ConsoleAPISettings(base_url=BASE_URL)

    def test_secret_never_exposed(self) -> None:
        s = _settings()
        assert REFRESH not in repr(s)
        assert REFRESH not in str(s)
        assert REFRESH not in str(s.model_dump())
        assert REFRESH not in s.model_dump_json()
        with pytest.raises(ValidationError) as exc_info:
            _settings(user_token="user-jwt")
        assert REFRESH not in str(exc_info.value)


@pytest.fixture
def api_wrapper_factory(monkeypatch: pytest.MonkeyPatch) -> MagicMock:
    factory = MagicMock(side_effect=lambda **kw: MagicMock(name=kw.get("name")))
    monkeypatch.setattr("pynetappfoundry.clients.console.api.APIWrapper", factory)
    return factory


@pytest.fixture
def agent_wrapper_factory(monkeypatch: pytest.MonkeyPatch) -> MagicMock:
    factory = MagicMock(side_effect=lambda **kw: MagicMock(name=kw.get("name")))
    monkeypatch.setattr("pynetappfoundry.clients.console.agent.APIWrapper", factory)
    return factory


def _user(client: ConsoleAPIClient) -> MagicMock:
    assert client._user is not None
    return cast("MagicMock", client._user)


class TestConsoleAPIClientRefreshToken:
    def test_user_wrapper_has_no_static_header_and_provider(
        self, api_wrapper_factory: MagicMock, tmp_path: Path
    ) -> None:
        session = _token_session("tok-1")
        client = ConsoleAPIClient(_config(_settings(), tmp_path), token_session=session)

        assert api_wrapper_factory.call_count == 1
        kwargs = api_wrapper_factory.call_args.kwargs
        assert kwargs["name"] == "console-user"
        assert kwargs["auth_header"] is None
        assert isinstance(client.user_token_provider, RefreshTokenProvider)
        assert client.service_token_provider is None
        assert session.post.call_count == 1  # eager exchange
        body = session.post.call_args.kwargs["json"]
        assert body["client_id"] == DEFAULT_CLIENT_ID
        assert body["grant_type"] == "refresh_token"

    def test_static_user_token_has_no_provider(
        self, api_wrapper_factory: MagicMock, tmp_path: Path
    ) -> None:
        settings = ConsoleAPISettings(base_url=BASE_URL, user_token="user-jwt")
        client = ConsoleAPIClient(_config(settings, tmp_path))
        assert client.user_token_provider is None

    def test_bad_refresh_token_raises_at_construction(
        self, api_wrapper_factory: MagicMock, tmp_path: Path
    ) -> None:
        session = MagicMock()
        session.post.return_value = _response(403, {"error": "invalid_grant"})
        with pytest.raises(ConsoleAuthError) as exc_info:
            ConsoleAPIClient(_config(_settings(), tmp_path), token_session=session)
        assert REFRESH not in str(exc_info.value)

    def test_call_sends_authorization_per_call(
        self, api_wrapper_factory: MagicMock, tmp_path: Path
    ) -> None:
        session = _token_session("t1")
        client = ConsoleAPIClient(_config(_settings(), tmp_path), token_session=session)
        user = _user(client)
        user.call_endpoint.return_value = ORG

        org = client.get_organization("org-1")

        assert isinstance(org, Organization)
        user.call_endpoint.assert_called_once_with(
            method="GET",
            path_template="/v1/management/organizations/{organization_id}",
            path_params={"organization_id": "org-1"},
            additional_headers={"Authorization": "Bearer t1"},
        )

    def test_401_then_200_refetches_once(
        self, api_wrapper_factory: MagicMock, tmp_path: Path
    ) -> None:
        session = _token_session("t1", "t2")
        client = ConsoleAPIClient(_config(_settings(), tmp_path), token_session=session)
        user = _user(client)
        user.call_endpoint.side_effect = [_http_error(401), {"items": [ORG]}]

        orgs = client.list_organizations()

        assert len(orgs) == 1
        assert session.post.call_count == 2
        sent = [c.kwargs["additional_headers"] for c in user.call_endpoint.call_args_list]
        assert sent == [{"Authorization": "Bearer t1"}, {"Authorization": "Bearer t2"}]

    def test_two_401s_propagate(self, api_wrapper_factory: MagicMock, tmp_path: Path) -> None:
        session = _token_session("t1", "t2")
        client = ConsoleAPIClient(_config(_settings(), tmp_path), token_session=session)
        user = _user(client)
        user.call_endpoint.side_effect = [_http_error(401), _http_error(401)]

        with pytest.raises(requests.HTTPError):
            client.list_organizations()
        assert user.call_endpoint.call_count == 2

    def test_refresh_token_with_client_credentials_routes_to_user_slot(
        self, api_wrapper_factory: MagicMock, tmp_path: Path
    ) -> None:
        settings = _settings(client_id="cid", client_secret=CLIENT_SECRET)
        session = _token_session("user-tok", "svc-tok")
        client = ConsoleAPIClient(_config(settings, tmp_path), token_session=session)
        user = _user(client)
        service = cast("MagicMock", client._service)
        user.call_endpoint.return_value = {"items": [ORG]}

        client.list_organizations()

        assert [c.kwargs["name"] for c in api_wrapper_factory.call_args_list] == [
            "console-user",
            "console-service",
        ]
        user.call_endpoint.assert_called_once()
        service.call_endpoint.assert_not_called()
        assert user.call_endpoint.call_args.kwargs["additional_headers"] == {
            "Authorization": "Bearer user-tok"
        }

    def test_missing_user_message_mentions_refresh_token(
        self, api_wrapper_factory: MagicMock, tmp_path: Path
    ) -> None:
        settings = ConsoleAPISettings(base_url=BASE_URL, service_token="service-jwt")
        client = ConsoleAPIClient(_config(settings, tmp_path))
        with pytest.raises(ConsoleUserTokenMissingError, match=r"users\.toml"):
            client._require_user()
        with pytest.raises(ConsoleUserTokenMissingError, match="user_token"):
            client._require_user()


class TestConsoleAgentClientRefreshToken:
    def test_refresh_token_builds_provider_and_agent_header_only(
        self, agent_wrapper_factory: MagicMock, tmp_path: Path
    ) -> None:
        session = _token_session("tok-1")
        client = ConsoleAgentClient(_config(_settings(), tmp_path), AGENT_ID, token_session=session)

        assert agent_wrapper_factory.call_args.kwargs["auth_header"] == {AGENT_ID_HEADER: AGENT_ID}
        assert isinstance(client._provider, RefreshTokenProvider)
        assert session.post.call_count == 1

    def test_401_is_refreshed_once(self, agent_wrapper_factory: MagicMock, tmp_path: Path) -> None:
        session = _token_session("t1", "t2")
        client = ConsoleAgentClient(_config(_settings(), tmp_path), AGENT_ID, token_session=session)
        wrapper = cast("MagicMock", client._wrapper)
        wrapper.call_endpoint.side_effect = [_http_error(401), {"ok": True}]

        result = client._call(method="GET", path_template="/x")

        assert result == {"ok": True}
        assert session.post.call_count == 2
        sent = [c.kwargs["additional_headers"] for c in wrapper.call_endpoint.call_args_list]
        assert sent == [{"Authorization": "Bearer t1"}, {"Authorization": "Bearer t2"}]

    def test_injected_provider_still_wins(
        self, agent_wrapper_factory: MagicMock, tmp_path: Path
    ) -> None:
        session = _token_session("tok-1")
        injected = MagicMock()
        client = ConsoleAgentClient(
            _config(_settings(), tmp_path),
            AGENT_ID,
            token_provider=injected,
            token_session=session,
        )
        assert client._provider is injected
        assert session.post.call_count == 0

    def test_refresh_token_beats_client_credentials(
        self, agent_wrapper_factory: MagicMock, tmp_path: Path
    ) -> None:
        session = _token_session("tok-1")
        client = ConsoleAgentClient(
            _config(_settings(client_id="cid", client_secret=CLIENT_SECRET), tmp_path),
            AGENT_ID,
            token_session=session,
        )
        assert isinstance(client._provider, RefreshTokenProvider)
        assert session.post.call_args.kwargs["json"]["grant_type"] == "refresh_token"
