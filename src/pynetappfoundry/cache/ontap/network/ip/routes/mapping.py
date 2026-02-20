"""OntapNetworkRoute type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.ontap.network.ip.routes.model import (
    OntapNetworkRoute,
    OntapNetworkRouteInterface,
)


def _transform_interfaces(record: dict[str, Any]) -> list[OntapNetworkRouteInterface]:
    """Transform interfaces into OntapNetworkRouteInterface list."""
    return [OntapNetworkRouteInterface(**item) for item in record.get("interfaces", [])]


ONTAPNETWORKROUTE_MAPPING = TypeMapping(
    name="OntapNetworkRoute",
    model_class=OntapNetworkRoute,
    api_endpoint="/network/ip/routes?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="destination_address",
            api_path="destination.address",
        ),
        FieldMapping(
            cache_attr="destination_family",
            api_path="destination.family",
        ),
        FieldMapping(
            cache_attr="destination_netmask",
            api_path="destination.netmask",
        ),
        FieldMapping(
            cache_attr="gateway",
            api_path="gateway",
        ),
        FieldMapping(
            cache_attr="interfaces",
            transform=_transform_interfaces,
            default=[],
            requires_explicit_fetch=True,
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
            cache_attr="metric",
            api_path="metric",
            default=0,
        ),
        FieldMapping(
            cache_attr="scope",
            api_path="scope",
        ),
        FieldMapping(
            cache_attr="svm_name",
            api_path="svm.name",
        ),
        FieldMapping(
            cache_attr="svm_uuid",
            api_path="svm.uuid",
        ),
        FieldMapping(
            cache_attr="uuid",
            api_path="uuid",
        ),
    ),
)

model_registry.register_mapping("OntapNetworkRoute", ONTAPNETWORKROUTE_MAPPING)
