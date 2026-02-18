"""OntapIpsecCaCertificate information."""

from __future__ import annotations

from pynetappfoundry.cache._base import CacheModel


class OntapIpsecCaCertificate(CacheModel):
    """OntapIpsecCaCertificate information."""

    certificate_uuid: str = ""
    scope: str = ""
    svm_name: str = ""
    svm_uuid: str = ""
