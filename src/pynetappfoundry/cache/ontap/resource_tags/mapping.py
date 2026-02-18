"""OntapResourceTag type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.ontap.resource_tags.model import OntapResourceTag

ONTAPRESOURCETAG_MAPPING = TypeMapping(
    name="OntapResourceTag",
    model_class=OntapResourceTag,
    api_endpoint="/resource-tags?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="num_resources",
            api_path="num_resources",
            default=0,
        ),
        FieldMapping(
            cache_attr="value",
            api_path="value",
        ),
    ),
)

model_registry.register_mapping("OntapResourceTag", ONTAPRESOURCETAG_MAPPING)
