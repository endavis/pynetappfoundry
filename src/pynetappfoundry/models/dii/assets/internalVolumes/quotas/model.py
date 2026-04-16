# ruff: noqa: N815
"""DiiAssetsInternalvolumesQuota information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class DiiAssetsInternalvolumesQuota(OntapModel):
    """DiiAssetsInternalvolumesQuota information."""

    softFileLimit: float = 0.0
    qtree: str = ""
    simpleName: str = ""
    name: str = ""
    usedFiles: float = 0.0
    annotations: list[str] = Field(default_factory=list)
    hardFileLimit: float = 0.0
    id: int = 0
    internalVolume: str = ""
    type_: str = ""
    userOrGroupTarget: str = ""
    capacity: str = ""
