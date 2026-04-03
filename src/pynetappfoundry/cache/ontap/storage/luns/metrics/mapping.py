"""OntapPerformanceLunMetricResponse type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.storage.luns.metrics.model import (
    OntapPerformanceLunMetricResponse,
)

ONTAPPERFORMANCELUNMETRICRESPONSE_MAPPING = TypeMapping(
    name="OntapPerformanceLunMetricResponse",
    model_class=OntapPerformanceLunMetricResponse,
    api_endpoint="/storage/luns/{lun.uuid}/metrics?fields=*",
    api_type="ontap",
    parent_mapping="OntapLun",
    parent_id_field="uuid",
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
        FieldMapping(
            cache_attr="uuid",
        ),
    ),
)

model_registry.register_mapping(
    "OntapPerformanceLunMetricResponse", ONTAPPERFORMANCELUNMETRICRESPONSE_MAPPING
)
