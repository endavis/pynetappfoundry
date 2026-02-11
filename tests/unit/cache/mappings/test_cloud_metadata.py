"""Tests for the cloud metadata type mapping definition."""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from pynetappfoundry.cache import CloudMetadata
from pynetappfoundry.cache.field_mapping import (
    parse_cli_record,
    parse_cli_records,
)
from pynetappfoundry.cache.mappings.cloud_metadata import CLOUD_METADATA_MAPPING

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def full_cli_record() -> dict[str, str]:
    """Full CLI record with all fields (normalized snake_case keys)."""
    return {
        "node": "PRODCL1-01",
        "instance_id": "i-0abc123def456789",
        "account_id": "123456789012",
        "image_id": "ami-0abc123def456789",
        "instance_type": "m5.2xlarge",
        "cpu_platform": "Intel Cascade Lake",
        "region": "us-east-1",
        "provider": "AWS",
        "consumer": "NetApp",
        "primary_ip": "10.0.1.100",
        "metadata_version": "V2",
        "availability_zone": "us-east-1a",
        "availability_zone_id": "use1-az1",
        "fault_domain": "",
        "update_domain": "",
        "resource_group_name": "",
        "offer": "",
        "sku": "",
        "sku_version": "",
    }


@pytest.fixture
def azure_cli_record() -> dict[str, str]:
    """CLI record for an Azure instance."""
    return {
        "node": "AZURECL1-01",
        "instance_id": (
            "/subscriptions/sub-id/resourceGroups/rg-1"
            "/providers/Microsoft.Compute/virtualMachines/vm-1"
        ),
        "account_id": "sub-id",
        "image_id": "Canonical:UbuntuServer:18.04-LTS:latest",
        "instance_type": "Standard_DS3_v2",
        "cpu_platform": "",
        "region": "eastus",
        "provider": "Azure",
        "consumer": "NetApp",
        "primary_ip": "10.0.2.50",
        "metadata_version": "V1",
        "availability_zone": "",
        "availability_zone_id": "",
        "fault_domain": "0",
        "update_domain": "0",
        "resource_group_name": "rg-1",
        "offer": "netapp-ontap-cloud",
        "sku": "ontap_cloud_byol",
        "sku_version": "9.14.0",
    }


# ---------------------------------------------------------------------------
# Mapping definition tests
# ---------------------------------------------------------------------------


class TestCloudMetadataMappingDefinition:
    """Tests for CLOUD_METADATA_MAPPING structure."""

    def test_all_cache_attrs_exist_on_model(self) -> None:
        """Every cache_attr in the mapping is a valid CloudMetadata field."""
        model_fields = set(CloudMetadata.model_fields.keys())
        for field in CLOUD_METADATA_MAPPING.fields:
            assert field.cache_attr in model_fields, (
                f"cache_attr '{field.cache_attr}' not on CloudMetadata"
            )

    def test_no_duplicate_cache_attrs(self) -> None:
        """No duplicate cache_attr values."""
        attrs = [f.cache_attr for f in CLOUD_METADATA_MAPPING.fields]
        assert len(attrs) == len(set(attrs))

    def test_api_endpoint_empty(self) -> None:
        """API endpoint is empty (CLI-only type)."""
        assert CLOUD_METADATA_MAPPING.api_endpoint == ""

    def test_cli_command(self) -> None:
        """CLI command is virtual-machine instance show."""
        assert CLOUD_METADATA_MAPPING.cli_command == "virtual-machine instance show"

    def test_model_class(self) -> None:
        """Model class is CloudMetadata."""
        assert CLOUD_METADATA_MAPPING.model_class is CloudMetadata

    def test_id_field(self) -> None:
        """id_field is node."""
        assert CLOUD_METADATA_MAPPING.id_field == "node"

    def test_field_count(self) -> None:
        """Mapping has expected number of fields (19 non-computed fields)."""
        assert len(CLOUD_METADATA_MAPPING.fields) == 19

    def test_cli_expected_fields(self) -> None:
        """cli_expected_fields returns correct CLI field names."""
        expected = CLOUD_METADATA_MAPPING.cli_expected_fields()
        assert expected == [
            "account_id",
            "availability_zone",
            "availability_zone_id",
            "consumer",
            "cpu_platform",
            "fault_domain",
            "image_id",
            "instance_id",
            "instance_type",
            "metadata_version",
            "node",
            "offer",
            "primary_ip",
            "provider",
            "region",
            "resource_group_name",
            "sku",
            "sku_version",
            "update_domain",
        ]

    def test_computed_link_fields_excluded(self) -> None:
        """Computed link fields are NOT in the mapping."""
        attrs = {f.cache_attr for f in CLOUD_METADATA_MAPPING.fields}
        assert "instance_link" not in attrs
        assert "instance_sso_link" not in attrs
        assert "resource_group_link" not in attrs

    def test_all_fields_use_cli_field_not_api_path(self) -> None:
        """All fields use cli_field (not api_path) since this is CLI-only."""
        for field in CLOUD_METADATA_MAPPING.fields:
            assert field.cli_field is not None, (
                f"Field '{field.cache_attr}' should have cli_field set"
            )
            assert field.api_path is None, (
                f"Field '{field.cache_attr}' should not have api_path (CLI-only type)"
            )


# ---------------------------------------------------------------------------
# CLI parsing tests
# ---------------------------------------------------------------------------


class TestCloudMetadataCliParsing:
    """Tests for parsing CLI cloud metadata records."""

    def test_full_aws_record(self, full_cli_record: dict[str, str]) -> None:
        """Full AWS CLI record parses to complete CloudMetadata."""
        cm = parse_cli_record(CLOUD_METADATA_MAPPING, full_cli_record, "[test]")
        assert isinstance(cm, CloudMetadata)
        assert cm.node == "PRODCL1-01"
        assert cm.instance_id == "i-0abc123def456789"
        assert cm.account_id == "123456789012"
        assert cm.image_id == "ami-0abc123def456789"
        assert cm.instance_type == "m5.2xlarge"
        assert cm.cpu_platform == "Intel Cascade Lake"
        assert cm.region == "us-east-1"
        assert cm.provider == "AWS"
        assert cm.consumer == "NetApp"
        assert cm.primary_ip == "10.0.1.100"
        assert cm.metadata_version == "V2"
        assert cm.availability_zone == "us-east-1a"
        assert cm.availability_zone_id == "use1-az1"

    def test_full_azure_record(self, azure_cli_record: dict[str, str]) -> None:
        """Full Azure CLI record parses to complete CloudMetadata."""
        cm = parse_cli_record(CLOUD_METADATA_MAPPING, azure_cli_record, "[test]")
        assert isinstance(cm, CloudMetadata)
        assert cm.node == "AZURECL1-01"
        assert cm.provider == "Azure"
        assert cm.fault_domain == "0"
        assert cm.update_domain == "0"
        assert cm.resource_group_name == "rg-1"
        assert cm.offer == "netapp-ontap-cloud"
        assert cm.sku == "ontap_cloud_byol"
        assert cm.sku_version == "9.14.0"

    def test_minimal_record(self) -> None:
        """Minimal record uses defaults for missing fields."""
        record: dict[str, str] = {"node": "node1"}
        cm = parse_cli_record(CLOUD_METADATA_MAPPING, record, "[test]")
        assert isinstance(cm, CloudMetadata)
        assert cm.node == "node1"
        assert cm.instance_id == ""
        assert cm.account_id == ""
        assert cm.image_id == ""
        assert cm.instance_type == ""
        assert cm.cpu_platform == ""
        assert cm.region == ""
        assert cm.provider == ""
        assert cm.consumer == ""
        assert cm.primary_ip == ""
        assert cm.metadata_version == ""
        assert cm.availability_zone == ""
        assert cm.availability_zone_id == ""
        assert cm.fault_domain == ""
        assert cm.update_domain == ""
        assert cm.resource_group_name == ""
        assert cm.offer == ""
        assert cm.sku == ""
        assert cm.sku_version == ""

    def test_empty_record(self) -> None:
        """Empty record uses defaults for all fields."""
        record: dict[str, str] = {}
        cm = parse_cli_record(CLOUD_METADATA_MAPPING, record, "[test]")
        assert isinstance(cm, CloudMetadata)
        assert cm.node == ""
        assert cm.instance_id == ""
        assert cm.provider == ""

    def test_dash_coercion(self) -> None:
        """CLI dash value is coerced to default (empty string)."""
        record: dict[str, str] = {
            "node": "node1",
            "instance_id": "-",
            "region": "-",
            "provider": "-",
        }
        cm = parse_cli_record(CLOUD_METADATA_MAPPING, record, "[test]")
        assert isinstance(cm, CloudMetadata)
        assert cm.instance_id == ""
        assert cm.region == ""
        assert cm.provider == ""

    def test_empty_string_coercion(self) -> None:
        """CLI empty string is coerced to default."""
        record: dict[str, str] = {
            "node": "node1",
            "instance_id": "",
            "region": "",
        }
        cm = parse_cli_record(CLOUD_METADATA_MAPPING, record, "[test]")
        assert isinstance(cm, CloudMetadata)
        assert cm.instance_id == ""
        assert cm.region == ""

    def test_whitespace_coercion(self) -> None:
        """CLI whitespace-only value is coerced properly (stripped then empty)."""
        record: dict[str, str] = {
            "node": "node1",
            "instance_id": "  ",
        }
        cm = parse_cli_record(CLOUD_METADATA_MAPPING, record, "[test]")
        assert isinstance(cm, CloudMetadata)
        assert cm.instance_id == ""

    def test_parse_cli_records_multiple(self) -> None:
        """parse_cli_records handles multiple records."""
        records = [
            {"node": "node1", "provider": "AWS", "region": "us-east-1"},
            {"node": "node2", "provider": "AWS", "region": "us-east-1"},
        ]
        results = parse_cli_records(CLOUD_METADATA_MAPPING, records, "[test]", MagicMock())
        assert len(results) == 2
        assert isinstance(results[0], CloudMetadata)
        assert isinstance(results[1], CloudMetadata)
        assert results[0].node == "node1"
        assert results[1].node == "node2"

    def test_parse_cli_records_empty(self) -> None:
        """parse_cli_records handles empty list."""
        results = parse_cli_records(CLOUD_METADATA_MAPPING, [], "[test]", MagicMock())
        assert results == []

    def test_computed_link_fields_default_empty(self, full_cli_record: dict[str, str]) -> None:
        """Computed link fields default to empty (not set by mapping)."""
        cm = parse_cli_record(CLOUD_METADATA_MAPPING, full_cli_record, "[test]")
        assert isinstance(cm, CloudMetadata)
        assert cm.instance_link == ""
        assert cm.instance_sso_link == ""
        assert cm.resource_group_link == ""


# ---------------------------------------------------------------------------
# Parity test: old parser vs new framework
# ---------------------------------------------------------------------------


class TestParityWithOldParser:
    """Verify framework produces same output as old hand-written _create_cloud_metadata.

    Note: parity tests cover the non-computed fields only. The computed link
    fields (instance_link, instance_sso_link, resource_group_link) are built
    as post-processing in the collector, not by the mapping.
    """

    _NON_COMPUTED_FIELDS = (
        "node",
        "instance_id",
        "account_id",
        "image_id",
        "instance_type",
        "cpu_platform",
        "region",
        "provider",
        "consumer",
        "primary_ip",
        "metadata_version",
        "availability_zone",
        "availability_zone_id",
        "fault_domain",
        "update_domain",
        "resource_group_name",
        "offer",
        "sku",
        "sku_version",
    )

    @staticmethod
    def _old_create_cloud_metadata(node: str, data: dict[str, str]) -> CloudMetadata:
        """Reproduce old _create_cloud_metadata logic (without links)."""
        return CloudMetadata(
            node=node,
            instance_id=data.get("instance_id", ""),
            account_id=data.get("account_id", ""),
            image_id=data.get("image_id", ""),
            instance_type=data.get("instance_type", ""),
            cpu_platform=data.get("cpu_platform", ""),
            region=data.get("region", ""),
            provider=data.get("provider", ""),
            consumer=data.get("consumer", ""),
            primary_ip=data.get("primary_ip", ""),
            metadata_version=data.get("metadata_version", ""),
            availability_zone=data.get("availability_zone", ""),
            availability_zone_id=data.get("availability_zone_id", ""),
            fault_domain=data.get("fault_domain", ""),
            update_domain=data.get("update_domain", ""),
            resource_group_name=data.get("resource_group_name", ""),
            offer=data.get("offer", ""),
            sku=data.get("sku", ""),
            sku_version=data.get("sku_version", ""),
        )

    def test_parity_full_aws_record(self, full_cli_record: dict[str, str]) -> None:
        """Framework and old parser produce identical CloudMetadata for AWS."""
        old = self._old_create_cloud_metadata(full_cli_record["node"], full_cli_record)
        new = parse_cli_record(CLOUD_METADATA_MAPPING, full_cli_record, "[test]")
        assert isinstance(new, CloudMetadata)
        for field_name in self._NON_COMPUTED_FIELDS:
            old_val = getattr(old, field_name)
            new_val = getattr(new, field_name)
            assert old_val == new_val, (
                f"Field '{field_name}' differs: old={old_val!r}, new={new_val!r}"
            )

    def test_parity_full_azure_record(self, azure_cli_record: dict[str, str]) -> None:
        """Framework and old parser produce identical CloudMetadata for Azure."""
        old = self._old_create_cloud_metadata(azure_cli_record["node"], azure_cli_record)
        new = parse_cli_record(CLOUD_METADATA_MAPPING, azure_cli_record, "[test]")
        assert isinstance(new, CloudMetadata)
        for field_name in self._NON_COMPUTED_FIELDS:
            old_val = getattr(old, field_name)
            new_val = getattr(new, field_name)
            assert old_val == new_val, (
                f"Field '{field_name}' differs: old={old_val!r}, new={new_val!r}"
            )

    def test_parity_minimal_record(self) -> None:
        """Framework and old parser match on minimal record."""
        data: dict[str, str] = {}
        old = self._old_create_cloud_metadata("node1", data)
        record = dict(data)
        record["node"] = "node1"
        new = parse_cli_record(CLOUD_METADATA_MAPPING, record, "[test]")
        assert isinstance(new, CloudMetadata)
        for field_name in self._NON_COMPUTED_FIELDS:
            old_val = getattr(old, field_name)
            new_val = getattr(new, field_name)
            assert old_val == new_val, (
                f"Field '{field_name}' differs: old={old_val!r}, new={new_val!r}"
            )

    def test_parity_missing_fields(self) -> None:
        """Framework and old parser match when most fields are missing."""
        data: dict[str, str] = {
            "provider": "AWS",
            "instance_id": "i-12345",
        }
        old = self._old_create_cloud_metadata("testnode", data)
        record = dict(data)
        record["node"] = "testnode"
        new = parse_cli_record(CLOUD_METADATA_MAPPING, record, "[test]")
        assert isinstance(new, CloudMetadata)
        for field_name in self._NON_COMPUTED_FIELDS:
            old_val = getattr(old, field_name)
            new_val = getattr(new, field_name)
            assert old_val == new_val, (
                f"Field '{field_name}' differs: old={old_val!r}, new={new_val!r}"
            )
