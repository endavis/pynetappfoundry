"""OntapFlexcacheOrigin type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.storage.flexcache.origins.model import (
    OntapFlexcacheOrigin,
    OntapFlexcacheOriginFlexcache,
)

ONTAPFLEXCACHEORIGIN_MAPPING = TypeMapping(
    name="OntapFlexcacheOrigin",
    model_class=OntapFlexcacheOrigin,
    api_endpoint="/storage/flexcache/origins?fields=*",
    api_type="ontap",
    identifier_field="uuid",
    fields=(
        FieldMapping(
            cache_attr="block_level_invalidation",
            default=False,
        ),
        FieldMapping(
            cache_attr="flexcaches",
            item_model=OntapFlexcacheOriginFlexcache,
            default=[],
        ),
        FieldMapping(
            cache_attr="global_file_locking_enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="svm.name",
        ),
        FieldMapping(
            cache_attr="svm.uuid",
        ),
        FieldMapping(
            cache_attr="uuid",
        ),
    ),
)

model_registry.register_mapping("OntapFlexcacheOrigin", ONTAPFLEXCACHEORIGIN_MAPPING)
