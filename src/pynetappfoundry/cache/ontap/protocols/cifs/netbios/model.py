"""OntapNetbios information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.cache._base import CacheModel


class OntapNetbiosWinsServer(CacheModel):
    """OntapNetbiosWinsServer sub-model for wins_servers."""

    wins_servers_ip: str = ""
    wins_servers_state: str = ""


class OntapNetbios(CacheModel):
    """OntapNetbios information."""

    interfaces: list[str] = Field(default_factory=list)
    mode: str = ""
    name: str = ""
    name_registration_type: str = ""
    node_name: str = ""
    node_uuid: str = ""
    scope: str = ""
    state: str = ""
    suffix: str = ""
    svm_name: str = ""
    svm_uuid: str = ""
    time_left: int = 0
    wins_servers: list[OntapNetbiosWinsServer] = Field(default_factory=list)
