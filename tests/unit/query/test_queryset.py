"""Tests for pynetappfoundry.query.queryset module."""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock, patch

import pytest
from pydantic import BaseModel

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.core.config import Config
from pynetappfoundry.query.exceptions import MultipleResultsError, NotFoundError
from pynetappfoundry.query.queryset import QuerySet

# ---------------------------------------------------------------------------
# Test model and mapping fixtures
# ---------------------------------------------------------------------------


class FakeVolume(BaseModel):
    """Minimal model for testing."""

    name: str = ""
    uuid: str = ""
    svm_name: str = ""
    state: str = ""


FAKE_FIELDS = (
    FieldMapping(cache_attr="name", api_path="name"),
    FieldMapping(cache_attr="uuid", api_path="uuid"),
    FieldMapping(cache_attr="svm_name", api_path="svm.name"),
    FieldMapping(cache_attr="state", api_path="state"),
)

FAKE_MAPPING = TypeMapping(
    name="FakeVolume",
    model_class=FakeVolume,
    api_endpoint="/storage/volumes?fields=*",
    fields=FAKE_FIELDS,
    id_field="name",
)


@pytest.fixture(autouse=True)
def _register_fake_mapping() -> Any:
    """Register FakeVolume mapping and clean up after test."""
    model_registry.register_mapping("FakeVolume", FAKE_MAPPING)
    yield
    # Remove the mapping after test to avoid leaking into other tests
    model_registry._mappings.pop("FakeVolume", None)


@pytest.fixture()
def mock_client() -> MagicMock:
    """Return a mocked APIWrapper with a name attribute."""
    client = MagicMock(spec=["get_all_records", "call_endpoint", "name"])
    client.name = "test-cluster"
    return client


@pytest.fixture()
def mock_config() -> MagicMock:
    """Return a mocked Config."""
    return MagicMock(spec=Config)


# ---------------------------------------------------------------------------
# Shared helper to build a QuerySet with mocked DataSource
# ---------------------------------------------------------------------------


def _make_qs(
    config: MagicMock,
    client: MagicMock,
) -> tuple[QuerySet, MagicMock, MagicMock]:
    """Build a QuerySet with mocked DataSource internals.

    Returns ``(qs, mock_data_source, mock_backend)``.
    """
    mock_backend = MagicMock()
    mock_backend._api_clients = {}

    mock_data_source = MagicMock()
    mock_data_source._get_backend.return_value = mock_backend

    with patch(
        "pynetappfoundry.query.queryset.DataSource",
        return_value=mock_data_source,
    ):
        qs = QuerySet(FakeVolume, client, config=config)
    return qs, mock_data_source, mock_backend


def _set_query_results(mock_data_source: MagicMock, results: list[Any]) -> MagicMock:
    """Wire ``mock_data_source.query(...)`` to a chainable builder mock.

    The returned builder iterates over *results*. Returns the builder
    mock so tests can assert on its ``.filter`` / ``.fields`` calls.
    """
    builder = MagicMock()
    builder.filter.return_value = builder
    builder.fields.return_value = builder
    builder.__iter__ = lambda self: iter(results)
    mock_data_source.query.return_value = builder
    return builder


# ---------------------------------------------------------------------------
# Constructor tests
# ---------------------------------------------------------------------------


class TestQuerySetInit:
    """Tests for QuerySet.__init__."""

    def test_init_with_valid_mapping(self, mock_config: MagicMock, mock_client: MagicMock) -> None:
        qs, _ds, _backend = _make_qs(mock_config, mock_client)
        assert qs._mapping is FAKE_MAPPING
        assert qs._client is mock_client

    def test_init_with_missing_mapping(
        self, mock_config: MagicMock, mock_client: MagicMock
    ) -> None:
        class Unregistered(BaseModel):
            pass

        with (
            pytest.raises(ValueError, match="No TypeMapping registered for 'Unregistered'"),
            patch("pynetappfoundry.query.queryset.DataSource"),
        ):
            QuerySet(Unregistered, mock_client, config=mock_config)


# ---------------------------------------------------------------------------
# Chaining tests
# ---------------------------------------------------------------------------


class TestQuerySetChaining:
    """Tests for chaining methods."""

    def test_filter_translates_attr_to_api_path(
        self, mock_config: MagicMock, mock_client: MagicMock
    ) -> None:
        qs, _ds, _backend = _make_qs(mock_config, mock_client)
        filtered = qs.filter(svm_name="vs1")
        assert filtered._filters == {"svm.name": "vs1"}

    def test_filter_passthrough_unknown_attr(
        self, mock_config: MagicMock, mock_client: MagicMock
    ) -> None:
        qs, _ds, _backend = _make_qs(mock_config, mock_client)
        filtered = qs.filter(unknown_field="val")
        assert filtered._filters == {"unknown_field": "val"}

    def test_filter_passthrough_dotted_path(
        self, mock_config: MagicMock, mock_client: MagicMock
    ) -> None:
        """Dotted paths are passed through unchanged (dunder rewrite removed)."""
        qs, _ds, _backend = _make_qs(mock_config, mock_client)
        filtered = qs.filter(**{"svm.name": "vs1"})
        assert filtered._filters == {"svm.name": "vs1"}

    def test_chaining_returns_new_instance(
        self, mock_config: MagicMock, mock_client: MagicMock
    ) -> None:
        qs1, _ds, _backend = _make_qs(mock_config, mock_client)
        qs2 = qs1.filter(name="vol1")
        assert qs1 is not qs2
        assert qs1._filters == {}
        assert qs2._filters == {"name": "vol1"}

    def test_chaining_accumulates_filters(
        self, mock_config: MagicMock, mock_client: MagicMock
    ) -> None:
        qs, _ds, _backend = _make_qs(mock_config, mock_client)
        filtered = qs.filter(svm_name="vs1").filter(state="online")
        assert filtered._filters == {"svm.name": "vs1", "state": "online"}

    def test_fields_sets_projection(self, mock_config: MagicMock, mock_client: MagicMock) -> None:
        qs, _ds, _backend = _make_qs(mock_config, mock_client)
        projected = qs.fields("name", "uuid")
        assert projected._fields_list == ["name", "uuid"]

    def test_fields_translates_attrs(self, mock_config: MagicMock, mock_client: MagicMock) -> None:
        qs, _ds, _backend = _make_qs(mock_config, mock_client)
        projected = qs.fields("svm_name")
        assert projected._fields_list == ["svm.name"]

    def test_order_by_translates_attr(self, mock_config: MagicMock, mock_client: MagicMock) -> None:
        qs, _ds, _backend = _make_qs(mock_config, mock_client)
        ordered = qs.order_by("name asc")
        assert ordered._order_by_list == ["name asc"]

    def test_order_by_translates_compound_attr(
        self, mock_config: MagicMock, mock_client: MagicMock
    ) -> None:
        qs, _ds, _backend = _make_qs(mock_config, mock_client)
        ordered = qs.order_by("svm_name desc")
        assert ordered._order_by_list == ["svm.name desc"]

    def test_limit_sets_max_records(self, mock_config: MagicMock, mock_client: MagicMock) -> None:
        qs, _ds, _backend = _make_qs(mock_config, mock_client)
        limited = qs.limit(10)
        assert limited._max_records == 10


# ---------------------------------------------------------------------------
# URL building tests (_build_url is retained for internal use)
# ---------------------------------------------------------------------------


class TestQuerySetBuildUrl:
    """Tests for _build_url."""

    def test_base_url_from_mapping(self, mock_config: MagicMock, mock_client: MagicMock) -> None:
        qs, _ds, _backend = _make_qs(mock_config, mock_client)
        url = qs._build_url()
        assert url.startswith("/storage/volumes")
        assert "fields=%2A" in url or "fields=*" in url

    def test_filter_added_to_url(self, mock_config: MagicMock, mock_client: MagicMock) -> None:
        qs, _ds, _backend = _make_qs(mock_config, mock_client)
        qs = qs.filter(svm_name="vs1")
        url = qs._build_url()
        assert "svm.name=vs1" in url

    def test_fields_override_default(self, mock_config: MagicMock, mock_client: MagicMock) -> None:
        qs, _ds, _backend = _make_qs(mock_config, mock_client)
        qs = qs.fields("name", "uuid")
        url = qs._build_url()
        assert "fields=name" in url
        assert "uuid" in url
        assert "fields=%2A" not in url or "fields=name" in url

    def test_order_by_in_url(self, mock_config: MagicMock, mock_client: MagicMock) -> None:
        qs, _ds, _backend = _make_qs(mock_config, mock_client)
        qs = qs.order_by("name asc")
        url = qs._build_url()
        assert "order_by=" in url

    def test_limit_in_url(self, mock_config: MagicMock, mock_client: MagicMock) -> None:
        qs, _ds, _backend = _make_qs(mock_config, mock_client)
        qs = qs.limit(5)
        url = qs._build_url()
        assert "max_records=5" in url

    def test_return_records_false(self, mock_config: MagicMock, mock_client: MagicMock) -> None:
        qs, _ds, _backend = _make_qs(mock_config, mock_client)
        url = qs._build_url(return_records=False)
        assert "return_records=false" in url


# ---------------------------------------------------------------------------
# Terminal method tests (all via DataSource)
# ---------------------------------------------------------------------------


class TestQuerySetAll:
    """Tests for .all() terminal method."""

    def test_all_routes_through_datasource(
        self, mock_config: MagicMock, mock_client: MagicMock
    ) -> None:
        qs, ds, _backend = _make_qs(mock_config, mock_client)
        vol = FakeVolume(name="vol1", uuid="abc")
        builder = _set_query_results(ds, [vol])

        results = qs.all()

        assert results == [vol]
        ds.query.assert_called_once_with(FakeVolume, cluster="test-cluster", source="live")
        builder.filter.assert_called_once_with({})

    def test_all_returns_typed_models(self, mock_config: MagicMock, mock_client: MagicMock) -> None:
        qs, ds, _backend = _make_qs(mock_config, mock_client)
        vol = FakeVolume(name="vol1", uuid="abc", svm_name="vs1", state="online")
        _set_query_results(ds, [vol])

        results = qs.all()
        assert len(results) == 1
        assert isinstance(results[0], FakeVolume)
        assert results[0].name == "vol1"
        assert results[0].svm_name == "vs1"

    def test_all_empty_response(self, mock_config: MagicMock, mock_client: MagicMock) -> None:
        qs, ds, _backend = _make_qs(mock_config, mock_client)
        _set_query_results(ds, [])
        results = qs.all()
        assert results == []


class TestQuerySetFirst:
    """Tests for .first() terminal method."""

    def test_first_returns_instance(self, mock_config: MagicMock, mock_client: MagicMock) -> None:
        qs, ds, _backend = _make_qs(mock_config, mock_client)
        vol = FakeVolume(name="vol1")
        _set_query_results(ds, [vol])

        result = qs.first()
        assert result is vol

    def test_first_returns_none_on_empty(
        self, mock_config: MagicMock, mock_client: MagicMock
    ) -> None:
        qs, ds, _backend = _make_qs(mock_config, mock_client)
        _set_query_results(ds, [])
        result = qs.first()
        assert result is None

    def test_first_uses_limit_one(self, mock_config: MagicMock, mock_client: MagicMock) -> None:
        qs, ds, _backend = _make_qs(mock_config, mock_client)
        builder = _set_query_results(ds, [])

        qs.first()
        builder.filter.assert_called_once_with({"max_records": "1"})


class TestQuerySetGet:
    """Tests for .get() terminal method."""

    def test_get_returns_single(self, mock_config: MagicMock, mock_client: MagicMock) -> None:
        qs, ds, _backend = _make_qs(mock_config, mock_client)
        vol = FakeVolume(name="vol1", uuid="abc")
        _set_query_results(ds, [vol])

        result = qs.get(uuid="abc")
        assert result is vol

    def test_get_raises_not_found(self, mock_config: MagicMock, mock_client: MagicMock) -> None:
        qs, ds, _backend = _make_qs(mock_config, mock_client)
        _set_query_results(ds, [])

        with pytest.raises(NotFoundError, match="FakeVolume"):
            qs.get(uuid="missing")

    def test_get_raises_multiple_results(
        self, mock_config: MagicMock, mock_client: MagicMock
    ) -> None:
        qs, ds, _backend = _make_qs(mock_config, mock_client)
        _set_query_results(ds, [FakeVolume(name="vol1"), FakeVolume(name="vol2")])

        with pytest.raises(MultipleResultsError, match="2"):
            qs.get(svm_name="vs1")


class TestQuerySetCount:
    """Tests for .count() terminal method."""

    def test_count_calls_backend_count_live(
        self, mock_config: MagicMock, mock_client: MagicMock
    ) -> None:
        qs, _ds, backend = _make_qs(mock_config, mock_client)
        backend._count_live.return_value = 42

        result = qs.count()

        assert result == 42
        backend._count_live.assert_called_once_with(FAKE_MAPPING, "test-cluster", {})

    def test_count_with_filters(self, mock_config: MagicMock, mock_client: MagicMock) -> None:
        qs, _ds, backend = _make_qs(mock_config, mock_client)
        backend._count_live.return_value = 5

        result = qs.filter(svm_name="vs1").count()
        assert result == 5
        backend._count_live.assert_called_once_with(
            FAKE_MAPPING, "test-cluster", {"svm.name": "vs1"}
        )


class TestQuerySetIter:
    """Tests for __iter__."""

    def test_iter_works(self, mock_config: MagicMock, mock_client: MagicMock) -> None:
        qs, ds, _backend = _make_qs(mock_config, mock_client)
        vols = [FakeVolume(name="v1"), FakeVolume(name="v2")]
        _set_query_results(ds, vols)

        names = [v.name for v in qs]
        assert names == ["v1", "v2"]


# ---------------------------------------------------------------------------
# Exception tests
# ---------------------------------------------------------------------------


class TestExceptions:
    """Tests for NotFoundError and MultipleResultsError."""

    def test_not_found_error_message(self) -> None:
        err = NotFoundError("Volume", {"name": "missing"})
        assert "Volume" in str(err)
        assert "missing" in str(err)
        assert err.model_name == "Volume"
        assert err.filters == {"name": "missing"}

    def test_multiple_results_error_message(self) -> None:
        err = MultipleResultsError("Volume", 3, {"svm.name": "vs1"})
        assert "3" in str(err)
        assert "Volume" in str(err)
        assert err.count == 3
        assert err.filters == {"svm.name": "vs1"}


# ---------------------------------------------------------------------------
# DataSource routing tests
# ---------------------------------------------------------------------------


class TestQuerySetRouting:
    """Tests for DataSource routing."""

    def test_api_client_injection(self, mock_config: MagicMock, mock_client: MagicMock) -> None:
        _qs, _ds, backend = _make_qs(mock_config, mock_client)
        assert backend._api_clients["test-cluster"] is mock_client

    def test_cluster_name_derived_from_client_name(
        self, mock_config: MagicMock, mock_client: MagicMock
    ) -> None:
        qs, _ds, _backend = _make_qs(mock_config, mock_client)
        assert qs._cluster_name == "test-cluster"

    def test_filter_with_dotted_path(self, mock_config: MagicMock, mock_client: MagicMock) -> None:
        """Dotted paths are passed through to DataSource filter."""
        qs, ds, _backend = _make_qs(mock_config, mock_client)
        builder = _set_query_results(ds, [])

        qs.filter(**{"svm.name": "vs1"}).all()
        builder.filter.assert_called_once_with({"svm.name": "vs1"})

    def test_order_by_translates_to_filter_entry(
        self, mock_config: MagicMock, mock_client: MagicMock
    ) -> None:
        qs, ds, _backend = _make_qs(mock_config, mock_client)
        builder = _set_query_results(ds, [])

        qs.order_by("name asc").all()
        builder.filter.assert_called_once_with({"order_by": "name asc"})

    def test_limit_translates_to_max_records_entry(
        self, mock_config: MagicMock, mock_client: MagicMock
    ) -> None:
        qs, ds, _backend = _make_qs(mock_config, mock_client)
        builder = _set_query_results(ds, [])

        qs.limit(10).all()
        builder.filter.assert_called_once_with({"max_records": "10"})

    def test_fields_routes_into_builder(
        self, mock_config: MagicMock, mock_client: MagicMock
    ) -> None:
        qs, ds, _backend = _make_qs(mock_config, mock_client)
        builder = _set_query_results(ds, [])

        qs.fields("name", "svm_name").all()
        builder.fields.assert_called_once_with("name", "svm.name")

    def test_clone_preserves_data_source(
        self, mock_config: MagicMock, mock_client: MagicMock
    ) -> None:
        qs, ds, _backend = _make_qs(mock_config, mock_client)
        clone = qs.filter(svm_name="vs1")
        assert clone._data_source is ds
        assert clone._cluster_name == "test-cluster"
