"""OntapPerformanceNamespaceMetricResponse type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.storage.namespaces.metrics.model import (
    OntapPerformanceNamespaceMetricResponse,
)

ONTAPPERFORMANCENAMESPACEMETRICRESPONSE_MAPPING = TypeMapping(
    name="OntapPerformanceNamespaceMetricResponse",
    model_class=OntapPerformanceNamespaceMetricResponse,
    api_endpoint="/storage/namespaces/{nvme_namespace.uuid}/metrics?fields=*",
    api_type="ontap",
    parent_mapping="OntapNvmeNamespace",
    parent_id_field="uuid",
    fields=(
        FieldMapping(
            cache_attr="duration",
            api_path="duration",
        ),
        FieldMapping(
            cache_attr="iops.other",
            api_path="iops.other",
            default=0,
        ),
        FieldMapping(
            cache_attr="iops.read",
            api_path="iops.read",
            default=0,
        ),
        FieldMapping(
            cache_attr="iops.total",
            api_path="iops.total",
            default=0,
        ),
        FieldMapping(
            cache_attr="iops.write",
            api_path="iops.write",
            default=0,
        ),
        FieldMapping(
            cache_attr="latency.other",
            api_path="latency.other",
            default=0,
        ),
        FieldMapping(
            cache_attr="latency.read",
            api_path="latency.read",
            default=0,
        ),
        FieldMapping(
            cache_attr="latency.total",
            api_path="latency.total",
            default=0,
        ),
        FieldMapping(
            cache_attr="latency.write",
            api_path="latency.write",
            default=0,
        ),
        FieldMapping(
            cache_attr="status",
            api_path="status",
        ),
        FieldMapping(
            cache_attr="throughput.read",
            api_path="throughput.read",
            default=0,
        ),
        FieldMapping(
            cache_attr="throughput.total",
            api_path="throughput.total",
            default=0,
        ),
        FieldMapping(
            cache_attr="throughput.write",
            api_path="throughput.write",
            default=0,
        ),
        FieldMapping(
            cache_attr="timestamp",
            api_path="timestamp",
        ),
        FieldMapping(
            cache_attr="uuid",
            api_path="uuid",
        ),
    ),
)

model_registry.register_mapping(
    "OntapPerformanceNamespaceMetricResponse", ONTAPPERFORMANCENAMESPACEMETRICRESPONSE_MAPPING
)
