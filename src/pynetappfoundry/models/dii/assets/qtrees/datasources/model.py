# ruff: noqa: N815
"""DiiAssetsQtreesDatasource information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class DiiAssetsQtreesDatasource(OntapModel):
    """DiiAssetsQtreesDatasource information."""

    vendorModelId: int = 0
    note: str = ""
    docLink: str = ""
    devices: list[str] = Field(default_factory=list)
    changeResponses: list[str] = Field(default_factory=list)
    packages: list[str] = Field(default_factory=list)
    lastSuccessfullyAcquired: str = ""
    resumeTime: str = ""
    pollStatus: str = ""
    dsTypeId: int = 0
    acquisitionUnit: str = ""
    vendor: str = ""
    statusText: str = ""
    name: str = ""
    activePatch: str = ""
    model_: str = ""
    id: int = 0
    config_: str = ""
    events: list[str] = Field(default_factory=list)
    status: str = ""
