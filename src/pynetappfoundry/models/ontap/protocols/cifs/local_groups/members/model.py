"""OntapLocalCifsGroupMembers information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapLocalCifsGroupMembersLocalCifsGroup(OntapModel):
    """OntapLocalCifsGroupMembersLocalCifsGroup sub-model for local_cifs_group."""

    sid: str = ""


class OntapLocalCifsGroupMembersRecord(OntapModel):
    """OntapLocalCifsGroupMembersRecord sub-model for records."""

    name: str = ""


class OntapLocalCifsGroupMembersSvm(OntapModel):
    """OntapLocalCifsGroupMembersSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapLocalCifsGroupMembers(OntapModel):
    """OntapLocalCifsGroupMembers information."""

    local_cifs_group: OntapLocalCifsGroupMembersLocalCifsGroup = Field(
        default_factory=OntapLocalCifsGroupMembersLocalCifsGroup
    )
    name: str = ""
    records: list[OntapLocalCifsGroupMembersRecord] = Field(default_factory=list)
    svm: OntapLocalCifsGroupMembersSvm = Field(default_factory=OntapLocalCifsGroupMembersSvm)
