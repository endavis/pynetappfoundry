# ruff: noqa: N815
"""DiiAssetsVolumesDatastore information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class DiiAssetsVolumesDatastore(OntapModel):
    """DiiAssetsVolumesDatastore information."""

    virtualCenterIp: str = ""
    performance: str = ""
    vmdks: list[str] = Field(default_factory=list)
    datasources: list[str] = Field(default_factory=list)
    simpleName: str = ""
    hosts: list[str] = Field(default_factory=list)
    name: str = ""
    storageResources: list[str] = Field(default_factory=list)
    annotations: list[str] = Field(default_factory=list)
    id: int = 0
    virtualMachines: list[str] = Field(default_factory=list)
    capacity: str = ""
