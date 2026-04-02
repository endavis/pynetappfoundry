"""OntapVscanServerStatus information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapVscanServerStatusInterfaceIp(OntapModel):
    """OntapVscanServerStatusInterfaceIp sub-model for ip."""

    address: str = ""


class OntapVscanServerStatusInterface(OntapModel):
    """OntapVscanServerStatusInterface sub-model for interface."""

    ip: OntapVscanServerStatusInterfaceIp = Field(default_factory=OntapVscanServerStatusInterfaceIp)
    name: str = ""
    uuid: str = ""


class OntapVscanServerStatusNode(OntapModel):
    """OntapVscanServerStatusNode sub-model for node."""

    name: str = ""
    uuid: str = ""


class OntapVscanServerStatusSvm(OntapModel):
    """OntapVscanServerStatusSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapVscanServerStatus(OntapModel):
    """OntapVscanServerStatus information."""

    disconnected_reason: str = ""
    interface: OntapVscanServerStatusInterface = Field(
        default_factory=OntapVscanServerStatusInterface
    )
    ip: str = ""
    node: OntapVscanServerStatusNode = Field(default_factory=OntapVscanServerStatusNode)
    state: str = ""
    svm: OntapVscanServerStatusSvm = Field(default_factory=OntapVscanServerStatusSvm)
    type_: str = ""
    update_time: str = ""
    vendor: str = ""
    version: str = ""
