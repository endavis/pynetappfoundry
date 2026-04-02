"""OntapSvmPeer information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapSvmPeerPeerCluster(OntapModel):
    """OntapSvmPeerPeerCluster sub-model for cluster."""

    name: str = ""
    uuid: str = ""


class OntapSvmPeerPeerSvm(OntapModel):
    """OntapSvmPeerPeerSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapSvmPeerPeer(OntapModel):
    """OntapSvmPeerPeer sub-model for peer."""

    cluster: OntapSvmPeerPeerCluster = Field(default_factory=OntapSvmPeerPeerCluster)
    svm: OntapSvmPeerPeerSvm = Field(default_factory=OntapSvmPeerPeerSvm)


class OntapSvmPeerSvm(OntapModel):
    """OntapSvmPeerSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapSvmPeer(OntapModel):
    """OntapSvmPeer information."""

    applications: list[str] = Field(default_factory=list)
    force: bool = False
    name: str = ""
    peer: OntapSvmPeerPeer = Field(default_factory=OntapSvmPeerPeer)
    state: str = ""
    svm: OntapSvmPeerSvm = Field(default_factory=OntapSvmPeerSvm)
    uuid: str = ""
