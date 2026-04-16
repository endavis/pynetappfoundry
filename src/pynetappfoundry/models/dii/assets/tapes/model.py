# ruff: noqa: N815
"""DiiAssetsTape information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class DiiAssetsTape(OntapModel):
    """DiiAssetsTape information."""

    serialNumber: str = ""
    simpleName: str = ""
    vendor: str = ""
    ip: str = ""
    name: str = ""
    fcPortCount: int = 0
    id: int = 0
    isActive: bool = False
