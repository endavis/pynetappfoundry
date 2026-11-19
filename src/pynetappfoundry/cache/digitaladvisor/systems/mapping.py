"""DigitalAdvisorSystem type mapping (hand-written, ADR-0037).

The fields come from ``DigitalAdvisorSystem.model_fields``, so the mapping cannot drift
from the model. The backend is live-only: there is no cache table for this mapping.
"""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.digitaladvisor.system import DigitalAdvisorSystem

DIGITALADVISORSYSTEM_MAPPING = TypeMapping(
    name="DigitalAdvisorSystem",
    model_class=DigitalAdvisorSystem,
    api_endpoint="systems",
    api_type="digitaladvisor",
    records_path="systems",
    identifier_field="serialNumber",
    id_field="hostName",
    fields=tuple(
        FieldMapping(cache_attr=name, default=None) for name in DigitalAdvisorSystem.model_fields
    ),
)

model_registry.register_mapping("DigitalAdvisorSystem", DIGITALADVISORSYSTEM_MAPPING)
