"""OntapCifsDomainPreferredDc information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapCifsDomainPreferredDcStatus(OntapModel):
    """OntapCifsDomainPreferredDcStatus sub-model for status."""

    details: str = ""
    reachable: bool = False


class OntapCifsDomainPreferredDcSvm(OntapModel):
    """OntapCifsDomainPreferredDcSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapCifsDomainPreferredDc(OntapModel):
    """OntapCifsDomainPreferredDc information."""

    fqdn: str = ""
    server_ip: str = ""
    status: OntapCifsDomainPreferredDcStatus = Field(
        default_factory=OntapCifsDomainPreferredDcStatus
    )
    svm: OntapCifsDomainPreferredDcSvm = Field(default_factory=OntapCifsDomainPreferredDcSvm)
