# ruff: noqa: N815
"""DiiIscsinetworkportal information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class DiiIscsinetworkportal(OntapModel):
    """DiiIscsinetworkportal information."""

    nicName: str = ""
    simpleName: str = ""
    port: str = ""
    ip: str = ""
    portalGroupTag: str = ""
    name: str = ""
    id: int = 0
    device: str = ""
    portalGroup: str = ""
