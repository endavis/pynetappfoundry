"""OntapPerformanceFcPortMetricResponse type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.network.fc.ports.metrics.model import (
    OntapPerformanceFcPortMetricResponse,
)

ONTAPPERFORMANCEFCPORTMETRICRESPONSE_MAPPING = TypeMapping(
    name="OntapPerformanceFcPortMetricResponse",
    model_class=OntapPerformanceFcPortMetricResponse,
    api_endpoint="/network/fc/ports/{fc_port.uuid}/metrics?fields=*",
    api_type="ontap",
    parent_mapping="OntapFcPort",
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
    "OntapPerformanceFcPortMetricResponse", ONTAPPERFORMANCEFCPORTMETRICRESPONSE_MAPPING
)
