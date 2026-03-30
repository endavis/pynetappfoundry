"""OntapVscanEvent information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class OntapVscanEvent(OntapModel):
    """OntapVscanEvent information."""

    disconnect_reason: str = ""
    event_time: str = ""
    file_path: str = ""
    interface_ip_address: str = ""
    interface_name: str = ""
    interface_uuid: str = ""
    node_name: str = ""
    node_uuid: str = ""
    server: str = ""
    svm_name: str = ""
    svm_uuid: str = ""
    type_: str = ""
    vendor: str = ""
    version: str = ""
