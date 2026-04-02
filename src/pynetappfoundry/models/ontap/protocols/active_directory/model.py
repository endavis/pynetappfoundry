"""OntapActiveDirectory information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapActiveDirectoryDiscoveredServerNode(OntapModel):
    """OntapActiveDirectoryDiscoveredServerNode sub-model for node."""

    name: str = ""
    uuid: str = ""


class OntapActiveDirectoryDiscoveredServerServer(OntapModel):
    """OntapActiveDirectoryDiscoveredServerServer sub-model for server."""

    ip: str = ""
    name: str = ""
    type_: str = ""


class OntapActiveDirectoryDiscoveredServer(OntapModel):
    """OntapActiveDirectoryDiscoveredServer sub-model for discovered_servers."""

    domain: str = ""
    node: OntapActiveDirectoryDiscoveredServerNode = Field(
        default_factory=OntapActiveDirectoryDiscoveredServerNode
    )
    preference: str = ""
    server: OntapActiveDirectoryDiscoveredServerServer = Field(
        default_factory=OntapActiveDirectoryDiscoveredServerServer
    )
    state: str = ""


class OntapActiveDirectoryPreferredDc(OntapModel):
    """OntapActiveDirectoryPreferredDc sub-model for preferred_dcs."""

    fqdn: str = ""
    server_ip: str = ""


class OntapActiveDirectorySvm(OntapModel):
    """OntapActiveDirectorySvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapActiveDirectory(OntapModel):
    """OntapActiveDirectory information."""

    discovered_servers: list[OntapActiveDirectoryDiscoveredServer] = Field(default_factory=list)
    force_account_overwrite: bool = False
    fqdn: str = ""
    name: str = ""
    organizational_unit: str = ""
    password: str = ""
    preferred_dcs: list[OntapActiveDirectoryPreferredDc] = Field(default_factory=list)
    svm: OntapActiveDirectorySvm = Field(default_factory=OntapActiveDirectorySvm)
    username: str = ""
