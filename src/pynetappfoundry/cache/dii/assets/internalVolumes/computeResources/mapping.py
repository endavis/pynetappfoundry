"""DiiAssetsInternalvolumesComputeresource type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.dii.assets.internalVolumes.computeResources.model import (
    DiiAssetsInternalvolumesComputeresource,
)

DIIASSETSINTERNALVOLUMESCOMPUTERESOURCE_MAPPING = TypeMapping(
    name="DiiAssetsInternalvolumesComputeresource",
    model_class=DiiAssetsInternalvolumesComputeresource,
    api_endpoint="/assets/internalVolumes/{id}/computeResources",
    api_type="dii",
    records_path="",
    fields=(
        FieldMapping(
            cache_attr="performance",
        ),
        FieldMapping(
            cache_attr="simpleName",
        ),
        FieldMapping(
            cache_attr="fileSystems",
            default=[],
        ),
        FieldMapping(
            cache_attr="paths",
            default=[],
        ),
        FieldMapping(
            cache_attr="ip",
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
            cache_attr="ports",
            default=[],
        ),
        FieldMapping(
            cache_attr="resourceType",
        ),
    ),
)

model_registry.register_mapping(
    "DiiAssetsInternalvolumesComputeresource", DIIASSETSINTERNALVOLUMESCOMPUTERESOURCE_MAPPING
)
