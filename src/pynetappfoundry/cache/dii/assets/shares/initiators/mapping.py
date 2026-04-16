"""DiiShareinitiator type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.dii.assets.shares.initiators.model import DiiShareinitiator

DIISHAREINITIATOR_MAPPING = TypeMapping(
    name="DiiShareinitiator",
    model_class=DiiShareinitiator,
    api_endpoint="/assets/shares/{id}/initiators",
    api_type="dii",
    fields=(
        FieldMapping(
            cache_attr="initiator",
        ),
        FieldMapping(
            cache_attr="permission",
        ),
    ),
)

model_registry.register_mapping("DiiShareinitiator", DIISHAREINITIATOR_MAPPING)
