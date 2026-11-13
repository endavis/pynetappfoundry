"""Tests for ConsoleAgentClient (#1001, ADR-0019)."""

from __future__ import annotations

import inspect
import json
import logging
from collections.abc import Iterator
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch
from urllib.parse import parse_qs, urlsplit

import pytest
import requests
import yaml
from pydantic import SecretStr

import pynetappfoundry.clients as clients_pkg
import pynetappfoundry.clients.console as console_pkg
from pynetappfoundry.clients.console.agent import AGENT_ID_HEADER, ConsoleAgentClient
from pynetappfoundry.clients.console.auth import ConsoleAuthError
from pynetappfoundry.core.models import ConsoleAPISettings

REAL_HOST = "https://api.bluexp.netapp.com"
AGENT_ID = "agent-placeholder-0001"
PASSWORD = "placeholder-password"
CLIENT_SECRET = "placeholder-client-secret"
USER_TOKEN = "placeholder-user-token"
SERVICE_TOKEN = "placeholder-service-token"

_ROOT = Path(__file__).parents[4]
_REAL_SPEC = _ROOT / "tools/console_openapi/generated/console_openapi.yaml"
_FIXTURES = _ROOT / "tests/fixtures/console_models"
_LIST_URL = f"{REAL_HOST}/occm/api/onprem/working-environments"


def _settings(**overrides: Any) -> ConsoleAPISettings:
    values: dict[str, Any] = {"base_url": REAL_HOST, "base_api_path": "/", "timeout": 15.0}
    values.update(overrides)
    return ConsoleAPISettings(**values)


def _config(settings: ConsoleAPISettings, schema_dir: Path) -> MagicMock:
    config = MagicMock()
    config.get_console_api_settings.return_value = settings
    config.get_schema_location.return_value = schema_dir
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


def _response(status: int = 200, body: Any = None, url: str = REAL_HOST) -> requests.Response:
    resp = requests.Response()
    resp.status_code = status
    resp.url = url
    resp._content = b"" if body is None else json.dumps(body).encode()
    return resp


class FakeProvider:
    """Token provider returning queued tokens and recording invalidations."""

    def __init__(self, *tokens: str) -> None:
        self._tokens = list(tokens)
        self.invalidated: list[str] = []

    def get_token(self) -> str:
        return self._tokens[0]

    def invalidate(self, token: str) -> None:
        self.invalidated.append(token)
        if len(self._tokens) > 1:
            self._tokens.pop(0)


@pytest.fixture(scope="module")
def schema_dir(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """Directory holding the real combined Console spec."""
    path = tmp_path_factory.mktemp("schema")
    spec = yaml.safe_load(_REAL_SPEC.read_text(encoding="utf-8"))
    (path / "console_openapi.yaml").write_text(json.dumps(spec), encoding="utf-8")
    return path


@pytest.fixture
def wrapper_factory(monkeypatch: pytest.MonkeyPatch) -> MagicMock:
    """Patch APIWrapper; each construction returns a mock."""
    factory = MagicMock(side_effect=lambda **kw: MagicMock(name=kw.get("name")))
    monkeypatch.setattr("pynetappfoundry.clients.console.agent.APIWrapper", factory)
    return factory


@pytest.fixture
def client(schema_dir: Path) -> ConsoleAgentClient:
    return ConsoleAgentClient(_config(_settings(user_token=USER_TOKEN), schema_dir), AGENT_ID)


@pytest.fixture
def request_mock(client: ConsoleAgentClient) -> Iterator[MagicMock]:
    with patch.object(client._wrapper.session, "request") as mocked:
        mocked.return_value = _response(200, [])
        yield mocked


def test_both_import_paths() -> None:
    assert console_pkg.ConsoleAgentClient is ConsoleAgentClient
    assert clients_pkg.ConsoleAgentClient is ConsoleAgentClient
    assert "ConsoleAgentClient" in console_pkg.__all__
    assert "ConsoleAgentClient" in clients_pkg.__all__


class TestConstruction:
    def test_user_token(self, wrapper_factory: MagicMock, tmp_path: Path) -> None:
        ConsoleAgentClient(_config(_settings(user_token=USER_TOKEN), tmp_path), AGENT_ID)
        kwargs = wrapper_factory.call_args.kwargs
        assert kwargs["auth_header"] == {
            AGENT_ID_HEADER: AGENT_ID,
            "Authorization": f"Bearer {USER_TOKEN}",
        }
        assert kwargs["use_operation_servers"] is True
        assert kwargs["name"] == "console-agent"

    def test_service_token(self, wrapper_factory: MagicMock, tmp_path: Path) -> None:
        ConsoleAgentClient(_config(_settings(service_token=SERVICE_TOKEN), tmp_path), AGENT_ID)
        assert wrapper_factory.call_args.kwargs["auth_header"] == {
            AGENT_ID_HEADER: AGENT_ID,
            "Authorization": f"Bearer {SERVICE_TOKEN}",
        }

    def test_client_credentials(self, wrapper_factory: MagicMock, tmp_path: Path) -> None:
        session = _token_session("tok-1")
        ConsoleAgentClient(
            _config(_settings(client_id="placeholder-id", client_secret=CLIENT_SECRET), tmp_path),
            AGENT_ID,
            token_session=session,
        )
        assert wrapper_factory.call_args.kwargs["auth_header"] == {AGENT_ID_HEADER: AGENT_ID}
        assert session.post.call_count == 1

    def test_bad_credentials_raise_at_construction(
        self, wrapper_factory: MagicMock, tmp_path: Path
    ) -> None:
        session = MagicMock()
        resp = MagicMock()
        resp.status_code = 401
        resp.json.return_value = {"error": "access_denied"}
        session.post.return_value = resp
        with pytest.raises(ConsoleAuthError) as exc_info:
            ConsoleAgentClient(
                _config(
                    _settings(client_id="placeholder-id", client_secret=CLIENT_SECRET), tmp_path
                ),
                AGENT_ID,
                token_session=session,
            )
        assert CLIENT_SECRET not in str(exc_info.value)

    def test_injected_provider_beats_user_token(
        self, wrapper_factory: MagicMock, tmp_path: Path
    ) -> None:
        client = ConsoleAgentClient(
            _config(_settings(user_token=USER_TOKEN), tmp_path),
            AGENT_ID,
            token_provider=FakeProvider("tok-1"),
        )
        assert wrapper_factory.call_args.kwargs["auth_header"] == {AGENT_ID_HEADER: AGENT_ID}
        assert client._provider is not None

    @pytest.mark.parametrize("agent_id", ["", "   "])
    def test_blank_agent_id_rejected(
        self, wrapper_factory: MagicMock, tmp_path: Path, agent_id: str
    ) -> None:
        with pytest.raises(ValueError, match="agent_id"):
            ConsoleAgentClient(_config(_settings(user_token=USER_TOKEN), tmp_path), agent_id)


class TestReads:
    def test_list_url_headers_and_models(
        self, client: ConsoleAgentClient, request_mock: MagicMock
    ) -> None:
        item = json.loads((_FIXTURES / "onprem_working_environment.json").read_text())
        request_mock.return_value = _response(200, [item])
        result = client.list_onprem_working_environments()

        args = request_mock.call_args
        assert args.args == ("GET", _LIST_URL)
        assert args.kwargs["headers"][AGENT_ID_HEADER] == AGENT_ID
        assert args.kwargs["headers"]["Authorization"] == f"Bearer {USER_TOKEN}"
        assert len(result) == 1
        assert result[0].publicId == "we-placeholder-0001"

    def test_fields_and_tenant_query(
        self, client: ConsoleAgentClient, request_mock: MagicMock
    ) -> None:
        client.list_onprem_working_environments(fields=["a", "b"], tenant_id="tenant-1")
        query = parse_qs(urlsplit(request_mock.call_args.args[1]).query)
        assert query == {"fields": ["a,b"], "tenantId": ["tenant-1"]}

    def test_fields_string_passthrough(
        self, client: ConsoleAgentClient, request_mock: MagicMock
    ) -> None:
        request_mock.return_value = _response(200, {})
        client.get_onprem_working_environment("we-1", fields="ontapClusterProperties")
        query = parse_qs(urlsplit(request_mock.call_args.args[1]).query)
        assert query == {"fields": ["ontapClusterProperties"]}

    def test_non_array_list_raises_without_content(
        self, client: ConsoleAgentClient, request_mock: MagicMock
    ) -> None:
        request_mock.return_value = _response(200, {"secretish": "response-content-marker"})
        with pytest.raises(TypeError) as exc_info:
            client.list_onprem_working_environments()
        assert "response-content-marker" not in str(exc_info.value)
        assert "dict" in str(exc_info.value)

    def test_get_encodes_path_parameter(
        self, client: ConsoleAgentClient, request_mock: MagicMock
    ) -> None:
        request_mock.return_value = _response(200, {})
        client.get_onprem_working_environment("a/b")
        assert request_mock.call_args.args[1].endswith("/working-environments/a%2Fb")

    def test_about(self, client: ConsoleAgentClient, request_mock: MagicMock) -> None:
        request_mock.return_value = _response(
            200, json.loads((_FIXTURES / "occm_system_about.json").read_text())
        )
        about = client.about()
        assert about.agentId == AGENT_ID
        assert request_mock.call_args.args[1] == f"{REAL_HOST}/occm/api/occm/system/about"


class TestMutations:
    def _add(self, client: ConsoleAgentClient, **kwargs: Any) -> Any:
        params: dict[str, Any] = {
            "tenant_id": "tenant-1",
            "cluster_address": "cluster.example.test",
            "cluster_user_name": "admin",
            "cluster_password": PASSWORD,
        }
        params.update(kwargs)
        return client.add_onprem_working_environment(**params)

    def test_add_minimal_body(self, client: ConsoleAgentClient, request_mock: MagicMock) -> None:
        request_mock.return_value = _response(200, {"publicId": "we-1", "name": "n"})
        result = self._add(client)
        assert request_mock.call_args.args == ("POST", _LIST_URL)
        assert request_mock.call_args.kwargs["json"] == {
            "tenantId": "tenant-1",
            "clusterAddress": "cluster.example.test",
            "clusterUserName": "admin",
            "clusterPassword": PASSWORD,
            "location": "ON_PREM",
        }
        assert result.publicId == "we-1"

    def test_add_with_name_description_and_secretstr(
        self, client: ConsoleAgentClient, request_mock: MagicMock
    ) -> None:
        request_mock.return_value = _response(200, {"publicId": "we-1"})
        self._add(client, cluster_password=SecretStr(PASSWORD), name="n", description="d")
        body = request_mock.call_args.kwargs["json"]
        assert body["clusterPassword"] == PASSWORD
        assert body["name"] == "n"
        assert body["description"] == "d"

    @pytest.mark.parametrize("op", ["add", "delete"])
    def test_mutations_not_retried_on_503(
        self, client: ConsoleAgentClient, request_mock: MagicMock, op: str
    ) -> None:
        request_mock.return_value = _response(503, {})
        with pytest.raises(requests.HTTPError):
            if op == "add":
                self._add(client)
            else:
                client.delete_onprem_working_environment("we-1")
        assert request_mock.call_count == 1

    def test_add_invalid_input_hides_password(
        self, client: ConsoleAgentClient, request_mock: MagicMock
    ) -> None:
        with pytest.raises(ValueError, match="tenantId") as exc_info:
            self._add(client, tenant_id=None)
        err = exc_info.value
        assert PASSWORD not in str(err)
        assert err.__cause__ is None
        assert PASSWORD not in repr(err.__context__)
        assert request_mock.call_count == 0

    def test_delete(self, client: ConsoleAgentClient, request_mock: MagicMock) -> None:
        request_mock.return_value = _response(200)
        client.delete_onprem_working_environment("we-1")
        assert inspect.signature(client.delete_onprem_working_environment).return_annotation in (
            None,
            "None",
        )
        assert request_mock.call_args.args == ("DELETE", f"{_LIST_URL}/we-1")

    @pytest.mark.parametrize("status", [200, 400])
    def test_debug_logging_hides_secrets(
        self,
        client: ConsoleAgentClient,
        request_mock: MagicMock,
        caplog: pytest.LogCaptureFixture,
        status: int,
    ) -> None:
        request_mock.return_value = _response(status, {"publicId": "we-1"})
        with caplog.at_level(logging.DEBUG):
            try:
                self._add(client)
            except requests.HTTPError:
                assert status == 400
        assert PASSWORD not in caplog.text
        assert USER_TOKEN not in caplog.text
        assert CLIENT_SECRET not in caplog.text
        assert "***" in caplog.text


class TestProviderHandling:
    def _client(self, schema_dir: Path, provider: FakeProvider) -> ConsoleAgentClient:
        return ConsoleAgentClient(
            _config(_settings(user_token=USER_TOKEN), schema_dir),
            AGENT_ID,
            token_provider=provider,
        )

    def test_401_then_200_refreshes_once(self, schema_dir: Path) -> None:
        provider = FakeProvider("old", "new")
        client = self._client(schema_dir, provider)
        with patch.object(client._wrapper.session, "request") as mocked:
            mocked.side_effect = [_response(401, {}), _response(200, [])]
            assert client.list_onprem_working_environments() == []
        assert provider.invalidated == ["old"]
        auths = [c.kwargs["headers"]["Authorization"] for c in mocked.call_args_list]
        assert auths == ["Bearer old", "Bearer new"]

    def test_two_401s_propagate(self, schema_dir: Path) -> None:
        client = self._client(schema_dir, FakeProvider("old", "new"))
        with patch.object(client._wrapper.session, "request") as mocked:
            mocked.side_effect = [_response(401, {}), _response(401, {})]
            with pytest.raises(requests.HTTPError):
                client.list_onprem_working_environments()
        assert mocked.call_count == 2

    def test_static_token_401_not_retried(
        self, client: ConsoleAgentClient, request_mock: MagicMock
    ) -> None:
        request_mock.return_value = _response(401, {})
        with pytest.raises(requests.HTTPError):
            client.list_onprem_working_environments()
        assert request_mock.call_count == 1


class TestConnectorLookup:
    """#734: get_connector and find_onprem_working_environment."""

    CLUSTER_UUID = "00000000-0000-0000-0000-000000000000"

    @staticmethod
    def _item() -> dict[str, Any]:
        result: dict[str, Any] = json.loads(
            (_FIXTURES / "onprem_working_environment.json").read_text()
        )
        return result

    def test_get_connector_maps_about(
        self, client: ConsoleAgentClient, request_mock: MagicMock
    ) -> None:
        about = json.loads((_FIXTURES / "occm_system_about.json").read_text())
        request_mock.return_value = _response(200, about)

        connector = client.get_connector()

        assert request_mock.call_args.args == ("GET", f"{REAL_HOST}/occm/api/occm/system/about")
        assert connector.agent_id == AGENT_ID
        assert "agent.example.test" not in connector.model_dump_json()

    def test_find_returns_match_and_sends_fields(
        self, client: ConsoleAgentClient, request_mock: MagicMock
    ) -> None:
        request_mock.return_value = _response(200, [self._item()])

        found = client.find_onprem_working_environment(self.CLUSTER_UUID)

        assert found is not None
        assert found.ontapClusterProperties is not None
        assert found.ontapClusterProperties.clusterUuid == self.CLUSTER_UUID
        query = parse_qs(urlsplit(request_mock.call_args.args[1]).query)
        assert query == {"fields": ["ontapClusterProperties"]}

    def test_find_returns_none_when_no_match(
        self, client: ConsoleAgentClient, request_mock: MagicMock
    ) -> None:
        request_mock.return_value = _response(200, [self._item()])
        other_uuid = "11111111-1111-1111-1111-111111111111"
        assert client.find_onprem_working_environment(other_uuid) is None

    def test_find_skips_items_without_cluster_properties(
        self, client: ConsoleAgentClient, request_mock: MagicMock
    ) -> None:
        item = self._item()
        del item["ontapClusterProperties"]
        request_mock.return_value = _response(200, [item])
        assert client.find_onprem_working_environment(self.CLUSTER_UUID) is None

    @pytest.mark.parametrize("cluster_uuid", ["", "  "])
    def test_find_blank_uuid_rejected(
        self, client: ConsoleAgentClient, request_mock: MagicMock, cluster_uuid: str
    ) -> None:
        with pytest.raises(ValueError, match="cluster_uuid"):
            client.find_onprem_working_environment(cluster_uuid)
        request_mock.assert_not_called()
