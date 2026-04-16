"""DiiAssetsFabricsZone type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.dii.assets.fabrics.zones.model import DiiAssetsFabricsZone

DIIASSETSFABRICSZONE_MAPPING = TypeMapping(
    name="DiiAssetsFabricsZone",
    model_class=DiiAssetsFabricsZone,
    api_endpoint="/assets/fabrics/{id}/zones",
    api_type="dii",
    records_path="",
    parent_mapping="DiiAssetsFabric",
    parent_id_field="id",
    fields=(
        FieldMapping(
            cache_attr="simpleName",
        ),
        FieldMapping(
            cache_attr="fabric",
        ),
        FieldMapping(
            cache_attr="zoneMembers",
            default=[],
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
        FieldMapping(
            cache_attr="initiators",
            default=0,
        ),
        FieldMapping(
            cache_attr="type_",
            api_path="type",
        ),
        FieldMapping(
            cache_attr="targets",
            default=0,
        ),
        FieldMapping(
            cache_attr="wwn",
        ),
    ),
)

model_registry.register_mapping("DiiAssetsFabricsZone", DIIASSETSFABRICSZONE_MAPPING)
