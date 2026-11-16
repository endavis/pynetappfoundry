"""Tests for fetching one AIQUM object by key (#1060).

A single ``{identifier_field: <str>}`` filter on a collection whose runtime spec
has ``<collection>/{key}`` is fetched from that item endpoint.  The unit tests
mock the API client; the URL test drives a real ``AIQUMAPIClient`` over a
synthetic spec with ``session.request`` mocked.
"""

from __future__ import annotations

import json
import logging
from collections.abc import Iterator
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch
from urllib.parse import quote

import pytest
import requests

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.clients.aiqum.api import AIQUMAPIClient
from pynetappfoundry.clients.trust import HostTrustStore
from pynetappfoundry.core.models import AIQUMAPISettings
from pynetappfoundry.data._routing import RoutingDecision
from pynetappfoundry.data.aiqum_backend import AiqumBackend
from pynetappfoundry.models._base import OntapModel

_COLLECTION = "/datacenter/storage/volumes"
_ITEM = "/datacenter/storage/volumes/{key}"
_LIVE = RoutingDecision(cache_fields=(), live_fields=("key", "name"))
_REAL_KEY = "a1b2,c-d:e=f/g"


class FakeKeyVolume(OntapModel):
    """Synthetic AIQUM model for item-route tests."""

    key: str = ""
    name: str = ""


def _mapping(**overrides: Any) -> TypeMapping:
    kwargs: dict[str, Any] = {
        "name": "FakeKeyVolume",
        "model_class": FakeKeyVolume,
        "api_endpoint": _COLLECTION,
        "api_type": "aiqum",
        "identifier_field": "key",
        "fields": (FieldMapping(cache_attr="key"), FieldMapping(cache_attr="name")),
    }
    kwargs.update(overrides)
    return TypeMapping(**kwargs)


@pytest.fixture
def mapping() -> Iterator[TypeMapping]:
    """Register the fake mapping for one test."""
    m = _mapping()
    model_registry.register_mapping("FakeKeyVolume", m)
    try:
        yield m
    finally:
        model_registry._mappings.pop("FakeKeyVolume", None)
        model_registry._mappings_by_class.pop(FakeKeyVolume, None)


def _client(spec: Any = None) -> MagicMock:
    client = MagicMock()
    client.api_spec = (
        {"paths": {_COLLECTION: {"get": {}}, _ITEM: {"get": {}}}} if spec is None else spec
    )
    return client


def _query(
    mapping: TypeMapping, client: Any, filters: dict[str, Any], **kwargs: Any
) -> list[FakeKeyVolume]:
    backend = AiqumBackend(MagicMock(name="Config"))
    with patch.object(backend, "_get_api_client", return_value=client):
        return backend.query(FakeKeyVolume, mapping, _LIVE, "aiqum1", filters, **kwargs)


def _http_error(status: int | None) -> requests.HTTPError:
    response = None
    if status is not None:
        response = MagicMock()
        response.status_code = status
    return requests.HTTPError(f"HTTP {status}", response=response)


class TestItemRoute:
    """A single identifier filter goes to the item endpoint."""

    def test_item_endpoint_called_once(self, mapping: TypeMapping) -> None:
        client = _client()
        client.call_endpoint.return_value = {"key": "k1", "name": "v1", "_links": {}}
        results = _query(mapping, client, {"key": "k1"})
        assert [(r.key, r.name) for r in results] == [("k1", "v1")]
        assert results[0].was_fetched("name")
        client.call_endpoint.assert_called_once_with(_ITEM, path_params={"key": "k1"})
        client.get_all_records.assert_not_called()

    def test_key_is_percent_encoded(self, mapping: TypeMapping) -> None:
        client = _client()
        client.call_endpoint.return_value = {"key": _REAL_KEY, "name": "v"}
        _query(mapping, client, {"key": _REAL_KEY})
        client.call_endpoint.assert_called_once_with(
            _ITEM, path_params={"key": quote(_REAL_KEY, safe="")}
        )
        assert "/" not in quote(_REAL_KEY, safe="")

    def test_404_returns_empty(self, mapping: TypeMapping) -> None:
        client = _client()
        client.call_endpoint.side_effect = _http_error(404)
        assert _query(mapping, client, {"key": "nope"}) == []
        client.get_all_records.assert_not_called()

    @pytest.mark.parametrize("status", [500, None])
    def test_other_http_errors_propagate(self, mapping: TypeMapping, status: int | None) -> None:
        client = _client()
        client.call_endpoint.side_effect = _http_error(status)
        with pytest.raises(requests.HTTPError):
            _query(mapping, client, {"key": "k1"})

    def test_non_dict_response_warns(
        self, mapping: TypeMapping, caplog: pytest.LogCaptureFixture
    ) -> None:
        client = _client()
        client.call_endpoint.return_value = "text"
        with caplog.at_level(logging.WARNING):
            assert _query(mapping, client, {"key": "k1"}) == []
        assert "expected dict" in caplog.text


class TestFallsBackToCollection:
    """Anything that is not one plain identifier lookup uses the collection."""

    @staticmethod
    def _assert_collection(client: MagicMock, filters: dict[str, Any]) -> None:
        client.call_endpoint.assert_not_called()
        client.get_all_records.assert_called_once_with(_COLLECTION, "GET", query_params=filters)

    @pytest.mark.parametrize(
        "spec",
        [
            {"paths": {_COLLECTION: {"get": {}}}},
            {"paths": {_COLLECTION: {"get": {}}, _ITEM: {"delete": {}}}},
            {"paths": {_COLLECTION: {"get": {}}, _ITEM: None}},
            {"paths": None},
            {},
            "not-a-dict",
        ],
    )
    def test_spec_without_get_item(self, mapping: TypeMapping, spec: Any) -> None:
        client = _client(spec)
        client.get_all_records.return_value = {"records": [{"key": "k1", "name": "n"}]}
        results = _query(mapping, client, {"key": "k1"})
        assert [r.key for r in results] == ["k1"]
        self._assert_collection(client, {"key": "k1"})

    @pytest.mark.parametrize(
        "filters",
        [
            {"key": "k1", "svm.name": "vs1"},
            {"svm.name": "vs1"},
            {"key": 5},
            {"key": ["a"]},
            {"key": ""},
            {"key": "."},
            {"key": ".."},
            {},
        ],
    )
    def test_unsuitable_filters(self, mapping: TypeMapping, filters: dict[str, Any]) -> None:
        client = _client()
        client.get_all_records.return_value = {"records": []}
        _query(mapping, client, filters)
        self._assert_collection(client, filters)

    @pytest.mark.parametrize("identifier", [("key", "name"), None])
    def test_non_str_identifier_field(self, identifier: Any) -> None:
        m = _mapping(identifier_field=identifier)
        client = _client()
        client.get_all_records.return_value = {"records": []}
        _query(m, client, {"key": "k1"})
        self._assert_collection(client, {"key": "k1"})

    def test_placeholder_mapping_with_path_params_unchanged(self) -> None:
        metrics = "/datacenter/storage/volumes/{key}/metrics"
        m = _mapping(api_endpoint=metrics)
        client = _client({"paths": {metrics: {"get": {}}, f"{metrics}/{{key}}": {"get": {}}}})
        client.get_all_records.return_value = {"records": []}
        _query(m, client, {"key": "k1"}, path_params={"key": "p"})
        client.call_endpoint.assert_not_called()
        client.get_all_records.assert_called_once_with(
            metrics, "GET", query_params={"key": "k1"}, path_params={"key": "p"}
        )

    def test_path_params_on_plain_collection_still_rejected(self, mapping: TypeMapping) -> None:
        client = _client()
        with pytest.raises(ValueError, match="path_params"):
            _query(mapping, client, {"key": "k1"}, path_params={"key": "p"})
        client.call_endpoint.assert_not_called()


class TestRealClientUrl:
    """A real AIQUMAPIClient requests the encoded item URL with no query string."""

    def test_url_and_bare_object(self, tmp_path: Path, mapping: TypeMapping) -> None:
        schema_dir = tmp_path / "aiqum"
        schema_dir.mkdir()
        spec = {
            "swagger": "2.0",
            "basePath": "/api",
            "paths": {
                _COLLECTION: {"get": {"summary": "List volumes"}},
                _ITEM: {"get": {"summary": "Get a volume"}},
            },
        }
        (schema_dir / "all.json").write_text(json.dumps(spec))
        config = MagicMock()
        config.get_user.return_value = ("umadmin", "secret")
        config.get_schema_location.return_value = schema_dir
        config.get_trust_store.return_value = HostTrustStore(tmp_path / ".trust", lambda h, p: b"d")
        config.get_aiqum_api_settings.return_value = AIQUMAPISettings()
        config.data = {"aiqums": {"aiqum1": {"ip": "10.0.0.5"}}}
        resp = MagicMock()
        resp.status_code = 200
        resp.json.return_value = {"key": _REAL_KEY, "name": "v1", "_links": {}}
        resp.raise_for_status.return_value = None
        client = AIQUMAPIClient("aiqum1", config)
        try:
            with patch.object(client.session, "request", return_value=resp) as request:
                results = _query(mapping, client, {"key": _REAL_KEY})
            assert [(r.key, r.name) for r in results] == [(_REAL_KEY, "v1")]
            assert request.call_count == 1
            assert request.call_args.args[1] == (
                f"https://10.0.0.5/api/datacenter/storage/volumes/{quote(_REAL_KEY, safe='')}"
            )
            assert "?" not in request.call_args.args[1]
        finally:
            client.session.close()
