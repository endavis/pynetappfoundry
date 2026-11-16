"""AiqumSvmAnalytics type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.aiqum.datacenter.svm.svms.analytics.model import AiqumSvmAnalytics

AIQUMSVMANALYTICS_MAPPING = TypeMapping(
    name="AiqumSvmAnalytics",
    model_class=AiqumSvmAnalytics,
    api_endpoint="/datacenter/svm/svms/analytics",
    api_type="aiqum",
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
            cache_attr="iops",
            default=0.0,
        ),
        FieldMapping(
            cache_attr="latency",
            default=0.0,
        ),
        FieldMapping(
            cache_attr="period",
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
            cache_attr="throughput",
            default=0.0,
        ),
    ),
)

model_registry.register_mapping("AiqumSvmAnalytics", AIQUMSVMANALYTICS_MAPPING)
