"""OntapSnaplockFileFingerprint type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.ontap.storage.snaplock.file_fingerprints.model import (
    OntapSnaplockFileFingerprint,
)

ONTAPSNAPLOCKFILEFINGERPRINT_MAPPING = TypeMapping(
    name="OntapSnaplockFileFingerprint",
    model_class=OntapSnaplockFileFingerprint,
    api_endpoint="/storage/snaplock/file-fingerprints/{id}?fields=*",
    api_type="ontap",
    parent_mapping=None,
    parent_id_field=None,
    fields=(
        FieldMapping(
            cache_attr="algorithm",
            api_path="algorithm",
        ),
        FieldMapping(
            cache_attr="data_fingerprint",
            api_path="data_fingerprint",
        ),
        FieldMapping(
            cache_attr="file_size",
            api_path="file_size",
            default=0,
        ),
        FieldMapping(
            cache_attr="file_type",
            api_path="file_type",
        ),
        FieldMapping(
            cache_attr="id",
            api_path="id",
            default=0,
        ),
        FieldMapping(
            cache_attr="metadata_fingerprint",
            api_path="metadata_fingerprint",
        ),
        FieldMapping(
            cache_attr="path",
            api_path="path",
        ),
        FieldMapping(
            cache_attr="scope",
            api_path="scope",
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

model_registry.register_mapping(
    "OntapSnaplockFileFingerprint", ONTAPSNAPLOCKFILEFINGERPRINT_MAPPING
)
