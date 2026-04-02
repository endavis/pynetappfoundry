"""OntapCapacityPoolResponse information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel, OntapUUID


class OntapCapacityPoolResponseLicenseManager(OntapModel):
    """OntapCapacityPoolResponseLicenseManager sub-model for license_manager."""

    uuid: OntapUUID = ""


class OntapCapacityPoolResponseNodeNode(OntapModel):
    """OntapCapacityPoolResponseNodeNode sub-model for node."""

    name: str = ""
    uuid: str = ""


class OntapCapacityPoolResponseNode(OntapModel):
    """OntapCapacityPoolResponseNode sub-model for nodes."""

    node: OntapCapacityPoolResponseNodeNode = Field(
        default_factory=OntapCapacityPoolResponseNodeNode
    )
    used_size: int = 0


class OntapCapacityPoolResponse(OntapModel):
    """OntapCapacityPoolResponse information."""

    license_manager: OntapCapacityPoolResponseLicenseManager = Field(
        default_factory=OntapCapacityPoolResponseLicenseManager
    )
    nodes: list[OntapCapacityPoolResponseNode] = Field(default_factory=list)
    serial_number: str = ""
