"""Tests for the LicensePackage type mapping definition."""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock

import pytest

from pynetappfoundry.cache.cluster.licensing.mapping import (
    LICENSE_PACKAGE_MAPPING,
    _api_instances,
)
from pynetappfoundry.cache.cluster.licensing.model import LicenseInstance, LicensePackage
from pynetappfoundry.cache.field_mapping import (
    parse_api_record,
    parse_api_response,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def full_api_record() -> dict[str, Any]:
    """Full API license package record with all fields populated."""
    return {
        "name": "nfs",
        "scope": "cluster",
        "state": "compliant",
        "description": "NFS License",
        "entitlement": {
            "action": "acquire_license",
            "risk": "medium",
        },
        "licenses": [
            {
                "active": True,
                "capacity": {"maximum_size": 109951162777600},
                "compliance": {"state": "compliant"},
                "evaluation": False,
                "expiry_time": "2025-12-31T23:59:59+00:00",
                "host_id": "4082368507",
                "installed_license": "Enterprise",
                "owner": "node1",
                "serial_number": "1-23-456789",
                "shutdown_imminent": False,
                "start_time": "2024-01-01T00:00:00+00:00",
            },
            {
                "active": True,
                "capacity": {"maximum_size": 109951162777600},
                "compliance": {"state": "compliant"},
                "evaluation": False,
                "host_id": "4082368508",
                "installed_license": "Enterprise",
                "owner": "node2",
                "serial_number": "1-23-456790",
                "shutdown_imminent": False,
            },
        ],
    }


# ---------------------------------------------------------------------------
# Mapping definition tests
# ---------------------------------------------------------------------------


class TestLicensePackageMappingDefinition:
    """Tests for LICENSE_PACKAGE_MAPPING structure."""

    def test_all_cache_attrs_exist_on_model(self) -> None:
        """Every cache_attr in the mapping is a valid LicensePackage field."""
        model_fields = set(LicensePackage.model_fields.keys())
        for field in LICENSE_PACKAGE_MAPPING.fields:
            assert field.cache_attr in model_fields, (
                f"cache_attr '{field.cache_attr}' not on LicensePackage"
            )

    def test_no_duplicate_cache_attrs(self) -> None:
        """No duplicate cache_attr values."""
        attrs = [f.cache_attr for f in LICENSE_PACKAGE_MAPPING.fields]
        assert len(attrs) == len(set(attrs))

    def test_field_count(self) -> None:
        """Mapping has expected number of fields (7)."""
        assert len(LICENSE_PACKAGE_MAPPING.fields) == 7

    def test_model_class(self) -> None:
        """Model class is LicensePackage."""
        assert LICENSE_PACKAGE_MAPPING.model_class is LicensePackage

    def test_endpoint(self) -> None:
        """API endpoint is correct."""
        assert LICENSE_PACKAGE_MAPPING.api_endpoint == (
            "/cluster/licensing/licenses?fields=name,scope,state,description,entitlement,licenses"
        )

    def test_cli_command_empty(self) -> None:
        """CLI command is empty (API-only type)."""
        assert LICENSE_PACKAGE_MAPPING.cli_command == ""

    def test_api_expected_fields(self) -> None:
        """api_expected_fields returns correct top-level keys."""
        expected = LICENSE_PACKAGE_MAPPING.api_expected_fields()
        assert expected == [
            "description",
            "entitlement",
            "name",
            "scope",
            "state",
        ]

    def test_id_field(self) -> None:
        """id_field is name (default)."""
        assert LICENSE_PACKAGE_MAPPING.id_field == "name"

    def test_all_model_fields_have_mapping(self) -> None:
        """Every LicensePackage model field has a corresponding mapping entry."""
        mapped_attrs = {f.cache_attr for f in LICENSE_PACKAGE_MAPPING.fields}
        model_fields = set(LicensePackage.model_fields.keys())
        unmapped = model_fields - mapped_attrs
        assert not unmapped, f"Model fields without mapping: {unmapped}"


# ---------------------------------------------------------------------------
# API parsing tests
# ---------------------------------------------------------------------------


class TestLicensePackageApiParsing:
    """Tests for parsing API license package records."""

    def test_full_record(self, full_api_record: dict[str, Any]) -> None:
        """Full API record parses correctly."""
        result = parse_api_record(LICENSE_PACKAGE_MAPPING, full_api_record, "[test]")
        assert isinstance(result, LicensePackage)

        assert result.name == "nfs"
        assert result.scope == "cluster"
        assert result.state == "compliant"
        assert result.description == "NFS License"
        assert result.entitlement_action == "acquire_license"
        assert result.entitlement_risk == "medium"
        assert len(result.instances) == 2

        inst = result.instances[0]
        assert inst.active is True
        assert inst.capacity_max == 109951162777600
        assert inst.compliance_state == "compliant"
        assert inst.evaluation is False
        assert inst.expiry_time == "2025-12-31T23:59:59+00:00"
        assert inst.host_id == "4082368507"
        assert inst.installed_license == "Enterprise"
        assert inst.owner == "node1"
        assert inst.serial_number == "1-23-456789"
        assert inst.shutdown_imminent is False
        assert inst.start_time == "2024-01-01T00:00:00+00:00"

    def test_minimal_record(self) -> None:
        """Minimal record uses defaults for missing fields."""
        record: dict[str, Any] = {"name": "cifs", "state": "compliant"}
        result = parse_api_record(LICENSE_PACKAGE_MAPPING, record, "[test]")
        assert isinstance(result, LicensePackage)
        assert result.name == "cifs"
        assert result.state == "compliant"
        assert result.scope == ""
        assert result.description == ""
        assert result.entitlement_action == ""
        assert result.entitlement_risk == ""
        assert result.instances == []

    def test_missing_fields(self) -> None:
        """Record with only name returns defaults for other fields."""
        record: dict[str, Any] = {"name": "iscsi"}
        result = parse_api_record(LICENSE_PACKAGE_MAPPING, record, "[test]")
        assert isinstance(result, LicensePackage)
        assert result.name == "iscsi"
        assert result.scope == ""
        assert result.state == ""
        assert result.instances == []

    def test_empty_instances(self) -> None:
        """Record with empty licenses array produces empty instances."""
        record: dict[str, Any] = {
            "name": "nfs",
            "state": "compliant",
            "licenses": [],
        }
        result = parse_api_record(LICENSE_PACKAGE_MAPPING, record, "[test]")
        assert isinstance(result, LicensePackage)
        assert result.instances == []

    def test_parse_api_response_multiple(self) -> None:
        """parse_api_response handles multiple records."""
        response = {
            "records": [
                {
                    "name": "nfs",
                    "state": "compliant",
                    "scope": "cluster",
                },
                {
                    "name": "cifs",
                    "state": "compliant",
                    "scope": "cluster",
                },
            ],
        }
        results = parse_api_response(LICENSE_PACKAGE_MAPPING, response, "[test]", MagicMock())
        assert len(results) == 2
        assert results[0].name == "nfs"  # type: ignore[union-attr]
        assert results[1].name == "cifs"  # type: ignore[union-attr]

    def test_parse_api_response_empty(self) -> None:
        """parse_api_response handles empty/None response."""
        assert parse_api_response(LICENSE_PACKAGE_MAPPING, None, "[test]", MagicMock()) == []
        assert parse_api_response(LICENSE_PACKAGE_MAPPING, {}, "[test]", MagicMock()) == []


# ---------------------------------------------------------------------------
# Transform function tests
# ---------------------------------------------------------------------------


class TestTransformFunctions:
    """Tests for the _api_instances transform function."""

    def test_full_data(self) -> None:
        """Transform with full nested data."""
        record: dict[str, Any] = {
            "name": "nfs",
            "licenses": [
                {
                    "active": True,
                    "capacity": {"maximum_size": 1024},
                    "compliance": {"state": "compliant"},
                    "evaluation": False,
                    "expiry_time": "2025-12-31T00:00:00+00:00",
                    "host_id": "12345",
                    "installed_license": "Enterprise",
                    "owner": "node1",
                    "serial_number": "SN-001",
                    "shutdown_imminent": False,
                    "start_time": "2024-01-01T00:00:00+00:00",
                },
            ],
        }
        result = _api_instances(record)
        assert len(result) == 1
        inst = result[0]
        assert isinstance(inst, LicenseInstance)
        assert inst.active is True
        assert inst.capacity_max == 1024
        assert inst.compliance_state == "compliant"
        assert inst.expiry_time == "2025-12-31T00:00:00+00:00"
        assert inst.host_id == "12345"
        assert inst.owner == "node1"

    def test_missing_capacity_and_compliance(self) -> None:
        """Transform handles missing capacity and compliance sub-objects."""
        record: dict[str, Any] = {
            "licenses": [
                {
                    "active": True,
                    "owner": "node1",
                },
            ],
        }
        result = _api_instances(record)
        assert len(result) == 1
        assert result[0].capacity_max == 0
        assert result[0].compliance_state == ""

    def test_non_dict_entries_skipped(self) -> None:
        """Transform skips non-dict entries in the licenses array."""
        record: dict[str, Any] = {
            "licenses": [
                {"active": True, "owner": "node1"},
                "not-a-dict",
                42,
                None,
            ],
        }
        result = _api_instances(record)
        assert len(result) == 1
        assert result[0].owner == "node1"

    def test_empty_licenses_array(self) -> None:
        """Transform returns empty list for empty licenses array."""
        assert _api_instances({"licenses": []}) == []

    def test_missing_licenses_key(self) -> None:
        """Transform returns empty list when licenses key is missing."""
        assert _api_instances({"name": "nfs"}) == []

    def test_licenses_not_a_list(self) -> None:
        """Transform returns empty list when licenses is not a list."""
        assert _api_instances({"licenses": "not-a-list"}) == []

    def test_null_capacity_and_compliance(self) -> None:
        """Transform handles None/null capacity and compliance gracefully."""
        record: dict[str, Any] = {
            "licenses": [
                {
                    "active": True,
                    "capacity": None,
                    "compliance": None,
                    "owner": "node1",
                },
            ],
        }
        result = _api_instances(record)
        assert len(result) == 1
        assert result[0].capacity_max == 0
        assert result[0].compliance_state == ""


# ---------------------------------------------------------------------------
# Parity test: old parser vs new framework
# ---------------------------------------------------------------------------


class TestParityWithOldParser:
    """Verify framework produces same output as old hand-written inline parser.

    Parity is checked for the original 3 package-level fields (name, state,
    scope) that were present in the old LicenseFeature model.
    """

    _ORIGINAL_SHARED_FIELDS = ("name", "state", "scope")

    @staticmethod
    def _old_parse_license(record: dict[str, Any]) -> dict[str, str]:
        """Reproduce old inline license parsing logic from collector.

        The old collector extracted name, state, and scope from each record
        and created a LicenseFeature with those three fields.
        """
        return {
            "name": record.get("name", ""),
            "state": record.get("state", ""),
            "scope": record.get("scope", ""),
        }

    def test_parity_full_record(self, full_api_record: dict[str, Any]) -> None:
        """Framework and old parser produce identical results for shared fields."""
        old = self._old_parse_license(full_api_record)
        new = parse_api_record(LICENSE_PACKAGE_MAPPING, full_api_record, "[test]")
        assert isinstance(new, LicensePackage)
        for field_name in self._ORIGINAL_SHARED_FIELDS:
            old_val = old[field_name]
            new_val = getattr(new, field_name)
            assert old_val == new_val, (
                f"Field '{field_name}' differs: old={old_val!r}, new={new_val!r}"
            )

    def test_parity_minimal_record(self) -> None:
        """Framework and old parser match on minimal record."""
        record: dict[str, Any] = {"name": "nfs"}
        old = self._old_parse_license(record)
        new = parse_api_record(LICENSE_PACKAGE_MAPPING, record, "[test]")
        assert isinstance(new, LicensePackage)
        for field_name in self._ORIGINAL_SHARED_FIELDS:
            old_val = old[field_name]
            new_val = getattr(new, field_name)
            assert old_val == new_val, (
                f"Field '{field_name}' differs: old={old_val!r}, new={new_val!r}"
            )
