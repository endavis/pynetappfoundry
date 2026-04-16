"""DiiAssetsZonesZonemember type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.dii.assets.zones.zoneMembers.model import DiiAssetsZonesZonemember

DIIASSETSZONESZONEMEMBER_MAPPING = TypeMapping(
    name="DiiAssetsZonesZonemember",
    model_class=DiiAssetsZonesZonemember,
    api_endpoint="/assets/zones/{id}/zoneMembers",
    api_type="dii",
    records_path="",
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

model_registry.register_mapping("DiiAssetsZonesZonemember", DIIASSETSZONESZONEMEMBER_MAPPING)
