"""DiiZonemember type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.dii.assets.zoneMembers.model import DiiZonemember

DIIZONEMEMBER_MAPPING = TypeMapping(
    name="DiiZonemember",
    model_class=DiiZonemember,
    api_endpoint="/assets/zoneMembers/{id}",
    api_type="dii",
    fields=(
        FieldMapping(
            cache_attr="simpleName",
        ),
        FieldMapping(
            cache_attr="zone",
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="id",
            default=0,
        ),
        FieldMapping(
            cache_attr="zoneStatus",
        ),
        FieldMapping(
            cache_attr="type_",
            api_path="type",
        ),
        FieldMapping(
            cache_attr="device",
        ),
        FieldMapping(
            cache_attr="wwn",
        ),
    ),
)

model_registry.register_mapping("DiiZonemember", DIIZONEMEMBER_MAPPING)
