"""OntapNetgroupFile information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class OntapNetgroupFile(OntapModel):
    """OntapNetgroupFile information."""

    file_size: int = 0
    hash_value: str = ""
    hash_value_by_host: str = ""
    svm_name: str = ""
    svm_uuid: str = ""
    timestamp: str = ""
