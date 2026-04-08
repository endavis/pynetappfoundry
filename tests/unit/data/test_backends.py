"""Tests for pynetappfoundry.data.backends.OntapBackend.

Backends are tested with mocked cache DB and mocked API client; no
real database or network is touched.
"""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from pynetappfoundry.cache.field_mapping import TypeMapping
from pynetappfoundry.data._routing import RoutingDecision
from pynetappfoundry.data.backends import OntapBackend
from tests.unit.data._fakes import FakeVolume


def _make_backend(mock_config: Any) -> OntapBackend:
    return OntapBackend(mock_config)


def _patch_metadata_path(backend: OntapBackend) -> Any:
    """Stub out the cache table registry lookup."""
    return patch.object(backend, "_resolve_metadata_path", return_value="storage.fake_volumes")


class TestOntapBackendGet:
    def test_ontap_get_cache_only(
        self,
        fake_volume_mapping: TypeMapping,
        mock_config: Any,
    ) -> None:
        backend = _make_backend(mock_config)
        decision = RoutingDecision(cache_fields=("name", "uuid"), live_fields=())
        cached_vol = FakeVolume(name="vol1", uuid="abc-123")

        mock_db = MagicMock()
        mock_db.query_with_filters.return_value = [cached_vol]

        with (
            patch.object(OntapBackend, "_cache_db", new=mock_db),
            _patch_metadata_path(backend),
        ):
            result = backend.get(
                FakeVolume,
                fake_volume_mapping,
                decision,
                cluster="prod1",
                identifier={"uuid": "abc-123"},
            )

        assert result is cached_vol
        mock_db.query_with_filters.assert_called_once_with(
            "prod1", "storage.fake_volumes", ["uuid = 'abc-123'"]
        )
        assert result is not None
        assert "name" in result._fetched_fields
        assert "uuid" in result._fetched_fields

    def test_ontap_get_live_only(
        self,
        fake_volume_mapping: TypeMapping,
        mock_config: Any,
    ) -> None:
        backend = _make_backend(mock_config)
        decision = RoutingDecision(cache_fields=(), live_fields=("iops",))
        live_vol = FakeVolume(uuid="abc-123", iops=42.5)

        mock_client = MagicMock()
        mock_client.get_all_records.return_value = {"records": [{"uuid": "abc-123"}]}

        with (
            patch.object(backend, "_get_api_client", return_value=mock_client),
            patch(
                "pynetappfoundry.data.backends.parse_api_response",
                return_value=[live_vol],
            ) as parse_mock,
        ):
            result = backend.get(
                FakeVolume,
                fake_volume_mapping,
                decision,
                cluster="prod1",
                identifier={"uuid": "abc-123"},
            )

        assert result is live_vol
        mock_client.get_all_records.assert_called_once()
        url = mock_client.get_all_records.call_args[0][0]
        assert "uuid=abc-123" in url
        assert "fields=iops" in url
        parse_mock.assert_called_once()
        assert "iops" in result._fetched_fields  # type: ignore[union-attr]

    def test_ontap_get_partial_merge(
        self,
        fake_volume_mapping: TypeMapping,
        mock_config: Any,
    ) -> None:
        backend = _make_backend(mock_config)
        decision = RoutingDecision(cache_fields=("name", "uuid"), live_fields=("iops",))
        cached_vol = FakeVolume(name="vol1", uuid="abc-123")
        cached_vol._fetched_fields.update({"name", "uuid"})
        live_vol = FakeVolume(iops=42.5)
        live_vol._fetched_fields.add("iops")

        mock_db = MagicMock()
        mock_db.query_with_filters.return_value = [cached_vol]
        mock_client = MagicMock()
        mock_client.get_all_records.return_value = {"records": [{"uuid": "abc-123"}]}

        with (
            patch.object(OntapBackend, "_cache_db", new=mock_db),
            patch.object(backend, "_get_api_client", return_value=mock_client),
            patch(
                "pynetappfoundry.data.backends.parse_api_response",
                return_value=[live_vol],
            ),
            _patch_metadata_path(backend),
        ):
            result = backend.get(
                FakeVolume,
                fake_volume_mapping,
                decision,
                cluster="prod1",
                identifier={"uuid": "abc-123"},
            )

        assert result is not None
        assert result.name == "vol1"
        assert result.iops == 42.5
        # union of fetched fields
        assert {"name", "uuid", "iops"}.issubset(result._fetched_fields)

    def test_ontap_get_no_match_returns_none(
        self,
        fake_volume_mapping: TypeMapping,
        mock_config: Any,
    ) -> None:
        backend = _make_backend(mock_config)
        decision = RoutingDecision(cache_fields=("uuid",), live_fields=())

        mock_db = MagicMock()
        mock_db.query_with_filters.return_value = []

        with (
            patch.object(OntapBackend, "_cache_db", new=mock_db),
            _patch_metadata_path(backend),
        ):
            result = backend.get(
                FakeVolume,
                fake_volume_mapping,
                decision,
                cluster="prod1",
                identifier={"uuid": "missing"},
            )

        assert result is None

    def test_ontap_get_multiple_matches_raises(
        self,
        fake_volume_mapping: TypeMapping,
        mock_config: Any,
    ) -> None:
        backend = _make_backend(mock_config)
        decision = RoutingDecision(cache_fields=("uuid",), live_fields=())

        mock_db = MagicMock()
        mock_db.query_with_filters.return_value = [
            FakeVolume(uuid="a"),
            FakeVolume(uuid="b"),
        ]

        with (
            patch.object(OntapBackend, "_cache_db", new=mock_db),
            _patch_metadata_path(backend),
            pytest.raises(ValueError, match="Expected exactly one"),
        ):
            backend.get(
                FakeVolume,
                fake_volume_mapping,
                decision,
                cluster="prod1",
                identifier={"uuid": "abc-123"},
            )


class TestOntapBackendQuery:
    def test_ontap_query_collection(
        self,
        fake_volume_mapping: TypeMapping,
        mock_config: Any,
    ) -> None:
        backend = _make_backend(mock_config)
        decision = RoutingDecision(cache_fields=("name", "uuid"), live_fields=())

        mock_db = MagicMock()
        mock_db.query_with_filters.return_value = [
            FakeVolume(name="v1", uuid="u1"),
            FakeVolume(name="v2", uuid="u2"),
        ]

        with (
            patch.object(OntapBackend, "_cache_db", new=mock_db),
            _patch_metadata_path(backend),
        ):
            results = backend.query(
                FakeVolume,
                fake_volume_mapping,
                decision,
                cluster="prod1",
                filters={"svm_name": "vs1"},
            )

        assert len(results) == 2
        mock_db.query_with_filters.assert_called_once_with(
            "prod1", "storage.fake_volumes", ["svm_name = 'vs1'"]
        )
        for vol in results:
            assert {"name", "uuid"}.issubset(vol._fetched_fields)

    def test_ontap_query_partial_raises(
        self,
        fake_volume_mapping: TypeMapping,
        mock_config: Any,
    ) -> None:
        backend = _make_backend(mock_config)
        decision = RoutingDecision(cache_fields=("name",), live_fields=("iops",))

        with pytest.raises(NotImplementedError, match="partial cache"):
            backend.query(
                FakeVolume,
                fake_volume_mapping,
                decision,
                cluster="prod1",
                filters={},
            )
