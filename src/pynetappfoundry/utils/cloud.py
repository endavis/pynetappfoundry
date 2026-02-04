"""Cloud-related utility functions for Azure, AWS, GCP, and IBM."""

from __future__ import annotations

AZURE_BASE_URL = "https://portal.azure.com/#resource"
AWS_CONSOLE_BASE_URL = "console.aws.amazon.com"

AZURE_PROVIDER_TYPES: dict[str, str] = {
    "vm": "Microsoft.Compute/virtualMachines",
}

CLOUD_TYPES: list[str] = ["aws", "azure", "gcp", "ibm"]

CLOUD_ACCOUNT_NAMES: dict[str, str] = {
    "azure": "subscription",
    "aws": "account",
    "ibm": "account",
    "gcp": "account",
}


def build_azure_id(
    sub_id: str,
    resource_group: str,
    resource_type: str = "vm",
    resource_name: str | None = None,
) -> str:
    """Build an Azure resource ID.

    Args:
        sub_id: Azure subscription ID.
        resource_group: Azure resource group name.
        resource_type: Type of resource (default: 'vm').
        resource_name: Name of the specific resource (optional).

    Returns:
        Azure resource ID string.
    """
    az_id = f"/subscriptions/{sub_id}/resourceGroups/{resource_group}"
    if resource_name:
        provider = AZURE_PROVIDER_TYPES[resource_type]
        az_id = f"{az_id}/providers/{provider}/{resource_name}"
    return az_id


def build_azure_portal_link(resource_id: str) -> str:
    """Build an Azure portal URL for a resource.

    Args:
        resource_id: Azure resource ID.

    Returns:
        Full Azure portal URL.
    """
    return f"{AZURE_BASE_URL}{resource_id}"


def get_cloud_account_name(cloud: str) -> str:
    """Get the account terminology for a cloud provider.

    Args:
        cloud: Cloud provider name (azure, aws, ibm, gcp).

    Returns:
        Account terminology (e.g., 'subscription' for Azure).
    """
    return CLOUD_ACCOUNT_NAMES[cloud]


def get_cloud_types() -> list[str]:
    """Get list of supported cloud types.

    Returns:
        List of cloud provider names.
    """
    return CLOUD_TYPES.copy()


def build_aws_instance_link(region: str, instance_id: str) -> str:
    """Build an AWS EC2 console URL for an instance.

    Args:
        region: AWS region (e.g., 'us-east-1').
        instance_id: EC2 instance ID (e.g., 'i-0123456789abcdef0').

    Returns:
        Full AWS console URL for the instance.
    """
    if not region or not instance_id:
        return ""
    return (
        f"https://{region}.{AWS_CONSOLE_BASE_URL}/ec2/home"
        f"?region={region}#InstanceDetails:instanceId={instance_id}"
    )


def build_cloud_instance_link(
    provider: str,
    instance_id: str,
    region: str = "",
    account_id: str = "",
    resource_group: str = "",
) -> str:
    """Build a cloud console URL for an instance based on provider.

    Args:
        provider: Cloud provider name (AWS, Azure).
        instance_id: Instance ID or name.
        region: Region (required for AWS).
        account_id: Account/subscription ID (required for Azure).
        resource_group: Resource group name (required for Azure).

    Returns:
        Cloud console URL for the instance, or empty string if not supported.
    """
    provider_lower = provider.lower()
    if provider_lower == "aws":
        return build_aws_instance_link(region, instance_id)
    elif provider_lower == "azure":
        if not account_id or not resource_group or not instance_id:
            return ""
        resource_id = build_azure_id(account_id, resource_group, "vm", instance_id)
        return build_azure_portal_link(resource_id)
    return ""


def build_cloud_resource_group_link(
    provider: str,
    account_id: str = "",
    resource_group: str = "",
) -> str:
    """Build a cloud console URL for a resource group based on provider.

    Args:
        provider: Cloud provider name (AWS, Azure).
        account_id: Account/subscription ID.
        resource_group: Resource group name (required for Azure).

    Returns:
        Cloud console URL for the resource group, or empty string if not supported.
    """
    provider_lower = provider.lower()
    if provider_lower == "azure":
        if not account_id or not resource_group:
            return ""
        resource_id = build_azure_id(account_id, resource_group)
        return build_azure_portal_link(resource_id)
    # AWS doesn't have resource groups in the same way
    return ""
