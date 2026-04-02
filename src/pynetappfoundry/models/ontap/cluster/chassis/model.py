"""OntapChassis information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapChassisFru(OntapModel):
    """OntapChassisFru sub-model for frus."""

    id: str = ""
    state: str = ""
    type_: str = ""


class OntapChassisNodePcisCard(OntapModel):
    """OntapChassisNodePcisCard sub-model for cards."""

    device: str = ""
    info: str = ""
    slot: str = ""


class OntapChassisNodePcis(OntapModel):
    """OntapChassisNodePcis sub-model for pcis."""

    cards: list[OntapChassisNodePcisCard] = Field(default_factory=list)


class OntapChassisNodeUsbsPort(OntapModel):
    """OntapChassisNodeUsbsPort sub-model for ports."""

    connected: bool = False


class OntapChassisNodeUsbs(OntapModel):
    """OntapChassisNodeUsbs sub-model for usbs."""

    enabled: bool = False
    ports: list[OntapChassisNodeUsbsPort] = Field(default_factory=list)
    supported: bool = False


class OntapChassisNode(OntapModel):
    """OntapChassisNode sub-model for nodes."""

    name: str = ""
    pcis: OntapChassisNodePcis = Field(default_factory=OntapChassisNodePcis)
    position: str = ""
    usbs: OntapChassisNodeUsbs = Field(default_factory=OntapChassisNodeUsbs)
    uuid: str = ""


class OntapChassisShelve(OntapModel):
    """OntapChassisShelve sub-model for shelves."""

    uid: str = ""


class OntapChassis(OntapModel):
    """OntapChassis information."""

    frus: list[OntapChassisFru] = Field(default_factory=list)
    id: str = ""
    nodes: list[OntapChassisNode] = Field(default_factory=list)
    shelves: list[OntapChassisShelve] = Field(default_factory=list)
    state: str = ""
