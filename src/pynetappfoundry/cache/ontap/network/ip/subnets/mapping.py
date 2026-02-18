"""OntapIpSubnet type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.ontap.network.ip.subnets.model import (
    OntapIpSubnet,
    OntapIpSubnetAvailableIpRange,
    OntapIpSubnetIpRange,
)


def _transform_available_ip_ranges(record: dict[str, Any]) -> list[OntapIpSubnetAvailableIpRange]:
    """Transform available_ip_ranges into OntapIpSubnetAvailableIpRange list."""
    return [OntapIpSubnetAvailableIpRange(**item) for item in record.get("available_ip_ranges", [])]


def _transform_ip_ranges(record: dict[str, Any]) -> list[OntapIpSubnetIpRange]:
    """Transform ip_ranges into OntapIpSubnetIpRange list."""
    return [OntapIpSubnetIpRange(**item) for item in record.get("ip_ranges", [])]


ONTAPIPSUBNET_MAPPING = TypeMapping(
    name="OntapIpSubnet",
    model_class=OntapIpSubnet,
    api_endpoint="/network/ip/subnets?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="available_count",
            api_path="available_count",
            default=0,
        ),
        FieldMapping(
            cache_attr="available_ip_ranges",
            transform=_transform_available_ip_ranges,
            default=[],
        ),
        FieldMapping(
            cache_attr="broadcast_domain_name",
            api_path="broadcast_domain.name",
        ),
        FieldMapping(
            cache_attr="broadcast_domain_uuid",
            api_path="broadcast_domain.uuid",
        ),
        FieldMapping(
            cache_attr="fail_if_lifs_conflict",
            api_path="fail_if_lifs_conflict",
            default=False,
        ),
        FieldMapping(
            cache_attr="gateway",
            api_path="gateway",
        ),
        FieldMapping(
            cache_attr="ip_ranges",
            transform=_transform_ip_ranges,
            default=[],
        ),
        FieldMapping(
            cache_attr="ipspace_name",
            api_path="ipspace.name",
        ),
        FieldMapping(
            cache_attr="ipspace_uuid",
            api_path="ipspace.uuid",
        ),
        FieldMapping(
            cache_attr="name",
            api_path="name",
        ),
        FieldMapping(
            cache_attr="subnet_address",
            api_path="subnet.address",
        ),
        FieldMapping(
            cache_attr="subnet_family",
            api_path="subnet.family",
        ),
        FieldMapping(
            cache_attr="subnet_netmask",
            api_path="subnet.netmask",
        ),
        FieldMapping(
            cache_attr="total_count",
            api_path="total_count",
            default=0,
        ),
        FieldMapping(
            cache_attr="used_count",
            api_path="used_count",
            default=0,
        ),
        FieldMapping(
            cache_attr="uuid",
            api_path="uuid",
        ),
    ),
)

model_registry.register_mapping("OntapIpSubnet", ONTAPIPSUBNET_MAPPING)
