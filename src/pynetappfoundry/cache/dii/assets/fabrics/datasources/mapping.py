"""DiiAssetsFabricsDatasource type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.dii.assets.fabrics.datasources.model import DiiAssetsFabricsDatasource

DIIASSETSFABRICSDATASOURCE_MAPPING = TypeMapping(
    name="DiiAssetsFabricsDatasource",
    model_class=DiiAssetsFabricsDatasource,
    api_endpoint="/assets/fabrics/{id}/datasources",
    api_type="dii",
    records_path="",
    parent_mapping="DiiAssetsFabric",
    parent_id_field="id",
    fields=(
        FieldMapping(
            cache_attr="vendorModelId",
            default=0,
        ),
        FieldMapping(
            cache_attr="note",
        ),
        FieldMapping(
            cache_attr="docLink",
        ),
        FieldMapping(
            cache_attr="devices",
            default=[],
        ),
        FieldMapping(
            cache_attr="changeResponses",
            default=[],
        ),
        FieldMapping(
            cache_attr="packages",
            default=[],
        ),
        FieldMapping(
            cache_attr="lastSuccessfullyAcquired",
        ),
        FieldMapping(
            cache_attr="resumeTime",
        ),
        FieldMapping(
            cache_attr="pollStatus",
        ),
        FieldMapping(
            cache_attr="dsTypeId",
            default=0,
        ),
        FieldMapping(
            cache_attr="acquisitionUnit",
        ),
        FieldMapping(
            cache_attr="vendor",
        ),
        FieldMapping(
            cache_attr="statusText",
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="activePatch",
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
            cache_attr="config_",
            api_path="config",
        ),
        FieldMapping(
            cache_attr="events",
            default=[],
        ),
        FieldMapping(
            cache_attr="status",
        ),
    ),
)

model_registry.register_mapping("DiiAssetsFabricsDatasource", DIIASSETSFABRICSDATASOURCE_MAPPING)
