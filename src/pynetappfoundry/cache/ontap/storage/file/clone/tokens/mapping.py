"""OntapToken type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.storage.file.clone.tokens.model import OntapToken

ONTAPTOKEN_MAPPING = TypeMapping(
    name="OntapToken",
    model_class=OntapToken,
    api_endpoint="/storage/file/clone/tokens?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="expiry_time.left",
        ),
        FieldMapping(
            cache_attr="expiry_time.limit",
        ),
        FieldMapping(
            cache_attr="node.name",
        ),
        FieldMapping(
            cache_attr="node.uuid",
        ),
        FieldMapping(
            cache_attr="reserve_size",
            default=0,
        ),
        FieldMapping(
            cache_attr="uuid",
        ),
    ),
)

model_registry.register_mapping("OntapToken", ONTAPTOKEN_MAPPING)
