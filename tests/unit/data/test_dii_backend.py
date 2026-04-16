"""Tests for pynetappfoundry.data.dii_backend.DiiBackend.

DiiBackend is live-only; no cache DB or network is touched -- all
API clients are mocked.
"""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.data._routing import RoutingDecision
from pynetappfoundry.data.dii_backend import DiiBackend
from pynetappfoundry.models._base import OntapModel

# ---------------------------------------------------------------------------
# Fake DII model & mapping
# ---------------------------------------------------------------------------


class FakeDiiAsset(OntapModel):
    """Synthetic DII model for backend tests."""

    id: int = 0
    name: str = ""
    vendor: str = ""


@pytest.fixture
def fake_dii_mapping() -> Iterator[TypeMapping]:
    """Register a synthetic DII mapping for the duration of one test."""
    mapping = TypeMapping(
        name="FakeDiiAsset",
        model_class=FakeDiiAsset,
        api_endpoint="/assets/storages",
        api_type="dii",
        identifier_field="id",
        records_path="",
        fields=(
            FieldMapping(cache_attr="id", default=0),
            FieldMapping(cache_attr="name"),
            FieldMapping(cache_attr="vendor"),
        ),
    )
    model_registry.register_mapping("FakeDiiAsset", mapping)
    try:
        yield mapping
    finally:
        model_registry._mappings.pop("FakeDiiAsset", None)
        model_registry._mappings_by_class.pop(FakeDiiAsset, None)


@pytest.fixture
def mock_config() -> Any:
    """A bare MagicMock standing in for :class:`Config`."""
    return MagicMock(name="Config")


def _make_backend(config: Any) -> DiiBackend:
    return DiiBackend(config)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestDiiBackendQuery:
    """Core query path tests for DiiBackend."""

    def test_live_query_bare_array_response(
        self,
        fake_dii_mapping: TypeMapping,
        mock_config: Any,
    ) -> None:
        """Bare-array DII response is parsed into model instances."""
        backend = _make_backend(mock_config)
        decision = RoutingDecision(cache_fields=(), live_fields=("id", "name", "vendor"))

        mock_client = MagicMock()
        mock_client.call_endpoint.return_value = [
            {"id": 1, "name": "stor1", "vendor": "NetApp"},
            {"id": 2, "name": "stor2", "vendor": "NetApp"},
        ]

        with patch.object(backend, "_get_api_client", return_value=mock_client):
            results = backend.query(
                FakeDiiAsset,
                fake_dii_mapping,
                decision,
                cluster="tenant1",
                filters={},
            )

        assert len(results) == 2
        assert results[0].id == 1
        assert results[0].name == "stor1"
        assert results[1].id == 2

    def test_empty_response_returns_empty_list(
        self,
        fake_dii_mapping: TypeMapping,
        mock_config: Any,
    ) -> None:
        """Empty list response produces no results."""
        backend = _make_backend(mock_config)
        decision = RoutingDecision(cache_fields=(), live_fields=("id",))

        mock_client = MagicMock()
        mock_client.call_endpoint.return_value = []

        with patch.object(backend, "_get_api_client", return_value=mock_client):
            results = backend.query(
                FakeDiiAsset,
                fake_dii_mapping,
                decision,
                cluster="tenant1",
                filters={},
            )

        assert results == []

    def test_none_response_returns_empty_list(
        self,
        fake_dii_mapping: TypeMapping,
        mock_config: Any,
    ) -> None:
        """None response is handled gracefully."""
        backend = _make_backend(mock_config)
        decision = RoutingDecision(cache_fields=(), live_fields=("id",))

        mock_client = MagicMock()
        mock_client.call_endpoint.return_value = None

        with patch.object(backend, "_get_api_client", return_value=mock_client):
            results = backend.query(
                FakeDiiAsset,
                fake_dii_mapping,
                decision,
                cluster="tenant1",
                filters={},
            )

        assert results == []

    def test_filters_translate_to_query_params(
        self,
        fake_dii_mapping: TypeMapping,
        mock_config: Any,
    ) -> None:
        """Dict filters are passed as query_params to call_endpoint."""
        backend = _make_backend(mock_config)
        decision = RoutingDecision(cache_fields=(), live_fields=("id", "name"))

        mock_client = MagicMock()
        mock_client.call_endpoint.return_value = []

        with patch.object(backend, "_get_api_client", return_value=mock_client):
            backend.query(
                FakeDiiAsset,
                fake_dii_mapping,
                decision,
                cluster="tenant1",
                filters={"vendor": "NetApp", "name": "stor1"},
            )

        mock_client.call_endpoint.assert_called_once_with(
            "/assets/storages",
            query_params={"vendor": "NetApp", "name": "stor1"},
        )

    def test_fetched_fields_stamped_on_instances(
        self,
        fake_dii_mapping: TypeMapping,
        mock_config: Any,
    ) -> None:
        """Returned instances have _fetched_fields populated."""
        backend = _make_backend(mock_config)
        live_fields = ("id", "name", "vendor")
        decision = RoutingDecision(cache_fields=(), live_fields=live_fields)

        mock_client = MagicMock()
        mock_client.call_endpoint.return_value = [
            {"id": 1, "name": "stor1", "vendor": "NetApp"},
        ]

        with patch.object(backend, "_get_api_client", return_value=mock_client):
            results = backend.query(
                FakeDiiAsset,
                fake_dii_mapping,
                decision,
                cluster="tenant1",
                filters={},
            )

        assert len(results) == 1
        for field in live_fields:
            assert results[0].was_fetched(field)


class TestDiiBackendErrors:
    """Error handling tests for DiiBackend."""

    def test_cache_only_decision_raises(
        self,
        fake_dii_mapping: TypeMapping,
        mock_config: Any,
    ) -> None:
        """Cache-only routing decision raises NotImplementedError."""
        backend = _make_backend(mock_config)
        decision = RoutingDecision(cache_fields=("id", "name"), live_fields=())

        with pytest.raises(NotImplementedError, match="cache-only"):
            backend.query(
                FakeDiiAsset,
                fake_dii_mapping,
                decision,
                cluster="tenant1",
                filters={},
            )

    def test_where_expressions_raises(
        self,
        fake_dii_mapping: TypeMapping,
        mock_config: Any,
    ) -> None:
        """where_expressions raises NotImplementedError."""
        backend = _make_backend(mock_config)
        decision = RoutingDecision(cache_fields=(), live_fields=("id",))

        mock_client = MagicMock()
        mock_client.call_endpoint.return_value = []

        with (
            patch.object(backend, "_get_api_client", return_value=mock_client),
            pytest.raises(NotImplementedError, match="where_expressions"),
        ):
            backend.query(
                FakeDiiAsset,
                fake_dii_mapping,
                decision,
                cluster="tenant1",
                filters={},
                where_expressions=("id > 10",),
            )

    def test_no_live_fields_returns_empty(
        self,
        fake_dii_mapping: TypeMapping,
        mock_config: Any,
    ) -> None:
        """Decision with no live_fields (and no cache_fields) returns []."""
        backend = _make_backend(mock_config)
        decision = RoutingDecision(cache_fields=(), live_fields=())

        results = backend.query(
            FakeDiiAsset,
            fake_dii_mapping,
            decision,
            cluster="tenant1",
            filters={},
        )

        assert results == []


class TestDiiBackendClientCaching:
    """Tests for lazy API client construction and caching."""

    def test_api_client_cached_per_cluster(
        self,
        mock_config: Any,
    ) -> None:
        """Repeated calls for the same cluster reuse the same client."""
        backend = _make_backend(mock_config)

        with patch(
            "pynetappfoundry.clients.dii.api.DIIAPIClient",
        ) as mock_cls:
            mock_cls.return_value = MagicMock()
            client1 = backend._get_api_client("tenant1")
            client2 = backend._get_api_client("tenant1")

        assert client1 is client2
        mock_cls.assert_called_once()

    def test_api_client_different_clusters(
        self,
        mock_config: Any,
    ) -> None:
        """Different clusters get different client instances."""
        backend = _make_backend(mock_config)

        with patch(
            "pynetappfoundry.clients.dii.api.DIIAPIClient",
        ) as mock_cls:
            mock_cls.side_effect = [MagicMock(), MagicMock()]
            client1 = backend._get_api_client("tenant1")
            client2 = backend._get_api_client("tenant2")

        assert client1 is not client2
        assert mock_cls.call_count == 2
