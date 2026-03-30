"""Tests for pynetappfoundry.query.mutation module."""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock

import pytest
from pydantic import BaseModel

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.core.models import RetryConfig
from pynetappfoundry.query.mutation import Mutation, _set_nested

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
    name="FakeVolumeMut",
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
    return MagicMock(spec=["call_endpoint"])


# ---------------------------------------------------------------------------
# Constructor tests
# ---------------------------------------------------------------------------


class TestMutationInit:
    """Tests for Mutation.__init__."""

    def test_init_with_valid_mapping(self, mock_client: MagicMock) -> None:
        m = Mutation(FakeVolume, mock_client)
        assert m._mapping is FAKE_MAPPING
        assert m._client is mock_client

    def test_init_with_missing_mapping(self, mock_client: MagicMock) -> None:
        class Unregistered(BaseModel):
            pass

        with pytest.raises(ValueError, match="No TypeMapping registered for 'Unregistered'"):
            Mutation(Unregistered, mock_client)


# ---------------------------------------------------------------------------
# _set_nested tests
# ---------------------------------------------------------------------------


class TestSetNested:
    """Tests for _set_nested helper."""

    def test_simple_path(self) -> None:
        d: dict[str, Any] = {}
        _set_nested(d, "name", "vol1")
        assert d == {"name": "vol1"}

    def test_deep_path(self) -> None:
        d: dict[str, Any] = {}
        _set_nested(d, "svm.name", "vs1")
        assert d == {"svm": {"name": "vs1"}}

    def test_deeper_path(self) -> None:
        d: dict[str, Any] = {}
        _set_nested(d, "a.b.c", "val")
        assert d == {"a": {"b": {"c": "val"}}}

    def test_merges_siblings(self) -> None:
        d: dict[str, Any] = {}
        _set_nested(d, "svm.name", "vs1")
        _set_nested(d, "svm.uuid", "abc")
        assert d == {"svm": {"name": "vs1", "uuid": "abc"}}


# ---------------------------------------------------------------------------
# _build_body tests
# ---------------------------------------------------------------------------


class TestBuildBody:
    """Tests for Mutation._build_body."""

    def test_translates_attrs(self, mock_client: MagicMock) -> None:
        m = Mutation(FakeVolume, mock_client)
        body = m._build_body({"svm_name": "vs1"})
        assert body == {"svm": {"name": "vs1"}}

    def test_passthrough_unknown(self, mock_client: MagicMock) -> None:
        m = Mutation(FakeVolume, mock_client)
        body = m._build_body({"unknown_field": "val"})
        assert body == {"unknown_field": "val"}

    def test_multiple_attrs_merge(self, mock_client: MagicMock) -> None:
        m = Mutation(FakeVolume, mock_client)
        body = m._build_body({"svm_name": "vs1", "svm_uuid": "abc", "name": "vol1"})
        assert body == {"svm": {"name": "vs1", "uuid": "abc"}, "name": "vol1"}


# ---------------------------------------------------------------------------
# _collection_path tests
# ---------------------------------------------------------------------------


class TestCollectionPath:
    """Tests for Mutation._collection_path."""

    def test_strips_query_params(self, mock_client: MagicMock) -> None:
        m = Mutation(FakeVolume, mock_client)
        assert m._collection_path() == "/storage/volumes"


# ---------------------------------------------------------------------------
# create tests
# ---------------------------------------------------------------------------


class TestCreate:
    """Tests for Mutation.create."""

    def test_posts_to_collection_endpoint(self, mock_client: MagicMock) -> None:
        mock_client.call_endpoint.return_value = {
            "name": "vol1",
            "uuid": "abc",
            "svm": {"name": "vs1", "uuid": "xyz"},
            "state": "online",
        }
        m = Mutation(FakeVolume, mock_client)
        m.create(name="vol1", svm_name="vs1")
        mock_client.call_endpoint.assert_called_once()
        call_args = mock_client.call_endpoint.call_args
        assert call_args[0][0] == "/storage/volumes"
        assert call_args[1]["method"] == "POST"

    def test_translates_attrs_to_nested_json(self, mock_client: MagicMock) -> None:
        mock_client.call_endpoint.return_value = {}
        m = Mutation(FakeVolume, mock_client)
        m.create(name="vol1", svm_name="vs1")
        call_args = mock_client.call_endpoint.call_args
        assert call_args[1]["body"] == {"name": "vol1", "svm": {"name": "vs1"}}

    def test_disables_retry(self, mock_client: MagicMock) -> None:
        mock_client.call_endpoint.return_value = {}
        m = Mutation(FakeVolume, mock_client)
        m.create(name="vol1")
        call_args = mock_client.call_endpoint.call_args
        retry_config = call_args[1]["retry_config"]
        assert isinstance(retry_config, RetryConfig)
        assert retry_config.enabled is False

    def test_parses_response_to_model(self, mock_client: MagicMock) -> None:
        mock_client.call_endpoint.return_value = {
            "name": "vol1",
            "uuid": "abc",
            "svm": {"name": "vs1", "uuid": "xyz"},
            "state": "online",
        }
        m = Mutation(FakeVolume, mock_client)
        result = m.create(name="vol1", svm_name="vs1")
        assert isinstance(result, FakeVolume)
        assert result.name == "vol1"
        assert result.svm_name == "vs1"


# ---------------------------------------------------------------------------
# update tests
# ---------------------------------------------------------------------------


class TestUpdate:
    """Tests for Mutation.update."""

    def test_patches_with_uuid_in_url(self, mock_client: MagicMock) -> None:
        mock_client.call_endpoint.return_value = {
            "name": "vol1",
            "uuid": "abc-123",
            "svm": {"name": "vs1", "uuid": "xyz"},
            "state": "offline",
        }
        m = Mutation(FakeVolume, mock_client)
        m.update("abc-123", state="offline")
        call_args = mock_client.call_endpoint.call_args
        assert call_args[0][0] == "/storage/volumes/abc-123"
        assert call_args[1]["method"] == "PATCH"

    def test_translates_attrs(self, mock_client: MagicMock) -> None:
        mock_client.call_endpoint.return_value = {}
        m = Mutation(FakeVolume, mock_client)
        m.update("abc-123", svm_name="vs2")
        call_args = mock_client.call_endpoint.call_args
        assert call_args[1]["body"] == {"svm": {"name": "vs2"}}

    def test_uses_default_retry(self, mock_client: MagicMock) -> None:
        mock_client.call_endpoint.return_value = {}
        m = Mutation(FakeVolume, mock_client)
        m.update("abc-123", state="offline")
        call_args = mock_client.call_endpoint.call_args
        # No retry_config kwarg means default retry is used
        assert "retry_config" not in call_args[1]


# ---------------------------------------------------------------------------
# delete tests
# ---------------------------------------------------------------------------


class TestDelete:
    """Tests for Mutation.delete."""

    def test_sends_delete_request(self, mock_client: MagicMock) -> None:
        mock_client.call_endpoint.return_value = None
        m = Mutation(FakeVolume, mock_client)
        m.delete("abc-123")
        call_args = mock_client.call_endpoint.call_args
        assert call_args[0][0] == "/storage/volumes/abc-123"
        assert call_args[1]["method"] == "DELETE"

    def test_with_body_kwargs(self, mock_client: MagicMock) -> None:
        mock_client.call_endpoint.return_value = None
        m = Mutation(FakeVolume, mock_client)
        m.delete("abc-123", force=True)
        call_args = mock_client.call_endpoint.call_args
        assert call_args[1]["body"] == {"force": True}

    def test_returns_raw_response(self, mock_client: MagicMock) -> None:
        mock_client.call_endpoint.return_value = {"job": {"uuid": "job-123"}}
        m = Mutation(FakeVolume, mock_client)
        result = m.delete("abc-123")
        assert result == {"job": {"uuid": "job-123"}}

    def test_no_body_when_no_kwargs(self, mock_client: MagicMock) -> None:
        mock_client.call_endpoint.return_value = None
        m = Mutation(FakeVolume, mock_client)
        m.delete("abc-123")
        call_args = mock_client.call_endpoint.call_args
        assert call_args[1]["body"] is None


# ---------------------------------------------------------------------------
# _parse_response tests
# ---------------------------------------------------------------------------


class TestParseResponse:
    """Tests for Mutation._parse_response."""

    def test_with_record(self, mock_client: MagicMock) -> None:
        m = Mutation(FakeVolume, mock_client)
        response = {
            "name": "vol1",
            "uuid": "abc",
            "svm": {"name": "vs1", "uuid": "xyz"},
            "state": "online",
        }
        result = m._parse_response(response)
        assert isinstance(result, FakeVolume)
        assert result.name == "vol1"

    def test_none_response(self, mock_client: MagicMock) -> None:
        m = Mutation(FakeVolume, mock_client)
        result = m._parse_response(None)
        assert result is None

    def test_non_record_dict(self, mock_client: MagicMock) -> None:
        m = Mutation(FakeVolume, mock_client)
        response = {"job": {"uuid": "job-123"}}
        result = m._parse_response(response)
        assert result == {"job": {"uuid": "job-123"}}
