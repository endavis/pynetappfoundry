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
    api_endpoint="/storage/snaplock/file-fingerprints?fields=*",
    api_type="ontap",
    identifier_field="id",
    fields=(
        FieldMapping(
            cache_attr="id",
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

model_registry.register_mapping(
    "OntapSnaplockFileFingerprint", ONTAPSNAPLOCKFILEFINGERPRINT_MAPPING
)
