"""OntapMultiAdminVerifyApprovalGroup information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.cache._base import CacheModel


class OntapMultiAdminVerifyApprovalGroup(CacheModel):
    """OntapMultiAdminVerifyApprovalGroup information."""

    approvers: list[str] = Field(default_factory=list)
    email: list[str] = Field(default_factory=list)
    name: str = ""
    owner_name: str = ""
    owner_uuid: str = ""
