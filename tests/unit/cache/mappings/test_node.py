"""Tests for the node type mapping definition."""

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
from pynetappfoundry.cache.mappings.node import NODE_MAPPING
from pynetappfoundry.cache.models import NodeInfo

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def full_api_record() -> dict[str, Any]:
    """Full API node record with all fields."""
    return {
        "uuid": "n1-uuid-1234-5678-abcd",
        "name": "PRODCL1-01",
        "serial_number": "123456789",
        "system_id": "0123456789",
        "model": "AFF-A400",
        "location": "rack-1",
        "membership": "available",
        "version": {"full": "NetApp Release 9.14.1: Tue Oct 10 01:00:00 UTC 2024"},
        "storage_configuration": "single_path_ha",
        "system_machine_type": "040000000000",
        "controller": {
            "board": "System Board XXIV",
            "memory_size": 65536000000,
            "cpu": {"count": 16},
        },
        "vm": {"provider_type": "AWS"},
        "ha": {
            "enabled": True,
            "auto_giveback": True,
            "partners": [
                {"uuid": "partner-uuid-1"},
                {"uuid": "partner-uuid-2"},
            ],
        },
        "system_aggregate": {"uuid": "sysaggr-uuid-1"},
        "cluster_interfaces": [
            {"uuid": "clif-uuid-1"},
            {"uuid": "clif-uuid-2"},
        ],
        "management_interfaces": [
            {"uuid": "mgmt-uuid-1"},
        ],
    }


@pytest.fixture
def full_cli_record() -> dict[str, Any]:
    """Full CLI node record with all mapped CLI fields."""
    return {
        "node": "PRODCL1-01",
        "serial-number": "123456789",
        "system-id": "0123456789",
        "model": "AFF-A400",
    }


# ---------------------------------------------------------------------------
# Mapping definition tests
# ---------------------------------------------------------------------------


class TestNodeMappingDefinition:
    """Tests for NODE_MAPPING structure."""

    def test_all_cache_attrs_exist_on_model(self) -> None:
        """Every cache_attr in the mapping is a valid NodeInfo field."""
        model_fields = set(NodeInfo.model_fields.keys())
        for field in NODE_MAPPING.fields:
            assert field.cache_attr in model_fields, (
                f"cache_attr '{field.cache_attr}' not on NodeInfo"
            )

    def test_no_duplicate_cache_attrs(self) -> None:
        """No duplicate cache_attr values."""
        attrs = [f.cache_attr for f in NODE_MAPPING.fields]
        assert len(attrs) == len(set(attrs))

    def test_endpoint(self) -> None:
        """API endpoint is /cluster/nodes?fields=*."""
        assert NODE_MAPPING.api_endpoint == "/cluster/nodes?fields=*"

    def test_cli_command(self) -> None:
        """CLI command is system node show."""
        assert NODE_MAPPING.cli_command == "system node show"

    def test_model_class(self) -> None:
        """Model class is NodeInfo."""
        assert NODE_MAPPING.model_class is NodeInfo

    def test_api_expected_fields(self) -> None:
        """api_expected_fields returns correct top-level keys."""
        expected = NODE_MAPPING.api_expected_fields()
        assert expected == [
            "cluster_interfaces",
            "controller",
            "ha",
            "location",
            "management_interfaces",
            "membership",
            "model",
            "name",
            "serial_number",
            "storage_configuration",
            "system_aggregate",
            "system_id",
            "system_machine_type",
            "uuid",
            "version",
            "vm",
        ]

    def test_field_count(self) -> None:
        """Mapping has expected number of fields (6 original + 14 new)."""
        assert len(NODE_MAPPING.fields) == 20


# ---------------------------------------------------------------------------
# API parsing tests
# ---------------------------------------------------------------------------


class TestNodeApiParsing:
    """Tests for parsing API node records."""

    def test_full_record(self, full_api_record: dict[str, Any]) -> None:
        """Full API record parses to complete NodeInfo."""
        node = parse_api_record(NODE_MAPPING, full_api_record, "[test]")
        assert isinstance(node, NodeInfo)
        # Original fields
        assert node.uuid == "n1-uuid-1234-5678-abcd"
        assert node.name == "PRODCL1-01"
        assert node.serial_number == "123456789"
        assert node.system_id == "0123456789"
        assert node.model == "AFF-A400"
        assert node.location == "rack-1"
        # New fields
        assert node.membership == "available"
        assert node.version_full == "NetApp Release 9.14.1: Tue Oct 10 01:00:00 UTC 2024"
        assert node.storage_configuration == "single_path_ha"
        assert node.system_machine_type == "040000000000"
        assert node.controller_board == "System Board XXIV"
        assert node.controller_memory_size == 65536000000
        assert node.controller_cpu_count == 16
        assert node.vm_provider_type == "AWS"
        assert node.ha_enabled is True
        assert node.ha_auto_giveback is True
        assert node.ha_partner_uuids == ["partner-uuid-1", "partner-uuid-2"]
        assert node.system_aggregate_uuid == "sysaggr-uuid-1"
        assert node.cluster_interface_uuids == ["clif-uuid-1", "clif-uuid-2"]
        assert node.management_interface_uuids == ["mgmt-uuid-1"]

    def test_minimal_record(self) -> None:
        """Minimal record uses defaults for missing fields."""
        record: dict[str, Any] = {"name": "minnode", "uuid": "abc"}
        node = parse_api_record(NODE_MAPPING, record, "[test]")
        assert isinstance(node, NodeInfo)
        assert node.name == "minnode"
        assert node.uuid == "abc"
        assert node.serial_number == ""
        assert node.system_id == ""
        assert node.model == ""
        assert node.location == ""
        assert node.membership == ""
        assert node.version_full == ""
        assert node.storage_configuration == ""
        assert node.system_machine_type == ""
        assert node.controller_board == ""
        assert node.controller_memory_size == 0
        assert node.controller_cpu_count == 0
        assert node.vm_provider_type == ""
        assert node.ha_enabled is False
        assert node.ha_auto_giveback is False
        assert node.ha_partner_uuids == []
        assert node.system_aggregate_uuid == ""
        assert node.cluster_interface_uuids == []
        assert node.management_interface_uuids == []

    def test_wildcard_partners_extraction(self) -> None:
        """ha.partners[*].uuid extracts list of partner UUIDs."""
        record: dict[str, Any] = {
            "ha": {
                "partners": [
                    {"uuid": "p1"},
                    {"uuid": "p2"},
                    {"uuid": "p3"},
                ],
            },
        }
        node = parse_api_record(NODE_MAPPING, record, "[test]")
        assert node.ha_partner_uuids == ["p1", "p2", "p3"]

    def test_wildcard_cluster_interfaces(self) -> None:
        """cluster_interfaces[*].uuid extracts list of interface UUIDs."""
        record: dict[str, Any] = {
            "cluster_interfaces": [
                {"uuid": "ci1"},
                {"uuid": "ci2"},
            ],
        }
        node = parse_api_record(NODE_MAPPING, record, "[test]")
        assert node.cluster_interface_uuids == ["ci1", "ci2"]

    def test_wildcard_management_interfaces(self) -> None:
        """management_interfaces[*].uuid extracts list of interface UUIDs."""
        record: dict[str, Any] = {
            "management_interfaces": [
                {"uuid": "mi1"},
            ],
        }
        node = parse_api_record(NODE_MAPPING, record, "[test]")
        assert node.management_interface_uuids == ["mi1"]

    def test_wildcard_empty_list(self) -> None:
        """Wildcard on empty list returns empty list."""
        record: dict[str, Any] = {
            "ha": {"partners": []},
            "cluster_interfaces": [],
            "management_interfaces": [],
        }
        node = parse_api_record(NODE_MAPPING, record, "[test]")
        assert node.ha_partner_uuids == []
        assert node.cluster_interface_uuids == []
        assert node.management_interface_uuids == []

    def test_nested_version_extraction(self) -> None:
        """version.full dot-path works."""
        record: dict[str, Any] = {"version": {"full": "9.14.1"}}
        node = parse_api_record(NODE_MAPPING, record, "[test]")
        assert node.version_full == "9.14.1"

    def test_nested_controller_cpu_extraction(self) -> None:
        """controller.cpu.count deep dot-path works."""
        record: dict[str, Any] = {"controller": {"cpu": {"count": 8}}}
        node = parse_api_record(NODE_MAPPING, record, "[test]")
        assert node.controller_cpu_count == 8

    def test_nested_controller_memory_extraction(self) -> None:
        """controller.memory_size dot-path works."""
        record: dict[str, Any] = {"controller": {"memory_size": 32768000000}}
        node = parse_api_record(NODE_MAPPING, record, "[test]")
        assert node.controller_memory_size == 32768000000

    def test_nested_system_aggregate_extraction(self) -> None:
        """system_aggregate.uuid dot-path works."""
        record: dict[str, Any] = {"system_aggregate": {"uuid": "sa-uuid"}}
        node = parse_api_record(NODE_MAPPING, record, "[test]")
        assert node.system_aggregate_uuid == "sa-uuid"

    def test_nested_vm_extraction(self) -> None:
        """vm.provider_type dot-path works."""
        record: dict[str, Any] = {"vm": {"provider_type": "Azure"}}
        node = parse_api_record(NODE_MAPPING, record, "[test]")
        assert node.vm_provider_type == "Azure"

    def test_parse_api_response_multiple(self) -> None:
        """parse_api_response handles multiple records."""
        response = {
            "records": [
                {"name": "node1", "uuid": "a"},
                {"name": "node2", "uuid": "b"},
            ],
        }
        results = parse_api_response(NODE_MAPPING, response, "[test]", MagicMock())
        assert len(results) == 2
        assert results[0].name == "node1"
        assert results[1].name == "node2"


# ---------------------------------------------------------------------------
# CLI parsing tests
# ---------------------------------------------------------------------------


class TestNodeCliParsing:
    """Tests for parsing CLI node records."""

    def test_full_record(self, full_cli_record: dict[str, Any]) -> None:
        """Full CLI record parses to NodeInfo with CLI fields populated."""
        node = parse_cli_record(NODE_MAPPING, full_cli_record, "[test]")
        assert isinstance(node, NodeInfo)
        assert node.name == "PRODCL1-01"
        assert node.serial_number == "123456789"
        assert node.system_id == "0123456789"
        assert node.model == "AFF-A400"
        # Fields without cli_field should use defaults
        assert node.uuid == ""
        assert node.location == ""
        assert node.membership == ""
        assert node.version_full == ""
        assert node.storage_configuration == ""
        assert node.system_machine_type == ""
        assert node.controller_board == ""
        assert node.controller_memory_size == 0
        assert node.controller_cpu_count == 0
        assert node.vm_provider_type == ""
        assert node.ha_enabled is False
        assert node.ha_auto_giveback is False
        assert node.ha_partner_uuids == []
        assert node.system_aggregate_uuid == ""
        assert node.cluster_interface_uuids == []
        assert node.management_interface_uuids == []

    def test_dash_values_use_defaults(self) -> None:
        """CLI dash values coerce to default."""
        record = {
            "node": "-",
            "serial-number": "-",
            "system-id": "-",
            "model": "-",
        }
        node = parse_cli_record(NODE_MAPPING, record, "[test]")
        assert node.name == ""
        assert node.serial_number == ""
        assert node.system_id == ""
        assert node.model == ""

    def test_parse_cli_records_multiple(self) -> None:
        """parse_cli_records handles multiple records."""
        records = [
            {"node": "node1", "serial-number": "111"},
            {"node": "node2", "serial-number": "222"},
        ]
        results = parse_cli_records(NODE_MAPPING, records, "[test]", MagicMock())
        assert len(results) == 2
        assert results[0].name == "node1"
        assert results[1].name == "node2"


# ---------------------------------------------------------------------------
# Parity test: old parser vs new framework
# ---------------------------------------------------------------------------


class TestParityWithOldParser:
    """Verify framework produces same output as old hand-written parser.

    Note: parity tests cover the original 6 fields that existed in the old
    parser (excluding dropped is_epsilon). New fields have no old-parser
    equivalent.
    """

    @staticmethod
    def _old_parse_node_api(record: dict[str, Any]) -> NodeInfo:
        """Reproduce old inline node parsing logic for API records."""
        return NodeInfo(
            uuid=record.get("uuid", ""),
            name=record.get("name", ""),
            serial_number=record.get("serial_number", ""),
            system_id=str(record.get("system_id", "")),
            model=str(record.get("model", "")),
            location=record.get("location", ""),
        )

    @staticmethod
    def _old_parse_node_cli(data: dict[str, Any]) -> NodeInfo:
        """Reproduce old inline node parsing logic for CLI records."""
        return NodeInfo(
            name=data.get("node", ""),
            serial_number=data.get("serial-number", ""),
            system_id=data.get("system-id", ""),
            model=data.get("model", ""),
        )

    _ORIGINAL_FIELDS = (
        "uuid",
        "name",
        "serial_number",
        "system_id",
        "model",
        "location",
    )

    def test_parity_api_full_record(self, full_api_record: dict[str, Any]) -> None:
        """Framework and old parser produce identical NodeInfo for original fields."""
        old = self._old_parse_node_api(full_api_record)
        new = parse_api_record(NODE_MAPPING, full_api_record, "[test]")
        assert isinstance(new, NodeInfo)
        for field_name in self._ORIGINAL_FIELDS:
            old_val = getattr(old, field_name)
            new_val = getattr(new, field_name)
            assert old_val == new_val, (
                f"Field '{field_name}' differs: old={old_val!r}, new={new_val!r}"
            )

    def test_parity_api_minimal_record(self) -> None:
        """Framework and old parser match on minimal API record."""
        record: dict[str, Any] = {"name": "testnode", "uuid": "xyz"}
        old = self._old_parse_node_api(record)
        new = parse_api_record(NODE_MAPPING, record, "[test]")
        assert isinstance(new, NodeInfo)
        for field_name in self._ORIGINAL_FIELDS:
            old_val = getattr(old, field_name)
            new_val = getattr(new, field_name)
            assert old_val == new_val, (
                f"Field '{field_name}' differs: old={old_val!r}, new={new_val!r}"
            )

    def test_parity_api_int_system_id_and_model(self) -> None:
        """Framework handles int system_id/model same as old str() wrapping."""
        record: dict[str, Any] = {
            "name": "node1",
            "uuid": "abc",
            "system_id": 1234567890,
            "model": 12345,
        }
        old = self._old_parse_node_api(record)
        new = parse_api_record(NODE_MAPPING, record, "[test]")
        assert isinstance(new, NodeInfo)
        # Old parser wrapped in str(), Pydantic lax mode coerces int→str
        assert old.system_id == new.system_id
        assert old.model == new.model

    def test_parity_api_missing_nested(self) -> None:
        """Framework and old parser match with missing fields."""
        record: dict[str, Any] = {"name": "node1"}
        old = self._old_parse_node_api(record)
        new = parse_api_record(NODE_MAPPING, record, "[test]")
        assert isinstance(new, NodeInfo)
        for field_name in self._ORIGINAL_FIELDS:
            old_val = getattr(old, field_name)
            new_val = getattr(new, field_name)
            assert old_val == new_val, (
                f"Field '{field_name}' differs: old={old_val!r}, new={new_val!r}"
            )

    def test_parity_cli_full_record(self, full_cli_record: dict[str, Any]) -> None:
        """Framework and old parser produce identical NodeInfo for CLI."""
        old = self._old_parse_node_cli(full_cli_record)
        new = parse_cli_record(NODE_MAPPING, full_cli_record, "[test]")
        assert isinstance(new, NodeInfo)
        for field_name in self._ORIGINAL_FIELDS:
            old_val = getattr(old, field_name)
            new_val = getattr(new, field_name)
            assert old_val == new_val, (
                f"Field '{field_name}' differs: old={old_val!r}, new={new_val!r}"
            )
