"""OntapFpolicyPersistentStore information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class OntapFpolicyPersistentStore(OntapModel):
    """OntapFpolicyPersistentStore information."""

    autosize_mode: str = ""
    name: str = ""
    size: int = 0
    svm_uuid: str = ""
    volume: str = ""
