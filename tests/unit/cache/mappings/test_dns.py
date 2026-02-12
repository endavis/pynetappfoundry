"""Tests for the DNS type mapping definition."""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock

import pytest

from pynetappfoundry.cache.field_mapping import (
    parse_api_record,
    parse_api_response,
)
from pynetappfoundry.cache.name_services.dns.mapping import DNS_MAPPING
from pynetappfoundry.cache.name_services.dns.model import DNSInfo

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def full_api_record() -> dict[str, Any]:
    """Full API DNS record with all fields populated."""
    return {
        "uuid": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
        "svm": {"name": "svm1", "uuid": "svm-uuid-1"},
        "scope": "svm",
        "domains": ["example.com", "test.local"],
        "servers": ["10.0.0.1", "10.0.0.2"],
        "timeout": 2,
        "attempts": 1,
        "dynamic_dns": {
            "enabled": True,
            "fqdn": "host1.example.com",
            "time_to_live": "24h",
            "use_secure": True,
        },
        "packet_query_match": False,
        "source_address_match": False,
        "tld_query_enabled": False,
        "service_ips": ["10.0.0.100", "10.0.0.101"],
    }


# ---------------------------------------------------------------------------
# Mapping definition tests
# ---------------------------------------------------------------------------


class TestDnsMappingDefinition:
    """Tests for DNS_MAPPING structure."""

    def test_all_cache_attrs_exist_on_model(self) -> None:
        """Every cache_attr in the mapping is a valid DNSInfo field."""
        model_fields = set(DNSInfo.model_fields.keys())
        for field in DNS_MAPPING.fields:
            assert field.cache_attr in model_fields, (
                f"cache_attr '{field.cache_attr}' not on DNSInfo"
            )

    def test_no_duplicate_cache_attrs(self) -> None:
        """No duplicate cache_attr values."""
        attrs = [f.cache_attr for f in DNS_MAPPING.fields]
        assert len(attrs) == len(set(attrs))

    def test_field_count(self) -> None:
        """Mapping has expected number of fields (15)."""
        assert len(DNS_MAPPING.fields) == 15

    def test_model_class(self) -> None:
        """Model class is DNSInfo."""
        assert DNS_MAPPING.model_class is DNSInfo

    def test_endpoint(self) -> None:
        """API endpoint is correct."""
        assert DNS_MAPPING.api_endpoint == (
            "/name-services/dns?fields=*,tld_query_enabled,source_address_match,packet_query_match"
        )

    def test_cli_command_empty(self) -> None:
        """CLI command is empty (API-only type)."""
        assert DNS_MAPPING.cli_command == ""

    def test_api_expected_fields(self) -> None:
        """api_expected_fields returns correct top-level keys."""
        expected = DNS_MAPPING.api_expected_fields()
        assert expected == [
            "attempts",
            "domains",
            "dynamic_dns",
            "packet_query_match",
            "scope",
            "servers",
            "service_ips",
            "source_address_match",
            "svm",
            "timeout",
            "tld_query_enabled",
            "uuid",
        ]

    def test_id_field(self) -> None:
        """id_field is name (default)."""
        assert DNS_MAPPING.id_field == "name"


# ---------------------------------------------------------------------------
# API parsing tests
# ---------------------------------------------------------------------------


class TestDnsApiParsing:
    """Tests for parsing API DNS records."""

    def test_full_record(self, full_api_record: dict[str, Any]) -> None:
        """Full API record parses correctly."""
        result = parse_api_record(DNS_MAPPING, full_api_record, "[test]")
        assert isinstance(result, DNSInfo)
        assert result.uuid == "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
        assert result.svm_uuid == "svm-uuid-1"
        assert result.scope == "svm"
        assert result.domains == ["example.com", "test.local"]
        assert result.servers == ["10.0.0.1", "10.0.0.2"]
        assert result.timeout == 2
        assert result.attempts == 1
        assert result.dynamic_dns_enabled is True
        assert result.dynamic_dns_fqdn == "host1.example.com"
        assert result.dynamic_dns_time_to_live == "24h"
        assert result.dynamic_dns_use_secure is True
        assert result.packet_query_match is False
        assert result.source_address_match is False
        assert result.tld_query_enabled is False
        assert result.service_ips == ["10.0.0.100", "10.0.0.101"]

    def test_minimal_record(self) -> None:
        """Minimal record uses defaults for missing fields."""
        record: dict[str, Any] = {"uuid": "abc", "scope": "cluster"}
        result = parse_api_record(DNS_MAPPING, record, "[test]")
        assert isinstance(result, DNSInfo)
        assert result.uuid == "abc"
        assert result.svm_uuid == ""
        assert result.scope == "cluster"
        assert result.domains == []
        assert result.servers == []
        assert result.timeout == 0
        assert result.attempts == 0
        assert result.dynamic_dns_enabled is False
        assert result.dynamic_dns_fqdn == ""
        assert result.dynamic_dns_time_to_live == ""
        assert result.dynamic_dns_use_secure is False
        assert result.packet_query_match is True
        assert result.source_address_match is True
        assert result.tld_query_enabled is True
        assert result.service_ips == []

    def test_missing_nested_dynamic_dns(self) -> None:
        """Record without dynamic_dns uses defaults."""
        record: dict[str, Any] = {
            "uuid": "abc",
            "svm": {"name": "svm1", "uuid": "svm-uuid-1"},
            "scope": "svm",
            "domains": ["example.com"],
            "servers": ["10.0.0.1"],
            "timeout": 2,
            "attempts": 1,
        }
        result = parse_api_record(DNS_MAPPING, record, "[test]")
        assert isinstance(result, DNSInfo)
        assert result.svm_uuid == "svm-uuid-1"
        assert result.dynamic_dns_enabled is False
        assert result.dynamic_dns_fqdn == ""
        assert result.dynamic_dns_time_to_live == ""
        assert result.dynamic_dns_use_secure is False

    def test_parse_api_response_multiple(self) -> None:
        """parse_api_response handles multiple records."""
        response = {
            "records": [
                {
                    "uuid": "dns-1",
                    "svm": {"name": "svm1", "uuid": "svm-uuid-1"},
                    "scope": "svm",
                    "domains": ["example.com"],
                    "servers": ["10.0.0.1"],
                    "timeout": 2,
                    "attempts": 1,
                },
                {
                    "uuid": "dns-2",
                    "svm": {"name": "svm2", "uuid": "svm-uuid-2"},
                    "scope": "svm",
                    "domains": ["test.local"],
                    "servers": ["10.0.0.2"],
                    "timeout": 3,
                    "attempts": 2,
                },
            ],
        }
        results = parse_api_response(DNS_MAPPING, response, "[test]", MagicMock())
        assert len(results) == 2
        assert results[0].uuid == "dns-1"  # type: ignore[union-attr]
        assert results[1].uuid == "dns-2"  # type: ignore[union-attr]

    def test_parse_api_response_empty(self) -> None:
        """parse_api_response handles empty/None response."""
        assert parse_api_response(DNS_MAPPING, None, "[test]", MagicMock()) == []
        assert parse_api_response(DNS_MAPPING, {}, "[test]", MagicMock()) == []

    def test_missing_svm_uuid(self) -> None:
        """Record without svm field defaults svm_uuid to empty string."""
        record: dict[str, Any] = {"uuid": "abc", "scope": "cluster"}
        result = parse_api_record(DNS_MAPPING, record, "[test]")
        assert isinstance(result, DNSInfo)
        assert result.svm_uuid == ""

    def test_service_ips_missing_for_older_ontap(self) -> None:
        """service_ips defaults to empty list when not present (pre-9.14)."""
        record: dict[str, Any] = {
            "uuid": "abc",
            "svm": {"name": "svm1", "uuid": "svm-uuid-1"},
            "scope": "svm",
        }
        result = parse_api_record(DNS_MAPPING, record, "[test]")
        assert isinstance(result, DNSInfo)
        assert result.service_ips == []


# ---------------------------------------------------------------------------
# Parity test: old parser vs new framework
# ---------------------------------------------------------------------------


class TestParityWithOldParser:
    """Verify framework produces same output as old hand-written inline parser.

    Parity is checked for the original 7 fields only. The new fields
    were not in the old parser. The old parser extracted ``svm.name``;
    the new mapping extracts ``svm.uuid``, so parity compares the
    remaining 6 shared fields.
    """

    _ORIGINAL_SHARED_FIELDS = (
        "uuid",
        "scope",
        "domains",
        "servers",
        "timeout",
        "attempts",
    )

    @staticmethod
    def _old_parse_dns(record: dict[str, Any]) -> DNSInfo:
        """Reproduce old inline DNS parsing logic from collector.

        This is a static copy of the code that was in
        ``_parse_dns_response`` before migration, adapted to the
        new model field names where applicable.
        """
        return DNSInfo(
            uuid=record.get("uuid", ""),
            svm_uuid=record.get("svm", {}).get("name", "") if record.get("svm") else "",
            scope=record.get("scope", ""),
            domains=record.get("domains", []) or [],
            servers=record.get("servers", []) or [],
            timeout=record.get("timeout", 0),
            attempts=record.get("attempts", 0),
        )

    def test_parity_full_record(self, full_api_record: dict[str, Any]) -> None:
        """Framework and old parser produce identical results for shared fields."""
        old = self._old_parse_dns(full_api_record)
        new = parse_api_record(DNS_MAPPING, full_api_record, "[test]")
        assert isinstance(new, DNSInfo)
        for field_name in self._ORIGINAL_SHARED_FIELDS:
            old_val = getattr(old, field_name)
            new_val = getattr(new, field_name)
            assert old_val == new_val, (
                f"Field '{field_name}' differs: old={old_val!r}, new={new_val!r}"
            )

    def test_parity_minimal_record(self) -> None:
        """Framework and old parser match on minimal record."""
        record: dict[str, Any] = {"uuid": "dns-1"}
        old = self._old_parse_dns(record)
        new = parse_api_record(DNS_MAPPING, record, "[test]")
        assert isinstance(new, DNSInfo)
        for field_name in self._ORIGINAL_SHARED_FIELDS:
            old_val = getattr(old, field_name)
            new_val = getattr(new, field_name)
            assert old_val == new_val, (
                f"Field '{field_name}' differs: old={old_val!r}, new={new_val!r}"
            )

    def test_parity_svm_name_vs_uuid(self, full_api_record: dict[str, Any]) -> None:
        """Old parser used svm.name; new mapping uses svm.uuid."""
        old = self._old_parse_dns(full_api_record)
        new = parse_api_record(DNS_MAPPING, full_api_record, "[test]")
        assert isinstance(new, DNSInfo)
        # Old parser stored svm name in svm_uuid (adapted field)
        assert old.svm_uuid == "svm1"
        # New mapping stores svm uuid
        assert new.svm_uuid == "svm-uuid-1"

    def test_parity_no_svm(self) -> None:
        """Both parsers handle missing svm field."""
        record: dict[str, Any] = {
            "uuid": "dns-1",
            "scope": "cluster",
            "domains": ["example.com"],
            "servers": ["10.0.0.1"],
            "timeout": 2,
            "attempts": 1,
        }
        old = self._old_parse_dns(record)
        new = parse_api_record(DNS_MAPPING, record, "[test]")
        assert isinstance(new, DNSInfo)
        for field_name in self._ORIGINAL_SHARED_FIELDS:
            old_val = getattr(old, field_name)
            new_val = getattr(new, field_name)
            assert old_val == new_val, (
                f"Field '{field_name}' differs: old={old_val!r}, new={new_val!r}"
            )
        # Both default svm_uuid to empty string when svm missing
        assert old.svm_uuid == ""
        assert new.svm_uuid == ""
