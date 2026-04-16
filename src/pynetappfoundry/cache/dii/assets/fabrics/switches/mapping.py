"""DiiAssetsFabricsSwitche type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.dii.assets.fabrics.switches.model import DiiAssetsFabricsSwitche

DIIASSETSFABRICSSWITCHE_MAPPING = TypeMapping(
    name="DiiAssetsFabricsSwitche",
    model_class=DiiAssetsFabricsSwitche,
    api_endpoint="/assets/fabrics/{id}/switches",
    api_type="dii",
    records_path="",
    parent_mapping="DiiAssetsFabric",
    parent_id_field="id",
    fields=(
        FieldMapping(
            cache_attr="isSanRouteEnabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="switchRole",
        ),
        FieldMapping(
            cache_attr="switchType",
        ),
        FieldMapping(
            cache_attr="annotations",
            default=[],
        ),
        FieldMapping(
            cache_attr="switchStatus",
        ),
        FieldMapping(
            cache_attr="isActive",
            default=False,
        ),
        FieldMapping(
            cache_attr="ports",
            default=[],
        ),
        FieldMapping(
            cache_attr="wwn",
        ),
        FieldMapping(
            cache_attr="vendor",
        ),
        FieldMapping(
            cache_attr="isNpv",
            default=False,
        ),
        FieldMapping(
            cache_attr="model_",
            api_path="model",
        ),
        FieldMapping(
            cache_attr="managementUrl",
        ),
        FieldMapping(
            cache_attr="id",
            default=0,
        ),
        FieldMapping(
            cache_attr="domainIdType",
        ),
        FieldMapping(
            cache_attr="firmware",
        ),
        FieldMapping(
            cache_attr="serialNumber",
        ),
        FieldMapping(
            cache_attr="ip",
        ),
        FieldMapping(
            cache_attr="priority",
        ),
        FieldMapping(
            cache_attr="zones",
            default=[],
        ),
        FieldMapping(
            cache_attr="domainId",
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
            cache_attr="createTime",
        ),
        FieldMapping(
            cache_attr="fabric",
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="isVsanEnabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="applications",
            default=[],
        ),
    ),
)

model_registry.register_mapping("DiiAssetsFabricsSwitche", DIIASSETSFABRICSSWITCHE_MAPPING)
