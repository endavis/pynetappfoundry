# ruff: noqa: N815
"""DiiAssetsVirtualmachinesFilesystem information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class DiiAssetsVirtualmachinesFilesystem(OntapModel):
    """DiiAssetsVirtualmachinesFilesystem information."""

    vmdks: list[str] = Field(default_factory=list)
    simpleName: str = ""
    name: str = ""
    storageResources: list[str] = Field(default_factory=list)
    id: int = 0
    type_: str = ""
    computeResource: str = ""
    capacity: str = ""
