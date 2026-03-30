"""OntapSplitLoad type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.storage.file.clone.split_loads.model import OntapSplitLoad

ONTAPSPLITLOAD_MAPPING = TypeMapping(
    name="OntapSplitLoad",
    model_class=OntapSplitLoad,
    api_endpoint="/storage/file/clone/split-loads?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="load_allowable",
            api_path="load.allowable",
            default=0,
        ),
        FieldMapping(
            cache_attr="load_current",
            api_path="load.current",
            default=0,
        ),
        FieldMapping(
            cache_attr="load_maximum",
            api_path="load.maximum",
            default=0,
        ),
        FieldMapping(
            cache_attr="load_token_reserved",
            api_path="load.token_reserved",
            default=0,
        ),
        FieldMapping(
            cache_attr="node_name",
            api_path="node.name",
        ),
        FieldMapping(
            cache_attr="node_uuid",
            api_path="node.uuid",
        ),
    ),
)

model_registry.register_mapping("OntapSplitLoad", ONTAPSPLITLOAD_MAPPING)
