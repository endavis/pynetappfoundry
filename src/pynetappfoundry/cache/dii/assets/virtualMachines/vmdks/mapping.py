"""DiiAssetsVirtualmachinesVmdk type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.dii.assets.virtualMachines.vmdks.model import (
    DiiAssetsVirtualmachinesVmdk,
)

DIIASSETSVIRTUALMACHINESVMDK_MAPPING = TypeMapping(
    name="DiiAssetsVirtualmachinesVmdk",
    model_class=DiiAssetsVirtualmachinesVmdk,
    api_endpoint="/assets/virtualMachines/{id}/vmdks",
    api_type="dii",
    records_path="",
    parent_mapping="DiiAssetsVirtualmachine",
    parent_id_field="id",
    fields=(
        FieldMapping(
            cache_attr="virtualMachine",
        ),
        FieldMapping(
            cache_attr="performance",
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
            cache_attr="storageResources",
            default=[],
        ),
        FieldMapping(
            cache_attr="dataStore",
        ),
        FieldMapping(
            cache_attr="annotations",
            default=[],
        ),
        FieldMapping(
            cache_attr="id",
            default=0,
        ),
        FieldMapping(
            cache_attr="isRdm",
            default=False,
        ),
        FieldMapping(
            cache_attr="type_",
            api_path="type",
        ),
        FieldMapping(
            cache_attr="capacity",
        ),
    ),
)

model_registry.register_mapping(
    "DiiAssetsVirtualmachinesVmdk", DIIASSETSVIRTUALMACHINESVMDK_MAPPING
)
