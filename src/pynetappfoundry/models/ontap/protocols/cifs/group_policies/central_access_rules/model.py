"""OntapGroupPolicyObjectCentralAccessRule information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapGroupPolicyObjectCentralAccessRuleSvm(OntapModel):
    """OntapGroupPolicyObjectCentralAccessRuleSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapGroupPolicyObjectCentralAccessRule(OntapModel):
    """OntapGroupPolicyObjectCentralAccessRule information."""

    create_time: str = ""
    current_permission: str = ""
    description: str = ""
    name: str = ""
    proposed_permission: str = ""
    resource_criteria: str = ""
    svm: OntapGroupPolicyObjectCentralAccessRuleSvm = Field(
        default_factory=OntapGroupPolicyObjectCentralAccessRuleSvm
    )
    update_time: str = ""
