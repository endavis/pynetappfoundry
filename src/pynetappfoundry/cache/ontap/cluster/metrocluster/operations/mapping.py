"""OntapMetroclusterOperation type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.cluster.metrocluster.operations.model import (
    OntapMetroclusterOperation,
)

ONTAPMETROCLUSTEROPERATION_MAPPING = TypeMapping(
    name="OntapMetroclusterOperation",
    model_class=OntapMetroclusterOperation,
    api_endpoint="/cluster/metrocluster/operations?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="additional_info",
        ),
        FieldMapping(
            cache_attr="command_line",
        ),
        FieldMapping(
            cache_attr="end_time",
        ),
        FieldMapping(
            cache_attr="errors",
            default=[],
        ),
        FieldMapping(
            cache_attr="node.name",
        ),
        FieldMapping(
            cache_attr="node.uuid",
        ),
        FieldMapping(
            cache_attr="start_time",
        ),
        FieldMapping(
            cache_attr="state",
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

model_registry.register_mapping("OntapMetroclusterOperation", ONTAPMETROCLUSTEROPERATION_MAPPING)
