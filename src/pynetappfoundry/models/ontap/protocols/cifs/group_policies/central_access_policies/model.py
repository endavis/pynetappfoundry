"""OntapGroupPolicyObjectCentralAccessPolicy information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapGroupPolicyObjectCentralAccessPolicySvm(OntapModel):
    """OntapGroupPolicyObjectCentralAccessPolicySvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapGroupPolicyObjectCentralAccessPolicy(OntapModel):
    """OntapGroupPolicyObjectCentralAccessPolicy information."""

    create_time: str = ""
    description: str = ""
    member_rules: list[str] = Field(default_factory=list)
    name: str = ""
    sid: str = ""
    svm: OntapGroupPolicyObjectCentralAccessPolicySvm = Field(
        default_factory=OntapGroupPolicyObjectCentralAccessPolicySvm
    )
    update_time: str = ""
