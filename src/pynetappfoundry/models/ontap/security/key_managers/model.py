"""OntapSecurityKeyManager information."""

from __future__ import annotations

from typing import Any

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapSecurityKeyManagerServerCaCertificate(OntapModel):
    """OntapSecurityKeyManagerServerCaCertificate sub-model for server_ca_certificates."""

    external_server_ca_certificates_name: str = ""
    external_server_ca_certificates_uuid: str = ""


class OntapSecurityKeyManagerServer(OntapModel):
    """OntapSecurityKeyManagerServer sub-model for servers."""

    external_servers_connectivity_cluster_availability: bool = False
    external_servers_connectivity_node_states: list[dict[str, Any]] = Field(default_factory=list)
    external_servers_secondary_key_servers: str = ""
    external_servers_server: str = ""
    external_servers_timeout: int = 0
    external_servers_username: str = ""


class OntapSecurityKeyManager(OntapModel):
    """OntapSecurityKeyManager information."""

    configuration_name: str = ""
    configuration_uuid: str = ""
    enabled: bool = False
    external_client_certificate_name: str = ""
    external_client_certificate_uuid: str = ""
    external_server_ca_certificates: list[OntapSecurityKeyManagerServerCaCertificate] = Field(
        default_factory=list
    )
    external_servers: list[OntapSecurityKeyManagerServer] = Field(default_factory=list)
    is_default_data_at_rest_encryption_disabled: bool = False
    onboard_enabled: bool = False
    onboard_existing_passphrase: str = ""
    onboard_key_backup: str = ""
    onboard_passphrase: str = ""
    onboard_synchronize: bool = False
    policy: str = ""
    scope: str = ""
    status_code: int = 0
    status_message: str = ""
    svm_name: str = ""
    svm_uuid: str = ""
    uuid: str = ""
    volume_encryption_code: int = 0
    volume_encryption_message: str = ""
    volume_encryption_supported: bool = False
