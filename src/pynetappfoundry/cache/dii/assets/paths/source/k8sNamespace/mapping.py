"""DiiK8snamespace type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.dii.assets.paths.source.k8sNamespace.model import DiiK8snamespace

DIIK8SNAMESPACE_MAPPING = TypeMapping(
    name="DiiK8snamespace",
    model_class=DiiK8snamespace,
    api_endpoint="/assets/paths/{id}/source/k8sNamespace",
    api_type="dii",
    fields=(
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="kubernetes_cluster",
        ),
    ),
)

model_registry.register_mapping("DiiK8snamespace", DIIK8SNAMESPACE_MAPPING)
