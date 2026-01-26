"""Cloud-related utility functions for Azure, AWS, GCP, and IBM."""

from __future__ import annotations

AZURE_BASE_URL = "https://portal.azure.com/#resource"

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
