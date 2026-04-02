"""OntapApplicationSnapshot information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapApplicationSnapshotApplication(OntapModel):
    """OntapApplicationSnapshotApplication sub-model for application."""

    name: str = ""
    uuid: str = ""


class OntapApplicationSnapshotComponent(OntapModel):
    """OntapApplicationSnapshotComponent sub-model for components."""

    name: str = ""
    uuid: str = ""


class OntapApplicationSnapshotSvm(OntapModel):
    """OntapApplicationSnapshotSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapApplicationSnapshot(OntapModel):
    """OntapApplicationSnapshot information."""

    application: OntapApplicationSnapshotApplication = Field(
        default_factory=OntapApplicationSnapshotApplication
    )
    comment: str = ""
    components: list[OntapApplicationSnapshotComponent] = Field(default_factory=list)
    consistency_type: str = ""
    create_time: str = ""
    is_partial: bool = False
    name: str = ""
    svm: OntapApplicationSnapshotSvm = Field(default_factory=OntapApplicationSnapshotSvm)
    uuid: str = ""
