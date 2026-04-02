"""OntapBroadcastDomain type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.network.ethernet.broadcast_domains.model import (
    OntapBroadcastDomain,
    OntapBroadcastDomainPort,
)


def _transform_ports(record: dict[str, Any]) -> list[OntapBroadcastDomainPort]:
    """Transform ports into OntapBroadcastDomainPort list."""
    return [OntapBroadcastDomainPort(**item) for item in record.get("ports", [])]


ONTAPBROADCASTDOMAIN_MAPPING = TypeMapping(
    name="OntapBroadcastDomain",
    model_class=OntapBroadcastDomain,
    api_endpoint="/network/ethernet/broadcast-domains?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="ipspace.name",
            api_path="ipspace.name",
        ),
        FieldMapping(
            cache_attr="ipspace.uuid",
            api_path="ipspace.uuid",
        ),
        FieldMapping(
            cache_attr="mtu",
            api_path="mtu",
            default=0,
        ),
        FieldMapping(
            cache_attr="name",
            api_path="name",
        ),
        FieldMapping(
            cache_attr="ports",
            api_path="ports",
            transform=_transform_ports,
            default=[],
        ),
        FieldMapping(
            cache_attr="uuid",
            api_path="uuid",
        ),
    ),
)

model_registry.register_mapping("OntapBroadcastDomain", ONTAPBROADCASTDOMAIN_MAPPING)
