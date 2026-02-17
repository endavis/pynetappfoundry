"""OntapLunMapReportingNode information."""

from __future__ import annotations

from pynetappfoundry.cache._base import CacheModel


class OntapLunMapReportingNode(CacheModel):
    """OntapLunMapReportingNode information."""

    igroup_uuid: str = ""
    lun_uuid: str = ""
    name: str = ""
    uuid: str = ""
