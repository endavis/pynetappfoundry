"""Tests for metadata collector."""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock

import pytest

from pynetappfoundry.cache.collector import (
    CollectionPhase,
    MetadataCollector,
    ProgressInfo,
)
from pynetappfoundry.cache.models import (
    HAInfo,
    LicenseInfo,
    NetworkInfo,
    RelationshipsInfo,
    StorageInfo,
)


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
            },
        }

    @pytest.fixture
    def mock_cluster_cli_output(self) -> dict[str, dict[str, str]]:
        """Mock CLI output for cluster identity show."""
        return {
            "mycluster": {
                "Cluster": "mycluster",
                "Cluster UUID": "abc-123-def-456",
            }
        }

    def test_collect_cluster_info_via_api(self, mock_cluster_api_response: dict[str, Any]) -> None:
        """Test collecting cluster info via API."""
        api_client = MagicMock()
        api_client.call_endpoint.return_value = mock_cluster_api_response

        collector = MetadataCollector(api_client=api_client)
        result = collector.collect_cluster_info()

        assert result.cluster_name == "mycluster"
        assert result.cluster_uuid == "abc-123-def-456"
        assert "9.14.1" in result.ontap_version
        api_client.call_endpoint.assert_called_with("/cluster?fields=*", method="GET")

    def test_collect_cluster_info_fallback_to_cli(
        self, mock_cluster_cli_output: dict[str, dict[str, str]]
    ) -> None:
        """Test cluster info falls back to CLI when API fails."""
        api_client = MagicMock()
        api_client.call_endpoint.side_effect = Exception("API unavailable")

        cli_client = MagicMock()
        cli_client.run_command_and_parse.return_value = mock_cluster_cli_output

        collector = MetadataCollector(api_client=api_client, cli_client=cli_client)
        result = collector.collect_cluster_info()

        assert result.cluster_name == "mycluster"
        assert result.cluster_uuid == "abc-123-def-456"
        cli_client.run_command_and_parse.assert_called()

    def test_collect_cluster_info_no_clients(self) -> None:
        """Test cluster info returns empty when no clients."""
        collector = MetadataCollector()
        result = collector.collect_cluster_info()

        assert result.cluster_name == ""
        assert result.cluster_uuid == ""


class TestNodesCollection:
    """Tests for node collection."""

    @pytest.fixture
    def mock_nodes_api_response(self) -> dict[str, Any]:
        """Mock API response for /cluster/nodes endpoint."""
        return {
            "records": [
                {
                    "name": "node1",
                    "serial_number": "123456",
                    "system_id": "0123456789",
                    "model": "SIMULATED",
                    "uptime": 86400,
                    "membership": {"epsilon": True},
                },
                {
                    "name": "node2",
                    "serial_number": "789012",
                    "system_id": "9876543210",
                    "model": "SIMULATED",
                    "uptime": 86400,
                    "membership": {"epsilon": False},
                },
            ]
        }

    def test_collect_nodes_via_api(self, mock_nodes_api_response: dict[str, Any]) -> None:
        """Test collecting nodes via API."""
        api_client = MagicMock()
        api_client.call_endpoint.return_value = mock_nodes_api_response

        collector = MetadataCollector(api_client=api_client)
        result = collector.collect_nodes()

        assert len(result) == 2
        assert result[0].name == "node1"
        assert result[0].serial_number == "123456"
        assert result[0].is_epsilon is True
        assert result[1].name == "node2"
        assert result[1].is_epsilon is False

    def test_collect_nodes_no_clients(self) -> None:
        """Test nodes returns empty list when no clients."""
        collector = MetadataCollector()
        result = collector.collect_nodes()

        assert result == []


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
        }

    def test_collect_network_via_api(
        self, mock_network_api_responses: dict[str, dict[str, Any]]
    ) -> None:
        """Test collecting network info via API."""
        api_client = MagicMock()
        api_client.call_endpoint.side_effect = lambda endpoint, **_: mock_network_api_responses.get(
            endpoint, {}
        )

        collector = MetadataCollector(api_client=api_client)
        result = collector.collect_network()

        assert len(result.data_lifs) == 1
        assert result.data_lifs[0].name == "data_lif1"
        assert len(result.broadcast_domains) == 1
        assert result.broadcast_domains[0].name == "Default"
        assert "Default" in result.ipspaces

    def test_collect_network_no_clients(self) -> None:
        """Test network returns empty when no clients."""
        collector = MetadataCollector()
        result = collector.collect_network()

        assert isinstance(result, NetworkInfo)
        assert result.data_lifs == []


class TestStorageCollection:
    """Tests for storage collection."""

    @pytest.fixture
    def mock_storage_api_responses(self) -> dict[str, dict[str, Any]]:
        """Mock API responses for storage endpoints."""
        return {
            "/storage/aggregates?fields=*": {
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
        }

    def test_collect_storage_via_api(
        self, mock_storage_api_responses: dict[str, dict[str, Any]]
    ) -> None:
        """Test collecting storage info via API."""
        api_client = MagicMock()
        api_client.call_endpoint.side_effect = lambda endpoint, **_: mock_storage_api_responses.get(
            endpoint, {}
        )

        collector = MetadataCollector(api_client=api_client)
        result = collector.collect_storage()

        assert len(result.aggregates) == 1
        assert result.aggregates[0].name == "aggr1"
        assert result.aggregates[0].type == "ssd"
        assert len(result.svms) == 1
        assert result.svms[0].name == "svm1"

    def test_collect_storage_no_clients(self) -> None:
        """Test storage returns empty when no clients."""
        collector = MetadataCollector()
        result = collector.collect_storage()

        assert isinstance(result, StorageInfo)
        assert result.aggregates == []


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
        api_client.call_endpoint.return_value = mock_licenses_api_response

        collector = MetadataCollector(api_client=api_client)
        result = collector.collect_licenses()

        assert len(result.feature_licenses) == 2
        assert result.feature_licenses[0].name == "NFS"
        assert len(result.capacity_licenses) == 1
        assert result.capacity_licenses[0].name == "Cloud Volumes ONTAP"

    def test_collect_licenses_no_clients(self) -> None:
        """Test licenses returns empty when no clients."""
        collector = MetadataCollector()
        result = collector.collect_licenses()

        assert isinstance(result, LicenseInfo)
        assert result.feature_licenses == []


class TestHAInfoCollection:
    """Tests for HA info collection."""

    def test_collect_ha_info_single_node(self) -> None:
        """Test HA info for single-node cluster."""
        api_client = MagicMock()
        api_client.call_endpoint.side_effect = [
            {"records": [{"name": "node1"}]},  # /cluster/nodes
            {"records": []},  # /cluster/mediators
        ]

        collector = MetadataCollector(api_client=api_client)
        result = collector.collect_ha_info()

        assert result.is_ha is False

    def test_collect_ha_info_ha_pair(self) -> None:
        """Test HA info for HA pair."""
        api_client = MagicMock()
        api_client.call_endpoint.side_effect = [
            {"records": [{"name": "node1"}, {"name": "node2"}]},  # /cluster/nodes
            {"records": [{"ip_address": "10.0.0.100", "reachable": True}]},  # /cluster/mediators
        ]

        collector = MetadataCollector(api_client=api_client)
        result = collector.collect_ha_info()

        assert result.is_ha is True
        assert result.mediator_address == "10.0.0.100"

    def test_collect_ha_info_no_clients(self) -> None:
        """Test HA info returns defaults when no clients."""
        collector = MetadataCollector()
        result = collector.collect_ha_info()

        assert isinstance(result, HAInfo)
        assert result.is_ha is False


class TestRelationshipsCollection:
    """Tests for relationships collection."""

    @pytest.fixture
    def mock_relationships_api_responses(self) -> dict[str, dict[str, Any]]:
        """Mock API responses for relationship endpoints."""
        return {
            "/snapmirror/relationships?fields=*": {
                "records": [
                    {
                        "source": {"svm": {"name": "svm1"}, "path": "vol1"},
                        "destination": {"svm": {"name": "svm2"}, "path": "vol1_dp"},
                        "policy": {"type": "async"},
                        "state": "snapmirrored",
                        "healthy": True,
                        "lag_time": "PT5M",
                    }
                ]
            },
            "/cluster/peers?fields=*": {
                "records": [
                    {
                        "name": "peer1",
                        "uuid": "abc-123",
                        "remote": {"name": "remote-cluster"},
                        "peer_applications": [{"address": "10.0.1.1"}],
                        "authentication": {"state": "ok"},
                        "status": {"state": "available"},
                    }
                ]
            },
        }

    def test_collect_relationships_via_api(
        self, mock_relationships_api_responses: dict[str, dict[str, Any]]
    ) -> None:
        """Test collecting relationships via API."""
        api_client = MagicMock()
        api_client.call_endpoint.side_effect = (
            lambda endpoint, **_: mock_relationships_api_responses.get(endpoint, {})
        )

        collector = MetadataCollector(api_client=api_client)
        result = collector.collect_relationships()

        assert len(result.snapmirror_destinations) == 1
        assert result.snapmirror_destinations[0].source_path == "svm1:vol1"
        assert len(result.cluster_peers) == 1
        assert result.cluster_peers[0].remote_cluster_name == "remote-cluster"

    def test_collect_relationships_no_clients(self) -> None:
        """Test relationships returns empty when no clients."""
        collector = MetadataCollector()
        result = collector.collect_relationships()

        assert isinstance(result, RelationshipsInfo)
        assert result.snapmirror_destinations == []


class TestCollectAll:
    """Tests for collect_all method."""

    def test_collect_all_returns_complete_metadata(self) -> None:
        """Test collect_all returns CachedClusterMetadata."""
        api_client = MagicMock()
        api_client.call_endpoint.return_value = {"records": []}

        cli_client = MagicMock()
        cli_client.run_command.return_value = []
        cli_client.run_command_and_parse.return_value = {}

        collector = MetadataCollector(api_client=api_client, cli_client=cli_client)
        result = collector.collect_all("test-cluster")

        assert result.cluster_name == "test-cluster"
        assert result.cached_at is not None
        assert result.cache_version == "1.1"


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
        api_client.call_endpoint.return_value = {"records": []}

        cli_client = MagicMock()
        cli_client.run_command.return_value = []
        cli_client.run_command_and_parse.return_value = {}

        callback = MagicMock()
        collector = MetadataCollector(
            api_client=api_client, cli_client=cli_client, progress_callback=callback
        )
        collector.collect_all("test-cluster")

        # Should have 8 phases * 2 calls (starting + completed) = 16 calls
        assert callback.call_count == 16

        # Verify callback was called with ProgressInfo objects
        for call in callback.call_args_list:
            info = call[0][0]
            assert isinstance(info, ProgressInfo)
            assert isinstance(info.phase, CollectionPhase)
            assert info.status in ("starting", "completed", "failed")

    def test_progress_callback_receives_correct_phases(self) -> None:
        """Test that progress callback receives all expected phases."""
        api_client = MagicMock()
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
            CollectionPhase.HA,
            CollectionPhase.RELATIONSHIPS,
        ]
        assert received_phases == expected_phases

    def test_progress_callback_elapsed_time(self) -> None:
        """Test that progress callback receives elapsed time on completion."""
        api_client = MagicMock()
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

        # Should have 8 elapsed times (one per completed phase)
        assert len(elapsed_times) == 8
        # All should be non-negative
        for elapsed in elapsed_times:
            assert elapsed >= 0

    def test_progress_callback_source_tracking(self) -> None:
        """Test that progress callback receives correct source information."""
        api_client = MagicMock()
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
        assert CollectionPhase.HA.value == "ha"
        assert CollectionPhase.RELATIONSHIPS.value == "relationships"
