"""OntapSecurityKeyManager information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapSecurityKeyManagerConfiguration(OntapModel):
    """OntapSecurityKeyManagerConfiguration sub-model for configuration."""

    name: str = ""
    uuid: str = ""


class OntapSecurityKeyManagerExternalClientCertificate(OntapModel):
    """OntapSecurityKeyManagerExternalClientCertificate sub-model for client_certificate."""

    name: str = ""
    uuid: str = ""


class OntapSecurityKeyManagerExternalServerCaCertificate(OntapModel):
    """OntapSecurityKeyManagerExternalServerCaCertificate sub-model for server_ca_certificates."""

    name: str = ""
    uuid: str = ""


class OntapSecurityKeyManagerExternalServerConnectivityNodeStateNode(OntapModel):
    """OntapSecurityKeyManagerExternalServerConnectivityNodeStateNode sub-model for node."""

    name: str = ""
    uuid: str = ""


class OntapSecurityKeyManagerExternalServerConnectivityNodeState(OntapModel):
    """OntapSecurityKeyManagerExternalServerConnectivityNodeState sub-model for node_states."""

    node: OntapSecurityKeyManagerExternalServerConnectivityNodeStateNode = Field(
        default_factory=OntapSecurityKeyManagerExternalServerConnectivityNodeStateNode
    )
    state: str = ""


class OntapSecurityKeyManagerExternalServerConnectivity(OntapModel):
    """OntapSecurityKeyManagerExternalServerConnectivity sub-model for connectivity."""

    cluster_availability: bool = False
    node_states: list[OntapSecurityKeyManagerExternalServerConnectivityNodeState] = Field(
        default_factory=list
    )


class OntapSecurityKeyManagerExternalServer(OntapModel):
    """OntapSecurityKeyManagerExternalServer sub-model for servers."""

    connectivity: OntapSecurityKeyManagerExternalServerConnectivity = Field(
        default_factory=OntapSecurityKeyManagerExternalServerConnectivity
    )
    secondary_key_servers: str = ""
    server: str = ""
    timeout: int = 0
    username: str = ""


class OntapSecurityKeyManagerExternal(OntapModel):
    """OntapSecurityKeyManagerExternal sub-model for external."""

    client_certificate: OntapSecurityKeyManagerExternalClientCertificate = Field(
        default_factory=OntapSecurityKeyManagerExternalClientCertificate
    )
    server_ca_certificates: list[OntapSecurityKeyManagerExternalServerCaCertificate] = Field(
        default_factory=list
    )
    servers: list[OntapSecurityKeyManagerExternalServer] = Field(default_factory=list)


class OntapSecurityKeyManagerOnboard(OntapModel):
    """OntapSecurityKeyManagerOnboard sub-model for onboard."""

    enabled: bool = False
    existing_passphrase: str = ""
    key_backup: str = ""
    passphrase: str = ""
    synchronize: bool = False


class OntapSecurityKeyManagerStatus(OntapModel):
    """OntapSecurityKeyManagerStatus sub-model for status."""

    code: int = 0
    message: str = ""


class OntapSecurityKeyManagerSvm(OntapModel):
    """OntapSecurityKeyManagerSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapSecurityKeyManagerVolumeEncryption(OntapModel):
    """OntapSecurityKeyManagerVolumeEncryption sub-model for volume_encryption."""

    code: int = 0
    message: str = ""
    supported: bool = False


class OntapSecurityKeyManager(OntapModel):
    """OntapSecurityKeyManager information."""

    configuration: OntapSecurityKeyManagerConfiguration = Field(
        default_factory=OntapSecurityKeyManagerConfiguration
    )
    enabled: bool = False
    external: OntapSecurityKeyManagerExternal = Field(
        default_factory=OntapSecurityKeyManagerExternal
    )
    is_default_data_at_rest_encryption_disabled: bool = False
    onboard: OntapSecurityKeyManagerOnboard = Field(default_factory=OntapSecurityKeyManagerOnboard)
    policy: str = ""
    scope: str = ""
    status: OntapSecurityKeyManagerStatus = Field(default_factory=OntapSecurityKeyManagerStatus)
    svm: OntapSecurityKeyManagerSvm = Field(default_factory=OntapSecurityKeyManagerSvm)
    uuid: str = ""
    volume_encryption: OntapSecurityKeyManagerVolumeEncryption = Field(
        default_factory=OntapSecurityKeyManagerVolumeEncryption
    )
