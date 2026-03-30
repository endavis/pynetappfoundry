"""OntapVscanServerStatus information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class OntapVscanServerStatus(OntapModel):
    """OntapVscanServerStatus information."""

    disconnected_reason: str = ""
    interface_ip_address: str = ""
    interface_name: str = ""
    interface_uuid: str = ""
    ip: str = ""
    node_name: str = ""
    node_uuid: str = ""
    state: str = ""
    svm_name: str = ""
    svm_uuid: str = ""
    type_: str = ""
    update_time: str = ""
    vendor: str = ""
    version: str = ""
