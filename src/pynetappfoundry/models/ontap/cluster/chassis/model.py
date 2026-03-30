"""OntapChassis information."""

from __future__ import annotations

from typing import Any

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapChassisFru(OntapModel):
    """OntapChassisFru sub-model for frus."""

    frus_id: str = ""
    frus_state: str = ""
    frus_type: str = ""


class OntapChassisNode(OntapModel):
    """OntapChassisNode sub-model for nodes."""

    nodes_name: str = ""
    nodes_pcis_cards: list[dict[str, Any]] = Field(default_factory=list)
    nodes_position: str = ""
    nodes_usbs_enabled: bool = False
    nodes_usbs_ports: list[dict[str, Any]] = Field(default_factory=list)
    nodes_usbs_supported: bool = False
    nodes_uuid: str = ""


class OntapChassisShelve(OntapModel):
    """OntapChassisShelve sub-model for shelves."""

    shelves_uid: str = ""


class OntapChassis(OntapModel):
    """OntapChassis information."""

    frus: list[OntapChassisFru] = Field(default_factory=list)
    id: str = ""
    nodes: list[OntapChassisNode] = Field(default_factory=list)
    shelves: list[OntapChassisShelve] = Field(default_factory=list)
    state: str = ""
