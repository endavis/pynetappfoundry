"""OntapMultiAdminVerifyRequest information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.cache._base import CacheModel


class OntapMultiAdminVerifyRequest(CacheModel):
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
    owner_name: str = ""
    owner_uuid: str = ""
    pending_approvers: int = 0
    permitted_users: list[str] = Field(default_factory=list)
    potential_approvers: list[str] = Field(default_factory=list)
    query: str = ""
    required_approvers: int = 0
    state: str = ""
    user_requested: str = ""
    user_vetoed: str = ""
