"""OntapNisService information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapNisServiceBindingDetailStatus(OntapModel):
    """OntapNisServiceBindingDetailStatus sub-model for status."""

    code: str = ""
    message: str = ""


class OntapNisServiceBindingDetail(OntapModel):
    """OntapNisServiceBindingDetail sub-model for binding_details."""

    server: str = ""
    status: OntapNisServiceBindingDetailStatus = Field(
        default_factory=OntapNisServiceBindingDetailStatus
    )


class OntapNisServiceSvm(OntapModel):
    """OntapNisServiceSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapNisService(OntapModel):
    """OntapNisService information."""

    binding_details: list[OntapNisServiceBindingDetail] = Field(default_factory=list)
    bound_servers: list[str] = Field(default_factory=list)
    domain: str = ""
    servers: list[str] = Field(default_factory=list)
    svm: OntapNisServiceSvm = Field(default_factory=OntapNisServiceSvm)
