# ruff: noqa: N815
"""DiiAssetsStoragevirtualmachinesQtree information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class DiiAssetsStoragevirtualmachinesQtree(OntapModel):
    """DiiAssetsStoragevirtualmachinesQtree information."""

    sourceReplica: str = ""
    quotas: list[str] = Field(default_factory=list)
    quotaCapacity: str = ""
    volumes: list[str] = Field(default_factory=list)
    annotations: list[str] = Field(default_factory=list)
    storage: str = ""
    internalVolume: str = ""
    type_: str = ""
    securityStyle: str = ""
    isOplocksEnabled: bool = False
    shares: list[str] = Field(default_factory=list)
    storageVirtualMachine: str = ""
    performance: str = ""
    datasources: list[str] = Field(default_factory=list)
    simpleName: str = ""
    statusText: str = ""
    name: str = ""
    id: int = 0
    applications: list[str] = Field(default_factory=list)
