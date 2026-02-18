"""OntapLocalCifsGroup information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.cache._base import CacheModel


class OntapLocalCifsGroupMember(CacheModel):
    """OntapLocalCifsGroupMember sub-model for members."""

    members_name: str = ""


class OntapLocalCifsGroup(CacheModel):
    """OntapLocalCifsGroup information."""

    description: str = ""
    members: list[OntapLocalCifsGroupMember] = Field(default_factory=list)
    name: str = ""
    sid: str = ""
    svm_name: str = ""
    svm_uuid: str = ""
