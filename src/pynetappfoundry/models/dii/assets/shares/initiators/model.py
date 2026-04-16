"""DiiShareinitiator information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class DiiShareinitiator(OntapModel):
    """DiiShareinitiator information."""

    initiator: str = ""
    permission: str = ""
