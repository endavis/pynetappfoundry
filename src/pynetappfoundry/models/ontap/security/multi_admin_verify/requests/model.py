"""OntapMultiAdminVerifyRequest information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapMultiAdminVerifyRequestOwner(OntapModel):
    """OntapMultiAdminVerifyRequestOwner sub-model for owner."""

    name: str = ""
    uuid: str = ""


class OntapMultiAdminVerifyRequest(OntapModel):
    """OntapMultiAdminVerifyRequest information."""

    approve_expiry_time: str = ""
    approve_time: str = ""
    approved_users: list[str] = Field(default_factory=list)
    comment: str = ""
    create_time: str = ""
    execute_on_approval: bool = False
    execution_expiry_time: str = ""
    index: int = 0
    operation: str = ""
    owner: OntapMultiAdminVerifyRequestOwner = Field(
        default_factory=OntapMultiAdminVerifyRequestOwner
    )
    pending_approvers: int = 0
    permitted_users: list[str] = Field(default_factory=list)
    potential_approvers: list[str] = Field(default_factory=list)
    query: str = ""
    required_approvers: int = 0
    state: str = ""
    user_requested: str = ""
    user_vetoed: str = ""
