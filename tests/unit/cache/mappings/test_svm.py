"""Tests for the SVM type mapping definition."""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock

import pytest

from pynetappfoundry.cache.field_mapping import (
    parse_api_record,
    parse_api_response,
)
from pynetappfoundry.cache.svm.mapping import SVM_MAPPING
from pynetappfoundry.cache.svm.model import SVMInfo

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def full_api_record() -> dict[str, Any]:
    """Full API SVM record with all fields populated."""
    return {
        "uuid": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
        "name": "svm1",
        "language": "en_us.utf_8",
        "subtype": "default",
        "aggregates": [
            {"uuid": "aggr-uuid-1"},
            {"uuid": "aggr-uuid-2"},
        ],
        "ip_interfaces": [
            {"uuid": "lif-uuid-1"},
            {"uuid": "lif-uuid-2"},
        ],
        "fc_interfaces": [
            {"uuid": "fc-uuid-1"},
        ],
        "snapshot_policy": {"uuid": "snap-policy-uuid-1"},
        "nis": {"enabled": True},
        "ldap": {"enabled": True},
        "nfs": {"enabled": True, "allowed": True},
        "cifs": {"enabled": True, "allowed": True},
        "iscsi": {"enabled": True, "allowed": True},
        "fcp": {"enabled": True, "allowed": True},
        "nvme": {"enabled": True, "allowed": True},
        "ndmp": {"allowed": False},
        "s3": {"allowed": False, "enabled": True},
        "aggregates_delegated": True,
        "max_volumes": "500",
        "auto_enable_analytics": True,
        "auto_enable_activity_tracking": True,
        "anti_ransomware_auto_switch_from_learning_to_enabled": False,
        "anti_ransomware_auto_switch_minimum_incoming_data_percent": 25,
        "anti_ransomware_auto_switch_duration_without_new_file_extension": 5,
        "anti_ransomware_auto_switch_minimum_learning_period": 14,
        "anti_ransomware_auto_switch_minimum_file_count": 500,
        "anti_ransomware_auto_switch_minimum_file_extension": 20,
        "snapmirror": {
            "is_protected": True,
            "protected_volumes_count": 3,
        },
        "storage": {"limit": 1099511627776},
        "is_space_enforcement_logical": True,
        "is_space_reporting_logical": True,
        "qos_adaptive_policy_group_template": {"uuid": "qos-adaptive-uuid-1"},
        "qos_policy": {"uuid": "qos-policy-uuid-1"},
        "qos_policy_group_template": {"uuid": "qos-group-uuid-1"},
        "nsswitch": {
            "group": ["files", "ldap"],
            "hosts": ["files", "dns"],
            "namemap": ["files"],
            "netgroup": ["files", "ldap"],
            "passwd": ["files", "ldap"],
        },
    }


# ---------------------------------------------------------------------------
# Mapping definition tests
# ---------------------------------------------------------------------------


class TestSvmMappingDefinition:
    """Tests for SVM_MAPPING structure."""

    def test_all_cache_attrs_exist_on_model(self) -> None:
        """Every cache_attr in the mapping is a valid SVMInfo field."""
        model_fields = set(SVMInfo.model_fields.keys())
        for field in SVM_MAPPING.fields:
            assert field.cache_attr in model_fields, (
                f"cache_attr '{field.cache_attr}' not on SVMInfo"
            )

    def test_no_duplicate_cache_attrs(self) -> None:
        """No duplicate cache_attr values."""
        attrs = [f.cache_attr for f in SVM_MAPPING.fields]
        assert len(attrs) == len(set(attrs))

    def test_field_count(self) -> None:
        """Mapping has expected number of fields (46)."""
        assert len(SVM_MAPPING.fields) == 46

    def test_model_field_count(self) -> None:
        """SVMInfo model has expected number of fields (46)."""
        assert len(SVMInfo.model_fields) == 46

    def test_model_class(self) -> None:
        """Model class is SVMInfo."""
        assert SVM_MAPPING.model_class is SVMInfo

    def test_endpoint(self) -> None:
        """API endpoint is correct with snapmirror expansion."""
        assert SVM_MAPPING.api_endpoint == "/svm/svms?fields=*,snapmirror"

    def test_cli_command_empty(self) -> None:
        """CLI command is empty (API-only type)."""
        assert SVM_MAPPING.cli_command == ""

    def test_id_field(self) -> None:
        """id_field is name (default)."""
        assert SVM_MAPPING.id_field == "name"

    def test_api_expected_fields(self) -> None:
        """api_expected_fields returns correct top-level keys."""
        expected = SVM_MAPPING.api_expected_fields()
        assert expected == [
            "aggregates",
            "aggregates_delegated",
            "anti_ransomware_auto_switch_duration_without_new_file_extension",
            "anti_ransomware_auto_switch_from_learning_to_enabled",
            "anti_ransomware_auto_switch_minimum_file_count",
            "anti_ransomware_auto_switch_minimum_file_extension",
            "anti_ransomware_auto_switch_minimum_incoming_data_percent",
            "anti_ransomware_auto_switch_minimum_learning_period",
            "auto_enable_activity_tracking",
            "auto_enable_analytics",
            "cifs",
            "fc_interfaces",
            "fcp",
            "ip_interfaces",
            "is_space_enforcement_logical",
            "is_space_reporting_logical",
            "iscsi",
            "language",
            "ldap",
            "max_volumes",
            "name",
            "ndmp",
            "nfs",
            "nis",
            "nsswitch",
            "nvme",
            "qos_adaptive_policy_group_template",
            "qos_policy",
            "qos_policy_group_template",
            "s3",
            "snapmirror",
            "snapshot_policy",
            "storage",
            "subtype",
            "uuid",
        ]

    def test_all_model_fields_have_mapping(self) -> None:
        """Every SVMInfo model field has a corresponding mapping entry."""
        mapped_attrs = {f.cache_attr for f in SVM_MAPPING.fields}
        model_fields = set(SVMInfo.model_fields.keys())
        unmapped = model_fields - mapped_attrs
        assert not unmapped, f"Model fields without mapping: {unmapped}"


# ---------------------------------------------------------------------------
# API parsing tests
# ---------------------------------------------------------------------------


class TestSvmApiParsing:
    """Tests for parsing API SVM records."""

    def test_full_record(self, full_api_record: dict[str, Any]) -> None:
        """Full API record parses correctly."""
        result = parse_api_record(SVM_MAPPING, full_api_record, "[test]")
        assert isinstance(result, SVMInfo)

        # Core
        assert result.uuid == "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
        assert result.name == "svm1"
        assert result.language == "en_us.utf_8"
        assert result.subtype == "default"

        # References / Lists
        assert result.aggregate_uuids == ["aggr-uuid-1", "aggr-uuid-2"]
        assert result.ip_interface_uuids == ["lif-uuid-1", "lif-uuid-2"]
        assert result.fc_interface_uuids == ["fc-uuid-1"]
        assert result.snapshot_policy_uuid == "snap-policy-uuid-1"

        # Name Services
        assert result.nis_enabled is True
        assert result.ldap_enabled is True

        # Protocol Flags
        assert result.nfs_enabled is True
        assert result.nfs_allowed is True
        assert result.cifs_enabled is True
        assert result.cifs_allowed is True
        assert result.iscsi_enabled is True
        assert result.iscsi_allowed is True
        assert result.fcp_enabled is True
        assert result.fcp_allowed is True
        assert result.nvme_enabled is True
        assert result.nvme_allowed is True
        assert result.ndmp_allowed is False
        assert result.s3_allowed is False
        assert result.s3_enabled is True

        # SVM Settings
        assert result.aggregates_delegated is True
        assert result.max_volumes == "500"
        assert result.auto_enable_analytics is True
        assert result.auto_enable_activity_tracking is True

        # Anti-Ransomware
        assert result.anti_ransomware_auto_switch_from_learning_to_enabled is False
        assert result.anti_ransomware_auto_switch_minimum_incoming_data_percent == 25
        assert result.anti_ransomware_auto_switch_duration_without_new_file_extension == 5
        assert result.anti_ransomware_auto_switch_minimum_learning_period == 14
        assert result.anti_ransomware_auto_switch_minimum_file_count == 500
        assert result.anti_ransomware_auto_switch_minimum_file_extension == 20

        # SnapMirror
        assert result.snapmirror_is_protected is True
        assert result.snapmirror_protected_volumes_count == 3

        # Storage
        assert result.storage_limit == 1099511627776

        # Space Management
        assert result.is_space_enforcement_logical is True
        assert result.is_space_reporting_logical is True

        # QoS References
        assert result.qos_adaptive_policy_group_template_uuid == "qos-adaptive-uuid-1"
        assert result.qos_policy_uuid == "qos-policy-uuid-1"
        assert result.qos_policy_group_template_uuid == "qos-group-uuid-1"

        # NSSwitch
        assert result.nsswitch_group == ["files", "ldap"]
        assert result.nsswitch_hosts == ["files", "dns"]
        assert result.nsswitch_namemap == ["files"]
        assert result.nsswitch_netgroup == ["files", "ldap"]
        assert result.nsswitch_passwd == ["files", "ldap"]

    def test_minimal_record(self) -> None:
        """Minimal record uses defaults for missing fields."""
        record: dict[str, Any] = {"uuid": "abc", "name": "svm-min"}
        result = parse_api_record(SVM_MAPPING, record, "[test]")
        assert isinstance(result, SVMInfo)
        assert result.uuid == "abc"
        assert result.name == "svm-min"
        assert result.language == ""
        assert result.subtype == ""

        # Lists default to empty
        assert result.aggregate_uuids == []
        assert result.ip_interface_uuids == []
        assert result.fc_interface_uuids == []
        assert result.snapshot_policy_uuid == ""

        # Name Services default to False
        assert result.nis_enabled is False
        assert result.ldap_enabled is False

        # Protocol defaults
        assert result.nfs_enabled is False
        assert result.nfs_allowed is True
        assert result.cifs_enabled is False
        assert result.cifs_allowed is True
        assert result.iscsi_enabled is False
        assert result.iscsi_allowed is True
        assert result.fcp_enabled is False
        assert result.fcp_allowed is True
        assert result.nvme_enabled is False
        assert result.nvme_allowed is True
        assert result.ndmp_allowed is True
        assert result.s3_allowed is True
        assert result.s3_enabled is False

        # SVM Settings defaults
        assert result.aggregates_delegated is False
        assert result.max_volumes == ""
        assert result.auto_enable_analytics is False
        assert result.auto_enable_activity_tracking is False

        # Anti-Ransomware defaults
        assert result.anti_ransomware_auto_switch_from_learning_to_enabled is True
        assert result.anti_ransomware_auto_switch_minimum_incoming_data_percent == 0
        assert result.anti_ransomware_auto_switch_duration_without_new_file_extension == 3
        assert result.anti_ransomware_auto_switch_minimum_learning_period == 10
        assert result.anti_ransomware_auto_switch_minimum_file_count == 200
        assert result.anti_ransomware_auto_switch_minimum_file_extension == 10

        # SnapMirror defaults
        assert result.snapmirror_is_protected is False
        assert result.snapmirror_protected_volumes_count == 0

        # Storage defaults
        assert result.storage_limit == 0

        # Space Management defaults
        assert result.is_space_enforcement_logical is False
        assert result.is_space_reporting_logical is False

        # QoS defaults
        assert result.qos_adaptive_policy_group_template_uuid == ""
        assert result.qos_policy_uuid == ""
        assert result.qos_policy_group_template_uuid == ""

        # NSSwitch defaults
        assert result.nsswitch_group == []
        assert result.nsswitch_hosts == []
        assert result.nsswitch_namemap == []
        assert result.nsswitch_netgroup == []
        assert result.nsswitch_passwd == []

    def test_missing_nested_snapmirror(self) -> None:
        """Record without snapmirror field uses defaults."""
        record: dict[str, Any] = {
            "uuid": "abc",
            "name": "svm1",
            "subtype": "default",
        }
        result = parse_api_record(SVM_MAPPING, record, "[test]")
        assert isinstance(result, SVMInfo)
        assert result.snapmirror_is_protected is False
        assert result.snapmirror_protected_volumes_count == 0

    def test_missing_nested_nsswitch(self) -> None:
        """Record without nsswitch field uses defaults."""
        record: dict[str, Any] = {
            "uuid": "abc",
            "name": "svm1",
        }
        result = parse_api_record(SVM_MAPPING, record, "[test]")
        assert isinstance(result, SVMInfo)
        assert result.nsswitch_group == []
        assert result.nsswitch_hosts == []
        assert result.nsswitch_namemap == []
        assert result.nsswitch_netgroup == []
        assert result.nsswitch_passwd == []

    def test_missing_nested_protocols(self) -> None:
        """Record without protocol sub-objects uses defaults."""
        record: dict[str, Any] = {
            "uuid": "abc",
            "name": "svm1",
        }
        result = parse_api_record(SVM_MAPPING, record, "[test]")
        assert isinstance(result, SVMInfo)
        assert result.nfs_enabled is False
        assert result.nfs_allowed is True
        assert result.cifs_enabled is False
        assert result.cifs_allowed is True
        assert result.iscsi_enabled is False
        assert result.iscsi_allowed is True
        assert result.fcp_enabled is False
        assert result.fcp_allowed is True
        assert result.nvme_enabled is False
        assert result.nvme_allowed is True
        assert result.ndmp_allowed is True
        assert result.s3_allowed is True
        assert result.s3_enabled is False

    def test_missing_qos_references(self) -> None:
        """Record without QoS fields uses defaults."""
        record: dict[str, Any] = {
            "uuid": "abc",
            "name": "svm1",
        }
        result = parse_api_record(SVM_MAPPING, record, "[test]")
        assert isinstance(result, SVMInfo)
        assert result.qos_adaptive_policy_group_template_uuid == ""
        assert result.qos_policy_uuid == ""
        assert result.qos_policy_group_template_uuid == ""

    def test_empty_aggregates_list(self) -> None:
        """Record with empty aggregates list produces empty uuid list."""
        record: dict[str, Any] = {
            "uuid": "abc",
            "name": "svm1",
            "aggregates": [],
        }
        result = parse_api_record(SVM_MAPPING, record, "[test]")
        assert isinstance(result, SVMInfo)
        assert result.aggregate_uuids == []

    def test_parse_api_response_multiple(self) -> None:
        """parse_api_response handles multiple records."""
        response = {
            "records": [
                {
                    "uuid": "svm-1",
                    "name": "svm1",
                    "subtype": "default",
                    "language": "en_us.utf_8",
                },
                {
                    "uuid": "svm-2",
                    "name": "svm2",
                    "subtype": "dp_destination",
                    "language": "c.utf_8",
                },
            ],
        }
        results = parse_api_response(SVM_MAPPING, response, "[test]", MagicMock())
        assert len(results) == 2
        assert results[0].uuid == "svm-1"  # type: ignore[union-attr]
        assert results[0].name == "svm1"  # type: ignore[union-attr]
        assert results[1].uuid == "svm-2"  # type: ignore[union-attr]
        assert results[1].name == "svm2"  # type: ignore[union-attr]

    def test_parse_api_response_empty(self) -> None:
        """parse_api_response handles empty/None response."""
        assert parse_api_response(SVM_MAPPING, None, "[test]", MagicMock()) == []
        assert parse_api_response(SVM_MAPPING, {}, "[test]", MagicMock()) == []

    def test_anti_ransomware_missing_on_older_ontap(self) -> None:
        """Anti-ransomware fields default when not present (pre-9.13)."""
        record: dict[str, Any] = {
            "uuid": "abc",
            "name": "svm1",
        }
        result = parse_api_record(SVM_MAPPING, record, "[test]")
        assert isinstance(result, SVMInfo)
        assert result.anti_ransomware_auto_switch_from_learning_to_enabled is True
        assert result.anti_ransomware_auto_switch_minimum_incoming_data_percent == 0
        assert result.anti_ransomware_auto_switch_duration_without_new_file_extension == 3
        assert result.anti_ransomware_auto_switch_minimum_learning_period == 10
        assert result.anti_ransomware_auto_switch_minimum_file_count == 200
        assert result.anti_ransomware_auto_switch_minimum_file_extension == 10

    def test_storage_limit_missing(self) -> None:
        """storage.limit defaults to 0 when storage object is missing."""
        record: dict[str, Any] = {"uuid": "abc", "name": "svm1"}
        result = parse_api_record(SVM_MAPPING, record, "[test]")
        assert isinstance(result, SVMInfo)
        assert result.storage_limit == 0


# ---------------------------------------------------------------------------
# Parity test: old parser vs new framework
# ---------------------------------------------------------------------------


class TestParityWithOldParser:
    """Verify framework produces same output as old hand-written inline parser.

    Parity is checked for the original shared fields only (uuid, name,
    subtype, language). The old fields ``state``, ``root_volume``,
    ``root_volume_aggregate``, and ``allowed_protocols`` have been removed.
    """

    _ORIGINAL_SHARED_FIELDS = (
        "uuid",
        "name",
        "subtype",
        "language",
    )

    @staticmethod
    def _old_parse_svm(record: dict[str, Any]) -> SVMInfo:
        """Reproduce old inline SVM parsing logic from collector.

        This is a static copy of the code that was in
        ``_collect_storage_via_api`` before migration, adapted to
        the new model (removed fields are omitted).
        """
        return SVMInfo(
            uuid=record.get("uuid", ""),
            name=record.get("name", ""),
            subtype=record.get("subtype", ""),
            language=record.get("language", ""),
        )

    def test_parity_full_record(self, full_api_record: dict[str, Any]) -> None:
        """Framework and old parser produce identical results for shared fields."""
        old = self._old_parse_svm(full_api_record)
        new = parse_api_record(SVM_MAPPING, full_api_record, "[test]")
        assert isinstance(new, SVMInfo)
        for field_name in self._ORIGINAL_SHARED_FIELDS:
            old_val = getattr(old, field_name)
            new_val = getattr(new, field_name)
            assert old_val == new_val, (
                f"Field '{field_name}' differs: old={old_val!r}, new={new_val!r}"
            )

    def test_parity_minimal_record(self) -> None:
        """Framework and old parser match on minimal record."""
        record: dict[str, Any] = {"uuid": "svm-1"}
        old = self._old_parse_svm(record)
        new = parse_api_record(SVM_MAPPING, record, "[test]")
        assert isinstance(new, SVMInfo)
        for field_name in self._ORIGINAL_SHARED_FIELDS:
            old_val = getattr(old, field_name)
            new_val = getattr(new, field_name)
            assert old_val == new_val, (
                f"Field '{field_name}' differs: old={old_val!r}, new={new_val!r}"
            )


# ---------------------------------------------------------------------------
# Removed fields tests
# ---------------------------------------------------------------------------


class TestRemovedFields:
    """Verify that removed legacy fields no longer exist on SVMInfo."""

    @pytest.mark.parametrize(
        "field_name",
        ["state", "root_volume", "root_volume_aggregate", "allowed_protocols"],
    )
    def test_removed_field_not_on_model(self, field_name: str) -> None:
        """Legacy field is no longer a model attribute."""
        assert field_name not in SVMInfo.model_fields
