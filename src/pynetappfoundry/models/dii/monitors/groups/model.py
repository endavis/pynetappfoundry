# ruff: noqa: N815
"""DiiMonitorsGroup information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel, OntapUUID


class DiiMonitorsGroupMonitorinfo(OntapModel):
    """DiiMonitorsGroupMonitorinfo sub-model for monitorInfo."""

    monitorCount: int = 0
    monitorsLink: str = ""
    monitors: list[str] = Field(default_factory=list)


class DiiMonitorsGroup(OntapModel):
    """DiiMonitorsGroup information."""

    groupType: str = ""
    created: int = 0
    name: str = ""
    monitorInfo: DiiMonitorsGroupMonitorinfo = Field(default_factory=DiiMonitorsGroupMonitorinfo)
    self: str = ""
    id: OntapUUID = ""
    updated: int = 0
