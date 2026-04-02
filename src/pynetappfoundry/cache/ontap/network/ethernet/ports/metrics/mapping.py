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
            api_path="duration",
        ),
        FieldMapping(
            cache_attr="status",
            api_path="status",
        ),
        FieldMapping(
            cache_attr="throughput.read",
            api_path="throughput.read",
            default=0,
        ),
        FieldMapping(
            cache_attr="throughput.total",
            api_path="throughput.total",
            default=0,
        ),
        FieldMapping(
            cache_attr="throughput.write",
            api_path="throughput.write",
            default=0,
        ),
        FieldMapping(
            cache_attr="timestamp",
            api_path="timestamp",
        ),
        FieldMapping(
            cache_attr="uuid",
            api_path="uuid",
        ),
    ),
)

model_registry.register_mapping("OntapPortMetricsResponse", ONTAPPORTMETRICSRESPONSE_MAPPING)
