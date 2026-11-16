"""AiqumEthernetPort type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.aiqum.datacenter.network.ethernet.ports.model import AiqumEthernetPort

AIQUMETHERNETPORT_MAPPING = TypeMapping(
    name="AiqumEthernetPort",
    model_class=AiqumEthernetPort,
    api_endpoint="/datacenter/network/ethernet/ports",
    api_type="aiqum",
    identifier_field="key",
    fields=(
        FieldMapping(
            cache_attr="broadcast_domain.ipspace.name",
        ),
        FieldMapping(
            cache_attr="broadcast_domain.key",
        ),
        FieldMapping(
            cache_attr="broadcast_domain.name",
        ),
        FieldMapping(
            cache_attr="broadcast_domain.uuid",
        ),
        FieldMapping(
            cache_attr="cluster.key",
        ),
        FieldMapping(
            cache_attr="cluster.name",
        ),
        FieldMapping(
            cache_attr="cluster.uuid",
        ),
        FieldMapping(
            cache_attr="enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="key",
        ),
        FieldMapping(
            cache_attr="mac_address",
        ),
        FieldMapping(
            cache_attr="mtu",
            default=0,
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="node.key",
        ),
        FieldMapping(
            cache_attr="node.name",
        ),
        FieldMapping(
            cache_attr="node.uuid",
        ),
        FieldMapping(
            cache_attr="speed",
        ),
        FieldMapping(
            cache_attr="state",
        ),
        FieldMapping(
            cache_attr="type_",
            api_path="type",
        ),
        FieldMapping(
            cache_attr="uuid",
        ),
        FieldMapping(
            cache_attr="vlan.base_port.name",
        ),
        FieldMapping(
            cache_attr="vlan.base_port.node.name",
        ),
        FieldMapping(
            cache_attr="vlan.base_port.uuid",
        ),
        FieldMapping(
            cache_attr="vlan.tag",
            default=0,
        ),
    ),
)

model_registry.register_mapping("AiqumEthernetPort", AIQUMETHERNETPORT_MAPPING)
