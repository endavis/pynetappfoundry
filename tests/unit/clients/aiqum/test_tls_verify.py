"""Optional CA validation for the AIQUM client (#1044). HTTP is mocked."""

from __future__ import annotations

import json
from collections.abc import Callable
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from pynetappfoundry.clients.aiqum.api import AIQUMAPIClient
from pynetappfoundry.clients.trust import FingerprintPinningAdapter, HostTrustStore
from pynetappfoundry.core.config import Config, ConfigurationError, resolve_tls_verify
from pynetappfoundry.core.models import AIQUMAPISettings, AIQUMConfig

NAME = "aiqum1"
SPEC: dict[str, Any] = {
    "swagger": "2.0",
    "basePath": "/api",
    "paths": {"/admin/datasources/clusters": {"get": {"summary": "List"}}},
}

MakeConfig = Callable[..., Config]


@pytest.fixture(autouse=True)
def _no_env_bundles(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("REQUESTS_CA_BUNDLE", raising=False)
    monkeypatch.delenv("CURL_CA_BUNDLE", raising=False)


def _resolve(config: Config, name: str = NAME) -> bool | str:
    return resolve_tls_verify(config, name, data_type="aiqums", settings_key="aiqumapi")


@pytest.fixture
def make_config(tmp_path: Path) -> MakeConfig:
    """Build a real Config from an aiqums entry body and an optional aiqumapi general body."""
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    schema_dir = config_dir / "apis" / "aiqum"
    schema_dir.mkdir(parents=True)
    (schema_dir / "all.json").write_text(json.dumps(SPEC))

    def make(entry: str = "", general: str | None = None, extra: str = "") -> Config:
        (config_dir / "aiqums.toml").write_text(
            f'[settings]\ntype = "data"\n\n[aiqums.{NAME}]\nip = "10.0.0.5"\n{entry}\n{extra}\n'
        )
        if general is not None:
            (config_dir / "aiqumapi.toml").write_text(f"[general]\n{general}\n")
        return Config(config_dir=str(config_dir), output_dir=str(tmp_path / "out"), script_name="t")

    return make


def _bundle(config: Config, name: str = "ca.pem") -> Path:
    path = config.config_dir / name
    path.write_text("placeholder")
    return path


def _toml_path(path: Path) -> str:
    return json.dumps(str(path))


class TestResolveAiqumTls:
    def test_no_tls_keys_is_false(self, make_config: MakeConfig) -> None:
        assert _resolve(make_config(general='base_api_path = "/api"')) is False

    def test_no_aiqumapi_toml_is_false(self, make_config: MakeConfig) -> None:
        assert _resolve(make_config()) is False

    def test_global_verify_true(self, make_config: MakeConfig) -> None:
        assert _resolve(make_config(general="verify_ssl = true")) is True

    def test_global_ca_bundle_absolute(self, make_config: MakeConfig) -> None:
        config = make_config(general='ca_bundle = "x"')
        bundle = _bundle(config)
        config.settings["aiqumapi"]["general"]["ca_bundle"] = str(bundle)
        assert _resolve(config) == str(bundle)

    def test_global_ca_bundle_relative_to_config_dir(self, make_config: MakeConfig) -> None:
        config = make_config(general='ca_bundle = "ca.pem"')
        bundle = _bundle(config)
        assert _resolve(config) == str(bundle)

    def test_entry_ca_bundle_beats_global_verify_false(self, make_config: MakeConfig) -> None:
        config = make_config(entry='ca_bundle = "ca.pem"', general="verify_ssl = false")
        bundle = _bundle(config)
        assert _resolve(config) == str(bundle)

    def test_entry_verify_false_beats_global_bundle(self, make_config: MakeConfig) -> None:
        config = make_config(entry="verify_ssl = false", general='ca_bundle = "ca.pem"')
        _bundle(config)
        assert _resolve(config) is False

    def test_entry_true_beats_global_false(self, make_config: MakeConfig) -> None:
        config = make_config(entry="verify_ssl = true", general="verify_ssl = false")
        assert _resolve(config) is True

    def test_invalid_global_bundle_overridden_by_entry(self, make_config: MakeConfig) -> None:
        config = make_config(entry="verify_ssl = true", general='ca_bundle = "missing.pem"')
        assert _resolve(config) is True

    def test_missing_entry_bundle_names_key(self, make_config: MakeConfig) -> None:
        config = make_config(entry='ca_bundle = "missing.pem"')
        with pytest.raises(ConfigurationError, match=r"aiqums\.aiqum1\.ca_bundle"):
            _resolve(config)

    def test_missing_global_bundle_names_key_and_instance(self, make_config: MakeConfig) -> None:
        config = make_config(general='ca_bundle = "missing.pem"')
        with pytest.raises(ConfigurationError) as exc:
            _resolve(config)
        assert "aiqumapi.general.ca_bundle" in str(exc.value)
        assert "(aiqum 'aiqum1')" in str(exc.value)

    def test_entry_verify_ssl_string_raises(self, make_config: MakeConfig) -> None:
        config = make_config(entry='verify_ssl = "yes"')
        with pytest.raises(ConfigurationError, match=r"aiqums\.aiqum1\.verify_ssl"):
            _resolve(config)

    def test_bundle_with_verify_false_raises(self, make_config: MakeConfig) -> None:
        config = make_config(entry='verify_ssl = false\nca_bundle = "ca.pem"')
        with pytest.raises(ConfigurationError, match="remove one of them"):
            _resolve(config)

    def test_ontap_keys_ignored_for_aiqum(self, make_config: MakeConfig) -> None:
        config = make_config()
        config.settings["ontapapi"] = {"general": {"verify_ssl": True}}
        config.data.setdefault("clusters", {})[NAME] = {"verify_ssl": True}
        assert _resolve(config) is False

    def test_aiqum_keys_ignored_for_ontap(self, make_config: MakeConfig) -> None:
        config = make_config(entry="verify_ssl = true", general="verify_ssl = true")
        config.data.setdefault("clusters", {})[NAME] = {"ip": "1.2.3.4"}
        assert resolve_tls_verify(config, NAME) is False


def _client(config: Config, tmp_path: Path) -> tuple[AIQUMAPIClient, HostTrustStore, list[Any]]:
    fetches: list[Any] = []

    def fetcher(host: str, port: int) -> bytes:
        fetches.append((host, port))
        return b"der"

    store = HostTrustStore(tmp_path / ".trust", fetcher)
    config._trust_store = store
    with patch.object(config, "get_user", return_value=("umadmin", "secret")):
        return AIQUMAPIClient(NAME, config), store, fetches


class TestAiqumClientTls:
    def test_default_is_false_and_pinned(self, make_config: MakeConfig, tmp_path: Path) -> None:
        client, store, fetches = _client(make_config(general='base_api_path = "/api"'), tmp_path)
        assert client.verify_ssl is False
        assert store.tls.get_fingerprint("10.0.0.5", 443) is not None
        assert fetches == [("10.0.0.5", 443)]
        client.session.close()

    def test_verify_true_keeps_adapter_and_makes_no_pin(
        self, make_config: MakeConfig, tmp_path: Path
    ) -> None:
        client, store, fetches = _client(
            make_config(entry="verify_ssl = true", general='base_api_path = "/api"'), tmp_path
        )
        assert client.verify_ssl is True
        assert isinstance(
            client.session.get_adapter("https://10.0.0.5/api"), FingerprintPinningAdapter
        )
        assert fetches == []
        assert not store.tls.path.exists()
        client.session.close()

    def test_ca_bundle_is_passed_to_requests(self, make_config: MakeConfig, tmp_path: Path) -> None:
        config = make_config(entry='ca_bundle = "ca.pem"', general='base_api_path = "/api"')
        bundle = _bundle(config)
        client, _store, fetches = _client(config, tmp_path)
        assert client.verify_ssl == str(bundle)
        resp = MagicMock()
        resp.status_code = 200
        resp.json.return_value = {}
        resp.raise_for_status.return_value = None
        with patch.object(client.session, "request", return_value=resp) as mock_request:
            client.call_endpoint("/admin/datasources/clusters")
        assert mock_request.call_args.kwargs["verify"] == str(bundle)
        assert fetches == []
        client.session.close()

    @pytest.mark.parametrize("entry", ['ca_bundle = "missing.pem"', 'verify_ssl = "maybe"'])
    def test_bad_tls_raises_before_get_user(self, make_config: MakeConfig, entry: str) -> None:
        config = make_config(entry=entry)
        with patch.object(config, "get_user") as get_user, pytest.raises(ConfigurationError):
            AIQUMAPIClient(NAME, config)
        get_user.assert_not_called()


class TestModels:
    def test_aiqum_config_defaults(self) -> None:
        cfg = AIQUMConfig.model_validate({"name": NAME})
        assert cfg.verify_ssl is None
        assert cfg.ca_bundle is None

    def test_aiqum_config_values(self) -> None:
        cfg = AIQUMConfig.model_validate({"name": NAME, "verify_ssl": True, "ca_bundle": "a.pem"})
        assert cfg.verify_ssl is True
        assert cfg.ca_bundle == "a.pem"

    def test_settings_defaults(self) -> None:
        s = AIQUMAPISettings()
        assert s.verify_ssl is False
        assert s.ca_bundle is None

    def test_settings_values(self) -> None:
        s = AIQUMAPISettings.model_validate({"verify_ssl": True, "ca_bundle": "a.pem"})
        assert s.verify_ssl is True
        assert s.ca_bundle == "a.pem"
