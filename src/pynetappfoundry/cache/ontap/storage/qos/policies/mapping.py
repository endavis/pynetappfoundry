"""OntapQosPolicy type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.ontap.storage.qos.policies.model import OntapQosPolicy

ONTAPQOSPOLICY_MAPPING = TypeMapping(
    name="OntapQosPolicy",
    model_class=OntapQosPolicy,
    api_endpoint="/storage/qos/policies?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="adaptive_absolute_min_iops",
            api_path="adaptive.absolute_min_iops",
            default=0,
        ),
        FieldMapping(
            cache_attr="adaptive_block_size",
            api_path="adaptive.block_size",
        ),
        FieldMapping(
            cache_attr="adaptive_expected_iops",
            api_path="adaptive.expected_iops",
            default=0,
        ),
        FieldMapping(
            cache_attr="adaptive_expected_iops_allocation",
            api_path="adaptive.expected_iops_allocation",
        ),
        FieldMapping(
            cache_attr="adaptive_peak_iops",
            api_path="adaptive.peak_iops",
            default=0,
        ),
        FieldMapping(
            cache_attr="adaptive_peak_iops_allocation",
            api_path="adaptive.peak_iops_allocation",
        ),
        FieldMapping(
            cache_attr="fixed_capacity_shared",
            api_path="fixed.capacity_shared",
            default=False,
        ),
        FieldMapping(
            cache_attr="fixed_max_throughput_iops",
            api_path="fixed.max_throughput_iops",
            default=0,
        ),
        FieldMapping(
            cache_attr="fixed_max_throughput_mbps",
            api_path="fixed.max_throughput_mbps",
            default=0,
        ),
        FieldMapping(
            cache_attr="fixed_min_throughput_iops",
            api_path="fixed.min_throughput_iops",
            default=0,
        ),
        FieldMapping(
            cache_attr="fixed_min_throughput_mbps",
            api_path="fixed.min_throughput_mbps",
            default=0,
        ),
        FieldMapping(
            cache_attr="name",
            api_path="name",
        ),
        FieldMapping(
            cache_attr="object_count",
            api_path="object_count",
            default=0,
        ),
        FieldMapping(
            cache_attr="pgid",
            api_path="pgid",
            default=0,
        ),
        FieldMapping(
            cache_attr="policy_class",
            api_path="policy_class",
        ),
        FieldMapping(
            cache_attr="scope",
            api_path="scope",
        ),
        FieldMapping(
            cache_attr="svm_name",
            api_path="svm.name",
        ),
        FieldMapping(
            cache_attr="svm_uuid",
            api_path="svm.uuid",
        ),
        FieldMapping(
            cache_attr="uuid",
            api_path="uuid",
        ),
    ),
)

model_registry.register_mapping("OntapQosPolicy", ONTAPQOSPOLICY_MAPPING)
