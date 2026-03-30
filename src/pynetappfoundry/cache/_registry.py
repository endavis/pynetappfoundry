"""Mapping registry for cache field mappings.

Provides a module-level singleton ``model_registry`` that collects
``TypeMapping`` definitions at import time.  Each ``mapping.py`` module
calls ``model_registry.register_mapping()`` to register its mapping.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pynetappfoundry.cache.field_mapping import TypeMapping


class ModelRegistry:
    """Registry of cache field mappings.

    Mappings are registered explicitly by each ``mapping.py`` module
    at import time.
    """

    def __init__(self) -> None:
        self._mappings: dict[str, TypeMapping] = {}

    def register_mapping(self, name: str, mapping: TypeMapping) -> None:
        """Register a type mapping by name.

        Args:
            name: Identifier for the mapping (e.g. ``"AGGREGATE_MAPPING"``).
            mapping: The TypeMapping instance.
        """
        self._mappings[name] = mapping

    def get_mapping(self, name: str) -> TypeMapping | None:
        """Look up a type mapping by name.

        Args:
            name: Identifier of the mapping.

        Returns:
            The TypeMapping instance, or None if not registered.
        """
        return self._mappings.get(name)

    @property
    def mappings(self) -> dict[str, TypeMapping]:
        """Return a defensive copy of all registered mappings."""
        return dict(self._mappings)


model_registry = ModelRegistry()
