"""Tests for cache._registry module -- ModelRegistry (mappings only)."""

from __future__ import annotations

import logging

import pytest
from pydantic import BaseModel

from pynetappfoundry.cache._registry import ModelRegistry, _ensure_bootstrapped


class TestModelRegistry:
    """Tests for ModelRegistry class."""

    def test_register_and_get_mapping(self) -> None:
        from pynetappfoundry.cache.field_mapping import TypeMapping

        registry = ModelRegistry()

        class Bar(BaseModel):
            pass

        mapping = TypeMapping(name="Bar", model_class=Bar, api_endpoint="/test")
        registry.register_mapping("BAR_MAPPING", mapping)
        assert registry.get_mapping("BAR_MAPPING") is mapping

    def test_get_mapping_missing(self) -> None:
        registry = ModelRegistry()
        assert registry.get_mapping("MISSING") is None

    def test_unregister_mapping_removes_from_both_indexes(self) -> None:
        from pynetappfoundry.cache.field_mapping import TypeMapping

        registry = ModelRegistry()

        class Baz(BaseModel):
            pass

        mapping = TypeMapping(name="Baz", model_class=Baz, api_endpoint="/baz")
        registry.register_mapping("BAZ", mapping)
        assert registry.get_mapping("BAZ") is mapping
        assert registry.get_mapping_by_model_class(Baz) is mapping

        registry.unregister_mapping("BAZ")
        assert registry.get_mapping("BAZ") is None
        assert registry.get_mapping_by_model_class(Baz) is None

    def test_unregister_mapping_is_idempotent(self) -> None:
        registry = ModelRegistry()
        # Must not raise on a name that was never registered.
        registry.unregister_mapping("NEVER_REGISTERED")
        registry.unregister_mapping("NEVER_REGISTERED")

    def test_mappings_property_returns_copy(self) -> None:
        from pynetappfoundry.cache.field_mapping import TypeMapping

        registry = ModelRegistry()

        class Qux(BaseModel):
            pass

        mapping = TypeMapping(name="Qux", model_class=Qux, api_endpoint="/q")
        registry.register_mapping("QUX", mapping)
        copy = registry.mappings
        copy["injected"] = mapping  # type: ignore[assignment]
        assert "injected" not in registry.mappings


class TestGlobalRegistryBootstrap:
    """Regression: importing ``pynetappfoundry.cache`` must register every
    TypeMapping under ``cache/ontap/**/mapping.py`` so later lookups via
    ``model_registry.get_mapping_by_model_class(model_class)`` succeed.

    Prior to the fix bundled with #524, importing ``pynetappfoundry.cache``
    only pulled in each sub-package's ``__init__.py`` (which imports the
    **model**, not the ``mapping.py``). As a result, many mapping modules
    never called ``register_mapping()``, and ``nf cache refresh`` failed at
    runtime with "fetch(): no TypeMapping registered for model class
    OntapCifsShare" (and similar) because the collector's phase methods
    pass model classes directly to ``fetchers.fetch()``.

    The fix: ``cache/__init__.py`` walks the ``cache.ontap`` package tree
    and explicitly imports every ``mapping.py`` module on first load.
    """

    def test_cifs_share_mapping_registered_after_cache_import(self) -> None:
        """A model whose mapping was previously missing registers now."""
        # Import the cache package (triggers the walk-packages bootstrap).
        import pynetappfoundry.cache  # noqa: F401
        from pynetappfoundry.cache._registry import model_registry
        from pynetappfoundry.models.ontap.protocols.cifs.shares.model import (
            OntapCifsShare,
        )

        mapping = model_registry.get_mapping_by_model_class(OntapCifsShare)
        assert mapping is not None
        assert mapping.model_class is OntapCifsShare

    def test_broad_sample_of_mappings_registered(self) -> None:
        """Spot-check a representative sample across cache.ontap sub-trees."""
        import pynetappfoundry.cache  # noqa: F401
        from pynetappfoundry.cache._registry import model_registry
        from pynetappfoundry.models.ontap.cluster.model import ClusterInfo
        from pynetappfoundry.models.ontap.cluster.nodes.model import (
            OntapNodeResponse,
        )
        from pynetappfoundry.models.ontap.network.ip.interfaces.model import (
            OntapIpInterface,
        )
        from pynetappfoundry.models.ontap.protocols.cifs.services.model import (
            OntapCifsService,
        )
        from pynetappfoundry.models.ontap.protocols.cifs.shares.model import (
            OntapCifsShare,
        )
        from pynetappfoundry.models.ontap.storage.volumes.model import OntapVolume
        from pynetappfoundry.models.ontap.svm.svms.model import OntapSvm

        sample_models = (
            ClusterInfo,
            OntapNodeResponse,
            OntapSvm,
            OntapCifsService,
            OntapCifsShare,
            OntapIpInterface,
            OntapVolume,
        )
        for model_class in sample_models:
            mapping = model_registry.get_mapping_by_model_class(model_class)
            assert mapping is not None, (
                f"No mapping registered for {model_class.__name__!r} — "
                "check cache/__init__.py mapping-import bootstrap."
            )
            assert mapping.model_class is model_class


class TestEnsureBootstrapped:
    """Tests for the ``_ensure_bootstrapped`` guard function."""

    def test_noop_when_cache_already_loaded(self) -> None:
        """Calling ``_ensure_bootstrapped`` after the cache package is loaded is a no-op."""
        import pynetappfoundry.cache  # noqa: F401
        from pynetappfoundry.cache._registry import model_registry

        # Snapshot current registry state
        before = dict(model_registry._mappings)
        assert len(before) > 0, "Registry should already be populated"

        # Calling the guard again must not raise or alter the registry
        _ensure_bootstrapped()

        after = dict(model_registry._mappings)
        assert before == after


class TestDuplicateRegistrationWarning:
    """Tests for the duplicate-registration warning guard (issue #603).

    When two mappings register under the same class name but target
    different model classes, ``register_mapping`` emits a
    ``logger.warning`` with both api_endpoint contexts.  This surfaces
    codegen regressions in CI/logs without making registry import a
    hard failure (last-wins is preserved for backward compat).
    """

    def test_warns_on_duplicate_with_different_model_class(
        self,
        caplog: pytest.LogCaptureFixture,
    ) -> None:
        from pynetappfoundry.cache.field_mapping import TypeMapping

        class ModelA(BaseModel):
            pass

        class ModelB(BaseModel):
            pass

        registry = ModelRegistry()
        first = TypeMapping(name="Foo", model_class=ModelA, api_endpoint="/a", api_type="dii")
        second = TypeMapping(name="Foo", model_class=ModelB, api_endpoint="/b", api_type="dii")

        registry.register_mapping("Foo", first)
        with caplog.at_level(logging.WARNING, logger="pynetappfoundry.cache._registry"):
            registry.register_mapping("Foo", second)

        # Warning was emitted with both api_endpoint contexts
        warnings = [r for r in caplog.records if r.levelno == logging.WARNING]
        assert len(warnings) == 1
        msg = warnings[0].getMessage()
        assert "Foo" in msg
        assert "'/a'" in msg
        assert "'/b'" in msg
        assert "ModelA" in msg
        assert "ModelB" in msg

        # Last-wins: the second mapping is what the registry now holds
        assert registry.get_mapping("Foo") is second

    def test_no_warning_on_same_instance_reregister(
        self,
        caplog: pytest.LogCaptureFixture,
    ) -> None:
        """Re-registering the exact same mapping instance does not warn."""
        from pynetappfoundry.cache.field_mapping import TypeMapping

        class Model(BaseModel):
            pass

        registry = ModelRegistry()
        mapping = TypeMapping(name="Foo", model_class=Model, api_endpoint="/a")

        registry.register_mapping("Foo", mapping)
        with caplog.at_level(logging.WARNING, logger="pynetappfoundry.cache._registry"):
            registry.register_mapping("Foo", mapping)

        warnings = [r for r in caplog.records if r.levelno == logging.WARNING]
        assert not warnings, "re-registering same instance must not warn"

    def test_no_warning_when_model_class_matches(
        self,
        caplog: pytest.LogCaptureFixture,
    ) -> None:
        """Overlay-loader-style updates (same model_class, new instance) do not warn.

        ``overlay_loader.apply_overlay_to_mapping`` returns a new
        ``TypeMapping`` with updated field configs but the same
        ``model_class``.  Treating that as a duplicate would spam the
        log on every package import.
        """
        from pynetappfoundry.cache.field_mapping import TypeMapping

        class Model(BaseModel):
            pass

        registry = ModelRegistry()
        first = TypeMapping(name="Foo", model_class=Model, api_endpoint="/a")
        updated = TypeMapping(name="Foo", model_class=Model, api_endpoint="/a")

        registry.register_mapping("Foo", first)
        with caplog.at_level(logging.WARNING, logger="pynetappfoundry.cache._registry"):
            registry.register_mapping("Foo", updated)

        warnings = [r for r in caplog.records if r.levelno == logging.WARNING]
        assert not warnings, "same model_class update must not warn"
        assert registry.get_mapping("Foo") is updated
