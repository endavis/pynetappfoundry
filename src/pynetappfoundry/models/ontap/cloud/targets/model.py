"""OntapCloudTarget information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class OntapCloudTarget(OntapModel):
    """OntapCloudTarget information."""

    access_key: str = ""
    authentication_type: str = ""
    azure_account: str = ""
    azure_msi_token: str = ""
    azure_private_key: str = ""
    azure_sas_token: str = ""
    cap_url: str = ""
    certificate_validation_enabled: bool = False
    cluster_name: str = ""
    cluster_uuid: str = ""
    container: str = ""
    ipspace_name: str = ""
    ipspace_uuid: str = ""
    name: str = ""
    owner: str = ""
    port: int = 0
    provider_type: str = ""
    read_latency_warning_threshold: int = 0
    scope: str = ""
    secret_password: str = ""
    server: str = ""
    server_side_encryption: str = ""
    snapmirror_use: str = ""
    ssl_enabled: bool = False
    svm_name: str = ""
    svm_uuid: str = ""
    url_style: str = ""
    use_http_proxy: bool = False
    used: int = 0
    uuid: str = ""
