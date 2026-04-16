"""DiiAssetsVolumesVirtualstorageresource type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.dii.assets.volumes.virtualStorageResources.model import (
    DiiAssetsVolumesVirtualstorageresource,
)

DIIASSETSVOLUMESVIRTUALSTORAGERESOURCE_MAPPING = TypeMapping(
    name="DiiAssetsVolumesVirtualstorageresource",
    model_class=DiiAssetsVolumesVirtualstorageresource,
    api_endpoint="/assets/volumes/{id}/virtualStorageResources",
    api_type="dii",
    records_path="",
    fields=(
        FieldMapping(
            cache_attr="dataStores",
            default=[],
        ),
        FieldMapping(
            cache_attr="performance",
        ),
        FieldMapping(
            cache_attr="storagePools",
            default=[],
        ),
        FieldMapping(
            cache_attr="simpleName",
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="computeResources",
            default=[],
        ),
        FieldMapping(
            cache_attr="isThinProvisioned",
            default=False,
        ),
        FieldMapping(
            cache_attr="id",
            default=0,
        ),
        FieldMapping(
            cache_attr="storage",
        ),
        FieldMapping(
            cache_attr="capacity",
        ),
        FieldMapping(
            cache_attr="resourceType",
        ),
        FieldMapping(
            cache_attr="applications",
            default=[],
        ),
    ),
)

model_registry.register_mapping(
    "DiiAssetsVolumesVirtualstorageresource", DIIASSETSVOLUMESVIRTUALSTORAGERESOURCE_MAPPING
)
