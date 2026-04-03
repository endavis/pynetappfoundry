"""OntapDns type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.name_services.dns.model import OntapDns, OntapDnsStatus


def _transform_status(record: dict[str, Any]) -> list[OntapDnsStatus]:
    """Transform status into OntapDnsStatus list."""
    return [OntapDnsStatus(**item) for item in record.get("status", [])]


ONTAPDNS_MAPPING = TypeMapping(
    name="OntapDns",
    model_class=OntapDns,
    api_endpoint="/name-services/dns?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="attempts",
            default=0,
        ),
        FieldMapping(
            cache_attr="domains",
            default=[],
        ),
        FieldMapping(
            cache_attr="dynamic_dns.enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="dynamic_dns.fqdn",
        ),
        FieldMapping(
            cache_attr="dynamic_dns.skip_fqdn_validation",
            default=False,
        ),
        FieldMapping(
            cache_attr="dynamic_dns.time_to_live",
        ),
        FieldMapping(
            cache_attr="dynamic_dns.use_secure",
            default=False,
        ),
        FieldMapping(
            cache_attr="packet_query_match",
            default=False,
        ),
        FieldMapping(
            cache_attr="scope",
        ),
        FieldMapping(
            cache_attr="servers",
            default=[],
        ),
        FieldMapping(
            cache_attr="service_ips",
            default=[],
        ),
        FieldMapping(
            cache_attr="skip_config_validation",
            default=False,
        ),
        FieldMapping(
            cache_attr="source_address_match",
            default=False,
        ),
        FieldMapping(
            cache_attr="status",
            transform=_transform_status,
            default=[],
        ),
        FieldMapping(
            cache_attr="svm.name",
        ),
        FieldMapping(
            cache_attr="svm.uuid",
        ),
        FieldMapping(
            cache_attr="timeout",
            default=0,
        ),
        FieldMapping(
            cache_attr="tld_query_enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="uuid",
        ),
    ),
)

model_registry.register_mapping("OntapDns", ONTAPDNS_MAPPING)
