"""OntapApplicationSnapshot information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapApplicationSnapshotComponent(OntapModel):
    """OntapApplicationSnapshotComponent sub-model for components."""

    name: str = ""
    uuid: str = ""


class OntapApplicationSnapshot(OntapModel):
    """OntapApplicationSnapshot information."""

    application_name: str = ""
    application_uuid: str = ""
    comment: str = ""
    components: list[OntapApplicationSnapshotComponent] = Field(default_factory=list)
    consistency_type: str = ""
    create_time: str = ""
    is_partial: bool = False
    name: str = ""
    svm_name: str = ""
    svm_uuid: str = ""
    uuid: str = ""
