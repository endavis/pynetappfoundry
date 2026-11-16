"""Tests for pynetappfoundry.data.aiqum_backend.AiqumBackend.

AiqumBackend is live-only; no cache DB or network is touched.  The unit tests
mock the API client; the paging test drives a real ``AIQUMAPIClient`` over a
synthetic spec written to ``tmp_path`` with ``session.request`` mocked.
"""

from __future__ import annotations

import json
import logging
from collections.abc import Iterator
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.clients.aiqum.api import AIQUMAPIClient
from pynetappfoundry.clients.trust import HostTrustStore
from pynetappfoundry.core.config import ConfigurationError
from pynetappfoundry.core.models import AIQUMAPISettings
from pynetappfoundry.data._path_params import placeholders as _placeholders
from pynetappfoundry.data._routing import RoutingDecision
from pynetappfoundry.data.aiqum_backend import AiqumBackend
from pynetappfoundry.models._base import OntapModel


class FakeAiqumVolume(OntapModel):
    """Synthetic AIQUM model for backend tests."""

    key: str = ""
    name: str = ""


_LIVE = RoutingDecision(cache_fields=(), live_fields=("key", "name"))


def _mapping(**overrides: Any) -> TypeMapping:
    kwargs: dict[str, Any] = {
        "name": "FakeAiqumVolume",
        "model_class": FakeAiqumVolume,
        "api_endpoint": "/datacenter/storage/volumes",
        "api_type": "aiqum",
        "identifier_field": "key",
        "fields": (FieldMapping(cache_attr="key"), FieldMapping(cache_attr="name")),
    }
    kwargs.update(overrides)
    return TypeMapping(**kwargs)


@pytest.fixture
def mapping() -> Iterator[TypeMapping]:
    """Register the fake AIQUM mapping for one test."""
    m = _mapping()
    model_registry.register_mapping("FakeAiqumVolume", m)
    try:
        yield m
    finally:
        model_registry._mappings.pop("FakeAiqumVolume", None)
        model_registry._mappings_by_class.pop(FakeAiqumVolume, None)


def _backend() -> AiqumBackend:
    return AiqumBackend(MagicMock(name="Config"))


def _query(
    backend: AiqumBackend,
    mapping: TypeMapping,
    client: Any,
    filters: dict[str, Any] | None = None,
    decision: RoutingDecision = _LIVE,
    cluster: str = "aiqum1",
) -> list[FakeAiqumVolume]:
    with patch.object(backend, "_get_api_client", return_value=client):
        return backend.query(FakeAiqumVolume, mapping, decision, cluster, filters or {})


class TestEnvelope:
    """Envelope endpoints go through get_all_records."""

    def test_records_parsed_and_stamped(self, mapping: TypeMapping) -> None:
        client = MagicMock()
        client.get_all_records.return_value = {
            "records": [{"key": "k1", "name": "v1"}, {"key": "k2", "name": "v2"}]
        }
        results = _query(_backend(), mapping, client, {"svm.name": "vs1"})
        assert [r.key for r in results] == ["k1", "k2"]
        assert results[0].was_fetched("name")
        client.get_all_records.assert_called_once_with(
            "/datacenter/storage/volumes", "GET", query_params={"svm.name": "vs1"}
        )

    def test_missing_records_path_warns(
        self, mapping: TypeMapping, caplog: pytest.LogCaptureFixture
    ) -> None:
        client = MagicMock()
        client.get_all_records.return_value = {"other": []}
        with caplog.at_level(logging.WARNING):
            assert _query(_backend(), mapping, client) == []
        assert "FakeAiqumVolume" in caplog.text
        assert "not found" in caplog.text

    def test_non_list_records_warns(
        self, mapping: TypeMapping, caplog: pytest.LogCaptureFixture
    ) -> None:
        client = MagicMock()
        client.get_all_records.return_value = {"records": {"key": "k1"}}
        with caplog.at_level(logging.WARNING):
            assert _query(_backend(), mapping, client) == []
        assert "expected list" in caplog.text


class TestSingleton:
    """Singleton mappings wrap the dict response."""

    def test_dict_response_wrapped(self) -> None:
        m = _mapping(response_shape="singleton")
        client = MagicMock()
        client.call_endpoint.return_value = {"key": "k1", "name": "sys"}
        results = _query(_backend(), m, client, {"a": "b"})
        assert [r.name for r in results] == ["sys"]
        client.call_endpoint.assert_called_once_with(
            "/datacenter/storage/volumes", query_params={"a": "b"}
        )
        client.get_all_records.assert_not_called()

    def test_non_dict_response_warns(self, caplog: pytest.LogCaptureFixture) -> None:
        m = _mapping(response_shape="singleton")
        client = MagicMock()
        client.call_endpoint.return_value = "text"
        with caplog.at_level(logging.WARNING):
            assert _query(_backend(), m, client) == []
        assert "expected dict" in caplog.text
        client.get_all_records.assert_not_called()


class TestTargeting:
    """The cluster argument selects the [aiqums] instance."""

    def test_client_cached_per_name(self) -> None:
        config = MagicMock(name="Config")
        backend = AiqumBackend(config)
        with patch(
            "pynetappfoundry.clients.aiqum.api.AIQUMAPIClient",
            side_effect=lambda *a, **k: MagicMock(),
        ) as cls:
            first = backend._get_api_client("aiqum1")
            again = backend._get_api_client("aiqum1")
            other = backend._get_api_client("aiqum2")
        assert first is again
        assert other is not first
        assert [c.args for c in cls.call_args_list] == [("aiqum1", config), ("aiqum2", config)]

    def test_configuration_error_propagates(self, mapping: TypeMapping) -> None:
        backend = _backend()
        with (
            patch(
                "pynetappfoundry.clients.aiqum.api.AIQUMAPIClient",
                side_effect=ConfigurationError("No AIQUM named 'x'"),
            ),
            pytest.raises(ConfigurationError),
        ):
            backend.query(FakeAiqumVolume, mapping, _LIVE, "x", {})


class TestRejections:
    """Unsupported requests fail before any client is built."""

    def test_cache_only_decision(self, mapping: TypeMapping) -> None:
        decision = RoutingDecision(cache_fields=("name",), live_fields=())
        with pytest.raises(NotImplementedError, match="cache-only"):
            _query(_backend(), mapping, MagicMock(), decision=decision)

    def test_where_expressions(self, mapping: TypeMapping) -> None:
        with pytest.raises(NotImplementedError, match="where_expressions"):
            _backend().query(
                FakeAiqumVolume, mapping, _LIVE, "aiqum1", {}, where_expressions=("a > 1",)
            )

    def test_empty_live_fields(self, mapping: TypeMapping) -> None:
        client = MagicMock()
        decision = RoutingDecision(cache_fields=(), live_fields=())
        assert _query(_backend(), mapping, client, decision=decision) == []
        client.get_all_records.assert_not_called()

    @pytest.mark.parametrize("endpoint", ["/x/{key}", "/x/{key}/metrics"])
    def test_placeholder_endpoint_builds_no_client(self, endpoint: str) -> None:
        m = _mapping(api_endpoint=endpoint)
        backend = _backend()
        with (
            patch.object(backend, "_get_api_client") as get_client,
            pytest.raises(ValueError, match=r"\{key\}"),
        ):
            backend.query(FakeAiqumVolume, m, _LIVE, "aiqum1", {})
        get_client.assert_not_called()

    def test_path_params_rejected(self, mapping: TypeMapping) -> None:
        backend = _backend()
        with (
            patch.object(backend, "_get_api_client") as get_client,
            pytest.raises(ValueError, match="path_params"),
        ):
            backend.query(FakeAiqumVolume, mapping, _LIVE, "aiqum1", {}, path_params={"key": "k"})
        get_client.assert_not_called()


class TestRealPaging:
    """A real AIQUMAPIClient follows the HAL _links.next.href."""

    def test_two_pages_merged(self, tmp_path: Path, mapping: TypeMapping) -> None:
        schema_dir = tmp_path / "aiqum"
        schema_dir.mkdir()
        spec = {
            "swagger": "2.0",
            "basePath": "/api",
            "paths": {"/datacenter/storage/volumes": {"get": {"summary": "List volumes"}}},
        }
        (schema_dir / "all.json").write_text(json.dumps(spec))
        config = MagicMock()
        config.get_user.return_value = ("umadmin", "secret")
        config.get_schema_location.return_value = schema_dir
        config.get_trust_store.return_value = HostTrustStore(tmp_path / ".trust", lambda h, p: b"d")
        config.get_aiqum_api_settings.return_value = AIQUMAPISettings()
        config.data = {"aiqums": {"aiqum1": {"ip": "10.0.0.5"}}}

        def resp(data: dict[str, Any]) -> MagicMock:
            r = MagicMock()
            r.status_code = 200
            r.json.return_value = data
            r.raise_for_status.return_value = None
            return r

        page1 = resp(
            {
                "records": [{"key": "k1", "name": "v1"}],
                "_links": {"next": {"href": "/api/datacenter/storage/volumes?offset=1"}},
            }
        )
        page2 = resp({"records": [{"key": "k2", "name": "v2"}], "_links": {}})
        client = AIQUMAPIClient("aiqum1", config)
        try:
            with patch.object(client.session, "request", side_effect=[page1, page2]) as request:
                results = _query(_backend(), mapping, client)
            assert [r.key for r in results] == ["k1", "k2"]
            assert request.call_args_list[1].args[1] == (
                "https://10.0.0.5/api/datacenter/storage/volumes?offset=1"
            )
        finally:
            client.session.close()


_METRICS = "/datacenter/storage/volumes/{key}/metrics"


class TestPathParams:
    """Caller-supplied path_params fill endpoint placeholders (#1054)."""

    def test_capability_flag(self) -> None:
        assert AiqumBackend.supports_path_params is True

    def test_singleton_metrics_with_path_params(self) -> None:
        m = _mapping(api_endpoint=_METRICS, response_shape="singleton")
        client = MagicMock()
        client.call_endpoint.return_value = {"key": "k1", "name": "sys"}
        backend = _backend()
        with patch.object(backend, "_get_api_client", return_value=client):
            results = backend.query(
                FakeAiqumVolume, m, _LIVE, "aiqum1", {}, path_params={"key": "a,b:c=d/e"}
            )
        assert [r.name for r in results] == ["sys"]
        assert results[0].was_fetched("name")
        client.call_endpoint.assert_called_once_with(
            _METRICS, query_params={}, path_params={"key": "a%2Cb%3Ac%3Dd%2Fe"}
        )
        client.get_all_records.assert_not_called()

    def test_filters_go_to_query_params(self) -> None:
        m = _mapping(api_endpoint=_METRICS, response_shape="singleton")
        client = MagicMock()
        client.call_endpoint.return_value = {"key": "k1"}
        backend = _backend()
        with patch.object(backend, "_get_api_client", return_value=client):
            backend.query(
                FakeAiqumVolume, m, _LIVE, "aiqum1", {"interval": "1h"}, path_params={"key": "k"}
            )
        client.call_endpoint.assert_called_once_with(
            _METRICS, query_params={"interval": "1h"}, path_params={"key": "k"}
        )

    def test_list_mapping_with_placeholder(self) -> None:
        m = _mapping(api_endpoint="/x/{key}/items")
        client = MagicMock()
        client.get_all_records.return_value = {"records": [{"key": "k1", "name": "n"}]}
        backend = _backend()
        with patch.object(backend, "_get_api_client", return_value=client):
            results = backend.query(
                FakeAiqumVolume, m, _LIVE, "aiqum1", {}, path_params={"key": 12}
            )
        assert [r.key for r in results] == ["k1"]
        client.get_all_records.assert_called_once_with(
            "/x/{key}/items", "GET", query_params={}, path_params={"key": "12"}
        )

    @pytest.mark.parametrize(
        ("path_params", "match"),
        [
            ({}, r"\{key\}"),
            ({"other": "v"}, "unknown path_params key"),
            ({"key": "v", "other": "v"}, "unknown path_params key"),
            ({"key": ""}, "must not be"),
            ({"key": "."}, "must not be"),
            ({"key": ".."}, "must not be"),
        ],
    )
    def test_invalid_path_params_build_no_client(
        self, path_params: dict[str, Any], match: str
    ) -> None:
        m = _mapping(api_endpoint=_METRICS, response_shape="singleton")
        backend = _backend()
        with (
            patch.object(backend, "_get_api_client") as get_client,
            pytest.raises(ValueError, match=match),
        ):
            backend.query(FakeAiqumVolume, m, _LIVE, "aiqum1", {}, path_params=path_params)
        get_client.assert_not_called()

    def test_parent_mapping_without_path_params_names_key_and_followup(self) -> None:
        m = _mapping(
            api_endpoint=_METRICS,
            response_shape="singleton",
            parent_mapping="AiqumVolume",
            parent_id_field="key",
        )
        backend = _backend()
        with (
            patch.object(backend, "_get_api_client") as get_client,
            pytest.raises(ValueError, match=r"(?s)\{key\}.*path_params.*#1057"),
        ):
            backend.query(FakeAiqumVolume, m, _LIVE, "aiqum1", {})
        get_client.assert_not_called()

    def test_registry_sweep_placeholder_mappings_issue_one_request(self) -> None:
        swept = 0
        for name, reg in model_registry.mappings.items():
            if reg.api_type != "aiqum":
                continue
            names = _placeholders(reg)
            if not names:
                continue
            assert names == ["key"], name
            client = MagicMock()
            client.call_endpoint.return_value = {}
            client.get_all_records.return_value = {"records": []}
            backend = _backend()
            with patch.object(backend, "_get_api_client", return_value=client):
                backend.query(
                    reg.model_class,
                    reg,
                    RoutingDecision(cache_fields=(), live_fields=("key",)),
                    "aiqum1",
                    {},
                    path_params={"key": "k"},
                )
            assert client.call_endpoint.call_count + client.get_all_records.call_count == 1, name
            swept += 1
        assert swept > 0
