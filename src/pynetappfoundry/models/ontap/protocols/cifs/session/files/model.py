"""OntapCifsOpenFile information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapCifsOpenFileConnection(OntapModel):
    """OntapCifsOpenFileConnection sub-model for connection."""

    count: int = 0
    identifier: int = 0


class OntapCifsOpenFileNode(OntapModel):
    """OntapCifsOpenFileNode sub-model for node."""

    name: str = ""
    uuid: str = ""


class OntapCifsOpenFileSession(OntapModel):
    """OntapCifsOpenFileSession sub-model for session."""

    identifier: int = 0


class OntapCifsOpenFileShare(OntapModel):
    """OntapCifsOpenFileShare sub-model for share."""

    mode: str = ""
    name: str = ""


class OntapCifsOpenFileSvm(OntapModel):
    """OntapCifsOpenFileSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapCifsOpenFileVolume(OntapModel):
    """OntapCifsOpenFileVolume sub-model for volume."""

    name: str = ""
    uuid: str = ""


class OntapCifsOpenFile(OntapModel):
    """OntapCifsOpenFile information."""

    connection: OntapCifsOpenFileConnection = Field(default_factory=OntapCifsOpenFileConnection)
    continuously_available: str = ""
    identifier: int = 0
    node: OntapCifsOpenFileNode = Field(default_factory=OntapCifsOpenFileNode)
    open_mode: str = ""
    path: str = ""
    range_locks_count: int = 0
    session: OntapCifsOpenFileSession = Field(default_factory=OntapCifsOpenFileSession)
    share: OntapCifsOpenFileShare = Field(default_factory=OntapCifsOpenFileShare)
    svm: OntapCifsOpenFileSvm = Field(default_factory=OntapCifsOpenFileSvm)
    type_: str = ""
    volume: OntapCifsOpenFileVolume = Field(default_factory=OntapCifsOpenFileVolume)
