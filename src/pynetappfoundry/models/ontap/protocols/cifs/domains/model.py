"""OntapCifsDomain information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapCifsDomainDiscoveredServer(OntapModel):
    """OntapCifsDomainDiscoveredServer sub-model for discovered_servers."""

    domain: str = ""
    node_name: str = ""
    node_uuid: str = ""
    preference: str = ""
    server_ip: str = ""
    server_name: str = ""
    server_type: str = ""
    state: str = ""


class OntapCifsDomainPreferredDc(OntapModel):
    """OntapCifsDomainPreferredDc sub-model for preferred_dcs."""

    fqdn: str = ""
    server_ip: str = ""


class OntapCifsDomainTrustRelationship(OntapModel):
    """OntapCifsDomainTrustRelationship sub-model for trust_relationships."""

    home_domain: str = ""
    node_name: str = ""
    node_uuid: str = ""
    trusted_domains: list[str] = Field(default_factory=list)


class OntapCifsDomain(OntapModel):
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
