"""BroadcastDomain type mapping definition for the declarative field mapping framework.

Defines BROADCAST_DOMAIN_MAPPING which maps ONTAP REST API broadcast domain
data to BroadcastDomain cache model attributes. BroadcastDomain is API-only --
there is no CLI command for this data.

All fields use simple dot-path extraction; no transform functions are needed.
"""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.network.ethernet.broadcast_domains.model import BroadcastDomain

BROADCAST_DOMAIN_MAPPING = TypeMapping(
    name="BroadcastDomain",
    model_class=BroadcastDomain,
    api_endpoint="/network/ethernet/broadcast-domains?fields=*",
    cli_command="",
    fields=(
        FieldMapping(
            cache_attr="uuid",
            api_path="uuid",
        ),
        FieldMapping(
            cache_attr="name",
            api_path="name",
        ),
        FieldMapping(
            cache_attr="mtu",
            api_path="mtu",
            default=0,
        ),
        FieldMapping(
            cache_attr="ipspace_uuid",
            api_path="ipspace.uuid",
        ),
        FieldMapping(
            cache_attr="port_uuids",
            api_path="ports[*].uuid",
            default=[],
        ),
    ),
)

model_registry.register_mapping("BroadcastDomain", BROADCAST_DOMAIN_MAPPING)
