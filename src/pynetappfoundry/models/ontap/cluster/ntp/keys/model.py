"""OntapNtpKey information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class OntapNtpKey(OntapModel):
    """OntapNtpKey information."""

    digest_type: str = ""
    id: int = 0
    value: str = ""
