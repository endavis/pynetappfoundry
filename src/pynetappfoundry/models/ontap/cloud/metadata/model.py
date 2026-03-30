"""Cloud provider metadata — CLI: virtual-machine instance show."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class CloudMetadata(OntapModel):
    """Cloud provider metadata from virtual-machine instance show.

    Contains instance-level information from the cloud provider.
    Each node in a cluster has its own cloud metadata.
    """

    node: str = ""  # Node name this metadata belongs to
    instance_id: str = ""
    account_id: str = ""
    image_id: str = ""
    instance_type: str = ""
    cpu_platform: str = ""
    region: str = ""
    provider: str = ""  # AWS, Azure, GCP
    consumer: str = ""
    primary_ip: str = ""
    metadata_version: str = ""
    # AWS-specific
    availability_zone: str = ""
    availability_zone_id: str = ""
    # Azure-specific
    fault_domain: str = ""
    update_domain: str = ""
    resource_group_name: str = ""
    offer: str = ""
    sku: str = ""
    sku_version: str = ""
    # Resource links (computed from other fields)
    instance_link: str = ""  # URL to cloud console for this instance
    instance_sso_link: str = ""  # URL to cloud console via AWS SSO (AWS only)
    resource_group_link: str = ""  # URL to cloud console for resource group (Azure)
