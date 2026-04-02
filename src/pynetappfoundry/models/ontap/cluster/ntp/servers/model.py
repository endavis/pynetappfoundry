"""OntapNtpServer information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapNtpServerKey(OntapModel):
    """OntapNtpServerKey sub-model for key."""

    id: int = 0


class OntapNtpServer(OntapModel):
    """OntapNtpServer information."""

    authentication_enabled: bool = False
    key: OntapNtpServerKey = Field(default_factory=OntapNtpServerKey)
    server: str = ""
    version: str = ""
