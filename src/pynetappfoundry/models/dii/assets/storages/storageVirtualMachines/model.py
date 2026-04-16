# ruff: noqa: N815
"""DiiAssetsStoragesStoragevirtualmachine information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class DiiAssetsStoragesStoragevirtualmachine(OntapModel):
    """DiiAssetsStoragesStoragevirtualmachine information."""

    internalVolumeLimit: int = 0
    internalVolumes: list[str] = Field(default_factory=list)
    volumes: list[str] = Field(default_factory=list)
    guidKey: str = ""
    annotations: list[str] = Field(default_factory=list)
    storage: str = ""
    type_: str = ""
    ipSpace: str = ""
    uuid: str = ""
    capacity: str = ""
    qtrees: list[str] = Field(default_factory=list)
    shares: list[str] = Field(default_factory=list)
    performance: str = ""
    storagePools: list[str] = Field(default_factory=list)
    simpleName: str = ""
    name: str = ""
    comment: str = ""
    id: int = 0
    state: str = ""
    protocols: str = ""
