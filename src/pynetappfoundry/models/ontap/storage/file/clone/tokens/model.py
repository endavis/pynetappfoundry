"""OntapToken information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapTokenExpiryTime(OntapModel):
    """OntapTokenExpiryTime sub-model for expiry_time."""

    left: str = ""
    limit: str = ""


class OntapTokenNode(OntapModel):
    """OntapTokenNode sub-model for node."""

    name: str = ""
    uuid: str = ""


class OntapToken(OntapModel):
    """OntapToken information."""

    expiry_time: OntapTokenExpiryTime = Field(default_factory=OntapTokenExpiryTime)
    node: OntapTokenNode = Field(default_factory=OntapTokenNode)
    reserve_size: int = 0
    uuid: str = ""
