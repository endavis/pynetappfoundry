"""OntapLocalCifsGroupMembers information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapLocalCifsGroupMembersRecord(OntapModel):
    """OntapLocalCifsGroupMembersRecord sub-model for records."""

    records_name: str = ""


class OntapLocalCifsGroupMembers(OntapModel):
    """OntapLocalCifsGroupMembers information."""

    local_cifs_group_sid: str = ""
    name: str = ""
    records: list[OntapLocalCifsGroupMembersRecord] = Field(default_factory=list)
    svm_name: str = ""
    svm_uuid: str = ""
