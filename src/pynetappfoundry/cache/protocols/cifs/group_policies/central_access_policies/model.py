"""OntapGroupPolicyObjectCentralAccessPolicy information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.cache._base import CacheModel


class OntapGroupPolicyObjectCentralAccessPolicy(CacheModel):
    """OntapGroupPolicyObjectCentralAccessPolicy information."""

    create_time: str = ""
    description: str = ""
    member_rules: list[str] = Field(default_factory=list)
    name: str = ""
    sid: str = ""
    svm_name: str = ""
    svm_uuid: str = ""
    update_time: str = ""
