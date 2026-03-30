"""OntapCapacityPoolResponse information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel, OntapUUID


class OntapCapacityPoolResponseNode(OntapModel):
    """OntapCapacityPoolResponseNode sub-model for nodes."""

    nodes_node_name: str = ""
    nodes_node_uuid: str = ""
    nodes_used_size: int = 0


class OntapCapacityPoolResponse(OntapModel):
    """OntapCapacityPoolResponse information."""

    license_manager_uuid: OntapUUID = ""
    nodes: list[OntapCapacityPoolResponseNode] = Field(default_factory=list)
    serial_number: str = ""
