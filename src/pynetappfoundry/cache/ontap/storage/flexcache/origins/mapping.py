"""OntapFlexcacheOrigin type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.ontap.storage.flexcache.origins.model import OntapFlexcacheOrigin

ONTAPFLEXCACHEORIGIN_MAPPING = TypeMapping(
    name="OntapFlexcacheOrigin",
    model_class=OntapFlexcacheOrigin,
    api_endpoint="/storage/flexcache/origins/{uuid}?fields=*",
    api_type="ontap",
    records_path="flexcaches",
    parent_mapping="OntapStorageFlexcacheOrigin",
    parent_id_field="uuid",
    fields=(
        FieldMapping(
            cache_attr="cluster_name",
            api_path="cluster.name",
        ),
        FieldMapping(
            cache_attr="cluster_uuid",
            api_path="cluster.uuid",
        ),
        FieldMapping(
            cache_attr="create_time",
            api_path="create_time",
        ),
        FieldMapping(
            cache_attr="ip_address",
            api_path="ip_address",
        ),
        FieldMapping(
            cache_attr="size",
            api_path="size",
            default=0,
        ),
        FieldMapping(
            cache_attr="state",
            api_path="state",
        ),
        FieldMapping(
            cache_attr="svm_name",
            api_path="svm.name",
        ),
        FieldMapping(
            cache_attr="svm_uuid",
            api_path="svm.uuid",
        ),
        FieldMapping(
            cache_attr="volume_name",
            api_path="volume.name",
        ),
        FieldMapping(
            cache_attr="volume_uuid",
            api_path="volume.uuid",
        ),
    ),
)

model_registry.register_mapping("OntapFlexcacheOrigin", ONTAPFLEXCACHEORIGIN_MAPPING)
