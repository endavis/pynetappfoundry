# ruff: noqa: N815
"""DiiAssetsZonemembersDevice information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class DiiAssetsZonemembersDevice(OntapModel):
    """DiiAssetsZonemembersDevice information."""

    simpleName: str = ""
    ip: str = ""
    name: str = ""
    description: str = ""
    self: str = ""
    id: str = ""
    type_: str = ""
    wwn: str = ""
