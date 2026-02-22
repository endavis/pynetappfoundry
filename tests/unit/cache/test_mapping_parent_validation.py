"""Regression tests for TypeMapping parent_mapping and parent_id_field validity.

Ensures that every TypeMapping with a parent_mapping value references a
registered mapping name, and that every parent_id_field value corresponds
to an actual field on the parent model class.

See: https://github.com/endavis/pynetappfoundry/issues/335
"""

from __future__ import annotations

import importlib
import pkgutil

import pytest

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import TypeMapping


def _import_all_mapping_modules() -> None:
    """Import every ``mapping`` module under ``pynetappfoundry.cache.ontap``.

    This triggers ``model_registry.register_mapping()`` calls in each
    module, ensuring the registry is fully populated before tests run.
    """
    import pynetappfoundry.cache.ontap as root

    for _, modname, _ in pkgutil.walk_packages(
        root.__path__,
        prefix=root.__name__ + ".",
    ):
        if modname.endswith(".mapping"):
            importlib.import_module(modname)


# Populate the registry once at module level.
_import_all_mapping_modules()


def _mappings_with_parent() -> list[tuple[str, TypeMapping]]:
    """Return all registered mappings that declare a parent_mapping."""
    return [
        (name, mapping)
        for name, mapping in model_registry.mappings.items()
        if mapping.parent_mapping is not None
    ]


class TestParentMappingResolution:
    """Every parent_mapping value must resolve to a registered mapping name."""

    @pytest.mark.parametrize(
        ("name", "mapping"),
        _mappings_with_parent(),
        ids=[name for name, _ in _mappings_with_parent()],
    )
    def test_parent_mapping_resolves(self, name: str, mapping: TypeMapping) -> None:
        parent = model_registry.get_mapping(mapping.parent_mapping)  # type: ignore[arg-type]
        assert parent is not None, (
            f"Mapping {name!r} references parent_mapping={mapping.parent_mapping!r} "
            f"which is not registered in model_registry"
        )


class TestParentIdFieldExists:
    """Every parent_id_field must exist on the parent model class."""

    @pytest.mark.parametrize(
        ("name", "mapping"),
        _mappings_with_parent(),
        ids=[name for name, _ in _mappings_with_parent()],
    )
    def test_parent_id_field_exists_on_parent_model(self, name: str, mapping: TypeMapping) -> None:
        if mapping.parent_id_field is None:
            pytest.skip("No parent_id_field set")

        parent = model_registry.get_mapping(mapping.parent_mapping)  # type: ignore[arg-type]
        assert parent is not None, (
            f"Cannot validate parent_id_field: parent_mapping={mapping.parent_mapping!r} not found"
        )

        parent_model = parent.model_class
        # Check Pydantic model_fields (preferred) or fallback to hasattr
        if hasattr(parent_model, "model_fields"):
            field_names = set(parent_model.model_fields.keys())
            assert mapping.parent_id_field in field_names, (
                f"Mapping {name!r} declares parent_id_field={mapping.parent_id_field!r} "
                f"but parent model {parent_model.__name__} has fields: "
                f"{sorted(field_names)}"
            )
        else:
            assert hasattr(parent_model, mapping.parent_id_field), (
                f"Mapping {name!r} declares parent_id_field={mapping.parent_id_field!r} "
                f"but parent model {parent_model.__name__} has no such attribute"
            )
