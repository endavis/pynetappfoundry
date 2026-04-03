"""OntapPortMetricsResponse type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.network.ethernet.ports.metrics.model import (
    OntapPortMetricsResponse,
)

ONTAPPORTMETRICSRESPONSE_MAPPING = TypeMapping(
    name="OntapPortMetricsResponse",
    model_class=OntapPortMetricsResponse,
    api_endpoint="/network/ethernet/ports/{uuid}/metrics?fields=*",
    api_type="ontap",
    parent_mapping="OntapPort",
    parent_id_field="uuid",
    fields=(
        FieldMapping(
            cache_attr="duration",
        ),
        FieldMapping(
            cache_attr="status",
        ),
        FieldMapping(
            cache_attr="throughput.read",
            default=0,
        ),
        FieldMapping(
            cache_attr="throughput.total",
            default=0,
        ),
        FieldMapping(
            cache_attr="throughput.write",
            default=0,
        ),
        FieldMapping(
            cache_attr="timestamp",
        ),
        FieldMapping(
            cache_attr="uuid",
        ),
    ),
)

model_registry.register_mapping("OntapPortMetricsResponse", ONTAPPORTMETRICSRESPONSE_MAPPING)
