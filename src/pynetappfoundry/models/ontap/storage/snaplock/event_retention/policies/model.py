"""OntapSnaplockRetentionPolicy information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class OntapSnaplockRetentionPolicy(OntapModel):
    """OntapSnaplockRetentionPolicy information."""

    name: str = ""
    retention_period: str = ""
    svm_name: str = ""
    svm_uuid: str = ""
