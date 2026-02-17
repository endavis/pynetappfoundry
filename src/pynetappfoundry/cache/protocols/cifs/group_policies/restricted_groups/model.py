"""OntapGroupPolicyObjectRestrictedGroup information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.cache._base import CacheModel


class OntapGroupPolicyObjectRestrictedGroup(CacheModel):
    """OntapGroupPolicyObjectRestrictedGroup information."""

    group_name: str = ""
    link: str = ""
    members: list[str] = Field(default_factory=list)
    memberships: list[str] = Field(default_factory=list)
    policy_name: str = ""
    svm_name: str = ""
    svm_uuid: str = ""
    version: int = 0
