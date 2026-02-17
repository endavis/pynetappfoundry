"""OntapNtpKey information."""

from __future__ import annotations

from pynetappfoundry.cache._base import CacheModel


class OntapNtpKey(CacheModel):
    """OntapNtpKey information."""

    digest_type: str = ""
    id: int = 0
    value: str = ""
