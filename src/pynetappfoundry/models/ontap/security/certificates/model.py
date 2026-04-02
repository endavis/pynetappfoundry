"""OntapSecurityCertificate information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapSecurityCertificateAzureProxy(OntapModel):
    """OntapSecurityCertificateAzureProxy sub-model for proxy."""

    host: str = ""
    password: str = ""
    port: int = 0
    type_: str = ""
    username: str = ""


class OntapSecurityCertificateAzure(OntapModel):
    """OntapSecurityCertificateAzure sub-model for azure."""

    client_certificate: str = ""
    client_id: str = ""
    client_secret: str = ""
    key_vault: str = ""
    oauth_host: str = ""
    proxy: OntapSecurityCertificateAzureProxy = Field(
        default_factory=OntapSecurityCertificateAzureProxy
    )
    tenant_id: str = ""
    timeout: int = 0
    verify_host: bool = False


class OntapSecurityCertificateSubjectAlternatives(OntapModel):
    """OntapSecurityCertificateSubjectAlternatives sub-model for subject_alternatives."""

    dns: list[str] = Field(default_factory=list)
    email: list[str] = Field(default_factory=list)
    ip: list[str] = Field(default_factory=list)
    uri: list[str] = Field(default_factory=list)


class OntapSecurityCertificateSvm(OntapModel):
    """OntapSecurityCertificateSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapSecurityCertificate(OntapModel):
    """OntapSecurityCertificate information."""

    authority_key_identifier: str = ""
    azure: OntapSecurityCertificateAzure = Field(default_factory=OntapSecurityCertificateAzure)
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
    subject_alternatives: OntapSecurityCertificateSubjectAlternatives = Field(
        default_factory=OntapSecurityCertificateSubjectAlternatives
    )
    subject_key_identifier: str = ""
    svm: OntapSecurityCertificateSvm = Field(default_factory=OntapSecurityCertificateSvm)
    type_: str = ""
    uuid: str = ""
