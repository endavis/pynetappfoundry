"""OntapLocalCifsGroup information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapLocalCifsGroupMember(OntapModel):
    """OntapLocalCifsGroupMember sub-model for members."""

    name: str = ""


class OntapLocalCifsGroup(OntapModel):
    """OntapLocalCifsGroup information."""

    description: str = ""
    members: list[OntapLocalCifsGroupMember] = Field(default_factory=list)
    name: str = ""
    sid: str = ""
    svm_name: str = ""
    svm_uuid: str = ""
