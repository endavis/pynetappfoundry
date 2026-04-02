"""OntapCloudTarget information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapCloudTargetCluster(OntapModel):
    """OntapCloudTargetCluster sub-model for cluster."""

    name: str = ""
    uuid: str = ""


class OntapCloudTargetIpspace(OntapModel):
    """OntapCloudTargetIpspace sub-model for ipspace."""

    name: str = ""
    uuid: str = ""


class OntapCloudTargetSvm(OntapModel):
    """OntapCloudTargetSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


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
    cluster: OntapCloudTargetCluster = Field(default_factory=OntapCloudTargetCluster)
    container: str = ""
    ipspace: OntapCloudTargetIpspace = Field(default_factory=OntapCloudTargetIpspace)
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
    svm: OntapCloudTargetSvm = Field(default_factory=OntapCloudTargetSvm)
    url_style: str = ""
    use_http_proxy: bool = False
    used: int = 0
    uuid: str = ""
