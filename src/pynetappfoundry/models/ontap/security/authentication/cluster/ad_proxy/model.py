"""OntapClusterAdProxy information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapClusterAdProxySvm(OntapModel):
    """OntapClusterAdProxySvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapClusterAdProxy(OntapModel):
    """OntapClusterAdProxy information."""

    svm: OntapClusterAdProxySvm = Field(default_factory=OntapClusterAdProxySvm)
