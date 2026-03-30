"""OntapNameMapping information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class OntapNameMapping(OntapModel):
    """OntapNameMapping information."""

    client_match: str = ""
    direction: str = ""
    index: int = 0
    pattern: str = ""
    replacement: str = ""
    svm_name: str = ""
    svm_uuid: str = ""
