# ruff: noqa: N815
"""DiiAssetsStoragesZone information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class DiiAssetsStoragesZone(OntapModel):
    """DiiAssetsStoragesZone information."""

    simpleName: str = ""
    fabric: str = ""
    zoneMembers: list[str] = Field(default_factory=list)
    name: str = ""
    isVsanEnabled: bool = False
    id: int = 0
    vsanId: str = ""
    initiators: int = 0
    type_: str = ""
    targets: int = 0
    wwn: str = ""
