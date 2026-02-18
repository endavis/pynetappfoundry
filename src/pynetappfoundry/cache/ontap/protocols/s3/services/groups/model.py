"""OntapS3Group information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.cache._base import CacheModel


class OntapS3GroupPolicy(CacheModel):
    """OntapS3GroupPolicy sub-model for policies."""

    policies_name: str = ""


class OntapS3GroupUser(CacheModel):
    """OntapS3GroupUser sub-model for users."""

    users_name: str = ""


class OntapS3Group(CacheModel):
    """OntapS3Group information."""

    comment: str = ""
    id: int = 0
    name: str = ""
    policies: list[OntapS3GroupPolicy] = Field(default_factory=list)
    svm_name: str = ""
    svm_uuid: str = ""
    users: list[OntapS3GroupUser] = Field(default_factory=list)
