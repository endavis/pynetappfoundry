"""OntapDns information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapDnsDynamicDns(OntapModel):
    """OntapDnsDynamicDns sub-model for dynamic_dns."""

    enabled: bool = False
    fqdn: str = ""
    skip_fqdn_validation: bool = False
    time_to_live: str = ""
    use_secure: bool = False


class OntapDnsStatus(OntapModel):
    """OntapDnsStatus sub-model for status."""

    code: int = 0
    message: str = ""
    name_server: str = ""
    state: str = ""


class OntapDnsSvm(OntapModel):
    """OntapDnsSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapDns(OntapModel):
    """OntapDns information."""

    attempts: int = 0
    domains: list[str] = Field(default_factory=list)
    dynamic_dns: OntapDnsDynamicDns = Field(default_factory=OntapDnsDynamicDns)
    packet_query_match: bool = False
    scope: str = ""
    servers: list[str] = Field(default_factory=list)
    service_ips: list[str] = Field(default_factory=list)
    skip_config_validation: bool = False
    source_address_match: bool = False
    status: list[OntapDnsStatus] = Field(default_factory=list)
    svm: OntapDnsSvm = Field(default_factory=OntapDnsSvm)
    timeout: int = 0
    tld_query_enabled: bool = False
    uuid: str = ""
