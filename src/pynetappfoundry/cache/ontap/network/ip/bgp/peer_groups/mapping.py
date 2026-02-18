"""OntapBgpPeerGroup type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.ontap.network.ip.bgp.peer_groups.model import OntapBgpPeerGroup

ONTAPBGPPEERGROUP_MAPPING = TypeMapping(
    name="OntapBgpPeerGroup",
    model_class=OntapBgpPeerGroup,
    api_endpoint="/network/ip/bgp/peer-groups?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="ipspace_name",
            api_path="ipspace.name",
        ),
        FieldMapping(
            cache_attr="ipspace_uuid",
            api_path="ipspace.uuid",
        ),
        FieldMapping(
            cache_attr="local_interface_ip_address",
            api_path="local.interface.ip.address",
        ),
        FieldMapping(
            cache_attr="local_interface_name",
            api_path="local.interface.name",
        ),
        FieldMapping(
            cache_attr="local_interface_uuid",
            api_path="local.interface.uuid",
        ),
        FieldMapping(
            cache_attr="local_ip_address",
            api_path="local.ip.address",
        ),
        FieldMapping(
            cache_attr="local_ip_netmask",
            api_path="local.ip.netmask",
        ),
        FieldMapping(
            cache_attr="local_port_name",
            api_path="local.port.name",
        ),
        FieldMapping(
            cache_attr="local_port_node_name",
            api_path="local.port.node.name",
        ),
        FieldMapping(
            cache_attr="local_port_uuid",
            api_path="local.port.uuid",
        ),
        FieldMapping(
            cache_attr="name",
            api_path="name",
        ),
        FieldMapping(
            cache_attr="peer_address",
            api_path="peer.address",
        ),
        FieldMapping(
            cache_attr="peer_asn",
            api_path="peer.asn",
            default=0,
        ),
        FieldMapping(
            cache_attr="peer_is_next_hop",
            api_path="peer.is_next_hop",
            default=False,
        ),
        FieldMapping(
            cache_attr="peer_md5_enabled",
            api_path="peer.md5_enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="peer_md5_secret",
            api_path="peer.md5_secret",
        ),
        FieldMapping(
            cache_attr="state",
            api_path="state",
        ),
        FieldMapping(
            cache_attr="uuid",
            api_path="uuid",
        ),
    ),
)

model_registry.register_mapping("OntapBgpPeerGroup", ONTAPBGPPEERGROUP_MAPPING)
