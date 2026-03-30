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
