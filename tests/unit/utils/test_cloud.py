"""Tests for cloud utility functions."""

from __future__ import annotations

from pynetappfoundry.utils.cloud import (
    AWS_CONSOLE_BASE_URL,
    AWS_SSO_BASE_URL,
    AZURE_BASE_URL,
    build_aws_instance_link,
    build_aws_sso_link,
    build_azure_id,
    build_azure_portal_link,
    build_azure_vm_name,
    build_cloud_instance_link,
    build_cloud_instance_sso_link,
    build_cloud_resource_group_link,
    get_cloud_account_name,
    get_cloud_types,
    get_node_number,
)


class TestGetNodeNumber:
    """Tests for get_node_number."""

    def test_extracts_number_with_dash(self) -> None:
        """Test extracts node number from name with dash separator."""
        assert get_node_number("mycluster-01") == 1
        assert get_node_number("mycluster-02") == 2
        assert get_node_number("cluster-1") == 1
        assert get_node_number("cluster-12") == 12

    def test_extracts_number_with_underscore(self) -> None:
        """Test extracts node number from name with underscore separator."""
        assert get_node_number("mycluster_01") == 1
        assert get_node_number("mycluster_02") == 2

    def test_extracts_number_without_separator(self) -> None:
        """Test extracts trailing number without separator."""
        assert get_node_number("cluster01") == 1
        assert get_node_number("cluster02") == 2

    def test_returns_none_for_no_number(self) -> None:
        """Test returns None when no trailing number found."""
        assert get_node_number("mycluster") is None
        assert get_node_number("cluster-abc") is None

    def test_returns_none_for_empty_string(self) -> None:
        """Test returns None for empty string."""
        assert get_node_number("") is None


class TestBuildAzureVmName:
    """Tests for build_azure_vm_name."""

    def test_ha_cluster_node_01(self) -> None:
        """Test HA cluster VM name for node 01."""
        result = build_azure_vm_name("mycluster", "mycluster-01", is_ha=True)
        assert result == "mycluster-vm1"

    def test_ha_cluster_node_02(self) -> None:
        """Test HA cluster VM name for node 02."""
        result = build_azure_vm_name("mycluster", "mycluster-02", is_ha=True)
        assert result == "mycluster-vm2"

    def test_single_node_cluster(self) -> None:
        """Test single node cluster VM name."""
        result = build_azure_vm_name("mycluster", "mycluster-01", is_ha=False)
        assert result == "mycluster"

    def test_single_node_empty_node_name(self) -> None:
        """Test single node cluster with empty node name."""
        result = build_azure_vm_name("mycluster", "", is_ha=False)
        assert result == "mycluster"

    def test_ha_cluster_no_node_number(self) -> None:
        """Test HA cluster fallback when node number can't be determined."""
        result = build_azure_vm_name("mycluster", "mycluster", is_ha=True)
        assert result == "mycluster"

    def test_returns_empty_for_empty_cluster_name(self) -> None:
        """Test returns empty string when cluster name is empty."""
        result = build_azure_vm_name("", "node-01", is_ha=True)
        assert result == ""

    def test_default_is_ha(self) -> None:
        """Test default is_ha is True."""
        result = build_azure_vm_name("mycluster", "mycluster-01")
        assert result == "mycluster-vm1"


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

    def test_azure_derives_vm_name_from_cluster_ha(self) -> None:
        """Test Azure VM name is derived from cluster/node info for HA."""
        result = build_cloud_instance_link(
            provider="Azure",
            instance_id="some-instance-id",  # This should be ignored
            account_id="sub-123",
            resource_group="my-rg",
            cluster_name="mycluster",
            node_name="mycluster-01",
            is_ha=True,
        )
        assert AZURE_BASE_URL in result
        assert "mycluster-vm1" in result
        assert "some-instance-id" not in result

    def test_azure_derives_vm_name_from_cluster_single_node(self) -> None:
        """Test Azure VM name is derived from cluster for single node."""
        result = build_cloud_instance_link(
            provider="Azure",
            instance_id="some-instance-id",  # This should be ignored
            account_id="sub-123",
            resource_group="my-rg",
            cluster_name="mycluster",
            node_name="mycluster-01",
            is_ha=False,
        )
        assert AZURE_BASE_URL in result
        assert "mycluster" in result
        # For single node, it should just be cluster name, not cluster-vm1
        assert "mycluster-vm1" not in result

    def test_azure_uses_instance_id_when_no_cluster_name(self) -> None:
        """Test Azure uses instance_id when cluster_name is not provided."""
        result = build_cloud_instance_link(
            provider="Azure",
            instance_id="my-vm-instance",
            account_id="sub-123",
            resource_group="my-rg",
        )
        assert "my-vm-instance" in result


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


class TestBuildAwsSsoLink:
    """Tests for build_aws_sso_link."""

    def test_builds_sso_shortcut_link(self) -> None:
        """Test building AWS SSO shortcut link."""
        destination = "https://us-east-1.console.aws.amazon.com/ec2/home?region=us-east-1"
        result = build_aws_sso_link(
            sso_subdomain="mycompany",
            account_id="123456789012",
            role_name="AdminAccess",
            destination_url=destination,
        )
        assert result.startswith("https://mycompany.awsapps.com/start/#/console")
        assert "account_id=123456789012" in result
        assert "role_name=AdminAccess" in result
        # Destination should be URL-encoded
        assert "destination=" in result
        assert "us-east-1" not in result.split("destination=")[0]  # encoded in destination

    def test_url_encodes_destination(self) -> None:
        """Test that destination URL is properly URL-encoded."""
        destination = "https://console.aws.amazon.com/ec2?param=value&other=test"
        result = build_aws_sso_link(
            sso_subdomain="mycompany",
            account_id="123456789012",
            role_name="Admin",
            destination_url=destination,
        )
        # The & and = should be encoded in the destination
        assert "%3A" in result  # encoded colon
        assert "%2F" in result  # encoded slash

    def test_url_encodes_role_name_with_spaces(self) -> None:
        """Test that role name with spaces is URL-encoded."""
        result = build_aws_sso_link(
            sso_subdomain="mycompany",
            account_id="123456789012",
            role_name="Admin Access Role",
            destination_url="https://console.aws.amazon.com/",
        )
        assert "Admin%20Access%20Role" in result

    def test_returns_empty_for_missing_subdomain(self) -> None:
        """Test returns empty string when subdomain is missing."""
        result = build_aws_sso_link(
            sso_subdomain="",
            account_id="123456789012",
            role_name="Admin",
            destination_url="https://console.aws.amazon.com/",
        )
        assert result == ""

    def test_returns_empty_for_missing_account_id(self) -> None:
        """Test returns empty string when account_id is missing."""
        result = build_aws_sso_link(
            sso_subdomain="mycompany",
            account_id="",
            role_name="Admin",
            destination_url="https://console.aws.amazon.com/",
        )
        assert result == ""

    def test_returns_empty_for_missing_role_name(self) -> None:
        """Test returns empty string when role_name is missing."""
        result = build_aws_sso_link(
            sso_subdomain="mycompany",
            account_id="123456789012",
            role_name="",
            destination_url="https://console.aws.amazon.com/",
        )
        assert result == ""

    def test_returns_empty_for_missing_destination(self) -> None:
        """Test returns empty string when destination_url is missing."""
        result = build_aws_sso_link(
            sso_subdomain="mycompany",
            account_id="123456789012",
            role_name="Admin",
            destination_url="",
        )
        assert result == ""


class TestBuildCloudInstanceSsoLink:
    """Tests for build_cloud_instance_sso_link."""

    def test_builds_aws_sso_link_with_config(self) -> None:
        """Test building AWS SSO link when config is provided."""
        sso_config = {
            "subdomain": "mycompany",
            "account_roles": {"123456789012": "AdminAccess"},
        }
        instance_link = "https://us-east-1.console.aws.amazon.com/ec2/home"
        result = build_cloud_instance_sso_link(
            provider="AWS",
            instance_link=instance_link,
            account_id="123456789012",
            sso_config=sso_config,
        )
        assert result.startswith("https://mycompany.awsapps.com/start/#/console")
        assert "account_id=123456789012" in result
        assert "role_name=AdminAccess" in result

    def test_returns_empty_for_aws_without_config(self) -> None:
        """Test returns empty string for AWS when no SSO config."""
        result = build_cloud_instance_sso_link(
            provider="AWS",
            instance_link="https://console.aws.amazon.com/",
            account_id="123456789012",
            sso_config=None,
        )
        assert result == ""

    def test_returns_empty_for_azure(self) -> None:
        """Test returns empty string for Azure (SSO not applicable)."""
        sso_config = {
            "subdomain": "mycompany",
            "account_roles": {"123456789012": "Admin"},
        }
        result = build_cloud_instance_sso_link(
            provider="Azure",
            instance_link="https://portal.azure.com/",
            account_id="sub-123",
            sso_config=sso_config,
        )
        assert result == ""

    def test_returns_empty_for_missing_account_role(self) -> None:
        """Test returns empty string when account has no role mapping."""
        sso_config = {
            "subdomain": "mycompany",
            "account_roles": {"999999999999": "OtherRole"},  # Different account
        }
        result = build_cloud_instance_sso_link(
            provider="AWS",
            instance_link="https://console.aws.amazon.com/",
            account_id="123456789012",
            sso_config=sso_config,
        )
        assert result == ""

    def test_returns_empty_for_missing_subdomain(self) -> None:
        """Test returns empty string when subdomain is missing from config."""
        sso_config = {
            "account_roles": {"123456789012": "Admin"},
        }
        result = build_cloud_instance_sso_link(
            provider="AWS",
            instance_link="https://console.aws.amazon.com/",
            account_id="123456789012",
            sso_config=sso_config,
        )
        assert result == ""

    def test_handles_lowercase_provider(self) -> None:
        """Test handles lowercase provider name."""
        sso_config = {
            "subdomain": "mycompany",
            "account_roles": {"123456789012": "Admin"},
        }
        result = build_cloud_instance_sso_link(
            provider="aws",
            instance_link="https://console.aws.amazon.com/",
            account_id="123456789012",
            sso_config=sso_config,
        )
        assert AWS_SSO_BASE_URL in result
