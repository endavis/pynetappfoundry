"""OntapNisService information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapNisServiceBindingDetail(OntapModel):
    """OntapNisServiceBindingDetail sub-model for binding_details."""

    binding_details_server: str = ""
    binding_details_status_code: str = ""
    binding_details_status_message: str = ""


class OntapNisService(OntapModel):
    """OntapNisService information."""

    binding_details: list[OntapNisServiceBindingDetail] = Field(default_factory=list)
    bound_servers: list[str] = Field(default_factory=list)
    domain: str = ""
    servers: list[str] = Field(default_factory=list)
    svm_name: str = ""
    svm_uuid: str = ""
