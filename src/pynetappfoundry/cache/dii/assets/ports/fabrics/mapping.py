"""DiiAssetsPortsFabric type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.dii.assets.ports.fabrics.model import DiiAssetsPortsFabric

DIIASSETSPORTSFABRIC_MAPPING = TypeMapping(
    name="DiiAssetsPortsFabric",
    model_class=DiiAssetsPortsFabric,
    api_endpoint="/assets/ports/{id}/fabrics",
    api_type="dii",
    records_path="",
    fields=(
        FieldMapping(
            cache_attr="switchesCount",
            default=0,
        ),
        FieldMapping(
            cache_attr="activeZoneSet",
        ),
        FieldMapping(
            cache_attr="switches",
            default=[],
        ),
        FieldMapping(
            cache_attr="annotations",
            default=[],
        ),
        FieldMapping(
            cache_attr="isZoningEnabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="isActive",
            default=False,
        ),
        FieldMapping(
            cache_attr="zonesCount",
            default=0,
        ),
        FieldMapping(
            cache_attr="zones",
            default=[],
        ),
        FieldMapping(
            cache_attr="ports",
            default=[],
        ),
        FieldMapping(
            cache_attr="wwn",
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
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="isVsanEnabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="id",
            default=0,
        ),
        FieldMapping(
            cache_attr="vsanId",
        ),
    ),
)

model_registry.register_mapping("DiiAssetsPortsFabric", DIIASSETSPORTSFABRIC_MAPPING)
