# ruff: noqa: N815
"""DiiAssetsHostsPort information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class DiiAssetsHostsPort(OntapModel):
    """DiiAssetsHostsPort information."""

    role: str = ""
    portState: str = ""
    annotations: list[str] = Field(default_factory=list)
    type_: str = ""
    gbicType: str = ""
    isActive: bool = False
    deviceName: str = ""
    speed: int = 0
    wwn: str = ""
    blade: int = 0
    portIndex: int = 0
    id: int = 0
    fc4Protocol: str = ""
    deviceType: str = ""
    classOfService: str = ""
    controller: str = ""
    nodeWwn: str = ""
    fabrics: list[str] = Field(default_factory=list)
    performance: str = ""
    connectedPorts: list[str] = Field(default_factory=list)
    datasources: list[str] = Field(default_factory=list)
    simpleName: str = ""
    name: str = ""
    device: str = ""
    applications: list[str] = Field(default_factory=list)
