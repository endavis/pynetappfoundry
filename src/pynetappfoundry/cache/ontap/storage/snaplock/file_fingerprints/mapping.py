"""OntapSnaplockFileFingerprint type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.storage.snaplock.file_fingerprints.model import (
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
        ),
        FieldMapping(
            cache_attr="data_fingerprint",
        ),
        FieldMapping(
            cache_attr="file_size",
            default=0,
        ),
        FieldMapping(
            cache_attr="file_type",
        ),
        FieldMapping(
            cache_attr="id",
            default=0,
        ),
        FieldMapping(
            cache_attr="metadata_fingerprint",
        ),
        FieldMapping(
            cache_attr="path",
        ),
        FieldMapping(
            cache_attr="scope",
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

model_registry.register_mapping(
    "OntapSnaplockFileFingerprint", ONTAPSNAPLOCKFILEFINGERPRINT_MAPPING
)
