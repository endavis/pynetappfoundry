"""AiqumAggregateCapability type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.aiqum.storage_provider.aggregate_capabilities.model import (
    AiqumAggregateCapability,
)

AIQUMAGGREGATECAPABILITY_MAPPING = TypeMapping(
    name="AiqumAggregateCapability",
    model_class=AiqumAggregateCapability,
    api_endpoint="/storage-provider/aggregate-capabilities",
    api_type="aiqum",
    identifier_field="key",
    fields=(
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
            cache_attr="key",
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="performance_service_levels",
            default=[],
        ),
        FieldMapping(
            cache_attr="uuid",
        ),
    ),
)

model_registry.register_mapping("AiqumAggregateCapability", AIQUMAGGREGATECAPABILITY_MAPPING)
