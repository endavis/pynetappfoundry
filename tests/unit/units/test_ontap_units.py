"""Tests for ONTAP unit registry population."""

from __future__ import annotations

import pytest

from pynetappfoundry.units.dimensions import BYTES, DAYS, PERCENT
from pynetappfoundry.units.ontap_units import ontap_registry


class TestOntapRegistryPopulation:
    """Tests verifying the ONTAP registry contains expected entries."""

    def test_registry_not_empty(self) -> None:
        assert len(ontap_registry) > 0

    def test_exact_entry_count(self) -> None:
        assert len(ontap_registry) == 8

    # --- Volume fields ---

    def test_volume_size_is_bytes(self) -> None:
        entry = ontap_registry.get("/storage/volumes", "size")
        assert entry is not None
        assert entry.unit is BYTES

    def test_volume_autosize_maximum_is_bytes(self) -> None:
        entry = ontap_registry.get("/storage/volumes", "autosize.maximum")
        assert entry is not None
        assert entry.unit is BYTES

    def test_volume_autosize_minimum_is_bytes(self) -> None:
        entry = ontap_registry.get("/storage/volumes", "autosize.minimum")
        assert entry is not None
        assert entry.unit is BYTES

    def test_volume_grow_threshold_is_percent(self) -> None:
        entry = ontap_registry.get("/storage/volumes", "autosize.grow_threshold")
        assert entry is not None
        assert entry.unit is PERCENT

    def test_volume_shrink_threshold_is_percent(self) -> None:
        entry = ontap_registry.get("/storage/volumes", "autosize.shrink_threshold")
        assert entry is not None
        assert entry.unit is PERCENT

    def test_volume_tiering_cooling_days(self) -> None:
        entry = ontap_registry.get("/storage/volumes", "tiering.min_cooling_days")
        assert entry is not None
        assert entry.unit is DAYS

    # --- Aggregate fields ---

    def test_aggregate_size_is_bytes(self) -> None:
        entry = ontap_registry.get("/storage/aggregates", "space.block_storage.size")
        assert entry is not None
        assert entry.unit is BYTES

    # --- Node fields ---

    def test_node_memory_size_is_bytes(self) -> None:
        entry = ontap_registry.get("/cluster/nodes", "controller.memory_size")
        assert entry is not None
        assert entry.unit is BYTES

    # --- Endpoint grouping ---

    def test_volume_entries_count(self) -> None:
        entries = ontap_registry.get_by_endpoint("/storage/volumes")
        assert len(entries) == 6

    def test_aggregate_entries_count(self) -> None:
        entries = ontap_registry.get_by_endpoint("/storage/aggregates")
        assert len(entries) == 1

    def test_node_entries_count(self) -> None:
        entries = ontap_registry.get_by_endpoint("/cluster/nodes")
        assert len(entries) == 1

    # --- Source traceability ---

    def test_all_entries_have_source(self) -> None:
        for entry in ontap_registry.all_entries():
            assert entry.source, f"Missing source for {entry.endpoint}:{entry.api_field_path}"

    @pytest.mark.parametrize(
        ("endpoint", "field_path"),
        [
            ("/storage/volumes", "size"),
            ("/storage/volumes", "autosize.maximum"),
            ("/storage/volumes", "autosize.minimum"),
            ("/storage/volumes", "autosize.grow_threshold"),
            ("/storage/volumes", "autosize.shrink_threshold"),
            ("/storage/volumes", "tiering.min_cooling_days"),
            ("/storage/aggregates", "space.block_storage.size"),
            ("/cluster/nodes", "controller.memory_size"),
        ],
    )
    def test_all_expected_fields_registered(self, endpoint: str, field_path: str) -> None:
        assert (endpoint, field_path) in ontap_registry
