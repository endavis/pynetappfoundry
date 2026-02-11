"""Cloud provider metadata models (/cloud API path)."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class CloudMetadata(BaseModel):
    """Cloud provider metadata from virtual-machine instance show.

    Contains instance-level information from the cloud provider.
    Each node in a cluster has its own cloud metadata.
    """

    model_config = ConfigDict(extra="allow")

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


class CloudTargetInfo(BaseModel):
    """Cloud object store target configuration.

    Represents a cloud target used for FabricPool tiering or SnapMirror-to-cloud.
    Available via /cloud/targets REST API (ONTAP 9.6+).
    """

    model_config = ConfigDict(extra="allow")

    name: str = ""
    uuid: str = ""
    provider_type: str = ""  # AWS_S3, Azure_Cloud, SGWS, etc.
    server: str = ""
    container: str = ""  # Bucket/container name
    owner: str = ""  # fabricpool, snapmirror
    scope: str = ""  # cluster, svm (9.12+)
    svm: str = ""
    ssl_enabled: bool = True
    authentication_type: str = ""  # key, cap, etc.
    ipspace: str = ""
    snapmirror_use: str = ""
    access_key: str = ""  # AWS/S3 access key ID
    azure_account: str = ""  # Azure account name
