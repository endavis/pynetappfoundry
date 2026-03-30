"""OntapUnixGroup information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapUnixGroupUser(OntapModel):
    """OntapUnixGroupUser sub-model for users."""

    users_name: str = ""


class OntapUnixGroup(OntapModel):
    """OntapUnixGroup information."""

    id: int = 0
    name: str = ""
    skip_name_validation: bool = False
    svm_name: str = ""
    svm_uuid: str = ""
    users: list[OntapUnixGroupUser] = Field(default_factory=list)
