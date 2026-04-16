"""DiiAssetsApplicationsComputeresource type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.dii.assets.applications.computeResources.model import (
    DiiAssetsApplicationsComputeresource,
)

DIIASSETSAPPLICATIONSCOMPUTERESOURCE_MAPPING = TypeMapping(
    name="DiiAssetsApplicationsComputeresource",
    model_class=DiiAssetsApplicationsComputeresource,
    api_endpoint="/assets/applications/{id}/computeResources",
    api_type="dii",
    records_path="",
    parent_mapping="DiiAssetsApplication",
    parent_id_field="id",
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
    "DiiAssetsApplicationsComputeresource", DIIASSETSAPPLICATIONSCOMPUTERESOURCE_MAPPING
)
