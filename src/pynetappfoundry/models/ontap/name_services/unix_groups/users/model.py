"""OntapUnixGroupUsers information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapUnixGroupUsersRecord(OntapModel):
    """OntapUnixGroupUsersRecord sub-model for records."""

    name: str = ""


class OntapUnixGroupUsersSvm(OntapModel):
    """OntapUnixGroupUsersSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapUnixGroupUsersUnixGroup(OntapModel):
    """OntapUnixGroupUsersUnixGroup sub-model for unix_group."""

    name: str = ""


class OntapUnixGroupUsers(OntapModel):
    """OntapUnixGroupUsers information."""

    name: str = ""
    records: list[OntapUnixGroupUsersRecord] = Field(default_factory=list)
    skip_name_validation: bool = False
    svm: OntapUnixGroupUsersSvm = Field(default_factory=OntapUnixGroupUsersSvm)
    unix_group: OntapUnixGroupUsersUnixGroup = Field(default_factory=OntapUnixGroupUsersUnixGroup)
