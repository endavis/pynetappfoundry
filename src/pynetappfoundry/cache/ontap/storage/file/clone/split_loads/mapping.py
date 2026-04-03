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
            cache_attr="load.allowable",
            default=0,
        ),
        FieldMapping(
            cache_attr="load.current",
            default=0,
        ),
        FieldMapping(
            cache_attr="load.maximum",
            default=0,
        ),
        FieldMapping(
            cache_attr="load.token_reserved",
            default=0,
        ),
        FieldMapping(
            cache_attr="node.name",
        ),
        FieldMapping(
            cache_attr="node.uuid",
        ),
    ),
)

model_registry.register_mapping("OntapSplitLoad", ONTAPSPLITLOAD_MAPPING)
