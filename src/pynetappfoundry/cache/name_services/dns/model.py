"""DNS configuration -- /name-services/dns."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.cache._base import CacheModel


class DNSInfo(CacheModel):
    """DNS configuration per SVM or cluster."""

    uuid: str = ""
    svm_uuid: str = ""
    scope: str = ""  # cluster, svm
    domains: list[str] = Field(default_factory=list)
    servers: list[str] = Field(default_factory=list)
    timeout: int = 0
    attempts: int = 0
    dynamic_dns_enabled: bool = False
    dynamic_dns_fqdn: str = ""
    dynamic_dns_time_to_live: str = ""
    dynamic_dns_use_secure: bool = False
    packet_query_match: bool = True
    source_address_match: bool = True
    tld_query_enabled: bool = True
    service_ips: list[str] = Field(default_factory=list)
