"""OntapWebSvm information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapWebSvmCertificate(OntapModel):
    """OntapWebSvmCertificate sub-model for certificate."""

    name: str = ""
    uuid: str = ""


class OntapWebSvmSvm(OntapModel):
    """OntapWebSvmSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapWebSvm(OntapModel):
    """OntapWebSvm information."""

    certificate: OntapWebSvmCertificate = Field(default_factory=OntapWebSvmCertificate)
    client_enabled: bool = False
    ocsp_enabled: bool = False
    svm: OntapWebSvmSvm = Field(default_factory=OntapWebSvmSvm)
