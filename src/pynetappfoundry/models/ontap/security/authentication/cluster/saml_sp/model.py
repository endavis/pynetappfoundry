"""OntapSecuritySamlSp information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapSecuritySamlSpCertificate(OntapModel):
    """OntapSecuritySamlSpCertificate sub-model for certificate."""

    ca: str = ""
    common_name: str = ""
    serial_number: str = ""


class OntapSecuritySamlSp(OntapModel):
    """OntapSecuritySamlSp information."""

    certificate: OntapSecuritySamlSpCertificate = Field(
        default_factory=OntapSecuritySamlSpCertificate
    )
    enabled: bool = False
    host: str = ""
    idp_uri: str = ""
