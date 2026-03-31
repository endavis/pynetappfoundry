"""OntapKeyServer information."""

from __future__ import annotations

from typing import Any

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapKeyServerNodeState(OntapModel):
    """OntapKeyServerNodeState sub-model for node_states."""

    node_name: str = ""
    node_uuid: str = ""
    state: str = ""


class OntapKeyServerRecord(OntapModel):
    """OntapKeyServerRecord sub-model for records."""

    connectivity_cluster_availability: bool = False
    connectivity_node_states: list[dict[str, Any]] = Field(default_factory=list)
    password: str = ""
    server: str = ""
    timeout: int = 0
    username: str = ""


class OntapKeyServer(OntapModel):
    """OntapKeyServer information."""

    connectivity_cluster_availability: bool = False
    connectivity_node_states: list[OntapKeyServerNodeState] = Field(default_factory=list)
    create_remove_timeout: int = 0
    password: str = ""
    records: list[OntapKeyServerRecord] = Field(default_factory=list)
    secondary_key_servers: list[str] = Field(default_factory=list)
    server: str = ""
    timeout: int = 0
    username: str = ""
