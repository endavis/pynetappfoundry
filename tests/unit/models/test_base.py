"""Tests for models._base module -- OntapModel, HasUUID, OntapUUID."""

from __future__ import annotations

import pytest
from pydantic import ConfigDict, Field, ValidationError, field_validator

from pynetappfoundry.models._base import (
    AiqumModel,
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
# _fetched_fields / was_fetched
# ---------------------------------------------------------------------------


class TestFetchedFields:
    """Tests for OntapModel._fetched_fields and was_fetched()."""

    def test_fetched_fields_starts_empty(self) -> None:
        """A freshly constructed model has an empty _fetched_fields set."""

        class M(OntapModel):
            name: str = ""

        obj = M(name="x")
        assert obj._fetched_fields == set()

    def test_fetched_fields_not_in_model_dump(self) -> None:
        """_fetched_fields is a PrivateAttr -- never appears in model_dump()."""

        class M(OntapModel):
            name: str = ""

        obj = M(name="x")
        obj._fetched_fields.add("name")
        dumped = obj.model_dump()
        assert "_fetched_fields" not in dumped
        assert dumped == {"name": "x"}

    def test_was_fetched_returns_bool(self) -> None:
        """was_fetched() returns True/False based on the underlying set."""

        class M(OntapModel):
            name: str = ""

        obj = M(name="x")
        assert obj.was_fetched("name") is False
        obj._fetched_fields.add("name")
        assert obj.was_fetched("name") is True
        assert obj.was_fetched("missing") is False

    def test_fetched_fields_is_per_instance(self) -> None:
        """Two instances do not share _fetched_fields state."""

        class M(OntapModel):
            name: str = ""

        a = M(name="a")
        b = M(name="b")
        a._fetched_fields.add("name")
        assert b._fetched_fields == set()
        assert a._fetched_fields == {"name"}


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


# ---------------------------------------------------------------------------
# AiqumModel (#1102)
# ---------------------------------------------------------------------------


class _AqSub(AiqumModel):
    name: str = ""
    flag: bool = False


class _AqItem(AiqumModel):
    label: str = ""


class _AqModel(AiqumModel):
    text: str = "d"
    flag: bool = False
    uuid: OntapUUID = ""
    tags: list[str] = Field(default_factory=list)
    sub: _AqSub = Field(default_factory=_AqSub)
    items: list[_AqItem] = Field(default_factory=list)
    opt: str | None = None


class TestAiqumModel:
    """AiqumModel maps null on declared fields to the field default."""

    def test_none_gives_defaults(self) -> None:
        m = _AqModel.model_validate(
            {"text": None, "flag": None, "uuid": None, "tags": None, "sub": None}
        )
        assert (m.text, m.flag, m.uuid, m.tags) == ("d", False, "", [])
        assert m.sub == _AqSub()

    def test_none_inside_nested_dict(self) -> None:
        m = _AqModel.model_validate({"sub": {"name": None, "flag": True}})
        assert (m.sub.name, m.sub.flag) == ("", True)

    def test_none_in_list_items(self) -> None:
        m = _AqModel.model_validate({"items": [{"label": None}, {"label": "x"}]})
        assert [i.label for i in m.items] == ["", "x"]

    def test_non_none_values_kept(self) -> None:
        m = _AqModel.model_validate({"text": "t", "flag": True, "tags": ["a"]})
        assert (m.text, m.flag, m.tags) == ("t", True, ["a"])

    def test_extra_key_none_kept(self) -> None:
        m = _AqModel.model_validate({"unknown": None})
        assert m.model_extra == {"unknown": None}

    def test_optional_field_keeps_none(self) -> None:
        assert _AqModel.model_validate({"opt": None}).opt is None

    def test_keyword_construction_with_none(self) -> None:
        assert _AqModel(text=None).text == "d"  # type: ignore[arg-type]  # null input is the point

    def test_non_dict_input_passes_through(self) -> None:
        existing = _AqModel(text="t")
        assert _AqModel.model_validate(existing) is existing
        with pytest.raises(ValidationError):
            _AqModel.model_validate("not a dict")

    def test_input_dict_not_mutated(self) -> None:
        data = {"text": None}
        _AqModel.model_validate(data)
        assert data == {"text": None}

    def test_plain_ontap_model_still_rejects_none(self) -> None:
        class Plain(OntapModel):
            text: str = ""

        with pytest.raises(ValidationError):
            Plain.model_validate({"text": None})

    def test_exported(self) -> None:
        from pynetappfoundry.models import AiqumModel as ExportedAiqumModel

        assert ExportedAiqumModel is AiqumModel
