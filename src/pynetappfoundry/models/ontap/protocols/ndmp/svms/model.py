"""OntapNdmpSvm information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapNdmpSvmSvm(OntapModel):
    """OntapNdmpSvmSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapNdmpSvm(OntapModel):
    """OntapNdmpSvm information."""

    authentication_types: list[str] = Field(default_factory=list)
    enabled: bool = False
    svm: OntapNdmpSvmSvm = Field(default_factory=OntapNdmpSvmSvm)
