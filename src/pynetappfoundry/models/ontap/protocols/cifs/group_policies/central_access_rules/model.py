"""OntapGroupPolicyObjectCentralAccessRule information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class OntapGroupPolicyObjectCentralAccessRule(OntapModel):
    """OntapGroupPolicyObjectCentralAccessRule information."""

    create_time: str = ""
    current_permission: str = ""
    description: str = ""
    name: str = ""
    proposed_permission: str = ""
    resource_criteria: str = ""
    svm_name: str = ""
    svm_uuid: str = ""
    update_time: str = ""
