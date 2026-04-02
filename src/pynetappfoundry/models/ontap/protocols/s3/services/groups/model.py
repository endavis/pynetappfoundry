"""OntapS3Group information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapS3GroupPolicy(OntapModel):
    """OntapS3GroupPolicy sub-model for policies."""

    name: str = ""


class OntapS3GroupSvm(OntapModel):
    """OntapS3GroupSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapS3GroupUser(OntapModel):
    """OntapS3GroupUser sub-model for users."""

    name: str = ""


class OntapS3Group(OntapModel):
    """OntapS3Group information."""

    comment: str = ""
    id: int = 0
    name: str = ""
    policies: list[OntapS3GroupPolicy] = Field(default_factory=list)
    svm: OntapS3GroupSvm = Field(default_factory=OntapS3GroupSvm)
    users: list[OntapS3GroupUser] = Field(default_factory=list)
