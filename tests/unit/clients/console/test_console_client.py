"""Tests for ConsoleAPIClient (ADR-0019 runtime client)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import pytest
import yaml
from pydantic import SecretStr

from pynetappfoundry.clients.console.api import (
    ConsoleAPIClient,
    ConsoleServiceTokenMissingError,
)
from pynetappfoundry.core.config import Config
from pynetappfoundry.core.models import ConsoleAPISettings
from pynetappfoundry.models.console_types import Folder, Organization, Project


@pytest.fixture
def base_settings() -> ConsoleAPISettings:
    """Settings with only the user_token populated (service_token absent)."""
    return ConsoleAPISettings(
        user_token=SecretStr("user-jwt"),
        base_url="https://api.bluexp.netapp.com",
        base_api_path="/",
        timeout=15.0,
    )


@pytest.fixture
def both_tokens_settings() -> ConsoleAPISettings:
    """Settings with both user_token and service_token populated."""
    return ConsoleAPISettings(
        user_token=SecretStr("user-jwt"),
        service_token=SecretStr("service-jwt"),
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
            path_template="/v1/management/organizations/{organization_id}",
            path_params={"organization_id": "org-abc"},
        )

    @pytest.mark.parametrize(
        ("method", "model", "path_template", "param"),
        [
            ("get_folder", Folder, "/v1/management/folders/{folder_id}", "folder_id"),
            ("get_project", Project, "/v1/management/projects/{project_id}", "project_id"),
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
            path_template="/v1/management/organizations",
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


class TestConsoleAPIClientRealSpec:
    """Construct against the real generated YAML spec, with APIWrapper unmocked (#1011)."""

    def test_constructs_from_documented_yaml_spec(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        repo_root = Path(__file__).resolve().parents[4]
        real_spec = repo_root / "tools" / "console_openapi" / "generated" / "console_openapi.yaml"
        api_dir = tmp_path / "cfg" / "apis" / "console"
        api_dir.mkdir(parents=True)
        (api_dir / "console_openapi.yaml").write_bytes(real_spec.read_bytes())
        (api_dir / "consoleapi.toml").write_text(
            "[general]\nuser_token = 'fake-user-jwt'\nbase_url = 'https://api.bluexp.netapp.com'\n",
            encoding="utf-8",
        )
        monkeypatch.chdir(tmp_path)

        client = ConsoleAPIClient(Config(config_dir=tmp_path / "cfg", output_dir=tmp_path / "out"))

        assert client._user is not None
        assert client._user.api_spec["paths"]


_REAL_SPEC = Path(__file__).parents[4] / "tools/console_openapi/generated/console_openapi.yaml"
_HOST = "https://api.bluexp.netapp.com"


def _real_client(settings: ConsoleAPISettings, tmp_path: Path) -> ConsoleAPIClient:
    """Build a client on the real Console spec (YAML loaded here, written as JSON)."""
    schema_dir = tmp_path / "schema"
    schema_dir.mkdir()
    spec = yaml.safe_load(_REAL_SPEC.read_text(encoding="utf-8"))
    (schema_dir / "console_openapi.yaml").write_text(json.dumps(spec), encoding="utf-8")
    return ConsoleAPIClient(_make_config(settings, schema_dir))


class TestConsoleOperationServers:
    """The Console client routes each operation to its own spec server (#1012)."""

    def test_wrappers_constructed_with_operation_servers(
        self,
        both_tokens_settings: ConsoleAPISettings,
        tmp_path: Any,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        wrapper_mock = MagicMock()
        monkeypatch.setattr("pynetappfoundry.clients.console.api.APIWrapper", wrapper_mock)
        ConsoleAPIClient(_make_config(both_tokens_settings, tmp_path))

        assert wrapper_mock.call_count == 2
        for call in wrapper_mock.call_args_list:
            assert call.kwargs["use_operation_servers"] is True

    def test_service_token_wrapper_uses_operation_servers(
        self,
        tmp_path: Any,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        wrapper_mock = MagicMock()
        monkeypatch.setattr("pynetappfoundry.clients.console.api.APIWrapper", wrapper_mock)
        settings = ConsoleAPISettings(
            service_token=SecretStr("service-jwt"), base_url=_HOST, base_api_path="/", timeout=15.0
        )
        ConsoleAPIClient(_make_config(settings, tmp_path))

        assert wrapper_mock.call_args.kwargs["use_operation_servers"] is True

    def test_list_organizations_requests_v1_management_url(
        self, base_settings: ConsoleAPISettings, tmp_path: Path
    ) -> None:
        client = _real_client(base_settings, tmp_path)
        wrapper = client._require_user()
        response = MagicMock()
        response.status_code = 200
        response.json.return_value = {"items": []}
        with patch.object(wrapper, "_execute_request_with_retry", return_value=response) as mocked:
            assert client.list_organizations() == []

        assert mocked.call_args.kwargs["url"] == f"{_HOST}/v1/management/organizations"

    def test_get_organization_path_has_v1_management_prefix(
        self, base_settings: ConsoleAPISettings, tmp_path: Path
    ) -> None:
        wrapper = _real_client(base_settings, tmp_path)._require_user()
        path = wrapper._format_path(
            "/v1/management/organizations/{organization_id}", {"organization_id": "abc"}, "GET"
        )
        assert path == "/v1/management/organizations/abc"

    def test_bare_host_operation_has_no_prefix(
        self, base_settings: ConsoleAPISettings, tmp_path: Path
    ) -> None:
        wrapper = _real_client(base_settings, tmp_path)._require_user()
        bare = [
            (path, method)
            for path, item in wrapper.api_spec["paths"].items()
            for method, op in item.items()
            if isinstance(op, dict) and op.get("servers", [{}])[0].get("url") == _HOST
        ]
        assert bare
        path, method = bare[0]
        assert wrapper._format_path(path, None, method.upper()) == path

    def test_legacy_hostname_as_base_url_is_kept(self, tmp_path: Path) -> None:
        legacy = "https://cloudmanager.cloud.netapp.com"
        settings = ConsoleAPISettings(
            user_token=SecretStr("user-jwt"), base_url=legacy, base_api_path="/", timeout=15.0
        )
        client = _real_client(settings, tmp_path)
        wrapper = client._require_user()
        response = MagicMock()
        response.status_code = 200
        response.json.return_value = {"items": []}
        with patch.object(wrapper, "_execute_request_with_retry", return_value=response) as mocked:
            client.list_organizations()

        assert mocked.call_args.kwargs["url"] == f"{legacy}/v1/management/organizations"

    def test_tenancyv4_keys_are_full_paths(
        self, base_settings: ConsoleAPISettings, tmp_path: Path
    ) -> None:
        wrapper = _real_client(base_settings, tmp_path)._require_user()
        tenancyv4_paths = [
            path
            for path, item in wrapper.api_spec["paths"].items()
            for op in item.values()
            if isinstance(op, dict) and op.get("tags") == ["tenancyv4"]
        ]
        assert tenancyv4_paths
        assert all(p.startswith("/v1/management/") for p in tenancyv4_paths)

    def test_every_operation_first_server_is_bare_host(
        self, base_settings: ConsoleAPISettings, tmp_path: Path
    ) -> None:
        wrapper = _real_client(base_settings, tmp_path)._require_user()
        urls = [
            op["servers"][0]["url"]
            for item in wrapper.api_spec["paths"].values()
            for op in item.values()
            if isinstance(op, dict)
        ]
        assert urls
        assert set(urls) == {_HOST}

    def test_legacy_base_api_path_does_not_double_prefix(self, tmp_path: Path) -> None:
        settings = ConsoleAPISettings(
            user_token=SecretStr("user-jwt"),
            base_url=_HOST,
            base_api_path="/v1/management",
            timeout=15.0,
        )
        client = _real_client(settings, tmp_path)
        wrapper = client._require_user()
        response = MagicMock()
        response.status_code = 200
        response.json.return_value = {"items": []}
        with patch.object(wrapper, "_execute_request_with_retry", return_value=response) as mocked:
            client.list_organizations()

        assert mocked.call_args.kwargs["url"] == f"{_HOST}/v1/management/organizations"
