"""SVM peering information — /svm/peers."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.cache._base import CacheModel


class SVMPeerInfo(CacheModel):
    """SVM peering information."""

    uuid: str = ""
    name: str = ""
    svm: str = ""
    peer_svm: str = ""
    peer_cluster: str = ""
    state: str = ""  # peered, initiated, pending, etc.
    applications: list[str] = Field(default_factory=list)
