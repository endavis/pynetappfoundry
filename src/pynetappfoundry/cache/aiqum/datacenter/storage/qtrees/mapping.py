"""AiqumQtree type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.aiqum.datacenter.storage.qtrees.model import AiqumQtree

AIQUMQTREE_MAPPING = TypeMapping(
    name="AiqumQtree",
    model_class=AiqumQtree,
    api_endpoint="/datacenter/storage/qtrees",
    api_type="aiqum",
    identifier_field="key",
    fields=(
        FieldMapping(
            cache_attr="cluster.key",
        ),
        FieldMapping(
            cache_attr="cluster.name",
        ),
        FieldMapping(
            cache_attr="cluster.uuid",
        ),
        FieldMapping(
            cache_attr="export_policy.id",
            default=0,
        ),
        FieldMapping(
            cache_attr="export_policy.key",
        ),
        FieldMapping(
            cache_attr="export_policy.name",
        ),
        FieldMapping(
            cache_attr="id",
            default=0,
        ),
        FieldMapping(
            cache_attr="key",
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="security_style",
        ),
        FieldMapping(
            cache_attr="svm.key",
        ),
        FieldMapping(
            cache_attr="svm.name",
        ),
        FieldMapping(
            cache_attr="svm.uuid",
        ),
        FieldMapping(
            cache_attr="volume.key",
        ),
        FieldMapping(
            cache_attr="volume.name",
        ),
        FieldMapping(
            cache_attr="volume.uuid",
        ),
    ),
)

model_registry.register_mapping("AiqumQtree", AIQUMQTREE_MAPPING)
