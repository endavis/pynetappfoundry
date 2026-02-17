"""OntapMetroclusterOperation type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.cluster.metrocluster.operations.model import OntapMetroclusterOperation
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping

ONTAPMETROCLUSTEROPERATION_MAPPING = TypeMapping(
    name="OntapMetroclusterOperation",
    model_class=OntapMetroclusterOperation,
    api_endpoint="/cluster/metrocluster/operations?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="additional_info",
            api_path="additional_info",
        ),
        FieldMapping(
            cache_attr="command_line",
            api_path="command_line",
        ),
        FieldMapping(
            cache_attr="end_time",
            api_path="end_time",
        ),
        FieldMapping(
            cache_attr="errors",
            api_path="errors",
            default=[],
        ),
        FieldMapping(
            cache_attr="node_name",
            api_path="node.name",
        ),
        FieldMapping(
            cache_attr="node_uuid",
            api_path="node.uuid",
        ),
        FieldMapping(
            cache_attr="start_time",
            api_path="start_time",
        ),
        FieldMapping(
            cache_attr="state",
            api_path="state",
        ),
        FieldMapping(
            cache_attr="type_",
            api_path="type",
        ),
        FieldMapping(
            cache_attr="uuid",
            api_path="uuid",
        ),
    ),
)

model_registry.register_mapping("OntapMetroclusterOperation", ONTAPMETROCLUSTEROPERATION_MAPPING)
