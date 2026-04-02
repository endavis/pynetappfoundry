"""OntapSoftwareHistory information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapSoftwareHistoryNode(OntapModel):
    """OntapSoftwareHistoryNode sub-model for node."""

    name: str = ""
    uuid: str = ""


class OntapSoftwareHistory(OntapModel):
    """OntapSoftwareHistory information."""

    end_time: str = ""
    from_version: str = ""
    node: OntapSoftwareHistoryNode = Field(default_factory=OntapSoftwareHistoryNode)
    start_time: str = ""
    state: str = ""
    to_version: str = ""
