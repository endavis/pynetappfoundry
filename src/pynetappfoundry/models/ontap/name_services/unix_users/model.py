"""OntapUnixUser information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class OntapUnixUser(OntapModel):
    """OntapUnixUser information."""

    full_name: str = ""
    id: int = 0
    name: str = ""
    primary_gid: int = 0
    skip_name_validation: bool = False
    svm_name: str = ""
    svm_uuid: str = ""
