"""OntapIpsecCaCertificate information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class OntapIpsecCaCertificate(OntapModel):
    """OntapIpsecCaCertificate information."""

    certificate_uuid: str = ""
    scope: str = ""
    svm_name: str = ""
    svm_uuid: str = ""
