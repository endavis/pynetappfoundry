"""DiiAssetsSwitchesAnnotation type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.dii.assets.switches.annotations.model import DiiAssetsSwitchesAnnotation

DIIASSETSSWITCHESANNOTATION_MAPPING = TypeMapping(
    name="DiiAssetsSwitchesAnnotation",
    model_class=DiiAssetsSwitchesAnnotation,
    api_endpoint="/assets/switches/{id}/annotations",
    api_type="dii",
    records_path="",
    parent_mapping="DiiAssetsSwitche",
    parent_id_field="id",
    fields=(
        FieldMapping(
            cache_attr="displayValue",
        ),
        FieldMapping(
            cache_attr="rawValue",
        ),
        FieldMapping(
            cache_attr="definition",
        ),
        FieldMapping(
            cache_attr="label",
        ),
        FieldMapping(
            cache_attr="annotationAssignment",
        ),
    ),
)

model_registry.register_mapping("DiiAssetsSwitchesAnnotation", DIIASSETSSWITCHESANNOTATION_MAPPING)
