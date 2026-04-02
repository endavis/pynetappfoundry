"""OntapKeyServer information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapKeyServerConnectivityNodeStateNode(OntapModel):
    """OntapKeyServerConnectivityNodeStateNode sub-model for node."""

    name: str = ""
    uuid: str = ""


class OntapKeyServerConnectivityNodeState(OntapModel):
    """OntapKeyServerConnectivityNodeState sub-model for node_states."""

    node: OntapKeyServerConnectivityNodeStateNode = Field(
        default_factory=OntapKeyServerConnectivityNodeStateNode
    )
    state: str = ""


class OntapKeyServerConnectivity(OntapModel):
    """OntapKeyServerConnectivity sub-model for connectivity."""

    cluster_availability: bool = False
    node_states: list[OntapKeyServerConnectivityNodeState] = Field(default_factory=list)


class OntapKeyServerRecordConnectivityNodeStateNode(OntapModel):
    """OntapKeyServerRecordConnectivityNodeStateNode sub-model for node."""

    name: str = ""
    uuid: str = ""


class OntapKeyServerRecordConnectivityNodeState(OntapModel):
    """OntapKeyServerRecordConnectivityNodeState sub-model for node_states."""

    node: OntapKeyServerRecordConnectivityNodeStateNode = Field(
        default_factory=OntapKeyServerRecordConnectivityNodeStateNode
    )
    state: str = ""


class OntapKeyServerRecordConnectivity(OntapModel):
    """OntapKeyServerRecordConnectivity sub-model for connectivity."""

    cluster_availability: bool = False
    node_states: list[OntapKeyServerRecordConnectivityNodeState] = Field(default_factory=list)


class OntapKeyServerRecord(OntapModel):
    """OntapKeyServerRecord sub-model for records."""

    connectivity: OntapKeyServerRecordConnectivity = Field(
        default_factory=OntapKeyServerRecordConnectivity
    )
    password: str = ""
    server: str = ""
    timeout: int = 0
    username: str = ""


class OntapKeyServer(OntapModel):
    """OntapKeyServer information."""

    connectivity: OntapKeyServerConnectivity = Field(default_factory=OntapKeyServerConnectivity)
    create_remove_timeout: int = 0
    password: str = ""
    records: list[OntapKeyServerRecord] = Field(default_factory=list)
    secondary_key_servers: list[str] = Field(default_factory=list)
    server: str = ""
    timeout: int = 0
    username: str = ""
