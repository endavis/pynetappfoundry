# ruff: noqa: N815
"""DiiAssetsGenericdevice information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class DiiAssetsGenericdevice(OntapModel):
    """DiiAssetsGenericdevice information."""

    simpleName: str = ""
    vendor: str = ""
    name: str = ""
    fcPortCount: int = 0
    model_: str = ""
    id: int = 0
    zones: list[str] = Field(default_factory=list)
    isActive: bool = False
    wwn: str = ""
