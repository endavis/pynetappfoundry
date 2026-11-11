"""OntapBroadcastDomain type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.network.ethernet.broadcast_domains.model import (
    OntapBroadcastDomain,
    OntapBroadcastDomainPort,
)

ONTAPBROADCASTDOMAIN_MAPPING = TypeMapping(
    name="OntapBroadcastDomain",
    model_class=OntapBroadcastDomain,
    api_endpoint="/network/ethernet/broadcast-domains?fields=*",
    api_type="ontap",
    identifier_field="uuid",
    fields=(
        FieldMapping(
            cache_attr="ipspace.name",
        ),
        FieldMapping(
            cache_attr="ipspace.uuid",
        ),
        FieldMapping(
            cache_attr="mtu",
            default=0,
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="ports",
            item_model=OntapBroadcastDomainPort,
            default=[],
        ),
        FieldMapping(
            cache_attr="uuid",
        ),
    ),
)

model_registry.register_mapping("OntapBroadcastDomain", ONTAPBROADCASTDOMAIN_MAPPING)
