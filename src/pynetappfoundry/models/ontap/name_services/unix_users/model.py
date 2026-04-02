"""OntapUnixUser information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapUnixUserSvm(OntapModel):
    """OntapUnixUserSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapUnixUser(OntapModel):
    """OntapUnixUser information."""

    full_name: str = ""
    id: int = 0
    name: str = ""
    primary_gid: int = 0
    skip_name_validation: bool = False
    svm: OntapUnixUserSvm = Field(default_factory=OntapUnixUserSvm)
