"""Cluster peering information — /cluster/peers."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.cache._base import CacheModel


class ClusterPeer(CacheModel):
    """Cluster peering information."""

    name: str = ""
    uuid: str = ""
    remote_cluster_name: str = ""
    peer_addresses: list[str] = Field(default_factory=list)
    authentication_state: str = ""
    authentication_in_use: str = ""
    encryption_state: str = ""
