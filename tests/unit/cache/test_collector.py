"""Tests for metadata collector."""

from __future__ import annotations

import logging
from typing import Any
from unittest.mock import MagicMock

import pytest

from pynetappfoundry.cache.cloud.metadata.model import CloudMetadata
from pynetappfoundry.cache.collector import (
    CollectionPhase,
    MetadataCollector,
    ProgressInfo,
)
from pynetappfoundry.cache.protocols.model import ProtocolsInfo


class TestMetadataCollectorInit:
    """Tests for MetadataCollector initialization."""

    def test_init_with_both_clients(self) -> None:
        """Test initialization with both API and CLI clients."""
        api_client = MagicMock()
        cli_client = MagicMock()
        collector = MetadataCollector(api_client=api_client, cli_client=cli_client)
        assert collector.api_client is api_client
        assert collector.cli_client is cli_client

    def test_init_with_api_only(self) -> None:
        """Test initialization with API client only."""
        api_client = MagicMock()
        collector = MetadataCollector(api_client=api_client)
        assert collector.api_client is api_client
        assert collector.cli_client is None

    def test_init_with_cli_only(self) -> None:
        """Test initialization with CLI client only."""
        cli_client = MagicMock()
        collector = MetadataCollector(cli_client=cli_client)
        assert collector.api_client is None
        assert collector.cli_client is cli_client


class TestCloudMetadataCollection:
    """Tests for cloud metadata collection."""

    @pytest.fixture
    def mock_vm_instance_output_aws(self) -> list[str]:
        """Mock CLI output for AWS virtual-machine instance show."""
        return [
            "Node: cvo-node1",
            "    Instance ID: i-0abc123def456",
            "    Account ID: 123456789012",
            "    Instance Type: m5.2xlarge",
            "    Region: us-east-1",
            "    Provider: AWS",
            "    Availability Zone: us-east-1a",
            "    Primary IP: 10.0.0.1",
        ]

    @pytest.fixture
    def mock_vm_instance_output_azure(self) -> list[str]:
        """Mock CLI output for Azure virtual-machine instance show."""
        return [
            "Node: cvo-node1",
            "    Instance ID: azure-vm-123",
            "    Account ID: sub-12345",
            "    Provider: Azure",
            "    Region: eastus",
            "    Fault Domain: 0",
            "    Update Domain: 1",
            "    Resource Group Name: rg-storage",
        ]

    def test_collect_cloud_metadata_aws(self, mock_vm_instance_output_aws: list[str]) -> None:
        """Test collecting AWS cloud metadata."""
        cli_client = MagicMock()
        cli_client.run_command.return_value = mock_vm_instance_output_aws

        collector = MetadataCollector(cli_client=cli_client)
        result = collector.collect_cloud_metadata()

        assert len(result) == 1
        assert result[0].node == "cvo-node1"
        assert result[0].provider == "AWS"
        assert result[0].instance_id == "i-0abc123def456"
        assert result[0].region == "us-east-1"
        assert result[0].availability_zone == "us-east-1a"
        assert result[0].instance_type == "m5.2xlarge"

    def test_collect_cloud_metadata_azure(self, mock_vm_instance_output_azure: list[str]) -> None:
        """Test collecting Azure cloud metadata."""
        cli_client = MagicMock()
        cli_client.run_command.return_value = mock_vm_instance_output_azure

        collector = MetadataCollector(cli_client=cli_client)
        result = collector.collect_cloud_metadata()

        assert len(result) == 1
        assert result[0].node == "cvo-node1"
        assert result[0].provider == "Azure"
        assert result[0].fault_domain == "0"
        assert result[0].resource_group_name == "rg-storage"

    def test_aws_instance_link_populated(self, mock_vm_instance_output_aws: list[str]) -> None:
        """Test that AWS instance_link is populated correctly."""
        cli_client = MagicMock()
        cli_client.run_command.return_value = mock_vm_instance_output_aws

        collector = MetadataCollector(cli_client=cli_client)
        result = collector.collect_cloud_metadata()

        assert len(result) == 1
        assert result[0].instance_link.startswith("https://us-east-1.console.aws.amazon.com/")
        assert "i-0abc123def456" in result[0].instance_link
        # AWS doesn't have resource groups
        assert result[0].resource_group_link == ""

    def test_azure_links_populated(self, mock_vm_instance_output_azure: list[str]) -> None:
        """Test that Azure instance_link and resource_group_link are populated."""
        cli_client = MagicMock()
        cli_client.run_command.return_value = mock_vm_instance_output_azure

        collector = MetadataCollector(cli_client=cli_client)
        result = collector.collect_cloud_metadata()

        assert len(result) == 1
        # Instance link should start with portal URL and contain resource details
        assert result[0].instance_link.startswith("https://portal.azure.com/")
        assert "sub-12345" in result[0].instance_link
        assert "rg-storage" in result[0].instance_link
        assert "azure-vm-123" in result[0].instance_link
        # Resource group link should start with portal URL and contain resource group
        assert result[0].resource_group_link.startswith("https://portal.azure.com/")
        assert "sub-12345" in result[0].resource_group_link
        assert "rg-storage" in result[0].resource_group_link

    def test_aws_sso_link_populated_with_config(self) -> None:
        """Test that AWS instance_sso_link is populated when SSO config provided."""
        cli_client = MagicMock()
        cli_client.run_command.return_value = [
            "Node: cvo-node1",
            "    Instance ID: i-0abc123def456",
            "    Account ID: 123456789012",
            "    Instance Type: m5.2xlarge",
            "    Region: us-east-1",
            "    Provider: AWS",
        ]
        sso_config = {
            "subdomain": "mycompany",
            "account_roles": {"123456789012": "AdminAccess"},
        }

        collector = MetadataCollector(cli_client=cli_client, aws_sso_config=sso_config)
        result = collector.collect_cloud_metadata()

        assert len(result) == 1
        assert result[0].instance_sso_link.startswith("https://mycompany.awsapps.com/start/")
        assert "account_id=123456789012" in result[0].instance_sso_link
        assert "role_name=AdminAccess" in result[0].instance_sso_link

    def test_aws_sso_link_empty_without_config(self) -> None:
        """Test that AWS instance_sso_link is empty when no SSO config."""
        cli_client = MagicMock()
        cli_client.run_command.return_value = [
            "Node: cvo-node1",
            "    Instance ID: i-0abc123def456",
            "    Account ID: 123456789012",
            "    Provider: AWS",
            "    Region: us-east-1",
        ]

        collector = MetadataCollector(cli_client=cli_client)  # No SSO config
        result = collector.collect_cloud_metadata()

        assert len(result) == 1
        assert result[0].instance_sso_link == ""

    def test_azure_sso_link_always_empty(self) -> None:
        """Test that Azure instance_sso_link is always empty (SSO not applicable)."""
        cli_client = MagicMock()
        cli_client.run_command.return_value = [
            "Node: cvo-node1",
            "    Instance ID: azure-vm-123",
            "    Account ID: sub-12345",
            "    Provider: Azure",
            "    Region: eastus",
            "    Resource Group Name: rg-storage",
        ]
        sso_config = {
            "subdomain": "mycompany",
            "account_roles": {"sub-12345": "SomeRole"},
        }

        collector = MetadataCollector(cli_client=cli_client, aws_sso_config=sso_config)
        result = collector.collect_cloud_metadata()

        assert len(result) == 1
        assert result[0].instance_sso_link == ""

    def test_collect_cloud_metadata_ha_cluster(self) -> None:
        """Test collecting cloud metadata from HA cluster with two nodes."""
        cli_client = MagicMock()
        cli_client.run_command.return_value = [
            "Node: cvo-node1",
            "    Instance ID: i-0abc123",
            "    Provider: AWS",
            "    Primary IP: 10.0.0.1",
            "    Availability Zone: us-east-1a",
            "Node: cvo-node2",
            "    Instance ID: i-0def456",
            "    Provider: AWS",
            "    Primary IP: 10.0.0.2",
            "    Availability Zone: us-east-1b",
        ]

        collector = MetadataCollector(cli_client=cli_client)
        result = collector.collect_cloud_metadata()

        assert len(result) == 2
        assert result[0].node == "cvo-node1"
        assert result[0].instance_id == "i-0abc123"
        assert result[0].primary_ip == "10.0.0.1"
        assert result[0].availability_zone == "us-east-1a"
        assert result[1].node == "cvo-node2"
        assert result[1].instance_id == "i-0def456"
        assert result[1].primary_ip == "10.0.0.2"
        assert result[1].availability_zone == "us-east-1b"

    def test_collect_cloud_metadata_no_cli(self) -> None:
        """Test cloud metadata returns empty list when no CLI client."""
        collector = MetadataCollector()
        result = collector.collect_cloud_metadata()

        assert result == []

    def test_collect_cloud_metadata_cli_error(self) -> None:
        """Test cloud metadata handles CLI errors gracefully."""
        cli_client = MagicMock()
        cli_client.run_command.side_effect = Exception("Connection failed")

        collector = MetadataCollector(cli_client=cli_client)
        result = collector.collect_cloud_metadata()

        assert isinstance(result, list)
        assert result == []


class TestClusterInfoCollection:
    """Tests for cluster info collection."""

    @pytest.fixture
    def mock_cluster_api_response(self) -> dict[str, Any]:
        """Mock API response for /cluster endpoint."""
        return {
            "name": "mycluster",
            "uuid": "abc-123-def-456",
            "version": {
                "full": "NetApp Release 9.14.1",
                "generation": "SIMULATED",
                "major": 9,
                "minor": 14,
            },
            "contact": "admin@example.com",
            "location": "datacenter-1",
            "san_optimized": True,
            "timezone": {"name": "America/New_York"},
            "dns_domains": ["example.com"],
            "name_servers": ["10.0.0.1"],
            "ntp_servers": ["time.nist.gov"],
            "peering_policy": {
                "authentication_required": True,
                "encryption_required": False,
                "minimum_passphrase_length": 8,
            },
            "management_interfaces": [
                {"uuid": "mgmt-uuid-1"},
            ],
            "disaggregated": False,
            "auto_enable_activity_tracking": True,
            "auto_enable_analytics": False,
        }

    @pytest.fixture
    def mock_cluster_cli_output(self) -> tuple[list[dict[str, str]], dict[str, str]]:
        """Mock CLI output for cluster identity show."""
        return (
            [{"cluster": "mycluster", "cluster-uuid": "abc-123-def-456"}],
            {},
        )

    def test_collect_cluster_info_via_api(self, mock_cluster_api_response: dict[str, Any]) -> None:
        """Test collecting cluster info via API."""
        api_client = MagicMock()
        api_client.call_endpoint.return_value = mock_cluster_api_response

        collector = MetadataCollector(api_client=api_client)
        result = collector.collect_cluster_info()

        assert result.cluster_name == "mycluster"
        assert result.cluster_uuid == "abc-123-def-456"
        assert "9.14.1" in result.ontap_version
        assert result.version_generation == "SIMULATED"
        assert result.version_major == 9
        assert result.version_minor == 14
        assert result.contact == "admin@example.com"
        assert result.location == "datacenter-1"
        assert result.san_optimized is True
        assert result.timezone == "America/New_York"
        assert result.dns_domains == ["example.com"]
        assert result.name_servers == ["10.0.0.1"]
        assert result.ntp_servers == ["time.nist.gov"]
        assert result.peering_policy_authentication_required is True
        assert result.peering_policy_encryption_required is False
        assert result.peering_policy_minimum_passphrase_length == 8
        assert result.management_interface_uuids == ["mgmt-uuid-1"]
        assert result.disaggregated is False
        assert result.auto_enable_activity_tracking is True
        assert result.auto_enable_analytics is False
        api_client.call_endpoint.assert_called_with("/cluster?fields=*", method="GET")

    def test_collect_cluster_info_api_failure_propagates(self) -> None:
        """Test cluster info raises when API call fails (no CLI fallback)."""
        api_client = MagicMock()
        api_client.call_endpoint.side_effect = Exception("API unavailable")

        collector = MetadataCollector(api_client=api_client)
        with pytest.raises(Exception, match="API unavailable"):
            collector.collect_cluster_info()

    def test_collect_cluster_info_no_clients(self) -> None:
        """Test cluster info raises CollectionError when no API client."""
        from pynetappfoundry.cache.collector import CollectionError

        collector = MetadataCollector()
        with pytest.raises(CollectionError, match="API_FAILURE"):
            collector.collect_cluster_info()


class TestNodesCollection:
    """Tests for node collection."""

    @pytest.fixture
    def mock_nodes_api_response(self) -> dict[str, Any]:
        """Mock API response for /cluster/nodes endpoint."""
        return {
            "records": [
                {
                    "uuid": "node-uuid-1",
                    "name": "node1",
                    "serial_number": "123456",
                    "system_id": "0123456789",
                    "model": "SIMULATED",
                    "membership": "available",
                    "location": "rack-1",
                },
                {
                    "uuid": "node-uuid-2",
                    "name": "node2",
                    "serial_number": "789012",
                    "system_id": "9876543210",
                    "model": "SIMULATED",
                    "membership": "available",
                    "location": "rack-2",
                },
            ]
        }

    def test_collect_nodes_via_api(self, mock_nodes_api_response: dict[str, Any]) -> None:
        """Test collecting nodes via API."""
        api_client = MagicMock()
        api_client.get_all_records.return_value = mock_nodes_api_response

        collector = MetadataCollector(api_client=api_client)
        result = collector.collect_nodes()

        assert len(result) == 2
        assert result[0].name == "node1"
        assert result[0].serial_number == "123456"
        assert result[0].membership == "available"
        assert result[1].name == "node2"
        assert result[1].membership == "available"

    def test_collect_nodes_no_clients(self) -> None:
        """Test nodes raises CollectionError when no API client."""
        from pynetappfoundry.cache.collector import CollectionError

        collector = MetadataCollector()
        with pytest.raises(CollectionError, match="API_FAILURE"):
            collector.collect_nodes()


class TestNetworkCollection:
    """Tests for network collection."""

    @pytest.fixture
    def mock_network_api_responses(self) -> dict[str, dict[str, Any]]:
        """Mock API responses for network endpoints."""
        return {
            "/network/ip/interfaces?fields=*": {
                "records": [
                    {
                        "name": "data_lif1",
                        "ip": {"address": "10.0.0.10", "netmask": "255.255.255.0"},
                        "location": {
                            "home_node": {"name": "node1"},
                            "home_port": {"name": "e0d"},
                            "node": {"name": "node1"},
                            "port": {"name": "e0d"},
                        },
                        "state": "up",
                        "scope": "svm",
                        "svm": {"name": "svm1"},
                    }
                ]
            },
            "/network/ethernet/broadcast-domains?fields=*": {
                "records": [
                    {
                        "name": "Default",
                        "ipspace": {"name": "Default"},
                        "mtu": 1500,
                        "ports": [{"name": "node1:e0c"}, {"name": "node1:e0d"}],
                    }
                ]
            },
            "/network/ipspaces?fields=*": {"records": [{"name": "Default"}, {"name": "Cluster"}]},
            "/name-services/dns?fields=*": {
                "records": [
                    {
                        "uuid": "dns-uuid-1",
                        "svm": {"name": "svm1"},
                        "scope": "svm",
                        "domains": ["example.com"],
                        "servers": ["10.0.0.1", "10.0.0.2"],
                        "timeout": 2,
                        "attempts": 1,
                    }
                ]
            },
            "/network/ip/subnets?fields=*": {
                "records": [
                    {
                        "uuid": "subnet-uuid-1",
                        "name": "data-subnet",
                        "ipspace": {"name": "Default"},
                        "broadcast_domain": {"name": "Default"},
                        "subnet": {"address": "10.0.0.0", "netmask": "24"},
                        "gateway": "10.0.0.1",
                        "ip_ranges": [{"start": "10.0.0.10", "end": "10.0.0.50"}],
                    }
                ]
            },
        }

    def test_collect_network_via_api(
        self, mock_network_api_responses: dict[str, dict[str, Any]]
    ) -> None:
        """Test collecting network info via API."""
        api_client = MagicMock()
        api_client.get_all_records.side_effect = lambda endpoint, **_: (
            mock_network_api_responses.get(endpoint, {})
        )

        collector = MetadataCollector(api_client=api_client)
        result = collector.collect_network()

        assert len(result.data_lifs) == 1
        assert result.data_lifs[0].name == "data_lif1"
        assert len(result.broadcast_domains) == 1
        assert result.broadcast_domains[0].name == "Default"
        assert "Default" in result.ipspaces
        assert len(result.dns) == 1
        assert result.dns[0].svm == "svm1"
        assert result.dns[0].domains == ["example.com"]
        assert result.dns[0].servers == ["10.0.0.1", "10.0.0.2"]
        assert len(result.subnets) == 1
        assert result.subnets[0].name == "data-subnet"
        assert result.subnets[0].subnet == "10.0.0.0/24"
        assert result.subnets[0].gateway == "10.0.0.1"
        assert result.subnets[0].ip_ranges == ["10.0.0.10-10.0.0.50"]

    def test_collect_network_no_clients(self) -> None:
        """Test network raises CollectionError when no API client."""
        from pynetappfoundry.cache.collector import CollectionError

        collector = MetadataCollector()
        with pytest.raises(CollectionError, match="API_FAILURE"):
            collector.collect_network()


class TestStorageCollection:
    """Tests for storage collection."""

    @pytest.fixture
    def mock_storage_api_responses(self) -> dict[str, dict[str, Any]]:
        """Mock API responses for storage endpoints."""
        return {
            "/storage/aggregates?fields=*,is_spare_low,sidl_enabled": {
                "records": [
                    {
                        "name": "aggr1",
                        "node": {"name": "node1"},
                        "state": "online",
                        "block_storage": {"primary": {"disk_type": "ssd"}},
                        "space": {
                            "block_storage": {
                                "size": 1099511627776,
                                "used": 549755813888,
                            }
                        },
                    }
                ]
            },
            "/svm/svms?fields=*": {
                "records": [{"name": "svm1", "state": "running", "subtype": "default"}]
            },
            "/cloud/targets?fields=*": {"records": []},
            "/storage/volumes?fields=*,autosize,files,nas.path,nas.security_style": {
                "records": [
                    {
                        "uuid": "vol-uuid-1",
                        "name": "vol1",
                        "svm": {"name": "svm1"},
                        "state": "online",
                        "type": "rw",
                        "style": "flexvol",
                        "size": 1099511627776,
                        "autosize": {"mode": "grow", "grow_threshold": 85},
                        "tiering": {"policy": "auto", "min_cooling_days": 31},
                        "aggregates": [{"name": "aggr1"}],
                        "snapshot_policy": {"name": "default"},
                        "nas": {
                            "export_policy": {"name": "default"},
                            "path": "/vol1",
                            "security_style": "unix",
                        },
                    }
                ]
            },
            "/storage/qtrees?fields=*": {
                "records": [
                    {
                        "id": 1,
                        "name": "qt1",
                        "svm": {"name": "svm1"},
                        "volume": {"name": "vol1"},
                        "path": "/vol1/qt1",
                        "security_style": "unix",
                        "unix_permissions": 755,
                        "export_policy": {"name": "default"},
                    }
                ]
            },
            "/storage/snapshot-policies?fields=*,copies": {
                "records": [
                    {
                        "uuid": "sp-uuid-1",
                        "name": "default",
                        "svm": {"name": "svm1"},
                        "enabled": True,
                        "scope": "svm",
                        "copies": [
                            {
                                "schedule": {"name": "hourly"},
                                "count": 6,
                                "prefix": "hourly",
                                "snapmirror_label": "",
                            }
                        ],
                    }
                ]
            },
            "/cluster/schedules?fields=*": {
                "records": [
                    {
                        "uuid": "sched-uuid-1",
                        "name": "hourly",
                        "type": "cron",
                        "scope": "cluster",
                        "cron": {"minutes": [0]},
                    }
                ]
            },
            "/storage/luns?fields=*": {
                "records": [
                    {
                        "uuid": "lun-uuid-1",
                        "name": "/vol/vol1/lun1",
                        "svm": {"name": "svm1"},
                        "location": {"volume": {"name": "vol1"}},
                        "space": {"size": 10737418240},
                        "os_type": "linux",
                        "serial_number": "ABC123",
                        "enabled": True,
                        "comment": "Test LUN",
                    }
                ]
            },
            "/protocols/san/igroups?fields=*": {
                "records": [
                    {
                        "uuid": "ig-uuid-1",
                        "name": "igroup1",
                        "svm": {"name": "svm1"},
                        "protocol": "iscsi",
                        "os_type": "linux",
                        "initiators": [{"name": "iqn.1991-05.com.example:host1"}],
                        "comment": "Test igroup",
                    }
                ]
            },
            "/storage/qos/policies?fields=*": {
                "records": [
                    {
                        "uuid": "qos-uuid-1",
                        "name": "qos-fixed",
                        "svm": {"name": "svm1"},
                        "scope": "svm",
                        "object_type": "user_defined",
                        "fixed": {
                            "max_throughput_iops": 5000,
                            "max_throughput_mbps": 200,
                        },
                    }
                ]
            },
            "/storage/flexcache/flexcaches?fields=*": {
                "records": [
                    {
                        "uuid": "fc-uuid-1",
                        "name": "fc_vol1",
                        "svm": {"name": "svm1"},
                        "path": "/fc_vol1",
                        "size": 1073741824,
                        "origins": [
                            {
                                "volume": {"name": "origin_vol1"},
                                "svm": {"name": "svm1"},
                            }
                        ],
                        "global_file_locking_enabled": True,
                        "dr_cache": False,
                    }
                ]
            },
        }

    def test_collect_storage_via_api(
        self, mock_storage_api_responses: dict[str, dict[str, Any]]
    ) -> None:
        """Test collecting storage info via API."""
        api_client = MagicMock()
        api_client.get_all_records.side_effect = lambda endpoint, **_: (
            mock_storage_api_responses.get(endpoint, {})
        )

        collector = MetadataCollector(api_client=api_client)
        result = collector.collect_storage()

        assert len(result.aggregates) == 1
        assert result.aggregates[0].name == "aggr1"
        assert result.aggregates[0].type == "ssd"
        assert len(result.svms) == 1
        assert result.svms[0].name == "svm1"
        assert len(result.volumes) == 1
        assert result.volumes[0].name == "vol1"
        assert result.volumes[0].uuid == "vol-uuid-1"
        assert result.volumes[0].junction_path == "/vol1"
        assert result.volumes[0].autosize_mode == "grow"
        assert result.volumes[0].tiering_policy == "auto"
        assert len(result.qtrees) == 1
        assert result.qtrees[0].name == "qt1"
        assert result.qtrees[0].security_style == "unix"
        assert len(result.snapshot_policies) == 1
        assert result.snapshot_policies[0].name == "default"
        assert len(result.snapshot_policies[0].schedules) == 1
        assert result.snapshot_policies[0].schedules[0].schedule == "hourly"
        assert result.snapshot_policies[0].schedules[0].count == 6
        assert len(result.schedules) == 1
        assert result.schedules[0].name == "hourly"
        assert result.schedules[0].type == "cron"
        assert len(result.luns) == 1
        assert result.luns[0].name == "/vol/vol1/lun1"
        assert result.luns[0].os_type == "linux"
        assert result.luns[0].size == 10737418240
        assert result.luns[0].volume == "vol1"
        assert len(result.igroups) == 1
        assert result.igroups[0].name == "igroup1"
        assert result.igroups[0].protocol == "iscsi"
        assert result.igroups[0].initiators == ["iqn.1991-05.com.example:host1"]
        assert len(result.qos_policies) == 1
        assert result.qos_policies[0].name == "qos-fixed"
        assert result.qos_policies[0].fixed_max_throughput_iops == 5000
        assert result.qos_policies[0].policy_class == "user_defined"
        assert len(result.flexcaches) == 1
        assert result.flexcaches[0].name == "fc_vol1"
        assert result.flexcaches[0].uuid == "fc-uuid-1"
        assert result.flexcaches[0].origins == ["svm1:origin_vol1"]
        assert result.flexcaches[0].global_file_locking_enabled is True

    def test_collect_storage_no_clients(self) -> None:
        """Test storage raises CollectionError when no API client."""
        from pynetappfoundry.cache.collector import CollectionError

        collector = MetadataCollector()
        with pytest.raises(CollectionError, match="API_FAILURE"):
            collector.collect_storage()


class TestCloudTargetsCollection:
    """Tests for cloud targets collection."""

    @pytest.fixture
    def mock_cloud_targets_api_response(self) -> dict[str, Any]:
        """Mock API response for /cloud/targets endpoint."""
        return {
            "records": [
                {
                    "name": "s3-target-1",
                    "uuid": "abc-123-def-456",
                    "provider_type": "AWS_S3",
                    "server": "s3.us-east-1.amazonaws.com",
                    "container": "my-bucket",
                    "owner": "fabricpool",
                    "scope": "cluster",
                    "used": 1099511627776,
                    "ssl_enabled": True,
                    "authentication_type": "key",
                    "ipspace": {"name": "Default"},
                },
                {
                    "name": "azure-target-1",
                    "uuid": "xyz-789",
                    "provider_type": "Azure_Cloud",
                    "server": "mystorageaccount.blob.core.windows.net",
                    "container": "mycontainer",
                    "owner": "snapmirror",
                    "scope": "svm",
                    "svm": {"name": "svm1"},
                    "used": 549755813888,
                    "ssl_enabled": True,
                    "authentication_type": "cap",
                    "snapmirror_use": "data_protection",
                },
            ]
        }

    @pytest.fixture
    def mock_storage_with_cloud_targets_api_responses(
        self, mock_cloud_targets_api_response: dict[str, Any]
    ) -> dict[str, dict[str, Any]]:
        """Mock API responses for storage endpoints including cloud targets."""
        return {
            "/storage/aggregates?fields=*,is_spare_low,sidl_enabled": {
                "records": [
                    {
                        "name": "aggr1",
                        "node": {"name": "node1"},
                        "state": "online",
                        "block_storage": {"primary": {"disk_type": "ssd"}},
                        "space": {"block_storage": {"size": 1099511627776, "used": 549755813888}},
                    }
                ]
            },
            "/svm/svms?fields=*": {
                "records": [{"name": "svm1", "state": "running", "subtype": "default"}]
            },
            "/cloud/targets?fields=*": mock_cloud_targets_api_response,
            "/storage/volumes?fields=*,autosize,files,nas.path,nas.security_style": {"records": []},
            "/storage/qtrees?fields=*": {"records": []},
            "/storage/snapshot-policies?fields=*,copies": {"records": []},
            "/cluster/schedules?fields=*": {"records": []},
            "/storage/luns?fields=*": {"records": []},
            "/protocols/san/igroups?fields=*": {"records": []},
            "/storage/qos/policies?fields=*": {"records": []},
            "/storage/flexcache/flexcaches?fields=*": {"records": []},
        }

    def test_collect_cloud_targets_via_api(
        self, mock_storage_with_cloud_targets_api_responses: dict[str, dict[str, Any]]
    ) -> None:
        """Test collecting cloud targets via API."""
        api_client = MagicMock()
        api_client.get_all_records.side_effect = lambda endpoint, **_: (
            mock_storage_with_cloud_targets_api_responses.get(endpoint, {})
        )

        collector = MetadataCollector(api_client=api_client)
        result = collector.collect_storage()

        assert len(result.cloud_targets) == 2
        # Check AWS S3 target
        s3_target = result.cloud_targets[0]
        assert s3_target.name == "s3-target-1"
        assert s3_target.provider_type == "AWS_S3"
        assert s3_target.container == "my-bucket"
        assert s3_target.owner == "fabricpool"
        assert s3_target.ipspace == "Default"
        # Check Azure target
        azure_target = result.cloud_targets[1]
        assert azure_target.name == "azure-target-1"
        assert azure_target.provider_type == "Azure_Cloud"
        assert azure_target.svm == "svm1"
        assert azure_target.snapmirror_use == "data_protection"

    def test_collect_cloud_targets_api_not_available(self) -> None:
        """Test that cloud targets collection handles API errors gracefully."""
        api_client = MagicMock()

        def side_effect(endpoint: str, **_: Any) -> dict[str, Any]:
            if endpoint == "/cloud/targets?fields=*":
                raise Exception("Endpoint not available")
            if endpoint == "/storage/aggregates?fields=*,is_spare_low,sidl_enabled":
                return {
                    "records": [{"name": "aggr1", "node": {"name": "node1"}, "state": "online"}]
                }
            if endpoint == "/svm/svms?fields=*":
                return {"records": [{"name": "svm1", "state": "running"}]}
            return {}

        api_client.get_all_records.side_effect = side_effect

        collector = MetadataCollector(api_client=api_client)
        result = collector.collect_storage()

        # Should still return storage info, just with empty cloud_targets
        assert len(result.aggregates) == 1
        assert result.cloud_targets == []

    def test_collect_cloud_targets_empty(self) -> None:
        """Test collecting when no cloud targets exist."""
        api_client = MagicMock()
        api_client.get_all_records.side_effect = lambda endpoint, **_: {
            "/storage/aggregates?fields=*,is_spare_low,sidl_enabled": {"records": []},
            "/svm/svms?fields=*": {"records": []},
            "/cloud/targets?fields=*": {"records": []},
        }.get(endpoint, {})

        collector = MetadataCollector(api_client=api_client)
        result = collector.collect_storage()

        assert result.cloud_targets == []


class TestLicenseCollection:
    """Tests for license collection."""

    @pytest.fixture
    def mock_licenses_api_response(self) -> dict[str, Any]:
        """Mock API response for /cluster/licensing/licenses endpoint."""
        return {
            "records": [
                {"name": "NFS", "state": "compliant", "scope": "cluster"},
                {"name": "CIFS", "state": "compliant", "scope": "cluster"},
                {
                    "name": "Cloud Volumes ONTAP",
                    "state": "compliant",
                    "scope": "cluster",
                    "capacity": {
                        "maximum_size": 109951162777600,
                        "used_size": 54975581388800,
                    },
                },
            ]
        }

    def test_collect_licenses_via_api(self, mock_licenses_api_response: dict[str, Any]) -> None:
        """Test collecting licenses via API."""
        api_client = MagicMock()
        api_client.get_all_records.return_value = mock_licenses_api_response

        collector = MetadataCollector(api_client=api_client)
        result = collector.collect_licenses()

        assert len(result.feature_licenses) == 2
        assert result.feature_licenses[0].name == "NFS"
        assert len(result.capacity_licenses) == 1
        assert result.capacity_licenses[0].name == "Cloud Volumes ONTAP"

    def test_collect_licenses_no_clients(self) -> None:
        """Test licenses raises CollectionError when no API client."""
        from pynetappfoundry.cache.collector import CollectionError

        collector = MetadataCollector()
        with pytest.raises(CollectionError, match="API_FAILURE"):
            collector.collect_licenses()


class TestMediatorCollection:
    """Tests for mediator info collection."""

    def test_collect_mediator_with_data(self) -> None:
        """Test mediator collection with mediator present."""
        api_client = MagicMock()
        api_client.get_all_records.return_value = {
            "records": [
                {
                    "ip_address": "10.0.0.100",
                    "uuid": "med-uuid-1",
                    "port": 31784,
                    "reachable": True,
                }
            ]
        }

        collector = MetadataCollector(api_client=api_client)
        result = collector.collect_mediator()

        assert result.mediator_address == "10.0.0.100"
        assert result.mediator_uuid == "med-uuid-1"
        assert result.mediator_port == 31784

    def test_collect_mediator_empty(self) -> None:
        """Test mediator collection with no mediator."""
        api_client = MagicMock()
        api_client.get_all_records.return_value = {"records": []}

        collector = MetadataCollector(api_client=api_client)
        result = collector.collect_mediator()

        assert result.mediator_address == ""
        assert result.mediator_uuid == ""
        assert result.mediator_port == 0

    def test_collect_mediator_endpoint_unavailable(self) -> None:
        """Test mediator collection when endpoint raises an exception."""
        api_client = MagicMock()
        api_client.get_all_records.side_effect = Exception("404 Not Found")

        collector = MetadataCollector(api_client=api_client)
        result = collector.collect_mediator()

        assert result.mediator_address == ""
        assert result.mediator_uuid == ""
        assert result.mediator_port == 0

    def test_collect_mediator_no_clients(self) -> None:
        """Test mediator raises CollectionError when no API client."""
        from pynetappfoundry.cache.collector import CollectionError

        collector = MetadataCollector()
        with pytest.raises(CollectionError, match="API_FAILURE"):
            collector.collect_mediator()


class TestRelationshipsCollection:
    """Tests for relationships collection."""

    @pytest.fixture
    def mock_relationships_api_responses(self) -> dict[str, dict[str, Any]]:
        """Mock API responses for relationship endpoints."""
        from pynetappfoundry.cache.snapmirror.relationships.mapping import SNAPMIRROR_MAPPING

        sm_endpoint = SNAPMIRROR_MAPPING.api_endpoint
        return {
            sm_endpoint: {
                "records": [
                    {
                        "uuid": "sm-uuid-1",
                        "source": {"path": "svm1:vol1"},
                        "destination": {"path": "svm2:vol1_dp"},
                        "policy": {"type": "async", "uuid": "pol-uuid-1"},
                        "throttle": 1024,
                        "group_type": "none",
                        "transfer_schedule": {"uuid": "sched-uuid-1"},
                    }
                ]
            },
            "/cluster/peers?fields=*": {
                "records": [
                    {
                        "name": "peer1",
                        "uuid": "abc-123",
                        "remote": {"name": "remote-cluster", "ip_addresses": ["10.0.1.1"]},
                        "peer_applications": ["snapmirror"],
                        "authentication": {"state": "ok"},
                    }
                ]
            },
            "/svm/peers?fields=*": {
                "records": [
                    {
                        "uuid": "svmpeer-uuid-1",
                        "name": "svm1_to_svm2",
                        "svm": {"name": "svm1"},
                        "peer": {
                            "svm": {"name": "svm2"},
                            "cluster": {"name": "remote-cluster"},
                        },
                        "state": "peered",
                        "applications": ["snapmirror"],
                    }
                ]
            },
        }

    def test_collect_relationships_via_api(
        self, mock_relationships_api_responses: dict[str, dict[str, Any]]
    ) -> None:
        """Test collecting relationships via API."""
        api_client = MagicMock()
        api_client.get_all_records.side_effect = lambda endpoint, **_: (
            mock_relationships_api_responses.get(endpoint, {})
        )

        collector = MetadataCollector(api_client=api_client)
        result = collector.collect_relationships()

        assert len(result.snapmirror_destinations) == 1
        assert result.snapmirror_destinations[0].source_path == "svm1:vol1"
        assert len(result.cluster_peers) == 1
        assert result.cluster_peers[0].remote_cluster_name == "remote-cluster"
        assert result.cluster_peers[0].peer_addresses == ["10.0.1.1"]
        assert len(result.svm_peers) == 1
        assert result.svm_peers[0].name == "svm1_to_svm2"
        assert result.svm_peers[0].svm == "svm1"
        assert result.svm_peers[0].peer_svm == "svm2"
        assert result.svm_peers[0].peer_cluster == "remote-cluster"
        assert result.svm_peers[0].state == "peered"
        assert result.svm_peers[0].applications == ["snapmirror"]

    def test_collect_relationships_no_clients(self) -> None:
        """Test relationships raises CollectionError when no API client."""
        from pynetappfoundry.cache.collector import CollectionError

        collector = MetadataCollector()
        with pytest.raises(CollectionError, match="API_FAILURE"):
            collector.collect_relationships()

    def test_collect_relationships_with_missing_source_dest(self) -> None:
        """Test relationships handles missing source/destination fields."""
        from pynetappfoundry.cache.snapmirror.relationships.mapping import SNAPMIRROR_MAPPING

        sm_endpoint = SNAPMIRROR_MAPPING.api_endpoint
        api_responses = {
            sm_endpoint: {
                "records": [
                    {
                        "uuid": "sm-uuid-1",
                        "policy": {"type": "async", "uuid": "pol-uuid-1"},
                    }
                ]
            },
            "/cluster/peers?fields=*": {"records": []},
            "/svm/peers?fields=*": {"records": []},
        }

        api_client = MagicMock()
        api_client.get_all_records.side_effect = lambda endpoint, **_: api_responses.get(
            endpoint, {}
        )

        collector = MetadataCollector(api_client=api_client)
        result = collector.collect_relationships()

        assert len(result.snapmirror_destinations) == 1
        assert result.snapmirror_destinations[0].source_path == ""
        assert result.snapmirror_destinations[0].destination_path == ""

    def test_collect_relationships_with_string_peer_fields(self) -> None:
        """Test relationships handles string fields in cluster peers (instead of dicts)."""
        from pynetappfoundry.cache.snapmirror.relationships.mapping import SNAPMIRROR_MAPPING

        sm_endpoint = SNAPMIRROR_MAPPING.api_endpoint
        api_responses = {
            sm_endpoint: {"records": []},
            "/cluster/peers?fields=*": {
                "records": [
                    {
                        "name": "peer1",
                        "uuid": "abc-123",
                        # API returns these as strings instead of dicts
                        "remote": "remote-cluster",
                        "peer_applications": [],
                        "authentication": "ok",
                    }
                ]
            },
            "/svm/peers?fields=*": {"records": []},
        }

        api_client = MagicMock()
        api_client.get_all_records.side_effect = lambda endpoint, **_: api_responses.get(
            endpoint, {}
        )

        collector = MetadataCollector(api_client=api_client)
        result = collector.collect_relationships()

        assert len(result.cluster_peers) == 1
        assert result.cluster_peers[0].name == "peer1"
        assert result.cluster_peers[0].remote_cluster_name == "remote-cluster"
        assert result.cluster_peers[0].authentication_state == "ok"
        # When remote is a string, peer_addresses will be empty
        assert result.cluster_peers[0].peer_addresses == []

    def test_collect_relationships_with_none_path(self) -> None:
        """Test relationships handles None path values."""
        from pynetappfoundry.cache.snapmirror.relationships.mapping import SNAPMIRROR_MAPPING

        sm_endpoint = SNAPMIRROR_MAPPING.api_endpoint
        api_responses = {
            sm_endpoint: {
                "records": [
                    {
                        "uuid": "sm-uuid-1",
                        "source": None,
                        "destination": None,
                        "policy": {"type": "async", "uuid": "pol-uuid-1"},
                    }
                ]
            },
            "/cluster/peers?fields=*": {"records": []},
            "/svm/peers?fields=*": {"records": []},
        }

        api_client = MagicMock()
        api_client.get_all_records.side_effect = lambda endpoint, **_: api_responses.get(
            endpoint, {}
        )

        collector = MetadataCollector(api_client=api_client)
        result = collector.collect_relationships()

        assert len(result.snapmirror_destinations) == 1
        assert result.snapmirror_destinations[0].source_path == ""
        assert result.snapmirror_destinations[0].destination_path == ""


class TestProtocolsCollection:
    """Tests for protocols collection."""

    @pytest.fixture
    def mock_protocols_api_responses(self) -> dict[str, dict[str, Any]]:
        """Mock API responses for protocol endpoints."""
        return {
            "/protocols/nfs/export-policies?fields=*,rules": {
                "records": [
                    {
                        "id": 1,
                        "name": "default",
                        "svm": {"name": "svm1"},
                        "rules": [
                            {
                                "index": 1,
                                "clients": [{"match": "0.0.0.0/0"}],
                                "protocols": ["nfs3", "nfs4"],
                                "ro_rule": ["sys"],
                                "rw_rule": ["sys"],
                                "superuser": ["none"],
                                "anonymous_user": "65534",
                            },
                        ],
                    },
                    {
                        "id": 2,
                        "name": "data_export",
                        "svm": {"name": "svm1"},
                        "rules": [
                            {
                                "index": 1,
                                "clients": [
                                    {"match": "10.0.0.0/8"},
                                    {"match": "172.16.0.0/12"},
                                ],
                                "protocols": ["nfs3"],
                                "ro_rule": ["sys"],
                                "rw_rule": ["sys"],
                                "superuser": ["sys"],
                                "anonymous_user": "65534",
                            },
                            {
                                "index": 2,
                                "clients": [{"match": "192.168.1.0/24"}],
                                "protocols": ["nfs4"],
                                "ro_rule": ["krb5"],
                                "rw_rule": ["krb5"],
                                "superuser": ["krb5"],
                                "anonymous_user": "nobody",
                            },
                        ],
                    },
                ]
            },
            "/protocols/cifs/shares?fields=*": {
                "records": [
                    {
                        "name": "share1",
                        "path": "/vol1",
                        "svm": {"name": "svm1"},
                        "comment": "Test share",
                        "home_directory": False,
                        "oplocks": True,
                        "access_based_enumeration": True,
                        "change_notify": True,
                        "encryption": False,
                        "unix_symlink": "local",
                    }
                ]
            },
            "/protocols/nfs/services?fields=*": {
                "records": [
                    {
                        "svm": {"name": "svm1"},
                        "enabled": True,
                        "protocol": {
                            "v3_enabled": True,
                            "v40_enabled": True,
                            "v41_enabled": False,
                        },
                        "showmount_enabled": True,
                        "vstorage_enabled": False,
                    }
                ]
            },
            "/protocols/cifs/services?fields=*": {
                "records": [
                    {
                        "svm": {"name": "svm1"},
                        "name": "CIFSSERVER",
                        "enabled": True,
                        "ad_domain": {"fqdn": "example.com"},
                        "comment": "Production CIFS",
                        "default_unix_user": "pcuser",
                        "netbios": {"aliases": ["ALIAS1"]},
                    }
                ]
            },
            "/protocols/s3/buckets?fields=*": {
                "records": [
                    {
                        "uuid": "bucket-uuid-1",
                        "name": "mybucket",
                        "svm": {"name": "svm1"},
                        "type": "s3",
                        "size": 1073741824,
                        "versioning_state": "enabled",
                        "comment": "Test bucket",
                        "nas_path": "",
                    }
                ]
            },
        }

    def test_collect_protocols_via_api(
        self, mock_protocols_api_responses: dict[str, dict[str, Any]]
    ) -> None:
        """Test collecting protocols via API."""
        api_client = MagicMock()
        api_client.get_all_records.side_effect = lambda endpoint, **_: (
            mock_protocols_api_responses.get(endpoint, {"records": []})
        )

        collector = MetadataCollector(api_client=api_client)
        result = collector.collect_protocols()

        assert isinstance(result, ProtocolsInfo)
        assert len(result.export_policies) == 2

        # Check first policy
        policy1 = result.export_policies[0]
        assert policy1.id == 1
        assert policy1.name == "default"
        assert policy1.svm == "svm1"
        assert len(policy1.rules) == 1
        assert policy1.rules[0].index == 1
        assert policy1.rules[0].clients == ["0.0.0.0/0"]
        assert policy1.rules[0].protocols == ["nfs3", "nfs4"]
        assert policy1.rules[0].ro_rule == ["sys"]
        assert policy1.rules[0].rw_rule == ["sys"]
        assert policy1.rules[0].superuser == ["none"]
        assert policy1.rules[0].anonymous_user == "65534"

        # Check second policy with multiple rules
        policy2 = result.export_policies[1]
        assert policy2.name == "data_export"
        assert len(policy2.rules) == 2
        assert policy2.rules[0].clients == ["10.0.0.0/8", "172.16.0.0/12"]
        assert policy2.rules[1].protocols == ["nfs4"]
        assert policy2.rules[1].superuser == ["krb5"]

        # Check CIFS shares
        assert len(result.cifs_shares) == 1
        assert result.cifs_shares[0].name == "share1"
        assert result.cifs_shares[0].path == "/vol1"
        assert result.cifs_shares[0].access_based_enumeration is True
        assert result.cifs_shares[0].unix_symlink == "local"

        # Check NFS services
        assert len(result.nfs_services) == 1
        assert result.nfs_services[0].svm == "svm1"
        assert result.nfs_services[0].enabled is True
        assert result.nfs_services[0].protocol_v3_enabled is True
        assert result.nfs_services[0].protocol_v4_enabled is True
        assert result.nfs_services[0].protocol_v41_enabled is False
        assert result.nfs_services[0].showmount_enabled is True

        # Check CIFS services
        assert len(result.cifs_services) == 1
        assert result.cifs_services[0].svm == "svm1"
        assert result.cifs_services[0].name == "CIFSSERVER"
        assert result.cifs_services[0].enabled is True
        assert result.cifs_services[0].ad_domain == "example.com"
        assert result.cifs_services[0].default_unix_user == "pcuser"
        assert result.cifs_services[0].netbios_aliases == ["ALIAS1"]

        # Check S3 buckets
        assert len(result.s3_buckets) == 1
        assert result.s3_buckets[0].uuid == "bucket-uuid-1"
        assert result.s3_buckets[0].name == "mybucket"
        assert result.s3_buckets[0].svm == "svm1"
        assert result.s3_buckets[0].type == "s3"
        assert result.s3_buckets[0].size == 1073741824
        assert result.s3_buckets[0].versioning_state == "enabled"

    def test_collect_protocols_empty_response(self) -> None:
        """Test protocols handles empty API response."""
        api_client = MagicMock()
        api_client.get_all_records.return_value = {"records": []}

        collector = MetadataCollector(api_client=api_client)
        result = collector.collect_protocols()

        assert isinstance(result, ProtocolsInfo)
        assert result.export_policies == []
        assert result.cifs_shares == []
        assert result.nfs_services == []
        assert result.cifs_services == []
        assert result.s3_buckets == []

    def test_collect_protocols_no_clients(self) -> None:
        """Test protocols raises CollectionError when no API client."""
        from pynetappfoundry.cache.collector import CollectionError

        collector = MetadataCollector()
        with pytest.raises(CollectionError, match="API_FAILURE"):
            collector.collect_protocols()

    def test_collect_protocols_api_failure_propagates(self) -> None:
        """Test protocols raises when API call fails (no silent fallback)."""
        api_client = MagicMock()
        api_client.get_all_records.side_effect = Exception("API error")

        collector = MetadataCollector(api_client=api_client)
        with pytest.raises(Exception, match="API error"):
            collector.collect_protocols()

    def test_collect_protocols_policy_without_rules(self) -> None:
        """Test protocols handles policy records with no rules."""
        responses: dict[str, dict[str, Any]] = {
            "/protocols/nfs/export-policies?fields=*,rules": {
                "records": [
                    {
                        "id": 1,
                        "name": "empty_policy",
                        "svm": {"name": "svm1"},
                    },
                ]
            },
            "/protocols/cifs/shares?fields=*": {"records": []},
            "/protocols/nfs/services?fields=*": {"records": []},
            "/protocols/cifs/services?fields=*": {"records": []},
            "/protocols/s3/buckets?fields=*": {"records": []},
        }
        api_client = MagicMock()
        api_client.get_all_records.side_effect = lambda endpoint, **_: responses.get(
            endpoint, {"records": []}
        )

        collector = MetadataCollector(api_client=api_client)
        result = collector.collect_protocols()

        assert len(result.export_policies) == 1
        assert result.export_policies[0].name == "empty_policy"
        assert result.export_policies[0].rules == []


class TestCollectAll:
    """Tests for collect_all method."""

    def test_collect_all_returns_complete_metadata(self) -> None:
        """Test collect_all returns CachedClusterMetadata."""
        api_client = MagicMock()
        api_client.get_all_records.return_value = {"records": []}
        api_client.call_endpoint.return_value = {"records": []}

        cli_client = MagicMock()
        cli_client.run_command.return_value = []
        cli_client.run_command_and_parse.return_value = {}

        collector = MetadataCollector(api_client=api_client, cli_client=cli_client)
        result = collector.collect_all("test-cluster")

        assert result.cluster_name == "test-cluster"
        assert result.cached_at is not None
        assert result.cache_version == "1.0"


class TestCachedApiCallPagination:
    """Tests for _cached_api_call pagination dispatch."""

    def test_cached_api_call_uses_get_all_records_by_default(self) -> None:
        """Verify get_all_records is called when paginate=True (default)."""
        api_client = MagicMock()
        api_client.get_all_records.return_value = {"records": [{"name": "vol1"}]}

        collector = MetadataCollector(api_client=api_client)
        result = collector._cached_api_call("/storage/volumes?fields=*")

        api_client.get_all_records.assert_called_once_with(
            "/storage/volumes?fields=*", method="GET"
        )
        api_client.call_endpoint.assert_not_called()
        assert result == {"records": [{"name": "vol1"}]}

    def test_cached_api_call_uses_call_endpoint_when_paginate_false(self) -> None:
        """Verify call_endpoint is called when paginate=False."""
        api_client = MagicMock()
        api_client.call_endpoint.return_value = {"name": "mycluster", "uuid": "abc-123"}

        collector = MetadataCollector(api_client=api_client)
        result = collector._cached_api_call("/cluster?fields=*", paginate=False)

        api_client.call_endpoint.assert_called_once_with("/cluster?fields=*", method="GET")
        api_client.get_all_records.assert_not_called()
        assert result == {"name": "mycluster", "uuid": "abc-123"}


class TestNormalizeCliKey:
    """Tests for CLI key normalization."""

    def test_normalize_simple(self) -> None:
        """Test normalizing simple keys."""
        assert MetadataCollector._normalize_cli_key("Instance ID") == "instance_id"
        assert MetadataCollector._normalize_cli_key("Provider") == "provider"

    def test_normalize_with_hyphens(self) -> None:
        """Test normalizing keys with hyphens."""
        assert MetadataCollector._normalize_cli_key("Availability-Zone") == "availability_zone"

    def test_normalize_special_chars(self) -> None:
        """Test normalizing keys with special characters."""
        assert MetadataCollector._normalize_cli_key("Region (AWS)") == "region_aws"


class TestProgressCallback:
    """Tests for progress callback functionality."""

    def test_init_with_progress_callback(self) -> None:
        """Test initialization with progress callback."""
        callback = MagicMock()
        collector = MetadataCollector(progress_callback=callback)
        assert collector.progress_callback is callback

    def test_progress_callback_called_for_each_phase(self) -> None:
        """Test that progress callback is called for each collection phase."""
        api_client = MagicMock()
        api_client.get_all_records.return_value = {"records": []}
        api_client.call_endpoint.return_value = {"records": []}

        cli_client = MagicMock()
        cli_client.run_command.return_value = []
        cli_client.run_command_and_parse.return_value = {}

        callback = MagicMock()
        collector = MetadataCollector(
            api_client=api_client, cli_client=cli_client, progress_callback=callback
        )
        collector.collect_all("test-cluster")

        # Should have phases * 2 calls (starting + completed)
        assert callback.call_count == len(CollectionPhase) * 2

        # Verify callback was called with ProgressInfo objects
        for call in callback.call_args_list:
            info = call[0][0]
            assert isinstance(info, ProgressInfo)
            assert isinstance(info.phase, CollectionPhase)
            assert info.status in ("starting", "completed", "failed")

    def test_progress_callback_receives_correct_phases(self) -> None:
        """Test that progress callback receives all expected phases."""
        api_client = MagicMock()
        api_client.get_all_records.return_value = {"records": []}
        api_client.call_endpoint.return_value = {"records": []}

        cli_client = MagicMock()
        cli_client.run_command.return_value = []
        cli_client.run_command_and_parse.return_value = {}

        received_phases: list[CollectionPhase] = []

        def track_phases(info: ProgressInfo) -> None:
            if info.status == "starting":
                received_phases.append(info.phase)

        collector = MetadataCollector(
            api_client=api_client, cli_client=cli_client, progress_callback=track_phases
        )
        collector.collect_all("test-cluster")

        expected_phases = [
            CollectionPhase.CLOUD,
            CollectionPhase.CLUSTER,
            CollectionPhase.NODES,
            CollectionPhase.NETWORK,
            CollectionPhase.STORAGE,
            CollectionPhase.LICENSES,
            CollectionPhase.MEDIATOR,
            CollectionPhase.RELATIONSHIPS,
            CollectionPhase.PROTOCOLS,
        ]
        assert received_phases == expected_phases

    def test_progress_callback_elapsed_time(self) -> None:
        """Test that progress callback receives elapsed time on completion."""
        api_client = MagicMock()
        api_client.get_all_records.return_value = {"records": []}
        api_client.call_endpoint.return_value = {"records": []}

        cli_client = MagicMock()
        cli_client.run_command.return_value = []
        cli_client.run_command_and_parse.return_value = {}

        elapsed_times: list[float] = []

        def track_elapsed(info: ProgressInfo) -> None:
            if info.status == "completed":
                elapsed_times.append(info.elapsed_seconds)

        collector = MetadataCollector(
            api_client=api_client, cli_client=cli_client, progress_callback=track_elapsed
        )
        collector.collect_all("test-cluster")

        # Should have elapsed times (one per completed phase)
        assert len(elapsed_times) == len(CollectionPhase)
        # All should be non-negative
        for elapsed in elapsed_times:
            assert elapsed >= 0

    def test_progress_callback_source_tracking(self) -> None:
        """Test that progress callback receives correct source information."""
        api_client = MagicMock()
        api_client.get_all_records.return_value = {"records": []}
        api_client.call_endpoint.return_value = {"records": []}

        cli_client = MagicMock()
        cli_client.run_command.return_value = []
        cli_client.run_command_and_parse.return_value = {}

        sources: dict[CollectionPhase, str | None] = {}

        def track_sources(info: ProgressInfo) -> None:
            if info.status == "completed":
                sources[info.phase] = info.source

        collector = MetadataCollector(
            api_client=api_client, cli_client=cli_client, progress_callback=track_sources
        )
        collector.collect_all("test-cluster")

        # Cloud metadata should be from CLI
        assert sources[CollectionPhase.CLOUD] == "cli"
        # Other phases should be from API (since API client is provided)
        assert sources[CollectionPhase.CLUSTER] == "api"
        assert sources[CollectionPhase.NODES] == "api"

    def test_progress_callback_none_no_error(self) -> None:
        """Test that no callback (None) doesn't cause errors."""
        api_client = MagicMock()
        api_client.get_all_records.return_value = {"records": []}
        api_client.call_endpoint.return_value = {"records": []}

        cli_client = MagicMock()
        cli_client.run_command.return_value = []
        cli_client.run_command_and_parse.return_value = {}

        collector = MetadataCollector(
            api_client=api_client, cli_client=cli_client, progress_callback=None
        )
        # Should not raise any errors
        result = collector.collect_all("test-cluster")
        assert result.cluster_name == "test-cluster"

    def test_report_progress_with_no_callback(self) -> None:
        """Test _report_progress does nothing when callback is None."""
        collector = MetadataCollector()
        # Should not raise any errors
        collector._report_progress(CollectionPhase.CLOUD, "starting")


class TestCollectionPhase:
    """Tests for CollectionPhase enum."""

    def test_all_phases_have_names(self) -> None:
        """Test that all phases have human-readable names."""
        for phase in CollectionPhase:
            assert phase in MetadataCollector.PHASE_NAMES
            assert len(MetadataCollector.PHASE_NAMES[phase]) > 0

    def test_phase_values(self) -> None:
        """Test CollectionPhase enum values."""
        assert CollectionPhase.CLOUD.value == "cloud"
        assert CollectionPhase.CLUSTER.value == "cluster"
        assert CollectionPhase.NODES.value == "nodes"
        assert CollectionPhase.NETWORK.value == "network"
        assert CollectionPhase.STORAGE.value == "storage"
        assert CollectionPhase.LICENSES.value == "licenses"
        assert CollectionPhase.MEDIATOR.value == "mediator"
        assert CollectionPhase.RELATIONSHIPS.value == "relationships"


class TestUpdateAzureCloudLinks:
    """Tests for Azure cloud link post-processing."""

    def test_updates_azure_ha_cluster_links(self) -> None:
        """Test Azure instance links are updated with cluster-based VM names for HA."""
        collector = MetadataCollector()
        cloud_metadata = [
            CloudMetadata(
                node="mycluster-01",
                instance_id="old-instance-id",
                account_id="sub-123",
                resource_group_name="my-rg",
                provider="Azure",
                instance_link="https://old-link.com",
            ),
            CloudMetadata(
                node="mycluster-02",
                instance_id="old-instance-id-2",
                account_id="sub-123",
                resource_group_name="my-rg",
                provider="Azure",
                instance_link="https://old-link-2.com",
            ),
        ]

        result = collector._update_azure_cloud_links(
            cloud_metadata,
            cluster_name="mycluster",
            is_ha=True,
        )

        assert len(result) == 2
        # Node 01 should get -vm1
        assert "mycluster-vm1" in result[0].instance_link
        assert "old-instance-id" not in result[0].instance_link
        # Node 02 should get -vm2
        assert "mycluster-vm2" in result[1].instance_link
        assert "old-instance-id-2" not in result[1].instance_link

    def test_updates_azure_single_node_links(self) -> None:
        """Test Azure instance links are updated for single node cluster."""
        collector = MetadataCollector()
        cloud_metadata = [
            CloudMetadata(
                node="mycluster-01",
                instance_id="old-instance-id",
                account_id="sub-123",
                resource_group_name="my-rg",
                provider="Azure",
                instance_link="https://old-link.com",
            ),
        ]

        result = collector._update_azure_cloud_links(
            cloud_metadata,
            cluster_name="mycluster",
            is_ha=False,
        )

        assert len(result) == 1
        # Single node should just use cluster name
        assert "mycluster" in result[0].instance_link
        assert "mycluster-vm1" not in result[0].instance_link

    def test_preserves_aws_cloud_metadata(self) -> None:
        """Test AWS cloud metadata is preserved without modification."""
        collector = MetadataCollector()
        cloud_metadata = [
            CloudMetadata(
                node="aws-node",
                instance_id="i-0abc123",
                account_id="123456789012",
                provider="AWS",
                region="us-east-1",
                instance_link="https://aws-link.com",
            ),
        ]

        result = collector._update_azure_cloud_links(
            cloud_metadata,
            cluster_name="mycluster",
            is_ha=True,
        )

        assert len(result) == 1
        # AWS should be unchanged
        assert result[0] is cloud_metadata[0]
        assert result[0].instance_link == "https://aws-link.com"

    def test_preserves_other_azure_fields(self) -> None:
        """Test that other Azure cloud metadata fields are preserved."""
        collector = MetadataCollector()
        cloud_metadata = [
            CloudMetadata(
                node="mycluster-01",
                instance_id="old-instance-id",
                account_id="sub-123",
                image_id="image-123",
                instance_type="Standard_D4s_v3",
                region="eastus",
                provider="Azure",
                fault_domain="0",
                update_domain="1",
                resource_group_name="my-rg",
                offer="netapp-ontap-cloud",
                sku="ontap_cloud",
                resource_group_link="https://rg-link.com",
            ),
        ]

        result = collector._update_azure_cloud_links(
            cloud_metadata,
            cluster_name="mycluster",
            is_ha=True,
        )

        assert len(result) == 1
        assert result[0].image_id == "image-123"
        assert result[0].instance_type == "Standard_D4s_v3"
        assert result[0].region == "eastus"
        assert result[0].fault_domain == "0"
        assert result[0].update_domain == "1"
        assert result[0].offer == "netapp-ontap-cloud"
        assert result[0].resource_group_link == "https://rg-link.com"


class TestLogMissingFields:
    """Tests for MISSING_FIELD error logging."""

    @pytest.fixture
    def collector(self) -> MetadataCollector:
        """Create a collector with cluster name set for log prefix."""
        c = MetadataCollector()
        c._cluster_name = "testcluster"
        return c

    def test_logs_missing_field(
        self, collector: MetadataCollector, caplog: pytest.LogCaptureFixture
    ) -> None:
        """Test that absent keys produce MISSING_FIELD log entries at error level."""
        record: dict[str, Any] = {"name": "vol1", "uuid": "abc-123"}
        with caplog.at_level(logging.ERROR):
            collector._log_missing_fields(
                record, ["name", "uuid", "autosize", "tiering"], "Volume", "vol1"
            )
        missing_messages = [r.message for r in caplog.records if "MISSING_FIELD" in r.message]
        assert len(missing_messages) == 2
        assert any("'autosize'" in m for m in missing_messages)
        assert any("'tiering'" in m for m in missing_messages)
        # Verify error level
        for rec in caplog.records:
            if "MISSING_FIELD" in rec.message:
                assert rec.levelno == logging.ERROR

    def test_no_log_for_present_fields(
        self, collector: MetadataCollector, caplog: pytest.LogCaptureFixture
    ) -> None:
        """Test that present keys do NOT produce log entries, even if values are empty/null."""
        record: dict[str, Any] = {
            "name": "",
            "uuid": None,
            "autosize": {},
            "size": 0,
            "enabled": False,
        }
        with caplog.at_level(logging.ERROR):
            collector._log_missing_fields(
                record,
                ["name", "uuid", "autosize", "size", "enabled"],
                "Volume",
                "testvol",
            )
        missing_messages = [r.message for r in caplog.records if "MISSING_FIELD" in r.message]
        assert len(missing_messages) == 0

    def test_log_includes_cluster_context(
        self, collector: MetadataCollector, caplog: pytest.LogCaptureFixture
    ) -> None:
        """Test that log messages include cluster name in prefix."""
        record: dict[str, Any] = {"name": "vol1"}
        with caplog.at_level(logging.ERROR):
            collector._log_missing_fields(record, ["autosize"], "Volume", "vol1")
        missing_messages = [r.message for r in caplog.records if "MISSING_FIELD" in r.message]
        assert len(missing_messages) == 1
        assert "[testcluster:collector]" in missing_messages[0]

    def test_log_includes_record_type_and_id(
        self, collector: MetadataCollector, caplog: pytest.LogCaptureFixture
    ) -> None:
        """Test that log messages include record type and identifier."""
        record: dict[str, Any] = {}
        with caplog.at_level(logging.ERROR):
            collector._log_missing_fields(record, ["uuid"], "Aggregate", "aggr1")
        missing_messages = [r.message for r in caplog.records if "MISSING_FIELD" in r.message]
        assert len(missing_messages) == 1
        assert "Aggregate" in missing_messages[0]
        assert "'aggr1'" in missing_messages[0]
        assert "'uuid'" in missing_messages[0]

    def test_log_missing_field_in_volume_parsing(self, caplog: pytest.LogCaptureFixture) -> None:
        """Test that volume parsing logs missing fields from real API responses."""
        api_client = MagicMock()
        collector = MetadataCollector(api_client=api_client)
        collector._cluster_name = "testcluster"

        # Simulate a response missing autosize, nas, files, tiering
        response: dict[str, Any] = {
            "records": [
                {
                    "uuid": "vol-uuid-1",
                    "name": "vol1",
                    "svm": {"name": "svm1"},
                    "state": "online",
                    "type": "rw",
                    "style": "flexvol",
                    "size": 1099511627776,
                    "aggregates": [{"name": "aggr1"}],
                    "snapshot_policy": {"name": "default"},
                }
            ]
        }
        with caplog.at_level(logging.ERROR):
            collector._parse_volumes_response(response)
        missing_messages = [r.message for r in caplog.records if "MISSING_FIELD" in r.message]
        missing_fields = {m.split("'")[-2] for m in missing_messages}
        assert "autosize" in missing_fields
        assert "nas" in missing_fields
        assert "files" in missing_fields
        assert "tiering" in missing_fields

    def test_no_missing_field_log_for_complete_volume(
        self, caplog: pytest.LogCaptureFixture
    ) -> None:
        """Test that a complete volume record produces no MISSING_FIELD logs."""
        api_client = MagicMock()
        collector = MetadataCollector(api_client=api_client)
        collector._cluster_name = "testcluster"

        response: dict[str, Any] = {
            "records": [
                {
                    "uuid": "vol-uuid-1",
                    "name": "vol1",
                    "svm": {"name": "svm1"},
                    "state": "online",
                    "type": "rw",
                    "style": "flexvol",
                    "size": 1099511627776,
                    "autosize": {"mode": "grow", "grow_threshold": 85},
                    "tiering": {"policy": "auto"},
                    "nas": {
                        "export_policy": {"name": "default"},
                        "path": "/vol1",
                        "security_style": "unix",
                    },
                    "files": {"maximum": 100000},
                    "snapshot_policy": {"name": "default"},
                    "aggregates": [{"name": "aggr1"}],
                }
            ]
        }
        with caplog.at_level(logging.ERROR):
            collector._parse_volumes_response(response)
        missing_messages = [r.message for r in caplog.records if "MISSING_FIELD" in r.message]
        assert len(missing_messages) == 0

    def test_missing_field_grepable_tag(
        self, collector: MetadataCollector, caplog: pytest.LogCaptureFixture
    ) -> None:
        """Test that the MISSING_FIELD tag is consistently present for grepping."""
        record: dict[str, Any] = {}
        with caplog.at_level(logging.ERROR):
            collector._log_missing_fields(record, ["field_a", "field_b"], "TestType", "test-id")
        for rec in caplog.records:
            if "MISSING_FIELD" in rec.message:
                assert "MISSING_FIELD:" in rec.message
                assert rec.levelno == logging.ERROR


class TestGrepableLogTags:
    """Tests for grepable error log tags (API_FAILURE, CLI_FAILURE, COLLECTION_ABORTED)."""

    def test_api_failure_tag_on_no_client(self, caplog: pytest.LogCaptureFixture) -> None:
        """Test that API_FAILURE tag is emitted when no API client."""
        from pynetappfoundry.cache.collector import CollectionError

        collector = MetadataCollector()
        with pytest.raises(CollectionError, match="API_FAILURE"):
            collector.collect_nodes()

    def test_api_failure_tag_on_api_error(self, caplog: pytest.LogCaptureFixture) -> None:
        """Test that API_FAILURE tag is logged at error level on API call failure."""
        api_client = MagicMock()
        api_client.get_all_records.side_effect = ConnectionError("Connection refused")

        collector = MetadataCollector(api_client=api_client)
        collector._cluster_name = "testcluster"
        with caplog.at_level(logging.ERROR), pytest.raises(ConnectionError):
            collector.collect_nodes()
        api_failure_msgs = [r for r in caplog.records if "API_FAILURE" in r.message]
        assert len(api_failure_msgs) >= 1
        assert api_failure_msgs[0].levelno == logging.ERROR
        assert "Nodes" in api_failure_msgs[0].message
        assert "ConnectionError" in api_failure_msgs[0].message

    def test_cli_failure_tag_on_cloud_metadata_error(
        self, caplog: pytest.LogCaptureFixture
    ) -> None:
        """Test that CLI_FAILURE tag is logged at error level on cloud metadata failure."""
        cli_client = MagicMock()
        cli_client.run_command.side_effect = Exception("SSH timeout")

        collector = MetadataCollector(cli_client=cli_client)
        collector._cluster_name = "testcluster"
        with caplog.at_level(logging.ERROR):
            result = collector.collect_cloud_metadata()
        assert result == []
        cli_failure_msgs = [r for r in caplog.records if "CLI_FAILURE" in r.message]
        assert len(cli_failure_msgs) == 1
        assert cli_failure_msgs[0].levelno == logging.ERROR
        assert "Cloud metadata" in cli_failure_msgs[0].message

    def test_collection_aborted_tag_sequential(self, caplog: pytest.LogCaptureFixture) -> None:
        """Test that COLLECTION_ABORTED is logged when sequential collection fails."""
        from pynetappfoundry.cache.collector import CollectionError

        collector = MetadataCollector(parallel=False)
        collector._cluster_name = "testcluster"
        with caplog.at_level(logging.ERROR), pytest.raises((CollectionError, Exception)):
            collector.collect_all("testcluster")
        aborted_msgs = [r for r in caplog.records if "COLLECTION_ABORTED" in r.message]
        assert len(aborted_msgs) >= 1
        assert aborted_msgs[0].levelno == logging.ERROR

    def test_collection_aborted_tag_parallel(self, caplog: pytest.LogCaptureFixture) -> None:
        """Test that COLLECTION_ABORTED is logged when parallel collection fails."""
        from pynetappfoundry.cache.collector import CollectionError

        collector = MetadataCollector(parallel=True)
        collector._cluster_name = "testcluster"
        with caplog.at_level(logging.ERROR), pytest.raises(CollectionError):
            collector.collect_all("testcluster")
        aborted_msgs = [r for r in caplog.records if "COLLECTION_ABORTED" in r.message]
        assert len(aborted_msgs) >= 1
        assert aborted_msgs[0].levelno == logging.ERROR
