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
        ),
        FieldMapping(
            cache_attr="file.name",
        ),
        FieldMapping(
            cache_attr="file.path",
        ),
        FieldMapping(
            cache_attr="file.reason",
        ),
        FieldMapping(
            cache_attr="file.suspect_time",
        ),
        FieldMapping(
            cache_attr="volume.name",
        ),
        FieldMapping(
            cache_attr="volume.uuid",
        ),
    ),
)

model_registry.register_mapping("OntapAntiRansomwareSuspect", ONTAPANTIRANSOMWARESUSPECT_MAPPING)
