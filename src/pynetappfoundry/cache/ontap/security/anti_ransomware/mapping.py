"""OntapAntiRansomware type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.security.anti_ransomware.model import OntapAntiRansomware

ONTAPANTIRANSOMWARE_MAPPING = TypeMapping(
    name="OntapAntiRansomware",
    model_class=OntapAntiRansomware,
    api_endpoint="/security/anti-ransomware?fields=*",
    api_type="ontap",
    records_path="nodes",
    fields=(
        FieldMapping(
            cache_attr="name",
            api_path="name",
        ),
        FieldMapping(
            cache_attr="version",
            api_path="version",
        ),
    ),
)

model_registry.register_mapping("OntapAntiRansomware", ONTAPANTIRANSOMWARE_MAPPING)
