"""OntapSensors type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.cluster.sensors.model import OntapSensors

ONTAPSENSORS_MAPPING = TypeMapping(
    name="OntapSensors",
    model_class=OntapSensors,
    api_endpoint="/cluster/sensors?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="critical_high_threshold",
            default=0,
        ),
        FieldMapping(
            cache_attr="critical_low_threshold",
            default=0,
        ),
        FieldMapping(
            cache_attr="discrete_state",
        ),
        FieldMapping(
            cache_attr="discrete_value",
        ),
        FieldMapping(
            cache_attr="index",
            default=0,
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="node.name",
        ),
        FieldMapping(
            cache_attr="node.uuid",
        ),
        FieldMapping(
            cache_attr="threshold_state",
        ),
        FieldMapping(
            cache_attr="type_",
            api_path="type",
        ),
        FieldMapping(
            cache_attr="value",
            default=0,
        ),
        FieldMapping(
            cache_attr="value_units",
        ),
        FieldMapping(
            cache_attr="warning_high_threshold",
            default=0,
        ),
        FieldMapping(
            cache_attr="warning_low_threshold",
            default=0,
        ),
    ),
)

model_registry.register_mapping("OntapSensors", ONTAPSENSORS_MAPPING)
