"""Tests for UnitRegistry and UnitEntry."""

from __future__ import annotations

import pytest

from pynetappfoundry.units.dimensions import BYTES, GIB, PERCENT
from pynetappfoundry.units.registry import UnitEntry, UnitRegistry


@pytest.fixture
def registry() -> UnitRegistry:
    """Fresh empty registry for testing."""
    return UnitRegistry()


@pytest.fixture
def sample_entry() -> UnitEntry:
    """Sample entry for /storage/volumes size field."""
    return UnitEntry(
        endpoint="/storage/volumes",
        api_field_path="size",
        unit=BYTES,
        source="test source",
    )


@pytest.fixture
def sample_entry_percent() -> UnitEntry:
    """Sample entry for a percentage field."""
    return UnitEntry(
        endpoint="/storage/volumes",
        api_field_path="autosize.grow_threshold",
        unit=PERCENT,
        source="test source",
    )


class TestUnitEntry:
    """Tests for UnitEntry frozen dataclass."""

    def test_entry_attributes(self, sample_entry: UnitEntry) -> None:
        assert sample_entry.endpoint == "/storage/volumes"
        assert sample_entry.api_field_path == "size"
        assert sample_entry.unit is BYTES
        assert sample_entry.source == "test source"

    def test_entry_is_frozen(self, sample_entry: UnitEntry) -> None:
        with pytest.raises(AttributeError):
            sample_entry.endpoint = "/changed"  # type: ignore[misc]

    def test_entry_equality(self) -> None:
        a = UnitEntry(endpoint="/x", api_field_path="y", unit=BYTES, source="s")
        b = UnitEntry(endpoint="/x", api_field_path="y", unit=BYTES, source="s")
        assert a == b


class TestUnitRegistry:
    """Tests for UnitRegistry."""

    def test_register_and_get(self, registry: UnitRegistry, sample_entry: UnitEntry) -> None:
        registry.register(sample_entry)
        result = registry.get("/storage/volumes", "size")
        assert result is sample_entry

    def test_get_returns_none_for_unknown(self, registry: UnitRegistry) -> None:
        assert registry.get("/unknown", "field") is None

    def test_idempotent_registration(self, registry: UnitRegistry, sample_entry: UnitEntry) -> None:
        registry.register(sample_entry)
        registry.register(sample_entry)
        assert len(registry) == 1

    def test_conflicting_registration_raises(
        self, registry: UnitRegistry, sample_entry: UnitEntry
    ) -> None:
        registry.register(sample_entry)
        conflicting = UnitEntry(
            endpoint="/storage/volumes",
            api_field_path="size",
            unit=GIB,
            source="different",
        )
        with pytest.raises(ValueError, match="Conflicting registration"):
            registry.register(conflicting)

    def test_get_by_endpoint_sorted(
        self,
        registry: UnitRegistry,
        sample_entry: UnitEntry,
        sample_entry_percent: UnitEntry,
    ) -> None:
        registry.register(sample_entry_percent)
        registry.register(sample_entry)
        results = registry.get_by_endpoint("/storage/volumes")
        assert len(results) == 2
        assert results[0].api_field_path == "autosize.grow_threshold"
        assert results[1].api_field_path == "size"

    def test_get_by_endpoint_empty_for_unknown(self, registry: UnitRegistry) -> None:
        assert registry.get_by_endpoint("/unknown") == ()

    def test_all_entries_sorted(self, registry: UnitRegistry, sample_entry: UnitEntry) -> None:
        other = UnitEntry(
            endpoint="/cluster/nodes",
            api_field_path="controller.memory_size",
            unit=BYTES,
            source="test",
        )
        registry.register(sample_entry)
        registry.register(other)
        entries = registry.all_entries()
        assert len(entries) == 2
        assert entries[0].endpoint == "/cluster/nodes"
        assert entries[1].endpoint == "/storage/volumes"

    def test_len(self, registry: UnitRegistry, sample_entry: UnitEntry) -> None:
        assert len(registry) == 0
        registry.register(sample_entry)
        assert len(registry) == 1

    def test_contains(self, registry: UnitRegistry, sample_entry: UnitEntry) -> None:
        assert ("/storage/volumes", "size") not in registry
        registry.register(sample_entry)
        assert ("/storage/volumes", "size") in registry

    def test_register_many(self, registry: UnitRegistry) -> None:
        entries = (
            UnitEntry(endpoint="/a", api_field_path="x", unit=BYTES, source="s"),
            UnitEntry(endpoint="/b", api_field_path="y", unit=PERCENT, source="s"),
        )
        registry.register_many(entries)
        assert len(registry) == 2
        assert registry.get("/a", "x") is entries[0]
        assert registry.get("/b", "y") is entries[1]
