"""OntapNodeMetricsResponse type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.cluster.nodes.metrics.model import OntapNodeMetricsResponse

ONTAPNODEMETRICSRESPONSE_MAPPING = TypeMapping(
    name="OntapNodeMetricsResponse",
    model_class=OntapNodeMetricsResponse,
    api_endpoint="/cluster/nodes/{uuid}/metrics?fields=*",
    api_type="ontap",
    parent_mapping="OntapNodeResponse",
    parent_id_field="uuid",
    fields=(
        FieldMapping(
            cache_attr="duration",
        ),
        FieldMapping(
            cache_attr="processor_utilization",
            default=0,
        ),
        FieldMapping(
            cache_attr="status",
        ),
        FieldMapping(
            cache_attr="timestamp",
        ),
        FieldMapping(
            cache_attr="uuid",
        ),
    ),
)

model_registry.register_mapping("OntapNodeMetricsResponse", ONTAPNODEMETRICSRESPONSE_MAPPING)
