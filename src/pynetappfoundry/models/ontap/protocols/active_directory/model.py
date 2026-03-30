"""OntapActiveDirectory information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapActiveDirectoryDiscoveredServer(OntapModel):
    """OntapActiveDirectoryDiscoveredServer sub-model for discovered_servers."""

    discovered_servers_domain: str = ""
    discovered_servers_node_name: str = ""
    discovered_servers_node_uuid: str = ""
    discovered_servers_preference: str = ""
    discovered_servers_server_ip: str = ""
    discovered_servers_server_name: str = ""
    discovered_servers_server_type: str = ""
    discovered_servers_state: str = ""


class OntapActiveDirectoryPreferredDc(OntapModel):
    """OntapActiveDirectoryPreferredDc sub-model for preferred_dcs."""

    preferred_dcs_fqdn: str = ""
    preferred_dcs_server_ip: str = ""


class OntapActiveDirectory(OntapModel):
    """OntapActiveDirectory information."""

    discovered_servers: list[OntapActiveDirectoryDiscoveredServer] = Field(default_factory=list)
    force_account_overwrite: bool = False
    fqdn: str = ""
    name: str = ""
    organizational_unit: str = ""
    password: str = ""
    preferred_dcs: list[OntapActiveDirectoryPreferredDc] = Field(default_factory=list)
    svm_name: str = ""
    svm_uuid: str = ""
    username: str = ""
