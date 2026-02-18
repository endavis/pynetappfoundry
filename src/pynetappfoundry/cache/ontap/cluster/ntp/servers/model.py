"""OntapNtpServer information."""

from __future__ import annotations

from pynetappfoundry.cache._base import CacheModel


class OntapNtpServer(CacheModel):
    """OntapNtpServer information."""

    authentication_enabled: bool = False
    key_id: int = 0
    server: str = ""
    version: str = ""
