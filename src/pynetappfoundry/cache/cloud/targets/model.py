"""Cloud target information — /cloud/targets."""

from __future__ import annotations

from pynetappfoundry.cache._base import CacheModel


class CloudTargetInfo(CacheModel):
    """Cloud object store target configuration.

    Represents a cloud target used for FabricPool tiering or SnapMirror-to-cloud.
    Available via /cloud/targets REST API (ONTAP 9.6+).
    """

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
