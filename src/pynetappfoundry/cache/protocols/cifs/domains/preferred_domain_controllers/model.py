"""OntapCifsDomainPreferredDc information."""

from __future__ import annotations

from pynetappfoundry.cache._base import CacheModel


class OntapCifsDomainPreferredDc(CacheModel):
    """OntapCifsDomainPreferredDc information."""

    fqdn: str = ""
    server_ip: str = ""
    status_details: str = ""
    status_reachable: bool = False
    svm_name: str = ""
    svm_uuid: str = ""
