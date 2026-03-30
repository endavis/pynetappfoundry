"""OntapIpServicePolicy information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapIpServicePolicy(OntapModel):
    """OntapIpServicePolicy information."""

    ipspace_name: str = ""
    ipspace_uuid: str = ""
    is_built_in: bool = False
    name: str = ""
    scope: str = ""
    services: list[str] = Field(default_factory=list)
    svm_name: str = ""
    svm_uuid: str = ""
    uuid: str = ""
