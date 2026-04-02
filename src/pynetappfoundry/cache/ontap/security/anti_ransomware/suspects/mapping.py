"""OntapAntiRansomwareSuspect type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.security.anti_ransomware.suspects.model import (
    OntapAntiRansomwareSuspect,
)

ONTAPANTIRANSOMWARESUSPECT_MAPPING = TypeMapping(
    name="OntapAntiRansomwareSuspect",
    model_class=OntapAntiRansomwareSuspect,
    api_endpoint="/security/anti-ransomware/suspects?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="file.format",
            api_path="file.format",
        ),
        FieldMapping(
            cache_attr="file.name",
            api_path="file.name",
        ),
        FieldMapping(
            cache_attr="file.path",
            api_path="file.path",
        ),
        FieldMapping(
            cache_attr="file.reason",
            api_path="file.reason",
        ),
        FieldMapping(
            cache_attr="file.suspect_time",
            api_path="file.suspect_time",
        ),
        FieldMapping(
            cache_attr="volume.name",
            api_path="volume.name",
        ),
        FieldMapping(
            cache_attr="volume.uuid",
            api_path="volume.uuid",
        ),
    ),
)

model_registry.register_mapping("OntapAntiRansomwareSuspect", ONTAPANTIRANSOMWARESUSPECT_MAPPING)
