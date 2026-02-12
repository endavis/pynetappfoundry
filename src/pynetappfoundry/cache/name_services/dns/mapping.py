"""DNS type mapping definition for the declarative field mapping framework.

Defines DNS_MAPPING which maps ONTAP REST API DNS configuration data
to DNSInfo cache model attributes. DNS is API-only -- there is no CLI
command for this data.

All fields use simple dot-path extraction; no transform functions are
needed.

Note: ``tld_query_enabled``, ``source_address_match``, and
``packet_query_match`` must be explicitly requested (not included in
``fields=*``). ``service_ips`` is only available on ONTAP 9.14+.
"""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.name_services.dns.model import DNSInfo

DNS_MAPPING = TypeMapping(
    name="DNS",
    model_class=DNSInfo,
    api_endpoint="/name-services/dns?fields=*,tld_query_enabled,source_address_match,packet_query_match",
    cli_command="",
    fields=(
        FieldMapping(
            cache_attr="uuid",
            api_path="uuid",
        ),
        FieldMapping(
            cache_attr="svm_uuid",
            api_path="svm.uuid",
        ),
        FieldMapping(
            cache_attr="scope",
            api_path="scope",
        ),
        FieldMapping(
            cache_attr="domains",
            api_path="domains",
            default=[],
        ),
        FieldMapping(
            cache_attr="servers",
            api_path="servers",
            default=[],
        ),
        FieldMapping(
            cache_attr="timeout",
            api_path="timeout",
            default=0,
        ),
        FieldMapping(
            cache_attr="attempts",
            api_path="attempts",
            default=0,
        ),
        FieldMapping(
            cache_attr="dynamic_dns_enabled",
            api_path="dynamic_dns.enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="dynamic_dns_fqdn",
            api_path="dynamic_dns.fqdn",
        ),
        FieldMapping(
            cache_attr="dynamic_dns_time_to_live",
            api_path="dynamic_dns.time_to_live",
        ),
        FieldMapping(
            cache_attr="dynamic_dns_use_secure",
            api_path="dynamic_dns.use_secure",
            default=False,
        ),
        FieldMapping(
            cache_attr="packet_query_match",
            api_path="packet_query_match",
            default=True,
        ),
        FieldMapping(
            cache_attr="source_address_match",
            api_path="source_address_match",
            default=True,
        ),
        FieldMapping(
            cache_attr="tld_query_enabled",
            api_path="tld_query_enabled",
            default=True,
        ),
        FieldMapping(
            cache_attr="service_ips",
            api_path="service_ips",
            default=[],
        ),
    ),
)

model_registry.register_mapping("DNS", DNS_MAPPING)
