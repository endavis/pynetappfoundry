"""OntapApplicationComponentSnapshot information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapApplicationComponentSnapshotApplication(OntapModel):
    """OntapApplicationComponentSnapshotApplication sub-model for application."""

    name: str = ""
    uuid: str = ""


class OntapApplicationComponentSnapshotComponent(OntapModel):
    """OntapApplicationComponentSnapshotComponent sub-model for component."""

    name: str = ""
    uuid: str = ""


class OntapApplicationComponentSnapshotSvm(OntapModel):
    """OntapApplicationComponentSnapshotSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapApplicationComponentSnapshot(OntapModel):
    """OntapApplicationComponentSnapshot information."""

    application: OntapApplicationComponentSnapshotApplication = Field(
        default_factory=OntapApplicationComponentSnapshotApplication
    )
    comment: str = ""
    component: OntapApplicationComponentSnapshotComponent = Field(
        default_factory=OntapApplicationComponentSnapshotComponent
    )
    consistency_type: str = ""
    create_time: str = ""
    is_partial: bool = False
    name: str = ""
    svm: OntapApplicationComponentSnapshotSvm = Field(
        default_factory=OntapApplicationComponentSnapshotSvm
    )
    uuid: str = ""
