"""OntapS3Policy information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.cache._base import CacheModel


class OntapS3PolicyStatement(CacheModel):
    """OntapS3PolicyStatement sub-model for statements."""

    statements_actions: list[str] = Field(default_factory=list)
    statements_effect: str = ""
    statements_index: int = 0
    statements_resources: list[str] = Field(default_factory=list)
    statements_sid: str = ""


class OntapS3Policy(CacheModel):
    """OntapS3Policy information."""

    comment: str = ""
    name: str = ""
    read_only: bool = False
    statements: list[OntapS3PolicyStatement] = Field(default_factory=list)
    svm_name: str = ""
    svm_uuid: str = ""
