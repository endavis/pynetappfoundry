# ruff: noqa: N815
"""DiiAssetsPathsApplication information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class DiiAssetsPathsApplication(OntapModel):
    """DiiAssetsPathsApplication information."""

    shares: list[str] = Field(default_factory=list)
    performance: str = ""
    simpleName: str = ""
    name: str = ""
    storageResources: list[str] = Field(default_factory=list)
    computeResources: list[str] = Field(default_factory=list)
    id: int = 0
    priority: str = ""
    ignoreShareViolations: bool = False
    qtrees: list[str] = Field(default_factory=list)
