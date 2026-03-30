"""OntapGroupPolicyObjectRestrictedGroup information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapGroupPolicyObjectRestrictedGroup(OntapModel):
    """OntapGroupPolicyObjectRestrictedGroup information."""

    group_name: str = ""
    link: str = ""
    members: list[str] = Field(default_factory=list)
    memberships: list[str] = Field(default_factory=list)
    policy_name: str = ""
    svm_name: str = ""
    svm_uuid: str = ""
    version: int = 0
