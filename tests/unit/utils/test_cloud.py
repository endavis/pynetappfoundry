"""Tests for cloud utility functions."""

from __future__ import annotations

from pynetappfoundry.utils.cloud import (
    AWS_CONSOLE_BASE_URL,
    AZURE_BASE_URL,
    build_aws_instance_link,
    build_azure_id,
    build_azure_portal_link,
    build_cloud_instance_link,
    build_cloud_resource_group_link,
    get_cloud_account_name,
    get_cloud_types,
)


class TestBuildAzureId:
    """Tests for build_azure_id."""

    def test_builds_resource_group_id(self) -> None:
        """Test building Azure resource group ID."""
        result = build_azure_id("sub-123", "my-rg")
        assert result == "/subscriptions/sub-123/resourceGroups/my-rg"

    def test_builds_vm_resource_id(self) -> None:
        """Test building Azure VM resource ID."""
        result = build_azure_id("sub-123", "my-rg", "vm", "my-vm")
        assert result == (
            "/subscriptions/sub-123/resourceGroups/my-rg"
            "/providers/Microsoft.Compute/virtualMachines/my-vm"
        )


class TestBuildAzurePortalLink:
    """Tests for build_azure_portal_link."""

    def test_builds_portal_link(self) -> None:
        """Test building Azure portal link."""
        resource_id = "/subscriptions/sub-123/resourceGroups/my-rg"
        result = build_azure_portal_link(resource_id)
        assert result == f"{AZURE_BASE_URL}{resource_id}"


class TestBuildAwsInstanceLink:
    """Tests for build_aws_instance_link."""

    def test_builds_ec2_console_link(self) -> None:
        """Test building AWS EC2 console link."""
        result = build_aws_instance_link("us-east-1", "i-0123456789abcdef0")
        expected = (
            f"https://us-east-1.{AWS_CONSOLE_BASE_URL}/ec2/home"
            "?region=us-east-1#InstanceDetails:instanceId=i-0123456789abcdef0"
        )
        assert result == expected

    def test_returns_empty_string_for_missing_region(self) -> None:
        """Test returns empty string when region is missing."""
        result = build_aws_instance_link("", "i-0123456789abcdef0")
        assert result == ""

    def test_returns_empty_string_for_missing_instance_id(self) -> None:
        """Test returns empty string when instance_id is missing."""
        result = build_aws_instance_link("us-east-1", "")
        assert result == ""


class TestBuildCloudInstanceLink:
    """Tests for build_cloud_instance_link."""

    def test_builds_aws_instance_link(self) -> None:
        """Test building AWS instance link via generic function."""
        result = build_cloud_instance_link(
            provider="AWS",
            instance_id="i-0123456789abcdef0",
            region="us-east-1",
        )
        assert "us-east-1" in result
        assert "i-0123456789abcdef0" in result
        assert AWS_CONSOLE_BASE_URL in result

    def test_builds_azure_instance_link(self) -> None:
        """Test building Azure instance link via generic function."""
        result = build_cloud_instance_link(
            provider="Azure",
            instance_id="my-vm",
            account_id="sub-123",
            resource_group="my-rg",
        )
        assert AZURE_BASE_URL in result
        assert "sub-123" in result
        assert "my-rg" in result
        assert "my-vm" in result

    def test_handles_lowercase_provider(self) -> None:
        """Test handles lowercase provider names."""
        result = build_cloud_instance_link(
            provider="aws",
            instance_id="i-0123456789abcdef0",
            region="us-west-2",
        )
        assert "us-west-2" in result

    def test_returns_empty_for_unsupported_provider(self) -> None:
        """Test returns empty string for unsupported provider."""
        result = build_cloud_instance_link(
            provider="GCP",
            instance_id="instance-1",
            region="us-central1",
        )
        assert result == ""

    def test_returns_empty_for_azure_missing_fields(self) -> None:
        """Test returns empty string when Azure required fields are missing."""
        result = build_cloud_instance_link(
            provider="Azure",
            instance_id="my-vm",
            # missing account_id and resource_group
        )
        assert result == ""


class TestBuildCloudResourceGroupLink:
    """Tests for build_cloud_resource_group_link."""

    def test_builds_azure_resource_group_link(self) -> None:
        """Test building Azure resource group link."""
        result = build_cloud_resource_group_link(
            provider="Azure",
            account_id="sub-123",
            resource_group="my-rg",
        )
        assert AZURE_BASE_URL in result
        assert "sub-123" in result
        assert "my-rg" in result

    def test_returns_empty_for_aws(self) -> None:
        """Test returns empty string for AWS (no resource groups)."""
        result = build_cloud_resource_group_link(
            provider="AWS",
            account_id="123456789012",
        )
        assert result == ""

    def test_returns_empty_for_azure_missing_fields(self) -> None:
        """Test returns empty string when Azure required fields are missing."""
        result = build_cloud_resource_group_link(
            provider="Azure",
            account_id="sub-123",
            # missing resource_group
        )
        assert result == ""


class TestGetCloudAccountName:
    """Tests for get_cloud_account_name."""

    def test_returns_subscription_for_azure(self) -> None:
        """Test returns 'subscription' for Azure."""
        assert get_cloud_account_name("azure") == "subscription"

    def test_returns_account_for_aws(self) -> None:
        """Test returns 'account' for AWS."""
        assert get_cloud_account_name("aws") == "account"


class TestGetCloudTypes:
    """Tests for get_cloud_types."""

    def test_returns_list_of_cloud_types(self) -> None:
        """Test returns list of supported cloud types."""
        result = get_cloud_types()
        assert "aws" in result
        assert "azure" in result
        assert "gcp" in result
        assert "ibm" in result

    def test_returns_copy(self) -> None:
        """Test returns a copy, not the original list."""
        result1 = get_cloud_types()
        result1.append("test")
        result2 = get_cloud_types()
        assert "test" not in result2
