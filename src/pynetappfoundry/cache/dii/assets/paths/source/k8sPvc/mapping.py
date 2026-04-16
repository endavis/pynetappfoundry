"""DiiK8spvc type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.dii.assets.paths.source.k8sPvc.model import DiiK8spvc

DIIK8SPVC_MAPPING = TypeMapping(
    name="DiiK8spvc",
    model_class=DiiK8spvc,
    api_endpoint="/assets/paths/{id}/source/k8sPvc",
    api_type="dii",
    fields=(
        FieldMapping(
            cache_attr="namespace",
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="kubernetes_cluster",
        ),
    ),
)

model_registry.register_mapping("DiiK8spvc", DIIK8SPVC_MAPPING)
