"""OntapSensors type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.cluster.sensors.model import OntapSensors
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping

ONTAPSENSORS_MAPPING = TypeMapping(
    name="OntapSensors",
    model_class=OntapSensors,
    api_endpoint="/cluster/sensors?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="critical_high_threshold",
            api_path="critical_high_threshold",
            default=0,
        ),
        FieldMapping(
            cache_attr="critical_low_threshold",
            api_path="critical_low_threshold",
            default=0,
        ),
        FieldMapping(
            cache_attr="discrete_state",
            api_path="discrete_state",
        ),
        FieldMapping(
            cache_attr="discrete_value",
            api_path="discrete_value",
        ),
        FieldMapping(
            cache_attr="index",
            api_path="index",
            default=0,
        ),
        FieldMapping(
            cache_attr="name",
            api_path="name",
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
            cache_attr="threshold_state",
            api_path="threshold_state",
        ),
        FieldMapping(
            cache_attr="type_",
            api_path="type",
        ),
        FieldMapping(
            cache_attr="value",
            api_path="value",
            default=0,
        ),
        FieldMapping(
            cache_attr="value_units",
            api_path="value_units",
        ),
        FieldMapping(
            cache_attr="warning_high_threshold",
            api_path="warning_high_threshold",
            default=0,
        ),
        FieldMapping(
            cache_attr="warning_low_threshold",
            api_path="warning_low_threshold",
            default=0,
        ),
    ),
)

model_registry.register_mapping("OntapSensors", ONTAPSENSORS_MAPPING)
