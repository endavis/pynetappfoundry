"""OntapGcpKms information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapGcpKmsEkmipReachabilityNode(OntapModel):
    """OntapGcpKmsEkmipReachabilityNode sub-model for node."""

    name: str = ""
    uuid: str = ""


class OntapGcpKmsEkmipReachability(OntapModel):
    """OntapGcpKmsEkmipReachability sub-model for ekmip_reachability."""

    code: str = ""
    message: str = ""
    node: OntapGcpKmsEkmipReachabilityNode = Field(default_factory=OntapGcpKmsEkmipReachabilityNode)
    reachable: bool = False


class OntapGcpKmsGoogleReachability(OntapModel):
    """OntapGcpKmsGoogleReachability sub-model for google_reachability."""

    code: str = ""
    message: str = ""
    reachable: bool = False


class OntapGcpKmsState(OntapModel):
    """OntapGcpKmsState sub-model for state."""

    cluster_state: bool = False
    code: str = ""
    message: str = ""


class OntapGcpKmsSvm(OntapModel):
    """OntapGcpKmsSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapGcpKms(OntapModel):
    """OntapGcpKms information."""

    application_credentials: str = ""
    caller_account: str = ""
    cloudkms_host: str = ""
    ekmip_reachability: list[OntapGcpKmsEkmipReachability] = Field(default_factory=list)
    google_reachability: OntapGcpKmsGoogleReachability = Field(
        default_factory=OntapGcpKmsGoogleReachability
    )
    key_name: str = ""
    key_ring_location: str = ""
    key_ring_name: str = ""
    oauth_host: str = ""
    oauth_url: str = ""
    port: int = 0
    privileged_account: str = ""
    project_id: str = ""
    proxy_host: str = ""
    proxy_password: str = ""
    proxy_port: int = 0
    proxy_type: str = ""
    proxy_username: str = ""
    scope: str = ""
    state: OntapGcpKmsState = Field(default_factory=OntapGcpKmsState)
    svm: OntapGcpKmsSvm = Field(default_factory=OntapGcpKmsSvm)
    uuid: str = ""
    verify_host: bool = False
    verify_ip: bool = False
