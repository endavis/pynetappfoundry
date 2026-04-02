"""OntapLunMap information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapLunMapIgroup(OntapModel):
    """OntapLunMapIgroup sub-model for igroup."""

    initiators: list[str] = Field(default_factory=list)
    name: str = ""
    os_type: str = ""
    protocol: str = ""
    replicated: bool = False
    uuid: str = ""


class OntapLunMapLunNode(OntapModel):
    """OntapLunMapLunNode sub-model for node."""

    name: str = ""
    uuid: str = ""


class OntapLunMapLunSmbc(OntapModel):
    """OntapLunMapLunSmbc sub-model for smbc."""

    replicated: bool = False


class OntapLunMapLun(OntapModel):
    """OntapLunMapLun sub-model for lun."""

    name: str = ""
    node: OntapLunMapLunNode = Field(default_factory=OntapLunMapLunNode)
    smbc: OntapLunMapLunSmbc = Field(default_factory=OntapLunMapLunSmbc)
    uuid: str = ""


class OntapLunMapReportingNode(OntapModel):
    """OntapLunMapReportingNode sub-model for reporting_nodes."""

    name: str = ""
    uuid: str = ""


class OntapLunMapSvm(OntapModel):
    """OntapLunMapSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapLunMap(OntapModel):
    """OntapLunMap information."""

    igroup: OntapLunMapIgroup = Field(default_factory=OntapLunMapIgroup)
    logical_unit_number: int = 0
    lun: OntapLunMapLun = Field(default_factory=OntapLunMapLun)
    reporting_nodes: list[OntapLunMapReportingNode] = Field(default_factory=list)
    svm: OntapLunMapSvm = Field(default_factory=OntapLunMapSvm)
