"""OntapCifsSearchPath information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapCifsSearchPathSvm(OntapModel):
    """OntapCifsSearchPathSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapCifsSearchPath(OntapModel):
    """OntapCifsSearchPath information."""

    index: int = 0
    path: str = ""
    svm: OntapCifsSearchPathSvm = Field(default_factory=OntapCifsSearchPathSvm)
