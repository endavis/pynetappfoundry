"""Tests for the NetworkLIF type mapping definition."""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock

import pytest

from pynetappfoundry.cache.field_mapping import (
    parse_api_record,
    parse_api_response,
)
from pynetappfoundry.cache.network.ip.interfaces.mapping import (
    NETWORK_LIF_MAPPING,
)
from pynetappfoundry.cache.network.ip.interfaces.model import (
    NetworkLIF,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def full_api_record() -> dict[str, Any]:
    """Full API network LIF record with all fields populated."""
    return {
        "uuid": "lif-uuid-1234",
        "name": "data_lif1",
        "ip": {
            "address": "10.0.0.10",
            "netmask": "255.255.255.0",
            "family": "ipv4",
        },
        "enabled": True,
        "state": "up",
        "scope": "svm",
        "vip": False,
        "svm": {"name": "svm1", "uuid": "svm-uuid-1"},
        "ipspace": {"name": "Default", "uuid": "ipspace-uuid-1"},
        "service_policy": {"name": "default-data-files", "uuid": "sp-uuid-1"},
        "services": ["data_core", "data_nfs"],
        "location": {
            "auto_revert": True,
            "failover": "sfo-partner-only",
            "is_home": True,
            "home_node": {"name": "node1", "uuid": "home-node-uuid-1"},
            "home_port": {"name": "e0d", "uuid": "home-port-uuid-1"},
            "node": {"name": "node1", "uuid": "current-node-uuid-1"},
            "port": {"name": "e0d", "uuid": "current-port-uuid-1"},
        },
        "dns_zone": "example.com",
        "ddns_enabled": False,
        "subnet": {"name": "data-subnet", "uuid": "subnet-uuid-1"},
        "probe_port": 8080,
        "rdma_protocols": ["roce"],
    }


# ---------------------------------------------------------------------------
# Mapping definition tests
# ---------------------------------------------------------------------------


class TestNetworkLIFMappingDefinition:
    """Tests for NETWORK_LIF_MAPPING structure."""

    def test_all_cache_attrs_exist_on_model(self) -> None:
        """Every cache_attr in the mapping is a valid NetworkLIF field."""
        model_fields = set(NetworkLIF.model_fields.keys())
        for field in NETWORK_LIF_MAPPING.fields:
            assert field.cache_attr in model_fields, (
                f"cache_attr '{field.cache_attr}' not on NetworkLIF"
            )

    def test_no_duplicate_cache_attrs(self) -> None:
        """No duplicate cache_attr values."""
        attrs = [f.cache_attr for f in NETWORK_LIF_MAPPING.fields]
        assert len(attrs) == len(set(attrs))

    def test_field_count(self) -> None:
        """Mapping has expected number of fields (25)."""
        assert len(NETWORK_LIF_MAPPING.fields) == 25

    def test_model_class(self) -> None:
        """Model class is NetworkLIF."""
        assert NETWORK_LIF_MAPPING.model_class is NetworkLIF

    def test_endpoint(self) -> None:
        """API endpoint is correct."""
        assert NETWORK_LIF_MAPPING.api_endpoint == "/network/ip/interfaces?fields=*"

    def test_cli_command_empty(self) -> None:
        """CLI command is empty (API-only type)."""
        assert NETWORK_LIF_MAPPING.cli_command == ""

    def test_api_expected_fields(self) -> None:
        """api_expected_fields returns correct top-level keys."""
        expected = NETWORK_LIF_MAPPING.api_expected_fields()
        assert expected == [
            "ddns_enabled",
            "dns_zone",
            "enabled",
            "ip",
            "ipspace",
            "location",
            "name",
            "probe_port",
            "rdma_protocols",
            "scope",
            "service_policy",
            "services",
            "state",
            "subnet",
            "svm",
            "uuid",
            "vip",
        ]

    def test_id_field(self) -> None:
        """id_field is name (default)."""
        assert NETWORK_LIF_MAPPING.id_field == "name"


# ---------------------------------------------------------------------------
# API parsing tests
# ---------------------------------------------------------------------------


class TestNetworkLIFApiParsing:
    """Tests for parsing API network LIF records."""

    def test_full_record(self, full_api_record: dict[str, Any]) -> None:
        """Full API record parses correctly."""
        result = parse_api_record(NETWORK_LIF_MAPPING, full_api_record, "[test]")
        assert isinstance(result, NetworkLIF)
        assert result.uuid == "lif-uuid-1234"
        assert result.name == "data_lif1"
        assert result.ip_address == "10.0.0.10"
        assert result.netmask == "255.255.255.0"
        assert result.ip_family == "ipv4"
        assert result.enabled is True
        assert result.state == "up"
        assert result.scope == "svm"
        assert result.vip is False
        assert result.svm_uuid == "svm-uuid-1"
        assert result.ipspace_uuid == "ipspace-uuid-1"
        assert result.service_policy_uuid == "sp-uuid-1"
        assert result.services == ["data_core", "data_nfs"]
        assert result.auto_revert is True
        assert result.failover == "sfo-partner-only"
        assert result.is_home is True
        assert result.home_node_uuid == "home-node-uuid-1"
        assert result.home_port_uuid == "home-port-uuid-1"
        assert result.current_node_uuid == "current-node-uuid-1"
        assert result.current_port_uuid == "current-port-uuid-1"
        assert result.dns_zone == "example.com"
        assert result.ddns_enabled is False
        assert result.subnet_uuid == "subnet-uuid-1"
        assert result.probe_port == 8080
        assert result.rdma_protocols == ["roce"]

    def test_minimal_record(self) -> None:
        """Minimal record uses defaults for missing fields."""
        record: dict[str, Any] = {"uuid": "lif-min", "name": "minimal_lif"}
        result = parse_api_record(NETWORK_LIF_MAPPING, record, "[test]")
        assert isinstance(result, NetworkLIF)
        assert result.uuid == "lif-min"
        assert result.name == "minimal_lif"
        assert result.ip_address == ""
        assert result.netmask == ""
        assert result.ip_family == ""
        assert result.enabled is True
        assert result.state == ""
        assert result.scope == ""
        assert result.vip is False
        assert result.svm_uuid == ""
        assert result.ipspace_uuid == ""
        assert result.service_policy_uuid == ""
        assert result.services == []
        assert result.auto_revert is False
        assert result.failover == ""
        assert result.is_home is True
        assert result.home_node_uuid == ""
        assert result.home_port_uuid == ""
        assert result.current_node_uuid == ""
        assert result.current_port_uuid == ""
        assert result.dns_zone == ""
        assert result.ddns_enabled is False
        assert result.subnet_uuid == ""
        assert result.probe_port == 0
        assert result.rdma_protocols == []

    def test_missing_nested_objects(self) -> None:
        """Record without nested objects defaults nested fields to empty strings."""
        record: dict[str, Any] = {
            "uuid": "lif-no-nested",
            "name": "no_nested_lif",
            "ip": {"address": "10.0.0.1"},
        }
        result = parse_api_record(NETWORK_LIF_MAPPING, record, "[test]")
        assert isinstance(result, NetworkLIF)
        assert result.ip_address == "10.0.0.1"
        assert result.netmask == ""
        assert result.svm_uuid == ""
        assert result.ipspace_uuid == ""
        assert result.service_policy_uuid == ""
        assert result.home_node_uuid == ""
        assert result.home_port_uuid == ""
        assert result.current_node_uuid == ""
        assert result.current_port_uuid == ""
        assert result.subnet_uuid == ""

    def test_parse_api_response_multiple(self) -> None:
        """parse_api_response handles multiple records."""
        response = {
            "records": [
                {
                    "uuid": "lif-1",
                    "name": "data_lif1",
                    "ip": {"address": "10.0.0.10", "netmask": "255.255.255.0"},
                    "scope": "svm",
                    "svm": {"uuid": "svm-uuid-1"},
                },
                {
                    "uuid": "lif-2",
                    "name": "ic_lif1",
                    "ip": {"address": "10.0.1.1", "netmask": "255.255.255.0"},
                    "scope": "cluster",
                    "svm": {"uuid": "svm-uuid-2"},
                },
            ],
        }
        results = parse_api_response(NETWORK_LIF_MAPPING, response, "[test]", MagicMock())
        assert len(results) == 2
        assert results[0].uuid == "lif-1"  # type: ignore[union-attr]
        assert results[1].uuid == "lif-2"  # type: ignore[union-attr]

    def test_parse_api_response_empty(self) -> None:
        """parse_api_response handles empty/None response."""
        assert parse_api_response(NETWORK_LIF_MAPPING, None, "[test]", MagicMock()) == []
        assert parse_api_response(NETWORK_LIF_MAPPING, {}, "[test]", MagicMock()) == []


# ---------------------------------------------------------------------------
# Parity test: old parser vs new framework
# ---------------------------------------------------------------------------


class TestParityWithOldParser:
    """Verify framework produces same output as old hand-written inline parser.

    Parity is checked for the 3 shared fields only (name, ip_address, netmask).
    The old parser extracted ``svm.name``, ``home_node.name``, ``home_port.name``;
    the new mapping extracts UUIDs instead, so those fields differ by design.
    The old ``role`` field was dead code (never set by collector) and is removed.
    """

    _ORIGINAL_SHARED_FIELDS = (
        "name",
        "ip_address",
        "netmask",
    )

    @staticmethod
    def _old_parse_lif(record: dict[str, Any]) -> NetworkLIF:
        """Reproduce old inline LIF parsing logic from collector.

        This is a static copy of the code that was in
        ``_collect_network_via_api`` before migration, adapted to the
        new model field names where applicable.
        """
        return NetworkLIF(
            name=record.get("name", ""),
            ip_address=record.get("ip", {}).get("address", ""),
            netmask=record.get("ip", {}).get("netmask", ""),
        )

    def test_parity_full_record(self, full_api_record: dict[str, Any]) -> None:
        """Framework and old parser produce identical results for shared fields."""
        old = self._old_parse_lif(full_api_record)
        new = parse_api_record(NETWORK_LIF_MAPPING, full_api_record, "[test]")
        assert isinstance(new, NetworkLIF)
        for field_name in self._ORIGINAL_SHARED_FIELDS:
            old_val = getattr(old, field_name)
            new_val = getattr(new, field_name)
            assert old_val == new_val, (
                f"Field '{field_name}' differs: old={old_val!r}, new={new_val!r}"
            )

    def test_parity_minimal_record(self) -> None:
        """Framework and old parser match on minimal record."""
        record: dict[str, Any] = {"uuid": "lif-1", "name": "data_lif1"}
        old = self._old_parse_lif(record)
        new = parse_api_record(NETWORK_LIF_MAPPING, record, "[test]")
        assert isinstance(new, NetworkLIF)
        for field_name in self._ORIGINAL_SHARED_FIELDS:
            old_val = getattr(old, field_name)
            new_val = getattr(new, field_name)
            assert old_val == new_val, (
                f"Field '{field_name}' differs: old={old_val!r}, new={new_val!r}"
            )

    def test_parity_old_stored_svm_name_new_stores_uuid(
        self, full_api_record: dict[str, Any]
    ) -> None:
        """Old parser used svm.name; new mapping uses svm.uuid."""
        new = parse_api_record(NETWORK_LIF_MAPPING, full_api_record, "[test]")
        assert isinstance(new, NetworkLIF)
        # New mapping stores svm uuid
        assert new.svm_uuid == "svm-uuid-1"

    def test_parity_old_stored_node_name_new_stores_uuid(
        self, full_api_record: dict[str, Any]
    ) -> None:
        """Old parser used home_node.name; new mapping uses home_node.uuid."""
        new = parse_api_record(NETWORK_LIF_MAPPING, full_api_record, "[test]")
        assert isinstance(new, NetworkLIF)
        # New mapping stores home_node uuid
        assert new.home_node_uuid == "home-node-uuid-1"

    def test_parity_old_stored_port_name_new_stores_uuid(
        self, full_api_record: dict[str, Any]
    ) -> None:
        """Old parser used home_port.name; new mapping uses home_port.uuid."""
        new = parse_api_record(NETWORK_LIF_MAPPING, full_api_record, "[test]")
        assert isinstance(new, NetworkLIF)
        # New mapping stores home_port uuid
        assert new.home_port_uuid == "home-port-uuid-1"
