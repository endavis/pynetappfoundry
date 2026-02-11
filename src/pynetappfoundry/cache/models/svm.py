"""SVM and peering models (/svm + /cluster/peers API path)."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class SVMInfo(BaseModel):
    """Storage Virtual Machine information."""

    model_config = ConfigDict(extra="allow")

    uuid: str = ""
    name: str = ""
    state: str = ""
    subtype: str = ""  # default, dp_destination, sync_source
    root_volume: str = ""
    root_volume_aggregate: str = ""
    allowed_protocols: list[str] = Field(default_factory=list)
    language: str = ""


class ClusterPeer(BaseModel):
    """Cluster peering information."""

    model_config = ConfigDict(extra="allow")

    name: str = ""
    uuid: str = ""
    remote_cluster_name: str = ""
    peer_addresses: list[str] = Field(default_factory=list)
    authentication_state: str = ""
    authentication_in_use: str = ""
    encryption_state: str = ""


class SVMPeerInfo(BaseModel):
    """SVM peering information."""

    model_config = ConfigDict(extra="allow")

    uuid: str = ""
    name: str = ""
    svm: str = ""
    peer_svm: str = ""
    peer_cluster: str = ""
    state: str = ""  # peered, initiated, pending, etc.
    applications: list[str] = Field(default_factory=list)
