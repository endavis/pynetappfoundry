"""OntapSnaplockRetentionPolicy information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapSnaplockRetentionPolicySvm(OntapModel):
    """OntapSnaplockRetentionPolicySvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapSnaplockRetentionPolicy(OntapModel):
    """OntapSnaplockRetentionPolicy information."""

    name: str = ""
    retention_period: str = ""
    svm: OntapSnaplockRetentionPolicySvm = Field(default_factory=OntapSnaplockRetentionPolicySvm)
