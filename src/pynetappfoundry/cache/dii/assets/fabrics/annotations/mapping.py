"""DiiAssetsFabricsAnnotation type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.dii.assets.fabrics.annotations.model import DiiAssetsFabricsAnnotation

DIIASSETSFABRICSANNOTATION_MAPPING = TypeMapping(
    name="DiiAssetsFabricsAnnotation",
    model_class=DiiAssetsFabricsAnnotation,
    api_endpoint="/assets/fabrics/{id}/annotations",
    api_type="dii",
    records_path="",
    parent_mapping="DiiAssetsFabric",
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

model_registry.register_mapping("DiiAssetsFabricsAnnotation", DIIASSETSFABRICSANNOTATION_MAPPING)
