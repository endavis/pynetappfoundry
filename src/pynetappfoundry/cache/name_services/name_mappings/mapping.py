"""OntapNameMapping type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.name_services.name_mappings.model import OntapNameMapping

ONTAPNAMEMAPPING_MAPPING = TypeMapping(
    name="OntapNameMapping",
    model_class=OntapNameMapping,
    api_endpoint="/name-services/name-mappings?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="client_match",
            api_path="client_match",
        ),
        FieldMapping(
            cache_attr="direction",
            api_path="direction",
        ),
        FieldMapping(
            cache_attr="index",
            api_path="index",
            default=0,
        ),
        FieldMapping(
            cache_attr="pattern",
            api_path="pattern",
        ),
        FieldMapping(
            cache_attr="replacement",
            api_path="replacement",
        ),
        FieldMapping(
            cache_attr="svm_name",
            api_path="svm.name",
        ),
        FieldMapping(
            cache_attr="svm_uuid",
            api_path="svm.uuid",
        ),
    ),
)

model_registry.register_mapping("OntapNameMapping", ONTAPNAMEMAPPING_MAPPING)
