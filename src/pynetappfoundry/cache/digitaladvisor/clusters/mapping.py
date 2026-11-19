"""DigitalAdvisorCluster type mapping (hand-written, ADR-0037).

The fields come from ``DigitalAdvisorCluster.model_fields``, so the mapping cannot drift
from the model. The backend is live-only: there is no cache table for this mapping.
"""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.digitaladvisor.cluster import DigitalAdvisorCluster

DIGITALADVISORCLUSTER_MAPPING = TypeMapping(
    name="DigitalAdvisorCluster",
    model_class=DigitalAdvisorCluster,
    api_endpoint="clusters",
    api_type="digitaladvisor",
    records_path="clusters",
    identifier_field="id",
    id_field="name",
    fields=tuple(
        FieldMapping(cache_attr=name, default=None) for name in DigitalAdvisorCluster.model_fields
    ),
)

model_registry.register_mapping("DigitalAdvisorCluster", DIGITALADVISORCLUSTER_MAPPING)
