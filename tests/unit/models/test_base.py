"""Tests for models._base module -- OntapModel, HasUUID, OntapUUID."""

from __future__ import annotations

import pytest
from pydantic import ConfigDict, ValidationError, field_validator

from pynetappfoundry.models._base import (
    HasUUID,
    OntapModel,
    OntapUUID,
    _validate_ontap_uuid,
)

# ---------------------------------------------------------------------------
# OntapModel base class
# ---------------------------------------------------------------------------


class TestOntapModel:
    """Tests for OntapModel base class behaviour."""

    def test_extra_allow_inherited(self) -> None:
        """Subclasses inherit extra='allow' without declaring model_config."""

        class MyModel(OntapModel):
            name: str = ""

        obj = MyModel(name="test", unknown_field="hello")  # type: ignore[call-arg]
        assert obj.name == "test"
        assert obj.unknown_field == "hello"  # type: ignore[attr-defined]

    def test_field_validator_works(self) -> None:
        """field_validator still works on OntapModel subclasses."""

        class Validated(OntapModel):
            value: str = ""

            @field_validator("value", mode="before")
            @classmethod
            def coerce(cls, v: object) -> str:
                return str(v) if v is not None else ""

        obj = Validated(value=42)  # type: ignore[arg-type]
        assert obj.value == "42"

    def test_model_config_override_in_subclass(self) -> None:
        """A subclass can override model_config and still work."""

        class Strict(OntapModel):
            model_config = ConfigDict(extra="forbid")
            x: int = 0

        obj = Strict(x=1)
        assert obj.x == 1
        with pytest.raises(ValidationError):
            Strict(x=1, bad="field")  # type: ignore[call-arg]

    def test_subclass_inheritance(self) -> None:
        """Children of OntapModel also inherit extra='allow'."""

        class Parent(OntapModel):
            pass

        class Child(Parent):
            name: str = ""

        obj = Child(name="test", extra="value")  # type: ignore[call-arg]
        assert obj.name == "test"
        assert obj.extra == "value"  # type: ignore[attr-defined]


# ---------------------------------------------------------------------------
# HasUUID protocol
# ---------------------------------------------------------------------------


class TestHasUUID:
    """Tests for HasUUID runtime-checkable protocol."""

    def test_model_with_uuid(self) -> None:

        class WithUUID(OntapModel):
            uuid: str = ""

        obj = WithUUID(uuid="abc-123")
        assert isinstance(obj, HasUUID)
        assert obj.uuid == "abc-123"

    def test_model_without_uuid(self) -> None:

        class NoUUID(OntapModel):
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

        class TestModel(OntapModel):
            uuid: OntapUUID = ""

        obj = TestModel(uuid="550e8400-e29b-41d4-a716-446655440000")
        assert obj.uuid == "550e8400-e29b-41d4-a716-446655440000"

    def test_pydantic_model_rejects_invalid(self) -> None:
        """Pydantic model construction rejects invalid UUID."""

        class TestModel(OntapModel):
            uuid: OntapUUID = ""

        with pytest.raises(ValidationError):
            TestModel(uuid="garbage")

    def test_pydantic_model_empty_default(self) -> None:
        """Default empty string is accepted."""

        class TestModel(OntapModel):
            uuid: OntapUUID = ""

        obj = TestModel()
        assert obj.uuid == ""
