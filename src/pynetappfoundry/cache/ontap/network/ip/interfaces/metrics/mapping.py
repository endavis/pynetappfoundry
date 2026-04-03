"""OntapInterfaceMetricsResponse type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.network.ip.interfaces.metrics.model import (
    OntapInterfaceMetricsResponse,
)

ONTAPINTERFACEMETRICSRESPONSE_MAPPING = TypeMapping(
    name="OntapInterfaceMetricsResponse",
    model_class=OntapInterfaceMetricsResponse,
    api_endpoint="/network/ip/interfaces/{uuid}/metrics?fields=*",
    api_type="ontap",
    parent_mapping="OntapIpInterface",
    parent_id_field="uuid",
    fields=(
        FieldMapping(
            cache_attr="duration",
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
    "OntapInterfaceMetricsResponse", ONTAPINTERFACEMETRICSRESPONSE_MAPPING
)
