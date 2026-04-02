"""OntapNdmpPassword information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapNdmpPasswordSvm(OntapModel):
    """OntapNdmpPasswordSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapNdmpPassword(OntapModel):
    """OntapNdmpPassword information."""

    password: str = ""
    svm: OntapNdmpPasswordSvm = Field(default_factory=OntapNdmpPasswordSvm)
    user: str = ""
