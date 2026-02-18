"""OntapNfsClientsMap information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.cache._base import CacheModel


class OntapNfsClientsMap(CacheModel):
    """OntapNfsClientsMap information."""

    client_ips: list[str] = Field(default_factory=list)
    node_name: str = ""
    node_uuid: str = ""
    server_ip: str = ""
    svm_name: str = ""
    svm_uuid: str = ""
