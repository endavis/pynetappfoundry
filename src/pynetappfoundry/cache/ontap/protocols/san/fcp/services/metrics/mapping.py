"""OntapPerformanceFcpMetricResponse type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.protocols.san.fcp.services.metrics.model import (
    OntapPerformanceFcpMetricResponse,
)

ONTAPPERFORMANCEFCPMETRICRESPONSE_MAPPING = TypeMapping(
    name="OntapPerformanceFcpMetricResponse",
    model_class=OntapPerformanceFcpMetricResponse,
    api_endpoint="/protocols/san/fcp/services/{svm.uuid}/metrics?fields=*",
    api_type="ontap",
    parent_mapping="OntapFcpService",
    parent_id_field="svm.uuid",
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
            cache_attr="svm.uuid",
            api_path="svm.uuid",
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
    ),
)

model_registry.register_mapping(
    "OntapPerformanceFcpMetricResponse", ONTAPPERFORMANCEFCPMETRICRESPONSE_MAPPING
)
