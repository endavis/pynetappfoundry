"""OntapPerformanceQtreeMetricResponse type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.storage.qtrees.metrics.model import (
    OntapPerformanceQtreeMetricResponse,
)

ONTAPPERFORMANCEQTREEMETRICRESPONSE_MAPPING = TypeMapping(
    name="OntapPerformanceQtreeMetricResponse",
    model_class=OntapPerformanceQtreeMetricResponse,
    api_endpoint="/storage/qtrees/{volume.uuid}/{qtree.id}/metrics?fields=*",
    api_type="ontap",
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
            cache_attr="qtree.id",
            default=0,
        ),
        FieldMapping(
            cache_attr="qtree.name",
        ),
        FieldMapping(
            cache_attr="status",
        ),
        FieldMapping(
            cache_attr="svm.name",
        ),
        FieldMapping(
            cache_attr="svm.uuid",
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
        FieldMapping(
            cache_attr="volume.name",
        ),
        FieldMapping(
            cache_attr="volume.uuid",
        ),
    ),
)

model_registry.register_mapping(
    "OntapPerformanceQtreeMetricResponse", ONTAPPERFORMANCEQTREEMETRICRESPONSE_MAPPING
)
