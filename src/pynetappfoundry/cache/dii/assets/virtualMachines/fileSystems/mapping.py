"""DiiAssetsVirtualmachinesFilesystem type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.dii.assets.virtualMachines.fileSystems.model import (
    DiiAssetsVirtualmachinesFilesystem,
)

DIIASSETSVIRTUALMACHINESFILESYSTEM_MAPPING = TypeMapping(
    name="DiiAssetsVirtualmachinesFilesystem",
    model_class=DiiAssetsVirtualmachinesFilesystem,
    api_endpoint="/assets/virtualMachines/{id}/fileSystems",
    api_type="dii",
    records_path="",
    parent_mapping="DiiAssetsVirtualmachine",
    parent_id_field="id",
    fields=(
        FieldMapping(
            cache_attr="vmdks",
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
            cache_attr="id",
            default=0,
        ),
        FieldMapping(
            cache_attr="type_",
            api_path="type",
        ),
        FieldMapping(
            cache_attr="computeResource",
        ),
        FieldMapping(
            cache_attr="capacity",
        ),
    ),
)

model_registry.register_mapping(
    "DiiAssetsVirtualmachinesFilesystem", DIIASSETSVIRTUALMACHINESFILESYSTEM_MAPPING
)
