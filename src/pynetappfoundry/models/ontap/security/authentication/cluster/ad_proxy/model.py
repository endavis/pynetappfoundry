"""OntapClusterAdProxy information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class OntapClusterAdProxy(OntapModel):
    """OntapClusterAdProxy information."""

    svm_name: str = ""
    svm_uuid: str = ""
