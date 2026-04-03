"""OntapQosPolicy type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.storage.qos.policies.model import OntapQosPolicy

ONTAPQOSPOLICY_MAPPING = TypeMapping(
    name="OntapQosPolicy",
    model_class=OntapQosPolicy,
    api_endpoint="/storage/qos/policies?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="adaptive.absolute_min_iops",
            default=0,
        ),
        FieldMapping(
            cache_attr="adaptive.block_size",
        ),
        FieldMapping(
            cache_attr="adaptive.expected_iops",
            default=0,
        ),
        FieldMapping(
            cache_attr="adaptive.expected_iops_allocation",
        ),
        FieldMapping(
            cache_attr="adaptive.peak_iops",
            default=0,
        ),
        FieldMapping(
            cache_attr="adaptive.peak_iops_allocation",
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
            cache_attr="fixed.min_throughput_mbps",
            default=0,
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="object_count",
            default=0,
        ),
        FieldMapping(
            cache_attr="pgid",
            default=0,
        ),
        FieldMapping(
            cache_attr="policy_class",
        ),
        FieldMapping(
            cache_attr="scope",
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

model_registry.register_mapping("OntapQosPolicy", ONTAPQOSPOLICY_MAPPING)
