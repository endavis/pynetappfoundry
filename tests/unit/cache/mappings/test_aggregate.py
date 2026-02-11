"""Tests for the aggregate type mapping definition."""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock

import pytest

from pynetappfoundry.cache.field_mapping import (
    parse_api_record,
    parse_api_response,
)
from pynetappfoundry.cache.storage.aggregates.mapping import AGGREGATE_MAPPING
from pynetappfoundry.cache.storage.aggregates.model import AggregateInfo

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def full_api_record() -> dict[str, Any]:
    """Full API aggregate record with all fields."""
    return {
        "uuid": "a1b2c3d4-5678-9abc-def0-123456789abc",
        "name": "PRODAGGR1",
        "node": {"name": "PRODCL1-01"},
        "state": "online",
        "block_storage": {
            "primary": {
                "disk_type": "ssd",
                "disk_count": 24,
                "raid_type": "raid_dp",
                "disk_class": "solid_state",
                "raid_size": 23,
                "checksum_style": "block",
            },
            "storage_type": "ssd",
            "uses_partitions": True,
            "mirror": {
                "enabled": False,
                "state": "unmirrored",
            },
            "hybrid_cache": {
                "enabled": False,
            },
        },
        "space": {
            "block_storage": {
                "size": 10995116277760,
            },
        },
        "snaplock_type": "non_snaplock",
        "home_node": {"name": "PRODCL1-01"},
        "dr_home_node": {"name": "PRODCL1-DR-01"},
        "create_time": "2024-01-15T10:30:00Z",
        "cloud_storage": {
            "attach_eligible": True,
        },
        "data_encryption": {
            "software_encryption_enabled": True,
            "drive_protection_enabled": False,
        },
        "sidl_enabled": True,
        "inactive_data_reporting": {
            "enabled": True,
        },
        "is_spare_low": False,
        "volume_count": 40,
    }


# ---------------------------------------------------------------------------
# Mapping definition tests
# ---------------------------------------------------------------------------


class TestAggregateMappingDefinition:
    """Tests for AGGREGATE_MAPPING structure."""

    def test_all_cache_attrs_exist_on_model(self) -> None:
        """Every cache_attr in the mapping is a valid AggregateInfo field."""
        model_fields = set(AggregateInfo.model_fields.keys())
        for field in AGGREGATE_MAPPING.fields:
            assert field.cache_attr in model_fields, (
                f"cache_attr '{field.cache_attr}' not on AggregateInfo"
            )

    def test_no_duplicate_cache_attrs(self) -> None:
        """No duplicate cache_attr values."""
        attrs = [f.cache_attr for f in AGGREGATE_MAPPING.fields]
        assert len(attrs) == len(set(attrs))

    def test_endpoint(self) -> None:
        """API endpoint includes explicit fields not returned by fields=*."""
        assert (
            AGGREGATE_MAPPING.api_endpoint
            == "/storage/aggregates?fields=*,is_spare_low,sidl_enabled"
        )

    def test_cli_command(self) -> None:
        """CLI command is aggr show."""
        assert AGGREGATE_MAPPING.cli_command == "aggr show"

    def test_model_class(self) -> None:
        """Model class is AggregateInfo."""
        assert AGGREGATE_MAPPING.model_class is AggregateInfo

    def test_api_expected_fields(self) -> None:
        """api_expected_fields returns correct top-level keys."""
        expected = AGGREGATE_MAPPING.api_expected_fields()
        assert expected == [
            "block_storage",
            "cloud_storage",
            "create_time",
            "data_encryption",
            "dr_home_node",
            "home_node",
            "inactive_data_reporting",
            "is_spare_low",
            "name",
            "node",
            "sidl_enabled",
            "snaplock_type",
            "space",
            "state",
            "uuid",
            "volume_count",
        ]

    def test_field_count(self) -> None:
        """Mapping has expected number of fields (9 original + 19 new)."""
        assert len(AGGREGATE_MAPPING.fields) == 28


# ---------------------------------------------------------------------------
# API parsing tests
# ---------------------------------------------------------------------------


class TestAggregateApiParsing:
    """Tests for parsing API aggregate records."""

    def test_full_record(self, full_api_record: dict[str, Any]) -> None:
        """Full API record parses to complete AggregateInfo."""
        aggr = parse_api_record(AGGREGATE_MAPPING, full_api_record, "[test]")
        assert isinstance(aggr, AggregateInfo)
        # Original fields
        assert aggr.uuid == "a1b2c3d4-5678-9abc-def0-123456789abc"
        assert aggr.name == "PRODAGGR1"
        assert aggr.node == "PRODCL1-01"
        assert aggr.state == "online"
        assert aggr.type == "ssd"
        assert aggr.total_size == 10995116277760
        assert aggr.disk_count == 24
        assert aggr.disk_type == "ssd"
        assert aggr.raid_type == "raid_dp"
        # New block_storage structural fields
        assert aggr.storage_type == "ssd"
        assert aggr.disk_class == "solid_state"
        assert aggr.raid_size == 23
        assert aggr.checksum_style == "block"
        assert aggr.uses_partitions is True
        assert aggr.mirror_enabled is False
        assert aggr.mirror_state == "unmirrored"
        assert aggr.hybrid_cache_enabled is False
        # New structural fields
        assert aggr.snaplock_type == "non_snaplock"
        assert aggr.home_node == "PRODCL1-01"
        assert aggr.dr_home_node == "PRODCL1-DR-01"
        assert aggr.create_time == "2024-01-15T10:30:00Z"
        # Config flags
        assert aggr.cloud_attach_eligible is True
        assert aggr.encryption_software is True
        assert aggr.encryption_drive is False
        assert aggr.sidl_enabled is True
        assert aggr.inactive_data_reporting_enabled is True
        assert aggr.volume_count == 40
        # Expensive field
        assert aggr.is_spare_low is False

    def test_minimal_record(self) -> None:
        """Minimal record uses defaults for missing fields."""
        record: dict[str, Any] = {"name": "minaggr", "uuid": "abc"}
        aggr = parse_api_record(AGGREGATE_MAPPING, record, "[test]")
        assert isinstance(aggr, AggregateInfo)
        assert aggr.name == "minaggr"
        assert aggr.uuid == "abc"
        assert aggr.node == ""
        assert aggr.state == ""
        assert aggr.type == ""
        assert aggr.total_size == 0
        assert aggr.disk_count == 0
        assert aggr.disk_type == ""
        assert aggr.raid_type == ""
        # New fields default correctly
        assert aggr.storage_type == ""
        assert aggr.disk_class == ""
        assert aggr.raid_size == 0
        assert aggr.checksum_style == ""
        assert aggr.uses_partitions is False
        assert aggr.mirror_enabled is False
        assert aggr.mirror_state == ""
        assert aggr.hybrid_cache_enabled is False
        assert aggr.snaplock_type == ""
        assert aggr.home_node == ""
        assert aggr.dr_home_node == ""
        assert aggr.create_time == ""
        assert aggr.cloud_attach_eligible is False
        assert aggr.encryption_software is False
        assert aggr.encryption_drive is False
        assert aggr.sidl_enabled is False
        assert aggr.inactive_data_reporting_enabled is False
        assert aggr.volume_count == 0
        assert aggr.is_spare_low is False

    def test_nested_node_extraction(self) -> None:
        """node.name dot-path works."""
        record: dict[str, Any] = {"node": {"name": "node1"}}
        aggr = parse_api_record(AGGREGATE_MAPPING, record, "[test]")
        assert aggr.node == "node1"

    def test_deep_nested_block_storage(self) -> None:
        """block_storage.primary.* fields extracted correctly."""
        record: dict[str, Any] = {
            "block_storage": {
                "primary": {
                    "disk_type": "hdd",
                    "disk_count": 12,
                    "raid_type": "raid4",
                    "disk_class": "capacity",
                    "raid_size": 14,
                    "checksum_style": "advanced_zoned",
                },
                "storage_type": "hdd",
                "uses_partitions": False,
                "mirror": {
                    "enabled": True,
                    "state": "normal",
                },
                "hybrid_cache": {
                    "enabled": True,
                },
            },
        }
        aggr = parse_api_record(AGGREGATE_MAPPING, record, "[test]")
        assert aggr.type == "hdd"
        assert aggr.disk_count == 12
        assert aggr.disk_type == "hdd"
        assert aggr.raid_type == "raid4"
        assert aggr.storage_type == "hdd"
        assert aggr.disk_class == "capacity"
        assert aggr.raid_size == 14
        assert aggr.checksum_style == "advanced_zoned"
        assert aggr.uses_partitions is False
        assert aggr.mirror_enabled is True
        assert aggr.mirror_state == "normal"
        assert aggr.hybrid_cache_enabled is True

    def test_deep_nested_space(self) -> None:
        """space.block_storage.size extracted correctly."""
        record: dict[str, Any] = {
            "space": {
                "block_storage": {
                    "size": 5000000000,
                },
            },
        }
        aggr = parse_api_record(AGGREGATE_MAPPING, record, "[test]")
        assert aggr.total_size == 5000000000

    def test_home_node_and_dr_home_node(self) -> None:
        """home_node.name and dr_home_node.name extracted correctly."""
        record: dict[str, Any] = {
            "home_node": {"name": "cluster1-01"},
            "dr_home_node": {"name": "cluster1-dr-01"},
        }
        aggr = parse_api_record(AGGREGATE_MAPPING, record, "[test]")
        assert aggr.home_node == "cluster1-01"
        assert aggr.dr_home_node == "cluster1-dr-01"

    def test_data_encryption_fields(self) -> None:
        """data_encryption nested booleans extracted correctly."""
        record: dict[str, Any] = {
            "data_encryption": {
                "software_encryption_enabled": True,
                "drive_protection_enabled": True,
            },
        }
        aggr = parse_api_record(AGGREGATE_MAPPING, record, "[test]")
        assert aggr.encryption_software is True
        assert aggr.encryption_drive is True

    def test_cloud_storage_and_inactive_reporting(self) -> None:
        """cloud_storage and inactive_data_reporting nested extraction."""
        record: dict[str, Any] = {
            "cloud_storage": {"attach_eligible": True},
            "inactive_data_reporting": {"enabled": True},
        }
        aggr = parse_api_record(AGGREGATE_MAPPING, record, "[test]")
        assert aggr.cloud_attach_eligible is True
        assert aggr.inactive_data_reporting_enabled is True

    def test_top_level_booleans(self) -> None:
        """Top-level boolean fields extracted correctly."""
        record: dict[str, Any] = {
            "sidl_enabled": True,
            "is_spare_low": True,
        }
        aggr = parse_api_record(AGGREGATE_MAPPING, record, "[test]")
        assert aggr.sidl_enabled is True
        assert aggr.is_spare_low is True

    def test_parse_api_response_multiple(self) -> None:
        """parse_api_response handles multiple records."""
        response = {
            "records": [
                {"name": "aggr1", "uuid": "a"},
                {"name": "aggr2", "uuid": "b"},
            ],
        }
        results = parse_api_response(AGGREGATE_MAPPING, response, "[test]", MagicMock())
        assert len(results) == 2
        assert results[0].name == "aggr1"
        assert results[1].name == "aggr2"


# ---------------------------------------------------------------------------
# Parity test: old parser vs new framework
# ---------------------------------------------------------------------------


class TestParityWithOldParser:
    """Verify framework produces same output as old hand-written parser.

    Note: parity tests only cover the original 9 fields that existed in the
    old parser. New fields have no old-parser equivalent.
    """

    @staticmethod
    def _old_parse_aggregate_api(record: dict[str, Any]) -> AggregateInfo:
        """Reproduce old inline aggregate parsing logic for API records."""
        block_storage = record.get("block_storage", {})
        primary = block_storage.get("primary", {})
        return AggregateInfo(
            uuid=record.get("uuid", ""),
            name=record.get("name", ""),
            node=record.get("node", {}).get("name", ""),
            state=record.get("state", ""),
            type=primary.get("disk_type", ""),
            total_size=record.get("space", {}).get("block_storage", {}).get("size", 0),
            disk_count=primary.get("disk_count", 0),
            disk_type=primary.get("disk_type", ""),
            raid_type=primary.get("raid_type", ""),
        )

    _ORIGINAL_FIELDS = (
        "uuid",
        "name",
        "node",
        "state",
        "type",
        "total_size",
        "disk_count",
        "disk_type",
        "raid_type",
    )

    def test_parity_api_full_record(self, full_api_record: dict[str, Any]) -> None:
        """Framework and old parser produce identical AggregateInfo for original fields."""
        old = self._old_parse_aggregate_api(full_api_record)
        new = parse_api_record(AGGREGATE_MAPPING, full_api_record, "[test]")
        assert isinstance(new, AggregateInfo)
        for field_name in self._ORIGINAL_FIELDS:
            old_val = getattr(old, field_name)
            new_val = getattr(new, field_name)
            assert old_val == new_val, (
                f"Field '{field_name}' differs: old={old_val!r}, new={new_val!r}"
            )

    def test_parity_api_minimal_record(self) -> None:
        """Framework and old parser match on minimal API record."""
        record: dict[str, Any] = {"name": "testaggr", "uuid": "xyz"}
        old = self._old_parse_aggregate_api(record)
        new = parse_api_record(AGGREGATE_MAPPING, record, "[test]")
        assert isinstance(new, AggregateInfo)
        for field_name in self._ORIGINAL_FIELDS:
            old_val = getattr(old, field_name)
            new_val = getattr(new, field_name)
            assert old_val == new_val, (
                f"Field '{field_name}' differs: old={old_val!r}, new={new_val!r}"
            )

    def test_parity_api_missing_nested(self) -> None:
        """Framework and old parser match with missing nested objects."""
        record: dict[str, Any] = {
            "name": "aggr1",
            "node": {},
            "block_storage": {},
            "space": {},
        }
        old = self._old_parse_aggregate_api(record)
        new = parse_api_record(AGGREGATE_MAPPING, record, "[test]")
        assert isinstance(new, AggregateInfo)
        for field_name in self._ORIGINAL_FIELDS:
            old_val = getattr(old, field_name)
            new_val = getattr(new, field_name)
            assert old_val == new_val, (
                f"Field '{field_name}' differs: old={old_val!r}, new={new_val!r}"
            )
