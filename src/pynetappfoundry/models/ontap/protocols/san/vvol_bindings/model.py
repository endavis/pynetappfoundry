"""OntapVvolBinding information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapVvolBindingProtocolEndpoint(OntapModel):
    """OntapVvolBindingProtocolEndpoint sub-model for protocol_endpoint."""

    name: str = ""
    uuid: str = ""


class OntapVvolBindingSvm(OntapModel):
    """OntapVvolBindingSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapVvolBindingVvol(OntapModel):
    """OntapVvolBindingVvol sub-model for vvol."""

    name: str = ""
    uuid: str = ""


class OntapVvolBinding(OntapModel):
    """OntapVvolBinding information."""

    count: int = 0
    id: int = 0
    is_optimal: bool = False
    protocol_endpoint: OntapVvolBindingProtocolEndpoint = Field(
        default_factory=OntapVvolBindingProtocolEndpoint
    )
    secondary_id: str = ""
    svm: OntapVvolBindingSvm = Field(default_factory=OntapVvolBindingSvm)
    vvol: OntapVvolBindingVvol = Field(default_factory=OntapVvolBindingVvol)
