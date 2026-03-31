"""Tests for pynetappfoundry.query.related module."""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock

import pytest
from pydantic import BaseModel

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.query.related import related, related_one

# ---------------------------------------------------------------------------
# Test model and mapping fixtures
# ---------------------------------------------------------------------------


class FakeVolume(BaseModel):
    """Minimal model for testing."""

    name: str = ""
    uuid: str = ""
    svm_name: str = ""
    svm_uuid: str = ""
    state: str = ""


FAKE_FIELDS = (
    FieldMapping(cache_attr="name", api_path="name"),
    FieldMapping(cache_attr="uuid", api_path="uuid"),
    FieldMapping(cache_attr="svm_name", api_path="svm.name"),
    FieldMapping(cache_attr="svm_uuid", api_path="svm.uuid"),
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
    model_registry._mappings.pop("FakeVolume", None)


@pytest.fixture()
def mock_client() -> MagicMock:
    """Return a mocked APIWrapper."""
    return MagicMock(spec=["get_all_records", "call_endpoint"])


def _make_api_response(records: list[dict[str, Any]]) -> dict[str, Any]:
    """Build a fake ONTAP API response envelope."""
    return {
        "records": records,
        "num_records": len(records),
    }


# ---------------------------------------------------------------------------
# related() tests
# ---------------------------------------------------------------------------


class TestRelated:
    """Tests for the related() function."""

    def test_related_returns_filtered_results(self, mock_client: MagicMock) -> None:
        """related() delegates to QuerySet.filter().all() and returns models."""
        mock_client.get_all_records.return_value = _make_api_response(
            [
                {
                    "name": "vol1",
                    "uuid": "a",
                    "svm": {"name": "vs1", "uuid": "s1"},
                    "state": "online",
                },
                {
                    "name": "vol2",
                    "uuid": "b",
                    "svm": {"name": "vs1", "uuid": "s1"},
                    "state": "online",
                },
            ]
        )
        results = related(FakeVolume, mock_client, svm_name="vs1")
        assert len(results) == 2
        assert all(isinstance(r, FakeVolume) for r in results)
        assert results[0].name == "vol1"
        assert results[1].name == "vol2"

    def test_related_translates_attrs(self, mock_client: MagicMock) -> None:
        """Filter kwargs use model attrs translated to API paths."""
        mock_client.get_all_records.return_value = _make_api_response([])
        related(FakeVolume, mock_client, svm_uuid="abc-123")
        call_url = mock_client.get_all_records.call_args[0][0]
        assert "svm.uuid=abc-123" in call_url

    def test_related_multiple_filters(self, mock_client: MagicMock) -> None:
        """Multiple kwargs are combined as filters."""
        mock_client.get_all_records.return_value = _make_api_response([])
        related(FakeVolume, mock_client, svm_name="vs1", state="online")
        call_url = mock_client.get_all_records.call_args[0][0]
        assert "svm.name=vs1" in call_url
        assert "state=online" in call_url

    def test_related_empty_kwargs_raises(self) -> None:
        """related() raises ValueError when no filters are provided."""
        mock_client = MagicMock()
        with pytest.raises(ValueError, match="requires at least one filter"):
            related(FakeVolume, mock_client)

    def test_related_unknown_model_raises(self, mock_client: MagicMock) -> None:
        """related() raises ValueError for unregistered model class."""

        class UnregisteredModel(BaseModel):
            pass

        with pytest.raises(ValueError, match="No TypeMapping registered"):
            related(UnregisteredModel, mock_client, name="test")

    def test_related_empty_results(self, mock_client: MagicMock) -> None:
        """related() returns empty list when no records match."""
        mock_client.get_all_records.return_value = _make_api_response([])
        results = related(FakeVolume, mock_client, svm_name="nonexistent")
        assert results == []

    def test_related_uses_pagination(self, mock_client: MagicMock) -> None:
        """related() calls get_all_records for paginated fetching."""
        mock_client.get_all_records.return_value = _make_api_response(
            [
                {
                    "name": f"vol{i}",
                    "uuid": str(i),
                    "svm": {"name": "vs1", "uuid": "s1"},
                    "state": "online",
                }
                for i in range(5)
            ]
        )
        results = related(FakeVolume, mock_client, svm_name="vs1")
        assert len(results) == 5
        mock_client.get_all_records.assert_called_once()


# ---------------------------------------------------------------------------
# related_one() tests
# ---------------------------------------------------------------------------


class TestRelatedOne:
    """Tests for the related_one() function."""

    def test_related_one_returns_first(self, mock_client: MagicMock) -> None:
        """related_one() returns the first matching model instance."""
        mock_client.get_all_records.return_value = _make_api_response(
            [{"name": "vol1", "uuid": "a", "svm": {"name": "vs1", "uuid": "s1"}, "state": "online"}]
        )
        result = related_one(FakeVolume, mock_client, svm_name="vs1")
        assert isinstance(result, FakeVolume)
        assert result.name == "vol1"

    def test_related_one_returns_none(self, mock_client: MagicMock) -> None:
        """related_one() returns None when no records match."""
        mock_client.get_all_records.return_value = _make_api_response([])
        result = related_one(FakeVolume, mock_client, svm_name="nonexistent")
        assert result is None

    def test_related_one_empty_kwargs_raises(self) -> None:
        """related_one() raises ValueError when no filters are provided."""
        mock_client = MagicMock()
        with pytest.raises(ValueError, match="requires at least one filter"):
            related_one(FakeVolume, mock_client)

    def test_related_one_limits_to_one(self, mock_client: MagicMock) -> None:
        """related_one() uses .first() which limits to max_records=1."""
        mock_client.get_all_records.return_value = _make_api_response([])
        related_one(FakeVolume, mock_client, svm_name="vs1")
        call_url = mock_client.get_all_records.call_args[0][0]
        assert "max_records=1" in call_url
