"""OntapLunAttribute type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.ontap.storage.luns.attributes.model import OntapLunAttribute

ONTAPLUNATTRIBUTE_MAPPING = TypeMapping(
    name="OntapLunAttribute",
    model_class=OntapLunAttribute,
    api_endpoint="/storage/luns/{lun.uuid}/attributes?fields=*",
    api_type="ontap",
    parent_mapping="OntapLun",
    parent_id_field="uuid",
    fields=(
        FieldMapping(
            cache_attr="lun_uuid",
            api_path="lun.uuid",
        ),
        FieldMapping(
            cache_attr="name",
            api_path="name",
        ),
        FieldMapping(
            cache_attr="value",
            api_path="value",
        ),
    ),
)

model_registry.register_mapping("OntapLunAttribute", ONTAPLUNATTRIBUTE_MAPPING)
