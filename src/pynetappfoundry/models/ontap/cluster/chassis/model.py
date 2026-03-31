"""OntapChassis information."""

from __future__ import annotations

from typing import Any

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapChassisFru(OntapModel):
    """OntapChassisFru sub-model for frus."""

    id: str = ""
    state: str = ""
    type: str = ""


class OntapChassisNode(OntapModel):
    """OntapChassisNode sub-model for nodes."""

    name: str = ""
    pcis_cards: list[dict[str, Any]] = Field(default_factory=list)
    position: str = ""
    usbs_enabled: bool = False
    usbs_ports: list[dict[str, Any]] = Field(default_factory=list)
    usbs_supported: bool = False
    uuid: str = ""


class OntapChassisShelve(OntapModel):
    """OntapChassisShelve sub-model for shelves."""

    uid: str = ""


class OntapChassis(OntapModel):
    """OntapChassis information."""

    frus: list[OntapChassisFru] = Field(default_factory=list)
    id: str = ""
    nodes: list[OntapChassisNode] = Field(default_factory=list)
    shelves: list[OntapChassisShelve] = Field(default_factory=list)
    state: str = ""
