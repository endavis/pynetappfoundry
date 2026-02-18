"""OntapCifsDomain information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.cache._base import CacheModel


class OntapCifsDomainDiscoveredServer(CacheModel):
    """OntapCifsDomainDiscoveredServer sub-model for discovered_servers."""

    discovered_servers_domain: str = ""
    discovered_servers_node_name: str = ""
    discovered_servers_node_uuid: str = ""
    discovered_servers_preference: str = ""
    discovered_servers_server_ip: str = ""
    discovered_servers_server_name: str = ""
    discovered_servers_server_type: str = ""
    discovered_servers_state: str = ""


class OntapCifsDomainPreferredDc(CacheModel):
    """OntapCifsDomainPreferredDc sub-model for preferred_dcs."""

    preferred_dcs_fqdn: str = ""
    preferred_dcs_server_ip: str = ""


class OntapCifsDomainTrustRelationship(CacheModel):
    """OntapCifsDomainTrustRelationship sub-model for trust_relationships."""

    trust_relationships_home_domain: str = ""
    trust_relationships_node_name: str = ""
    trust_relationships_node_uuid: str = ""
    trust_relationships_trusted_domains: list[str] = Field(default_factory=list)


class OntapCifsDomain(CacheModel):
    """OntapCifsDomain information."""

    ad_domain_password: str = ""
    ad_domain_user: str = ""
    client_certificate: str = ""
    client_id: str = ""
    discovered_servers: list[OntapCifsDomainDiscoveredServer] = Field(default_factory=list)
    name_mapping_trusted_domains: list[str] = Field(default_factory=list)
    password_schedule_schedule_day_of_week: str = ""
    password_schedule_schedule_description: str = ""
    password_schedule_schedule_enabled: bool = False
    password_schedule_schedule_last_changed_time: str = ""
    password_schedule_schedule_randomized_minute: int = 0
    password_schedule_schedule_time_of_day: str = ""
    password_schedule_schedule_warn_message: str = ""
    password_schedule_schedule_weekly_interval: int = 0
    preferred_dcs: list[OntapCifsDomainPreferredDc] = Field(default_factory=list)
    server_discovery_mode: str = ""
    svm_name: str = ""
    svm_uuid: str = ""
    tenant_id: str = ""
    trust_relationships: list[OntapCifsDomainTrustRelationship] = Field(default_factory=list)
