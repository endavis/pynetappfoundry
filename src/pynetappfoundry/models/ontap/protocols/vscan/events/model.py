"""OntapVscanEvent information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapVscanEventInterfaceIp(OntapModel):
    """OntapVscanEventInterfaceIp sub-model for ip."""

    address: str = ""


class OntapVscanEventInterface(OntapModel):
    """OntapVscanEventInterface sub-model for interface."""

    ip: OntapVscanEventInterfaceIp = Field(default_factory=OntapVscanEventInterfaceIp)
    name: str = ""
    uuid: str = ""


class OntapVscanEventNode(OntapModel):
    """OntapVscanEventNode sub-model for node."""

    name: str = ""
    uuid: str = ""


class OntapVscanEventSvm(OntapModel):
    """OntapVscanEventSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapVscanEvent(OntapModel):
    """OntapVscanEvent information."""

    disconnect_reason: str = ""
    event_time: str = ""
    file_path: str = ""
    interface: OntapVscanEventInterface = Field(default_factory=OntapVscanEventInterface)
    node: OntapVscanEventNode = Field(default_factory=OntapVscanEventNode)
    server: str = ""
    svm: OntapVscanEventSvm = Field(default_factory=OntapVscanEventSvm)
    type_: str = ""
    vendor: str = ""
    version: str = ""
