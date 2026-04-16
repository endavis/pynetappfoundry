"""DiiAssetsSwitchesApplication type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.dii.assets.switches.applications.model import (
    DiiAssetsSwitchesApplication,
)

DIIASSETSSWITCHESAPPLICATION_MAPPING = TypeMapping(
    name="DiiAssetsSwitchesApplication",
    model_class=DiiAssetsSwitchesApplication,
    api_endpoint="/assets/switches/{id}/applications",
    api_type="dii",
    records_path="",
    parent_mapping="DiiAssetsSwitche",
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
    "DiiAssetsSwitchesApplication", DIIASSETSSWITCHESAPPLICATION_MAPPING
)
