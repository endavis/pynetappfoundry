"""OntapLunMap information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.cache._base import CacheModel


class OntapLunMapReportingNode(CacheModel):
    """OntapLunMapReportingNode sub-model for reporting_nodes."""

    reporting_nodes_name: str = ""
    reporting_nodes_uuid: str = ""


class OntapLunMap(CacheModel):
    """OntapLunMap information."""

    igroup_initiators: list[str] = Field(default_factory=list)
    igroup_name: str = ""
    igroup_os_type: str = ""
    igroup_protocol: str = ""
    igroup_replicated: bool = False
    igroup_uuid: str = ""
    logical_unit_number: int = 0
    lun_name: str = ""
    lun_node_name: str = ""
    lun_node_uuid: str = ""
    lun_smbc_replicated: bool = False
    lun_uuid: str = ""
    reporting_nodes: list[OntapLunMapReportingNode] = Field(default_factory=list)
    svm_name: str = ""
    svm_uuid: str = ""
