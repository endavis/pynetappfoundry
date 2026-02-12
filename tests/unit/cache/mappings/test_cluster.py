"""Tests for the cluster type mapping definition."""

from __future__ import annotations

from typing import Any

import pytest

from pynetappfoundry.cache.cluster.mapping import CLUSTER_MAPPING
from pynetappfoundry.cache.cluster.model import ClusterInfo
from pynetappfoundry.cache.field_mapping import (
    parse_api_record,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def full_api_record() -> dict[str, Any]:
    """Full API cluster record with all fields."""
    return {
        "name": "mycluster",
        "uuid": "abc-123-def-456",
        "version": {
            "full": "NetApp Release 9.14.1",
            "generation": "SIMULATED",
        },
        "contact": "admin@example.com",
        "location": "datacenter-1",
        "san_optimized": True,
        "timezone": {"name": "America/New_York"},
        "dns_domains": ["example.com", "corp.example.com"],
        "name_servers": ["10.0.0.1", "10.0.0.2"],
        "ntp_servers": ["time.nist.gov", "pool.ntp.org"],
        "peering_policy": {
            "authentication_required": True,
            "encryption_required": True,
            "minimum_passphrase_length": 8,
        },
        "management_interfaces": [
            {"uuid": "mgmt-uuid-1"},
            {"uuid": "mgmt-uuid-2"},
        ],
        "disaggregated": True,
        "auto_enable_activity_tracking": True,
        "auto_enable_analytics": True,
    }


# ---------------------------------------------------------------------------
# Mapping definition tests
# ---------------------------------------------------------------------------


class TestClusterMappingDefinition:
    """Tests for CLUSTER_MAPPING structure."""

    def test_all_cache_attrs_exist_on_model(self) -> None:
        """Every cache_attr in the mapping is a valid ClusterInfo field."""
        model_fields = set(ClusterInfo.model_fields.keys())
        for field in CLUSTER_MAPPING.fields:
            assert field.cache_attr in model_fields, (
                f"cache_attr '{field.cache_attr}' not on ClusterInfo"
            )

    def test_no_duplicate_cache_attrs(self) -> None:
        """No duplicate cache_attr values."""
        attrs = [f.cache_attr for f in CLUSTER_MAPPING.fields]
        assert len(attrs) == len(set(attrs))

    def test_field_count(self) -> None:
        """Mapping has expected number of fields (18)."""
        assert len(CLUSTER_MAPPING.fields) == 18

    def test_model_class(self) -> None:
        """Model class is ClusterInfo."""
        assert CLUSTER_MAPPING.model_class is ClusterInfo

    def test_endpoint(self) -> None:
        """API endpoint is /cluster?fields=*."""
        assert CLUSTER_MAPPING.api_endpoint == "/cluster?fields=*"

    def test_cli_command_empty(self) -> None:
        """CLI command is empty (API-only)."""
        assert CLUSTER_MAPPING.cli_command == ""

    def test_id_field(self) -> None:
        """ID field is name."""
        assert CLUSTER_MAPPING.id_field == "name"

    def test_api_expected_fields(self) -> None:
        """api_expected_fields returns correct top-level keys."""
        expected = CLUSTER_MAPPING.api_expected_fields()
        assert expected == sorted(
            [
                "auto_enable_activity_tracking",
                "auto_enable_analytics",
                "contact",
                "disaggregated",
                "dns_domains",
                "location",
                "management_interfaces",
                "name",
                "name_servers",
                "ntp_servers",
                "peering_policy",
                "san_optimized",
                "timezone",
                "uuid",
                "version",
            ]
        )


# ---------------------------------------------------------------------------
# API parsing tests
# ---------------------------------------------------------------------------


class TestClusterApiParsing:
    """Tests for parsing API cluster records."""

    def test_full_record(self, full_api_record: dict[str, Any]) -> None:
        """Full API record parses to complete ClusterInfo."""
        result = parse_api_record(CLUSTER_MAPPING, full_api_record, "[test]")
        assert isinstance(result, ClusterInfo)
        assert result.cluster_name == "mycluster"
        assert result.cluster_uuid == "abc-123-def-456"
        assert result.ontap_version == "NetApp Release 9.14.1"
        assert result.model == "SIMULATED"
        assert result.contact == "admin@example.com"
        assert result.location == "datacenter-1"
        assert result.san_optimized is True
        assert result.timezone == "America/New_York"
        assert result.dns_domains == ["example.com", "corp.example.com"]
        assert result.name_servers == ["10.0.0.1", "10.0.0.2"]
        assert result.ntp_servers == ["time.nist.gov", "pool.ntp.org"]
        assert result.peering_policy_authentication_required is True
        assert result.peering_policy_encryption_required is True
        assert result.peering_policy_minimum_passphrase_length == 8
        assert result.management_interface_uuids == ["mgmt-uuid-1", "mgmt-uuid-2"]
        assert result.disaggregated is True
        assert result.auto_enable_activity_tracking is True
        assert result.auto_enable_analytics is True

    def test_minimal_record(self) -> None:
        """Minimal record uses defaults for missing fields."""
        record: dict[str, Any] = {"name": "minimal", "uuid": "xyz"}
        result = parse_api_record(CLUSTER_MAPPING, record, "[test]")
        assert isinstance(result, ClusterInfo)
        assert result.cluster_name == "minimal"
        assert result.cluster_uuid == "xyz"
        assert result.ontap_version == ""
        assert result.model == ""
        assert result.contact == ""
        assert result.location == ""
        assert result.san_optimized is False
        assert result.timezone == ""
        assert result.dns_domains == []
        assert result.name_servers == []
        assert result.ntp_servers == []
        assert result.peering_policy_authentication_required is False
        assert result.peering_policy_encryption_required is False
        assert result.peering_policy_minimum_passphrase_length == 0
        assert result.management_interface_uuids == []
        assert result.disaggregated is False
        assert result.auto_enable_activity_tracking is False
        assert result.auto_enable_analytics is False

    def test_empty_record(self) -> None:
        """Empty record uses all defaults."""
        record: dict[str, Any] = {}
        result = parse_api_record(CLUSTER_MAPPING, record, "[test]")
        assert isinstance(result, ClusterInfo)
        assert result.cluster_name == ""
        assert result.cluster_uuid == ""
        assert result.ontap_version == ""
        assert result.model == ""

    def test_nested_version_fields(self) -> None:
        """Nested version.full and version.generation parse correctly."""
        record: dict[str, Any] = {
            "name": "test",
            "version": {"full": "9.15.0", "generation": 9},
        }
        result = parse_api_record(CLUSTER_MAPPING, record, "[test]")
        assert isinstance(result, ClusterInfo)
        assert result.ontap_version == "9.15.0"
        # model field_validator coerces int to str
        assert result.model == "9"

    def test_nested_timezone_field(self) -> None:
        """Nested timezone.name parses correctly."""
        record: dict[str, Any] = {
            "name": "test",
            "timezone": {"name": "UTC"},
        }
        result = parse_api_record(CLUSTER_MAPPING, record, "[test]")
        assert isinstance(result, ClusterInfo)
        assert result.timezone == "UTC"

    def test_nested_peering_policy_fields(self) -> None:
        """Nested peering_policy.* fields parse correctly."""
        record: dict[str, Any] = {
            "name": "test",
            "peering_policy": {
                "authentication_required": True,
                "encryption_required": False,
                "minimum_passphrase_length": 12,
            },
        }
        result = parse_api_record(CLUSTER_MAPPING, record, "[test]")
        assert isinstance(result, ClusterInfo)
        assert result.peering_policy_authentication_required is True
        assert result.peering_policy_encryption_required is False
        assert result.peering_policy_minimum_passphrase_length == 12

    def test_wildcard_management_interfaces(self) -> None:
        """Wildcard management_interfaces[*].uuid parses correctly."""
        record: dict[str, Any] = {
            "name": "test",
            "management_interfaces": [
                {"uuid": "uuid-1", "name": "mgmt1"},
                {"uuid": "uuid-2", "name": "mgmt2"},
                {"uuid": "uuid-3", "name": "mgmt3"},
            ],
        }
        result = parse_api_record(CLUSTER_MAPPING, record, "[test]")
        assert isinstance(result, ClusterInfo)
        assert result.management_interface_uuids == ["uuid-1", "uuid-2", "uuid-3"]

    def test_wildcard_empty_management_interfaces(self) -> None:
        """Empty management_interfaces list returns default."""
        record: dict[str, Any] = {
            "name": "test",
            "management_interfaces": [],
        }
        result = parse_api_record(CLUSTER_MAPPING, record, "[test]")
        assert isinstance(result, ClusterInfo)
        assert result.management_interface_uuids == []

    def test_missing_management_interfaces_uses_default(self) -> None:
        """Missing management_interfaces key uses default empty list."""
        record: dict[str, Any] = {"name": "test"}
        result = parse_api_record(CLUSTER_MAPPING, record, "[test]")
        assert isinstance(result, ClusterInfo)
        assert result.management_interface_uuids == []

    def test_list_fields(self) -> None:
        """Top-level list fields (dns_domains, name_servers, ntp_servers) parse correctly."""
        record: dict[str, Any] = {
            "name": "test",
            "dns_domains": ["a.com", "b.com"],
            "name_servers": ["1.1.1.1"],
            "ntp_servers": ["ntp1", "ntp2", "ntp3"],
        }
        result = parse_api_record(CLUSTER_MAPPING, record, "[test]")
        assert isinstance(result, ClusterInfo)
        assert result.dns_domains == ["a.com", "b.com"]
        assert result.name_servers == ["1.1.1.1"]
        assert result.ntp_servers == ["ntp1", "ntp2", "ntp3"]

    def test_is_ha_not_set_by_mapping(self) -> None:
        """is_ha is not set by the mapping (derived post-collection)."""
        record: dict[str, Any] = {"name": "test"}
        result = parse_api_record(CLUSTER_MAPPING, record, "[test]")
        assert isinstance(result, ClusterInfo)
        assert result.is_ha is False


# ---------------------------------------------------------------------------
# Parity test: old parser vs new framework
# ---------------------------------------------------------------------------


class TestParityWithOldParser:
    """Verify framework produces same output as old hand-written parser.

    Reproduces the manual .get() logic from the collector to confirm the
    declarative mapping produces identical results for the original 6 fields.
    """

    @staticmethod
    def _old_parse_cluster(record: dict[str, Any]) -> ClusterInfo:
        """Reproduce old inline cluster parsing logic."""
        return ClusterInfo(
            cluster_name=record.get("name", ""),
            cluster_uuid=record.get("uuid", ""),
            ontap_version=record.get("version", {}).get("full", ""),
            model=record.get("version", {}).get("generation", ""),
            contact=record.get("contact", ""),
            location=record.get("location", ""),
        )

    _ORIGINAL_FIELDS = (
        "cluster_name",
        "cluster_uuid",
        "ontap_version",
        "model",
        "contact",
        "location",
    )

    def test_parity_full_record(self, full_api_record: dict[str, Any]) -> None:
        """Framework and old parser produce identical ClusterInfo for full record."""
        old = self._old_parse_cluster(full_api_record)
        new = parse_api_record(CLUSTER_MAPPING, full_api_record, "[test]")
        assert isinstance(new, ClusterInfo)
        for field_name in self._ORIGINAL_FIELDS:
            old_val = getattr(old, field_name)
            new_val = getattr(new, field_name)
            assert old_val == new_val, (
                f"Field '{field_name}' differs: old={old_val!r}, new={new_val!r}"
            )

    def test_parity_minimal_record(self) -> None:
        """Framework and old parser match on minimal record."""
        record: dict[str, Any] = {"name": "test", "uuid": "xyz"}
        old = self._old_parse_cluster(record)
        new = parse_api_record(CLUSTER_MAPPING, record, "[test]")
        assert isinstance(new, ClusterInfo)
        for field_name in self._ORIGINAL_FIELDS:
            old_val = getattr(old, field_name)
            new_val = getattr(new, field_name)
            assert old_val == new_val, (
                f"Field '{field_name}' differs: old={old_val!r}, new={new_val!r}"
            )

    def test_parity_empty_record(self) -> None:
        """Framework and old parser match on empty record."""
        record: dict[str, Any] = {}
        old = self._old_parse_cluster(record)
        new = parse_api_record(CLUSTER_MAPPING, record, "[test]")
        assert isinstance(new, ClusterInfo)
        for field_name in self._ORIGINAL_FIELDS:
            old_val = getattr(old, field_name)
            new_val = getattr(new, field_name)
            assert old_val == new_val, (
                f"Field '{field_name}' differs: old={old_val!r}, new={new_val!r}"
            )
