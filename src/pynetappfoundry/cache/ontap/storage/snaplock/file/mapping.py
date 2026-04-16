"""OntapSnaplockFileRetention type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.storage.snaplock.file.model import OntapSnaplockFileRetention

ONTAPSNAPLOCKFILERETENTION_MAPPING = TypeMapping(
    name="OntapSnaplockFileRetention",
    model_class=OntapSnaplockFileRetention,
    api_endpoint="/storage/snaplock/file/{volume.uuid}/{path}?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="expiry_time",
        ),
        FieldMapping(
            cache_attr="file_path",
        ),
        FieldMapping(
            cache_attr="is_expired",
            default=False,
        ),
        FieldMapping(
            cache_attr="retention_period",
        ),
        FieldMapping(
            cache_attr="seconds_until_expiry",
            default=0,
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

model_registry.register_mapping("OntapSnaplockFileRetention", ONTAPSNAPLOCKFILERETENTION_MAPPING)
