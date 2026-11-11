"""OntapNetworkRoute type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.network.ip.routes.model import (
    OntapNetworkRoute,
    OntapNetworkRouteInterface,
)

ONTAPNETWORKROUTE_MAPPING = TypeMapping(
    name="OntapNetworkRoute",
    model_class=OntapNetworkRoute,
    api_endpoint="/network/ip/routes?fields=*",
    api_type="ontap",
    identifier_field="uuid",
    fields=(
        FieldMapping(
            cache_attr="destination.address",
        ),
        FieldMapping(
            cache_attr="destination.family",
        ),
        FieldMapping(
            cache_attr="destination.netmask",
        ),
        FieldMapping(
            cache_attr="gateway",
        ),
        FieldMapping(
            cache_attr="interfaces",
            item_model=OntapNetworkRouteInterface,
            default=[],
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="ipspace.name",
        ),
        FieldMapping(
            cache_attr="ipspace.uuid",
        ),
        FieldMapping(
            cache_attr="metric",
            default=0,
        ),
        FieldMapping(
            cache_attr="scope",
        ),
        FieldMapping(
            cache_attr="svm.name",
        ),
        FieldMapping(
            cache_attr="svm.uuid",
        ),
        FieldMapping(
            cache_attr="uuid",
        ),
    ),
)

model_registry.register_mapping("OntapNetworkRoute", ONTAPNETWORKROUTE_MAPPING)
