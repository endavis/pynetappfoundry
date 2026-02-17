"""OntapToken type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.storage.file.clone.tokens.model import OntapToken

ONTAPTOKEN_MAPPING = TypeMapping(
    name="OntapToken",
    model_class=OntapToken,
    api_endpoint="/storage/file/clone/tokens?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="expiry_time_left",
            api_path="expiry_time.left",
        ),
        FieldMapping(
            cache_attr="expiry_time_limit",
            api_path="expiry_time.limit",
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
            cache_attr="reserve_size",
            api_path="reserve_size",
            default=0,
        ),
        FieldMapping(
            cache_attr="uuid",
            api_path="uuid",
        ),
    ),
)

model_registry.register_mapping("OntapToken", ONTAPTOKEN_MAPPING)
