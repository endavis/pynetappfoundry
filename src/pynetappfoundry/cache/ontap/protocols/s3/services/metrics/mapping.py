"""OntapPerformanceS3MetricResponse type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.ontap.protocols.s3.services.metrics.model import (
    OntapPerformanceS3MetricResponse,
)

ONTAPPERFORMANCES3METRICRESPONSE_MAPPING = TypeMapping(
    name="OntapPerformanceS3MetricResponse",
    model_class=OntapPerformanceS3MetricResponse,
    api_endpoint="/protocols/s3/services/{svm.uuid}/metrics?fields=*",
    api_type="ontap",
    parent_mapping="OntapS3Service",
    parent_id_field="svm_uuid",
    fields=(
        FieldMapping(
            cache_attr="duration",
            api_path="duration",
        ),
        FieldMapping(
            cache_attr="iops_other",
            api_path="iops.other",
            default=0,
        ),
        FieldMapping(
            cache_attr="iops_read",
            api_path="iops.read",
            default=0,
        ),
        FieldMapping(
            cache_attr="iops_total",
            api_path="iops.total",
            default=0,
        ),
        FieldMapping(
            cache_attr="iops_write",
            api_path="iops.write",
            default=0,
        ),
        FieldMapping(
            cache_attr="latency_other",
            api_path="latency.other",
            default=0,
        ),
        FieldMapping(
            cache_attr="latency_read",
            api_path="latency.read",
            default=0,
        ),
        FieldMapping(
            cache_attr="latency_total",
            api_path="latency.total",
            default=0,
        ),
        FieldMapping(
            cache_attr="latency_write",
            api_path="latency.write",
            default=0,
        ),
        FieldMapping(
            cache_attr="status",
            api_path="status",
        ),
        FieldMapping(
            cache_attr="throughput_other",
            api_path="throughput.other",
            default=0,
        ),
        FieldMapping(
            cache_attr="throughput_read",
            api_path="throughput.read",
            default=0,
        ),
        FieldMapping(
            cache_attr="throughput_total",
            api_path="throughput.total",
            default=0,
        ),
        FieldMapping(
            cache_attr="throughput_write",
            api_path="throughput.write",
            default=0,
        ),
        FieldMapping(
            cache_attr="timestamp",
            api_path="timestamp",
        ),
    ),
)

model_registry.register_mapping(
    "OntapPerformanceS3MetricResponse", ONTAPPERFORMANCES3METRICRESPONSE_MAPPING
)
