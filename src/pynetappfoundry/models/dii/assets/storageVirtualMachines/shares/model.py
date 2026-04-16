# ruff: noqa: N815
"""DiiAssetsStoragevirtualmachinesShare information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class DiiAssetsStoragevirtualmachinesShare(OntapModel):
    """DiiAssetsStoragevirtualmachinesShare information."""

    qtree: str = ""
    description: str = ""
    annotations: list[str] = Field(default_factory=list)
    storage: str = ""
    internalVolume: str = ""
    initiators: list[str] = Field(default_factory=list)
    path: str = ""
    protocol: str = ""
    storageVirtualMachine: str = ""
    datasources: list[str] = Field(default_factory=list)
    simpleName: str = ""
    name: str = ""
    id: int = 0
    storagePool: str = ""
    applications: list[str] = Field(default_factory=list)
