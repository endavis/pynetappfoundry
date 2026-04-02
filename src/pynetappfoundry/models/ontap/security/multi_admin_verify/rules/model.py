"""OntapMultiAdminVerifyRule information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapMultiAdminVerifyRuleApprovalGroup(OntapModel):
    """OntapMultiAdminVerifyRuleApprovalGroup sub-model for approval_groups."""

    name: str = ""


class OntapMultiAdminVerifyRuleOwner(OntapModel):
    """OntapMultiAdminVerifyRuleOwner sub-model for owner."""

    name: str = ""
    uuid: str = ""


class OntapMultiAdminVerifyRule(OntapModel):
    """OntapMultiAdminVerifyRule information."""

    approval_expiry: str = ""
    approval_groups: list[OntapMultiAdminVerifyRuleApprovalGroup] = Field(default_factory=list)
    auto_request_create: bool = False
    create_time: str = ""
    execution_expiry: str = ""
    operation: str = ""
    owner: OntapMultiAdminVerifyRuleOwner = Field(default_factory=OntapMultiAdminVerifyRuleOwner)
    query: str = ""
    required_approvers: int = 0
    system_defined: bool = False
