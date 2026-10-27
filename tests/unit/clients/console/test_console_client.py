"""Tests for ConsoleAPIClient (ADR-0019 runtime client)."""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock

import pytest

from pynetappfoundry.clients.console.api import (
    ConsoleAPIClient,
    ConsoleServiceTokenMissingError,
)
from pynetappfoundry.core.models import ConsoleAPISettings
from pynetappfoundry.models.console_types import Folder, Organization, Project


@pytest.fixture
def base_settings() -> ConsoleAPISettings:
    """Settings with only the user_token populated (service_token absent)."""
    return ConsoleAPISettings(
        user_token="user-jwt",
        base_url="https://api.bluexp.netapp.com",
        base_api_path="/",
        timeout=15.0,
    )


@pytest.fixture
def both_tokens_settings() -> ConsoleAPISettings:
    """Settings with both user_token and service_token populated."""
    return ConsoleAPISettings(
        user_token="user-jwt",
        service_token="service-jwt",
        base_url="https://api.bluexp.netapp.com",
        base_api_path="/",
        timeout=15.0,
    )


def _make_config(settings: ConsoleAPISettings, tmp_path: Any) -> MagicMock:
    """Build a stub Config object that returns the given settings and a writable schema path."""
    config = MagicMock()
    config.get_console_api_settings.return_value = settings
    # The Console client calls config.get_schema_location("console") / "console_openapi.yaml".
    # Point at a non-existent path; APIWrapper is mocked below so the file is never read.
    config.get_schema_location.return_value = tmp_path
    return config


class TestConsoleAPIClientConstruction:
    """Two-wrapper composition per ADR-0019."""

    def test_constructs_user_wrapper_only_when_service_token_absent(
        self,
        base_settings: ConsoleAPISettings,
        tmp_path: Any,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """`_service` is None when service_token is omitted."""
        wrapper_mock = MagicMock()
        monkeypatch.setattr(
            "pynetappfoundry.clients.console.api.APIWrapper",
            wrapper_mock,
        )
        client = ConsoleAPIClient(_make_config(base_settings, tmp_path))

        assert wrapper_mock.call_count == 1
        assert client._service is None
        # User wrapper was constructed with the user-token bearer header
        user_call_kwargs = wrapper_mock.call_args_list[0].kwargs
        assert user_call_kwargs["auth_header"] == {"Authorization": "Bearer user-jwt"}
        assert user_call_kwargs["name"] == "console-user"

    def test_constructs_both_wrappers_when_service_token_present(
        self,
        both_tokens_settings: ConsoleAPISettings,
        tmp_path: Any,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Both `_user` and `_service` wrappers exist when both tokens are configured."""
        wrapper_mock = MagicMock()
        monkeypatch.setattr(
            "pynetappfoundry.clients.console.api.APIWrapper",
            wrapper_mock,
        )
        client = ConsoleAPIClient(_make_config(both_tokens_settings, tmp_path))

        assert wrapper_mock.call_count == 2
        assert client._service is not None
        service_call_kwargs = wrapper_mock.call_args_list[1].kwargs
        assert service_call_kwargs["auth_header"] == {"Authorization": "Bearer service-jwt"}
        assert service_call_kwargs["name"] == "console-service"


class TestServiceTokenLazyValidation:
    """`_require_service` raises only when callers reach for the missing wrapper."""

    def test_require_service_raises_when_missing(
        self,
        base_settings: ConsoleAPISettings,
        tmp_path: Any,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        monkeypatch.setattr(
            "pynetappfoundry.clients.console.api.APIWrapper",
            MagicMock(),
        )
        client = ConsoleAPIClient(_make_config(base_settings, tmp_path))

        with pytest.raises(ConsoleServiceTokenMissingError, match="service_token"):
            client._require_service()

    def test_require_service_returns_wrapper_when_present(
        self,
        both_tokens_settings: ConsoleAPISettings,
        tmp_path: Any,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        wrapper_mock = MagicMock()
        monkeypatch.setattr(
            "pynetappfoundry.clients.console.api.APIWrapper",
            wrapper_mock,
        )
        client = ConsoleAPIClient(_make_config(both_tokens_settings, tmp_path))

        assert client._require_service() is client._service


class TestHandAuthoredOperations:
    """v1 hand-authored methods route to `_user` and parse the compact Organization type."""

    def test_get_organization_calls_user_wrapper(
        self,
        base_settings: ConsoleAPISettings,
        tmp_path: Any,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        wrapper_instance = MagicMock()
        wrapper_instance.call_endpoint.return_value = {
            "id": "org-abc",
            "name": "Test Org",
            "resourceClass": "tenancyv4",
            "resourceType": "organization",
        }
        wrapper_factory = MagicMock(return_value=wrapper_instance)
        monkeypatch.setattr(
            "pynetappfoundry.clients.console.api.APIWrapper",
            wrapper_factory,
        )

        client = ConsoleAPIClient(_make_config(base_settings, tmp_path))
        org = client.get_organization("org-abc")

        assert isinstance(org, Organization)
        assert org.id == "org-abc"
        assert org.resource_class == "tenancyv4"

        wrapper_instance.call_endpoint.assert_called_once_with(
            method="GET",
            path_template="/organizations/{organization_id}",
            path_params={"organization_id": "org-abc"},
        )

    @pytest.mark.parametrize(
        ("method", "model", "path_template", "param"),
        [
            ("get_folder", Folder, "/folders/{folder_id}", "folder_id"),
            ("get_project", Project, "/projects/{project_id}", "project_id"),
        ],
    )
    def test_get_folder_and_project_call_user_wrapper(
        self,
        method: str,
        model: type[Folder] | type[Project],
        path_template: str,
        param: str,
        both_tokens_settings: ConsoleAPISettings,
        tmp_path: Any,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        user_wrapper = MagicMock()
        user_wrapper.call_endpoint.return_value = {
            "id": "res-1",
            "name": "Res",
            "resourceClass": "tenancyv4",
            "resourceType": method.removeprefix("get_"),
        }
        service_wrapper = MagicMock()
        monkeypatch.setattr(
            "pynetappfoundry.clients.console.api.APIWrapper",
            MagicMock(side_effect=[user_wrapper, service_wrapper]),
        )

        client = ConsoleAPIClient(_make_config(both_tokens_settings, tmp_path))
        result = getattr(client, method)("res-1")

        assert isinstance(result, model)
        assert result.id == "res-1"
        user_wrapper.call_endpoint.assert_called_once_with(
            method="GET",
            path_template=path_template,
            path_params={param: "res-1"},
        )
        service_wrapper.call_endpoint.assert_not_called()

    def test_list_organizations_parses_items(
        self,
        base_settings: ConsoleAPISettings,
        tmp_path: Any,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        wrapper_instance = MagicMock()
        wrapper_instance.call_endpoint.return_value = {
            "items": [
                {
                    "id": "org-1",
                    "name": "Org One",
                    "resourceClass": "tenancyv4",
                    "resourceType": "organization",
                },
                {
                    "id": "org-2",
                    "name": "Org Two",
                    "resourceClass": "tenancyv4",
                    "resourceType": "organization",
                },
            ],
            "count": 2,
        }
        wrapper_factory = MagicMock(return_value=wrapper_instance)
        monkeypatch.setattr(
            "pynetappfoundry.clients.console.api.APIWrapper",
            wrapper_factory,
        )

        client = ConsoleAPIClient(_make_config(base_settings, tmp_path))
        orgs = client.list_organizations()

        assert len(orgs) == 2
        assert {o.id for o in orgs} == {"org-1", "org-2"}

        wrapper_instance.call_endpoint.assert_called_once_with(
            method="GET",
            path_template="/organizations",
        )

    def test_list_organizations_handles_empty_response(
        self,
        base_settings: ConsoleAPISettings,
        tmp_path: Any,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        wrapper_instance = MagicMock()
        wrapper_instance.call_endpoint.return_value = {"count": 0}  # no "items" key
        wrapper_factory = MagicMock(return_value=wrapper_instance)
        monkeypatch.setattr(
            "pynetappfoundry.clients.console.api.APIWrapper",
            wrapper_factory,
        )

        client = ConsoleAPIClient(_make_config(base_settings, tmp_path))
        assert client.list_organizations() == []
