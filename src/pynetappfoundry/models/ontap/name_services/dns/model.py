"""OntapDns information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapDnsStatus(OntapModel):
    """OntapDnsStatus sub-model for status."""

    code: int = 0
    message: str = ""
    name_server: str = ""
    state: str = ""


class OntapDns(OntapModel):
    """OntapDns information."""

    attempts: int = 0
    domains: list[str] = Field(default_factory=list)
    dynamic_dns_enabled: bool = False
    dynamic_dns_fqdn: str = ""
    dynamic_dns_skip_fqdn_validation: bool = False
    dynamic_dns_time_to_live: str = ""
    dynamic_dns_use_secure: bool = False
    packet_query_match: bool = False
    scope: str = ""
    servers: list[str] = Field(default_factory=list)
    service_ips: list[str] = Field(default_factory=list)
    skip_config_validation: bool = False
    source_address_match: bool = False
    status: list[OntapDnsStatus] = Field(default_factory=list)
    svm_name: str = ""
    svm_uuid: str = ""
    timeout: int = 0
    tld_query_enabled: bool = False
    uuid: str = ""
