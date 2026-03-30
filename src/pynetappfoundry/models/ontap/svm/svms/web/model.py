"""OntapWebSvm information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class OntapWebSvm(OntapModel):
    """OntapWebSvm information."""

    certificate_name: str = ""
    certificate_uuid: str = ""
    client_enabled: bool = False
    ocsp_enabled: bool = False
    svm_name: str = ""
    svm_uuid: str = ""
