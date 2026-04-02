"""OntapExportClient information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapExportClientPolicy(OntapModel):
    """OntapExportClientPolicy sub-model for policy."""

    id: int = 0


class OntapExportClientSvm(OntapModel):
    """OntapExportClientSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapExportClient(OntapModel):
    """OntapExportClient information."""

    index: int = 0
    match: str = ""
    policy: OntapExportClientPolicy = Field(default_factory=OntapExportClientPolicy)
    svm: OntapExportClientSvm = Field(default_factory=OntapExportClientSvm)
