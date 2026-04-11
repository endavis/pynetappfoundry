"""Tests for cache._registry module -- ModelRegistry (mappings only)."""

from __future__ import annotations

from pydantic import BaseModel

from pynetappfoundry.cache._registry import ModelRegistry


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
