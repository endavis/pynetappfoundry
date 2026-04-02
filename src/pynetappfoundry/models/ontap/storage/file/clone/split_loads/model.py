"""OntapSplitLoad information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapSplitLoadLoad(OntapModel):
    """OntapSplitLoadLoad sub-model for load."""

    allowable: int = 0
    current: int = 0
    maximum: int = 0
    token_reserved: int = 0


class OntapSplitLoadNode(OntapModel):
    """OntapSplitLoadNode sub-model for node."""

    name: str = ""
    uuid: str = ""


class OntapSplitLoad(OntapModel):
    """OntapSplitLoad information."""

    load: OntapSplitLoadLoad = Field(default_factory=OntapSplitLoadLoad)
    node: OntapSplitLoadNode = Field(default_factory=OntapSplitLoadNode)
