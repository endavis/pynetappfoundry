"""OntapResourceTagResource type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.resource_tags.resources.model import OntapResourceTagResource

ONTAPRESOURCETAGRESOURCE_MAPPING = TypeMapping(
    name="OntapResourceTagResource",
    model_class=OntapResourceTagResource,
    api_endpoint="/resource-tags/{resource_tag.value}/resources?fields=*",
    api_type="ontap",
    parent_mapping="OntapResourceTag",
    parent_id_field="value",
    fields=(
        FieldMapping(
            cache_attr="href",
        ),
        FieldMapping(
            cache_attr="label",
        ),
        FieldMapping(
            cache_attr="svm.name",
        ),
        FieldMapping(
            cache_attr="svm.uuid",
        ),
        FieldMapping(
            cache_attr="value",
        ),
    ),
)

model_registry.register_mapping("OntapResourceTagResource", ONTAPRESOURCETAGRESOURCE_MAPPING)
