"""OntapIpSubnet type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.network.ip.subnets.model import (
    OntapIpSubnet,
    OntapIpSubnetAvailableIpRange,
    OntapIpSubnetIpRange,
)

ONTAPIPSUBNET_MAPPING = TypeMapping(
    name="OntapIpSubnet",
    model_class=OntapIpSubnet,
    api_endpoint="/network/ip/subnets?fields=*",
    api_type="ontap",
    identifier_field="uuid",
    fields=(
        FieldMapping(
            cache_attr="available_count",
            default=0,
        ),
        FieldMapping(
            cache_attr="available_ip_ranges",
            item_model=OntapIpSubnetAvailableIpRange,
            default=[],
        ),
        FieldMapping(
            cache_attr="broadcast_domain.name",
        ),
        FieldMapping(
            cache_attr="broadcast_domain.uuid",
        ),
        FieldMapping(
            cache_attr="fail_if_lifs_conflict",
            default=False,
        ),
        FieldMapping(
            cache_attr="gateway",
        ),
        FieldMapping(
            cache_attr="ip_ranges",
            item_model=OntapIpSubnetIpRange,
            default=[],
        ),
        FieldMapping(
            cache_attr="ipspace.name",
        ),
        FieldMapping(
            cache_attr="ipspace.uuid",
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="subnet.address",
        ),
        FieldMapping(
            cache_attr="subnet.family",
        ),
        FieldMapping(
            cache_attr="subnet.netmask",
        ),
        FieldMapping(
            cache_attr="total_count",
            default=0,
        ),
        FieldMapping(
            cache_attr="used_count",
            default=0,
        ),
        FieldMapping(
            cache_attr="uuid",
        ),
    ),
)

model_registry.register_mapping("OntapIpSubnet", ONTAPIPSUBNET_MAPPING)
