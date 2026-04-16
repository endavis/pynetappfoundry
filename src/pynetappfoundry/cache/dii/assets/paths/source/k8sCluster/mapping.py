"""DiiK8scluster type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.dii.assets.paths.source.k8sCluster.model import DiiK8scluster

DIIK8SCLUSTER_MAPPING = TypeMapping(
    name="DiiK8scluster",
    model_class=DiiK8scluster,
    api_endpoint="/assets/paths/{id}/source/k8sCluster",
    api_type="dii",
    fields=(
        FieldMapping(
            cache_attr="name",
        ),
    ),
)

model_registry.register_mapping("DiiK8scluster", DIIK8SCLUSTER_MAPPING)
