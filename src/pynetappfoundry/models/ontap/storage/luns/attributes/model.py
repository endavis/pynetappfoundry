"""OntapLunAttribute information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class OntapLunAttribute(OntapModel):
    """OntapLunAttribute information."""

    lun_uuid: str = ""
    name: str = ""
    value: str = ""
