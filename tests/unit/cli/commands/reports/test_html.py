"""Tests for HTML report generation."""

from __future__ import annotations

from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from pynetappfoundry.cli.commands.reports.html import (
    CSS_STYLES,
    JS_SCRIPT,
    ClusterData,
    HTMLReportBuilder,
)


@pytest.fixture
def mock_config() -> MagicMock:
    """Create a mock Config object."""
    config = MagicMock()
    config.data = {
        "azure": {
            "test-subscription": {"id": "sub-12345-67890"},
        },
        "aiqums": {},
        "connectors": {},
        "cloudinsights": {},
    }
    config.output_dir = Path("/tmp/test-output")
    config.count.return_value = 0
    config.find_closest.return_value = None
    config.get_user.return_value = ("admin", "password123")
    return config


@pytest.fixture
def sample_cluster_config() -> dict[str, dict[str, Any]]:
    """Sample cluster configuration for testing."""
    return {
        "test-cluster-1": {
            "name": "test-cluster-1",
            "ip": "10.0.0.1",
            "div": "Engineering",
            "bu": "Platform",
            "app": "MyApp",
            "env": "Prod",
            "subapp": "",
            "cloud": "azure",
            "region": "eastus",
            "tags": ["active"],
        },
    }


@pytest.fixture
def sample_cluster_config_multi() -> dict[str, dict[str, Any]]:
    """Sample cluster configuration with multiple clusters."""
    return {
        "test-cluster-1": {
            "name": "test-cluster-1",
            "ip": "10.0.0.1",
            "div": "Engineering",
            "bu": "Platform",
            "app": "App1",
            "env": "Prod",
            "subapp": "",
            "cloud": "azure",
            "region": "eastus",
            "tags": ["active"],
        },
        "test-cluster-2": {
            "name": "test-cluster-2",
            "ip": "10.0.0.2",
            "div": "Engineering",
            "bu": "Platform",
            "app": "App2",
            "env": "Dev",
            "subapp": "",
            "cloud": "azure",
            "region": "westus",
            "tags": [],
        },
        "test-cluster-3": {
            "name": "test-cluster-3",
            "ip": "10.0.0.3",
            "div": "Finance",
            "bu": "Accounting",
            "app": "",
            "env": "Prod",
            "subapp": "",
            "cloud": "aws",
            "region": "us-east-1",
            "tags": [],
        },
    }


@pytest.fixture
def mock_ontap_data() -> dict[str, Any]:
    """Mock data returned from ONTAP cluster."""
    return {
        "cluster": {
            "name": "test-cluster-1",
            "version": {"full": "9.12.1"},
            "management_interfaces": [{"ip": {"address": "10.0.0.1"}}],
            "dns_domains": ["example.com"],
            "name_servers": ["8.8.8.8", "8.8.4.4"],
            "ntp_servers": ["time.example.com"],
        },
        "nodes": {
            "test-cluster-1-01": {
                "name": "test-cluster-1-01",
                "serial_number": "SN123456",
                "management_interfaces": [{"ip": {"address": "10.0.0.11"}}],
            },
            "test-cluster-1-02": {
                "name": "test-cluster-1-02",
                "serial_number": "SN123457",
                "management_interfaces": [{"ip": {"address": "10.0.0.12"}}],
            },
        },
        "svms": {
            "svm1": {
                "name": "svm1",
                "state": "running",
                "ip_interfaces": [{"name": "lif1"}],
                "dns": {"domains": ["example.com"], "servers": ["8.8.8.8"]},
                "cifs": {"name": "cifs1"},
            },
        },
        "interfaces": {
            "lif1": {
                "name": "lif1",
                "ip": {"address": "10.0.0.100", "netmask": "24"},
                "location": {"home_node": {"name": "test-cluster-1-01"}},
            },
        },
        "cifs": {
            "cifs1": {
                "name": "cifs1",
                "enabled": True,
                "ad_domain": {"fqdn": "ad.example.com", "organizational_unit": "OU=Servers"},
                "security": {
                    "smb_signing": True,
                    "use_start_tls": False,
                    "lm_compatibility_level": "ntlm_ntlmv2_krb",
                    "smb_encryption": False,
                    "session_security": "none",
                    "ldap_referral_enabled": True,
                    "use_ldaps": False,
                    "encrypt_dc_connection": False,
                    "aes_netlogon_enabled": True,
                    "try_ldap_channel_binding": True,
                    "advertised_kdc_encryptions": ["aes128", "aes256"],
                },
            },
        },
    }


class TestHTMLReportBuilder:
    """Tests for HTMLReportBuilder class."""

    @patch("pynetappfoundry.cli.commands.reports.html.ClusterData")
    def test_init_creates_hierarchy(
        self,
        mock_cluster_data: MagicMock,
        mock_config: MagicMock,
        sample_cluster_config: dict[str, dict[str, Any]],
    ) -> None:
        """Test that initialization creates cluster hierarchy."""
        mock_cluster = MagicMock()
        mock_cluster.name = "test-cluster-1"
        mock_cluster.div = "Engineering"
        mock_cluster.bu = "Platform"
        mock_cluster.app = "MyApp"
        mock_cluster.env = "Prod"
        mock_cluster.subapp = ""
        mock_cluster.cloud = "azure"
        mock_cluster.region = "eastus"
        mock_cluster.ele_class = ""
        mock_cluster.fetched_data = {"nodes": {"node1": {}}}
        mock_cluster_data.return_value = mock_cluster

        builder = HTMLReportBuilder("Test Report", sample_cluster_config, mock_config)

        assert "Engineering" in builder.divisions
        assert "Platform" in builder.divisions["Engineering"]
        assert builder.counts["sn"] == 1  # Single node cluster

    @patch("pynetappfoundry.cli.commands.reports.html.ClusterData")
    def test_counts_ha_clusters(
        self,
        mock_cluster_data: MagicMock,
        mock_config: MagicMock,
        sample_cluster_config: dict[str, dict[str, Any]],
    ) -> None:
        """Test that HA clusters are counted correctly."""
        mock_cluster = MagicMock()
        mock_cluster.name = "test-cluster-1"
        mock_cluster.div = "Engineering"
        mock_cluster.bu = "Platform"
        mock_cluster.app = "MyApp"
        mock_cluster.env = "Prod"
        mock_cluster.subapp = ""
        mock_cluster.cloud = "azure"
        mock_cluster.region = "eastus"
        mock_cluster.ele_class = ""
        mock_cluster.fetched_data = {"nodes": {"node1": {}, "node2": {}}}  # HA pair
        mock_cluster_data.return_value = mock_cluster

        builder = HTMLReportBuilder("Test Report", sample_cluster_config, mock_config)

        assert builder.counts["ha"] == 1
        assert builder.counts["sn"] == 0

    @patch("pynetappfoundry.cli.commands.reports.html.ClusterData")
    def test_generate_html_includes_css(
        self,
        mock_cluster_data: MagicMock,
        mock_config: MagicMock,
        sample_cluster_config: dict[str, dict[str, Any]],
    ) -> None:
        """Test that generated HTML includes CSS styles."""
        mock_cluster = MagicMock()
        mock_cluster.name = "test-cluster-1"
        mock_cluster.div = "Engineering"
        mock_cluster.bu = "Platform"
        mock_cluster.app = "MyApp"
        mock_cluster.env = "Prod"
        mock_cluster.subapp = ""
        mock_cluster.cloud = "azure"
        mock_cluster.region = "eastus"
        mock_cluster.ele_class = ""
        mock_cluster.fetched_data = {"nodes": {"node1": {}}}
        mock_cluster_data.return_value = mock_cluster

        builder = HTMLReportBuilder("Test Report", sample_cluster_config, mock_config)
        html = builder.generate_html()

        assert ".tree" in html
        assert ".custom-table" in html
        assert ".active" in html

    @patch("pynetappfoundry.cli.commands.reports.html.ClusterData")
    def test_generate_html_includes_javascript(
        self,
        mock_cluster_data: MagicMock,
        mock_config: MagicMock,
        sample_cluster_config: dict[str, dict[str, Any]],
    ) -> None:
        """Test that generated HTML includes JavaScript."""
        mock_cluster = MagicMock()
        mock_cluster.name = "test-cluster-1"
        mock_cluster.div = "Engineering"
        mock_cluster.bu = "Platform"
        mock_cluster.app = "MyApp"
        mock_cluster.env = "Prod"
        mock_cluster.subapp = ""
        mock_cluster.cloud = "azure"
        mock_cluster.region = "eastus"
        mock_cluster.ele_class = ""
        mock_cluster.fetched_data = {"nodes": {"node1": {}}}
        mock_cluster_data.return_value = mock_cluster

        builder = HTMLReportBuilder("Test Report", sample_cluster_config, mock_config)
        html = builder.generate_html()

        assert "openActiveTrees" in html
        assert "openDetailsToButtons" in html

    @patch("pynetappfoundry.cli.commands.reports.html.ClusterData")
    def test_generate_html_has_proper_structure(
        self,
        mock_cluster_data: MagicMock,
        mock_config: MagicMock,
        sample_cluster_config: dict[str, dict[str, Any]],
    ) -> None:
        """Test that generated HTML has proper structure."""
        mock_cluster = MagicMock()
        mock_cluster.name = "test-cluster-1"
        mock_cluster.div = "Engineering"
        mock_cluster.bu = "Platform"
        mock_cluster.app = "MyApp"
        mock_cluster.env = "Prod"
        mock_cluster.subapp = ""
        mock_cluster.cloud = "azure"
        mock_cluster.region = "eastus"
        mock_cluster.ele_class = ""
        mock_cluster.fetched_data = {"nodes": {"node1": {}}}
        mock_cluster_data.return_value = mock_cluster

        builder = HTMLReportBuilder("Test Report", sample_cluster_config, mock_config)
        html = builder.generate_html()

        assert "<!DOCTYPE html>" in html
        assert "<html" in html
        assert "</html>" in html
        assert '<meta charset="utf-8">' in html
        assert '<ul class="tree">' in html
        assert "<details" in html
        assert "<summary>" in html

    def test_format_table_row_text(self, mock_config: MagicMock) -> None:
        """Test format_table_row_text generates correct HTML."""
        with patch("pynetappfoundry.cli.commands.reports.html.ClusterData"):
            builder = HTMLReportBuilder("Test", {}, mock_config)
            builder.format_table_row_text("Label", "Value")

        html = builder.doc.getvalue()
        assert "<tr>" in html
        assert "<td>" in html
        assert "Label" in html
        assert "Value" in html

    def test_format_table_row_text_with_header(self, mock_config: MagicMock) -> None:
        """Test format_table_row_text with header=True."""
        with patch("pynetappfoundry.cli.commands.reports.html.ClusterData"):
            builder = HTMLReportBuilder("Test", {}, mock_config)
            builder.format_table_row_text("Header1", "Header2", header=True)

        html = builder.doc.getvalue()
        assert "<th>" in html

    def test_format_table_row_link(self, mock_config: MagicMock) -> None:
        """Test format_table_row_link generates link correctly."""
        with patch("pynetappfoundry.cli.commands.reports.html.ClusterData"):
            builder = HTMLReportBuilder("Test", {}, mock_config)
            builder.format_table_row_link("Label", "Link Text", "https://example.com")

        html = builder.doc.getvalue()
        assert '<a href="https://example.com">' in html
        assert "Link Text" in html


class TestClusterData:
    """Tests for ClusterData class."""

    def test_ele_class_for_active_cluster(
        self,
        mock_config: MagicMock,
    ) -> None:
        """Test that ele_class is set for active clusters."""
        mock_builder = MagicMock()
        mock_builder.config = mock_config

        with patch.object(ClusterData, "_gather_data"):
            cluster = ClusterData(
                "test-cluster",
                mock_builder,
                div="Div1",
                bu="BU1",
                app="App1",
                env="Prod",
                subapp="",
                tags=["active"],
                ip="10.0.0.1",
            )

        assert cluster.ele_class == "Div1-BU1-App1-Prod"

    def test_ele_class_with_subapp(
        self,
        mock_config: MagicMock,
    ) -> None:
        """Test that ele_class includes subapp when present."""
        mock_builder = MagicMock()
        mock_builder.config = mock_config

        with patch.object(ClusterData, "_gather_data"):
            cluster = ClusterData(
                "test-cluster",
                mock_builder,
                div="Div1",
                bu="BU1",
                app="App1",
                env="Prod",
                subapp="SubApp1",
                tags=["active"],
                ip="10.0.0.1",
            )

        assert cluster.ele_class == "Div1-BU1-App1-Prod-SubApp1"

    def test_ele_class_empty_for_inactive_cluster(
        self,
        mock_config: MagicMock,
    ) -> None:
        """Test that ele_class is empty for inactive clusters."""
        mock_builder = MagicMock()
        mock_builder.config = mock_config

        with patch.object(ClusterData, "_gather_data"):
            cluster = ClusterData(
                "test-cluster",
                mock_builder,
                div="Div1",
                bu="BU1",
                app="App1",
                env="Prod",
                subapp="",
                tags=[],
                ip="10.0.0.1",
            )

        assert cluster.ele_class == ""

    def test_ele_class_sanitizes_special_chars(
        self,
        mock_config: MagicMock,
    ) -> None:
        """Test that ele_class removes & and / characters."""
        mock_builder = MagicMock()
        mock_builder.config = mock_config

        with patch.object(ClusterData, "_gather_data"):
            cluster = ClusterData(
                "test-cluster",
                mock_builder,
                div="Div&1",
                bu="BU/1",
                app="App&/1",
                env="Prod",
                subapp="",
                tags=["active"],
                ip="10.0.0.1",
            )

        assert "&" not in cluster.ele_class
        assert "/" not in cluster.ele_class

    def test_gather_data_handles_missing_ip(
        self,
        mock_config: MagicMock,
    ) -> None:
        """Test that _gather_data handles missing IP gracefully."""
        mock_builder = MagicMock()
        mock_builder.config = mock_config

        # No IP provided
        cluster = ClusterData(
            "test-cluster",
            mock_builder,
            div="Div1",
            bu="BU1",
            tags=[],
        )

        # Should not raise, should have empty fetched_data
        assert cluster.fetched_data == {}

    def test_gather_data_handles_credential_error(
        self,
        mock_config: MagicMock,
    ) -> None:
        """Test that _gather_data handles credential errors gracefully."""
        mock_builder = MagicMock()
        mock_builder.config = mock_config
        mock_config.get_user.side_effect = Exception("Credential error")

        cluster = ClusterData(
            "test-cluster",
            mock_builder,
            div="Div1",
            bu="BU1",
            ip="10.0.0.1",
            tags=[],
        )

        # Should not raise, should have empty fetched_data
        assert cluster.fetched_data == {}


class TestCSSAndJS:
    """Tests for CSS and JavaScript constants."""

    def test_css_has_tree_styles(self) -> None:
        """Test that CSS includes tree styles."""
        assert ".tree" in CSS_STYLES
        assert "--spacing" in CSS_STYLES
        assert "--radius" in CSS_STYLES

    def test_css_has_table_styles(self) -> None:
        """Test that CSS includes table styles."""
        assert ".custom-table" in CSS_STYLES
        assert ".noborder-table" in CSS_STYLES

    def test_css_has_active_badge_style(self) -> None:
        """Test that CSS includes active badge style."""
        assert ".active" in CSS_STYLES
        assert "background-color: green" in CSS_STYLES

    def test_css_has_error_style(self) -> None:
        """Test that CSS includes error style."""
        assert ".error" in CSS_STYLES
        assert "background-color: red" in CSS_STYLES

    def test_css_has_button_style(self) -> None:
        """Test that CSS includes button style."""
        assert ".env-button" in CSS_STYLES

    def test_js_has_open_active_trees_function(self) -> None:
        """Test that JS includes openActiveTrees function."""
        assert "function openActiveTrees" in JS_SCRIPT

    def test_js_has_open_details_to_buttons_function(self) -> None:
        """Test that JS includes openDetailsToButtons function."""
        assert "function openDetailsToButtons" in JS_SCRIPT

    def test_js_has_button_event_listeners(self) -> None:
        """Test that JS sets up button event listeners."""
        assert "envButtons.forEach" in JS_SCRIPT
        assert "addEventListener" in JS_SCRIPT


class TestAzureIntegration:
    """Tests for Azure portal link generation."""

    def test_format_azure_info(self, mock_config: MagicMock) -> None:
        """Test format_azure_info generates Azure information."""
        with patch("pynetappfoundry.cli.commands.reports.html.ClusterData"):
            builder = HTMLReportBuilder("Test", {}, mock_config)
            builder.format_azure_info(
                {
                    "location": "test-subscription",
                    "resource_group": "rg-test",
                }
            )

        html = builder.doc.getvalue()
        assert "Azure Subscription Name" in html
        assert "Azure Resource Group" in html

    def test_format_azure_info_with_vmname(self, mock_config: MagicMock) -> None:
        """Test format_azure_info includes VM link when vmname present."""
        with patch("pynetappfoundry.cli.commands.reports.html.ClusterData"):
            builder = HTMLReportBuilder("Test", {}, mock_config)
            builder.format_azure_info(
                {
                    "location": "test-subscription",
                    "resource_group": "rg-test",
                    "vmname": "test-vm",
                }
            )

        html = builder.doc.getvalue()
        assert "Azure VM Name" in html
        assert "test-vm" in html


class TestUtilitiesFormatting:
    """Tests for utilities section formatting."""

    def test_format_ci(self, mock_config: MagicMock) -> None:
        """Test format_ci generates Cloud Insights link."""
        with patch("pynetappfoundry.cli.commands.reports.html.ClusterData"):
            builder = HTMLReportBuilder("Test", {}, mock_config)
            builder.format_ci({"url": "https://cloudinsights.example.com"})

        html = builder.doc.getvalue()
        assert "Cloud Insights" in html
        assert "https://cloudinsights.example.com" in html

    def test_format_generic_cloud_item(self, mock_config: MagicMock) -> None:
        """Test format_generic_cloud_item generates item details."""
        with patch("pynetappfoundry.cli.commands.reports.html.ClusterData"):
            builder = HTMLReportBuilder("Test", {}, mock_config)
            builder.format_generic_cloud_item("AIQUM", {"ip": "10.0.0.100"})

        html = builder.doc.getvalue()
        assert "AIQUM" in html
        assert "10.0.0.100" in html
        assert "https://10.0.0.100" in html


class TestHierarchyBuilding:
    """Tests for hierarchy building functionality."""

    @patch("pynetappfoundry.cli.commands.reports.html.ClusterData")
    def test_multiple_divisions(
        self,
        mock_cluster_data: MagicMock,
        mock_config: MagicMock,
        sample_cluster_config_multi: dict[str, dict[str, Any]],
    ) -> None:
        """Test that multiple divisions are organized correctly."""

        def create_mock_cluster(name: str, **kwargs: Any) -> MagicMock:
            mock = MagicMock()
            mock.name = name
            mock.div = kwargs.get("div", "")
            mock.bu = kwargs.get("bu", "")
            mock.app = kwargs.get("app", "")
            mock.env = kwargs.get("env", "")
            mock.subapp = kwargs.get("subapp", "")
            mock.cloud = kwargs.get("cloud", "")
            mock.region = kwargs.get("region", "")
            mock.ele_class = ""
            mock.fetched_data = {"nodes": {"node1": {}}}
            return mock

        mock_cluster_data.side_effect = [
            create_mock_cluster(
                "test-cluster-1",
                div="Engineering",
                bu="Platform",
                app="App1",
                env="Prod",
                cloud="azure",
                region="eastus",
            ),
            create_mock_cluster(
                "test-cluster-2",
                div="Engineering",
                bu="Platform",
                app="App2",
                env="Dev",
                cloud="azure",
                region="westus",
            ),
            create_mock_cluster(
                "test-cluster-3",
                div="Finance",
                bu="Accounting",
                app="",
                env="Prod",
                cloud="aws",
                region="us-east-1",
            ),
        ]

        builder = HTMLReportBuilder("Test", sample_cluster_config_multi, mock_config)

        assert "Engineering" in builder.divisions
        assert "Finance" in builder.divisions
        assert len(builder.divisions) == 2

    @patch("pynetappfoundry.cli.commands.reports.html.ClusterData")
    def test_button_ids_tracked_for_active_clusters(
        self,
        mock_cluster_data: MagicMock,
        mock_config: MagicMock,
    ) -> None:
        """Test that button IDs are tracked for active clusters."""
        mock_cluster = MagicMock()
        mock_cluster.name = "test-cluster"
        mock_cluster.div = "Div"
        mock_cluster.bu = "BU"
        mock_cluster.app = "App"
        mock_cluster.env = "Prod"
        mock_cluster.subapp = ""
        mock_cluster.cloud = "azure"
        mock_cluster.region = "eastus"
        mock_cluster.ele_class = "Div-BU-App-Prod"
        mock_cluster.fetched_data = {"nodes": {"node1": {}}}
        mock_cluster_data.return_value = mock_cluster

        builder = HTMLReportBuilder(
            "Test",
            {"test-cluster": {"name": "test-cluster", "ip": "10.0.0.1"}},
            mock_config,
        )

        assert "Div-BU-App-Prod" in builder.button_ids


class TestHTMLFileGeneration:
    """Tests that generate actual HTML files for visual inspection."""

    @pytest.fixture
    def comprehensive_cluster_configs(self) -> dict[str, dict[str, Any]]:
        """Comprehensive cluster configs with various cloud providers."""
        return {
            "AZURE-PROD-01": {
                "name": "AZURE-PROD-01",
                "ip": "10.0.1.100",
                "div": "Engineering",
                "bu": "Platform",
                "app": "DataServices",
                "env": "Prod",
                "subapp": "",
                "cloud": "azure",
                "region": "eastus",
                "tags": ["active", "cvo", "ha"],
            },
            "AZURE-DEV-01": {
                "name": "AZURE-DEV-01",
                "ip": "10.0.2.100",
                "div": "Engineering",
                "bu": "Platform",
                "app": "DataServices",
                "env": "Dev",
                "subapp": "",
                "cloud": "azure",
                "region": "westus",
                "tags": ["active", "cvo"],
            },
            "AWS-PROD-01": {
                "name": "AWS-PROD-01",
                "ip": "10.1.1.100",
                "div": "Finance",
                "bu": "Treasury",
                "app": "FinanceData",
                "env": "Prod",
                "subapp": "",
                "cloud": "aws",
                "region": "us-east-1",
                "tags": ["active", "cvo", "ha"],
            },
            "GCP-PROD-01": {
                "name": "GCP-PROD-01",
                "ip": "10.2.1.100",
                "div": "Research",
                "bu": "DataScience",
                "app": "MLPipeline",
                "env": "Prod",
                "subapp": "",
                "cloud": "gcp",
                "region": "us-central1",
                "tags": ["active", "cvo"],
            },
            "ONPREM-PROD-01": {
                "name": "ONPREM-PROD-01",
                "ip": "192.168.1.100",
                "div": "Corporate",
                "bu": "Infrastructure",
                "app": "FileServices",
                "env": "Prod",
                "subapp": "",
                "cloud": "onprem",
                "region": "DATACENTER-EAST",
                "tags": ["active", "fas", "nfs", "cifs"],
            },
            "ONPREM-DR-01": {
                "name": "ONPREM-DR-01",
                "ip": "192.168.3.100",
                "div": "Corporate",
                "bu": "Infrastructure",
                "app": "FileServices",
                "env": "DR",
                "subapp": "",
                "cloud": "onprem",
                "region": "DATACENTER-WEST",
                "tags": ["standby", "fas", "dr"],
            },
        }

    @pytest.fixture
    def comprehensive_ontap_data(self) -> dict[str, Any]:
        """Comprehensive mock ONTAP data for realistic HTML output."""
        return {
            "cluster": {
                "name": "test-cluster",
                "version": {"full": "NetApp Release 9.14.1"},
                "management_interfaces": [{"ip": {"address": "10.0.0.1"}}],
                "dns_domains": ["corp.example.com", "example.com"],
                "name_servers": ["10.0.0.10", "10.0.0.11"],
                "ntp_servers": ["time1.example.com", "time2.example.com"],
            },
            "nodes": {
                "cluster-01": {
                    "name": "cluster-01",
                    "serial_number": "SN-ABC123456",
                    "model": "FAS8700",
                    "management_interfaces": [{"ip": {"address": "10.0.0.11"}}],
                },
                "cluster-02": {
                    "name": "cluster-02",
                    "serial_number": "SN-ABC123457",
                    "model": "FAS8700",
                    "management_interfaces": [{"ip": {"address": "10.0.0.12"}}],
                },
            },
            "svms": {
                "svm-data-01": {
                    "name": "svm-data-01",
                    "state": "running",
                    "ip_interfaces": [{"name": "lif-data-01"}, {"name": "lif-data-02"}],
                    "dns": {
                        "domains": ["corp.example.com"],
                        "servers": ["10.0.0.10"],
                    },
                    "cifs": {"name": "CIFS-SVM01"},
                },
                "svm-data-02": {
                    "name": "svm-data-02",
                    "state": "running",
                    "ip_interfaces": [{"name": "lif-data-03"}],
                    "dns": {
                        "domains": ["corp.example.com"],
                        "servers": ["10.0.0.10"],
                    },
                },
            },
            "interfaces": {
                "lif-data-01": {
                    "name": "lif-data-01",
                    "ip": {"address": "10.0.1.100", "netmask": "24"},
                    "location": {"home_node": {"name": "cluster-01"}},
                },
                "lif-data-02": {
                    "name": "lif-data-02",
                    "ip": {"address": "10.0.1.101", "netmask": "24"},
                    "location": {"home_node": {"name": "cluster-02"}},
                },
                "lif-data-03": {
                    "name": "lif-data-03",
                    "ip": {"address": "10.0.2.100", "netmask": "24"},
                    "location": {"home_node": {"name": "cluster-01"}},
                },
            },
            "cifs": {
                "CIFS-SVM01": {
                    "name": "CIFS-SVM01",
                    "enabled": True,
                    "ad_domain": {
                        "fqdn": "ad.corp.example.com",
                        "organizational_unit": "OU=NetApp,OU=Servers,DC=corp,DC=example,DC=com",
                    },
                    "security": {
                        "smb_signing": True,
                        "use_start_tls": False,
                        "lm_compatibility_level": "ntlm_ntlmv2_krb",
                        "smb_encryption": True,
                        "session_security": "seal",
                        "ldap_referral_enabled": True,
                        "use_ldaps": True,
                        "encrypt_dc_connection": True,
                        "aes_netlogon_enabled": True,
                        "try_ldap_channel_binding": True,
                        "advertised_kdc_encryptions": ["aes128", "aes256", "des3"],
                    },
                },
            },
        }

    def test_generate_html_file(
        self,
        mock_config: MagicMock,
        comprehensive_cluster_configs: dict[str, dict[str, Any]],
        comprehensive_ontap_data: dict[str, Any],
        tmp_path: Path,
    ) -> None:
        """Generate an actual HTML file for visual inspection.

        This test creates a complete HTML report that can be opened in a browser
        to verify the visual output and functionality.
        """
        from pynetappfoundry.cli.commands.reports.html import ClusterData

        # Build mock cloud metadata for each cluster
        cloud_data_by_cluster: dict[str, dict[str, str]] = {
            "AZURE-PROD-01": {
                "provider": "Azure",
                "region": "eastus",
                "account_id": "12345678-1234-1234-1234-123456789abc",
                "resource_group_name": "rg-netapp-prod",
                "instance_id": "i-azure123",
                "instance_type": "Standard_DS4_v2",
                "primary_ip": "10.0.1.100",
                "availability_zone": "eastus-1",
            },
            "AZURE-DEV-01": {
                "provider": "Azure",
                "region": "westus",
                "account_id": "12345678-1234-1234-1234-123456789abc",
                "resource_group_name": "rg-netapp-dev",
                "instance_id": "",
                "instance_type": "",
                "primary_ip": "",
                "availability_zone": "",
            },
            "AWS-PROD-01": {
                "provider": "AWS",
                "region": "us-east-1",
                "account_id": "123456789012",
                "resource_group_name": "",
                "instance_id": "i-0abc123def456",
                "instance_type": "m5.xlarge",
                "primary_ip": "10.1.1.100",
                "availability_zone": "us-east-1a",
            },
            "GCP-PROD-01": {
                "provider": "GCP",
                "region": "us-central1",
                "account_id": "my-gcp-project",
                "resource_group_name": "",
                "instance_id": "",
                "instance_type": "n1-standard-4",
                "primary_ip": "",
                "availability_zone": "us-central1-a",
            },
        }

        def _make_mock_entry(cluster_name: str, data: dict[str, Any]) -> MagicMock:
            """Create a mock ClusterEntry with cloud metadata."""
            mock_entry = MagicMock()
            # Make the mock support dict-like access for **entry unpacking
            mock_entry.keys.return_value = data.keys()
            mock_entry.__getitem__ = lambda self, k: data[k]
            mock_entry.__iter__ = lambda self: iter(data)
            mock_entry.__contains__ = lambda self, k: k in data

            if cluster_name in cloud_data_by_cluster:
                cloud_mock = MagicMock()
                cd = cloud_data_by_cluster[cluster_name]
                for field, value in cd.items():
                    setattr(cloud_mock, field, value)
                ontap_mock = MagicMock()
                ontap_mock.cloud = [cloud_mock]
                mock_entry.ontap = ontap_mock
            else:
                mock_entry.ontap = None

            return mock_entry

        # Wrap cluster configs in mock ClusterEntry objects
        wrapped_configs: dict[str, Any] = {}
        for name, data in comprehensive_cluster_configs.items():
            wrapped_configs[name] = _make_mock_entry(name, data)

        # Store original _gather_data
        original_gather_data = ClusterData._gather_data

        # Mock _gather_data to populate fetched_data without calling ONTAP
        def mock_gather_data(cluster_self: Any) -> None:
            cluster_self._build_cloud_info()
            # Use different data based on cluster name for variety
            if "ONPREM" in cluster_self.name or "DR" in cluster_self.name:
                cluster_self.fetched_data = comprehensive_ontap_data.copy()
                cluster_self.cluster_type = "HA"
            elif "DEV" in cluster_self.name:
                cluster_self.fetched_data = {
                    "cluster": comprehensive_ontap_data["cluster"].copy(),
                    "nodes": {"dev-node-01": comprehensive_ontap_data["nodes"]["cluster-01"]},
                    "svms": {"svm-dev": comprehensive_ontap_data["svms"]["svm-data-02"]},
                    "interfaces": {
                        "lif-dev": comprehensive_ontap_data["interfaces"]["lif-data-01"]
                    },
                    "cifs": {},
                }
                cluster_self.cluster_type = "SN"
            else:
                cluster_self.fetched_data = comprehensive_ontap_data.copy()
                cluster_self.cluster_type = "HA"

        # Monkey-patch the method
        ClusterData._gather_data = mock_gather_data  # type: ignore[method-assign]

        try:
            builder = HTMLReportBuilder(
                "NetApp Infrastructure Report",
                wrapped_configs,
                mock_config,
            )
            html_content = builder.generate_html()

            # Write to tmp_path for inspection
            output_file = tmp_path / "test_report.html"
            output_file.write_text(html_content)

            # Also write to a known location for easy access during development
            import tempfile

            dev_output = Path(tempfile.gettempdir()) / "test_html_report.html"
            dev_output.write_text(html_content)

            # Verify the HTML contains expected elements
            assert "<!DOCTYPE html>" in html_content
            assert "NetApp Cluster Report" in html_content

            # Verify all divisions are present
            assert "Engineering" in html_content
            assert "Finance" in html_content
            assert "Research" in html_content
            assert "Corporate" in html_content

            # Verify cloud providers are shown
            assert "Azure Information" in html_content
            assert "AWS Information" in html_content
            assert "GCP Information" in html_content

            # Verify Azure-specific fields
            assert "Subscription ID" in html_content
            assert "Resource Group" in html_content
            assert "12345678-1234-1234-1234-123456789abc" in html_content

            # Verify cluster data
            assert "AZURE-PROD-01" in html_content
            assert "AWS-PROD-01" in html_content
            assert "ONPREM-PROD-01" in html_content

            # Verify ONTAP data
            assert "NetApp Release 9.14.1" in html_content
            assert "svm-data-01" in html_content

            # Verify active cluster buttons
            assert "Go to Active Cluster(s)" in html_content

            # Verify CSS and JS included
            assert ".tree" in html_content
            assert "openActiveTrees" in html_content

            print(f"\nHTML report generated at: {dev_output}")
            print("Open this file in a browser to visually inspect the output.")
        finally:
            # Restore original method
            ClusterData._gather_data = original_gather_data  # type: ignore[method-assign]
