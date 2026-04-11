"""Mapping registry for cache field mappings.

Provides a module-level singleton ``model_registry`` that collects
``TypeMapping`` definitions at import time.  Each ``mapping.py`` module
calls ``model_registry.register_mapping()`` to register its mapping.

Two parallel indexes are maintained: a name-keyed ``_mappings`` dict
(the original API) and a class-keyed ``_mappings_by_class`` dict used by
:func:`pynetappfoundry.cache.fetchers.fetch` for model-class lookups.
Both are populated at ``register_mapping()`` time, so mapping modules
must be imported before any lookup fires — same import-order rule as
the original name-keyed registry.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pydantic import BaseModel

    from pynetappfoundry.cache.field_mapping import TypeMapping


class ModelRegistry:
    """Registry of cache field mappings.

    Mappings are registered explicitly by each ``mapping.py`` module
    at import time.
    """

    def __init__(self) -> None:
        self._mappings: dict[str, TypeMapping] = {}
        self._mappings_by_class: dict[type[BaseModel], TypeMapping] = {}

    def register_mapping(self, name: str, mapping: TypeMapping) -> None:
        """Register a type mapping by name.

        Args:
            name: Identifier for the mapping (e.g. ``"AGGREGATE_MAPPING"``).
            mapping: The TypeMapping instance.
        """
        self._mappings[name] = mapping
        self._mappings_by_class[mapping.model_class] = mapping

    def get_mapping(self, name: str) -> TypeMapping | None:
        """Look up a type mapping by name.

        Args:
            name: Identifier of the mapping.

        Returns:
            The TypeMapping instance, or None if not registered.
        """
        return self._mappings.get(name)

    def get_mapping_by_model_class(self, model_class: type[BaseModel]) -> TypeMapping | None:
        """Look up a type mapping by its Pydantic model class.

        Args:
            model_class: The Pydantic model class registered on a TypeMapping.

        Returns:
            The TypeMapping instance, or None if no mapping registers that
            class.
        """
        return self._mappings_by_class.get(model_class)

    @property
    def mappings(self) -> dict[str, TypeMapping]:
        """Return a defensive copy of all registered mappings."""
        return dict(self._mappings)


model_registry = ModelRegistry()
