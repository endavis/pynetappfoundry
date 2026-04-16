# ruff: noqa: N815
"""DiiAssetsStoragesDisk information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class DiiAssetsStoragesDisk(OntapModel):
    """DiiAssetsStoragesDisk information."""

    role: str = ""
    serialNumber: str = ""
    storageResources: list[str] = Field(default_factory=list)
    annotations: list[str] = Field(default_factory=list)
    storage: str = ""
    type_: str = ""
    speed: str = ""
    diskSize: str = ""
    backendVolumes: list[str] = Field(default_factory=list)
    performance: str = ""
    storagePools: list[str] = Field(default_factory=list)
    datasources: list[str] = Field(default_factory=list)
    simpleName: str = ""
    diskGroup: str = ""
    vendor: str = ""
    name: str = ""
    location: str = ""
    model_: str = ""
    id: int = 0
    isVirtual: bool = False
    status: str = ""
