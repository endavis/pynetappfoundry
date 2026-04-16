# ruff: noqa: N815
"""DiiAssetsDisksStorageresource information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class DiiAssetsDisksStorageresource(OntapModel):
    """DiiAssetsDisksStorageresource information."""

    dataStores: list[str] = Field(default_factory=list)
    performance: str = ""
    storagePools: list[str] = Field(default_factory=list)
    simpleName: str = ""
    name: str = ""
    computeResources: list[str] = Field(default_factory=list)
    isThinProvisioned: bool = False
    id: int = 0
    storage: str = ""
    capacity: str = ""
    resourceType: str = ""
    applications: list[str] = Field(default_factory=list)
