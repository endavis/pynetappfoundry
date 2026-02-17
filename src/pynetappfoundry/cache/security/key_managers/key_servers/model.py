"""OntapKeyServer information."""

from __future__ import annotations

from typing import Any

from pydantic import Field

from pynetappfoundry.cache._base import CacheModel


class OntapKeyServerNodeState(CacheModel):
    """OntapKeyServerNodeState sub-model for node_states."""

    connectivity_node_states_node_name: str = ""
    connectivity_node_states_node_uuid: str = ""
    connectivity_node_states_state: str = ""


class OntapKeyServerRecord(CacheModel):
    """OntapKeyServerRecord sub-model for records."""

    records_connectivity_cluster_availability: bool = False
    records_connectivity_node_states: list[dict[str, Any]] = Field(default_factory=list)
    records_password: str = ""
    records_server: str = ""
    records_timeout: int = 0
    records_username: str = ""


class OntapKeyServer(CacheModel):
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
