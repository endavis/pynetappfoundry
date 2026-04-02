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
        # Resolve dotted parent_id_field paths (e.g. "svm.uuid") by
        # walking through nested Pydantic model_fields.
        parts = mapping.parent_id_field.split(".")
        current_model = parent_model
        for i, part in enumerate(parts):
            if hasattr(current_model, "model_fields"):
                field_names = set(current_model.model_fields.keys())
                assert part in field_names, (
                    f"Mapping {name!r} declares parent_id_field={mapping.parent_id_field!r} "
                    f"but {current_model.__name__} has no field {part!r} "
                    f"(available: {sorted(field_names)})"
                )
                # If there are more parts, descend into the nested model
                if i < len(parts) - 1:
                    field_info = current_model.model_fields[part]
                    current_model = field_info.annotation
            else:
                assert hasattr(current_model, part), (
                    f"Mapping {name!r} declares parent_id_field={mapping.parent_id_field!r} "
                    f"but {current_model.__name__} has no attribute {part!r}"
                )
