"""OntapGroupPolicyObjectCentralAccessPolicy information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapGroupPolicyObjectCentralAccessPolicy(OntapModel):
    """OntapGroupPolicyObjectCentralAccessPolicy information."""

    create_time: str = ""
    description: str = ""
    member_rules: list[str] = Field(default_factory=list)
    name: str = ""
    sid: str = ""
    svm_name: str = ""
    svm_uuid: str = ""
    update_time: str = ""
