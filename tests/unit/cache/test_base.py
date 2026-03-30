"""Tests for cache._base module -- CacheModel alias, HasUUID, OntapUUID, schema utilities."""

from __future__ import annotations

import pytest
from pydantic import ConfigDict, ValidationError, field_validator

from pynetappfoundry.cache._base import (
    METADATA_SCHEMA_MIN_COMPATIBLE,
    METADATA_SCHEMA_VERSION,
    CacheModel,
    HasUUID,
    OntapUUID,
    _utcnow,
    _validate_ontap_uuid,
    is_schema_compatible,
    parse_schema_version,
)

# ---------------------------------------------------------------------------
# Schema versioning
# ---------------------------------------------------------------------------


class TestParseSchemaVersion:
    """Tests for parse_schema_version()."""

    def test_major_minor(self) -> None:
        assert parse_schema_version("1.0") == (1, 0)

    def test_major_only(self) -> None:
        assert parse_schema_version("2") == (2, 0)

    def test_higher_versions(self) -> None:
        assert parse_schema_version("3.14") == (3, 14)

    def test_invalid_raises(self) -> None:
        with pytest.raises(ValueError, match="Invalid schema version"):
            parse_schema_version("abc")

    def test_empty_raises(self) -> None:
        with pytest.raises(ValueError, match="Invalid schema version"):
            parse_schema_version("")


class TestIsSchemaCompatible:
    """Tests for is_schema_compatible()."""

    def test_none_incompatible(self) -> None:
        assert is_schema_compatible(None) is False

    def test_current_compatible(self) -> None:
        assert is_schema_compatible(METADATA_SCHEMA_VERSION) is True

    def test_min_compatible(self) -> None:
        assert is_schema_compatible(METADATA_SCHEMA_MIN_COMPATIBLE) is True

    def test_invalid_string(self) -> None:
        assert is_schema_compatible("not-a-version") is False


class TestUtcNow:
    """Tests for _utcnow()."""

    def test_returns_aware_datetime(self) -> None:
        dt = _utcnow()
        assert dt.tzinfo is not None


# ---------------------------------------------------------------------------
# CacheModel alias
# ---------------------------------------------------------------------------


class TestCacheModel:
    """Tests for CacheModel (alias of OntapModel) base class behaviour."""

    def test_cache_model_is_ontap_model(self) -> None:
        """CacheModel is an alias for OntapModel."""
        from pynetappfoundry.models._base import OntapModel

        assert CacheModel is OntapModel

    def test_extra_allow_inherited(self) -> None:
        """Subclasses inherit extra='allow' without declaring model_config."""

        class MyModel(CacheModel):
            name: str = ""

        obj = MyModel(name="test", unknown_field="hello")  # type: ignore[call-arg]
        assert obj.name == "test"
        assert obj.unknown_field == "hello"  # type: ignore[attr-defined]

    def test_field_validator_works(self) -> None:
        """field_validator still works on CacheModel subclasses."""

        class Validated(CacheModel):
            value: str = ""

            @field_validator("value", mode="before")
            @classmethod
            def coerce(cls, v: object) -> str:
                return str(v) if v is not None else ""

        obj = Validated(value=42)  # type: ignore[arg-type]
        assert obj.value == "42"

    def test_model_config_override_in_subclass(self) -> None:
        """A subclass can override model_config and still work."""

        class Strict(CacheModel):
            model_config = ConfigDict(extra="forbid")
            x: int = 0

        obj = Strict(x=1)
        assert obj.x == 1
        with pytest.raises(ValidationError):
            Strict(x=1, bad="field")  # type: ignore[call-arg]


# ---------------------------------------------------------------------------
# HasUUID protocol
# ---------------------------------------------------------------------------


class TestHasUUID:
    """Tests for HasUUID runtime-checkable protocol."""

    def test_model_with_uuid(self) -> None:

        class WithUUID(CacheModel):
            uuid: str = ""

        obj = WithUUID(uuid="abc-123")
        assert isinstance(obj, HasUUID)
        assert obj.uuid == "abc-123"

    def test_model_without_uuid(self) -> None:

        class NoUUID(CacheModel):
            name: str = ""

        obj = NoUUID(name="test")
        assert not isinstance(obj, HasUUID)


# ---------------------------------------------------------------------------
# OntapUUID type
# ---------------------------------------------------------------------------


class TestOntapUUID:
    """Tests for OntapUUID validated type."""

    def test_valid_uuid(self) -> None:
        """Valid UUID format passes validation."""
        assert _validate_ontap_uuid("550e8400-e29b-41d4-a716-446655440000") == (
            "550e8400-e29b-41d4-a716-446655440000"
        )

    def test_empty_string_allowed(self) -> None:
        """Empty string is allowed (ONTAP returns '' for optional UUID fields)."""
        assert _validate_ontap_uuid("") == ""

    def test_invalid_uuid_raises(self) -> None:
        """Malformed UUID raises ValueError."""
        with pytest.raises(ValueError, match="Invalid UUID"):
            _validate_ontap_uuid("not-a-uuid")

    def test_uppercase_uuid(self) -> None:
        """Uppercase UUIDs are accepted."""
        assert _validate_ontap_uuid("550E8400-E29B-41D4-A716-446655440000") == (
            "550E8400-E29B-41D4-A716-446655440000"
        )

    def test_pydantic_model_with_ontap_uuid(self) -> None:
        """OntapUUID works as a Pydantic field type."""

        class TestModel(CacheModel):
            uuid: OntapUUID = ""

        obj = TestModel(uuid="550e8400-e29b-41d4-a716-446655440000")
        assert obj.uuid == "550e8400-e29b-41d4-a716-446655440000"

    def test_pydantic_model_rejects_invalid(self) -> None:
        """Pydantic model construction rejects invalid UUID."""

        class TestModel(CacheModel):
            uuid: OntapUUID = ""

        with pytest.raises(ValidationError):
            TestModel(uuid="garbage")

    def test_pydantic_model_empty_default(self) -> None:
        """Default empty string is accepted."""

        class TestModel(CacheModel):
            uuid: OntapUUID = ""

        obj = TestModel()
        assert obj.uuid == ""
