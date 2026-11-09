"""OntapClusterNisService information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapClusterNisServiceBindingDetailStatus(OntapModel):
    """OntapClusterNisServiceBindingDetailStatus sub-model for status."""

    code: str = ""
    message: str = ""


class OntapClusterNisServiceBindingDetail(OntapModel):
    """OntapClusterNisServiceBindingDetail sub-model for binding_details."""

    server: str = ""
    status: OntapClusterNisServiceBindingDetailStatus = Field(
        default_factory=OntapClusterNisServiceBindingDetailStatus
    )


class OntapClusterNisService(OntapModel):
    """OntapClusterNisService information."""

    binding_details: list[OntapClusterNisServiceBindingDetail] = Field(default_factory=list)
    bound_servers: list[str] = Field(default_factory=list)
    domain: str = ""
    servers: list[str] = Field(default_factory=list)
