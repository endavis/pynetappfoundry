"""OntapSvmPeer information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.cache._base import CacheModel


class OntapSvmPeer(CacheModel):
    """OntapSvmPeer information."""

    applications: list[str] = Field(default_factory=list)
    force: bool = False
    name: str = ""
    peer_cluster_name: str = ""
    peer_cluster_uuid: str = ""
    peer_svm_name: str = ""
    peer_svm_uuid: str = ""
    state: str = ""
    svm_name: str = ""
    svm_uuid: str = ""
    uuid: str = ""
