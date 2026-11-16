"""AiqumGatewaysService type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.aiqum.gateways.model import AiqumGatewaysService

AIQUMGATEWAYSSERVICE_MAPPING = TypeMapping(
    name="AiqumGatewaysService",
    model_class=AiqumGatewaysService,
    api_endpoint="/gateways",
    api_type="aiqum",
    fields=(
        FieldMapping(
            cache_attr="ip_address",
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="type_",
            api_path="type",
        ),
        FieldMapping(
            cache_attr="uuid",
        ),
    ),
)

model_registry.register_mapping("AiqumGatewaysService", AIQUMGATEWAYSSERVICE_MAPPING)
