"""OntapSnaplockRetentionPolicy information."""

from __future__ import annotations

from pynetappfoundry.cache._base import CacheModel


class OntapSnaplockRetentionPolicy(CacheModel):
    """OntapSnaplockRetentionPolicy information."""

    name: str = ""
    retention_period: str = ""
    svm_name: str = ""
    svm_uuid: str = ""
