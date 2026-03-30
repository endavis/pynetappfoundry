"""OntapUnixGroupUsers information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapUnixGroupUsersRecord(OntapModel):
    """OntapUnixGroupUsersRecord sub-model for records."""

    records_name: str = ""


class OntapUnixGroupUsers(OntapModel):
    """OntapUnixGroupUsers information."""

    name: str = ""
    records: list[OntapUnixGroupUsersRecord] = Field(default_factory=list)
    skip_name_validation: bool = False
    svm_name: str = ""
    svm_uuid: str = ""
    unix_group_name: str = ""
