# ruff: noqa: N815
"""DiiAssetsVirtualmachinesPath information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class DiiAssetsVirtualmachinesPath(OntapModel):
    """DiiAssetsVirtualmachinesPath information."""

    hostPortCount: int = 0
    connectionCount: int = 0
    source: str = ""
    isNonRedundant: bool = False
    pathType: str = ""
    target: str = ""
    fabrics: list[str] = Field(default_factory=list)
    isBackendPath: bool = False
    simpleName: str = ""
    sessionCount: int = 0
    storagePortCount: int = 0
    hopCount: str = ""
    name: str = ""
    id: int = 0
    since: str = ""
    storagePorts: list[str] = Field(default_factory=list)
    applications: list[str] = Field(default_factory=list)
