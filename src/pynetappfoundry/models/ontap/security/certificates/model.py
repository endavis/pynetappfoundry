"""OntapSecurityCertificate information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapSecurityCertificate(OntapModel):
    """OntapSecurityCertificate information."""

    authority_key_identifier: str = ""
    azure_client_certificate: str = ""
    azure_client_id: str = ""
    azure_client_secret: str = ""
    azure_key_vault: str = ""
    azure_oauth_host: str = ""
    azure_proxy_host: str = ""
    azure_proxy_password: str = ""
    azure_proxy_port: int = 0
    azure_proxy_type: str = ""
    azure_proxy_username: str = ""
    azure_tenant_id: str = ""
    azure_timeout: int = 0
    azure_verify_host: bool = False
    ca: str = ""
    common_name: str = ""
    expiry_time: str = ""
    hash_function: str = ""
    intermediate_certificates: list[str] = Field(default_factory=list)
    key_size: int = 0
    name: str = ""
    private_key: str = ""
    public_certificate: str = ""
    scope: str = ""
    serial_number: str = ""
    subject_alternatives_dns: list[str] = Field(default_factory=list)
    subject_alternatives_email: list[str] = Field(default_factory=list)
    subject_alternatives_ip: list[str] = Field(default_factory=list)
    subject_alternatives_uri: list[str] = Field(default_factory=list)
    subject_key_identifier: str = ""
    svm_name: str = ""
    svm_uuid: str = ""
    type_: str = ""
    uuid: str = ""
