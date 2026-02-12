"""Re-export DNS cache models and mappings."""

from __future__ import annotations

from pynetappfoundry.cache.name_services.dns.mapping import DNS_MAPPING
from pynetappfoundry.cache.name_services.dns.model import DNSInfo

__all__ = [
    "DNS_MAPPING",
    "DNSInfo",
]
