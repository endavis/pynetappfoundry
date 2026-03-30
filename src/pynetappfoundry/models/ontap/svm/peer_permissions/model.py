"""OntapSvmPeerPermission information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapSvmPeerPermission(OntapModel):
    """OntapSvmPeerPermission information."""

    applications: list[str] = Field(default_factory=list)
    cluster_peer_name: str = ""
    cluster_peer_uuid: str = ""
    svm_name: str = ""
    svm_uuid: str = ""
