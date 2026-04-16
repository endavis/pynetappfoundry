"""DiiAssetsStoragevirtualmachinesQtree type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.dii.assets.storageVirtualMachines.qtrees.model import (
    DiiAssetsStoragevirtualmachinesQtree,
)

DIIASSETSSTORAGEVIRTUALMACHINESQTREE_MAPPING = TypeMapping(
    name="DiiAssetsStoragevirtualmachinesQtree",
    model_class=DiiAssetsStoragevirtualmachinesQtree,
    api_endpoint="/assets/storageVirtualMachines/{id}/qtrees",
    api_type="dii",
    records_path="",
    fields=(
        FieldMapping(
            cache_attr="sourceReplica",
        ),
        FieldMapping(
            cache_attr="quotas",
            default=[],
        ),
        FieldMapping(
            cache_attr="quotaCapacity",
        ),
        FieldMapping(
            cache_attr="volumes",
            default=[],
        ),
        FieldMapping(
            cache_attr="annotations",
            default=[],
        ),
        FieldMapping(
            cache_attr="storage",
        ),
        FieldMapping(
            cache_attr="internalVolume",
        ),
        FieldMapping(
            cache_attr="type_",
            api_path="type",
        ),
        FieldMapping(
            cache_attr="securityStyle",
        ),
        FieldMapping(
            cache_attr="isOplocksEnabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="shares",
            default=[],
        ),
        FieldMapping(
            cache_attr="storageVirtualMachine",
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
            cache_attr="statusText",
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="id",
            default=0,
        ),
        FieldMapping(
            cache_attr="applications",
            default=[],
        ),
    ),
)

model_registry.register_mapping(
    "DiiAssetsStoragevirtualmachinesQtree", DIIASSETSSTORAGEVIRTUALMACHINESQTREE_MAPPING
)
