"""DiiAssetsVirtualmachinesZone type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.dii.assets.virtualMachines.zones.model import (
    DiiAssetsVirtualmachinesZone,
)

DIIASSETSVIRTUALMACHINESZONE_MAPPING = TypeMapping(
    name="DiiAssetsVirtualmachinesZone",
    model_class=DiiAssetsVirtualmachinesZone,
    api_endpoint="/assets/virtualMachines/{id}/zones",
    api_type="dii",
    records_path="",
    parent_mapping="DiiAssetsVirtualmachine",
    parent_id_field="id",
    fields=(
        FieldMapping(
            cache_attr="simpleName",
        ),
        FieldMapping(
            cache_attr="fabric",
        ),
        FieldMapping(
            cache_attr="zoneMembers",
            default=[],
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="isVsanEnabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="id",
            default=0,
        ),
        FieldMapping(
            cache_attr="vsanId",
        ),
        FieldMapping(
            cache_attr="initiators",
            default=0,
        ),
        FieldMapping(
            cache_attr="type_",
            api_path="type",
        ),
        FieldMapping(
            cache_attr="targets",
            default=0,
        ),
        FieldMapping(
            cache_attr="wwn",
        ),
    ),
)

model_registry.register_mapping(
    "DiiAssetsVirtualmachinesZone", DIIASSETSVIRTUALMACHINESZONE_MAPPING
)
