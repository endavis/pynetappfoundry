"""OntapFileMove information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapFileMoveDestinationSvm(OntapModel):
    """OntapFileMoveDestinationSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapFileMoveDestinationVolume(OntapModel):
    """OntapFileMoveDestinationVolume sub-model for volume."""

    name: str = ""
    uuid: str = ""


class OntapFileMoveDestination(OntapModel):
    """OntapFileMoveDestination sub-model for destination."""

    path: str = ""
    svm: OntapFileMoveDestinationSvm = Field(default_factory=OntapFileMoveDestinationSvm)
    volume: OntapFileMoveDestinationVolume = Field(default_factory=OntapFileMoveDestinationVolume)


class OntapFileMoveFailureArgument(OntapModel):
    """OntapFileMoveFailureArgument sub-model for arguments."""

    code: str = ""
    message: str = ""


class OntapFileMoveFailure(OntapModel):
    """OntapFileMoveFailure sub-model for failure."""

    arguments: list[OntapFileMoveFailureArgument] = Field(default_factory=list)
    code: str = ""
    message: str = ""


class OntapFileMoveFilesToMoveDestinationSvm(OntapModel):
    """OntapFileMoveFilesToMoveDestinationSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapFileMoveFilesToMoveDestinationVolume(OntapModel):
    """OntapFileMoveFilesToMoveDestinationVolume sub-model for volume."""

    name: str = ""
    uuid: str = ""


class OntapFileMoveFilesToMoveDestination(OntapModel):
    """OntapFileMoveFilesToMoveDestination sub-model for destinations."""

    path: str = ""
    svm: OntapFileMoveFilesToMoveDestinationSvm = Field(
        default_factory=OntapFileMoveFilesToMoveDestinationSvm
    )
    volume: OntapFileMoveFilesToMoveDestinationVolume = Field(
        default_factory=OntapFileMoveFilesToMoveDestinationVolume
    )


class OntapFileMoveFilesToMoveSourceSvm(OntapModel):
    """OntapFileMoveFilesToMoveSourceSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapFileMoveFilesToMoveSourceVolume(OntapModel):
    """OntapFileMoveFilesToMoveSourceVolume sub-model for volume."""

    name: str = ""
    uuid: str = ""


class OntapFileMoveFilesToMoveSource(OntapModel):
    """OntapFileMoveFilesToMoveSource sub-model for sources."""

    path: str = ""
    svm: OntapFileMoveFilesToMoveSourceSvm = Field(
        default_factory=OntapFileMoveFilesToMoveSourceSvm
    )
    volume: OntapFileMoveFilesToMoveSourceVolume = Field(
        default_factory=OntapFileMoveFilesToMoveSourceVolume
    )


class OntapFileMoveFilesToMove(OntapModel):
    """OntapFileMoveFilesToMove sub-model for files_to_move."""

    destinations: list[OntapFileMoveFilesToMoveDestination] = Field(default_factory=list)
    sources: list[OntapFileMoveFilesToMoveSource] = Field(default_factory=list)


class OntapFileMoveNode(OntapModel):
    """OntapFileMoveNode sub-model for node."""

    name: str = ""
    uuid: str = ""


class OntapFileMoveReferenceSvm(OntapModel):
    """OntapFileMoveReferenceSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapFileMoveReferenceVolume(OntapModel):
    """OntapFileMoveReferenceVolume sub-model for volume."""

    name: str = ""
    uuid: str = ""


class OntapFileMoveReference(OntapModel):
    """OntapFileMoveReference sub-model for reference."""

    max_cutover_time: int = 0
    path: str = ""
    svm: OntapFileMoveReferenceSvm = Field(default_factory=OntapFileMoveReferenceSvm)
    volume: OntapFileMoveReferenceVolume = Field(default_factory=OntapFileMoveReferenceVolume)


class OntapFileMoveScanner(OntapModel):
    """OntapFileMoveScanner sub-model for scanner."""

    percent: int = 0
    progress: int = 0
    state: str = ""
    total: int = 0


class OntapFileMoveSourceSvm(OntapModel):
    """OntapFileMoveSourceSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapFileMoveSourceVolume(OntapModel):
    """OntapFileMoveSourceVolume sub-model for volume."""

    name: str = ""
    uuid: str = ""


class OntapFileMoveSource(OntapModel):
    """OntapFileMoveSource sub-model for source."""

    path: str = ""
    svm: OntapFileMoveSourceSvm = Field(default_factory=OntapFileMoveSourceSvm)
    volume: OntapFileMoveSourceVolume = Field(default_factory=OntapFileMoveSourceVolume)


class OntapFileMoveSvm(OntapModel):
    """OntapFileMoveSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapFileMoveVolume(OntapModel):
    """OntapFileMoveVolume sub-model for volume."""

    name: str = ""
    uuid: str = ""


class OntapFileMove(OntapModel):
    """OntapFileMove information."""

    cutover_time: int = 0
    destination: OntapFileMoveDestination = Field(default_factory=OntapFileMoveDestination)
    elapsed_time: int = 0
    failure: OntapFileMoveFailure = Field(default_factory=OntapFileMoveFailure)
    files_to_move: OntapFileMoveFilesToMove = Field(default_factory=OntapFileMoveFilesToMove)
    index: int = 0
    is_destination_ready: bool = False
    is_flexgroup: bool = False
    is_snapshot_fenced: bool = False
    max_cutover_time: int = 0
    max_throughput: int = 0
    node: OntapFileMoveNode = Field(default_factory=OntapFileMoveNode)
    reference: OntapFileMoveReference = Field(default_factory=OntapFileMoveReference)
    scanner: OntapFileMoveScanner = Field(default_factory=OntapFileMoveScanner)
    source: OntapFileMoveSource = Field(default_factory=OntapFileMoveSource)
    svm: OntapFileMoveSvm = Field(default_factory=OntapFileMoveSvm)
    uuid: str = ""
    volume: OntapFileMoveVolume = Field(default_factory=OntapFileMoveVolume)
