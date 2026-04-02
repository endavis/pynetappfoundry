"""OntapAzureKeyVault information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapAzureKeyVaultAzureReachability(OntapModel):
    """OntapAzureKeyVaultAzureReachability sub-model for azure_reachability."""

    code: str = ""
    message: str = ""
    reachable: bool = False


class OntapAzureKeyVaultConfiguration(OntapModel):
    """OntapAzureKeyVaultConfiguration sub-model for configuration."""

    name: str = ""
    uuid: str = ""


class OntapAzureKeyVaultEkmipReachabilityNode(OntapModel):
    """OntapAzureKeyVaultEkmipReachabilityNode sub-model for node."""

    name: str = ""
    uuid: str = ""


class OntapAzureKeyVaultEkmipReachability(OntapModel):
    """OntapAzureKeyVaultEkmipReachability sub-model for ekmip_reachability."""

    code: str = ""
    message: str = ""
    node: OntapAzureKeyVaultEkmipReachabilityNode = Field(
        default_factory=OntapAzureKeyVaultEkmipReachabilityNode
    )
    reachable: bool = False


class OntapAzureKeyVaultState(OntapModel):
    """OntapAzureKeyVaultState sub-model for state."""

    available: bool = False
    code: str = ""
    message: str = ""


class OntapAzureKeyVaultSvm(OntapModel):
    """OntapAzureKeyVaultSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapAzureKeyVault(OntapModel):
    """OntapAzureKeyVault information."""

    authentication_method: str = ""
    azure_reachability: OntapAzureKeyVaultAzureReachability = Field(
        default_factory=OntapAzureKeyVaultAzureReachability
    )
    client_certificate: str = ""
    client_id: str = ""
    client_secret: str = ""
    configuration: OntapAzureKeyVaultConfiguration = Field(
        default_factory=OntapAzureKeyVaultConfiguration
    )
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
    state: OntapAzureKeyVaultState = Field(default_factory=OntapAzureKeyVaultState)
    svm: OntapAzureKeyVaultSvm = Field(default_factory=OntapAzureKeyVaultSvm)
    tenant_id: str = ""
    uuid: str = ""
    vault_host: str = ""
    verify_host: bool = False
    verify_ip: bool = False
