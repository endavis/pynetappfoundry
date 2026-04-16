"""DiiK8spv type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.dii.assets.paths.source.k8sPv.model import DiiK8spv

DIIK8SPV_MAPPING = TypeMapping(
    name="DiiK8spv",
    model_class=DiiK8spv,
    api_endpoint="/assets/paths/{id}/source/k8sPv",
    api_type="dii",
    fields=(
        FieldMapping(
            cache_attr="phase",
        ),
        FieldMapping(
            cache_attr="capacity_bytes",
            default=0.0,
        ),
        FieldMapping(
            cache_attr="pv_type",
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="kubernetes_cluster",
        ),
        FieldMapping(
            cache_attr="storageclass",
        ),
    ),
)

model_registry.register_mapping("DiiK8spv", DIIK8SPV_MAPPING)
