"""DiiRisk type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.dii.assets.risks.model import DiiRisk

DIIRISK_MAPPING = TypeMapping(
    name="DiiRisk",
    model_class=DiiRisk,
    api_endpoint="/assets/risks/{id}",
    api_type="dii",
    fields=(
        FieldMapping(
            cache_attr="severity",
        ),
        FieldMapping(
            cache_attr="sourceId",
            default=0,
        ),
        FieldMapping(
            cache_attr="parent",
        ),
        FieldMapping(
            cache_attr="resource",
        ),
        FieldMapping(
            cache_attr="impact",
        ),
        FieldMapping(
            cache_attr="link",
        ),
        FieldMapping(
            cache_attr="simpleName",
        ),
        FieldMapping(
            cache_attr="sourceType",
        ),
        FieldMapping(
            cache_attr="mitigationCategory",
        ),
        FieldMapping(
            cache_attr="riskSource",
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="details",
        ),
        FieldMapping(
            cache_attr="id",
            default=0,
        ),
        FieldMapping(
            cache_attr="category",
        ),
        FieldMapping(
            cache_attr="statusCode",
        ),
    ),
)

model_registry.register_mapping("DiiRisk", DIIRISK_MAPPING)
