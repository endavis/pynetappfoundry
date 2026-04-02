"""OntapNetgroupFile information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapNetgroupFileSvm(OntapModel):
    """OntapNetgroupFileSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapNetgroupFile(OntapModel):
    """OntapNetgroupFile information."""

    file_size: int = 0
    hash_value: str = ""
    hash_value_by_host: str = ""
    svm: OntapNetgroupFileSvm = Field(default_factory=OntapNetgroupFileSvm)
    timestamp: str = ""
