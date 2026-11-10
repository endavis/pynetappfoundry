"""Mapping registry for cache field mappings.

Provides a module-level singleton ``model_registry`` that collects
``TypeMapping`` definitions.  Each ``mapping.py`` module calls
``model_registry.register_mapping()`` when it is imported.

The singleton is built with the generated ``_mapping_index`` (see ADR-0023):
lookups import an indexed ``mapping.py`` on first use instead of importing all
of them at startup.  A bare ``ModelRegistry()`` has no index and behaves as a
plain dict-backed registry.  If the index is stale (a ``mapping.py`` exists that
it does not list), a lookup miss on the singleton falls back to one
``pkgutil.walk_packages`` pass and logs a warning to run ``doit mapping_index``.

Two parallel indexes are maintained: a name-keyed ``_mappings`` dict
(the original API) and a class-keyed ``_mappings_by_class`` dict used by
:func:`pynetappfoundry.cache.fetchers.fetch` for model-class lookups.
Both are populated at ``register_mapping()`` time.
"""

from __future__ import annotations

import importlib
import logging
import pkgutil
import sys
import threading
from collections.abc import Mapping
from typing import TYPE_CHECKING, NamedTuple

if TYPE_CHECKING:
    from pydantic import BaseModel

    from pynetappfoundry.cache.field_mapping import TypeMapping

logger = logging.getLogger(__name__)

# Packages the stale-index fallback walks for ``*.mapping`` modules.
_FALLBACK_PACKAGES: tuple[str, ...] = (
    "pynetappfoundry.cache.ontap",
    "pynetappfoundry.cache.dii",
)


class MappingIndexEntry(NamedTuple):
    """One row of the generated mapping index."""

    mapping_module: str
    """Dotted path of the ``mapping.py`` module that registers the name."""
    model_module: str
    """Module of the mapping's ``model_class``."""
    model_qualname: str
    """``__qualname__`` of the mapping's ``model_class``."""
    overlay: str | None
    """Package TOML overlay path relative to ``cache/``, or ``None``."""


def _ensure_bootstrapped() -> None:
    """Import the cache package if it hasn't been loaded yet.

    The ``cache/__init__.py`` module imports the hand-written mapping
    sub-packages, which register their :class:`TypeMapping` instances on
    :data:`model_registry`.  Most code paths already trigger this import
    transitively, but registry look-ups that run before the cache package
    is loaded would miss them.

    Cost: a single ``dict.__contains__`` on the common (already-loaded)
    path.
    """
    if "pynetappfoundry.cache" not in sys.modules:
        import pynetappfoundry.cache  # noqa: F401


class ModelRegistry:
    """Registry of cache field mappings.

    Mappings are registered explicitly by each ``mapping.py`` module
    when it is imported.  Look-up methods call :func:`_ensure_bootstrapped`
    so callers do not need manual mapping imports.

    Args:
        index: Optional generated mapping index (name -> entry).  With an
            index, look-ups import the indexed ``mapping.py`` on first use,
            and a miss falls back to one stale-index walk.  Without one the
            registry only knows what has been registered.
    """

    def __init__(self, index: Mapping[str, MappingIndexEntry] | None = None) -> None:
        self._mappings: dict[str, TypeMapping] = {}
        self._mappings_by_class: dict[type[BaseModel], TypeMapping] = {}
        self._index: Mapping[str, MappingIndexEntry] | None = index
        self._index_by_class: dict[tuple[str, str], str] = {}
        if index is not None:
            self._index_by_class = {
                (entry.model_module, entry.model_qualname): name for name, entry in index.items()
            }
        self._overlaid: set[str] = set()
        self._walked = False
        self._lock = threading.RLock()

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
        mapping = self._apply_indexed_overlay(name, mapping)
        self._mappings[name] = mapping
        self._mappings_by_class[mapping.model_class] = mapping

    def _apply_indexed_overlay(self, name: str, mapping: TypeMapping) -> TypeMapping:
        """Apply the package TOML overlay for an indexed *name*, once per name."""
        if self._index is None or name not in self._index:
            return mapping
        with self._lock:
            if name in self._overlaid:
                return mapping
            self._overlaid.add(name)
        # Deferred: overlay_loader imports this module.
        from pynetappfoundry.cache import overlay_loader

        rel_path = self._index[name].overlay
        if rel_path is not None and not (overlay_loader._PACKAGE_OVERLAY_ROOT / rel_path).is_file():
            logger.warning(
                "mapping index is stale: overlay %s for %s is missing; run doit mapping_index",
                rel_path,
                name,
            )
            found = overlay_loader.discover_toml_overlays(overlay_loader._PACKAGE_OVERLAY_ROOT)
            path = found.get(name)
            rel_path = (
                path.relative_to(overlay_loader._PACKAGE_OVERLAY_ROOT).as_posix() if path else None
            )
        if rel_path is None:
            return mapping
        return overlay_loader.apply_package_overlay(mapping, rel_path)

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
        self._overlaid.discard(name)

    def _load(self, name: str) -> None:
        """Import the indexed ``mapping.py`` for *name* unless it is already loaded."""
        if self._index is None:
            return
        module = self._index[name].mapping_module
        if module not in sys.modules:
            importlib.import_module(module)

    def _fallback_walk(self) -> None:
        """Import the ``*.mapping`` modules the index does not list (stale index).

        Runs at most once per process and only on a registry that has an index.
        Walks the fallback packages, logs a warning for each unindexed module and
        imports only those.  Indexed modules are never imported here: lookups reach
        them through the index and :attr:`mappings` loads them separately, so an
        unknown name costs a directory walk, not ~470 imports.

        Limit: a mapping renamed inside an already-indexed file is not found by
        name until ``doit mapping_index`` runs.  The index drift test catches that
        in the repository.
        """
        if self._index is None:
            return
        with self._lock:
            if self._walked:
                return
            self._walked = True
            indexed = {entry.mapping_module for entry in self._index.values()}
            for package_name in _FALLBACK_PACKAGES:
                package = importlib.import_module(package_name)
                for info in pkgutil.walk_packages(package.__path__, prefix=f"{package_name}."):
                    if not info.name.endswith(".mapping"):
                        continue
                    if info.name in indexed:
                        continue
                    logger.warning(
                        "mapping index is stale: %s is not indexed; run doit mapping_index",
                        info.name,
                    )
                    if info.name not in sys.modules:
                        importlib.import_module(info.name)

    def get_mapping(self, name: str) -> TypeMapping | None:
        """Look up a type mapping by name.

        Args:
            name: Identifier of the mapping.

        Returns:
            The TypeMapping instance, or None if not registered.
        """
        _ensure_bootstrapped()
        mapping = self._mappings.get(name)
        if mapping is not None or self._index is None:
            return mapping
        if name in self._index:
            self._load(name)
        else:
            self._fallback_walk()
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
        mapping = self._mappings_by_class.get(model_class)
        if mapping is not None or self._index is None:
            return mapping
        indexed_name = self._index_by_class.get((model_class.__module__, model_class.__qualname__))
        if indexed_name is not None:
            self._load(indexed_name)
        else:
            self._fallback_walk()
        return self._mappings_by_class.get(model_class)

    @property
    def mappings(self) -> dict[str, TypeMapping]:
        """Return a defensive copy of all registered mappings.

        On an indexed registry this first imports every indexed ``mapping.py``
        (and runs the stale-index fallback), so the result is complete.
        """
        if self._index is not None:
            _ensure_bootstrapped()
            for name in self._index:
                self._load(name)
            self._fallback_walk()
        return dict(self._mappings)


def _build_singleton() -> ModelRegistry:
    from pynetappfoundry.cache._mapping_index import MAPPING_INDEX

    return ModelRegistry({name: MappingIndexEntry(*row) for name, row in MAPPING_INDEX.items()})


model_registry = _build_singleton()
