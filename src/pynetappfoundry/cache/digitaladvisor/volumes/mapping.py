"""DigitalAdvisorVolume type mapping (hand-written, ADR-0037).

The fields come from ``DigitalAdvisorVolume.model_fields``, so the mapping cannot drift
from the model. The backend is live-only: there is no cache table for this mapping.
"""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.digitaladvisor.volume import DigitalAdvisorVolume

DIGITALADVISORVOLUME_MAPPING = TypeMapping(
    name="DigitalAdvisorVolume",
    model_class=DigitalAdvisorVolume,
    api_endpoint="volumes",
    api_type="digitaladvisor",
    records_path="volumes",
    identifier_field="id",
    id_field="name",
    fields=tuple(
        FieldMapping(cache_attr=name, default=None) for name in DigitalAdvisorVolume.model_fields
    ),
)

model_registry.register_mapping("DigitalAdvisorVolume", DIGITALADVISORVOLUME_MAPPING)
