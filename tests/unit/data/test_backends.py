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
        assert "fields=iops" in url

    def test_partial_query_identifier_extract_single_key(self) -> None:
        instances = [
            FakeVolume(uuid="u1"),
            FakeVolume(uuid="u2"),
            FakeVolume(uuid="u3"),
        ]
        ids = OntapBackend._extract_identifiers(instances, "uuid")
        assert ids == ["u1", "u2", "u3"]

    def test_partial_query_identifier_index_builds_correct_keys(self) -> None:
        instances = [
            FakeVolume(uuid="u1", iops=1.0),
            FakeVolume(uuid="u2", iops=2.0),
        ]
        index = OntapBackend._build_identifier_index(instances, "uuid")
        assert set(index.keys()) == {"u1", "u2"}
        assert index["u1"].iops == 1.0
        assert index["u2"].iops == 2.0

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
