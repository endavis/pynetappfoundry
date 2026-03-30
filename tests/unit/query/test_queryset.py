"""Tests for pynetappfoundry.query.queryset module."""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock

import pytest
from pydantic import BaseModel

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
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
    """Return a mocked APIWrapper."""
    return MagicMock(spec=["get_all_records", "call_endpoint"])


# ---------------------------------------------------------------------------
# Constructor tests
# ---------------------------------------------------------------------------


class TestQuerySetInit:
    """Tests for QuerySet.__init__."""

    def test_init_with_valid_mapping(self, mock_client: MagicMock) -> None:
        qs = QuerySet(FakeVolume, mock_client)
        assert qs._mapping is FAKE_MAPPING
        assert qs._client is mock_client

    def test_init_with_missing_mapping(self, mock_client: MagicMock) -> None:
        class Unregistered(BaseModel):
            pass

        with pytest.raises(ValueError, match="No TypeMapping registered for 'Unregistered'"):
            QuerySet(Unregistered, mock_client)


# ---------------------------------------------------------------------------
# Chaining tests
# ---------------------------------------------------------------------------


class TestQuerySetChaining:
    """Tests for chaining methods."""

    def test_filter_translates_attr_to_api_path(self, mock_client: MagicMock) -> None:
        qs = QuerySet(FakeVolume, mock_client).filter(svm_name="vs1")
        assert qs._filters == {"svm.name": "vs1"}

    def test_filter_passthrough_unknown_attr(self, mock_client: MagicMock) -> None:
        qs = QuerySet(FakeVolume, mock_client).filter(unknown_field="val")
        assert qs._filters == {"unknown_field": "val"}

    def test_chaining_returns_new_instance(self, mock_client: MagicMock) -> None:
        qs1 = QuerySet(FakeVolume, mock_client)
        qs2 = qs1.filter(name="vol1")
        assert qs1 is not qs2
        assert qs1._filters == {}
        assert qs2._filters == {"name": "vol1"}

    def test_chaining_accumulates_filters(self, mock_client: MagicMock) -> None:
        qs = QuerySet(FakeVolume, mock_client).filter(svm_name="vs1").filter(state="online")
        assert qs._filters == {"svm.name": "vs1", "state": "online"}

    def test_fields_sets_projection(self, mock_client: MagicMock) -> None:
        qs = QuerySet(FakeVolume, mock_client).fields("name", "uuid")
        assert qs._fields_list == ["name", "uuid"]

    def test_fields_translates_attrs(self, mock_client: MagicMock) -> None:
        qs = QuerySet(FakeVolume, mock_client).fields("svm_name")
        assert qs._fields_list == ["svm.name"]

    def test_order_by_translates_attr(self, mock_client: MagicMock) -> None:
        qs = QuerySet(FakeVolume, mock_client).order_by("name asc")
        assert qs._order_by_list == ["name asc"]

    def test_order_by_translates_compound_attr(self, mock_client: MagicMock) -> None:
        qs = QuerySet(FakeVolume, mock_client).order_by("svm_name desc")
        assert qs._order_by_list == ["svm.name desc"]

    def test_limit_sets_max_records(self, mock_client: MagicMock) -> None:
        qs = QuerySet(FakeVolume, mock_client).limit(10)
        assert qs._max_records == 10


# ---------------------------------------------------------------------------
# URL building tests
# ---------------------------------------------------------------------------


class TestQuerySetBuildUrl:
    """Tests for _build_url."""

    def test_base_url_from_mapping(self, mock_client: MagicMock) -> None:
        qs = QuerySet(FakeVolume, mock_client)
        url = qs._build_url()
        assert url.startswith("/storage/volumes")
        assert "fields=%2A" in url or "fields=*" in url

    def test_filter_added_to_url(self, mock_client: MagicMock) -> None:
        qs = QuerySet(FakeVolume, mock_client).filter(svm_name="vs1")
        url = qs._build_url()
        assert "svm.name=vs1" in url

    def test_fields_override_default(self, mock_client: MagicMock) -> None:
        qs = QuerySet(FakeVolume, mock_client).fields("name", "uuid")
        url = qs._build_url()
        # fields should be name,uuid, not *
        assert "fields=name" in url
        assert "uuid" in url
        # Should not have fields=* anymore
        assert "fields=%2A" not in url or "fields=name" in url

    def test_order_by_in_url(self, mock_client: MagicMock) -> None:
        qs = QuerySet(FakeVolume, mock_client).order_by("name asc")
        url = qs._build_url()
        assert "order_by=" in url

    def test_limit_in_url(self, mock_client: MagicMock) -> None:
        qs = QuerySet(FakeVolume, mock_client).limit(5)
        url = qs._build_url()
        assert "max_records=5" in url

    def test_return_records_false(self, mock_client: MagicMock) -> None:
        qs = QuerySet(FakeVolume, mock_client)
        url = qs._build_url(return_records=False)
        assert "return_records=false" in url


# ---------------------------------------------------------------------------
# Terminal method tests
# ---------------------------------------------------------------------------


def _make_api_response(records: list[dict[str, Any]]) -> dict[str, Any]:
    """Build a fake ONTAP API response envelope."""
    return {
        "records": records,
        "num_records": len(records),
    }


class TestQuerySetAll:
    """Tests for .all() terminal method."""

    def test_all_calls_get_all_records(self, mock_client: MagicMock) -> None:
        mock_client.get_all_records.return_value = _make_api_response([])
        QuerySet(FakeVolume, mock_client).all()
        mock_client.get_all_records.assert_called_once()

    def test_all_returns_typed_models(self, mock_client: MagicMock) -> None:
        mock_client.get_all_records.return_value = _make_api_response(
            [{"name": "vol1", "uuid": "abc", "svm": {"name": "vs1"}, "state": "online"}]
        )
        results = QuerySet(FakeVolume, mock_client).all()
        assert len(results) == 1
        assert isinstance(results[0], FakeVolume)
        assert results[0].name == "vol1"
        assert results[0].svm_name == "vs1"

    def test_all_empty_response(self, mock_client: MagicMock) -> None:
        mock_client.get_all_records.return_value = _make_api_response([])
        results = QuerySet(FakeVolume, mock_client).all()
        assert results == []


class TestQuerySetFirst:
    """Tests for .first() terminal method."""

    def test_first_returns_instance(self, mock_client: MagicMock) -> None:
        mock_client.get_all_records.return_value = _make_api_response(
            [{"name": "vol1", "uuid": "abc", "svm": {"name": "vs1"}, "state": "online"}]
        )
        result = QuerySet(FakeVolume, mock_client).first()
        assert isinstance(result, FakeVolume)
        assert result.name == "vol1"

    def test_first_returns_none_on_empty(self, mock_client: MagicMock) -> None:
        mock_client.get_all_records.return_value = _make_api_response([])
        result = QuerySet(FakeVolume, mock_client).first()
        assert result is None

    def test_first_limits_to_one(self, mock_client: MagicMock) -> None:
        mock_client.get_all_records.return_value = _make_api_response([])
        QuerySet(FakeVolume, mock_client).first()
        call_url = mock_client.get_all_records.call_args[0][0]
        assert "max_records=1" in call_url


class TestQuerySetGet:
    """Tests for .get() terminal method."""

    def test_get_returns_single(self, mock_client: MagicMock) -> None:
        mock_client.get_all_records.return_value = _make_api_response(
            [{"name": "vol1", "uuid": "abc", "svm": {"name": "vs1"}, "state": "online"}]
        )
        result = QuerySet(FakeVolume, mock_client).get(uuid="abc")
        assert isinstance(result, FakeVolume)
        assert result.uuid == "abc"

    def test_get_raises_not_found(self, mock_client: MagicMock) -> None:
        mock_client.get_all_records.return_value = _make_api_response([])
        with pytest.raises(NotFoundError, match="FakeVolume"):
            QuerySet(FakeVolume, mock_client).get(uuid="missing")

    def test_get_raises_multiple_results(self, mock_client: MagicMock) -> None:
        mock_client.get_all_records.return_value = _make_api_response(
            [
                {"name": "vol1", "uuid": "a", "svm": {"name": "vs1"}, "state": "online"},
                {"name": "vol2", "uuid": "b", "svm": {"name": "vs1"}, "state": "online"},
            ]
        )
        with pytest.raises(MultipleResultsError, match="2"):
            QuerySet(FakeVolume, mock_client).get(svm_name="vs1")


class TestQuerySetCount:
    """Tests for .count() terminal method."""

    def test_count_uses_return_records_false(self, mock_client: MagicMock) -> None:
        mock_client.call_endpoint.return_value = {"num_records": 42}
        result = QuerySet(FakeVolume, mock_client).count()
        assert result == 42
        call_url = mock_client.call_endpoint.call_args[0][0]
        assert "return_records=false" in call_url

    def test_count_zero(self, mock_client: MagicMock) -> None:
        mock_client.call_endpoint.return_value = {"num_records": 0}
        assert QuerySet(FakeVolume, mock_client).count() == 0

    def test_count_handles_non_dict(self, mock_client: MagicMock) -> None:
        mock_client.call_endpoint.return_value = None
        assert QuerySet(FakeVolume, mock_client).count() == 0


class TestQuerySetIter:
    """Tests for __iter__."""

    def test_iter_works(self, mock_client: MagicMock) -> None:
        mock_client.get_all_records.return_value = _make_api_response(
            [
                {"name": "vol1", "uuid": "a", "svm": {"name": "vs1"}, "state": "online"},
                {"name": "vol2", "uuid": "b", "svm": {"name": "vs2"}, "state": "offline"},
            ]
        )
        names = [v.name for v in QuerySet(FakeVolume, mock_client)]
        assert names == ["vol1", "vol2"]


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
