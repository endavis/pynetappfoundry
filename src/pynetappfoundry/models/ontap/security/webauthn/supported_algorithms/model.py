"""OntapSupportedAlgorithms information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapSupportedAlgorithmsAlgorithm(OntapModel):
    """OntapSupportedAlgorithmsAlgorithm sub-model for algorithm."""

    id: int = 0
    name: str = ""
    type_: str = ""


class OntapSupportedAlgorithmsOwner(OntapModel):
    """OntapSupportedAlgorithmsOwner sub-model for owner."""

    name: str = ""
    uuid: str = ""


class OntapSupportedAlgorithms(OntapModel):
    """OntapSupportedAlgorithms information."""

    algorithm: OntapSupportedAlgorithmsAlgorithm = Field(
        default_factory=OntapSupportedAlgorithmsAlgorithm
    )
    owner: OntapSupportedAlgorithmsOwner = Field(default_factory=OntapSupportedAlgorithmsOwner)
    scope: str = ""
