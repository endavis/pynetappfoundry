"""OntapStoragePort information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapStoragePortCable(OntapModel):
    """OntapStoragePortCable sub-model for cable."""

    identifier: str = ""
    length: str = ""
    part_number: str = ""
    serial_number: str = ""
    transceiver: str = ""
    vendor: str = ""


class OntapStoragePortError(OntapModel):
    """OntapStoragePortError sub-model for error."""

    corrective_action: str = ""
    message: str = ""


class OntapStoragePortNode(OntapModel):
    """OntapStoragePortNode sub-model for node."""

    name: str = ""
    uuid: str = ""


class OntapStoragePort(OntapModel):
    """OntapStoragePort information."""

    board_name: str = ""
    cable: OntapStoragePortCable = Field(default_factory=OntapStoragePortCable)
    description: str = ""
    enabled: bool = False
    error: OntapStoragePortError = Field(default_factory=OntapStoragePortError)
    firmware_version: str = ""
    force: bool = False
    in_use: bool = False
    mac_address: str = ""
    mode: str = ""
    name: str = ""
    node: OntapStoragePortNode = Field(default_factory=OntapStoragePortNode)
    part_number: str = ""
    redundant: bool = False
    serial_number: str = ""
    speed: float = 0.0
    state: str = ""
    type_: str = ""
    wwn: str = ""
    wwpn: str = ""
