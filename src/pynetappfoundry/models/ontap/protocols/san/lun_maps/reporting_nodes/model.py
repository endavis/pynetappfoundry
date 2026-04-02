"""OntapLunMapReportingNode information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapLunMapReportingNodeIgroup(OntapModel):
    """OntapLunMapReportingNodeIgroup sub-model for igroup."""

    uuid: str = ""


class OntapLunMapReportingNodeLun(OntapModel):
    """OntapLunMapReportingNodeLun sub-model for lun."""

    uuid: str = ""


class OntapLunMapReportingNode(OntapModel):
    """OntapLunMapReportingNode information."""

    igroup: OntapLunMapReportingNodeIgroup = Field(default_factory=OntapLunMapReportingNodeIgroup)
    lun: OntapLunMapReportingNodeLun = Field(default_factory=OntapLunMapReportingNodeLun)
    name: str = ""
    uuid: str = ""
