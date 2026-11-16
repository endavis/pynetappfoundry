"""AiqumLun type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.aiqum.datacenter.storage.luns.model import AiqumLun, AiqumLunLunMap

AIQUMLUN_MAPPING = TypeMapping(
    name="AiqumLun",
    model_class=AiqumLun,
    api_endpoint="/datacenter/storage/luns",
    api_type="aiqum",
    identifier_field="key",
    fields=(
        FieldMapping(
            cache_attr="class_",
            api_path="class",
        ),
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
            cache_attr="comment",
        ),
        FieldMapping(
            cache_attr="key",
        ),
        FieldMapping(
            cache_attr="location.qtree.id",
        ),
        FieldMapping(
            cache_attr="location.qtree.key",
        ),
        FieldMapping(
            cache_attr="location.qtree.name",
        ),
        FieldMapping(
            cache_attr="location.volume.key",
        ),
        FieldMapping(
            cache_attr="location.volume.name",
        ),
        FieldMapping(
            cache_attr="location.volume.uuid",
        ),
        FieldMapping(
            cache_attr="lun_maps",
            item_model=AiqumLunLunMap,
            default=[],
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="os_type",
        ),
        FieldMapping(
            cache_attr="qos_policy.key",
        ),
        FieldMapping(
            cache_attr="qos_policy.name",
        ),
        FieldMapping(
            cache_attr="qos_policy.uuid",
        ),
        FieldMapping(
            cache_attr="serial_number",
        ),
        FieldMapping(
            cache_attr="space.size",
            default=0,
        ),
        FieldMapping(
            cache_attr="space.used",
            default=0,
        ),
        FieldMapping(
            cache_attr="status.mapped",
            default=False,
        ),
        FieldMapping(
            cache_attr="status.state",
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
            cache_attr="uuid",
        ),
    ),
)

model_registry.register_mapping("AiqumLun", AIQUMLUN_MAPPING)
