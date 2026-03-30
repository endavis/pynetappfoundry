"""OntapQosOption type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.storage.qos.qos_options.model import OntapQosOption

ONTAPQOSOPTION_MAPPING = TypeMapping(
    name="OntapQosOption",
    model_class=OntapQosOption,
    api_endpoint="/storage/qos/qos-options?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="background_task_reserve",
            api_path="background_task_reserve",
            default=0,
        ),
    ),
)

model_registry.register_mapping("OntapQosOption", ONTAPQOSOPTION_MAPPING)
