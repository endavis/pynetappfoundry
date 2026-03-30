"""OntapLunMapReportingNode information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class OntapLunMapReportingNode(OntapModel):
    """OntapLunMapReportingNode information."""

    igroup_uuid: str = ""
    lun_uuid: str = ""
    name: str = ""
    uuid: str = ""
