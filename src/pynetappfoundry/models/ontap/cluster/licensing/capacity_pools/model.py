"""OntapCapacityPoolResponse information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel, OntapUUID


class OntapCapacityPoolResponseNode(OntapModel):
    """OntapCapacityPoolResponseNode sub-model for nodes."""

    node_name: str = ""
    node_uuid: str = ""
    used_size: int = 0


class OntapCapacityPoolResponse(OntapModel):
    """OntapCapacityPoolResponse information."""

    license_manager_uuid: OntapUUID = ""
    nodes: list[OntapCapacityPoolResponseNode] = Field(default_factory=list)
    serial_number: str = ""
