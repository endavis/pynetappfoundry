"""DiiAssetsStoragesPath type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.dii.assets.storages.paths.model import DiiAssetsStoragesPath

DIIASSETSSTORAGESPATH_MAPPING = TypeMapping(
    name="DiiAssetsStoragesPath",
    model_class=DiiAssetsStoragesPath,
    api_endpoint="/assets/storages/{id}/paths",
    api_type="dii",
    records_path="",
    parent_mapping="DiiAssetsStorage",
    parent_id_field="id",
    fields=(
        FieldMapping(
            cache_attr="hostPortCount",
            default=0,
        ),
        FieldMapping(
            cache_attr="connectionCount",
            default=0,
        ),
        FieldMapping(
            cache_attr="source",
        ),
        FieldMapping(
            cache_attr="isNonRedundant",
            default=False,
        ),
        FieldMapping(
            cache_attr="pathType",
        ),
        FieldMapping(
            cache_attr="target",
        ),
        FieldMapping(
            cache_attr="fabrics",
            default=[],
        ),
        FieldMapping(
            cache_attr="isBackendPath",
            default=False,
        ),
        FieldMapping(
            cache_attr="simpleName",
        ),
        FieldMapping(
            cache_attr="sessionCount",
            default=0,
        ),
        FieldMapping(
            cache_attr="storagePortCount",
            default=0,
        ),
        FieldMapping(
            cache_attr="hopCount",
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="id",
            default=0,
        ),
        FieldMapping(
            cache_attr="since",
        ),
        FieldMapping(
            cache_attr="storagePorts",
            default=[],
        ),
        FieldMapping(
            cache_attr="applications",
            default=[],
        ),
    ),
)

model_registry.register_mapping("DiiAssetsStoragesPath", DIIASSETSSTORAGESPATH_MAPPING)
