"""OntapCifsDomain information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapCifsDomainAdDomain(OntapModel):
    """OntapCifsDomainAdDomain sub-model for ad_domain."""

    password: str = ""
    user: str = ""


class OntapCifsDomainDiscoveredServerNode(OntapModel):
    """OntapCifsDomainDiscoveredServerNode sub-model for node."""

    name: str = ""
    uuid: str = ""


class OntapCifsDomainDiscoveredServer(OntapModel):
    """OntapCifsDomainDiscoveredServer sub-model for discovered_servers."""

    domain: str = ""
    node: OntapCifsDomainDiscoveredServerNode = Field(
        default_factory=OntapCifsDomainDiscoveredServerNode
    )
    preference: str = ""
    server_ip: str = ""
    server_name: str = ""
    server_type: str = ""
    state: str = ""


class OntapCifsDomainNameMapping(OntapModel):
    """OntapCifsDomainNameMapping sub-model for name_mapping."""

    trusted_domains: list[str] = Field(default_factory=list)


class OntapCifsDomainPasswordSchedule(OntapModel):
    """OntapCifsDomainPasswordSchedule sub-model for password_schedule."""

    schedule_day_of_week: str = ""
    schedule_description: str = ""
    schedule_enabled: bool = False
    schedule_last_changed_time: str = ""
    schedule_randomized_minute: int = 0
    schedule_time_of_day: str = ""
    schedule_warn_message: str = ""
    schedule_weekly_interval: int = 0


class OntapCifsDomainPreferredDc(OntapModel):
    """OntapCifsDomainPreferredDc sub-model for preferred_dcs."""

    fqdn: str = ""
    server_ip: str = ""


class OntapCifsDomainSvm(OntapModel):
    """OntapCifsDomainSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapCifsDomainTrustRelationshipNode(OntapModel):
    """OntapCifsDomainTrustRelationshipNode sub-model for node."""

    name: str = ""
    uuid: str = ""


class OntapCifsDomainTrustRelationship(OntapModel):
    """OntapCifsDomainTrustRelationship sub-model for trust_relationships."""

    home_domain: str = ""
    node: OntapCifsDomainTrustRelationshipNode = Field(
        default_factory=OntapCifsDomainTrustRelationshipNode
    )
    trusted_domains: list[str] = Field(default_factory=list)


class OntapCifsDomain(OntapModel):
    """OntapCifsDomain information."""

    ad_domain: OntapCifsDomainAdDomain = Field(default_factory=OntapCifsDomainAdDomain)
    client_certificate: str = ""
    client_id: str = ""
    discovered_servers: list[OntapCifsDomainDiscoveredServer] = Field(default_factory=list)
    name_mapping: OntapCifsDomainNameMapping = Field(default_factory=OntapCifsDomainNameMapping)
    password_schedule: OntapCifsDomainPasswordSchedule = Field(
        default_factory=OntapCifsDomainPasswordSchedule
    )
    preferred_dcs: list[OntapCifsDomainPreferredDc] = Field(default_factory=list)
    server_discovery_mode: str = ""
    svm: OntapCifsDomainSvm = Field(default_factory=OntapCifsDomainSvm)
    tenant_id: str = ""
    trust_relationships: list[OntapCifsDomainTrustRelationship] = Field(default_factory=list)
