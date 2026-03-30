"""OntapNdmpPassword information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class OntapNdmpPassword(OntapModel):
    """OntapNdmpPassword information."""

    password: str = ""
    svm_name: str = ""
    svm_uuid: str = ""
    user: str = ""
