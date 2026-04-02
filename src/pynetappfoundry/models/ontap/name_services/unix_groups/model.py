"""OntapUnixGroup information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapUnixGroupSvm(OntapModel):
    """OntapUnixGroupSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapUnixGroupUser(OntapModel):
    """OntapUnixGroupUser sub-model for users."""

    name: str = ""


class OntapUnixGroup(OntapModel):
    """OntapUnixGroup information."""

    id: int = 0
    name: str = ""
    skip_name_validation: bool = False
    svm: OntapUnixGroupSvm = Field(default_factory=OntapUnixGroupSvm)
    users: list[OntapUnixGroupUser] = Field(default_factory=list)
