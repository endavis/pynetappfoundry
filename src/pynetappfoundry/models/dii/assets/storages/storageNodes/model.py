# ruff: noqa: N815
"""DiiAssetsStoragesStoragenode information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class DiiAssetsStoragesStoragenode(OntapModel):
    """DiiAssetsStoragesStoragenode information."""

    cache: str = ""
    internalVolumes: list[str] = Field(default_factory=list)
    serialNumber: str = ""
    memory: str = ""
    volumes: list[str] = Field(default_factory=list)
    annotations: list[str] = Field(default_factory=list)
    nodeVersion: str = ""
    storage: str = ""
    monitoring: str = ""
    ports: list[str] = Field(default_factory=list)
    uuid: str = ""
    performance: str = ""
    numberOfProcessors: int = 0
    risks: list[str] = Field(default_factory=list)
    partner: str = ""
    datasources: list[str] = Field(default_factory=list)
    storagePools: list[str] = Field(default_factory=list)
    simpleName: str = ""
    name: str = ""
    model_: str = ""
    id: int = 0
    state: str = ""
