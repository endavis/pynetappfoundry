"""DiiAssetsApplicationsAsset type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.dii.assets.applications.assets.model import DiiAssetsApplicationsAsset

DIIASSETSAPPLICATIONSASSET_MAPPING = TypeMapping(
    name="DiiAssetsApplicationsAsset",
    model_class=DiiAssetsApplicationsAsset,
    api_endpoint="/assets/applications/{id}/assets",
    api_type="dii",
    records_path="",
    parent_mapping="DiiAssetsApplication",
    parent_id_field="id",
    fields=(
        FieldMapping(
            cache_attr="simpleName",
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="id",
            default=0,
        ),
    ),
)

model_registry.register_mapping("DiiAssetsApplicationsAsset", DIIASSETSAPPLICATIONSASSET_MAPPING)
