"""Model registry for automatic discovery of cache models and mappings.

Provides a module-level singleton ``model_registry`` that collects all
``CacheModel`` subclasses (via ``__init_subclass__``) and their associated
``TypeMapping`` definitions at import time.

This module is imported lazily by ``_base.CacheModel.__init_subclass__``
to avoid circular dependencies.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pydantic import BaseModel

    from pynetappfoundry.cache.field_mapping import TypeMapping


class ModelRegistry:
    """Registry of cache models and their field mappings.

    Models are registered automatically when their class is defined
    (via ``CacheModel.__init_subclass__``).  Mappings are registered
    explicitly by each ``mapping.py`` module at import time.
    """

    def __init__(self) -> None:
        self._models: dict[str, type[BaseModel]] = {}
        self._mappings: dict[str, TypeMapping] = {}

    def register_model(self, cls: type[BaseModel]) -> None:
        """Register a model class by its ``__name__``.

        Model names must be unique across the entire ``cache/`` tree.
        If two classes share the same ``__name__``, the second registration
        silently overwrites the first.

        Args:
            cls: The model class to register.
        """
        self._models[cls.__name__] = cls

    def register_mapping(self, name: str, mapping: TypeMapping) -> None:
        """Register a type mapping by name.

        Args:
            name: Identifier for the mapping (e.g. ``"AGGREGATE_MAPPING"``).
            mapping: The TypeMapping instance.
        """
        self._mappings[name] = mapping

    def get_model(self, name: str) -> type[BaseModel] | None:
        """Look up a model class by name.

        Args:
            name: Class name of the model.

        Returns:
            The model class, or None if not registered.
        """
        return self._models.get(name)

    def get_mapping(self, name: str) -> TypeMapping | None:
        """Look up a type mapping by name.

        Args:
            name: Identifier of the mapping.

        Returns:
            The TypeMapping instance, or None if not registered.
        """
        return self._mappings.get(name)

    @property
    def models(self) -> dict[str, type[BaseModel]]:
        """Return a defensive copy of all registered models."""
        return dict(self._models)

    @property
    def mappings(self) -> dict[str, TypeMapping]:
        """Return a defensive copy of all registered mappings."""
        return dict(self._mappings)


model_registry = ModelRegistry()
