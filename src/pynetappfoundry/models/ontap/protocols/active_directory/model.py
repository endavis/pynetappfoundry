"""OntapActiveDirectory information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapActiveDirectoryDiscoveredServer(OntapModel):
    """OntapActiveDirectoryDiscoveredServer sub-model for discovered_servers."""

    domain: str = ""
    node_name: str = ""
    node_uuid: str = ""
    preference: str = ""
    server_ip: str = ""
    server_name: str = ""
    server_type: str = ""
    state: str = ""


class OntapActiveDirectoryPreferredDc(OntapModel):
    """OntapActiveDirectoryPreferredDc sub-model for preferred_dcs."""

    fqdn: str = ""
    server_ip: str = ""


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
