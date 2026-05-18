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
from tests.unit.data._fakes import (
    FakeChildVolume,
    FakeChildWithDottedRef,
    FakeOrphanChild,
    FakeParentModel,
    FakeVolume,
)


def _make_backend(mock_config: Any) -> OntapBackend:
    return OntapBackend(mock_config)


def _patch_metadata_path(backend: OntapBackend) -> Any:
    """Stub out the cache table registry lookup."""
    return patch.object(backend, "_resolve_metadata_path", return_value="storage.fake_volumes")


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

    def test_live_query_unfiltered_delegates_to_fetch(
        self,
        fake_volume_mapping: TypeMapping,
        mock_config: Any,
    ) -> None:
        """Whole-model, unfiltered live query delegates to ``fetch()``."""
        backend = _make_backend(mock_config)
        # Full live-eligible set: every non-derived field in the mapping.
        live_fields = tuple(
            f.cache_attr for f in fake_volume_mapping.fields if f.cache_strategy != "derived"
        )
        decision = RoutingDecision(cache_fields=(), live_fields=live_fields)
        fetched = [FakeVolume(uuid="u1"), FakeVolume(uuid="u2")]

        mock_client = MagicMock()
        with (
            patch.object(backend, "_get_api_client", return_value=mock_client),
            patch(
                "pynetappfoundry.data.backends.fetch",
                return_value=fetched,
            ) as fetch_mock,
        ):
            results = backend.query(
                FakeVolume,
                fake_volume_mapping,
                decision,
                cluster="prod1",
                filters={},
            )

        assert results == fetched
        fetch_mock.assert_called_once()
        kwargs = fetch_mock.call_args.kwargs
        assert kwargs["cluster"] == "prod1"
        assert kwargs["config"] is mock_config
        assert kwargs["api_client"] is mock_client
        for vol in results:
            assert set(live_fields).issubset(vol._fetched_fields)

    def test_live_query_filtered_does_not_delegate_to_fetch(
        self,
        fake_volume_mapping: TypeMapping,
        mock_config: Any,
    ) -> None:
        """Live query with a filter falls through to ``_fetch_live_filtered``."""
        backend = _make_backend(mock_config)
        live_fields = tuple(
            f.cache_attr for f in fake_volume_mapping.fields if f.cache_strategy != "derived"
        )
        decision = RoutingDecision(cache_fields=(), live_fields=live_fields)
        live_vol = FakeVolume(uuid="abc-123", name="vol1")

        mock_client = MagicMock()
        mock_client.get_all_records.return_value = {"records": [{"uuid": "abc-123"}]}

        with (
            patch.object(backend, "_get_api_client", return_value=mock_client),
            patch(
                "pynetappfoundry.data.backends.parse_api_response",
                return_value=[live_vol],
            ),
            patch("pynetappfoundry.data.backends.fetch") as fetch_mock,
        ):
            results = backend.query(
                FakeVolume,
                fake_volume_mapping,
                decision,
                cluster="prod1",
                filters={"name": "vol1"},
            )

        assert results == [live_vol]
        fetch_mock.assert_not_called()
        mock_client.get_all_records.assert_called_once()
        url = mock_client.get_all_records.call_args[0][0]
        assert "name=vol1" in url

    def test_live_query_field_restricted_does_not_delegate_to_fetch(
        self,
        fake_volume_mapping: TypeMapping,
        mock_config: Any,
    ) -> None:
        """Live query with restricted live_fields uses _fetch_live_filtered."""
        backend = _make_backend(mock_config)
        # Only one field requested — not the full live-eligible set.
        decision = RoutingDecision(cache_fields=(), live_fields=("iops",))
        live_vol = FakeVolume(uuid="abc-123", iops=42.5)

        mock_client = MagicMock()
        mock_client.get_all_records.return_value = {"records": [{"uuid": "abc-123"}]}

        with (
            patch.object(backend, "_get_api_client", return_value=mock_client),
            patch(
                "pynetappfoundry.data.backends.parse_api_response",
                return_value=[live_vol],
            ),
            patch("pynetappfoundry.data.backends.fetch") as fetch_mock,
        ):
            results = backend.query(
                FakeVolume,
                fake_volume_mapping,
                decision,
                cluster="prod1",
                filters={},
            )

        assert results == [live_vol]
        fetch_mock.assert_not_called()
        mock_client.get_all_records.assert_called_once()

    def test_live_query_fetch_returns_singleton(
        self,
        fake_volume_mapping: TypeMapping,
        mock_config: Any,
    ) -> None:
        """When ``fetch()`` returns a single model (singleton shape),
        the backend wraps it in a list."""
        backend = _make_backend(mock_config)
        live_fields = tuple(
            f.cache_attr for f in fake_volume_mapping.fields if f.cache_strategy != "derived"
        )
        decision = RoutingDecision(cache_fields=(), live_fields=live_fields)
        single_vol = FakeVolume(uuid="u1")

        with (
            patch.object(backend, "_get_api_client", return_value=MagicMock()),
            patch(
                "pynetappfoundry.data.backends.fetch",
                return_value=single_vol,
            ),
        ):
            results = backend.query(
                FakeVolume,
                fake_volume_mapping,
                decision,
                cluster="prod1",
                filters={},
            )

        assert results == [single_vol]


class TestOntapBackendQueryPartial:
    """Tests for the Approach C partial-fetch algorithm in ``query()``."""

    def test_partial_query_happy_path_single_key(
        self,
        fake_volume_mapping: TypeMapping,
        mock_config: Any,
    ) -> None:
        backend = _make_backend(mock_config)
        decision = RoutingDecision(
            cache_fields=("name", "uuid", "size"),
            live_fields=("iops",),
        )
        cached = [
            FakeVolume(name="v1", uuid="u1", size=100),
            FakeVolume(name="v2", uuid="u2", size=200),
            FakeVolume(name="v3", uuid="u3", size=300),
        ]
        live = [
            FakeVolume(uuid="u1", iops=10.0),
            FakeVolume(uuid="u2", iops=20.0),
            FakeVolume(uuid="u3", iops=30.0),
        ]

        mock_db = MagicMock()
        mock_db.query_with_filters.return_value = cached
        mock_client = MagicMock()
        mock_client.get_all_records.return_value = {"records": []}

        with (
            patch.object(OntapBackend, "_cache_db", new=mock_db),
            patch.object(backend, "_get_api_client", return_value=mock_client),
            patch(
                "pynetappfoundry.data.backends.parse_api_response",
                return_value=live,
            ),
            _patch_metadata_path(backend),
        ):
            results = backend.query(
                FakeVolume,
                fake_volume_mapping,
                decision,
                cluster="prod1",
                filters={"name": "v1"},
            )

        assert len(results) == 3
        by_uuid = {r.uuid: r for r in results}
        assert by_uuid["u1"].iops == 10.0
        assert by_uuid["u2"].iops == 20.0
        assert by_uuid["u3"].iops == 30.0
        for r in results:
            assert r.was_fetched("name")
            assert r.was_fetched("uuid")
            assert r.was_fetched("iops")

    def test_partial_query_composite_key_raises_not_implemented(
        self,
        fake_composite_mapping: TypeMapping,
        mock_config: Any,
    ) -> None:
        from tests.unit.data._fakes import FakeComposite

        backend = _make_backend(mock_config)
        decision = RoutingDecision(cache_fields=("name",), live_fields=("svm_name",))

        with pytest.raises(NotImplementedError, match="FakeComposite"):
            backend.query(
                FakeComposite,
                fake_composite_mapping,
                decision,
                cluster="prod1",
                filters={},
            )

    def test_partial_query_realtime_field_filter_raises(
        self,
        fake_volume_mapping: TypeMapping,
        mock_config: Any,
    ) -> None:
        backend = _make_backend(mock_config)
        decision = RoutingDecision(cache_fields=("name",), live_fields=("iops",))

        with pytest.raises(NotImplementedError, match="'iops'"):
            backend.query(
                FakeVolume,
                fake_volume_mapping,
                decision,
                cluster="prod1",
                filters={"iops": 42.0},
            )

    def test_partial_query_no_identifier_field_raises(
        self,
        mock_config: Any,
    ) -> None:
        from pynetappfoundry.cache._registry import model_registry
        from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping

        mapping = TypeMapping(
            name="NoIdVolume",
            model_class=FakeVolume,
            api_endpoint="/storage/no-id?fields=*",
            api_type="ontap",
            identifier_field=None,
            fields=(
                FieldMapping(cache_attr="name", cache_strategy="cache"),
                FieldMapping(cache_attr="iops", cache_strategy="realtime"),
            ),
        )
        model_registry.register_mapping("NoIdVolume", mapping)
        try:
            backend = _make_backend(mock_config)
            decision = RoutingDecision(cache_fields=("name",), live_fields=("iops",))
            with pytest.raises(ValueError, match="NoIdVolume"):
                backend.query(
                    FakeVolume,
                    mapping,
                    decision,
                    cluster="prod1",
                    filters={},
                )
        finally:
            model_registry._mappings.pop("NoIdVolume", None)

    def test_partial_query_empty_cache_result(
        self,
        fake_volume_mapping: TypeMapping,
        mock_config: Any,
    ) -> None:
        backend = _make_backend(mock_config)
        decision = RoutingDecision(cache_fields=("name",), live_fields=("iops",))

        mock_db = MagicMock()
        mock_db.query_with_filters.return_value = []
        mock_client = MagicMock()

        with (
            patch.object(OntapBackend, "_cache_db", new=mock_db),
            patch.object(backend, "_get_api_client", return_value=mock_client),
            _patch_metadata_path(backend),
        ):
            results = backend.query(
                FakeVolume,
                fake_volume_mapping,
                decision,
                cluster="prod1",
                filters={"name": "nope"},
            )

        assert results == []
        mock_client.get_all_records.assert_not_called()

    def test_partial_query_live_returns_extras_dropped(
        self,
        fake_volume_mapping: TypeMapping,
        mock_config: Any,
    ) -> None:
        backend = _make_backend(mock_config)
        decision = RoutingDecision(cache_fields=("uuid",), live_fields=("iops",))
        cached = [FakeVolume(uuid=f"u{i}") for i in range(1, 4)]
        live = [FakeVolume(uuid=f"u{i}", iops=float(i)) for i in range(1, 6)]

        mock_db = MagicMock()
        mock_db.query_with_filters.return_value = cached
        mock_client = MagicMock()
        mock_client.get_all_records.return_value = {"records": []}

        with (
            patch.object(OntapBackend, "_cache_db", new=mock_db),
            patch.object(backend, "_get_api_client", return_value=mock_client),
            patch(
                "pynetappfoundry.data.backends.parse_api_response",
                return_value=live,
            ),
            _patch_metadata_path(backend),
        ):
            results = backend.query(
                FakeVolume,
                fake_volume_mapping,
                decision,
                cluster="prod1",
                filters={},
            )

        assert len(results) == 3
        uuids = {r.uuid for r in results}
        assert uuids == {"u1", "u2", "u3"}

    def test_partial_query_live_returns_fewer_unmerged_passthrough(
        self,
        fake_volume_mapping: TypeMapping,
        mock_config: Any,
    ) -> None:
        backend = _make_backend(mock_config)
        decision = RoutingDecision(cache_fields=("uuid",), live_fields=("iops",))
        cached = [FakeVolume(uuid=f"u{i}") for i in range(1, 6)]
        live = [FakeVolume(uuid=f"u{i}", iops=float(i)) for i in range(1, 4)]

        mock_db = MagicMock()
        mock_db.query_with_filters.return_value = cached
        mock_client = MagicMock()
        mock_client.get_all_records.return_value = {"records": []}

        with (
            patch.object(OntapBackend, "_cache_db", new=mock_db),
            patch.object(backend, "_get_api_client", return_value=mock_client),
            patch(
                "pynetappfoundry.data.backends.parse_api_response",
                return_value=live,
            ),
            _patch_metadata_path(backend),
        ):
            results = backend.query(
                FakeVolume,
                fake_volume_mapping,
                decision,
                cluster="prod1",
                filters={},
            )

        assert len(results) == 5
        by_uuid = {r.uuid: r for r in results}
        for uid in ("u1", "u2", "u3"):
            assert by_uuid[uid].was_fetched("iops")
        for uid in ("u4", "u5"):
            assert not by_uuid[uid].was_fetched("iops")
            assert by_uuid[uid].was_fetched("uuid")

    def test_partial_query_chunks_over_batch_size(
        self,
        fake_volume_mapping: TypeMapping,
        mock_config: Any,
    ) -> None:
        backend = _make_backend(mock_config)
        decision = RoutingDecision(cache_fields=("uuid",), live_fields=("iops",))
        cached = [FakeVolume(uuid=f"u{i}") for i in range(250)]
        live_all = [FakeVolume(uuid=f"u{i}", iops=float(i)) for i in range(250)]

        mock_db = MagicMock()
        mock_db.query_with_filters.return_value = cached
        mock_client = MagicMock()
        mock_client.get_all_records.return_value = {"records": []}

        # Return chunked slices of live records, 100/100/50, on successive
        # parse_api_response calls.
        parse_side_effect = [live_all[0:100], live_all[100:200], live_all[200:250]]

        with (
            patch.object(OntapBackend, "_cache_db", new=mock_db),
            patch.object(backend, "_get_api_client", return_value=mock_client),
            patch(
                "pynetappfoundry.data.backends.parse_api_response",
                side_effect=parse_side_effect,
            ),
            _patch_metadata_path(backend),
        ):
            results = backend.query(
                FakeVolume,
                fake_volume_mapping,
                decision,
                cluster="prod1",
                filters={},
            )

        assert len(results) == 250
        assert mock_client.get_all_records.call_count == 3
        # Verify merged iops values populated
        for i, r in enumerate(results):
            assert r.iops == float(i)

    def test_partial_query_chunk_failure_propagates(
        self,
        fake_volume_mapping: TypeMapping,
        mock_config: Any,
    ) -> None:
        backend = _make_backend(mock_config)
        decision = RoutingDecision(cache_fields=("uuid",), live_fields=("iops",))
        cached = [FakeVolume(uuid=f"u{i}") for i in range(250)]

        mock_db = MagicMock()
        mock_db.query_with_filters.return_value = cached
        mock_client = MagicMock()
        mock_client.get_all_records.side_effect = [
            {"records": []},
            RuntimeError("second chunk boom"),
            {"records": []},
        ]

        with (
            patch.object(OntapBackend, "_cache_db", new=mock_db),
            patch.object(backend, "_get_api_client", return_value=mock_client),
            patch(
                "pynetappfoundry.data.backends.parse_api_response",
                return_value=[],
            ),
            _patch_metadata_path(backend),
            pytest.raises(RuntimeError, match="second chunk boom"),
        ):
            backend.query(
                FakeVolume,
                fake_volume_mapping,
                decision,
                cluster="prod1",
                filters={},
            )

    def test_partial_query_url_uses_pipe_or_for_identifiers(
        self,
        fake_volume_mapping: TypeMapping,
        mock_config: Any,
    ) -> None:
        backend = _make_backend(mock_config)
        decision = RoutingDecision(cache_fields=("uuid",), live_fields=("iops",))
        cached = [FakeVolume(uuid=f"u{i}") for i in range(1, 4)]

        mock_db = MagicMock()
        mock_db.query_with_filters.return_value = cached
        mock_client = MagicMock()
        mock_client.get_all_records.return_value = {"records": []}

        with (
            patch.object(OntapBackend, "_cache_db", new=mock_db),
            patch.object(backend, "_get_api_client", return_value=mock_client),
            patch(
                "pynetappfoundry.data.backends.parse_api_response",
                return_value=[],
            ),
            _patch_metadata_path(backend),
        ):
            backend.query(
                FakeVolume,
                fake_volume_mapping,
                decision,
                cluster="prod1",
                filters={},
            )

        mock_client.get_all_records.assert_called_once()
        url = mock_client.get_all_records.call_args[0][0]
        # urlencode quotes `|` as %7C
        assert "uuid=u1%7Cu2%7Cu3" in url
        assert "fields=%2A" in url or "fields=*" in url

    def test_partial_query_parent_keyed_delegates_to_parent_path(
        self,
        fake_child_mapping: TypeMapping,
        mock_config: Any,
    ) -> None:
        """Parent-keyed mappings now route through the parent-keyed path."""
        backend = _make_backend(mock_config)
        decision = RoutingDecision(cache_fields=("uuid", "volume.uuid"), live_fields=("metric",))
        cached = [
            FakeChildWithDottedRef(uuid="c1", volume=FakeChildVolume(uuid="vol-1"), metric=0.0),
        ]
        live = [
            FakeChildWithDottedRef(uuid="c1", metric=99.0),
        ]

        mock_db = MagicMock()
        mock_db.query_with_filters.return_value = cached
        mock_client = MagicMock()
        mock_client.get_all_records.return_value = {"records": []}

        with (
            patch.object(OntapBackend, "_cache_db", new=mock_db),
            patch.object(backend, "_get_api_client", return_value=mock_client),
            patch(
                "pynetappfoundry.data.backends.parse_api_response",
                return_value=live,
            ),
            patch.object(backend, "_resolve_metadata_path", return_value="storage.fake_children"),
        ):
            results = backend.query(
                FakeChildWithDottedRef,
                fake_child_mapping,
                decision,
                cluster="prod1",
                filters={},
            )

        assert len(results) == 1
        assert results[0].metric == 99.0
        mock_client.get_all_records.assert_called_once()
        url = mock_client.get_all_records.call_args[0][0]
        assert "vol-1" in url

    def test_partial_query_chunked_helper(self) -> None:
        assert list(OntapBackend._chunked([], 100)) == []
        assert list(OntapBackend._chunked([1, 2, 3], 100)) == [[1, 2, 3]]
        assert list(OntapBackend._chunked([1, 2, 3, 4], 2)) == [[1, 2], [3, 4]]
        assert list(OntapBackend._chunked(list(range(5)), 2)) == [
            [0, 1],
            [2, 3],
            [4],
        ]
        assert list(OntapBackend._chunked(list(range(250)), 100)) == [
            list(range(0, 100)),
            list(range(100, 200)),
            list(range(200, 250)),
        ]

    def test_partial_query_exactly_batch_size(
        self,
        fake_volume_mapping: TypeMapping,
        mock_config: Any,
    ) -> None:
        """Exactly 100 cached records should produce 1 API call (no split)."""
        backend = _make_backend(mock_config)
        decision = RoutingDecision(cache_fields=("uuid",), live_fields=("iops",))
        cached = [FakeVolume(uuid=f"u{i}") for i in range(100)]
        live_all = [FakeVolume(uuid=f"u{i}", iops=float(i)) for i in range(100)]

        mock_db = MagicMock()
        mock_db.query_with_filters.return_value = cached
        mock_client = MagicMock()
        mock_client.get_all_records.return_value = {"records": []}

        with (
            patch.object(OntapBackend, "_cache_db", new=mock_db),
            patch.object(backend, "_get_api_client", return_value=mock_client),
            patch(
                "pynetappfoundry.data.backends.parse_api_response",
                return_value=live_all,
            ),
            _patch_metadata_path(backend),
        ):
            results = backend.query(
                FakeVolume,
                fake_volume_mapping,
                decision,
                cluster="prod1",
                filters={},
            )

        assert len(results) == 100
        assert mock_client.get_all_records.call_count == 1

    def test_partial_query_batch_size_plus_one(
        self,
        fake_volume_mapping: TypeMapping,
        mock_config: Any,
    ) -> None:
        """101 cached records should produce exactly 2 API calls (100 + 1)."""
        backend = _make_backend(mock_config)
        decision = RoutingDecision(cache_fields=("uuid",), live_fields=("iops",))
        cached = [FakeVolume(uuid=f"u{i}") for i in range(101)]
        live_chunk1 = [FakeVolume(uuid=f"u{i}", iops=float(i)) for i in range(100)]
        live_chunk2 = [FakeVolume(uuid="u100", iops=100.0)]

        mock_db = MagicMock()
        mock_db.query_with_filters.return_value = cached
        mock_client = MagicMock()
        mock_client.get_all_records.return_value = {"records": []}

        with (
            patch.object(OntapBackend, "_cache_db", new=mock_db),
            patch.object(backend, "_get_api_client", return_value=mock_client),
            patch(
                "pynetappfoundry.data.backends.parse_api_response",
                side_effect=[live_chunk1, live_chunk2],
            ),
            _patch_metadata_path(backend),
        ):
            results = backend.query(
                FakeVolume,
                fake_volume_mapping,
                decision,
                cluster="prod1",
                filters={},
            )

        assert len(results) == 101
        assert mock_client.get_all_records.call_count == 2

    def test_partial_query_custom_batch_size(
        self,
        mock_config: Any,
    ) -> None:
        """Mapping with batch_size=50 and 250 records produces 5 API calls."""
        from pynetappfoundry.cache._registry import model_registry
        from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping

        mapping = TypeMapping(
            name="SmallBatchVolume",
            model_class=FakeVolume,
            api_endpoint="/storage/small-batch?fields=*",
            api_type="ontap",
            identifier_field="uuid",
            batch_size=50,
            fields=(
                FieldMapping(cache_attr="name", cache_strategy="cache"),
                FieldMapping(cache_attr="uuid", cache_strategy="cache"),
                FieldMapping(cache_attr="size", cache_strategy="cache"),
                FieldMapping(cache_attr="iops", cache_strategy="realtime"),
                FieldMapping(cache_attr="is_root", cache_strategy="derived"),
            ),
        )
        model_registry.register_mapping("SmallBatchVolume", mapping)
        try:
            backend = _make_backend(mock_config)
            decision = RoutingDecision(cache_fields=("uuid",), live_fields=("iops",))
            cached = [FakeVolume(uuid=f"u{i}") for i in range(250)]
            live_chunks = [
                [FakeVolume(uuid=f"u{i}", iops=float(i)) for i in range(j, j + 50)]
                for j in range(0, 250, 50)
            ]

            mock_db = MagicMock()
            mock_db.query_with_filters.return_value = cached
            mock_client = MagicMock()
            mock_client.get_all_records.return_value = {"records": []}

            with (
                patch.object(OntapBackend, "_cache_db", new=mock_db),
                patch.object(backend, "_get_api_client", return_value=mock_client),
                patch(
                    "pynetappfoundry.data.backends.parse_api_response",
                    side_effect=live_chunks,
                ),
                patch.object(backend, "_resolve_metadata_path", return_value="storage.small_batch"),
            ):
                results = backend.query(
                    FakeVolume,
                    mapping,
                    decision,
                    cluster="prod1",
                    filters={},
                )

            assert len(results) == 250
            assert mock_client.get_all_records.call_count == 5
        finally:
            model_registry._mappings.pop("SmallBatchVolume", None)


class TestOntapBackendQueryPartialParentKeyed:
    """Tests for parent-keyed partial-fetch in ``_query_partial``."""

    def test_parent_keyed_single_parent_single_child(
        self,
        fake_child_mapping: TypeMapping,
        mock_config: Any,
    ) -> None:
        """One cached child under one parent; API returns updated metric."""
        backend = _make_backend(mock_config)
        decision = RoutingDecision(cache_fields=("uuid", "volume.uuid"), live_fields=("metric",))
        cached = [
            FakeChildWithDottedRef(uuid="c1", volume=FakeChildVolume(uuid="vol-1"), metric=0.0),
        ]
        live = [
            FakeChildWithDottedRef(uuid="c1", metric=42.0),
        ]

        mock_db = MagicMock()
        mock_db.query_with_filters.return_value = cached
        mock_client = MagicMock()
        mock_client.get_all_records.return_value = {"records": []}

        with (
            patch.object(OntapBackend, "_cache_db", new=mock_db),
            patch.object(backend, "_get_api_client", return_value=mock_client),
            patch(
                "pynetappfoundry.data.backends.parse_api_response",
                return_value=live,
            ),
            patch.object(backend, "_resolve_metadata_path", return_value="storage.fake_children"),
        ):
            results = backend.query(
                FakeChildWithDottedRef,
                fake_child_mapping,
                decision,
                cluster="prod1",
                filters={},
            )

        assert len(results) == 1
        assert results[0].metric == 42.0
        assert results[0].uuid == "c1"
        mock_client.get_all_records.assert_called_once()
        url = mock_client.get_all_records.call_args[0][0]
        assert "vol-1" in url
        assert "{volume.uuid}" not in url

    def test_parent_keyed_single_parent_multi_child(
        self,
        fake_child_mapping: TypeMapping,
        mock_config: Any,
    ) -> None:
        """Three children under the same parent; single API call with pipe-OR."""
        backend = _make_backend(mock_config)
        decision = RoutingDecision(cache_fields=("uuid", "volume.uuid"), live_fields=("metric",))
        cached = [
            FakeChildWithDottedRef(uuid=f"c{i}", volume=FakeChildVolume(uuid="vol-1"))
            for i in range(1, 4)
        ]
        live = [FakeChildWithDottedRef(uuid=f"c{i}", metric=float(i) * 10) for i in range(1, 4)]

        mock_db = MagicMock()
        mock_db.query_with_filters.return_value = cached
        mock_client = MagicMock()
        mock_client.get_all_records.return_value = {"records": []}

        with (
            patch.object(OntapBackend, "_cache_db", new=mock_db),
            patch.object(backend, "_get_api_client", return_value=mock_client),
            patch(
                "pynetappfoundry.data.backends.parse_api_response",
                return_value=live,
            ),
            patch.object(backend, "_resolve_metadata_path", return_value="storage.fake_children"),
        ):
            results = backend.query(
                FakeChildWithDottedRef,
                fake_child_mapping,
                decision,
                cluster="prod1",
                filters={},
            )

        assert len(results) == 3
        mock_client.get_all_records.assert_called_once()
        url = mock_client.get_all_records.call_args[0][0]
        assert "c1" in url
        assert "c2" in url
        assert "c3" in url

    def test_parent_keyed_multiple_parents(
        self,
        fake_child_mapping: TypeMapping,
        mock_config: Any,
    ) -> None:
        """Children spanning two parents; API called once per parent."""
        backend = _make_backend(mock_config)
        decision = RoutingDecision(cache_fields=("uuid", "volume.uuid"), live_fields=("metric",))
        cached = [
            FakeChildWithDottedRef(uuid="c1", volume=FakeChildVolume(uuid="vol-1")),
            FakeChildWithDottedRef(uuid="c2", volume=FakeChildVolume(uuid="vol-2")),
            FakeChildWithDottedRef(uuid="c3", volume=FakeChildVolume(uuid="vol-1")),
        ]
        live_vol1 = [
            FakeChildWithDottedRef(uuid="c1", metric=10.0),
            FakeChildWithDottedRef(uuid="c3", metric=30.0),
        ]
        live_vol2 = [
            FakeChildWithDottedRef(uuid="c2", metric=20.0),
        ]

        mock_db = MagicMock()
        mock_db.query_with_filters.return_value = cached
        mock_client = MagicMock()
        mock_client.get_all_records.return_value = {"records": []}

        with (
            patch.object(OntapBackend, "_cache_db", new=mock_db),
            patch.object(backend, "_get_api_client", return_value=mock_client),
            patch(
                "pynetappfoundry.data.backends.parse_api_response",
                side_effect=[live_vol1, live_vol2],
            ),
            patch.object(backend, "_resolve_metadata_path", return_value="storage.fake_children"),
        ):
            results = backend.query(
                FakeChildWithDottedRef,
                fake_child_mapping,
                decision,
                cluster="prod1",
                filters={},
            )

        assert len(results) == 3
        by_uuid = {r.uuid: r for r in results}
        assert by_uuid["c1"].metric == 10.0
        assert by_uuid["c2"].metric == 20.0
        assert by_uuid["c3"].metric == 30.0
        assert mock_client.get_all_records.call_count == 2
        urls = [call.args[0] for call in mock_client.get_all_records.call_args_list]
        parent_uuids_in_urls = {"vol-1" in u or "vol-2" in u for u in urls}
        assert all(parent_uuids_in_urls)

    def test_parent_keyed_missing_parent_uuid_warns(
        self,
        fake_child_mapping: TypeMapping,
        mock_config: Any,
    ) -> None:
        """Children with empty parent ref pass through unmerged; warning logged."""
        backend = _make_backend(mock_config)
        decision = RoutingDecision(cache_fields=("uuid", "volume.uuid"), live_fields=("metric",))
        cached = [
            FakeChildWithDottedRef(uuid="c1", volume=FakeChildVolume(uuid="vol-1")),
            FakeChildWithDottedRef(uuid="c2", volume=FakeChildVolume(uuid="")),
        ]
        live = [FakeChildWithDottedRef(uuid="c1", metric=10.0)]

        mock_db = MagicMock()
        mock_db.query_with_filters.return_value = cached
        mock_client = MagicMock()
        mock_client.get_all_records.return_value = {"records": []}

        with (
            patch.object(OntapBackend, "_cache_db", new=mock_db),
            patch.object(backend, "_get_api_client", return_value=mock_client),
            patch(
                "pynetappfoundry.data.backends.parse_api_response",
                return_value=live,
            ),
            patch.object(backend, "_resolve_metadata_path", return_value="storage.fake_children"),
            patch("pynetappfoundry.data.backends.logger") as mock_logger,
        ):
            results = backend.query(
                FakeChildWithDottedRef,
                fake_child_mapping,
                decision,
                cluster="prod1",
                filters={},
            )

        # c1 merged, c2 unmerged (no live data for it)
        assert len(results) == 2
        by_uuid = {r.uuid: r for r in results}
        assert by_uuid["c1"].metric == 10.0
        assert by_uuid["c2"].metric == 0.0
        mock_logger.warning.assert_called_once()
        assert "1 cached children" in mock_logger.warning.call_args[0][1] or (
            mock_logger.warning.call_args[0][2] == 1
        )

    def test_parent_keyed_cache_fallback_no_child_ref(
        self,
        fake_orphan_child_mapping: TypeMapping,
        mock_config: Any,
    ) -> None:
        """Orphan children (no parent back-ref) trigger parent cache lookup."""
        backend = _make_backend(mock_config)
        decision = RoutingDecision(cache_fields=("volume_uuid",), live_fields=("transfer_state",))
        cached = [
            FakeOrphanChild(volume_uuid="vu1", transfer_state=""),
            FakeOrphanChild(volume_uuid="vu2", transfer_state=""),
        ]
        parents = [
            FakeParentModel(uuid="p1", name="parent1"),
            FakeParentModel(uuid="p2", name="parent2"),
        ]
        live_p1 = [FakeOrphanChild(volume_uuid="vu1", transfer_state="done")]
        live_p2 = [FakeOrphanChild(volume_uuid="vu2", transfer_state="running")]

        mock_db = MagicMock()
        # First call returns children, second returns parents.
        mock_db.query_with_filters.side_effect = [cached, parents]
        mock_client = MagicMock()
        mock_client.get_all_records.return_value = {"records": []}

        with (
            patch.object(OntapBackend, "_cache_db", new=mock_db),
            patch.object(backend, "_get_api_client", return_value=mock_client),
            patch(
                "pynetappfoundry.data.backends.parse_api_response",
                side_effect=[live_p1, live_p2],
            ),
            patch.object(
                backend,
                "_resolve_metadata_path",
                side_effect=["svm.fake_orphans", "storage.fake_parents"],
            ),
        ):
            results = backend.query(
                FakeOrphanChild,
                fake_orphan_child_mapping,
                decision,
                cluster="prod1",
                filters={},
            )

        assert len(results) == 2
        assert mock_client.get_all_records.call_count == 2

    def test_parent_keyed_empty_cache_short_circuits(
        self,
        fake_child_mapping: TypeMapping,
        mock_config: Any,
    ) -> None:
        """Empty cache result returns [] with no API calls."""
        backend = _make_backend(mock_config)
        decision = RoutingDecision(cache_fields=("uuid", "volume.uuid"), live_fields=("metric",))

        mock_db = MagicMock()
        mock_db.query_with_filters.return_value = []
        mock_client = MagicMock()

        with (
            patch.object(OntapBackend, "_cache_db", new=mock_db),
            patch.object(backend, "_get_api_client", return_value=mock_client),
            patch.object(backend, "_resolve_metadata_path", return_value="storage.fake_children"),
        ):
            results = backend.query(
                FakeChildWithDottedRef,
                fake_child_mapping,
                decision,
                cluster="prod1",
                filters={},
            )

        assert results == []
        mock_client.get_all_records.assert_not_called()

    def test_parent_keyed_chunking_large_child_set(
        self,
        fake_child_mapping: TypeMapping,
        mock_config: Any,
    ) -> None:
        """1 parent with 150 children should produce 2 API calls (100 + 50)."""
        backend = _make_backend(mock_config)
        decision = RoutingDecision(cache_fields=("uuid", "volume.uuid"), live_fields=("metric",))
        cached = [
            FakeChildWithDottedRef(uuid=f"c{i}", volume=FakeChildVolume(uuid="vol-1"), metric=0.0)
            for i in range(150)
        ]
        live_chunk1 = [FakeChildWithDottedRef(uuid=f"c{i}", metric=float(i)) for i in range(100)]
        live_chunk2 = [
            FakeChildWithDottedRef(uuid=f"c{i}", metric=float(i)) for i in range(100, 150)
        ]

        mock_db = MagicMock()
        mock_db.query_with_filters.return_value = cached
        mock_client = MagicMock()
        mock_client.get_all_records.return_value = {"records": []}

        with (
            patch.object(OntapBackend, "_cache_db", new=mock_db),
            patch.object(backend, "_get_api_client", return_value=mock_client),
            patch(
                "pynetappfoundry.data.backends.parse_api_response",
                side_effect=[live_chunk1, live_chunk2],
            ),
            patch.object(backend, "_resolve_metadata_path", return_value="storage.fake_children"),
        ):
            results = backend.query(
                FakeChildWithDottedRef,
                fake_child_mapping,
                decision,
                cluster="prod1",
                filters={},
            )

        assert len(results) == 150
        assert mock_client.get_all_records.call_count == 2

    def test_extract_parent_ref_field(self) -> None:
        """Unit test for _extract_parent_ref_field with various URL patterns."""
        from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping

        def _mapping_with_endpoint(endpoint: str) -> TypeMapping:
            return TypeMapping(
                name="Test",
                model_class=FakeVolume,
                api_endpoint=endpoint,
                api_type="ontap",
                fields=(FieldMapping(cache_attr="uuid"),),
            )

        assert (
            OntapBackend._extract_parent_ref_field(
                _mapping_with_endpoint("/storage/volumes/{volume.uuid}/snapshots?fields=*")
            )
            == "volume.uuid"
        )
        assert (
            OntapBackend._extract_parent_ref_field(
                _mapping_with_endpoint("/svm/migrations/{svm_migration.uuid}/volumes?fields=*")
            )
            == "svm_migration.uuid"
        )
        assert (
            OntapBackend._extract_parent_ref_field(
                _mapping_with_endpoint("/snapmirror/relationships/{relationship.uuid}/transfers")
            )
            == "relationship.uuid"
        )
        assert (
            OntapBackend._extract_parent_ref_field(_mapping_with_endpoint("/storage/volumes"))
            is None
        )


class TestQueryWithWhereExpressions:
    """Tests for ``where_expressions`` kwarg on :meth:`OntapBackend.query`."""

    def test_cache_path_concatenates_filter_dict_with_where_exprs(
        self,
        fake_volume_mapping: TypeMapping,
        mock_config: Any,
    ) -> None:
        backend = _make_backend(mock_config)
        decision = RoutingDecision(cache_fields=("name", "uuid"), live_fields=())

        mock_db = MagicMock()
        mock_db.query_with_filters.return_value = []

        with (
            patch.object(OntapBackend, "_cache_db", new=mock_db),
            _patch_metadata_path(backend),
        ):
            backend.query(
                FakeVolume,
                fake_volume_mapping,
                decision,
                cluster="prod1",
                filters={"svm.name": "vs1"},
                where_expressions=("size > 1000000000",),
            )

        mock_db.query_with_filters.assert_called_once_with(
            "prod1",
            "storage.fake_volumes",
            ["svm.name = 'vs1'", "size > 1000000000"],
        )

    def test_cache_path_where_only(
        self,
        fake_volume_mapping: TypeMapping,
        mock_config: Any,
    ) -> None:
        backend = _make_backend(mock_config)
        decision = RoutingDecision(cache_fields=("name", "uuid"), live_fields=())

        mock_db = MagicMock()
        mock_db.query_with_filters.return_value = []

        with (
            patch.object(OntapBackend, "_cache_db", new=mock_db),
            _patch_metadata_path(backend),
        ):
            backend.query(
                FakeVolume,
                fake_volume_mapping,
                decision,
                cluster="prod1",
                filters={},
                where_expressions=("size > 0",),
            )

        mock_db.query_with_filters.assert_called_once_with(
            "prod1", "storage.fake_volumes", ["size > 0"]
        )

    def test_cache_path_no_where_unchanged(
        self,
        fake_volume_mapping: TypeMapping,
        mock_config: Any,
    ) -> None:
        backend = _make_backend(mock_config)
        decision = RoutingDecision(cache_fields=("name", "uuid"), live_fields=())

        mock_db = MagicMock()
        mock_db.query_with_filters.return_value = []

        with (
            patch.object(OntapBackend, "_cache_db", new=mock_db),
            _patch_metadata_path(backend),
        ):
            backend.query(
                FakeVolume,
                fake_volume_mapping,
                decision,
                cluster="prod1",
                filters={"svm.name": "vs1"},
            )

        mock_db.query_with_filters.assert_called_once_with(
            "prod1", "storage.fake_volumes", ["svm.name = 'vs1'"]
        )

    def test_live_path_raises_when_where_used(
        self,
        fake_volume_mapping: TypeMapping,
        mock_config: Any,
    ) -> None:
        backend = _make_backend(mock_config)
        decision = RoutingDecision(cache_fields=(), live_fields=("iops",))

        with pytest.raises(NotImplementedError, match=r"\.filter") as exc_info:
            backend.query(
                FakeVolume,
                fake_volume_mapping,
                decision,
                cluster="prod1",
                filters={},
                where_expressions=("iops > 100",),
            )
        assert "#512" in str(exc_info.value)

    def test_live_path_no_where_unchanged(
        self,
        fake_volume_mapping: TypeMapping,
        mock_config: Any,
    ) -> None:
        backend = _make_backend(mock_config)
        decision = RoutingDecision(cache_fields=(), live_fields=("iops",))

        mock_client = MagicMock()
        mock_client.get_all_records.return_value = {"records": []}

        with (
            patch.object(backend, "_get_api_client", return_value=mock_client),
            patch(
                "pynetappfoundry.data.backends.parse_api_response",
                return_value=[],
            ),
        ):
            result = backend.query(
                FakeVolume,
                fake_volume_mapping,
                decision,
                cluster="prod1",
                filters={},
            )

        assert result == []
        mock_client.get_all_records.assert_called_once()

    def test_partial_path_raises_when_where_used(
        self,
        fake_volume_mapping: TypeMapping,
        mock_config: Any,
    ) -> None:
        backend = _make_backend(mock_config)
        decision = RoutingDecision(cache_fields=("name",), live_fields=("iops",))

        with pytest.raises(NotImplementedError, match="source='cache'"):
            backend.query(
                FakeVolume,
                fake_volume_mapping,
                decision,
                cluster="prod1",
                filters={},
                where_expressions=("size > 0",),
            )

    def test_partial_path_no_where_unchanged(
        self,
        fake_volume_mapping: TypeMapping,
        mock_config: Any,
    ) -> None:
        backend = _make_backend(mock_config)
        decision = RoutingDecision(cache_fields=("name",), live_fields=("iops",))

        mock_db = MagicMock()
        mock_db.query_with_filters.return_value = []
        mock_client = MagicMock()

        with (
            patch.object(OntapBackend, "_cache_db", new=mock_db),
            patch.object(backend, "_get_api_client", return_value=mock_client),
            _patch_metadata_path(backend),
        ):
            result = backend.query(
                FakeVolume,
                fake_volume_mapping,
                decision,
                cluster="prod1",
                filters={"name": "v1"},
            )

        assert result == []
        mock_db.query_with_filters.assert_called_once()


class TestCountLive:
    """Tests for :meth:`OntapBackend._count_live`.

    Counts route through ``call_endpoint`` (NOT ``get_all_records``) so
    the live API can return ``num_records`` without sending the records.
    """

    def test_count_live_returns_num_records(
        self,
        fake_volume_mapping: TypeMapping,
        mock_config: Any,
    ) -> None:
        backend = _make_backend(mock_config)
        mock_client = MagicMock()
        mock_client.call_endpoint.return_value = {"num_records": 42}

        with patch.object(backend, "_get_api_client", return_value=mock_client):
            result = backend._count_live(fake_volume_mapping, "prod1", {})

        assert result == 42
        mock_client.call_endpoint.assert_called_once()
        mock_client.get_all_records.assert_not_called()

    def test_count_live_empty_response_returns_zero(
        self,
        fake_volume_mapping: TypeMapping,
        mock_config: Any,
    ) -> None:
        backend = _make_backend(mock_config)
        mock_client = MagicMock()
        mock_client.call_endpoint.return_value = {}

        with patch.object(backend, "_get_api_client", return_value=mock_client):
            result = backend._count_live(fake_volume_mapping, "prod1", {})

        assert result == 0

    def test_count_live_none_response_returns_zero(
        self,
        fake_volume_mapping: TypeMapping,
        mock_config: Any,
    ) -> None:
        backend = _make_backend(mock_config)
        mock_client = MagicMock()
        mock_client.call_endpoint.return_value = None

        with patch.object(backend, "_get_api_client", return_value=mock_client):
            result = backend._count_live(fake_volume_mapping, "prod1", {})

        assert result == 0

    def test_count_live_url_includes_return_records_false(
        self,
        fake_volume_mapping: TypeMapping,
        mock_config: Any,
    ) -> None:
        backend = _make_backend(mock_config)
        mock_client = MagicMock()
        mock_client.call_endpoint.return_value = {"num_records": 0}

        with patch.object(backend, "_get_api_client", return_value=mock_client):
            backend._count_live(fake_volume_mapping, "prod1", {})

        url = mock_client.call_endpoint.call_args[0][0]
        assert "return_records=false" in url

    def test_count_live_filters_in_url(
        self,
        fake_volume_mapping: TypeMapping,
        mock_config: Any,
    ) -> None:
        backend = _make_backend(mock_config)
        mock_client = MagicMock()
        mock_client.call_endpoint.return_value = {"num_records": 0}

        with patch.object(backend, "_get_api_client", return_value=mock_client):
            backend._count_live(
                fake_volume_mapping,
                "prod1",
                {"svm.name": "vs1"},
            )

        url = mock_client.call_endpoint.call_args[0][0]
        assert "svm.name=vs1" in url


class TestBuildLiveUrlFieldsStar:
    """Tests for :meth:`OntapBackend._build_live_url` preserving ``fields=*``."""

    def test_fields_star_preserved_when_base_endpoint_has_star(
        self,
        fake_volume_mapping: TypeMapping,
        mock_config: Any,
    ) -> None:
        """When api_endpoint has ``fields=*``, _build_live_url must not
        overwrite it with enumerated field names (#522)."""
        backend = _make_backend(mock_config)
        url = backend._build_live_url(
            fake_volume_mapping,
            params={"svm.name": "vs1"},
            live_field_paths=("iops",),
        )
        # fields=* must survive; must NOT become fields=iops
        assert "fields=%2A" in url or "fields=*" in url
        assert "fields=iops" not in url
        assert "svm.name=vs1" in url

    def test_fields_enumerated_when_base_endpoint_has_no_star(
        self,
        mock_config: Any,
    ) -> None:
        """When api_endpoint does NOT have ``fields=*``, _build_live_url
        must enumerate individual field api_paths as before."""
        from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping

        mapping = TypeMapping(
            name="NoStar",
            model_class=FakeVolume,
            api_endpoint="/storage/volumes",
            api_type="ontap",
            identifier_field="uuid",
            fields=(
                FieldMapping(cache_attr="uuid", cache_strategy="cache"),
                FieldMapping(cache_attr="iops", cache_strategy="realtime"),
            ),
        )
        backend = _make_backend(mock_config)
        url = backend._build_live_url(
            mapping,
            params={},
            live_field_paths=("iops",),
        )
        assert "fields=iops" in url

    def test_fields_star_preserved_with_return_records_false(
        self,
        fake_volume_mapping: TypeMapping,
        mock_config: Any,
    ) -> None:
        """Preserve ``fields=*`` even when return_records=False."""
        backend = _make_backend(mock_config)
        url = backend._build_live_url(
            fake_volume_mapping,
            params={},
            live_field_paths=("iops",),
            return_records=False,
        )
        assert "fields=%2A" in url or "fields=*" in url
        assert "return_records=false" in url


# ---------------------------------------------------------------------------
# CLI backend dispatch (#532)
# ---------------------------------------------------------------------------


class TestOntapBackendCliDispatch:
    """Tests for CLI-only mapping dispatch through ``OntapBackend.query()``."""

    def test_cli_mapping_dispatches_to_fetch_with_cli_client(
        self,
        mock_config: Any,
    ) -> None:
        """Cloud cluster + CLI-only mapping delegates to ``fetch()`` with cli_client."""
        from pynetappfoundry.cache.ontap.cloud.metadata.mapping import CLOUD_METADATA_MAPPING
        from pynetappfoundry.models.ontap.cloud.metadata.model import CloudMetadata

        backend = _make_backend(mock_config)
        live_fields = tuple(
            f.cache_attr for f in CLOUD_METADATA_MAPPING.fields if f.cache_strategy != "derived"
        )
        decision = RoutingDecision(cache_fields=(), live_fields=live_fields)

        mock_cli = MagicMock()
        fetched = [CloudMetadata(node="n1", provider="AWS")]

        with (
            patch.object(backend, "_is_cloud_cluster", return_value=True),
            patch.object(backend, "_get_cli_client", return_value=mock_cli),
            patch.object(backend, "_get_api_client", return_value=MagicMock()),
            patch("pynetappfoundry.data.backends.fetch", return_value=fetched) as fetch_mock,
        ):
            results = backend.query(
                CloudMetadata,
                CLOUD_METADATA_MAPPING,
                decision,
                cluster="cloud1",
                filters={},
            )

        assert results == fetched
        fetch_mock.assert_called_once()
        assert fetch_mock.call_args.kwargs["cli_client"] is mock_cli

    def test_cli_mapping_skips_non_cloud_cluster(
        self,
        mock_config: Any,
    ) -> None:
        """Non-cloud cluster returns empty list for CLI-only mappings."""
        from pynetappfoundry.cache.ontap.cloud.metadata.mapping import CLOUD_METADATA_MAPPING
        from pynetappfoundry.models.ontap.cloud.metadata.model import CloudMetadata

        backend = _make_backend(mock_config)
        live_fields = tuple(
            f.cache_attr for f in CLOUD_METADATA_MAPPING.fields if f.cache_strategy != "derived"
        )
        decision = RoutingDecision(cache_fields=(), live_fields=live_fields)

        with patch.object(backend, "_is_cloud_cluster", return_value=False):
            results = backend.query(
                CloudMetadata,
                CLOUD_METADATA_MAPPING,
                decision,
                cluster="onprem1",
                filters={},
            )

        assert results == []


# ---------------------------------------------------------------------------
# _get_api_client IP resolution (#740)
# ---------------------------------------------------------------------------


class TestGetApiClient:
    """Tests for :meth:`OntapBackend._get_api_client` IP resolution.

    Verifies that the client is constructed with the configured IP address
    rather than the cluster name, mirroring the pattern in ``_get_cli_client``.
    """

    def test_uses_configured_ip(self, mock_config: Any) -> None:
        """ClusterConfig.ip uses the ``ip`` key from the clusters config."""
        mock_config.data = {"clusters": {"cl1": {"ip": "10.0.0.5"}}}
        backend = _make_backend(mock_config)

        with patch(
            "pynetappfoundry.clients.ontap.api.ONTAPAPIClient.__init__",
            return_value=None,
        ) as mock_init:
            backend._get_api_client("cl1")

        mock_init.assert_called_once()
        cluster_arg = mock_init.call_args.kwargs["cluster"]
        assert cluster_arg.name == "cl1"
        assert cluster_arg.ip == "10.0.0.5"

    def test_falls_back_to_cluster_name_when_ip_absent(self, mock_config: Any) -> None:
        """ClusterConfig.ip falls back to the cluster name when no ``ip`` key is present."""
        mock_config.data = {"clusters": {"cl1": {}}}
        backend = _make_backend(mock_config)

        with patch(
            "pynetappfoundry.clients.ontap.api.ONTAPAPIClient.__init__",
            return_value=None,
        ) as mock_init:
            backend._get_api_client("cl1")

        mock_init.assert_called_once()
        cluster_arg = mock_init.call_args.kwargs["cluster"]
        assert cluster_arg.name == "cl1"
        assert cluster_arg.ip == "cl1"
