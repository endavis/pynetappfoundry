"""Tests for pynetappfoundry.query.related module."""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock, patch

import pytest
from pydantic import BaseModel

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.core.config import Config
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
    """Return a mocked APIWrapper with a name attribute."""
    client = MagicMock(spec=["get_all_records", "call_endpoint", "name"])
    client.name = "test-cluster"
    return client


@pytest.fixture()
def mock_config() -> MagicMock:
    """Return a mocked Config."""
    return MagicMock(spec=Config)


def _make_mocked_ds() -> tuple[MagicMock, MagicMock]:
    """Create a mocked DataSource and a chainable builder.

    Returns ``(ds_instance, builder)``.
    """
    builder = MagicMock()
    builder.filter.return_value = builder
    builder.fields.return_value = builder
    builder.__iter__ = lambda self: iter(getattr(self, "_results", []))
    builder._results = []

    ds_instance = MagicMock()
    ds_instance.query.return_value = builder
    ds_instance._get_backend.return_value = MagicMock(_api_clients={})
    return ds_instance, builder


# ---------------------------------------------------------------------------
# related() tests
# ---------------------------------------------------------------------------


class TestRelated:
    """Tests for the related() function."""

    def test_related_returns_filtered_results(
        self, mock_client: MagicMock, mock_config: MagicMock
    ) -> None:
        """related() delegates to QuerySet.filter().all() and returns models."""
        ds, builder = _make_mocked_ds()
        vols = [
            FakeVolume(name="vol1", uuid="a", svm_name="vs1"),
            FakeVolume(name="vol2", uuid="b", svm_name="vs1"),
        ]
        builder._results = vols

        with patch("pynetappfoundry.query.queryset.DataSource", return_value=ds):
            results = related(FakeVolume, mock_client, config=mock_config, svm_name="vs1")

        assert len(results) == 2
        assert all(isinstance(r, FakeVolume) for r in results)
        assert results[0].name == "vol1"

    def test_related_empty_kwargs_raises(self, mock_config: MagicMock) -> None:
        """related() raises ValueError when no filters are provided."""
        mock_client = MagicMock()
        with pytest.raises(ValueError, match="requires at least one filter"):
            related(FakeVolume, mock_client, config=mock_config)

    def test_related_unknown_model_raises(
        self, mock_client: MagicMock, mock_config: MagicMock
    ) -> None:
        """related() raises ValueError for unregistered model class."""

        class UnregisteredModel(BaseModel):
            pass

        with (
            pytest.raises(ValueError, match="No TypeMapping registered"),
            patch("pynetappfoundry.query.queryset.DataSource"),
        ):
            related(UnregisteredModel, mock_client, config=mock_config, name="test")

    def test_related_empty_results(self, mock_client: MagicMock, mock_config: MagicMock) -> None:
        """related() returns empty list when no records match."""
        ds, builder = _make_mocked_ds()
        builder._results = []

        with patch("pynetappfoundry.query.queryset.DataSource", return_value=ds):
            results = related(FakeVolume, mock_client, config=mock_config, svm_name="nonexistent")
        assert results == []


# ---------------------------------------------------------------------------
# related_one() tests
# ---------------------------------------------------------------------------


class TestRelatedOne:
    """Tests for the related_one() function."""

    def test_related_one_returns_first(
        self, mock_client: MagicMock, mock_config: MagicMock
    ) -> None:
        """related_one() returns the first matching model instance."""
        ds, builder = _make_mocked_ds()
        vol = FakeVolume(name="vol1", uuid="a", svm_name="vs1")
        builder._results = [vol]

        with patch("pynetappfoundry.query.queryset.DataSource", return_value=ds):
            result = related_one(FakeVolume, mock_client, config=mock_config, svm_name="vs1")

        assert isinstance(result, FakeVolume)
        assert result.name == "vol1"

    def test_related_one_returns_none(self, mock_client: MagicMock, mock_config: MagicMock) -> None:
        """related_one() returns None when no records match."""
        ds, builder = _make_mocked_ds()
        builder._results = []

        with patch("pynetappfoundry.query.queryset.DataSource", return_value=ds):
            result = related_one(
                FakeVolume, mock_client, config=mock_config, svm_name="nonexistent"
            )
        assert result is None

    def test_related_one_empty_kwargs_raises(self, mock_config: MagicMock) -> None:
        """related_one() raises ValueError when no filters are provided."""
        mock_client = MagicMock()
        with pytest.raises(ValueError, match="requires at least one filter"):
            related_one(FakeVolume, mock_client, config=mock_config)
