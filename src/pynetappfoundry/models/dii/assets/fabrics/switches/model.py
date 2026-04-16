# ruff: noqa: N815
"""DiiAssetsFabricsSwitche information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class DiiAssetsFabricsSwitche(OntapModel):
    """DiiAssetsFabricsSwitche information."""

    isSanRouteEnabled: bool = False
    switchRole: str = ""
    switchType: str = ""
    annotations: list[str] = Field(default_factory=list)
    switchStatus: str = ""
    isActive: bool = False
    ports: list[str] = Field(default_factory=list)
    wwn: str = ""
    vendor: str = ""
    isNpv: bool = False
    model_: str = ""
    managementUrl: str = ""
    id: int = 0
    domainIdType: str = ""
    firmware: str = ""
    serialNumber: str = ""
    ip: str = ""
    priority: str = ""
    zones: list[str] = Field(default_factory=list)
    domainId: str = ""
    performance: str = ""
    datasources: list[str] = Field(default_factory=list)
    simpleName: str = ""
    createTime: str = ""
    fabric: str = ""
    name: str = ""
    isVsanEnabled: bool = False
    applications: list[str] = Field(default_factory=list)
