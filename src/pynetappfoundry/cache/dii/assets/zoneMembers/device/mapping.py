"""DiiAssetsZonemembersDevice type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.dii.assets.zoneMembers.device.model import DiiAssetsZonemembersDevice

DIIASSETSZONEMEMBERSDEVICE_MAPPING = TypeMapping(
    name="DiiAssetsZonemembersDevice",
    model_class=DiiAssetsZonemembersDevice,
    api_endpoint="/assets/zoneMembers/{id}/device",
    api_type="dii",
    fields=(
        FieldMapping(
            cache_attr="simpleName",
        ),
        FieldMapping(
            cache_attr="ip",
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="description",
        ),
        FieldMapping(
            cache_attr="self",
        ),
        FieldMapping(
            cache_attr="id",
        ),
        FieldMapping(
            cache_attr="type_",
            api_path="type",
        ),
        FieldMapping(
            cache_attr="wwn",
        ),
    ),
)

model_registry.register_mapping("DiiAssetsZonemembersDevice", DIIASSETSZONEMEMBERSDEVICE_MAPPING)
