"""OntapGcpKms information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapGcpKmsEkmipReachability(OntapModel):
    """OntapGcpKmsEkmipReachability sub-model for ekmip_reachability."""

    ekmip_reachability_code: str = ""
    ekmip_reachability_message: str = ""
    ekmip_reachability_node_name: str = ""
    ekmip_reachability_node_uuid: str = ""
    ekmip_reachability_reachable: bool = False


class OntapGcpKms(OntapModel):
    """OntapGcpKms information."""

    application_credentials: str = ""
    caller_account: str = ""
    cloudkms_host: str = ""
    ekmip_reachability: list[OntapGcpKmsEkmipReachability] = Field(default_factory=list)
    google_reachability_code: str = ""
    google_reachability_message: str = ""
    google_reachability_reachable: bool = False
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
    state_cluster_state: bool = False
    state_code: str = ""
    state_message: str = ""
    svm_name: str = ""
    svm_uuid: str = ""
    uuid: str = ""
    verify_host: bool = False
    verify_ip: bool = False
