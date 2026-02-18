"""OntapSnaplockFileRetention type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.ontap.storage.snaplock.file.model import OntapSnaplockFileRetention

ONTAPSNAPLOCKFILERETENTION_MAPPING = TypeMapping(
    name="OntapSnaplockFileRetention",
    model_class=OntapSnaplockFileRetention,
    api_endpoint="/storage/snaplock/file/{volume.uuid}/{path}?fields=*",
    api_type="ontap",
    parent_mapping="OntapStorageSnaplockFile",
    parent_id_field="uuid",
    fields=(
        FieldMapping(
            cache_attr="expiry_time",
            api_path="expiry_time",
        ),
        FieldMapping(
            cache_attr="file_path",
            api_path="file_path",
        ),
        FieldMapping(
            cache_attr="is_expired",
            api_path="is_expired",
            default=False,
        ),
        FieldMapping(
            cache_attr="retention_period",
            api_path="retention_period",
        ),
        FieldMapping(
            cache_attr="seconds_until_expiry",
            api_path="seconds_until_expiry",
            default=0,
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

model_registry.register_mapping("OntapSnaplockFileRetention", ONTAPSNAPLOCKFILERETENTION_MAPPING)
