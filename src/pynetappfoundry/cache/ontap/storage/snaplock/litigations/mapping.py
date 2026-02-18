"""OntapSnaplockLitigation type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.ontap.storage.snaplock.litigations.model import OntapSnaplockLitigation

ONTAPSNAPLOCKLITIGATION_MAPPING = TypeMapping(
    name="OntapSnaplockLitigation",
    model_class=OntapSnaplockLitigation,
    api_endpoint="/storage/snaplock/litigations/{id}?fields=*",
    api_type="ontap",
    records_path="operations",
    parent_mapping="OntapStorageSnaplockLitigation",
    parent_id_field="uuid",
    fields=(
        FieldMapping(
            cache_attr="id",
            api_path="id",
            default=0,
        ),
        FieldMapping(
            cache_attr="num_files_failed",
            api_path="num_files_failed",
        ),
        FieldMapping(
            cache_attr="num_files_processed",
            api_path="num_files_processed",
        ),
        FieldMapping(
            cache_attr="num_files_skipped",
            api_path="num_files_skipped",
        ),
        FieldMapping(
            cache_attr="num_inodes_ignored",
            api_path="num_inodes_ignored",
        ),
        FieldMapping(
            cache_attr="path",
            api_path="path",
        ),
        FieldMapping(
            cache_attr="state",
            api_path="state",
        ),
        FieldMapping(
            cache_attr="type_",
            api_path="type",
        ),
    ),
)

model_registry.register_mapping("OntapSnaplockLitigation", ONTAPSNAPLOCKLITIGATION_MAPPING)
