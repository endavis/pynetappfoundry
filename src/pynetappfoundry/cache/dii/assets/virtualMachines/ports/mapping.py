"""DiiAssetsVirtualmachinesPort type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.dii.assets.virtualMachines.ports.model import (
    DiiAssetsVirtualmachinesPort,
)

DIIASSETSVIRTUALMACHINESPORT_MAPPING = TypeMapping(
    name="DiiAssetsVirtualmachinesPort",
    model_class=DiiAssetsVirtualmachinesPort,
    api_endpoint="/assets/virtualMachines/{id}/ports",
    api_type="dii",
    records_path="",
    parent_mapping="DiiAssetsVirtualmachine",
    parent_id_field="id",
    fields=(
        FieldMapping(
            cache_attr="role",
        ),
        FieldMapping(
            cache_attr="portState",
        ),
        FieldMapping(
            cache_attr="annotations",
            default=[],
        ),
        FieldMapping(
            cache_attr="type_",
            api_path="type",
        ),
        FieldMapping(
            cache_attr="gbicType",
        ),
        FieldMapping(
            cache_attr="isActive",
            default=False,
        ),
        FieldMapping(
            cache_attr="deviceName",
        ),
        FieldMapping(
            cache_attr="speed",
            default=0,
        ),
        FieldMapping(
            cache_attr="wwn",
        ),
        FieldMapping(
            cache_attr="blade",
            default=0,
        ),
        FieldMapping(
            cache_attr="portIndex",
            default=0,
        ),
        FieldMapping(
            cache_attr="id",
            default=0,
        ),
        FieldMapping(
            cache_attr="fc4Protocol",
        ),
        FieldMapping(
            cache_attr="deviceType",
        ),
        FieldMapping(
            cache_attr="classOfService",
        ),
        FieldMapping(
            cache_attr="controller",
        ),
        FieldMapping(
            cache_attr="nodeWwn",
        ),
        FieldMapping(
            cache_attr="fabrics",
            default=[],
        ),
        FieldMapping(
            cache_attr="performance",
        ),
        FieldMapping(
            cache_attr="connectedPorts",
            default=[],
        ),
        FieldMapping(
            cache_attr="datasources",
            default=[],
        ),
        FieldMapping(
            cache_attr="simpleName",
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="device",
        ),
        FieldMapping(
            cache_attr="applications",
            default=[],
        ),
    ),
)

model_registry.register_mapping(
    "DiiAssetsVirtualmachinesPort", DIIASSETSVIRTUALMACHINESPORT_MAPPING
)
