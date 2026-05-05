"""Mapping registry for cache field mappings.

Provides a module-level singleton ``model_registry`` that collects
``TypeMapping`` definitions at import time.  Each ``mapping.py`` module
calls ``model_registry.register_mapping()`` to register its mapping.

Two parallel indexes are maintained: a name-keyed ``_mappings`` dict
(the original API) and a class-keyed ``_mappings_by_class`` dict used by
:func:`pynetappfoundry.cache.fetchers.fetch` for model-class lookups.
Both are populated at ``register_mapping()`` time.  A defensive
:func:`_ensure_bootstrapped` guard triggers the ``cache`` package
import (which walks ``cache/ontap/**/mapping.py``) on first lookup,
so callers no longer need manual mapping imports.
"""

from __future__ import annotations

import logging
import sys
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pydantic import BaseModel

    from pynetappfoundry.cache.field_mapping import TypeMapping

logger = logging.getLogger(__name__)


def _ensure_bootstrapped() -> None:
    """Import the cache package if it hasn't been loaded yet.

    The ``cache/__init__.py`` module walks ``cache.ontap`` and imports
    every ``mapping.py``, which registers all :class:`TypeMapping`
    instances on :data:`model_registry`.  Most code paths already
    trigger this import transitively, but registry look-ups that run
    before the cache package is loaded would see an empty registry.

    This guard makes the registration self-healing: callers no longer
    need manual ``import pynetappfoundry.cache.ontap.<...>.mapping``
    lines.

    Cost: a single ``dict.__contains__`` on the common (already-loaded)
    path.
    """
    if "pynetappfoundry.cache" not in sys.modules:
        import pynetappfoundry.cache  # noqa: F401


class ModelRegistry:
    """Registry of cache field mappings.

    Mappings are registered explicitly by each ``mapping.py`` module
    at import time.  Look-up methods call :func:`_ensure_bootstrapped`
    so callers do not need manual mapping imports.
    """

    def __init__(self) -> None:
        self._mappings: dict[str, TypeMapping] = {}
        self._mappings_by_class: dict[type[BaseModel], TypeMapping] = {}

    def register_mapping(self, name: str, mapping: TypeMapping) -> None:
        """Register a type mapping by name.

        Emits a warning (but still registers, last-wins) when the same
        name is already bound to a mapping targeting a **different**
        ``model_class``.  Collisions of that shape usually indicate a
        codegen regression where multiple endpoints share a response
        schema and produce the same class name — see ADR-0008 for the
        shared-schema naming rule that prevents this for generated
        mappings.  The warning surfaces the regression in CI/logs
        without making registry import a hard failure.

        Re-registrations that target the **same** model_class (e.g. the
        overlay loader's ``replace(mapping, fields=...)`` pass) are
        treated as legitimate updates and do not warn.

        Args:
            name: Identifier for the mapping (e.g. ``"AGGREGATE_MAPPING"``).
            mapping: The TypeMapping instance.
        """
        existing = self._mappings.get(name)
        if (
            existing is not None
            and existing is not mapping
            and existing.model_class is not mapping.model_class
        ):
            logger.warning(
                "Duplicate mapping registration for %r: replacing "
                "api_endpoint=%r (api_type=%r, model_class=%r) with "
                "api_endpoint=%r (api_type=%r, model_class=%r). "
                "Last-wins behavior preserved — see ADR-0008 "
                "shared-schema naming rule.",
                name,
                existing.api_endpoint,
                existing.api_type,
                existing.model_class.__name__,
                mapping.api_endpoint,
                mapping.api_type,
                mapping.model_class.__name__,
            )
        self._mappings[name] = mapping
        self._mappings_by_class[mapping.model_class] = mapping

    def unregister_mapping(self, name: str) -> None:
        """Remove a mapping from both indexes by name.

        Idempotent: silently ignores names that are not registered.
        Primarily intended for test fixtures that register a mapping
        for the duration of one test and need to tear it down without
        reaching into the private indexes.

        Args:
            name: Identifier of the mapping to remove.
        """
        mapping = self._mappings.pop(name, None)
        if mapping is not None:
            self._mappings_by_class.pop(mapping.model_class, None)

    def get_mapping(self, name: str) -> TypeMapping | None:
        """Look up a type mapping by name.

        Args:
            name: Identifier of the mapping.

        Returns:
            The TypeMapping instance, or None if not registered.
        """
        _ensure_bootstrapped()
        return self._mappings.get(name)

    def get_mapping_by_model_class(self, model_class: type[BaseModel]) -> TypeMapping | None:
        """Look up a type mapping by its Pydantic model class.

        Args:
            model_class: The Pydantic model class registered on a TypeMapping.

        Returns:
            The TypeMapping instance, or None if no mapping registers that
            class.
        """
        _ensure_bootstrapped()
        return self._mappings_by_class.get(model_class)

    @property
    def mappings(self) -> dict[str, TypeMapping]:
        """Return a defensive copy of all registered mappings."""
        return dict(self._mappings)


model_registry = ModelRegistry()
