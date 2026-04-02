"""OntapIpsecCaCertificate information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapIpsecCaCertificateCertificate(OntapModel):
    """OntapIpsecCaCertificateCertificate sub-model for certificate."""

    uuid: str = ""


class OntapIpsecCaCertificateSvm(OntapModel):
    """OntapIpsecCaCertificateSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapIpsecCaCertificate(OntapModel):
    """OntapIpsecCaCertificate information."""

    certificate: OntapIpsecCaCertificateCertificate = Field(
        default_factory=OntapIpsecCaCertificateCertificate
    )
    scope: str = ""
    svm: OntapIpsecCaCertificateSvm = Field(default_factory=OntapIpsecCaCertificateSvm)
