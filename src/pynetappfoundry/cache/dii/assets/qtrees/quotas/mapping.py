"""DiiAssetsQtreesQuota type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.dii.assets.qtrees.quotas.model import DiiAssetsQtreesQuota

DIIASSETSQTREESQUOTA_MAPPING = TypeMapping(
    name="DiiAssetsQtreesQuota",
    model_class=DiiAssetsQtreesQuota,
    api_endpoint="/assets/qtrees/{id}/quotas",
    api_type="dii",
    records_path="",
    fields=(
        FieldMapping(
            cache_attr="softFileLimit",
            default=0.0,
        ),
        FieldMapping(
            cache_attr="qtree",
        ),
        FieldMapping(
            cache_attr="simpleName",
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="usedFiles",
            default=0.0,
        ),
        FieldMapping(
            cache_attr="annotations",
            default=[],
        ),
        FieldMapping(
            cache_attr="hardFileLimit",
            default=0.0,
        ),
        FieldMapping(
            cache_attr="id",
            default=0,
        ),
        FieldMapping(
            cache_attr="internalVolume",
        ),
        FieldMapping(
            cache_attr="type_",
            api_path="type",
        ),
        FieldMapping(
            cache_attr="userOrGroupTarget",
        ),
        FieldMapping(
            cache_attr="capacity",
        ),
    ),
)

model_registry.register_mapping("DiiAssetsQtreesQuota", DIIASSETSQTREESQUOTA_MAPPING)
