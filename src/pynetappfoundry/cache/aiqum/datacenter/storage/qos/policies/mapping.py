"""AiqumQosPolicy type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.aiqum.datacenter.storage.qos.policies.model import AiqumQosPolicy

AIQUMQOSPOLICY_MAPPING = TypeMapping(
    name="AiqumQosPolicy",
    model_class=AiqumQosPolicy,
    api_endpoint="/datacenter/storage/qos/policies",
    api_type="aiqum",
    identifier_field="key",
    fields=(
        FieldMapping(
            cache_attr="adaptive.absolute_min_iops",
            default=0,
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
            cache_attr="fixed.capacity_shared",
            default=False,
        ),
        FieldMapping(
            cache_attr="fixed.max_throughput_iops",
            default=0,
        ),
        FieldMapping(
            cache_attr="fixed.max_throughput_mbps",
            default=0,
        ),
        FieldMapping(
            cache_attr="fixed.min_throughput_iops",
            default=0,
        ),
        FieldMapping(
            cache_attr="key",
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="object_count",
            default=0,
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

model_registry.register_mapping("AiqumQosPolicy", AIQUMQOSPOLICY_MAPPING)
