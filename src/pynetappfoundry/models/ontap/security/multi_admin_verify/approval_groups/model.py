"""OntapMultiAdminVerifyApprovalGroup information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapMultiAdminVerifyApprovalGroupOwner(OntapModel):
    """OntapMultiAdminVerifyApprovalGroupOwner sub-model for owner."""

    name: str = ""
    uuid: str = ""


class OntapMultiAdminVerifyApprovalGroup(OntapModel):
    """OntapMultiAdminVerifyApprovalGroup information."""

    approvers: list[str] = Field(default_factory=list)
    email: list[str] = Field(default_factory=list)
    name: str = ""
    owner: OntapMultiAdminVerifyApprovalGroupOwner = Field(
        default_factory=OntapMultiAdminVerifyApprovalGroupOwner
    )
