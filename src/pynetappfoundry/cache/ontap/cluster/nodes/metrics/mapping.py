"""OntapNodeMetricsResponse type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.ontap.cluster.nodes.metrics.model import OntapNodeMetricsResponse

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
            api_path="duration",
        ),
        FieldMapping(
            cache_attr="processor_utilization",
            api_path="processor_utilization",
            default=0,
        ),
        FieldMapping(
            cache_attr="status",
            api_path="status",
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

model_registry.register_mapping("OntapNodeMetricsResponse", ONTAPNODEMETRICSRESPONSE_MAPPING)
