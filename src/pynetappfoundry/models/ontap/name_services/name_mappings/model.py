"""OntapNameMapping information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapNameMappingSvm(OntapModel):
    """OntapNameMappingSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapNameMapping(OntapModel):
    """OntapNameMapping information."""

    client_match: str = ""
    direction: str = ""
    index: int = 0
    pattern: str = ""
    replacement: str = ""
    svm: OntapNameMappingSvm = Field(default_factory=OntapNameMappingSvm)
