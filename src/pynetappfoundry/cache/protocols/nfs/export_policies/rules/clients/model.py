"""OntapExportClient information."""

from __future__ import annotations

from pynetappfoundry.cache._base import CacheModel


class OntapExportClient(CacheModel):
    """OntapExportClient information."""

    index: int = 0
    match: str = ""
    policy_id: int = 0
    svm_name: str = ""
    svm_uuid: str = ""
