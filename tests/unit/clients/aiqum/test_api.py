"""Tests for AIQUMAPIClient (mocked HTTP, synthetic spec)."""

from __future__ import annotations

import base64
import hashlib
import json
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import pytest

import pynetappfoundry
import pynetappfoundry.clients
from pynetappfoundry.clients.aiqum.api import AIQUMAPIClient
from pynetappfoundry.clients.trust import FingerprintPinningAdapter, HostTrustStore
from pynetappfoundry.core.config import Config, ConfigurationError
from pynetappfoundry.core.models import AIQUMAPISettings

SPEC: dict[str, Any] = {
    "swagger": "2.0",
    "basePath": "/api",
    "paths": {
        "/admin/datasources/clusters": {
            "get": {"summary": "List data sources"},
            "post": {"summary": "Add a data source"},
        },
        "/admin/datasources/clusters/{key}": {
            "delete": {
                "summary": "Remove a data source",
                "parameters": [{"name": "key", "in": "path", "type": "string", "required": True}],
            },
        },
    },
}


@dataclass
class Built:
    """A built client with its collaborators."""

    client: AIQUMAPIClient
    config: MagicMock
    store: HostTrustStore
    fetches: list[tuple[str, int]]
    tmp_path: Path


def _response(data: dict[str, Any]) -> MagicMock:
    resp = MagicMock()
    resp.status_code = 200
    resp.json.return_value = data
    resp.raise_for_status.return_value = None
    return resp


@pytest.fixture
def built(tmp_path: Path) -> Iterator[Built]:
    schema_dir = tmp_path / "aiqum"
    schema_dir.mkdir()
    (schema_dir / "all.json").write_text(json.dumps(SPEC))
    fetches: list[tuple[str, int]] = []

    def fetcher(host: str, port: int) -> bytes:
        fetches.append((host, port))
        return b"der"

    store = HostTrustStore(tmp_path / ".trust", fetcher)
    config = MagicMock()
    config.get_user.return_value = ("umadmin", "secret")
    config.get_schema_location.return_value = schema_dir
    config.get_trust_store.return_value = store
    config.get_aiqum_api_settings.return_value = AIQUMAPISettings()
    config.data = {"aiqums": {"aiqum1": {"ip": "10.0.0.5"}}}
    client = AIQUMAPIClient("aiqum1", config)
    yield Built(client, config, store, fetches, tmp_path)
    client.session.close()


class TestAIQUMAPIClient:
    """Construction, auth, URLs and paging."""

    def test_basic_auth_header(self, built: Built) -> None:
        expected = base64.b64encode(b"umadmin:secret").decode()
        assert built.client.session.headers["authorization"] == f"Basic {expected}"
        built.config.get_user.assert_called_once_with("aiqums", "aiqum1")
        built.config.get_schema_location.assert_called_once_with("aiqum")

    def test_url_built_from_ip_and_base_path(self, built: Built) -> None:
        with patch.object(built.client.session, "request") as mock_request:
            mock_request.return_value = _response({"records": []})
            built.client.call_endpoint("/admin/datasources/clusters")
        assert mock_request.call_args.args[1] == "https://10.0.0.5/api/admin/datasources/clusters"

    def test_hal_paging_merges_records(self, built: Built) -> None:
        page1 = {
            "records": [{"key": "a"}],
            "num_records": 1,
            "_links": {"next": {"href": "/api/admin/datasources/clusters?start=2"}},
        }
        page2 = {"records": [{"key": "b"}], "num_records": 1}
        with patch.object(built.client.session, "request") as mock_request:
            mock_request.side_effect = [_response(page1), _response(page2)]
            result = built.client.get_all_records("/admin/datasources/clusters", "GET")
        assert result["records"] == [{"key": "a"}, {"key": "b"}]
        assert result["num_records"] == 2
        assert "_links" not in result
        assert mock_request.call_args_list[1].args[1] == (
            "https://10.0.0.5/api/admin/datasources/clusters?start=2"
        )

    def test_post_sends_json_body(self, built: Built) -> None:
        body = {"address": "10.1.1.1"}
        with patch.object(built.client.session, "request") as mock_request:
            mock_request.return_value = _response({})
            built.client.call_endpoint("/admin/datasources/clusters", method="POST", body=body)
        assert mock_request.call_args.args[0] == "POST"
        assert mock_request.call_args.kwargs["json"] == body

    def test_delete_resolves_path_param(self, built: Built) -> None:
        with patch.object(built.client.session, "request") as mock_request:
            mock_request.return_value = _response({})
            built.client.call_endpoint(
                "/admin/datasources/clusters/{key}", method="DELETE", path_params={"key": "k1"}
            )
        assert mock_request.call_args.args[0] == "DELETE"
        url = "https://10.0.0.5/api/admin/datasources/clusters/k1"
        assert mock_request.call_args.args[1] == url

    def test_tls_pin_only(self, built: Built) -> None:
        client = built.client
        adapter = client.session.get_adapter("https://10.0.0.5/api")
        assert isinstance(adapter, FingerprintPinningAdapter)
        assert client.verify_ssl is False
        assert adapter._store is built.store.tls
        expected = hashlib.sha256(b"der").hexdigest()
        assert built.store.tls.get_fingerprint("10.0.0.5", 443) == expected
        assert built.fetches == [("10.0.0.5", 443)]
        recorded = json.loads(built.store.tls.path.read_text())["hosts"]
        assert "10.0.0.5:443" in recorded


class TestAIQUMAPIClientErrors:
    """Configuration failures happen before credentials are read."""

    def test_missing_settings_propagates(self, built: Built) -> None:
        built.config.get_aiqum_api_settings.side_effect = ConfigurationError("no aiqumapi")
        built.config.get_user.reset_mock()
        with pytest.raises(ConfigurationError, match="no aiqumapi"):
            AIQUMAPIClient("aiqum1", built.config)
        built.config.get_user.assert_not_called()

    def test_missing_aiqumapi_toml_end_to_end(self, tmp_path: Path) -> None:
        config_dir = tmp_path / "config"
        config_dir.mkdir()
        (config_dir / "aiqums.toml").write_text(
            '[settings]\ntype = "data"\n\n[aiqums.aiqum1]\nip = "10.0.0.5"\n'
        )
        config = Config(
            config_dir=str(config_dir), output_dir=str(tmp_path / "out"), script_name="t"
        )
        with pytest.raises(ConfigurationError):
            AIQUMAPIClient("aiqum1", config)

    def test_unknown_name(self, built: Built) -> None:
        built.config.get_user.reset_mock()
        with pytest.raises(ConfigurationError, match="nope"):
            AIQUMAPIClient("nope", built.config)
        built.config.get_user.assert_not_called()

    def test_entry_without_ip(self, built: Built) -> None:
        built.config.data = {"aiqums": {"aiqum2": {"env": "dev"}}}
        built.config.get_user.reset_mock()
        with pytest.raises(ConfigurationError, match=r"aiqums\.aiqum2\.ip"):
            AIQUMAPIClient("aiqum2", built.config)
        built.config.get_user.assert_not_called()


def test_exports() -> None:
    assert pynetappfoundry.clients.AIQUMAPIClient is AIQUMAPIClient
    assert pynetappfoundry.AIQUMAPIClient is AIQUMAPIClient
