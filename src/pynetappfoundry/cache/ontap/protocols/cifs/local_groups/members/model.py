"""OntapLocalCifsGroupMembers information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.cache._base import CacheModel


class OntapLocalCifsGroupMembersRecord(CacheModel):
    """OntapLocalCifsGroupMembersRecord sub-model for records."""

    records_name: str = ""


class OntapLocalCifsGroupMembers(CacheModel):
    """OntapLocalCifsGroupMembers information."""

    local_cifs_group_sid: str = ""
    name: str = ""
    records: list[OntapLocalCifsGroupMembersRecord] = Field(default_factory=list)
    svm_name: str = ""
    svm_uuid: str = ""
