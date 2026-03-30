"""OntapAzureKeyVault information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapAzureKeyVaultEkmipReachability(OntapModel):
    """OntapAzureKeyVaultEkmipReachability sub-model for ekmip_reachability."""

    ekmip_reachability_code: str = ""
    ekmip_reachability_message: str = ""
    ekmip_reachability_node_name: str = ""
    ekmip_reachability_node_uuid: str = ""
    ekmip_reachability_reachable: bool = False


class OntapAzureKeyVault(OntapModel):
    """OntapAzureKeyVault information."""

    authentication_method: str = ""
    azure_reachability_code: str = ""
    azure_reachability_message: str = ""
    azure_reachability_reachable: bool = False
    client_certificate: str = ""
    client_id: str = ""
    client_secret: str = ""
    configuration_name: str = ""
    configuration_uuid: str = ""
    ekmip_reachability: list[OntapAzureKeyVaultEkmipReachability] = Field(default_factory=list)
    enabled: bool = False
    key_id: str = ""
    name: str = ""
    oauth_host: str = ""
    port: int = 0
    proxy_host: str = ""
    proxy_password: str = ""
    proxy_port: int = 0
    proxy_type: str = ""
    proxy_username: str = ""
    scope: str = ""
    skip_verification: bool = False
    state_available: bool = False
    state_code: str = ""
    state_message: str = ""
    svm_name: str = ""
    svm_uuid: str = ""
    tenant_id: str = ""
    uuid: str = ""
    vault_host: str = ""
    verify_host: bool = False
    verify_ip: bool = False
