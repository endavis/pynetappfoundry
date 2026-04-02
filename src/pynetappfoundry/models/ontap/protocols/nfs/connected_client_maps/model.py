"""OntapNfsClientsMap information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapNfsClientsMapNode(OntapModel):
    """OntapNfsClientsMapNode sub-model for node."""

    name: str = ""
    uuid: str = ""


class OntapNfsClientsMapSvm(OntapModel):
    """OntapNfsClientsMapSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapNfsClientsMap(OntapModel):
    """OntapNfsClientsMap information."""

    client_ips: list[str] = Field(default_factory=list)
    node: OntapNfsClientsMapNode = Field(default_factory=OntapNfsClientsMapNode)
    server_ip: str = ""
    svm: OntapNfsClientsMapSvm = Field(default_factory=OntapNfsClientsMapSvm)
