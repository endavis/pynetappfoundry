"""OntapBgpPeerGroup type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.network.ip.bgp.peer_groups.model import OntapBgpPeerGroup

ONTAPBGPPEERGROUP_MAPPING = TypeMapping(
    name="OntapBgpPeerGroup",
    model_class=OntapBgpPeerGroup,
    api_endpoint="/network/ip/bgp/peer-groups?fields=*",
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
            cache_attr="local.interface.ip.address",
        ),
        FieldMapping(
            cache_attr="local.interface.name",
        ),
        FieldMapping(
            cache_attr="local.interface.uuid",
        ),
        FieldMapping(
            cache_attr="local.ip.address",
        ),
        FieldMapping(
            cache_attr="local.ip.netmask",
        ),
        FieldMapping(
            cache_attr="local.port.name",
        ),
        FieldMapping(
            cache_attr="local.port.node.name",
        ),
        FieldMapping(
            cache_attr="local.port.uuid",
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="peer.address",
        ),
        FieldMapping(
            cache_attr="peer.asn",
            default=0,
        ),
        FieldMapping(
            cache_attr="peer.is_next_hop",
            default=False,
        ),
        FieldMapping(
            cache_attr="peer.md5_enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="peer.md5_secret",
        ),
        FieldMapping(
            cache_attr="state",
        ),
        FieldMapping(
            cache_attr="uuid",
        ),
    ),
)

model_registry.register_mapping("OntapBgpPeerGroup", ONTAPBGPPEERGROUP_MAPPING)
