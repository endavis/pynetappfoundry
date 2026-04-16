# ruff: noqa: N815
"""DiiAssetsPortsFabric information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class DiiAssetsPortsFabric(OntapModel):
    """DiiAssetsPortsFabric information."""

    switchesCount: int = 0
    activeZoneSet: str = ""
    switches: list[str] = Field(default_factory=list)
    annotations: list[str] = Field(default_factory=list)
    isZoningEnabled: bool = False
    isActive: bool = False
    zonesCount: int = 0
    zones: list[str] = Field(default_factory=list)
    ports: list[str] = Field(default_factory=list)
    wwn: str = ""
    performance: str = ""
    datasources: list[str] = Field(default_factory=list)
    simpleName: str = ""
    name: str = ""
    isVsanEnabled: bool = False
    id: int = 0
    vsanId: str = ""
