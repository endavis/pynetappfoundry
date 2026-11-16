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


class FakeAiqumParent(OntapModel):
    """Synthetic parent model for per-parent tests."""

    key: str | None = None
    name: str = ""


@pytest.fixture
def parent_mapping() -> Iterator[TypeMapping]:
    """Register a parent mapping that lists ``/parents`` for one test."""
    m = _mapping(
        name="FakeAiqumParent",
        model_class=FakeAiqumParent,
        api_endpoint="/parents",
    )
    model_registry.register_mapping("FakeAiqumParent", m)
    try:
        yield m
    finally:
        model_registry._mappings.pop("FakeAiqumParent", None)
        model_registry._mappings_by_class.pop(FakeAiqumParent, None)


def _child_mapping(**overrides: Any) -> TypeMapping:
    kwargs: dict[str, Any] = {
        "api_endpoint": _METRICS,
        "response_shape": "singleton",
        "parent_mapping": "FakeAiqumParent",
        "parent_id_field": "key",
    }
    kwargs.update(overrides)
    return _mapping(**kwargs)


def _per_parent_backend(max_parent_requests: int = 500) -> AiqumBackend:
    config = MagicMock(name="Config")
    config.get_aiqum_api_settings.return_value = AIQUMAPISettings(
        max_parent_requests=max_parent_requests
    )
    return AiqumBackend(config)


def _per_parent_client(parents: list[dict[str, Any]]) -> MagicMock:
    client = MagicMock()
    client.get_all_records.return_value = {"records": parents}
    client.call_endpoint.side_effect = lambda _ep, **kw: {
        "key": kw["path_params"]["key"],
        "name": "m",
    }
    return client


class TestPerParent:
    """A placeholder mapping with a parent_mapping is fetched per parent (#1057)."""

    def test_one_record_per_parent_in_order(self, parent_mapping: TypeMapping) -> None:
        client = _per_parent_client([{"key": "a,b", "name": "p1"}, {"key": "k2", "name": "p2"}])
        backend = _per_parent_backend()
        with patch.object(backend, "_get_api_client", return_value=client):
            results = backend.query(
                FakeAiqumVolume, _child_mapping(), _LIVE, "aiqum1", {"interval": "1h"}
            )
        assert [r.key for r in results] == ["a%2Cb", "k2"]
        assert all(r.was_fetched("name") for r in results)
        # Parents are fetched unfiltered; filters go to the child calls only.
        client.get_all_records.assert_called_once_with("/parents", "GET", query_params={})
        assert [c.kwargs for c in client.call_endpoint.call_args_list] == [
            {"query_params": {"interval": "1h"}, "path_params": {"key": "a%2Cb"}},
            {"query_params": {"interval": "1h"}, "path_params": {"key": "k2"}},
        ]

    def test_over_cap_raises_before_child_call(self, parent_mapping: TypeMapping) -> None:
        client = _per_parent_client([{"key": "a"}, {"key": "b"}, {"key": "c"}])
        backend = _per_parent_backend(max_parent_requests=2)
        with (
            patch.object(backend, "_get_api_client", return_value=client),
            pytest.raises(ValueError, match=r"(?s)3 parent.*max_parent_requests.*path_params"),
        ):
            backend.query(FakeAiqumVolume, _child_mapping(), _LIVE, "aiqum1", {})
        client.call_endpoint.assert_not_called()

    def test_at_cap_succeeds(self, parent_mapping: TypeMapping) -> None:
        client = _per_parent_client([{"key": "a"}, {"key": "b"}])
        backend = _per_parent_backend(max_parent_requests=2)
        with patch.object(backend, "_get_api_client", return_value=client):
            results = backend.query(FakeAiqumVolume, _child_mapping(), _LIVE, "aiqum1", {})
        assert [r.key for r in results] == ["a", "b"]

    def test_zero_cap_is_unlimited(self, parent_mapping: TypeMapping) -> None:
        client = _per_parent_client([{"key": f"k{i}"} for i in range(5)])
        backend = _per_parent_backend(max_parent_requests=0)
        with patch.object(backend, "_get_api_client", return_value=client):
            results = backend.query(FakeAiqumVolume, _child_mapping(), _LIVE, "aiqum1", {})
        assert len(results) == 5

    def test_parent_without_key_skipped(
        self, parent_mapping: TypeMapping, caplog: pytest.LogCaptureFixture
    ) -> None:
        client = _per_parent_client([{"name": "nokey"}, {"key": "k2"}])
        backend = _per_parent_backend()
        with (
            caplog.at_level(logging.WARNING),
            patch.object(backend, "_get_api_client", return_value=client),
        ):
            results = backend.query(FakeAiqumVolume, _child_mapping(), _LIVE, "aiqum1", {})
        assert [r.key for r in results] == ["k2"]
        assert "SKIP_PARENT" in caplog.text
        assert client.call_endpoint.call_count == 1

    def test_failing_child_skipped_and_logged(
        self, parent_mapping: TypeMapping, caplog: pytest.LogCaptureFixture
    ) -> None:
        client = _per_parent_client([{"key": "bad"}, {"key": "ok"}])

        def call(_ep: str, **kw: Any) -> dict[str, Any]:
            if kw["path_params"]["key"] == "bad":
                raise RuntimeError("404")
            return {"key": "ok", "name": "m"}

        client.call_endpoint.side_effect = call
        backend = _per_parent_backend()
        with (
            caplog.at_level(logging.WARNING),
            patch.object(backend, "_get_api_client", return_value=client),
        ):
            results = backend.query(FakeAiqumVolume, _child_mapping(), _LIVE, "aiqum1", {})
        assert [r.key for r in results] == ["ok"]
        assert "CHILD_FETCH_FAILED" in caplog.text

    def test_dotdot_key_skipped(
        self, parent_mapping: TypeMapping, caplog: pytest.LogCaptureFixture
    ) -> None:
        client = _per_parent_client([{"key": ".."}, {"key": "k2"}])
        backend = _per_parent_backend()
        with (
            caplog.at_level(logging.WARNING),
            patch.object(backend, "_get_api_client", return_value=client),
        ):
            results = backend.query(FakeAiqumVolume, _child_mapping(), _LIVE, "aiqum1", {})
        assert [r.key for r in results] == ["k2"]
        assert "CHILD_FETCH_FAILED" in caplog.text
        assert client.call_endpoint.call_count == 1

    def test_parent_query_error_propagates(self, parent_mapping: TypeMapping) -> None:
        client = MagicMock()
        client.get_all_records.side_effect = RuntimeError("parent down")
        backend = _per_parent_backend()
        with (
            patch.object(backend, "_get_api_client", return_value=client),
            pytest.raises(RuntimeError, match="parent down"),
        ):
            backend.query(FakeAiqumVolume, _child_mapping(), _LIVE, "aiqum1", {})
        client.call_endpoint.assert_not_called()

    def test_zero_parents_returns_empty(self, parent_mapping: TypeMapping) -> None:
        client = _per_parent_client([])
        backend = _per_parent_backend()
        with patch.object(backend, "_get_api_client", return_value=client):
            assert backend.query(FakeAiqumVolume, _child_mapping(), _LIVE, "aiqum1", {}) == []
        client.call_endpoint.assert_not_called()

    def test_placeholder_without_parent_still_raises(self) -> None:
        m = _child_mapping(parent_mapping=None, parent_id_field=None)
        backend = _per_parent_backend()
        with (
            patch.object(backend, "_get_api_client") as get_client,
            pytest.raises(ValueError, match=r"(?s)\{key\}.*no parent_mapping.*path_params"),
        ):
            backend.query(FakeAiqumVolume, m, _LIVE, "aiqum1", {})
        get_client.assert_not_called()

    def test_caller_path_params_keep_single_request(self, parent_mapping: TypeMapping) -> None:
        client = _per_parent_client([{"key": "a"}, {"key": "b"}])
        backend = _per_parent_backend()
        with patch.object(backend, "_get_api_client", return_value=client):
            results = backend.query(
                FakeAiqumVolume, _child_mapping(), _LIVE, "aiqum1", {}, path_params={"key": "x"}
            )
        assert [r.key for r in results] == ["x"]
        client.get_all_records.assert_not_called()
        client.call_endpoint.assert_called_once()

    def test_unregistered_parent_raises_before_any_request(self) -> None:
        m = _child_mapping(parent_mapping="NoSuchParent")
        backend = _per_parent_backend()
        with (
            patch.object(backend, "_get_api_client") as get_client,
            pytest.raises(ValueError, match="not registered"),
        ):
            backend.query(FakeAiqumVolume, m, _LIVE, "aiqum1", {})
        get_client.assert_not_called()

    def test_cycle_raises_before_any_request(self, parent_mapping: TypeMapping) -> None:
        cyclic = _mapping(
            name="FakeAiqumParent",
            model_class=FakeAiqumParent,
            api_endpoint="/parents",
            parent_mapping="FakeAiqumVolume",
            parent_id_field="key",
        )
        model_registry._mappings["FakeAiqumParent"] = cyclic
        child = _child_mapping()
        model_registry._mappings["FakeAiqumVolume"] = child
        try:
            backend = _per_parent_backend()
            with (
                patch.object(backend, "_get_api_client") as get_client,
                pytest.raises(ValueError, match="cycle"),
            ):
                backend.query(FakeAiqumVolume, child, _LIVE, "aiqum1", {})
            get_client.assert_not_called()
        finally:
            model_registry._mappings.pop("FakeAiqumVolume", None)

    def test_registry_sweep_per_parent_mappings(self) -> None:
        swept = 0
        for name, reg in model_registry.mappings.items():
            if reg.api_type != "aiqum" or not _placeholders(reg):
                continue
            assert reg.parent_mapping, name
            parent = model_registry.get_mapping(reg.parent_mapping)
            assert parent is not None, name
            assert not _placeholders(parent), name
            swept += 1
        assert swept > 0


class TestParentFilters:
    """parent_filters narrow the parent collection request of a per-parent query (#1061)."""

    def test_capability_flag(self) -> None:
        from pynetappfoundry.data.backends import OntapBackend
        from pynetappfoundry.data.dii_backend import DiiBackend

        assert AiqumBackend.supports_parent_filters is True
        assert DiiBackend.supports_parent_filters is False
        assert OntapBackend.supports_parent_filters is False

    def test_parent_request_carries_filters_child_only_filters(
        self, parent_mapping: TypeMapping
    ) -> None:
        client = _per_parent_client([{"key": "a"}, {"key": "b"}])
        backend = _per_parent_backend()
        with patch.object(backend, "_get_api_client", return_value=client):
            results = backend.query(
                FakeAiqumVolume,
                _child_mapping(),
                _LIVE,
                "aiqum1",
                {"interval": "1h"},
                parent_filters={"cluster.name": "c1"},
            )
        assert [r.key for r in results] == ["a", "b"]
        client.get_all_records.assert_called_once_with(
            "/parents", "GET", query_params={"cluster.name": "c1"}
        )
        assert [c.kwargs["query_params"] for c in client.call_endpoint.call_args_list] == [
            {"interval": "1h"},
            {"interval": "1h"},
        ]

    @pytest.mark.parametrize("parent_filters", [None, {}])
    def test_empty_parent_filters_send_empty_query_params(
        self, parent_mapping: TypeMapping, parent_filters: dict[str, Any] | None
    ) -> None:
        client = _per_parent_client([{"key": "a"}])
        backend = _per_parent_backend()
        with patch.object(backend, "_get_api_client", return_value=client):
            backend.query(
                FakeAiqumVolume,
                _child_mapping(),
                _LIVE,
                "aiqum1",
                {},
                parent_filters=parent_filters,
            )
        client.get_all_records.assert_called_once_with("/parents", "GET", query_params={})

    def test_cap_applies_after_filtering(self, parent_mapping: TypeMapping) -> None:
        client = _per_parent_client([{"key": "a"}, {"key": "b"}])
        backend = _per_parent_backend(max_parent_requests=2)
        with patch.object(backend, "_get_api_client", return_value=client):
            results = backend.query(
                FakeAiqumVolume,
                _child_mapping(),
                _LIVE,
                "aiqum1",
                {},
                parent_filters={"svm.name": "vs1"},
            )
        assert len(results) == 2

    def test_filtered_parents_over_cap_raise_before_child_call(
        self, parent_mapping: TypeMapping
    ) -> None:
        client = _per_parent_client([{"key": "a"}, {"key": "b"}, {"key": "c"}])
        backend = _per_parent_backend(max_parent_requests=2)
        with (
            patch.object(backend, "_get_api_client", return_value=client),
            pytest.raises(ValueError, match="max_parent_requests"),
        ):
            backend.query(
                FakeAiqumVolume,
                _child_mapping(),
                _LIVE,
                "aiqum1",
                {},
                parent_filters={"svm.name": "vs1"},
            )
        client.call_endpoint.assert_not_called()

    def test_key_parent_filter_takes_item_route(self, parent_mapping: TypeMapping) -> None:
        client = MagicMock()
        client.api_spec = {"paths": {"/parents": {"get": {}}, "/parents/{key}": {"get": {}}}}
        client.call_endpoint.side_effect = [
            {"key": "k1", "name": "p1"},
            {"key": "k1", "name": "m"},
        ]
        backend = _per_parent_backend()
        with patch.object(backend, "_get_api_client", return_value=client):
            results = backend.query(
                FakeAiqumVolume,
                _child_mapping(),
                _LIVE,
                "aiqum1",
                {"interval": "1h"},
                parent_filters={"key": "k1"},
            )
        assert [r.key for r in results] == ["k1"]
        client.get_all_records.assert_not_called()
        assert [c.args[0] for c in client.call_endpoint.call_args_list] == [
            "/parents/{key}",
            _METRICS,
        ]
        assert client.call_endpoint.call_args_list[1].kwargs == {
            "query_params": {"interval": "1h"},
            "path_params": {"key": "k1"},
        }

    def test_with_path_params_rejected(self, parent_mapping: TypeMapping) -> None:
        backend = _per_parent_backend()
        with (
            patch.object(backend, "_get_api_client") as get_client,
            pytest.raises(ValueError, match="parent_filters"),
        ):
            backend.query(
                FakeAiqumVolume,
                _child_mapping(),
                _LIVE,
                "aiqum1",
                {},
                path_params={"key": "x"},
                parent_filters={"svm.name": "vs1"},
            )
        get_client.assert_not_called()

    def test_non_per_parent_mapping_rejected(self, mapping: TypeMapping) -> None:
        backend = _backend()
        with (
            patch.object(backend, "_get_api_client") as get_client,
            pytest.raises(ValueError, match="parent_filters"),
        ):
            backend.query(
                FakeAiqumVolume,
                mapping,
                _LIVE,
                "aiqum1",
                {},
                parent_filters={"svm.name": "vs1"},
            )
        get_client.assert_not_called()
