"""Tests for ConsoleAPIClient with an OAuth client-credentials service slot."""

from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import Any, cast
from unittest.mock import MagicMock

import pytest
import requests
from pydantic import SecretStr

from pynetappfoundry.clients.console.api import (
    ConsoleAPIClient,
    ConsoleServiceTokenMissingError,
    ConsoleUserTokenMissingError,
)
from pynetappfoundry.clients.console.auth import ConsoleAuthError
from pynetappfoundry.console import Console
from pynetappfoundry.core.config import Config, ConfigurationError
from pynetappfoundry.core.models import ConsoleAPISettings
from pynetappfoundry.models.console_types import Organization

SECRET = "s3cr3t-value"
BASE_URL = "https://api.example.test"
ORG = {"id": "org-1", "name": "Org", "resourceClass": "tenancyv4", "resourceType": "organization"}


def _settings(**overrides: Any) -> ConsoleAPISettings:
    values: dict[str, Any] = {
        "base_url": BASE_URL,
        "base_api_path": "/",
        "client_id": "test-client-id",
        "client_secret": SECRET,
    }
    values.update(overrides)
    return ConsoleAPISettings(**values)


def _config(settings: ConsoleAPISettings, tmp_path: Any) -> MagicMock:
    config = MagicMock()
    config.get_console_api_settings.return_value = settings
    config.get_schema_location.return_value = tmp_path
    return config


def _token_session(*tokens: str) -> MagicMock:
    session = MagicMock()
    responses = []
    for tok in tokens:
        resp = MagicMock()
        resp.status_code = 200
        resp.json.return_value = {"access_token": tok, "expires_in": 3600}
        responses.append(resp)
    session.post.side_effect = responses
    return session


def _svc(client: ConsoleAPIClient) -> MagicMock:
    """Return the (mocked) service wrapper of a client built with a patched APIWrapper."""
    assert client._service is not None
    return cast("MagicMock", client._service)


def _http_error(status: int) -> requests.HTTPError:
    resp = requests.Response()
    resp.status_code = status
    return requests.HTTPError(f"{status}", response=resp)


@pytest.fixture
def wrapper_factory(monkeypatch: pytest.MonkeyPatch) -> MagicMock:
    """Patch APIWrapper; each construction returns a fresh mock."""
    factory = MagicMock(side_effect=lambda **kw: MagicMock(name=kw.get("name")))
    monkeypatch.setattr("pynetappfoundry.clients.console.api.APIWrapper", factory)
    return factory


class TestConstruction:
    def test_credentials_only(self, wrapper_factory: MagicMock, tmp_path: Any) -> None:
        session = _token_session("tok-1")
        client = ConsoleAPIClient(_config(_settings(), tmp_path), token_session=session)

        assert wrapper_factory.call_count == 1
        kwargs = wrapper_factory.call_args.kwargs
        assert kwargs["name"] == "console-service"
        assert kwargs["auth_header"] is None
        assert client._user is None
        assert client.service_token_provider is not None
        assert session.post.call_count == 1  # eager exchange

    def test_user_plus_credentials_builds_user_first(
        self, wrapper_factory: MagicMock, tmp_path: Any
    ) -> None:
        ConsoleAPIClient(
            _config(_settings(user_token="user-jwt"), tmp_path),
            token_session=_token_session("tok-1"),
        )
        names = [c.kwargs["name"] for c in wrapper_factory.call_args_list]
        assert names == ["console-user", "console-service"]
        assert wrapper_factory.call_args_list[0].kwargs["auth_header"] == {
            "Authorization": "Bearer user-jwt"
        }

    def test_static_service_token_has_no_provider(
        self, wrapper_factory: MagicMock, tmp_path: Any
    ) -> None:
        settings = ConsoleAPISettings(
            base_url=BASE_URL,
            user_token=SecretStr("user-jwt"),
            service_token=SecretStr("service-jwt"),
        )
        client = ConsoleAPIClient(_config(settings, tmp_path))
        assert client.service_token_provider is None

    def test_bad_credentials_raise_at_construction(
        self, wrapper_factory: MagicMock, tmp_path: Any
    ) -> None:
        session = MagicMock()
        resp = MagicMock()
        resp.status_code = 401
        resp.json.return_value = {"error": "access_denied"}
        session.post.return_value = resp
        with pytest.raises(ConsoleAuthError) as exc_info:
            ConsoleAPIClient(_config(_settings(), tmp_path), token_session=session)
        assert SECRET not in str(exc_info.value)

    def test_require_user_raises_without_user_token(
        self, wrapper_factory: MagicMock, tmp_path: Any
    ) -> None:
        client = ConsoleAPIClient(_config(_settings(), tmp_path), token_session=_token_session("t"))
        with pytest.raises(ConsoleUserTokenMissingError, match="user_token"):
            client._require_user()


class TestRouting:
    def test_credentials_only_sends_bearer_per_call(
        self, wrapper_factory: MagicMock, tmp_path: Any
    ) -> None:
        client = ConsoleAPIClient(
            _config(_settings(), tmp_path), token_session=_token_session("tok-1")
        )
        service = _svc(client)
        service.call_endpoint.return_value = ORG

        org = client.get_organization("org-1")

        assert isinstance(org, Organization)
        service.call_endpoint.assert_called_once_with(
            method="GET",
            path_template="/v1/management/organizations/{organization_id}",
            path_params={"organization_id": "org-1"},
            additional_headers={"Authorization": "Bearer tok-1"},
        )

    def test_user_token_preferred_with_exact_kwargs(
        self, wrapper_factory: MagicMock, tmp_path: Any
    ) -> None:
        client = ConsoleAPIClient(
            _config(_settings(user_token="user-jwt"), tmp_path),
            token_session=_token_session("tok-1"),
        )
        user = cast("MagicMock", client._user)
        user.call_endpoint.return_value = {"items": [ORG]}

        orgs = client.list_organizations()

        assert len(orgs) == 1
        user.call_endpoint.assert_called_once_with(
            method="GET", path_template="/v1/management/organizations"
        )
        _svc(client).call_endpoint.assert_not_called()

    def test_static_service_token_only_uses_service_without_headers(
        self, wrapper_factory: MagicMock, tmp_path: Any
    ) -> None:
        settings = ConsoleAPISettings(base_url=BASE_URL, service_token=SecretStr("service-jwt"))
        client = ConsoleAPIClient(_config(settings, tmp_path))
        service = _svc(client)
        service.call_endpoint.return_value = ORG
        client.get_organization("org-1")
        service.call_endpoint.assert_called_once_with(
            method="GET",
            path_template="/v1/management/organizations/{organization_id}",
            path_params={"organization_id": "org-1"},
        )

    def test_static_service_token_401_not_retried(
        self, wrapper_factory: MagicMock, tmp_path: Any
    ) -> None:
        settings = ConsoleAPISettings(base_url=BASE_URL, service_token=SecretStr("service-jwt"))
        client = ConsoleAPIClient(_config(settings, tmp_path))
        service = _svc(client)
        service.call_endpoint.side_effect = _http_error(401)
        with pytest.raises(requests.HTTPError):
            client.get_organization("org-1")
        assert service.call_endpoint.call_count == 1

    def test_require_service_unaffected(self, wrapper_factory: MagicMock, tmp_path: Any) -> None:
        client = ConsoleAPIClient(
            _config(ConsoleAPISettings(base_url=BASE_URL, user_token=SecretStr("u")), tmp_path)
        )
        with pytest.raises(ConsoleServiceTokenMissingError):
            client._require_service()


class TestRefreshOn401:
    def test_401_then_success_refetches_once(
        self, wrapper_factory: MagicMock, tmp_path: Any
    ) -> None:
        session = _token_session("tok-1", "tok-2")
        client = ConsoleAPIClient(_config(_settings(), tmp_path), token_session=session)
        service = _svc(client)
        service.call_endpoint.side_effect = [_http_error(401), ORG]

        client.get_organization("org-1")

        assert session.post.call_count == 2
        sent = [c.kwargs["additional_headers"] for c in service.call_endpoint.call_args_list]
        assert sent == [
            {"Authorization": "Bearer tok-1"},
            {"Authorization": "Bearer tok-2"},
        ]

    def test_401_twice_propagates(self, wrapper_factory: MagicMock, tmp_path: Any) -> None:
        session = _token_session("tok-1", "tok-2")
        client = ConsoleAPIClient(_config(_settings(), tmp_path), token_session=session)
        service = _svc(client)
        service.call_endpoint.side_effect = [_http_error(401), _http_error(401)]

        with pytest.raises(requests.HTTPError):
            client.get_organization("org-1")
        assert service.call_endpoint.call_count == 2
        assert session.post.call_count == 2

    def test_non_401_does_not_refetch(self, wrapper_factory: MagicMock, tmp_path: Any) -> None:
        session = _token_session("tok-1", "tok-2")
        client = ConsoleAPIClient(_config(_settings(), tmp_path), token_session=session)
        service = _svc(client)
        service.call_endpoint.side_effect = _http_error(500)

        with pytest.raises(requests.HTTPError):
            client.get_organization("org-1")
        assert service.call_endpoint.call_count == 1
        assert session.post.call_count == 1


class TestFacade:
    def test_facade_works_with_credentials_only(
        self, wrapper_factory: MagicMock, tmp_path: Any, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        provider = MagicMock()
        provider.get_token.return_value = "tok-1"
        monkeypatch.setattr(
            "pynetappfoundry.clients.console.api.ClientCredentialsTokenProvider",
            MagicMock(return_value=provider),
        )
        console = Console(_config(_settings(org_id="org-1"), tmp_path))
        service = _svc(console._client)
        service.call_endpoint.return_value = ORG

        org = console.get_organization()

        assert org.id == "org-1"
        assert service.call_endpoint.call_args.kwargs["additional_headers"] == {
            "Authorization": "Bearer tok-1"
        }


class TestConfigAccessor:
    def _config_for(self, config_dir: Path, tmp_path: Path, toml: str) -> Config:
        (config_dir / "consoleapi.toml").write_text(toml)
        output_dir = tmp_path / "output"
        output_dir.mkdir(exist_ok=True)
        return Config(
            config_dir=str(config_dir), output_dir=str(output_dir), script_name="test_script"
        )

    def test_credentials_only_toml_loads(self, tmp_path: Path) -> None:
        config_dir = tmp_path / "cfg"
        config_dir.mkdir()
        original = os.getcwd()
        os.chdir(tmp_path)
        try:
            config = self._config_for(
                config_dir,
                tmp_path,
                f'[general]\nbase_url = "{BASE_URL}"\nclient_id = "test-client-id"\n'
                f'client_secret = "{SECRET}"\n',
            )
            settings = config.get_console_api_settings()
            assert settings.uses_client_credentials
            assert settings.client_secret is not None
            assert settings.client_secret.get_secret_value() == SECRET
        finally:
            os.chdir(original)

    def test_invalid_combination_error_has_no_secret(self, tmp_path: Path) -> None:
        config_dir = tmp_path / "cfg"
        config_dir.mkdir()
        original = os.getcwd()
        os.chdir(tmp_path)
        try:
            config = self._config_for(
                config_dir,
                tmp_path,
                f'[general]\nbase_url = "{BASE_URL}"\nservice_token = "svc"\n'
                f'client_id = "test-client-id"\nclient_secret = "{SECRET}"\n',
            )
            with pytest.raises(ConfigurationError) as exc_info:
                config.get_console_api_settings()
            assert SECRET not in str(exc_info.value)
            assert "mutually exclusive" in str(exc_info.value)
        finally:
            os.chdir(original)


def test_token_not_logged_during_calls(
    wrapper_factory: MagicMock, tmp_path: Any, caplog: pytest.LogCaptureFixture
) -> None:
    with caplog.at_level(logging.DEBUG):
        client = ConsoleAPIClient(
            _config(_settings(), tmp_path), token_session=_token_session("tok-visible-check")
        )
        _svc(client).call_endpoint.return_value = ORG
        client.get_organization("org-1")
    assert "tok-visible-check" not in caplog.text
    assert SECRET not in caplog.text
