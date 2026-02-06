"""Tests for the aggregate type mapping definition."""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock

import pytest

from pynetappfoundry.cache.field_mapping import (
    parse_api_record,
    parse_api_response,
    parse_cli_record,
    parse_cli_records,
)
from pynetappfoundry.cache.mappings.aggregate import AGGREGATE_MAPPING
from pynetappfoundry.cache.models import AggregateInfo

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
            },
        },
        "space": {
            "block_storage": {
                "size": 10995116277760,
            },
        },
    }


@pytest.fixture
def full_cli_record() -> dict[str, Any]:
    """Full CLI aggregate record with all fields."""
    return {
        "aggregate": "PRODAGGR1",
        "node": "PRODCL1-01",
        "state": "online",
        "type": "ssd",
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
        """API endpoint is storage aggregates with all fields."""
        assert AGGREGATE_MAPPING.api_endpoint == "/storage/aggregates?fields=*"

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
            "name",
            "node",
            "space",
            "state",
            "uuid",
        ]


# ---------------------------------------------------------------------------
# API parsing tests
# ---------------------------------------------------------------------------


class TestAggregateApiParsing:
    """Tests for parsing API aggregate records."""

    def test_full_record(self, full_api_record: dict[str, Any]) -> None:
        """Full API record parses to complete AggregateInfo."""
        aggr = parse_api_record(AGGREGATE_MAPPING, full_api_record, "[test]")
        assert isinstance(aggr, AggregateInfo)
        assert aggr.uuid == "a1b2c3d4-5678-9abc-def0-123456789abc"
        assert aggr.name == "PRODAGGR1"
        assert aggr.node == "PRODCL1-01"
        assert aggr.state == "online"
        assert aggr.type == "ssd"
        assert aggr.total_size == 10995116277760
        assert aggr.disk_count == 24
        assert aggr.disk_type == "ssd"
        assert aggr.raid_type == "raid_dp"

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
                },
            },
        }
        aggr = parse_api_record(AGGREGATE_MAPPING, record, "[test]")
        assert aggr.type == "hdd"
        assert aggr.disk_count == 12
        assert aggr.disk_type == "hdd"
        assert aggr.raid_type == "raid4"

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
# CLI parsing tests
# ---------------------------------------------------------------------------


class TestAggregateCliParsing:
    """Tests for parsing CLI aggregate records."""

    def test_full_record(self, full_cli_record: dict[str, Any]) -> None:
        """Full CLI record parses to complete AggregateInfo."""
        aggr = parse_cli_record(AGGREGATE_MAPPING, full_cli_record, "[test]")
        assert isinstance(aggr, AggregateInfo)
        assert aggr.name == "PRODAGGR1"
        assert aggr.node == "PRODCL1-01"
        assert aggr.state == "online"
        assert aggr.type == "ssd"
        # Fields without cli_field should use defaults
        assert aggr.uuid == ""
        assert aggr.total_size == 0
        assert aggr.disk_count == 0
        assert aggr.disk_type == ""
        assert aggr.raid_type == ""

    def test_dash_values_use_defaults(self) -> None:
        """CLI dash values coerce to default."""
        record = {
            "aggregate": "-",
            "node": "-",
            "state": "-",
            "type": "-",
        }
        aggr = parse_cli_record(AGGREGATE_MAPPING, record, "[test]")
        assert aggr.name == ""
        assert aggr.node == ""
        assert aggr.state == ""
        assert aggr.type == ""

    def test_parse_cli_records_multiple(self) -> None:
        """parse_cli_records handles multiple records."""
        records = [
            {"aggregate": "aggr1", "node": "node1"},
            {"aggregate": "aggr2", "node": "node2"},
        ]
        results = parse_cli_records(AGGREGATE_MAPPING, records, "[test]", MagicMock())
        assert len(results) == 2
        assert results[0].name == "aggr1"
        assert results[1].name == "aggr2"


# ---------------------------------------------------------------------------
# Parity test: old parser vs new framework
# ---------------------------------------------------------------------------


class TestParityWithOldParser:
    """Verify framework produces same output as old hand-written parser."""

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

    @staticmethod
    def _old_parse_aggregate_cli(data: dict[str, Any]) -> AggregateInfo:
        """Reproduce old inline aggregate parsing logic for CLI records."""
        return AggregateInfo(
            name=data.get("aggregate", ""),
            node=data.get("node", ""),
            state=data.get("state", ""),
            type=data.get("type", ""),
        )

    def test_parity_api_full_record(self, full_api_record: dict[str, Any]) -> None:
        """Framework and old parser produce identical AggregateInfo for API."""
        old = self._old_parse_aggregate_api(full_api_record)
        new = parse_api_record(AGGREGATE_MAPPING, full_api_record, "[test]")
        assert isinstance(new, AggregateInfo)
        for field_name in AggregateInfo.model_fields:
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
        for field_name in AggregateInfo.model_fields:
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
        for field_name in AggregateInfo.model_fields:
            old_val = getattr(old, field_name)
            new_val = getattr(new, field_name)
            assert old_val == new_val, (
                f"Field '{field_name}' differs: old={old_val!r}, new={new_val!r}"
            )

    def test_parity_cli_full_record(self, full_cli_record: dict[str, Any]) -> None:
        """Framework and old parser produce identical AggregateInfo for CLI."""
        old = self._old_parse_aggregate_cli(full_cli_record)
        new = parse_cli_record(AGGREGATE_MAPPING, full_cli_record, "[test]")
        assert isinstance(new, AggregateInfo)
        for field_name in AggregateInfo.model_fields:
            old_val = getattr(old, field_name)
            new_val = getattr(new, field_name)
            assert old_val == new_val, (
                f"Field '{field_name}' differs: old={old_val!r}, new={new_val!r}"
            )
