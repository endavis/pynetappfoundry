# ruff: noqa: N815
"""DiiZonemember information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class DiiZonemember(OntapModel):
    """DiiZonemember information."""

    simpleName: str = ""
    zone: str = ""
    name: str = ""
    id: int = 0
    zoneStatus: str = ""
    type_: str = ""
    device: str = ""
    wwn: str = ""
