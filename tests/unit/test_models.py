"""Tests for Pydantic configuration models."""

from __future__ import annotations

import pytest

from pynetappfoundry.core.models import (
    AIQUMConfig,
    AzureConfig,
    BaseResource,
    CloudInsightsConfig,
    ClusterConfig,
    ConnectorConfig,
    DIIAPISettings,
    LicensingSettings,
    ONTAPAPISettings,
    SearchableKeysConfig,
    SMTPSettings,
    UserCredentials,
)


class TestBaseResource:
    """Tests for BaseResource model."""

    def test_default_values(self) -> None:
        """Test that all fields have empty string defaults."""
        resource = BaseResource()
        assert resource.name == ""
        assert resource.ip == ""
        assert resource.div == ""
        assert resource.bu == ""
        assert resource.env == ""

    def test_with_values(self) -> None:
        """Test creating resource with values."""
        resource = BaseResource(
            name="test-resource",
            ip="192.168.1.1",
            div="ITS",
            bu="LAR",
            env="Prod",
        )
        assert resource.name == "test-resource"
        assert resource.ip == "192.168.1.1"
        assert resource.div == "ITS"
        assert resource.bu == "LAR"
        assert resource.env == "Prod"

    def test_extra_fields_allowed(self) -> None:
        """Test that extra fields are allowed."""
        resource = BaseResource(
            name="test",
            custom_field="custom_value",
        )
        assert resource.name == "test"
        assert resource.custom_field == "custom_value"  # type: ignore[attr-defined]


class TestClusterConfig:
    """Tests for ClusterConfig model."""

    def test_default_values(self) -> None:
        """Test default values for cluster config."""
        cluster = ClusterConfig()
        assert cluster.app == ""
        assert cluster.subapp == ""
        assert cluster.tags == []
        assert cluster.region == ""
        assert cluster.cloud == ""
        assert cluster.user is None
        assert cluster.enc is None

    def test_full_cluster_config(self) -> None:
        """Test creating a full cluster config."""
        cluster = ClusterConfig(
            name="CLUSTER-PROD-01",
            ip="192.168.1.173",
            div="ITS",
            bu="LAR",
            app="Storage",
            env="Prod",
            subapp="PD1",
            tags=["active", "nfs"],
            region="USCU",
        )
        assert cluster.name == "CLUSTER-PROD-01"
        assert cluster.ip == "192.168.1.173"
        assert cluster.tags == ["active", "nfs"]
        assert cluster.region == "USCU"

    def test_cluster_with_credentials(self) -> None:
        """Test cluster with per-cluster credentials."""
        cluster = ClusterConfig(
            name="CLUSTER-01",
            ip="10.0.0.1",
            user="admin",
            enc="encrypted_password",
        )
        assert cluster.user == "admin"
        assert cluster.enc == "encrypted_password"

    def test_from_toml_dict(self) -> None:
        """Test creating cluster from TOML-style dict."""
        toml_data = {
            "ip": "192.168.1.173",
            "div": "ITS",
            "bu": "LAR",
            "app": "Storage",
            "env": "PD",
            "subapp": "PD1",
            "tags": ["active", "nfs"],
            "region": "USCU",
        }
        cluster = ClusterConfig(**toml_data)
        cluster.name = "CLUSTER-PROD-01"  # Set from TOML key

        assert cluster.name == "CLUSTER-PROD-01"
        assert cluster.ip == "192.168.1.173"
        assert cluster.tags == ["active", "nfs"]


class TestAIQUMConfig:
    """Tests for AIQUMConfig model."""

    def test_inherits_base_resource(self) -> None:
        """Test that AIQUMConfig inherits from BaseResource."""
        aiqum = AIQUMConfig(
            name="AIQUM-Prod",
            ip="192.168.1.150",
            div="ITS",
            bu="LAR",
            env="Prod",
        )
        assert aiqum.name == "AIQUM-Prod"
        assert aiqum.ip == "192.168.1.150"


class TestConnectorConfig:
    """Tests for ConnectorConfig model."""

    def test_inherits_base_resource(self) -> None:
        """Test that ConnectorConfig inherits from BaseResource."""
        connector = ConnectorConfig(
            name="CONNECTOR-PROD-01",
            ip="192.168.1.132",
            div="ITS",
            bu="LAR",
            env="Prod",
        )
        assert connector.name == "CONNECTOR-PROD-01"
        assert connector.ip == "192.168.1.132"


class TestCloudInsightsConfig:
    """Tests for CloudInsightsConfig model."""

    def test_inherits_base_resource(self) -> None:
        """Test that CloudInsightsConfig inherits from BaseResource."""
        ci = CloudInsightsConfig(
            name="CI-Tenant-01",
            env="Prod",
        )
        assert ci.name == "CI-Tenant-01"


class TestAzureConfig:
    """Tests for AzureConfig model."""

    def test_azure_specific_fields(self) -> None:
        """Test Azure-specific fields."""
        azure = AzureConfig(
            name="Azure-Prod",
            subscription_id="sub-123",
            resource_group="rg-storage",
        )
        assert azure.subscription_id == "sub-123"
        assert azure.resource_group == "rg-storage"


class TestUserCredentials:
    """Tests for UserCredentials model."""

    def test_required_fields(self) -> None:
        """Test that user and enc are required."""
        creds = UserCredentials(user="admin", enc="encrypted_pass")
        assert creds.user == "admin"
        assert creds.enc == "encrypted_pass"

    def test_missing_required_field_raises(self) -> None:
        """Test that missing required fields raise ValidationError."""
        from pydantic import ValidationError

        with pytest.raises(ValidationError):
            UserCredentials(user="admin")  # type: ignore[call-arg]


class TestSMTPSettings:
    """Tests for SMTPSettings model."""

    def test_default_values(self) -> None:
        """Test SMTP default values."""
        smtp = SMTPSettings(server="smtp.example.com")
        assert smtp.server == "smtp.example.com"
        assert smtp.user == ""
        assert smtp.password == ""
        assert smtp.auth == "False"
        assert smtp.port == 25

    def test_full_config(self) -> None:
        """Test full SMTP configuration."""
        smtp = SMTPSettings(
            server="smtp.example.com",
            user="smtp_user",
            password="smtp_pass",
            auth="True",
            port=587,
        )
        assert smtp.server == "smtp.example.com"
        assert smtp.user == "smtp_user"
        assert smtp.port == 587


class TestLicensingSettings:
    """Tests for LicensingSettings model."""

    def test_required_fields(self) -> None:
        """Test licensing required fields."""
        licensing = LicensingSettings(
            mailfrom="netapp-licensing@example.com",
            mailto="netapp-team@example.com",
        )
        assert licensing.mailfrom == "netapp-licensing@example.com"
        assert licensing.mailto == "netapp-team@example.com"


class TestONTAPAPISettings:
    """Tests for ONTAPAPISettings model."""

    def test_default_base_path(self) -> None:
        """Test default base API path."""
        settings = ONTAPAPISettings()
        assert settings.base_api_path == "/api"

    def test_custom_base_path(self) -> None:
        """Test custom base API path."""
        settings = ONTAPAPISettings(base_api_path="/api/v2")
        assert settings.base_api_path == "/api/v2"


class TestDIIAPISettings:
    """Tests for DIIAPISettings model."""

    def test_required_fields(self) -> None:
        """Test DII API required fields."""
        settings = DIIAPISettings(
            api_ro_token="token123",
            base_url="https://client.cloudinsights.netapp.com",
        )
        assert settings.api_ro_token == "token123"
        assert settings.base_url == "https://client.cloudinsights.netapp.com"
        assert settings.base_api_path == "/rest/v1"

    def test_custom_base_path(self) -> None:
        """Test custom base API path."""
        settings = DIIAPISettings(
            api_ro_token="token123",
            base_url="https://client.cloudinsights.netapp.com",
            base_api_path="/rest/v2",
        )
        assert settings.base_api_path == "/rest/v2"


class TestSearchableKeysConfig:
    """Tests for SearchableKeysConfig model."""

    def test_default_empty_list(self) -> None:
        """Test default empty searchable keys."""
        config = SearchableKeysConfig()
        assert config.searchable_keys == []

    def test_with_keys(self) -> None:
        """Test with searchable keys."""
        config = SearchableKeysConfig(
            searchable_keys=["div", "bu", "env", "app", "region"],
        )
        assert "div" in config.searchable_keys
        assert "bu" in config.searchable_keys
        assert len(config.searchable_keys) == 5


class TestModelSerialization:
    """Tests for model serialization."""

    def test_model_dump(self) -> None:
        """Test converting model to dict."""
        cluster = ClusterConfig(
            name="CLUSTER-01",
            ip="10.0.0.1",
            tags=["active"],
        )
        data = cluster.model_dump()
        assert data["name"] == "CLUSTER-01"
        assert data["ip"] == "10.0.0.1"
        assert data["tags"] == ["active"]

    def test_model_dump_exclude_unset(self) -> None:
        """Test excluding unset fields."""
        cluster = ClusterConfig(name="CLUSTER-01", ip="10.0.0.1")
        data = cluster.model_dump(exclude_unset=True)
        assert "name" in data
        assert "ip" in data
        # Default values are still included because they were set

    def test_model_json(self) -> None:
        """Test JSON serialization."""
        cluster = ClusterConfig(name="CLUSTER-01", ip="10.0.0.1")
        json_str = cluster.model_dump_json()
        assert '"name":"CLUSTER-01"' in json_str
        assert '"ip":"10.0.0.1"' in json_str
