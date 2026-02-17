"""OntapNetgroupFile information."""

from __future__ import annotations

from pynetappfoundry.cache._base import CacheModel


class OntapNetgroupFile(CacheModel):
    """OntapNetgroupFile information."""

    file_size: int = 0
    hash_value: str = ""
    hash_value_by_host: str = ""
    svm_name: str = ""
    svm_uuid: str = ""
    timestamp: str = ""
