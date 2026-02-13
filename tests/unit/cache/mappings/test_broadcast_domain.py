"""Tests for the BroadcastDomain type mapping definition."""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock

import pytest

from pynetappfoundry.cache.field_mapping import (
    parse_api_record,
    parse_api_response,
)
from pynetappfoundry.cache.network.ethernet.broadcast_domains.mapping import (
    BROADCAST_DOMAIN_MAPPING,
)
from pynetappfoundry.cache.network.ethernet.broadcast_domains.model import (
    BroadcastDomain,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def full_api_record() -> dict[str, Any]:
    """Full API broadcast domain record with all fields populated."""
    return {
        "uuid": "bd-uuid-1234",
        "name": "Default",
        "mtu": 1500,
        "ipspace": {"name": "Default", "uuid": "ipspace-uuid-1"},
        "ports": [
            {"name": "node1:e0c", "uuid": "port-uuid-1"},
            {"name": "node1:e0d", "uuid": "port-uuid-2"},
        ],
    }


# ---------------------------------------------------------------------------
# Mapping definition tests
# ---------------------------------------------------------------------------


class TestBroadcastDomainMappingDefinition:
    """Tests for BROADCAST_DOMAIN_MAPPING structure."""

    def test_all_cache_attrs_exist_on_model(self) -> None:
        """Every cache_attr in the mapping is a valid BroadcastDomain field."""
        model_fields = set(BroadcastDomain.model_fields.keys())
        for field in BROADCAST_DOMAIN_MAPPING.fields:
            assert field.cache_attr in model_fields, (
                f"cache_attr '{field.cache_attr}' not on BroadcastDomain"
            )

    def test_no_duplicate_cache_attrs(self) -> None:
        """No duplicate cache_attr values."""
        attrs = [f.cache_attr for f in BROADCAST_DOMAIN_MAPPING.fields]
        assert len(attrs) == len(set(attrs))

    def test_field_count(self) -> None:
        """Mapping has expected number of fields (5)."""
        assert len(BROADCAST_DOMAIN_MAPPING.fields) == 5

    def test_model_class(self) -> None:
        """Model class is BroadcastDomain."""
        assert BROADCAST_DOMAIN_MAPPING.model_class is BroadcastDomain

    def test_endpoint(self) -> None:
        """API endpoint is correct."""
        assert BROADCAST_DOMAIN_MAPPING.api_endpoint == (
            "/network/ethernet/broadcast-domains?fields=*"
        )

    def test_cli_command_empty(self) -> None:
        """CLI command is empty (API-only type)."""
        assert BROADCAST_DOMAIN_MAPPING.cli_command == ""

    def test_api_expected_fields(self) -> None:
        """api_expected_fields returns correct top-level keys."""
        expected = BROADCAST_DOMAIN_MAPPING.api_expected_fields()
        assert expected == [
            "ipspace",
            "mtu",
            "name",
            "ports",
            "uuid",
        ]

    def test_id_field(self) -> None:
        """id_field is name (default)."""
        assert BROADCAST_DOMAIN_MAPPING.id_field == "name"


# ---------------------------------------------------------------------------
# API parsing tests
# ---------------------------------------------------------------------------


class TestBroadcastDomainApiParsing:
    """Tests for parsing API broadcast domain records."""

    def test_full_record(self, full_api_record: dict[str, Any]) -> None:
        """Full API record parses correctly."""
        result = parse_api_record(BROADCAST_DOMAIN_MAPPING, full_api_record, "[test]")
        assert isinstance(result, BroadcastDomain)
        assert result.uuid == "bd-uuid-1234"
        assert result.name == "Default"
        assert result.mtu == 1500
        assert result.ipspace_uuid == "ipspace-uuid-1"
        assert result.port_uuids == ["port-uuid-1", "port-uuid-2"]

    def test_minimal_record(self) -> None:
        """Minimal record uses defaults for missing fields."""
        record: dict[str, Any] = {"uuid": "bd-min", "name": "Minimal"}
        result = parse_api_record(BROADCAST_DOMAIN_MAPPING, record, "[test]")
        assert isinstance(result, BroadcastDomain)
        assert result.uuid == "bd-min"
        assert result.name == "Minimal"
        assert result.mtu == 0
        assert result.ipspace_uuid == ""
        assert result.port_uuids == []

    def test_missing_nested_ipspace(self) -> None:
        """Record without ipspace defaults ipspace_uuid to empty string."""
        record: dict[str, Any] = {
            "uuid": "bd-no-ipspace",
            "name": "NoIpspace",
            "mtu": 9000,
        }
        result = parse_api_record(BROADCAST_DOMAIN_MAPPING, record, "[test]")
        assert isinstance(result, BroadcastDomain)
        assert result.ipspace_uuid == ""

    def test_missing_ports(self) -> None:
        """Record without ports defaults port_uuids to empty list."""
        record: dict[str, Any] = {
            "uuid": "bd-no-ports",
            "name": "NoPorts",
            "mtu": 1500,
            "ipspace": {"name": "Default", "uuid": "ipspace-uuid-1"},
        }
        result = parse_api_record(BROADCAST_DOMAIN_MAPPING, record, "[test]")
        assert isinstance(result, BroadcastDomain)
        assert result.port_uuids == []

    def test_parse_api_response_multiple(self) -> None:
        """parse_api_response handles multiple records."""
        response = {
            "records": [
                {
                    "uuid": "bd-1",
                    "name": "Default",
                    "mtu": 1500,
                    "ipspace": {"name": "Default", "uuid": "ipspace-uuid-1"},
                    "ports": [{"name": "node1:e0c", "uuid": "port-uuid-1"}],
                },
                {
                    "uuid": "bd-2",
                    "name": "Cluster",
                    "mtu": 9000,
                    "ipspace": {"name": "Cluster", "uuid": "ipspace-uuid-2"},
                    "ports": [{"name": "node1:e0a", "uuid": "port-uuid-3"}],
                },
            ],
        }
        results = parse_api_response(BROADCAST_DOMAIN_MAPPING, response, "[test]", MagicMock())
        assert len(results) == 2
        assert results[0].uuid == "bd-1"  # type: ignore[union-attr]
        assert results[1].uuid == "bd-2"  # type: ignore[union-attr]

    def test_parse_api_response_empty(self) -> None:
        """parse_api_response handles empty/None response."""
        assert parse_api_response(BROADCAST_DOMAIN_MAPPING, None, "[test]", MagicMock()) == []
        assert parse_api_response(BROADCAST_DOMAIN_MAPPING, {}, "[test]", MagicMock()) == []


# ---------------------------------------------------------------------------
# Parity test: old parser vs new framework
# ---------------------------------------------------------------------------


class TestParityWithOldParser:
    """Verify framework produces same output as old hand-written inline parser.

    Parity is checked for the original 3 shared fields only (uuid, name, mtu).
    The old parser extracted ``ipspace.name`` and port names; the new mapping
    extracts ``ipspace.uuid`` and port UUIDs, so those fields differ by design.
    """

    _ORIGINAL_SHARED_FIELDS = (
        "uuid",
        "name",
        "mtu",
    )

    @staticmethod
    def _old_parse_broadcast_domain(record: dict[str, Any]) -> BroadcastDomain:
        """Reproduce old inline broadcast domain parsing logic from collector.

        This is a static copy of the code that was in
        ``_collect_network_via_api`` before migration, adapted to the
        new model field names where applicable.
        """
        return BroadcastDomain(
            uuid=record.get("uuid", ""),
            name=record.get("name", ""),
            mtu=record.get("mtu", 0),
            # Old parser stored ipspace name; new stores ipspace uuid
            ipspace_uuid=record.get("ipspace", {}).get("name", ""),
            # Old parser stored port names; new stores port uuids
            port_uuids=[p.get("name", "") for p in record.get("ports", []) if p.get("name")],
        )

    def test_parity_full_record(self, full_api_record: dict[str, Any]) -> None:
        """Framework and old parser produce identical results for shared fields."""
        old = self._old_parse_broadcast_domain(full_api_record)
        new = parse_api_record(BROADCAST_DOMAIN_MAPPING, full_api_record, "[test]")
        assert isinstance(new, BroadcastDomain)
        for field_name in self._ORIGINAL_SHARED_FIELDS:
            old_val = getattr(old, field_name)
            new_val = getattr(new, field_name)
            assert old_val == new_val, (
                f"Field '{field_name}' differs: old={old_val!r}, new={new_val!r}"
            )

    def test_parity_minimal_record(self) -> None:
        """Framework and old parser match on minimal record."""
        record: dict[str, Any] = {"uuid": "bd-1", "name": "Default"}
        old = self._old_parse_broadcast_domain(record)
        new = parse_api_record(BROADCAST_DOMAIN_MAPPING, record, "[test]")
        assert isinstance(new, BroadcastDomain)
        for field_name in self._ORIGINAL_SHARED_FIELDS:
            old_val = getattr(old, field_name)
            new_val = getattr(new, field_name)
            assert old_val == new_val, (
                f"Field '{field_name}' differs: old={old_val!r}, new={new_val!r}"
            )

    def test_parity_ipspace_name_vs_uuid(self, full_api_record: dict[str, Any]) -> None:
        """Old parser used ipspace.name; new mapping uses ipspace.uuid."""
        old = self._old_parse_broadcast_domain(full_api_record)
        new = parse_api_record(BROADCAST_DOMAIN_MAPPING, full_api_record, "[test]")
        assert isinstance(new, BroadcastDomain)
        # Old parser stored ipspace name
        assert old.ipspace_uuid == "Default"
        # New mapping stores ipspace uuid
        assert new.ipspace_uuid == "ipspace-uuid-1"

    def test_parity_ports_names_vs_uuids(self, full_api_record: dict[str, Any]) -> None:
        """Old parser used port names; new mapping uses port UUIDs."""
        old = self._old_parse_broadcast_domain(full_api_record)
        new = parse_api_record(BROADCAST_DOMAIN_MAPPING, full_api_record, "[test]")
        assert isinstance(new, BroadcastDomain)
        # Old parser stored port names
        assert old.port_uuids == ["node1:e0c", "node1:e0d"]
        # New mapping stores port uuids
        assert new.port_uuids == ["port-uuid-1", "port-uuid-2"]
