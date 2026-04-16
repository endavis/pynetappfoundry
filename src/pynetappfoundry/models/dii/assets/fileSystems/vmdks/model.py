# ruff: noqa: N815
"""DiiAssetsFilesystemsVmdk information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class DiiAssetsFilesystemsVmdk(OntapModel):
    """DiiAssetsFilesystemsVmdk information."""

    virtualMachine: str = ""
    performance: str = ""
    datasources: list[str] = Field(default_factory=list)
    simpleName: str = ""
    name: str = ""
    storageResources: list[str] = Field(default_factory=list)
    dataStore: str = ""
    annotations: list[str] = Field(default_factory=list)
    id: int = 0
    isRdm: bool = False
    type_: str = ""
    capacity: str = ""
