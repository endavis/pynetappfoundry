"""OntapHostsSettings information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class OntapHostsSettings(OntapModel):
    """OntapHostsSettings information."""

    dns_ttl_enabled: bool = False
    enabled: bool = False
    negative_cache_enabled: bool = False
    negative_ttl: str = ""
    svm_name: str = ""
    svm_uuid: str = ""
    ttl: str = ""
    uuid: str = ""
