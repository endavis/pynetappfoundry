"""OntapS3Policy information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapS3PolicyStatement(OntapModel):
    """OntapS3PolicyStatement sub-model for statements."""

    actions: list[str] = Field(default_factory=list)
    effect: str = ""
    index: int = 0
    resources: list[str] = Field(default_factory=list)
    sid: str = ""


class OntapS3Policy(OntapModel):
    """OntapS3Policy information."""

    comment: str = ""
    name: str = ""
    read_only: bool = False
    statements: list[OntapS3PolicyStatement] = Field(default_factory=list)
    svm_name: str = ""
    svm_uuid: str = ""
