"""OntapSvmPeerPermission information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.cache._base import CacheModel


class OntapSvmPeerPermission(CacheModel):
    """OntapSvmPeerPermission information."""

    applications: list[str] = Field(default_factory=list)
    cluster_peer_name: str = ""
    cluster_peer_uuid: str = ""
    svm_name: str = ""
    svm_uuid: str = ""
