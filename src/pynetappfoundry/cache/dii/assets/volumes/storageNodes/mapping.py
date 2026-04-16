"""DiiAssetsVolumesStoragenode type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.dii.assets.volumes.storageNodes.model import DiiAssetsVolumesStoragenode

DIIASSETSVOLUMESSTORAGENODE_MAPPING = TypeMapping(
    name="DiiAssetsVolumesStoragenode",
    model_class=DiiAssetsVolumesStoragenode,
    api_endpoint="/assets/volumes/{id}/storageNodes",
    api_type="dii",
    records_path="",
    fields=(
        FieldMapping(
            cache_attr="cache",
        ),
        FieldMapping(
            cache_attr="internalVolumes",
            default=[],
        ),
        FieldMapping(
            cache_attr="serialNumber",
        ),
        FieldMapping(
            cache_attr="memory",
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
            cache_attr="nodeVersion",
        ),
        FieldMapping(
            cache_attr="storage",
        ),
        FieldMapping(
            cache_attr="monitoring",
        ),
        FieldMapping(
            cache_attr="ports",
            default=[],
        ),
        FieldMapping(
            cache_attr="uuid",
        ),
        FieldMapping(
            cache_attr="performance",
        ),
        FieldMapping(
            cache_attr="numberOfProcessors",
            default=0,
        ),
        FieldMapping(
            cache_attr="risks",
            default=[],
        ),
        FieldMapping(
            cache_attr="partner",
        ),
        FieldMapping(
            cache_attr="datasources",
            default=[],
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
            cache_attr="model_",
            api_path="model",
        ),
        FieldMapping(
            cache_attr="id",
            default=0,
        ),
        FieldMapping(
            cache_attr="state",
        ),
    ),
)

model_registry.register_mapping("DiiAssetsVolumesStoragenode", DIIASSETSVOLUMESSTORAGENODE_MAPPING)
