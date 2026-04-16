# ruff: noqa: N815
"""DiiAssetsInternalvolumesComputeresource information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class DiiAssetsInternalvolumesComputeresource(OntapModel):
    """DiiAssetsInternalvolumesComputeresource information."""

    performance: str = ""
    simpleName: str = ""
    fileSystems: list[str] = Field(default_factory=list)
    paths: list[str] = Field(default_factory=list)
    ip: str = ""
    name: str = ""
    storageResources: list[str] = Field(default_factory=list)
    id: int = 0
    ports: list[str] = Field(default_factory=list)
    resourceType: str = ""
