"""OntapClusterNisService information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapClusterNisServiceStatus(OntapModel):
    """OntapClusterNisServiceStatus sub-model for status."""

    code: str = ""
    message: str = ""


class OntapClusterNisService(OntapModel):
    """OntapClusterNisService information."""

    server: str = ""
    status: OntapClusterNisServiceStatus = Field(default_factory=OntapClusterNisServiceStatus)
