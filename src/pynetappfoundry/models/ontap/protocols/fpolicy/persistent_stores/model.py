"""OntapFpolicyPersistentStore information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapFpolicyPersistentStoreSvm(OntapModel):
    """OntapFpolicyPersistentStoreSvm sub-model for svm."""

    uuid: str = ""


class OntapFpolicyPersistentStore(OntapModel):
    """OntapFpolicyPersistentStore information."""

    autosize_mode: str = ""
    name: str = ""
    size: int = 0
    svm: OntapFpolicyPersistentStoreSvm = Field(default_factory=OntapFpolicyPersistentStoreSvm)
    volume: str = ""
