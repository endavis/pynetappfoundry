"""OntapCifsDomainPreferredDc information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class OntapCifsDomainPreferredDc(OntapModel):
    """OntapCifsDomainPreferredDc information."""

    fqdn: str = ""
    server_ip: str = ""
    status_details: str = ""
    status_reachable: bool = False
    svm_name: str = ""
    svm_uuid: str = ""
