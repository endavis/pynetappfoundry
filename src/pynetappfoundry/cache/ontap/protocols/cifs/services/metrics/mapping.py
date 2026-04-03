"""OntapPerformanceCifsMetricResponse type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.protocols.cifs.services.metrics.model import (
    OntapPerformanceCifsMetricResponse,
)

ONTAPPERFORMANCECIFSMETRICRESPONSE_MAPPING = TypeMapping(
    name="OntapPerformanceCifsMetricResponse",
    model_class=OntapPerformanceCifsMetricResponse,
    api_endpoint="/protocols/cifs/services/{svm.uuid}/metrics?fields=*",
    api_type="ontap",
    parent_mapping="OntapCifsService",
    parent_id_field="svm.uuid",
    fields=(
        FieldMapping(
            cache_attr="duration",
        ),
        FieldMapping(
            cache_attr="iops.other",
            default=0,
        ),
        FieldMapping(
            cache_attr="iops.read",
            default=0,
        ),
        FieldMapping(
            cache_attr="iops.total",
            default=0,
        ),
        FieldMapping(
            cache_attr="iops.write",
            default=0,
        ),
        FieldMapping(
            cache_attr="latency.other",
            default=0,
        ),
        FieldMapping(
            cache_attr="latency.read",
            default=0,
        ),
        FieldMapping(
            cache_attr="latency.total",
            default=0,
        ),
        FieldMapping(
            cache_attr="latency.write",
            default=0,
        ),
        FieldMapping(
            cache_attr="status",
        ),
        FieldMapping(
            cache_attr="throughput.other",
            default=0,
        ),
        FieldMapping(
            cache_attr="throughput.read",
            default=0,
        ),
        FieldMapping(
            cache_attr="throughput.total",
            default=0,
        ),
        FieldMapping(
            cache_attr="throughput.write",
            default=0,
        ),
        FieldMapping(
            cache_attr="timestamp",
        ),
    ),
)

model_registry.register_mapping(
    "OntapPerformanceCifsMetricResponse", ONTAPPERFORMANCECIFSMETRICRESPONSE_MAPPING
)
