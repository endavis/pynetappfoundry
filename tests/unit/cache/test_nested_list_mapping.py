"""Registry-wide regression for the generic nested-list mapping (#900)."""

from __future__ import annotations

import pytest

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping, parse_api_record


def _item_model_fields() -> list[tuple[str, TypeMapping, FieldMapping]]:
    found: list[tuple[str, TypeMapping, FieldMapping]] = []
    for name, mapping in model_registry.mappings.items():
        found.extend((name, mapping, f) for f in mapping.fields if f.item_model is not None)
    return found


_FIELDS = _item_model_fields()


def test_registry_has_item_model_fields() -> None:
    assert _FIELDS


def test_no_generated_list_transforms_remain() -> None:
    offenders = [
        f"{name}.{f.cache_attr}"
        for name, mapping in model_registry.mappings.items()
        for f in mapping.fields
        if f.transform is not None
        and getattr(f.transform, "__name__", "").startswith("_transform_")
    ]
    assert offenders == []


@pytest.mark.parametrize(
    ("name", "mapping", "field"),
    _FIELDS,
    ids=[f"{n}.{f.cache_attr}" for n, _, f in _FIELDS],
)
def test_item_model_field_tolerates_empty_input(
    name: str, mapping: TypeMapping, field: FieldMapping
) -> None:
    """Absent, null and ``[{}]`` values each parse without error."""
    assert field.api_path is not None
    only = TypeMapping(
        name=mapping.name,
        model_class=mapping.model_class,
        api_endpoint=mapping.api_endpoint,
        fields=(field,),
    )
    parse_api_record(only, {}, "[t]")
    parse_api_record(only, _nest(field.api_path, None), "[t]")
    assert field.item_model is not None
    parse_api_record(only, _nest(field.api_path, [{}]), "[t]")


def _nest(path: str, value: object) -> dict[str, object]:
    """Build a record with ``value`` at dotted ``path``."""
    record: object = value
    for part in reversed(path.split(".")):
        record = {part: record}
    assert isinstance(record, dict)
    return record
