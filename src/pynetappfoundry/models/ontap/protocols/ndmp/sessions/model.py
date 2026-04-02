"""OntapNdmpSession information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapNdmpSessionDataConnection(OntapModel):
    """OntapNdmpSessionDataConnection sub-model for connection."""

    address: str = ""
    port: int = 0
    type_: str = ""


class OntapNdmpSessionData(OntapModel):
    """OntapNdmpSessionData sub-model for data."""

    bytes_processed: int = 0
    connection: OntapNdmpSessionDataConnection = Field(
        default_factory=OntapNdmpSessionDataConnection
    )
    operation: str = ""
    reason: str = ""
    state: str = ""


class OntapNdmpSessionMoverConnection(OntapModel):
    """OntapNdmpSessionMoverConnection sub-model for connection."""

    address: str = ""
    port: int = 0
    type_: str = ""


class OntapNdmpSessionMover(OntapModel):
    """OntapNdmpSessionMover sub-model for mover."""

    bytes_moved: int = 0
    connection: OntapNdmpSessionMoverConnection = Field(
        default_factory=OntapNdmpSessionMoverConnection
    )
    mode: str = ""
    reason: str = ""
    state: str = ""


class OntapNdmpSessionNode(OntapModel):
    """OntapNdmpSessionNode sub-model for node."""

    name: str = ""
    uuid: str = ""


class OntapNdmpSessionScsi(OntapModel):
    """OntapNdmpSessionScsi sub-model for scsi."""

    device_id: str = ""
    host_adapter: int = 0
    lun_id: int = 0
    target_id: int = 0


class OntapNdmpSessionSvm(OntapModel):
    """OntapNdmpSessionSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapNdmpSession(OntapModel):
    """OntapNdmpSession information."""

    backup_engine: str = ""
    client_address: str = ""
    client_port: int = 0
    data: OntapNdmpSessionData = Field(default_factory=OntapNdmpSessionData)
    data_path: str = ""
    id: str = ""
    mover: OntapNdmpSessionMover = Field(default_factory=OntapNdmpSessionMover)
    node: OntapNdmpSessionNode = Field(default_factory=OntapNdmpSessionNode)
    scsi: OntapNdmpSessionScsi = Field(default_factory=OntapNdmpSessionScsi)
    source_address: str = ""
    svm: OntapNdmpSessionSvm = Field(default_factory=OntapNdmpSessionSvm)
    tape_device: str = ""
    tape_mode: str = ""
    uuid: str = ""
