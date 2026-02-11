"""Tests for cache._registry module — ModelRegistry."""

from __future__ import annotations

from pydantic import BaseModel

from pynetappfoundry.cache._registry import ModelRegistry


class TestModelRegistry:
    """Tests for ModelRegistry class."""

    def test_register_and_get_model(self) -> None:
        registry = ModelRegistry()

        class Foo(BaseModel):
            x: int = 0

        registry.register_model(Foo)
        assert registry.get_model("Foo") is Foo

    def test_get_model_missing(self) -> None:
        registry = ModelRegistry()
        assert registry.get_model("Nonexistent") is None

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

    def test_models_property_returns_copy(self) -> None:
        registry = ModelRegistry()

        class Baz(BaseModel):
            pass

        registry.register_model(Baz)
        copy = registry.models
        copy["injected"] = Baz  # type: ignore[assignment]
        assert "injected" not in registry.models

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

    def test_duplicate_registration_overwrites(self) -> None:
        registry = ModelRegistry()

        class V1(BaseModel):
            pass

        class V2(BaseModel):
            pass

        # Register both under same name — last wins
        registry._models["Same"] = V1
        registry.register_model(V2)
        # V2 is under its own name
        assert registry.get_model("V2") is V2
        # V1 is still under "Same"
        assert registry.get_model("Same") is V1
