"""DiiAssetsVirtualmachinesApplication type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.dii.assets.virtualMachines.applications.model import (
    DiiAssetsVirtualmachinesApplication,
)

DIIASSETSVIRTUALMACHINESAPPLICATION_MAPPING = TypeMapping(
    name="DiiAssetsVirtualmachinesApplication",
    model_class=DiiAssetsVirtualmachinesApplication,
    api_endpoint="/assets/virtualMachines/{id}/applications",
    api_type="dii",
    records_path="",
    parent_mapping="DiiAssetsVirtualmachine",
    parent_id_field="id",
    fields=(
        FieldMapping(
            cache_attr="shares",
            default=[],
        ),
        FieldMapping(
            cache_attr="performance",
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
            cache_attr="computeResources",
            default=[],
        ),
        FieldMapping(
            cache_attr="id",
            default=0,
        ),
        FieldMapping(
            cache_attr="priority",
        ),
        FieldMapping(
            cache_attr="ignoreShareViolations",
            default=False,
        ),
        FieldMapping(
            cache_attr="qtrees",
            default=[],
        ),
    ),
)

model_registry.register_mapping(
    "DiiAssetsVirtualmachinesApplication", DIIASSETSVIRTUALMACHINESAPPLICATION_MAPPING
)
