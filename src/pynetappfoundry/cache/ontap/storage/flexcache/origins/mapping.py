"""OntapFlexcacheOrigin type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.storage.flexcache.origins.model import OntapFlexcacheOrigin

ONTAPFLEXCACHEORIGIN_MAPPING = TypeMapping(
    name="OntapFlexcacheOrigin",
    model_class=OntapFlexcacheOrigin,
    api_endpoint="/storage/flexcache/origins/{uuid}?fields=*",
    api_type="ontap",
    records_path="flexcaches",
    fields=(
        FieldMapping(
            cache_attr="cluster.name",
        ),
        FieldMapping(
            cache_attr="cluster.uuid",
        ),
        FieldMapping(
            cache_attr="create_time",
        ),
        FieldMapping(
            cache_attr="ip_address",
        ),
        FieldMapping(
            cache_attr="size",
            default=0,
        ),
        FieldMapping(
            cache_attr="state",
        ),
        FieldMapping(
            cache_attr="svm.name",
        ),
        FieldMapping(
            cache_attr="svm.uuid",
        ),
        FieldMapping(
            cache_attr="volume.name",
        ),
        FieldMapping(
            cache_attr="volume.uuid",
        ),
    ),
)

model_registry.register_mapping("OntapFlexcacheOrigin", ONTAPFLEXCACHEORIGIN_MAPPING)
