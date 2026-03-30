"""OntapNtpServer information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class OntapNtpServer(OntapModel):
    """OntapNtpServer information."""

    authentication_enabled: bool = False
    key_id: int = 0
    server: str = ""
    version: str = ""
