"""AiqumSystemResponse type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.aiqum.management_server.system.model import (
    AiqumSystemResponse,
    AiqumSystemResponseService,
)

AIQUMSYSTEMRESPONSE_MAPPING = TypeMapping(
    name="AiqumSystemResponse",
    model_class=AiqumSystemResponse,
    api_endpoint="/management-server/system",
    api_type="aiqum",
    response_shape="singleton",
    fields=(
        FieldMapping(
            cache_attr="deployment",
        ),
        FieldMapping(
            cache_attr="product",
        ),
        FieldMapping(
            cache_attr="services",
            item_model=AiqumSystemResponseService,
            default=[],
        ),
        FieldMapping(
            cache_attr="uuid",
        ),
        FieldMapping(
            cache_attr="vendor",
        ),
        FieldMapping(
            cache_attr="version",
        ),
    ),
)

model_registry.register_mapping("AiqumSystemResponse", AIQUMSYSTEMRESPONSE_MAPPING)
