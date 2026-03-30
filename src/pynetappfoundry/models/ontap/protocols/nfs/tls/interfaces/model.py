"""OntapNfsTlsInterface information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class OntapNfsTlsInterface(OntapModel):
    """OntapNfsTlsInterface information."""

    certificate_name: str = ""
    certificate_uuid: str = ""
    enabled: bool = False
    interface_ip_address: str = ""
    interface_name: str = ""
    interface_uuid: str = ""
    svm_name: str = ""
    svm_uuid: str = ""
