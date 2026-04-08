"""Tests for pynetappfoundry.data.source.DataSource and QueryBuilder."""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import TypeMapping
from pynetappfoundry.data.source import _BACKENDS, DataSource, QueryBuilder

from .conftest import FakeComposite, FakeVolume


class TestDataSourceGet:
    def test_get_dispatches_to_correct_backend(
        self,
        fake_volume_mapping: TypeMapping,
        mock_config: Any,
    ) -> None:
        ds = DataSource(mock_config)
        fake_vol = FakeVolume(uuid="abc-123", name="vol1")
        fake_backend = MagicMock()
        fake_backend.get.return_value = fake_vol

        ds._backends["ontap"] = fake_backend
        result = ds.get(FakeVolume, cluster="prod1", id="abc-123")

        assert result is fake_vol
        fake_backend.get.assert_called_once()
        args = fake_backend.get.call_args.args
        # Positional: model_class, mapping, decision, cluster, identifier
        assert args[0] is FakeVolume
        assert args[1] is fake_volume_mapping
        assert args[3] == "prod1"
        assert args[4] == {"uuid": "abc-123"}

    def test_get_unknown_api_type_raises(
        self,
        mock_config: Any,
    ) -> None:
        # Register a temporary mapping with an unknown api_type.
        from pynetappfoundry.cache.field_mapping import FieldMapping

        class _Other(FakeVolume):
            pass

        mapping = TypeMapping(
            name="_Other",
            model_class=_Other,
            api_endpoint="/x",
            api_type="aiqum",
            identifier_field="uuid",
            fields=(FieldMapping(cache_attr="uuid"),),
        )
        model_registry.register_mapping("_Other", mapping)
        try:
            ds = DataSource(mock_config)
            with pytest.raises(ValueError, match="No backend registered"):
                ds.get(_Other, cluster="prod1", id="abc")
        finally:
            model_registry._mappings.pop("_Other", None)

    def test_per_call_source_override_passed_through(
        self,
        fake_volume_mapping: TypeMapping,
        mock_config: Any,
    ) -> None:
        ds = DataSource(mock_config)
        fake_backend = MagicMock()
        fake_backend.get.return_value = None
        ds._backends["ontap"] = fake_backend

        with patch(
            "pynetappfoundry.data.source.decide_path", wraps=lambda m, f, s: MagicMock()
        ) as decide:
            ds.get(FakeVolume, cluster="prod1", id="abc-123", source="live")
            assert decide.call_args.args[2] == "live"

    def test_get_normalizes_string_id_for_single_key_model(
        self,
        fake_volume_mapping: TypeMapping,
        mock_config: Any,
    ) -> None:
        ds = DataSource(mock_config)
        fake_backend = MagicMock()
        fake_backend.get.return_value = None
        ds._backends["ontap"] = fake_backend

        ds.get(FakeVolume, cluster="prod1", id="abc-123")
        identifier = fake_backend.get.call_args.args[4]
        assert identifier == {"uuid": "abc-123"}

    def test_get_normalizes_dict_id_for_composite_key_model(
        self,
        fake_composite_mapping: TypeMapping,
        mock_config: Any,
    ) -> None:
        ds = DataSource(mock_config)
        fake_backend = MagicMock()
        fake_backend.get.return_value = None
        ds._backends["ontap"] = fake_backend

        ds.get(
            FakeComposite,
            cluster="prod1",
            id={"svm_name": "vs1", "name": "vol1"},
        )
        identifier = fake_backend.get.call_args.args[4]
        assert identifier == {"svm_name": "vs1", "name": "vol1"}

    def test_get_raises_when_identifier_field_undeclared(
        self,
        mock_config: Any,
    ) -> None:
        from pynetappfoundry.cache.field_mapping import FieldMapping

        class _NoId(FakeVolume):
            pass

        mapping = TypeMapping(
            name="_NoId",
            model_class=_NoId,
            api_endpoint="/x",
            api_type="ontap",
            fields=(FieldMapping(cache_attr="uuid"),),
        )
        model_registry.register_mapping("_NoId", mapping)
        try:
            ds = DataSource(mock_config)
            with pytest.raises(ValueError, match="no identifier_field"):
                ds.get(_NoId, cluster="prod1", id="abc")
        finally:
            model_registry._mappings.pop("_NoId", None)

    def test_get_raises_when_composite_key_passed_string(
        self,
        fake_composite_mapping: TypeMapping,
        mock_config: Any,
    ) -> None:
        ds = DataSource(mock_config)
        with pytest.raises(ValueError, match="composite identifier"):
            ds.get(FakeComposite, cluster="prod1", id="oops")

    def test_get_raises_when_dict_id_missing_required_key(
        self,
        fake_composite_mapping: TypeMapping,
        mock_config: Any,
    ) -> None:
        ds = DataSource(mock_config)
        with pytest.raises(ValueError, match="missing required key"):
            ds.get(FakeComposite, cluster="prod1", id={"svm_name": "vs1"})

    def test_get_raises_when_unknown_model(self, mock_config: Any) -> None:
        ds = DataSource(mock_config)

        class Unregistered(FakeVolume):
            pass

        with pytest.raises(ValueError, match="No TypeMapping registered"):
            ds.get(Unregistered, cluster="prod1", id="abc")


class TestDataSourceQuery:
    def test_query_returns_iterable(
        self,
        fake_volume_mapping: TypeMapping,
        mock_config: Any,
    ) -> None:
        ds = DataSource(mock_config)
        fake_backend = MagicMock()
        fake_backend.query.return_value = [
            FakeVolume(uuid="u1"),
            FakeVolume(uuid="u2"),
        ]
        ds._backends["ontap"] = fake_backend

        qb = ds.query(FakeVolume, cluster="prod1")
        assert isinstance(qb, QueryBuilder)
        results = list(qb.filter({"svm.name": "vs1"}))
        assert len(results) == 2
        # Backend should have been called with the dict unchanged.
        filters_arg = fake_backend.query.call_args.args[4]
        assert filters_arg == {"svm.name": "vs1"}

    def test_query_filter_kwargs_merge_with_dict(
        self,
        fake_volume_mapping: TypeMapping,
        mock_config: Any,
    ) -> None:
        ds = DataSource(mock_config)
        fake_backend = MagicMock()
        fake_backend.query.return_value = []
        ds._backends["ontap"] = fake_backend

        list(ds.query(FakeVolume, cluster="prod1").filter({"svm.name": "vs1"}, name="vol1"))
        filters_arg = fake_backend.query.call_args.args[4]
        assert filters_arg == {"svm.name": "vs1", "name": "vol1"}


class TestBackendsRegistry:
    def test_ontap_backend_registered_at_import(self) -> None:
        assert "ontap" in _BACKENDS


class TestRealOntapVolumeRouting:
    """Smoke test against the real OntapVolume mapping.

    Verifies that the routing decision against the production
    ``ONTAPVOLUME_MAPPING`` lists the expected real field names. This
    catches regressions where the real mapping changes shape under us.
    """

    def test_real_volume_default_routing(self) -> None:
        from pynetappfoundry.cache.ontap.storage.volumes.mapping import (
            ONTAPVOLUME_MAPPING,
        )
        from pynetappfoundry.data._routing import decide_path

        decision = decide_path(ONTAPVOLUME_MAPPING, None, "auto")
        # Default set must contain core cached fields and exclude realtime.
        assert "uuid" in decision.cache_fields
        assert "name" in decision.cache_fields
        # No realtime fields appear in default set.
        for field in ONTAPVOLUME_MAPPING.realtime_fields():
            assert field.cache_attr not in decision.cache_fields
            assert field.cache_attr not in decision.live_fields

    def test_real_volume_identifier_field(self) -> None:
        from pynetappfoundry.cache.ontap.storage.volumes.mapping import (
            ONTAPVOLUME_MAPPING,
        )

        assert ONTAPVOLUME_MAPPING.identifier_field == "uuid"
