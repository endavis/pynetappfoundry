"""OntapSvmPeerPermission information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapSvmPeerPermissionClusterPeer(OntapModel):
    """OntapSvmPeerPermissionClusterPeer sub-model for cluster_peer."""

    name: str = ""
    uuid: str = ""


class OntapSvmPeerPermissionSvm(OntapModel):
    """OntapSvmPeerPermissionSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapSvmPeerPermission(OntapModel):
    """OntapSvmPeerPermission information."""

    applications: list[str] = Field(default_factory=list)
    cluster_peer: OntapSvmPeerPermissionClusterPeer = Field(
        default_factory=OntapSvmPeerPermissionClusterPeer
    )
    svm: OntapSvmPeerPermissionSvm = Field(default_factory=OntapSvmPeerPermissionSvm)
